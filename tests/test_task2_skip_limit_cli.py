import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from usersim.task2 import recovery
from usersim.task2.debug import Task2DebugRunner
from usersim.task2.reconciliation import check_skip_bounds
from test_task2_debug_runner import start_body, scenario


class SkipLimitCliTests(unittest.TestCase):
    def test_selected_limit_pauses_then_resumes_same_failed_turn_once(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td)
            posts, models = [], []
            frame, remote = 0, None

            def organizer_post(path, payload):
                nonlocal frame, remote
                posts.append((path, payload))
                if path.endswith("/start"):
                    return 200, start_body("c0")
                user = payload["user_utterance"]
                self.assertEqual(user["conversation_id"], f"c{frame}")
                if frame in (4, 9) and user["text"] != "I'll stop here.":
                    remote = {
                        "conversation_id": f"c{frame}",
                        "scenario": scenario(),
                        "chat_messages": [user],
                    }
                    return 500, {"detail": "Synthetic backend error"}
                frame += 1
                return (
                    (428, {"detail": "Run completed"})
                    if frame == 10
                    else (
                        200,
                        {
                            "conversation_id": f"c{frame}",
                            "scenario": scenario(),
                            "utterance": None,
                        },
                    )
                )

            def model_post(request):
                models.append(request)
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

            class Session:
                def get(self, *_args, **_kwargs):
                    return SimpleNamespace(status_code=200, json=lambda: remote)

            def invoke(limit):
                with (
                    patch.object(recovery, "_read_secret", return_value="synthetic"),
                    patch.object(
                        recovery,
                        "_live_transports",
                        return_value=(organizer_post, model_post, Session()),
                    ),
                    patch.object(recovery, "_preflight", return_value={}),
                ):
                    recovery.main(
                        [
                            "--run",
                            "--mode",
                            "debug",
                            "--run-id",
                            "r",
                            "--output-dir",
                            str(out),
                            "--max-operational-skips",
                            str(limit),
                        ]
                    )

            with self.assertRaisesRegex(RuntimeError, "Operational skip"):
                invoke(1)
            state = json.loads((out / "state.json").read_text())
            self.assertEqual(
                (state["completed_conversations"], state["skipped_conversations"]),
                (8, 1),
            )
            self.assertEqual(state["total_user_turns"], 10)
            self.assertFalse((out / "organizer/continue-0011.json").exists())
            self.assertEqual(len(models), 20)
            old_policy = json.loads((out / "recovery-policy.json").read_text())
            self.assertEqual(old_policy["max_skips"], 1)
            before_posts = len(posts)
            with self.assertRaisesRegex(RuntimeError, "Recovery policy changed"):
                invoke(2)
            self.assertEqual(len(posts), before_posts)
            self.assertEqual(len(models), 20)
            self.assertEqual(json.loads((out / "state.json").read_text()), state)

            # Simulate the enabling write of a separately reviewed migration.
            # Preserve the failed request and halted state; recovery posts only
            # the distinct close and never regenerates or resends that request.
            (out / "recovery-policy.json").write_text(
                json.dumps({**old_policy, "max_skips": 2})
            )
            invoke(2)
            state = json.loads((out / "state.json").read_text())
            self.assertEqual(state["status"], "complete")
            self.assertEqual(
                (state["completed_conversations"], state["skipped_conversations"]),
                (8, 2),
            )
            self.assertEqual(state["total_user_turns"], 12)
            self.assertEqual(len(models), 20)
            self.assertEqual(sum(path.endswith("/start") for path, _ in posts), 1)
            self.assertEqual(len(posts), before_posts + 1)
            self.assertEqual(posts[-1][1]["user_utterance"]["text"], "I'll stop here.")

    def test_timeout_dispatch_uses_selected_absolute_limit(self):
        with tempfile.TemporaryDirectory() as td:
            r = Task2DebugRunner(
                Path(td),
                run_id="r",
                organizer_post=None,
                model_post=None,
                source_files=[],
            )
            state = r._load_state()
            state["status"] = "halted"
            r._save_state(state)
            r.pending_path.write_text("{}")
            with (
                patch.object(recovery, "recover_timeout") as timeout,
                patch.object(r, "run", return_value={"status": "complete"}),
            ):
                recovery.run_with_recovery(r, lambda: None, max_skips=48)
            self.assertEqual(timeout.call_args.kwargs["max_skips"], 48)

    def test_larger_absolute_limit_preserves_fraction_and_consecutive_circuits(self):
        for completed, skipped, consecutive in ((0, 2, 0), (20, 3, 3)):
            with self.subTest(completed=completed), tempfile.TemporaryDirectory() as td:
                r = Task2DebugRunner(
                    Path(td),
                    run_id="r",
                    organizer_post=None,
                    model_post=None,
                    source_files=[],
                )
                state = r._load_state()
                state.update(
                    completed_conversations=completed,
                    skipped_conversations=skipped,
                    consecutive_operational_skips=consecutive,
                )
                with self.assertRaisesRegex(
                    RuntimeError, "Operational skip|Consecutive backend-error"
                ):
                    check_skip_bounds(r, state, max_skips=48)

    def test_invalid_skip_limit_rejected_before_credentials(self):
        for value in ("0", "-1", "1.5", "nan"):
            with self.subTest(value=value), tempfile.TemporaryDirectory() as td:
                with (
                    patch.object(recovery, "_read_secret") as secret,
                    self.assertRaises(SystemExit) as error,
                ):
                    recovery.main(
                        [
                            "--run",
                            "--mode",
                            "debug",
                            "--run-id",
                            "r",
                            "--output-dir",
                            td,
                            "--max-operational-skips",
                            value,
                        ]
                    )
                self.assertEqual(error.exception.code, 2)
                secret.assert_not_called()
