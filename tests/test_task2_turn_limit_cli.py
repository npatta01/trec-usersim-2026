import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from usersim.task2 import recovery
from usersim.task2.debug import Task2DebugRunner
from test_task2_debug_runner import continue_body, start_body


class TurnLimitCliTests(unittest.TestCase):
    def test_total_turn_pause_and_explicit_resume_do_not_repeat_completed_requests(
        self,
    ):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td)
            posts, models = [], []

            def organizer_post(path, payload):
                posts.append(path)
                if path.endswith("/start"):
                    return 200, start_body()
                if len(posts) == 2:
                    return 200, continue_body(
                        user_text=payload["user_utterance"]["text"]
                    )
                return 428, {"detail": "Run completed"}

            def model_post(request):
                models.append(request)
                final = len(models) > 2
                text = "Thanks" if final else "Tell me more"
                if request.get("response_format"):
                    text = json.dumps({"text": text, "is_final": final})
                return 200, {
                    "choices": [
                        {"finish_reason": "stop", "message": {"content": text}}
                    ],
                    "usage": {"cost": 0.001},
                }

            def invoke(limit):
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
                            "--max-total-turns",
                            str(limit),
                        ]
                    )

            invoke(1)
            manifest = json.loads((out / "manifest.json").read_text())
            state = json.loads((out / "state.json").read_text())
            self.assertEqual(manifest["config"]["max_total_turns"], 1)
            self.assertEqual(state["status"], "halted")
            self.assertEqual(state["halt_reason"], "operational_total_turn_cap")
            self.assertEqual(state["total_user_turns"], 1)
            self.assertEqual(len(models), 2)
            self.assertFalse((out / "model/turn-0001-draft.json").exists())
            self.assertEqual(posts, ["/task2/debug/start", "/task2/debug/continue"])

            with self.assertRaisesRegex(
                RuntimeError, "Frozen Task 2 debug manifest changed"
            ):
                invoke(3)
            self.assertEqual(len(models), 2)
            self.assertEqual(len(posts), 2)
            self.assertEqual(json.loads((out / "manifest.json").read_text()), manifest)

            # Simulate a separately audited configuration migration. Freezing
            # a larger bound alone must not enable a halted checkpoint.
            runner = Task2DebugRunner(
                out,
                run_id="r",
                organizer_post=organizer_post,
                model_post=model_post,
                cap_usd=6,
                max_total_turns=3,
                description=manifest["config"]["description"],
            )
            (out / "manifest.json").unlink()
            runner.freeze()
            with self.assertRaisesRegex(RuntimeError, "No backend failure receipt"):
                recovery.run_with_recovery(runner, lambda: self.fail("Unexpected GET"))
            self.assertEqual(len(models), 2)
            self.assertEqual(len(posts), 2)
            state = runner._load_state()
            state["status"] = "running"
            state.pop("halt_reason", None)
            (out / "error.json").unlink()
            runner._save_state(state)
            invoke(3)
            self.assertEqual(runner._load_state()["status"], "complete")
            self.assertEqual(runner._load_state()["total_user_turns"], 2)
            self.assertEqual(len(models), 4)
            self.assertEqual(
                posts,
                [
                    "/task2/debug/start",
                    "/task2/debug/continue",
                    "/task2/debug/continue",
                ],
            )

    def test_invalid_turn_limit_rejected_before_credentials(self):
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
                            "--max-total-turns",
                            value,
                        ]
                    )
                self.assertEqual(error.exception.code, 2)
                secret.assert_not_called()


if __name__ == "__main__":
    unittest.main()
