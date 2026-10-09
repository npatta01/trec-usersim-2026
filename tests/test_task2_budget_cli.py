import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from usersim.task2 import recovery
from test_task2_debug_runner import start_body


class BudgetCliTests(unittest.TestCase):
    def test_selected_budget_is_frozen_and_used_by_real_debug_loop(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td)
            posts = []

            def organizer_post(path, payload):
                posts.append(path)
                if path.endswith("/start"):
                    return 200, start_body()
                return 428, {"detail": "Run completed"}

            def model_post(request):
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

            with (
                patch.object(recovery, "_read_secret", return_value="synthetic"),
                patch.object(
                    recovery,
                    "_live_transports",
                    return_value=(organizer_post, model_post, None),
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
                        "--cap-usd",
                        "6",
                    ]
                )
            self.assertEqual(
                json.loads((out / "manifest.json").read_text())["config"]["cap_usd"],
                6.0,
            )
            self.assertEqual(
                json.loads((out / "manifest.json").read_text())["config"][
                    "max_total_turns"
                ],
                500,
            )
            self.assertEqual(
                json.loads((out / "state.json").read_text())["status"], "complete"
            )
            self.assertEqual(posts, ["/task2/debug/start", "/task2/debug/continue"])

            # An override cannot silently mutate a frozen run's budget.
            with (
                patch.object(recovery, "_read_secret", return_value="synthetic"),
                patch.object(
                    recovery,
                    "_live_transports",
                    return_value=(organizer_post, model_post, None),
                ),
                patch.object(recovery, "_preflight", return_value={}),
            ):
                with self.assertRaisesRegex(
                    RuntimeError, "Frozen Task 2 debug manifest changed"
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
                            "--cap-usd",
                            "7",
                        ]
                    )
            self.assertEqual(posts, ["/task2/debug/start", "/task2/debug/continue"])

    def test_budget_pause_resumes_cached_draft_without_duplicate_model_or_organizer_call(
        self,
    ):
        from usersim.task2.debug import Task2DebugRunner

        with tempfile.TemporaryDirectory() as td:
            out = Path(td)
            models, posts = [], []

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

            def organizer_post(path, payload):
                posts.append(path)
                return (
                    (200, start_body())
                    if path.endswith("/start")
                    else (428, {"detail": "Run completed"})
                )

            old = Task2DebugRunner(
                out,
                run_id="r",
                cap_usd=0.004,
                organizer_post=organizer_post,
                model_post=model_post,
                source_files=[],
            )
            with self.assertRaisesRegex(RuntimeError, "Model budget cap reached"):
                old.run()
            old.record_failure()
            self.assertEqual(len(models), 1)
            self.assertFalse(old.model.has_pending())
            self.assertFalse(old.pending_path.exists())
            self.assertEqual(posts, ["/task2/debug/start"])

            # Simulate the explicit, audited configuration migration, with
            # original manifest/state retained. No request receipt is changed.
            (out / "manifest.json").rename(out / "original-manifest.json")
            state = old._load_state()
            (out / "original-state.json").write_text(json.dumps(state))
            new = Task2DebugRunner(
                out,
                run_id="r",
                cap_usd=1,
                organizer_post=organizer_post,
                model_post=model_post,
                source_files=[],
            )
            new.freeze()
            # If migration is interrupted after freezing the larger cap,
            # the old halted state still blocks all paid/submission calls.
            with self.assertRaisesRegex(RuntimeError, "No backend failure receipt"):
                recovery.run_with_recovery(
                    new,
                    lambda: (_ for _ in ()).throw(AssertionError("Unneeded GET")),
                )
            self.assertEqual(len(models), 1)
            self.assertEqual(posts, ["/task2/debug/start"])
            state["status"] = "running"
            state.pop("halt_reason", None)
            old._save_state(state)
            result = recovery.run_with_recovery(
                new,
                lambda: (_ for _ in ()).throw(
                    AssertionError("Unneeded session recovery")
                ),
            )
            self.assertEqual(result["status"], "complete")
            self.assertEqual(len(models), 2)
            self.assertEqual(sum("response_format" in request for request in models), 1)
            self.assertEqual(posts, ["/task2/debug/start", "/task2/debug/continue"])

    def test_invalid_budget_rejected_before_credentials_or_transport(self):
        for value in ("nan", "inf", "-inf", "0", "-1"):
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
                            "--cap-usd",
                            value,
                        ]
                    )
                self.assertEqual(error.exception.code, 2)
                secret.assert_not_called()


if __name__ == "__main__":
    unittest.main()
