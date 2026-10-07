import copy
import hashlib
import json
import unittest

from usersim.prompts import build_messages, editor_messages


def _item(chat_messages):
    return {
        "conversation_id": "c1",
        "scenario": {
            "goal": {
                "context": "Context",
                "topic": "Topic",
                "discipline": "Discipline",
            },
            "persona": {
                "general_info": {"age": "35"},
                "experience_with_ai": {"trust": "cautious"},
                "individual_traits": {"interaction_style": "concise"},
            },
            "persona_goal_interaction": {
                "domain_familiarity": "moderate",
                "known_datasets": ["Known"],
            },
        },
        "chat_messages": chat_messages,
        "future_target": "DO NOT LEAK",
    }


def _request_digest(messages):
    payload = json.dumps(messages, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(payload.encode()).hexdigest()


class ResearcherTailTests(unittest.TestCase):
    def test_single_researcher_message_is_retained_without_fake_reply(self):
        item = _item(
            [
                {
                    "participant_name": "user",
                    "text": "My current researcher request.",
                    "annotations": {"private_future_label": "DO NOT LEAK"},
                }
            ]
        )
        before = copy.deepcopy(item)

        messages = build_messages(item)

        self.assertEqual(item, before)
        self.assertEqual(
            messages[1:],
            [{"role": "assistant", "content": "My current researcher request."}],
        )
        self.assertNotIn("Please start the conversation", json.dumps(messages))
        self.assertNotIn("DO NOT LEAK", json.dumps(messages))
        self.assertNotIn(
            "reacting to the latest search-assistant reply", messages[0]["content"]
        )
        self.assertIn(
            "assistant-role messages are your past researcher utterances",
            messages[0]["content"],
        )
        self.assertIn("Continue as the researcher from the supplied prefix", messages[0]["content"])
        self.assertIn("Do not invent an intervening search-assistant reply", messages[0]["content"])

    def test_multiturn_researcher_tail_maps_every_message_once(self):
        item = _item(
            [
                {"participant_name": "user", "text": "Researcher first."},
                {"participant_name": "agent", "text": "Search assistant reply."},
                {"participant_name": "user", "text": "Researcher latest."},
            ]
        )

        messages = build_messages(item)

        self.assertEqual(
            messages[1:],
            [
                {"role": "assistant", "content": "Researcher first."},
                {"role": "user", "content": "Search assistant reply."},
                {"role": "assistant", "content": "Researcher latest."},
            ],
        )
        payload = json.loads(editor_messages(messages, "Draft")[1]["content"])
        self.assertEqual(
            payload["researcher_last_two_messages"],
            ["Researcher first.", "Researcher latest."],
        )

    def test_empty_and_agent_ending_requests_remain_byte_exact(self):
        empty = build_messages(_item([]))
        agent_ending = build_messages(
            _item(
                [
                    {"participant_name": "user", "text": "Researcher asks."},
                    {"participant_name": "agent", "text": "Search reply."},
                ]
            )
        )

        self.assertEqual(
            _request_digest(empty),
            "cbd2509939e640fdfe4ebbe51cf7c5d95d841fc265eb7254f1b75a3d0577366e",
        )
        self.assertEqual(
            _request_digest(agent_ending),
            "cd2d94616ead37fcfd83fc3767e5a3824613555d7bb471c523bc4506f7d7bda9",
        )


if __name__ == "__main__":
    unittest.main()
