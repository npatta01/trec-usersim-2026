import json
import tempfile
import unittest
from pathlib import Path
from datetime import datetime, timedelta, timezone

from requests.exceptions import ReadTimeout

from usersim.task2.debug import Task2DebugRunner
from usersim.task2.protocol import build_continue_payload
from usersim.task2.recovery import run_with_recovery
from test_task2_debug_runner import start_body, scenario


class Clock:
    def __init__(self):
        self.value = datetime(2026, 1, 1, tzinfo=timezone.utc)
        self.elapsed = 0

    def now(self):
        return self.value

    def wait(self, seconds):
        self.elapsed += seconds
        self.value += timedelta(seconds=seconds)


class TimeoutTests(unittest.TestCase):
    def setup_timeout(self, out, *, timestamp="2020-01-01T00:00:00+00:00", close=None):
        calls = []

        def post(path, payload):
            calls.append((path, payload))
            if len(calls) == 1:
                raise ReadTimeout("synthetic organizer timeout")
            if payload["user_utterance"]["conversation_id"] == "c1":
                if close:
                    return close(path, payload)
                return 200, {
                    "conversation_id": "c2",
                    "scenario": scenario(),
                    "utterance": None,
                }
            return 428, {"detail": "Run completed"}

        def model(request):
            content = (
                '{"text":"Thanks","is_final":true}'
                if request.get("response_format")
                else "Thanks"
            )
            return 200, {
                "choices": [{"finish_reason": "stop", "message": {"content": content}}],
                "usage": {"cost": 0.001},
            }

        runner = Task2DebugRunner(
            out, run_id="r", organizer_post=post, model_post=model, source_files=[]
        )
        state = runner._load_state()
        state.update(status="halted", current={"item": start_body(), "turns": 0})
        runner._save_state(state)
        payload = build_continue_payload(
            "r", "c1", "Find data", False, timestamp=timestamp
        )
        with self.assertRaises(ReadTimeout):
            runner._organizer_call("continue-0000", runner.continue_path, payload)
        remote = {
            "conversation_id": "c1",
            "scenario": scenario(),
            "chat_messages": [payload["user_utterance"]],
        }
        return runner, calls, remote

    def test_original_timeout_is_classified_without_fabricating_http_response(self):
        # Missing transport classification would strand the original request forever.
        with tempfile.TemporaryDirectory() as td:
            runner, calls, remote = self.setup_timeout(Path(td))
            proof = runner.organizer_dir / "transport-error-continue-0000.json"
            self.assertTrue(
                proof.exists(),
                "A received ReadTimeout needs a durable transport error record",
            )
            event = json.loads(proof.read_text())
            pending = json.loads(runner.pending_path.read_text())
            self.assertEqual(event["type"], "ReadTimeout")
            self.assertEqual(event["request_sha256"], pending["request_sha256"])
            self.assertFalse((runner.organizer_dir / "continue-0000.json").exists())
            self.assertTrue(runner.pending_path.exists())

    def test_full_loop_closes_verified_timeout_and_finishes_without_resending_it(self):
        # A missing timeout branch in the real controller used to halt the full run.
        with tempfile.TemporaryDirectory() as td:
            runner, calls, remote = self.setup_timeout(Path(td))
            clock = Clock()
            try:
                result = run_with_recovery(
                    runner, lambda: remote, now=clock.now, wait=clock.wait
                )
            except RuntimeError as exc:
                self.fail(
                    f"Verified original timeout still strands the full run: {exc}"
                )
            self.assertEqual(result["status"], "complete")
            self.assertEqual(result["total_user_turns"], 3)
            self.assertEqual(result["completed_conversations"], 1)
            self.assertEqual(result["skipped_conversations"], 1)
            self.assertEqual(result["user_stops"], 1)
            self.assertEqual(
                [p["user_utterance"]["conversation_id"] for _, p in calls],
                ["c1", "c1", "c2"],
            )
            self.assertEqual(
                sum(p["user_utterance"]["text"] == "Find data" for _, p in calls), 1
            )
            self.assertTrue(calls[1][1]["user_utterance"]["is_final"])
            self.assertFalse(runner.pending_path.exists())
            self.assertGreaterEqual(clock.elapsed, 1800)

    def test_delayed_reply_survives_crash_and_future_raw_prefix_checks(self):
        # Losing the GET-derived reply makes the next failure in this conversation unsafe.
        from usersim.task2.timeout import recover_timeout
        from usersim.task2.reconciliation import _verify_raw_prefix

        with tempfile.TemporaryDirectory() as td:
            runner, calls, remote = self.setup_timeout(Path(td))
            old = runner._load_state()
            remote["chat_messages"].append(
                {
                    "participant_name": "agent",
                    "text": "Here are data",
                    "conversation_id": "c1",
                    "is_final": False,
                }
            )
            result = recover_timeout(runner, lambda: remote)
            self.assertEqual(result["total_user_turns"], 1)
            self.assertEqual(len(calls), 1)
            self.assertFalse((runner.organizer_dir / "continue-0000.json").exists())
            self.assertTrue((runner.out / "reconciliation/continue-0000.json").exists())
            _verify_raw_prefix(runner, 1, remote["chat_messages"], "c1")
            runner._save_state(old)
            replay = recover_timeout(
                runner, lambda: (_ for _ in ()).throw(AssertionError("Unneeded GET"))
            )
            self.assertEqual(replay["total_user_turns"], 1)
            self.assertEqual(len(calls), 1)

    def test_closing_timeout_remains_uncertain_and_never_closes_again(self):
        from usersim.task2.timeout import recover_timeout

        with tempfile.TemporaryDirectory() as td:
            runner, calls, remote = self.setup_timeout(
                Path(td),
                close=lambda *_: (_ for _ in ()).throw(ReadTimeout("close timeout")),
            )
            clock = Clock()
            with self.assertRaises(ReadTimeout):
                recover_timeout(runner, lambda: remote, now=clock.now, wait=clock.wait)
            with self.assertRaises(RuntimeError):
                recover_timeout(runner, lambda: remote, now=clock.now, wait=clock.wait)
            self.assertEqual(len(calls), 2)
            self.assertTrue(runner.pending_path.exists())

    def test_changed_history_at_final_observation_blocks_close(self):
        from usersim.task2.timeout import recover_timeout

        with tempfile.TemporaryDirectory() as td:
            runner, calls, remote = self.setup_timeout(Path(td))
            clock = Clock()
            observations = []

            def get():
                observations.append(clock.elapsed)
                result = json.loads(json.dumps(remote))
                if clock.elapsed >= 1800 and len(observations) > 61:
                    result["chat_messages"][0]["annotations"] = {"changed": True}
                return result

            with self.assertRaises(RuntimeError):
                recover_timeout(runner, get, now=clock.now, wait=clock.wait)
            self.assertEqual(len(calls), 1)
            self.assertTrue(runner.pending_path.exists())

    def test_missing_transport_proof_keeps_original_request_pending(self):
        from usersim.task2.timeout import recover_timeout

        with tempfile.TemporaryDirectory() as td:
            runner, calls, remote = self.setup_timeout(Path(td))
            (runner.organizer_dir / "transport-error-continue-0000.json").unlink()
            with self.assertRaises(RuntimeError):
                recover_timeout(runner, lambda: remote)
            self.assertEqual(len(calls), 1)
            self.assertTrue(runner.pending_path.exists())

    def test_crash_after_closing_receipt_never_posts_twice(self):
        from usersim.task2.timeout import recover_timeout

        with tempfile.TemporaryDirectory() as td:
            runner, calls, remote = self.setup_timeout(Path(td))
            old = runner._load_state()
            clock = Clock()
            result = recover_timeout(
                runner, lambda: remote, now=clock.now, wait=clock.wait
            )
            self.assertEqual(result["skipped_conversations"], 1)
            runner._save_state(old)
            replay = recover_timeout(
                runner,
                lambda: (_ for _ in ()).throw(AssertionError("Unneeded GET")),
                now=clock.now,
                wait=clock.wait,
            )
            self.assertEqual(replay["skipped_conversations"], 1)
            self.assertEqual(len(calls), 2)

    def test_reply_arriving_at_final_check_is_reconciled_instead_of_closed(self):
        from usersim.task2.timeout import recover_timeout

        with tempfile.TemporaryDirectory() as td:
            runner, calls, remote = self.setup_timeout(Path(td))
            clock = Clock()
            seen = []

            def get():
                seen.append(clock.elapsed)
                result = json.loads(json.dumps(remote))
                if len(seen) > 61:
                    result["chat_messages"].append(
                        {"participant_name": "agent", "text": "Found data"}
                    )
                return result

            result = recover_timeout(runner, get, now=clock.now, wait=clock.wait)
            self.assertEqual(result["total_user_turns"], 1)
            self.assertEqual(result.get("skipped_conversations", 0), 0)
            self.assertEqual(len(calls), 1)

    def test_guard_stops_outage_but_allows_small_warmup(self):
        from usersim.task2.reconciliation import check_skip_bounds

        with tempfile.TemporaryDirectory() as td:
            runner, _, _ = self.setup_timeout(Path(td))
            state = runner._load_state()
            check_skip_bounds(runner, state)
            for completed, skipped, consecutive in (
                (40, 13, 0),
                (40, 24, 0),
                (40, 1, 3),
            ):
                bad = {
                    **state,
                    "completed_conversations": completed,
                    "skipped_conversations": skipped,
                    "consecutive_operational_skips": consecutive,
                }
                with self.assertRaises(RuntimeError):
                    check_skip_bounds(runner, bad)
            check_skip_bounds(
                runner,
                {**state, "completed_conversations": 40, "skipped_conversations": 11},
            )

    def test_corrupt_observation_cannot_accelerate_closure(self):
        from usersim.task2.timeout import recover_timeout

        with tempfile.TemporaryDirectory() as td:
            runner, calls, remote = self.setup_timeout(Path(td))
            clock = Clock()

            def wait(seconds):
                path = runner.out / "recovery/0000-timeout-observation.json"
                obs = json.loads(path.read_text())
                obs["first_seen"] = "2020-01-01T00:00:00+00:00"
                path.write_text(json.dumps(obs))
                raise RuntimeError("synthetic shutdown")

            with self.assertRaises(RuntimeError):
                recover_timeout(runner, lambda: remote, now=clock.now, wait=wait)
            with self.assertRaises(RuntimeError):
                recover_timeout(runner, lambda: remote, now=clock.now, wait=clock.wait)
            self.assertEqual(len(calls), 1)
            self.assertTrue(runner.pending_path.exists())

    def test_reconciliation_event_must_match_original_transport_request(self):
        from usersim.checkpoints import digest
        from usersim.task2.reconciliation import _verify_raw_prefix
        from usersim.task2.timeout import recover_timeout

        with tempfile.TemporaryDirectory() as td:
            runner, calls, remote = self.setup_timeout(Path(td))
            remote["chat_messages"].append(
                {"participant_name": "agent", "text": "Found data"}
            )
            recover_timeout(runner, lambda: remote)
            event_path = runner.out / "reconciliation/continue-0000.json"
            event = json.loads(event_path.read_text())
            event["payload"]["user_utterance"]["text"] = "Changed request"
            event["request_sha256"] = digest(event["payload"])
            event["server_session"]["chat_messages"][0]["text"] = "Changed request"
            event["server_session_sha256"] = digest(event["server_session"])
            event_path.write_text(json.dumps(event))
            with self.assertRaises(RuntimeError):
                _verify_raw_prefix(
                    runner, 1, event["server_session"]["chat_messages"], "c1"
                )
            self.assertEqual(len(calls), 1)

    def test_durable_close_receipt_with_matching_pending_replays_without_post(self):
        from usersim.checkpoints import digest
        from usersim.task2.timeout import recover_timeout

        with tempfile.TemporaryDirectory() as td:
            runner, calls, remote = self.setup_timeout(Path(td))
            old = runner._load_state()
            clock = Clock()
            recover_timeout(runner, lambda: remote, now=clock.now, wait=clock.wait)
            runner._save_state(old)
            (runner.out / "recovery/0000-timeout-result.json").unlink()
            receipt = json.loads(
                (runner.organizer_dir / "continue-0001.json").read_text()
            )
            pending = {
                "checkpoint_name": "continue-0001",
                "path": receipt["path"],
                "payload": receipt["payload"],
                "request_sha256": digest(receipt["payload"]),
            }
            runner.pending_path.write_text(json.dumps(pending))
            result = recover_timeout(
                runner, lambda: (_ for _ in ()).throw(AssertionError("Unneeded GET"))
            )
            self.assertEqual(result["total_user_turns"], 2)
            self.assertEqual(result["skipped_conversations"], 1)
            self.assertEqual(len(calls), 2)
            self.assertFalse(runner.pending_path.exists())

    def test_durable_close_receipt_with_different_pending_keeps_marker(self):
        from usersim.checkpoints import digest
        from usersim.task2.timeout import recover_timeout

        with tempfile.TemporaryDirectory() as td:
            runner, calls, remote = self.setup_timeout(Path(td))
            old = runner._load_state()
            clock = Clock()
            recover_timeout(runner, lambda: remote, now=clock.now, wait=clock.wait)
            runner._save_state(old)
            receipt = json.loads(
                (runner.organizer_dir / "continue-0001.json").read_text()
            )
            pending = {
                "checkpoint_name": "continue-0001",
                "path": receipt["path"],
                "payload": receipt["payload"],
                "request_sha256": digest(receipt["payload"]),
            }
            pending["payload"]["user_utterance"]["text"] = "Different uncertain request"
            pending["request_sha256"] = digest(pending["payload"])
            runner.pending_path.write_text(json.dumps(pending))
            with self.assertRaises(RuntimeError):
                recover_timeout(runner, lambda: remote)
            self.assertEqual(len(calls), 2)
            self.assertTrue(runner.pending_path.exists())

    def test_wrong_request_proof_and_missing_turn_never_trigger_close(self):
        from usersim.task2.timeout import recover_timeout

        for changed in ("proof", "missing_turn", "scenario", "model_pending"):
            with self.subTest(changed=changed), tempfile.TemporaryDirectory() as td:
                runner, calls, remote = self.setup_timeout(Path(td))
                if changed == "proof":
                    path = runner.organizer_dir / "transport-error-continue-0000.json"
                    proof = json.loads(path.read_text())
                    proof["request_sha256"] = "different"
                    path.write_text(json.dumps(proof))
                elif changed == "missing_turn":
                    remote["chat_messages"] = []
                elif changed == "scenario":
                    remote["scenario"]["goal"]["description"] = "Different goal"
                else:
                    (runner.out / "model/inflight.json").write_text("{}")
                with self.assertRaises(RuntimeError):
                    recover_timeout(runner, lambda: remote)
                self.assertEqual(len(calls), 1)
                self.assertTrue(runner.pending_path.exists())


if __name__ == "__main__":
    unittest.main()
