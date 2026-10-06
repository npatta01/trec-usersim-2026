"""Synthetic pre-refactor requests, captured at commit 946aacf without inference."""

import copy
import json
import subprocess
import sys
import unittest
from pathlib import Path

from usersim.task2.core import Conversation, Turn
from usersim.task2.generator import generate_turn

ROOT = Path(__file__).resolve().parents[1]


class RequestParityTests(unittest.TestCase):
    def test_opening_followup_long_history_and_stop_requests_match_reference(self):
        fixture = json.loads(
            (Path(__file__).parent / "fixtures/task2_requests_v1.json").read_text()
        )
        for number, case in enumerate(fixture["cases"]):
            with self.subTest(case=number):
                item = copy.deepcopy(case["item"])
                original = copy.deepcopy(item)
                conversation = Conversation.start(
                    item["conversation_id"], item["scenario"]
                )
                for message in item["chat_messages"]:
                    if message["participant_name"] == "user":
                        conversation = conversation.append_user(
                            Turn(message["text"], False)
                        )
                    else:
                        conversation = conversation.append_agent(message["text"])
                calls = []

                def call(stage, request):
                    calls.append({"stage": stage, "request": request})
                    if stage == "draft":
                        return json.dumps(
                            {
                                "text": (
                                    "Enough, thanks."
                                    if case["draft_final"]
                                    else "Does it include audio?"
                                ),
                                "is_final": case["draft_final"],
                            }
                        )
                    return (
                        "Thanks, enough." if case["draft_final"] else "Audio included?"
                    )

                result = generate_turn(conversation, call)
                self.assertEqual(calls, case["requests"])
                self.assertEqual(
                    {"text": result.text, "is_final": result.is_final}, case["result"]
                )
                self.assertEqual(item, original)

    def test_runtime_does_not_load_experiments_or_litellm(self):
        code = """
import sys
import usersim.task2.debug
for name in sys.modules:
    if name == 'experiments' or name.startswith(('experiments.', 'litellm', 'run_')):
        raise RuntimeError('Unexpected runtime dependency: ' + name)
"""
        result = subprocess.run(
            [sys.executable, "-c", code],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_cli_help_from_outside_checkout(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/run_task2_debug.py"), "--help"],
            cwd="/tmp",
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("--run-id", result.stdout)

    def test_historical_cli_module_entrypoints_show_help(self):
        for name in (
            "run_offline_baseline",
            "run_researcher_role_diagnostic",
            "run_single_call_prompt_comparison",
            "run_prompt_iteration_b21",
            "run_prompt_iteration_b22",
            "run_style_postedit",
            "run_task1_debug",
        ):
            with self.subTest(module=name):
                result = subprocess.run(
                    [sys.executable, "-m", "experiments." + name, "--help"],
                    cwd=ROOT,
                    capture_output=True,
                    text=True,
                    timeout=30,
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn("usage:", result.stdout)
