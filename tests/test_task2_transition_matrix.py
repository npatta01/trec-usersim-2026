"""Synthetic coverage for observed HTTP200 transitions and ambiguous responses."""

import copy
import unittest
from test_task2_debug_runner import start_body, scenario
from usersim.task2.protocol import validate_continue_response, build_continue_payload


class TransitionMatrix(unittest.TestCase):
    def test_200_new_empty_scenario_closes_user_or_server_turn(self):
        for final in (False, True):
            for history in (False, True):
                with self.subTest(final=final, history=history):
                    body = {
                        "conversation_id": "c2",
                        "scenario": scenario(),
                        "utterance": None,
                    }
                    if history:
                        body["chat_messages"] = []
                    result = validate_continue_response(
                        200,
                        body,
                        start_body(),
                        build_continue_payload("r", "c1", "Thanks", final),
                    )
                    self.assertEqual(result["kind"], "new_conversation")
                    self.assertEqual(result["item"]["chat_messages"], [])

    def test_ambiguous_200_never_advances(self):
        base = {"conversation_id": "c2", "scenario": scenario(), "utterance": None}
        variants = []
        b = copy.deepcopy(base)
        b["conversation_id"] = "c1"
        variants.append(b)
        b = copy.deepcopy(base)
        b.pop("utterance")
        variants.append(b)
        b = copy.deepcopy(base)
        b["chat_messages"] = [{"participant_name": "user", "text": "old"}]
        variants.append(b)
        b = copy.deepcopy(base)
        b["utterance"] = {
            "participant_name": "agent",
            "text": "unexpected",
            "conversation_id": "c2",
        }
        variants.append(b)
        b = copy.deepcopy(base)
        b["scenario"] = None
        variants.append(b)
        for body in variants:
            with self.subTest(body=body), self.assertRaises(ValueError):
                validate_continue_response(
                    200,
                    body,
                    start_body(),
                    build_continue_payload("r", "c1", "Thanks", True),
                )

    def test_full_lifecycle_with_200_transition_and_cached_completion(self):
        import tempfile
        from pathlib import Path
        from usersim.task2.debug import Task2DebugRunner

        responses = [
            (200, start_body()),
            (
                200,
                {
                    "conversation_id": "c2",
                    "scenario": scenario("new goal"),
                    "utterance": None,
                },
            ),
            (428, {"detail": "Run was finished!"}),
        ]
        requests = []

        def organizer(path, payload):
            requests.append(payload)
            return responses.pop(0)

        def model(request):
            content = (
                '{"text":"Thanks, goodbye.","is_final":true}'
                if request.get("response_format")
                else "Thanks, goodbye."
            )
            return 200, {
                "choices": [{"finish_reason": "stop", "message": {"content": content}}],
                "usage": {"cost": 0.001},
            }

        with tempfile.TemporaryDirectory() as td:
            runner = Task2DebugRunner(
                Path(td),
                run_id="r",
                organizer_post=organizer,
                model_post=model,
                source_files=[],
            )
            result = runner.run()
            self.assertEqual(result["completed_conversations"], 2)
            self.assertEqual(result["user_stops"], 2)
            self.assertEqual(result["status"], "complete")
            self.assertEqual(
                [r["user_utterance"]["conversation_id"] for r in requests[1:]],
                ["c1", "c2"],
            )
            self.assertEqual(runner.run(), result)
            self.assertEqual(len(requests), 3)

    def test_failure_refreshes_totals_without_advancing_or_clearing_pending(self):
        import tempfile, json
        from pathlib import Path
        from unittest.mock import patch
        from usersim.task2.debug import Task2DebugRunner

        with tempfile.TemporaryDirectory() as td:
            r = Task2DebugRunner(
                Path(td),
                run_id="r",
                organizer_post=None,
                model_post=None,
                source_files=[],
            )
            state = r._load_state()
            state.update(status="running", total_user_turns=4)
            r._save_state(state)
            r.pending_path.write_text("{}")
            totals = {"spent_usd": 0.03, "reserved_usd": 0.05, "model_calls": 10}
            with patch.object(r.model, "totals", return_value=totals):
                r.record_failure()
            actual = json.loads(r.state_path.read_text())
            self.assertEqual(actual["status"], "halted")
            self.assertEqual(actual["total_user_turns"], 4)
            self.assertEqual(actual["model_calls"], 10)
            self.assertTrue(r.pending_path.exists())
