import copy
import json
import unittest

from usersim.prompts import EDITOR, editor_messages


ORIGINAL = [
    {"role": "system", "content": "persona and goal"},
    {"role": "assistant", "content": "researcher first"},
    {"role": "user", "content": "search assistant first"},
    {"role": "assistant", "content": "researcher second"},
    {"role": "user", "content": "search assistant second"},
    {"role": "assistant", "content": "researcher third"},
    {"role": "user", "content": "search assistant latest"},
]


class EditorPolicyTests(unittest.TestCase):
    def test_default_and_explicit_style_preserve_historical_payload(self):
        draft = "candidate response"
        expected = [
            {"role": "system", "content": EDITOR},
            {
                "role": "user",
                "content": json.dumps(
                    {
                        "original_request_messages": ORIGINAL,
                        "researcher_last_two_messages": [
                            "researcher second",
                            "researcher third",
                        ],
                        "draft": draft,
                    },
                    ensure_ascii=False,
                ),
            },
        ]

        self.assertEqual(editor_messages(ORIGINAL, draft), expected)
        self.assertEqual(editor_messages(ORIGINAL, draft, policy="style"), expected)

    def test_fidelity_retains_full_input_and_draft_without_mutation(self):
        original = copy.deepcopy(ORIGINAL)
        before = copy.deepcopy(original)
        draft = "I already downloaded the files and can waive the date range."

        messages = editor_messages(original, draft, policy="fidelity")

        self.assertEqual(original, before)
        self.assertEqual(messages[0]["role"], "system")
        self.assertNotEqual(messages[0]["content"], EDITOR)
        payload = json.loads(messages[1]["content"])
        self.assertEqual(payload["original_request_messages"], before)
        self.assertEqual(payload["draft"], draft)

    def test_recent_researcher_subset_uses_actual_mapped_roles(self):
        messages = editor_messages(ORIGINAL, "draft", policy="fidelity")
        payload = json.loads(messages[1]["content"])

        self.assertEqual(
            payload["researcher_last_two_messages"],
            ["researcher second", "researcher third"],
        )
        self.assertTrue(
            all(
                text not in payload["researcher_last_two_messages"]
                for text in (
                    "search assistant first",
                    "search assistant second",
                    "search assistant latest",
                )
            )
        )

    def test_unknown_policy_is_rejected(self):
        with self.assertRaises(ValueError):
            editor_messages(ORIGINAL, "draft", policy="unknown")


if __name__ == "__main__":
    unittest.main()
