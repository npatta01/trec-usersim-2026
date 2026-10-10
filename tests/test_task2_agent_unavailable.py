import json
import tempfile
import unittest
from pathlib import Path

from usersim.checkpoints import digest
from usersim.task2.recovery import recover_backend_error, run_with_recovery
from usersim.task2.reconciliation import _verify_raw_prefix


def unavailable_body(conversation_id="c1", agent="synthetic-agent"):
    detail = json.dumps({"detail": f"Agent '{agent}' is currently unavailable."})
    return {
        "detail": f"Error occurred while generating agent response for session {conversation_id}: {detail}"
    }


class AgentUnavailableTests(unittest.TestCase):
    def setup_runner(self, folder):
        from test_task2_recovery import RecoveryTests

        runner, calls, remote = RecoveryTests().setup_runner(folder)
        path = runner.organizer_dir / "continue-0000.json"
        receipt = json.loads(path.read_text())
        receipt.update(status=503, body=unavailable_body())
        path.write_text(json.dumps(receipt))
        return runner, calls, remote

    def test_verified_unavailable_agent_closes_once_and_replays_locally(self):
        with tempfile.TemporaryDirectory() as td:
            runner, calls, remote = self.setup_runner(Path(td))
            previous = runner._load_state()
            result = recover_backend_error(runner, lambda: remote)
            self.assertEqual(result["skipped_conversations"], 1)
            self.assertEqual(result["completed_conversations"], 0)
            self.assertEqual(result["total_user_turns"], 2)
            self.assertEqual(len(calls), 1)
            self.assertEqual(calls[0][1]["user_utterance"]["text"], "I'll stop here.")
            runner._save_state(previous)
            replay = recover_backend_error(
                runner, lambda: self.fail("Cached closing receipt needs no GET")
            )
            self.assertEqual(replay, result)
            self.assertEqual(len(calls), 1)

    def test_unclassified_or_mismatched_availability_errors_never_read_or_close(self):
        cases = [
            (503, {"detail": "Service unavailable"}),
            (503, unavailable_body("other-conversation")),
            (504, unavailable_body()),
            (
                503,
                {
                    "detail": "Error occurred while generating agent response for session c1: not JSON"
                },
            ),
            (
                503,
                {
                    "detail": 'Error occurred while generating agent response for session c1: {"detail":"Quota exceeded"}'
                },
            ),
            (503, unavailable_body(agent="")),
            (503, {"detail": None}),
        ]
        for code, body in cases:
            with (
                self.subTest(code=code, body=body),
                tempfile.TemporaryDirectory() as td,
            ):
                runner, calls, remote = self.setup_runner(Path(td))
                path = runner.organizer_dir / "continue-0000.json"
                receipt = json.loads(path.read_text())
                receipt.update(status=code, body=body)
                path.write_text(json.dumps(receipt))
                with self.assertRaises(RuntimeError):
                    recover_backend_error(runner, lambda: self.fail("No GET expected"))
                self.assertEqual(calls, [])

    def test_verified_error_still_requires_exact_persisted_prefix(self):
        with tempfile.TemporaryDirectory() as td:
            runner, calls, remote = self.setup_runner(Path(td))
            remote["chat_messages"][0]["text"] = "Different"
            with self.assertRaises(RuntimeError):
                recover_backend_error(runner, lambda: remote)
            self.assertEqual(calls, [])

    def test_delayed_reply_has_classified_proof_for_future_prefix_checks(self):
        with tempfile.TemporaryDirectory() as td:
            runner, calls, remote = self.setup_runner(Path(td))
            remote["chat_messages"].append(
                {
                    "participant_name": "agent",
                    "text": "Here are data",
                    "conversation_id": "c1",
                }
            )
            recovered = recover_backend_error(runner, lambda: remote)
            self.assertEqual(recovered["total_user_turns"], 1)
            self.assertEqual(calls, [])
            event_path = runner.out / "reconciliation/continue-0000.json"
            event = json.loads(event_path.read_text())
            self.assertEqual(event["origin"], "HTTP503")
            _verify_raw_prefix(runner, 1, remote["chat_messages"], "c1")
            # Even an internally rehashed event cannot turn generic 503 into proof.
            proof_path = runner.organizer_dir / "continue-0000.json"
            proof = json.loads(proof_path.read_text())
            proof["body"] = {"detail": "Service unavailable"}
            proof_path.write_text(json.dumps(proof))
            event["source_proof_sha256"] = digest(proof)
            event_path.write_text(json.dumps(event))
            with self.assertRaises(RuntimeError):
                _verify_raw_prefix(runner, 1, remote["chat_messages"], "c1")

    def test_full_recovery_loop_resumes_then_finishes_without_original_repost(self):
        with tempfile.TemporaryDirectory() as td:
            runner, calls, remote = self.setup_runner(Path(td))
            original_post = runner.organizer_post

            def post(path, payload):
                if payload["user_utterance"]["conversation_id"] == "c1":
                    return original_post(path, payload)
                calls.append((path, payload))
                return 428, {"detail": "Run completed"}

            def model(request):
                text = (
                    '{"text":"Thanks","is_final":true}'
                    if request.get("response_format")
                    else "Thanks"
                )
                return 200, {
                    "choices": [
                        {"finish_reason": "stop", "message": {"content": text}}
                    ],
                    "usage": {"cost": 0.001},
                }

            runner.organizer_post = post
            runner.model.post = model
            result = run_with_recovery(runner, lambda: remote)
            self.assertEqual(result["status"], "complete")
            self.assertEqual(result["skipped_conversations"], 1)
            self.assertEqual(result["completed_conversations"], 1)
            self.assertEqual(len(calls), 2)
            self.assertFalse(
                any(p["user_utterance"]["text"] == "Find data" for _, p in calls)
            )
