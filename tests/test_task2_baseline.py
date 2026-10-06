import copy
import json
import unittest
from usersim.task2.core import Conversation, Turn, parse_turn, rollout
from usersim.task2.generator import generate_turn

SCENARIO = {
    "goal": {"context": "Need Latin letters", "topic": "Transcribed Latin letters"},
    "persona": {},
    "persona_goal_interaction": {},
}


class CoreTests(unittest.TestCase):
    def test_strict_turn_contract(self):
        self.assertEqual(
            parse_turn('{"text":"Thanks, that is enough.","is_final":true}'),
            Turn("Thanks, that is enough.", True),
        )
        for obj in [
            {"text": "", "is_final": True},
            {"text": "x", "is_final": "false"},
            {"text": "x"},
            {"text": "x", "is_final": False, "reason": "hidden"},
            {"text": "<think>x", "is_final": False},
        ]:
            with self.subTest(obj=obj), self.assertRaises(ValueError):
                parse_turn(json.dumps(obj))

    def test_history_roundtrip_and_reset(self):
        original = copy.deepcopy(SCENARIO)
        c = Conversation.start("one", original)
        original["goal"]["topic"] = "mutated"
        c = c.append_user(Turn("Need text", False)).append_agent("Only scans")
        self.assertEqual(
            [m["participant_name"] for m in c.item()["chat_messages"]],
            ["user", "agent"],
        )
        self.assertEqual(
            c.item()["scenario"]["goal"]["topic"], "Transcribed Latin letters"
        )
        other = Conversation.start(
            "two", {"goal": {"context": "NEW", "topic": "NEW"}, "persona": {}}
        )
        self.assertNotIn("Need text", str(other.item()))
        self.assertEqual(other.history, ())

    def test_stop_blocks_new_turns(self):
        c = Conversation.start("one", SCENARIO).append_user(Turn("Enough", True))
        with self.assertRaises(ValueError):
            c.append_agent("More?")
        with self.assertRaises(ValueError):
            c.append_user(Turn("Again", False))

    def test_turn_order(self):
        c = Conversation.start("one", SCENARIO)
        with self.assertRaises(ValueError):
            c.append_agent("Unsolicited")
        c = c.append_user(Turn("Hello", False))
        with self.assertRaises(ValueError):
            c.append_user(Turn("Duplicate", False))

    def test_rollout_uses_own_generated_history_and_stops(self):
        seen = []
        answers = []

        def gen(c):
            seen.append(c.item())
            return Turn(
                "Need letters" if len(seen) == 1 else "Thanks enough", len(seen) == 2
            )

        def agent(c):
            answers.append(c.history[-1][1])
            return "Here are letters"

        result = rollout(Conversation.start("one", SCENARIO), gen, agent, max_turns=4)
        self.assertEqual(result["termination"], "user_stop")
        self.assertEqual(answers, ["Need letters"])
        self.assertEqual(seen[1]["chat_messages"][0]["text"], "Need letters")

    def test_cutoff_is_not_user_stop(self):
        result = rollout(
            Conversation.start("one", SCENARIO),
            lambda c: Turn("More", False),
            lambda c: "Still none",
            max_turns=2,
        )
        self.assertEqual(result["termination"], "safety_cutoff")
        self.assertFalse(result["conversation"].stopped)


class GeneratorTests(unittest.TestCase):
    def test_editor_cannot_change_stop_boolean(self):
        calls = []

        def call(stage, request):
            calls.append((stage, request))
            return (
                '{"text":"Thanks, enough.","is_final":true}'
                if stage == "draft"
                else "Thank you, that is enough."
            )

        turn = generate_turn(Conversation.start("one", SCENARIO), call)
        self.assertTrue(turn.is_final)
        self.assertEqual(turn.text, "Thank you, that is enough.")
        payload = json.loads(calls[1][1]["messages"][1]["content"])
        self.assertTrue(payload["fixed_is_final"])
        self.assertNotIn("Return JSON", str(payload["original_request_messages"]))

    def test_opt_out_one_call_and_role_mapping(self):
        calls = []
        c = (
            Conversation.start("one", SCENARIO)
            .append_user(Turn("Need text", False))
            .append_agent("Only scans")
        )

        def call(stage, req):
            calls.append(req)
            return '{"text":"Any text versions?","is_final":false}'

        generate_turn(c, call, style_postedit=False)
        self.assertEqual(len(calls), 1)
        self.assertEqual(
            calls[0]["messages"][-2:],
            [
                {"role": "assistant", "content": "Need text"},
                {"role": "user", "content": "Only scans"},
            ],
        )

    def test_invalid_draft_blocks_editor(self):
        stages = []

        def call(stage, req):
            stages.append(stage)
            return '{"text":"x","is_final":"yes"}'

        with self.assertRaises(ValueError):
            generate_turn(Conversation.start("one", SCENARIO), call)
        self.assertEqual(stages, ["draft"])


class EditorGuardTests(unittest.TestCase):
    def test_empty_edit_stops_generation(self):
        def call(stage, req):
            return (
                '{"text":"Thanks, enough.","is_final":true}' if stage == "draft" else ""
            )

        with self.assertRaises(ValueError):
            generate_turn(Conversation.start("one", SCENARIO), call)

    def test_no_model_call_after_stop(self):
        c = Conversation.start("one", SCENARIO).append_user(Turn("Enough", True))
        with self.assertRaises(ValueError):
            generate_turn(c, lambda *args: self.fail("Called after stop"))
