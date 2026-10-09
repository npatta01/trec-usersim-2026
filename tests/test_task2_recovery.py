import json
import tempfile
import unittest
from pathlib import Path
from usersim.task2.debug import Task2DebugRunner
from usersim.task2.protocol import build_continue_payload
from test_task2_debug_runner import start_body, scenario


class RecoveryTests(unittest.TestCase):
    def setup_runner(self, out, close_status=200, close_body=None):
        calls = []

        def post(path, payload):
            calls.append((path, payload))
            return close_status, close_body or {
                "conversation_id": "c2",
                "scenario": scenario(),
                "utterance": None,
            }

        r = Task2DebugRunner(
            out,
            run_id="r",
            organizer_post=post,
            model_post=lambda _: None,
            source_files=[],
        )
        s = r._load_state()
        s.update(status="halted", current={"item": start_body(), "turns": 0})
        r._save_state(s)
        payload = build_continue_payload("r", "c1", "Find data", False)
        r._organizer_call("continue-0000", "/task2/debug/continue", payload)
        # Replace synthetic receipt with the originally failed request.
        f = out / "organizer/continue-0000.json"
        d = json.loads(f.read_text())
        d.update(status=500, body={"detail": "backend failure"})
        f.write_text(json.dumps(d))
        calls.clear()
        remote = {
            "conversation_id": "c1",
            "scenario": scenario(),
            "chat_messages": [payload["user_utterance"]],
        }
        return r, calls, remote

    def test_persisted_turn_skips_and_crash_replay_never_posts_twice(self):
        from usersim.task2.recovery import recover_backend_error

        with tempfile.TemporaryDirectory() as td:
            r, calls, remote = self.setup_runner(Path(td))
            old = r._load_state()
            result = recover_backend_error(r, lambda: remote)
            self.assertEqual(result["skipped_conversations"], 1)
            self.assertEqual(result["completed_conversations"], 0)
            self.assertEqual(result["total_user_turns"], 2)
            self.assertEqual(result["current"]["item"]["conversation_id"], "c2")
            self.assertEqual(len(calls), 1)
            self.assertTrue(calls[0][1]["user_utterance"]["is_final"])
            r._save_state(old)
            result = recover_backend_error(
                r, lambda: (_ for _ in ()).throw(AssertionError("unneeded GET"))
            )
            self.assertEqual(result["skipped_conversations"], 1)
            self.assertEqual(len(calls), 1)

    def test_mismatch_blocks_any_close(self):
        from usersim.task2.recovery import recover_backend_error

        with tempfile.TemporaryDirectory() as td:
            r, calls, remote = self.setup_runner(Path(td))
            remote["chat_messages"][0]["text"] = "Different"
            with self.assertRaises(RuntimeError):
                recover_backend_error(r, lambda: remote)
            self.assertEqual(calls, [])

    def test_delayed_reply_recovers_without_post(self):
        from usersim.task2.recovery import recover_backend_error

        with tempfile.TemporaryDirectory() as td:
            r, calls, remote = self.setup_runner(Path(td))
            remote["chat_messages"].append(
                {"participant_name": "agent", "text": "Here are data"}
            )
            s = recover_backend_error(r, lambda: remote)
            self.assertEqual(s["total_user_turns"], 1)
            self.assertEqual(s.get("skipped_conversations", 0), 0)
            self.assertEqual(calls, [])

    def test_failed_close_never_reposts_on_recovery(self):
        from usersim.task2.recovery import recover_backend_error

        with tempfile.TemporaryDirectory() as td:
            r, calls, remote = self.setup_runner(Path(td), close_status=502)
            for _ in range(2):
                with self.assertRaises(ValueError):
                    recover_backend_error(r, lambda: remote)
            self.assertEqual(len(calls), 1)

    def test_skip_completion_is_not_natural_stop(self):
        from usersim.task2.recovery import recover_backend_error

        with tempfile.TemporaryDirectory() as td:
            r, calls, remote = self.setup_runner(
                Path(td), close_status=428, close_body={"detail": "Run was finished!"}
            )
            s = recover_backend_error(r, lambda: remote)
            self.assertEqual(s["status"], "complete")
            self.assertEqual(s["completed_conversations"], 0)
            self.assertEqual(s["user_stops"], 0)
            self.assertEqual(s["skipped_conversations"], 1)

    def test_skip_cap_and_pending_marker_block_writes(self):
        from usersim.task2.recovery import recover_backend_error

        for pending in (True, False):
            with self.subTest(pending=pending), tempfile.TemporaryDirectory() as td:
                r, calls, remote = self.setup_runner(Path(td))
                if pending:
                    r.pending_path.write_text("{}")
                with self.assertRaises(RuntimeError):
                    recover_backend_error(r, lambda: remote, max_skips=0)
                self.assertEqual(calls, [])

    def test_model_or_schema_errors_are_not_skipped(self):
        from usersim.task2.recovery import recover_backend_error

        with tempfile.TemporaryDirectory() as td:
            r, calls, remote = self.setup_runner(Path(td))
            f = r.organizer_dir / "continue-0000.json"
            d = json.loads(f.read_text())
            d["status"] = 200
            f.write_text(json.dumps(d))
            with self.assertRaises(RuntimeError):
                recover_backend_error(r, lambda: remote)
            self.assertEqual(calls, [])

    def test_final_turn_already_advanced_is_natural_completion(self):
        from usersim.task2.recovery import recover_backend_error
        from usersim.checkpoints import digest

        with tempfile.TemporaryDirectory() as td:
            r, calls, _ = self.setup_runner(Path(td))
            f = r.organizer_dir / "continue-0000.json"
            d = json.loads(f.read_text())
            d["payload"]["user_utterance"]["is_final"] = True
            d["request_sha256"] = digest(d["payload"])
            f.write_text(json.dumps(d))
            s = recover_backend_error(r, lambda: start_body("c2"))
            self.assertEqual(s["completed_conversations"], 1)
            self.assertEqual(s["user_stops"], 1)
            self.assertEqual(s.get("skipped_conversations", 0), 0)
            self.assertEqual(calls, [])

    def test_debug_and_official_route_boundaries(self):
        from usersim.task2.recovery import Task2OfficialRunner

        with tempfile.TemporaryDirectory() as td:
            r = Task2OfficialRunner(
                Path(td),
                run_id="r",
                organizer_post=lambda *_: (200, start_body()),
                model_post=None,
                source_files=[],
            )
            with self.assertRaises(ValueError):
                r._organizer_call("bad", "/task2/debug/start", {})
            r._organizer_call("start", "/task2/run/start", {"run_id": "r"})
            self.assertEqual(
                r._config()["routes"], ["/task2/run/continue", "/task2/run/start"]
            )

    def test_loop_reconciles_then_completes_without_reusing_model_request(self):
        from usersim.task2.recovery import run_with_recovery

        with tempfile.TemporaryDirectory() as td:
            r, calls, remote = self.setup_runner(Path(td))
            r.organizer_post = (
                lambda path, payload: (
                    200,
                    {
                        "conversation_id": "c2",
                        "scenario": scenario(),
                        "utterance": None,
                    },
                )
                if payload["user_utterance"]["conversation_id"] == "c1"
                else (428, {"detail": "Run completed"})
            )
            model_inputs = []

            def model(request):
                model_inputs.append(request)
                content = (
                    '{"text":"Thanks","is_final":true}'
                    if request.get("response_format")
                    else "Thanks"
                )
                return 200, {
                    "choices": [
                        {"finish_reason": "stop", "message": {"content": content}}
                    ],
                    "usage": {"cost": 0.001},
                }

            r.model.post = model
            result = run_with_recovery(r, lambda: remote)
            self.assertEqual(result["status"], "complete")
            self.assertEqual(result["completed_conversations"], 1)
            self.assertEqual(result["skipped_conversations"], 1)
            self.assertEqual(len(model_inputs), 2)
            self.assertTrue((r.organizer_dir / "continue-0002.json").exists())

    def test_changed_persisted_metadata_blocks_close(self):
        from usersim.task2.recovery import recover_backend_error

        for key, value in [
            ("is_final", True),
            ("timestamp", "2000-01-01T00:00:00Z"),
            ("conversation_id", "wrong"),
            ("annotations", {"unexpected": True}),
        ]:
            with self.subTest(key=key), tempfile.TemporaryDirectory() as td:
                r, calls, remote = self.setup_runner(Path(td))
                remote["chat_messages"][0][key] = value
                with self.assertRaises(RuntimeError):
                    recover_backend_error(r, lambda: remote)
                self.assertEqual(calls, [])

    def test_closing_message_respects_total_and_conversation_limits(self):
        from usersim.task2.recovery import recover_backend_error

        for limit in ("max_total_turns", "max_conversation_turns"):
            with self.subTest(limit=limit), tempfile.TemporaryDirectory() as td:
                r, calls, remote = self.setup_runner(Path(td))
                setattr(r, limit, 1)
                with self.assertRaises(RuntimeError):
                    recover_backend_error(r, lambda: remote)
                self.assertEqual(calls, [])

    def test_official_gate_requires_completed_debug_and_reviewed_evidence(self):
        from usersim.task2.recovery import verify_official_gate

        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(RuntimeError):
                verify_official_gate(Path(td), None)

    def test_equivalent_UTC_timestamp_spelling_is_accepted(self):
        from usersim.task2.recovery import recover_backend_error

        with tempfile.TemporaryDirectory() as td:
            r, calls, remote = self.setup_runner(Path(td))
            remote["chat_messages"][0]["timestamp"] = remote["chat_messages"][0][
                "timestamp"
            ].replace("+00:00", "Z")
            result = recover_backend_error(r, lambda: remote)
            self.assertEqual(result["skipped_conversations"], 1)

    def test_unapproved_503_and_504_never_close(self):
        from usersim.task2.recovery import recover_backend_error

        for code in (503, 504):
            with self.subTest(code=code), tempfile.TemporaryDirectory() as td:
                r, calls, remote = self.setup_runner(Path(td))
                f = r.organizer_dir / "continue-0000.json"
                d = json.loads(f.read_text())
                d["status"] = code
                f.write_text(json.dumps(d))
                with self.assertRaises(RuntimeError):
                    recover_backend_error(r, lambda: remote)
                self.assertEqual(calls, [])

    def test_official_gate_hashes_review_and_rejects_incomplete_or_changed_state(self):
        from usersim.task2.recovery import (
            verify_official_gate,
            DEBUG_RECOVERY_DESCRIPTION,
        )
        from usersim.checkpoints import digest

        self.assertIn("skipped", DEBUG_RECOVERY_DESCRIPTION)
        with tempfile.TemporaryDirectory() as td:
            p = Path(td)
            (p / "organizer").mkdir()
            state = {
                "run_id": "debug-r",
                "status": "complete",
                "completed_conversations": 1,
            }
            manifest = Task2DebugRunner(
                p, run_id="debug-r", organizer_post=None, model_post=None
            ).freeze()
            from usersim.task2.recovery import POLICY

            (p / "recovery-policy.json").write_text(
                json.dumps({**POLICY, "mode": "debug"})
            )
            payload = {"run_id": "debug-r"}
            final = {
                "path": "/task2/debug/continue",
                "payload": payload,
                "request_sha256": digest(payload),
                "status": 428,
                "body": {"detail": "Run completed"},
            }
            for name, value in [
                ("state.json", state),
                ("manifest.json", manifest),
                ("organizer/continue-0000.json", final),
            ]:
                (p / name).write_text(json.dumps(value))
            review = {
                "run_id": "debug-r",
                "state_sha256": digest(state),
                "approved_for_official": True,
                "manifest_sha256": digest(manifest),
                "completion_receipt_sha256": digest(final),
                "reviewed_conversation_ids": ["c1"],
            }
            f = p / "review.json"
            f.write_text(json.dumps(review))
            self.assertEqual(verify_official_gate(p, f)["debug_run_id"], "debug-r")
            selected_policy = {**POLICY, "max_skips": 48, "mode": "debug"}
            (p / "recovery-policy.json").write_text(json.dumps(selected_policy))
            with self.assertRaises(RuntimeError):
                verify_official_gate(p, f)
            with self.assertRaisesRegex(RuntimeError, "review is not bound"):
                verify_official_gate(p, f, max_skips=48)
            review["recovery_policy_sha256"] = digest(selected_policy)
            f.write_text(json.dumps(review))
            self.assertEqual(
                verify_official_gate(p, f, max_skips=48)["debug_run_id"], "debug-r"
            )
            review["recovery_policy_sha256"] = "wrong"
            f.write_text(json.dumps(review))
            with self.assertRaisesRegex(RuntimeError, "review is not bound"):
                verify_official_gate(p, f, max_skips=48)
            del review["recovery_policy_sha256"]
            f.write_text(json.dumps(review))
            (p / "recovery-policy.json").write_text(
                json.dumps({**POLICY, "mode": "debug"})
            )
            (p / "recovery-policy.json").unlink()
            with self.assertRaises(RuntimeError):
                verify_official_gate(p, f)
            (p / "recovery-policy.json").write_text(
                json.dumps({**POLICY, "mode": "debug"})
            )
            frozen = p / "frozen/usersim/task2/recovery.py"
            original_frozen = frozen.read_bytes()
            frozen.write_text("changed code")
            with self.assertRaises(RuntimeError):
                verify_official_gate(p, f)
            frozen.write_bytes(original_frozen)
            state["status"] = "halted"
            (p / "state.json").write_text(json.dumps(state))
            with self.assertRaises(RuntimeError):
                verify_official_gate(p, f)
            state["status"] = "complete"
            state["completed_conversations"] = 2
            (p / "state.json").write_text(json.dumps(state))
            with self.assertRaises(RuntimeError):
                verify_official_gate(p, f)
