import json
import tempfile
import subprocess
import sys
import unittest
from pathlib import Path
from unittest import mock

import usersim.task2.debug as debug
from usersim.task2.protocol import (
    is_completion,
    validate_start_response,
    validate_continue_response,
    build_continue_payload,
)

from usersim.task2.debug import (
    DEBUG_ROUTES,
    MODEL,
    Task2DebugRunner,
    freeze_manifest,
)


def scenario(topic="datasets"):
    return {
        "goal": {"topic": topic, "context": "find useful data"},
        "persona": {"individual_traits": {"interaction_style": "elaborate"}},
    }


def start_body(cid="c1", topic="datasets"):
    return {"conversation_id": cid, "scenario": scenario(topic), "chat_messages": []}


def continue_body(
    cid="c1",
    topic="datasets",
    text="Please give the download page.",
    user_text="Find a dataset.",
):
    return {
        "conversation_id": cid,
        "scenario": scenario(topic),
        "chat_messages": [
            {"participant_name": "user", "text": user_text},
            {"participant_name": "agent", "text": text},
        ],
    }


class ContractTests(unittest.TestCase):
    def test_start_normalizes_missing_history(self):
        item = validate_start_response(
            200, {"conversation_id": "c1", "scenario": scenario()}
        )
        self.assertEqual(item["chat_messages"], [])

    def test_fresh_start_rejects_nonempty_history(self):
        body = start_body()
        body["chat_messages"] = [
            {"participant_name": "user", "text": "Unexpected prior turn."},
            {"participant_name": "agent", "text": "Unexpected prior reply."},
        ]
        with self.assertRaises(ValueError):
            validate_start_response(200, body)

    def test_200_requires_exact_full_history(self):
        current = start_body()
        payload = build_continue_payload(
            "run", "c1", "Find a dataset.", False, timestamp="2026-10-06T12:00:00+00:00"
        )
        valid = validate_continue_response(200, continue_body(), current, payload)
        self.assertEqual(
            valid["item"]["chat_messages"][-1]["participant_name"], "agent"
        )
        missing_agent = dict(continue_body())
        missing_agent["chat_messages"] = missing_agent["chat_messages"][:1]
        with self.assertRaises(ValueError):
            validate_continue_response(200, missing_agent, current, payload)

    def test_200_accepts_openapi_incremental_agent_utterance(self):
        current = start_body()
        payload = build_continue_payload(
            "run", "c1", "Find a dataset.", False, timestamp="2026-10-06T12:00:00+00:00"
        )
        body = {
            "conversation_id": "c1",
            "scenario": scenario(),
            "utterance": {
                "conversation_id": "c1",
                "participant_name": "agent",
                "text": "Please give the download page.",
                "is_final": False,
            },
        }
        value = validate_continue_response(200, body, current, payload)
        self.assertEqual(value["kind"], "continue")
        self.assertEqual(
            value["item"]["chat_messages"][-1]["text"], "Please give the download page."
        )

    def test_incremental_and_full_history_must_agree(self):
        current = start_body()
        payload = build_continue_payload(
            "run", "c1", "Find a dataset.", False, timestamp="2026-10-06T12:00:00+00:00"
        )
        body = continue_body()
        body["utterance"] = {
            "conversation_id": "c1",
            "participant_name": "agent",
            "text": "A different reply.",
            "is_final": False,
        }
        with self.assertRaises(ValueError):
            validate_continue_response(200, body, current, payload)

    def test_incremental_utterance_requires_matching_conversation_id(self):
        current = start_body()
        payload = build_continue_payload(
            "run", "c1", "Find a dataset.", False, timestamp="2026-10-06T12:00:00+00:00"
        )
        for utterance in (
            {"participant_name": "agent", "text": "Reply."},
            {"conversation_id": "wrong", "participant_name": "agent", "text": "Reply."},
        ):
            body = {
                "conversation_id": "c1",
                "scenario": scenario(),
                "utterance": utterance,
            }
            with self.assertRaises(ValueError):
                validate_continue_response(200, body, current, payload)

    def test_full_history_rejects_present_mismatched_message_id(self):
        current = start_body()
        payload = build_continue_payload(
            "run", "c1", "Find a dataset.", False, timestamp="2026-10-06T12:00:00+00:00"
        )
        body = continue_body(user_text="Find a dataset.")
        body["chat_messages"][0]["conversation_id"] = "wrong"
        with self.assertRaises(ValueError):
            validate_continue_response(200, body, current, payload)

    def test_200_rejects_rewritten_or_duplicate_history(self):
        current = start_body()
        payload = build_continue_payload(
            "run", "c1", "Find a dataset.", False, timestamp="2026-10-06T12:00:00+00:00"
        )
        duplicate = continue_body()
        duplicate["chat_messages"].insert(
            0, {"participant_name": "user", "text": "Find a dataset."}
        )
        with self.assertRaises(ValueError):
            validate_continue_response(200, duplicate, current, payload)
        changed = continue_body()
        changed["chat_messages"][0]["text"] = "A different request."
        with self.assertRaises(ValueError):
            validate_continue_response(200, changed, current, payload)

    def test_201_resets_to_empty_new_scenario(self):
        current = start_body()
        payload = build_continue_payload(
            "run", "c1", "Find a dataset.", False, timestamp="2026-10-06T12:00:00+00:00"
        )
        new = validate_continue_response(
            201, start_body("c2", "other"), current, payload
        )
        self.assertEqual(new["item"]["conversation_id"], "c2")
        self.assertEqual(new["item"]["chat_messages"], [])

    def test_201_accepts_openapi_omitted_null_utterance(self):
        current = start_body()
        payload = build_continue_payload(
            "run", "c1", "Find a dataset.", False, timestamp="2026-10-06T12:00:00+00:00"
        )
        body = {"conversation_id": "c2", "scenario": scenario("other")}
        value = validate_continue_response(201, body, current, payload)
        self.assertEqual(value["kind"], "new_conversation")

    def test_final_user_turn_cannot_receive_active_200(self):
        current = start_body()
        payload = build_continue_payload(
            "run", "c1", "Done.", True, timestamp="2026-10-06T12:00:00+00:00"
        )
        with self.assertRaises(ValueError):
            validate_continue_response(
                200, continue_body(user_text="Done."), current, payload
            )

    def test_assistant_final_marker_cannot_receive_active_200(self):
        current = start_body()
        payload = build_continue_payload(
            "run", "c1", "Find a dataset.", False, timestamp="2026-10-06T12:00:00+00:00"
        )
        body = {
            "conversation_id": "c1",
            "scenario": scenario(),
            "utterance": {
                "conversation_id": "c1",
                "participant_name": "agent",
                "text": "No more results.",
                "is_final": True,
            },
        }
        with self.assertRaises(ValueError):
            validate_continue_response(200, body, current, payload)

    def test_201_requires_new_id_and_empty_history(self):
        current = start_body()
        payload = build_continue_payload(
            "run", "c1", "Find a dataset.", True, timestamp="2026-10-06T12:00:00+00:00"
        )
        with self.assertRaises(ValueError):
            validate_continue_response(201, start_body("c1", "other"), current, payload)
        nonempty = start_body("c2", "other")
        nonempty["chat_messages"] = [{"participant_name": "user", "text": "leaked"}]
        with self.assertRaises(ValueError):
            validate_continue_response(201, nonempty, current, payload)
        with self.assertRaises(ValueError):
            validate_continue_response(
                201,
                {
                    "conversation_id": "c2",
                    "scenario": scenario("other"),
                    "utterance": {"participant_name": "agent", "text": "leak"},
                },
                current,
                payload,
            )

    def test_completion_rejects_negated_partial_and_nested_messages(self):
        for detail in (
            "Run not completed",
            "Run has not completed",
            "Run completed partially",
            "Run was finished incorrectly",
            {"status": "completed"},
            "Run does not exist or was completed",
        ):
            with self.subTest(detail=detail):
                self.assertFalse(is_completion(428, {"detail": detail}))

    def test_completion_requires_explicit_finished_text(self):
        self.assertTrue(is_completion(428, {"detail": "Run was finished!"}))
        self.assertTrue(is_completion(428, {"detail": "Run completed"}))
        self.assertFalse(is_completion(428, {"detail": "Run does not exist"}))
        self.assertFalse(is_completion(428, {"detail": "unknown"}))
        self.assertFalse(is_completion(504, {"detail": "completed"}))


class ReceiptTests(unittest.TestCase):
    def test_pending_payload_is_saved_before_organizer_post_and_receipt_reused(self):
        with tempfile.TemporaryDirectory() as td:
            calls = []
            out = Path(td)

            def post(path, payload):
                self.assertTrue((out / "organizer" / "inflight.json").exists())
                calls.append((path, payload))
                return 200, start_body()

            runner = Task2DebugRunner(
                out, run_id="run", organizer_post=post, model_post=lambda _: (200, {})
            )
            value = runner._organizer_call(
                "start", "/task2/debug/start", {"run_id": "run"}
            )
            self.assertEqual(len(calls), 1)
            value2 = runner._organizer_call(
                "start", "/task2/debug/start", {"run_id": "run"}
            )
            self.assertEqual(value, value2)
            self.assertEqual(len(calls), 1)
            self.assertFalse((out / "organizer" / "inflight.json").exists())

    def test_uncertain_pending_request_blocks_resume(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td)
            (out / "organizer").mkdir()
            (out / "organizer" / "inflight.json").write_text(
                json.dumps({"path": "/task2/debug/start"})
            )
            runner = Task2DebugRunner(
                out,
                run_id="run",
                organizer_post=lambda *_: (200, {}),
                model_post=lambda _: (200, {}),
            )
            with self.assertRaises(RuntimeError):
                runner._organizer_call("start", "/task2/debug/start", {"run_id": "run"})

    def test_transport_exception_leaves_pending_and_blocks_retry(self):
        with tempfile.TemporaryDirectory() as td:
            calls = []

            def unavailable(path, payload):
                calls.append((path, payload))
                raise TimeoutError("transport outcome unknown")

            runner = Task2DebugRunner(
                Path(td),
                run_id="run",
                organizer_post=unavailable,
                model_post=lambda _: (200, {}),
            )
            with self.assertRaises(TimeoutError):
                runner._organizer_call("start", "/task2/debug/start", {"run_id": "run"})
            self.assertTrue(runner.pending_path.exists())
            with self.assertRaises(RuntimeError):
                runner._organizer_call("start", "/task2/debug/start", {"run_id": "run"})
            self.assertEqual(len(calls), 1)

    def test_pending_and_receipt_crash_window_blocks_retry(self):
        with tempfile.TemporaryDirectory() as td:
            calls = []
            out = Path(td)

            def post(path, payload):
                calls.append((path, payload))
                return 200, start_body()

            runner = Task2DebugRunner(
                out, run_id="run", organizer_post=post, model_post=lambda _: (200, {})
            )
            runner._organizer_call("start", "/task2/debug/start", {"run_id": "run"})
            runner.pending_path.write_text(json.dumps({"path": "/task2/debug/start"}))
            with self.assertRaises(RuntimeError):
                runner._organizer_call("start", "/task2/debug/start", {"run_id": "run"})
            self.assertEqual(len(calls), 1)

    def test_only_debug_routes_are_allowed(self):
        self.assertEqual(DEBUG_ROUTES, {"/task2/debug/start", "/task2/debug/continue"})
        with tempfile.TemporaryDirectory() as td:
            runner = Task2DebugRunner(
                Path(td),
                run_id="run",
                organizer_post=lambda *_: (200, {}),
                model_post=lambda _: (200, {}),
            )
            with self.assertRaises(ValueError):
                runner._organizer_call("bad", "/task2/run/start", {})

    def test_resume_replays_continue_receipt_without_duplicate_calls(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td)
            organizer_calls = []
            model_calls = []
            responses = [
                (200, start_body()),
                (200, continue_body(user_text="Find a dataset.")),
            ]

            def organizer_post(path, payload):
                organizer_calls.append((path, payload))
                return responses.pop(0)

            def model_post(request):
                model_calls.append(request)
                content = (
                    '{"text":"Find a dataset.","is_final":false}'
                    if request.get("response_format")
                    else "Find a dataset."
                )
                return 200, {
                    "choices": [
                        {"finish_reason": "stop", "message": {"content": content}}
                    ],
                    "usage": {"cost": 0.001},
                }

            first = Task2DebugRunner(
                out,
                run_id="run",
                organizer_post=organizer_post,
                model_post=model_post,
                max_total_turns=1,
                source_files=[],
            )
            original_save = first._save_state
            saves = [0]

            def crash_after_continue(state):
                saves[0] += 1
                if saves[0] == 2:
                    raise RuntimeError("simulated process crash after receipt")
                original_save(state)

            first._save_state = crash_after_continue
            with self.assertRaises(RuntimeError):
                first.run()
            receipt = json.loads((out / "organizer" / "continue-0000.json").read_text())
            submitted_timestamp = receipt["payload"]["user_utterance"]["timestamp"]
            second_organizer_calls = []

            def should_not_post(path, payload):
                second_organizer_calls.append((path, payload))
                raise AssertionError("resume duplicated an organizer request")

            second = Task2DebugRunner(
                out,
                run_id="run",
                organizer_post=should_not_post,
                model_post=model_post,
                max_total_turns=1,
                source_files=[],
            )
            state = second.run()
            self.assertEqual(state["status"], "halted")
            self.assertEqual(len(organizer_calls), 2)
            self.assertEqual(second_organizer_calls, [])
            self.assertEqual(len(model_calls), 2)
            self.assertEqual(
                json.loads((out / "organizer" / "continue-0000.json").read_text())[
                    "payload"
                ]["user_utterance"]["timestamp"],
                submitted_timestamp,
            )

    def test_saved_500_replays_without_model_or_organizer_calls(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td)
            organizer_calls = []
            model_calls = []
            responses = [
                (200, start_body()),
                (500, {"detail": "agent generation failed"}),
            ]

            def organizer_post(path, payload):
                organizer_calls.append((path, payload))
                return responses.pop(0)

            def model_post(request):
                model_calls.append(request)
                content = (
                    '{"text":"Find a dataset.","is_final":false}'
                    if request.get("response_format")
                    else "Find a dataset."
                )
                return 200, {
                    "choices": [
                        {"finish_reason": "stop", "message": {"content": content}}
                    ],
                    "usage": {"cost": 0.001},
                }

            first = Task2DebugRunner(
                out,
                run_id="run",
                organizer_post=organizer_post,
                model_post=model_post,
                source_files=[],
            )
            with self.assertRaises(ValueError):
                first.run()
            before = json.loads(first.state_path.read_text())
            self.assertEqual((len(organizer_calls), len(model_calls)), (2, 2))

            def unexpected(*_args):
                raise AssertionError("saved failure replayed an external call")

            second = Task2DebugRunner(
                out,
                run_id="run",
                organizer_post=unexpected,
                model_post=unexpected,
                source_files=[],
            )
            with self.assertRaises(ValueError):
                second.run()
            self.assertEqual(json.loads(second.state_path.read_text()), before)

    def test_201_and_428_receipts_replay_once_after_state_write_crash(self):
        cases = (
            (201, start_body("c2", "other"), "halted"),
            (428, {"detail": "Run completed"}, "complete"),
        )
        for status, body, expected_status in cases:
            with self.subTest(status=status), tempfile.TemporaryDirectory() as td:
                out = Path(td)
                organizer_calls = []
                model_calls = []
                responses = [(200, start_body()), (status, body)]

                def organizer_post(path, payload):
                    organizer_calls.append((path, payload))
                    return responses.pop(0)

                def model_post(request):
                    model_calls.append(request)
                    content = (
                        '{"text":"Find a dataset.","is_final":false}'
                        if request.get("response_format")
                        else "Find a dataset."
                    )
                    return 200, {
                        "choices": [
                            {"finish_reason": "stop", "message": {"content": content}}
                        ],
                        "usage": {"cost": 0.001},
                    }

                first = Task2DebugRunner(
                    out,
                    run_id="run",
                    organizer_post=organizer_post,
                    model_post=model_post,
                    max_total_turns=1,
                    source_files=[],
                )
                original_save = first._save_state
                saves = [0]

                def crash_after_receipt(state):
                    saves[0] += 1
                    if saves[0] == 2:
                        raise RuntimeError("simulated state-write crash")
                    original_save(state)

                first._save_state = crash_after_receipt
                with self.assertRaises(RuntimeError):
                    first.run()

                def unexpected(*_args):
                    raise AssertionError("receipt replayed an external call")

                second = Task2DebugRunner(
                    out,
                    run_id="run",
                    organizer_post=unexpected,
                    model_post=unexpected,
                    max_total_turns=1,
                    source_files=[],
                )
                state = second.run()
                self.assertEqual(state["status"], expected_status)
                self.assertEqual(state["total_user_turns"], 1)
                self.assertEqual(state["completed_conversations"], 1)
                self.assertEqual((len(organizer_calls), len(model_calls)), (2, 2))
                self.assertEqual(second.run(), state)
                self.assertEqual((len(organizer_calls), len(model_calls)), (2, 2))

    def test_negative_428_replay_leaves_state_unchanged(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td)
            responses = [(200, start_body()), (428, {"detail": "Run not completed"})]

            def organizer_post(_path, _payload):
                return responses.pop(0)

            def model_post(request):
                content = (
                    '{"text":"Continue.","is_final":false}'
                    if request.get("response_format")
                    else "Continue."
                )
                return 200, {
                    "choices": [
                        {"finish_reason": "stop", "message": {"content": content}}
                    ],
                    "usage": {"cost": 0.001},
                }

            first = Task2DebugRunner(
                out,
                run_id="run",
                organizer_post=organizer_post,
                model_post=model_post,
                source_files=[],
            )
            with self.assertRaises(ValueError):
                first.run()
            before = json.loads(first.state_path.read_text())
            self.assertEqual(before["total_user_turns"], 0)

            def unexpected(*_args):
                raise AssertionError("negative completion replayed an external call")

            second = Task2DebugRunner(
                out,
                run_id="run",
                organizer_post=unexpected,
                model_post=unexpected,
                source_files=[],
            )
            with self.assertRaises(ValueError):
                second.run()
            self.assertEqual(json.loads(second.state_path.read_text()), before)

    def test_malformed_model_output_never_sends_continue(self):
        with tempfile.TemporaryDirectory() as td:
            calls = []

            def organizer_post(path, payload):
                calls.append(path)
                return 200, start_body()

            def bad_model(_request):
                return 200, {
                    "choices": [
                        {"finish_reason": "stop", "message": {"content": "not-json"}}
                    ],
                    "usage": {"cost": 0.001},
                }

            runner = Task2DebugRunner(
                Path(td),
                run_id="run",
                organizer_post=organizer_post,
                model_post=bad_model,
                source_files=[],
            )
            with self.assertRaises(ValueError):
                runner.run()
            self.assertEqual(calls, ["/task2/debug/start"])
            self.assertFalse((Path(td) / "organizer" / "continue-0000.json").exists())

    def test_model_pending_blocks_before_start(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td)
            (out / "model").mkdir()
            (out / "model" / "inflight.json").write_text(
                json.dumps({"name": "turn-0000-draft"})
            )
            calls = []
            runner = Task2DebugRunner(
                out,
                run_id="run",
                organizer_post=lambda path, payload: calls.append(path)
                or (200, start_body()),
                model_post=lambda _: (200, {}),
                source_files=[],
            )
            with self.assertRaises(RuntimeError):
                runner.run()
            self.assertEqual(calls, [])


class RunnerFlowTests(unittest.TestCase):
    def test_mock_two_conversation_flow_resets_and_stops(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td)
            organizer_calls = []
            responses = [
                (200, start_body()),
                (200, continue_body()),
                (201, start_body("c2", "other")),
                (428, {"detail": "Run was finished!"}),
            ]

            def organizer_post(path, payload):
                organizer_calls.append((path, payload))
                return responses.pop(0)

            def model_post(request):
                text = '{"text":"Find a dataset.","is_final":false}'
                if request.get("response_format"):
                    return 200, {
                        "choices": [
                            {"finish_reason": "stop", "message": {"content": text}}
                        ],
                        "usage": {"cost": 0.001},
                    }
                return 200, {
                    "choices": [
                        {
                            "finish_reason": "stop",
                            "message": {"content": "Find a dataset."},
                        }
                    ],
                    "usage": {"cost": 0.001},
                }

            runner = Task2DebugRunner(
                out,
                run_id="run",
                organizer_post=organizer_post,
                model_post=model_post,
                cap_usd=3.0,
            )
            # The model sees an editor request after the draft; both return valid text.
            state = runner.run()
            self.assertEqual(state["status"], "complete")
            self.assertEqual(state["total_user_turns"], 3)
            self.assertEqual(state["server_cutoffs"], 2)
            self.assertEqual(state["completed_conversations"], 2)
            self.assertEqual(
                [p for p, _ in organizer_calls],
                [
                    "/task2/debug/start",
                    "/task2/debug/continue",
                    "/task2/debug/continue",
                    "/task2/debug/continue",
                ],
            )
            self.assertTrue(all("/task2/run/" not in p for p, _ in organizer_calls))

    def test_max_turns_halts_without_sending_artificial_final(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td)
            responses = [(200, start_body())]

            def organizer_post(path, payload):
                responses.append((200, continue_body()))
                return responses.pop(0)

            def model_post(request):
                content = (
                    '{"text":"Continue.","is_final":false}'
                    if request.get("response_format")
                    else "Continue."
                )
                return 200, {
                    "choices": [
                        {"finish_reason": "stop", "message": {"content": content}}
                    ],
                    "usage": {"cost": 0.001},
                }

            runner = Task2DebugRunner(
                out,
                run_id="run",
                organizer_post=organizer_post,
                model_post=model_post,
                max_total_turns=0,
            )
            state = runner.run()
            self.assertEqual(state["status"], "halted")
            self.assertEqual(state["total_user_turns"], 0)
            self.assertEqual(len(list((out / "organizer").glob("continue-*.json"))), 0)

    def test_per_conversation_cap_halts_after_real_turn(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td)
            calls = []

            def organizer_post(path, payload):
                calls.append(path)
                if path.endswith("/start"):
                    return 200, start_body()
                return 200, continue_body(user_text=payload["user_utterance"]["text"])

            def model_post(request):
                content = (
                    '{"text":"Find a dataset.","is_final":false}'
                    if request.get("response_format")
                    else "Find a dataset."
                )
                return 200, {
                    "choices": [
                        {"finish_reason": "stop", "message": {"content": content}}
                    ],
                    "usage": {"cost": 0.001},
                }

            runner = Task2DebugRunner(
                out,
                run_id="run",
                organizer_post=organizer_post,
                model_post=model_post,
                max_conversation_turns=1,
                source_files=[],
            )
            state = runner.run()
            self.assertEqual(state["status"], "halted")
            self.assertEqual(state["halt_reason"], "operational_conversation_turn_cap")
            self.assertEqual(calls.count("/task2/debug/continue"), 1)

    def test_final_completion_counts_user_stop(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td)
            calls = []

            def organizer_post(path, payload):
                calls.append(path)
                if path.endswith("/start"):
                    return 200, start_body()
                return 428, {"detail": "Run was finished!"}

            def final_model(request):
                content = (
                    '{"text":"Done.","is_final":true}'
                    if request.get("response_format")
                    else "Done."
                )
                return 200, {
                    "choices": [
                        {"finish_reason": "stop", "message": {"content": content}}
                    ],
                    "usage": {"cost": 0.001},
                }

            runner = Task2DebugRunner(
                out,
                run_id="run",
                organizer_post=organizer_post,
                model_post=final_model,
                source_files=[],
            )
            state = runner.run()
            self.assertEqual(state["status"], "complete")
            self.assertEqual(state["completed_conversations"], 1)
            self.assertEqual(state["user_stops"], 1)


class ManifestTests(unittest.TestCase):
    def test_default_source_closure_includes_loaded_style_dependencies(self):
        # A fresh interpreter avoids accidentally counting test-only imports.
        check = """
import sys
from pathlib import Path
import usersim.task2.debug as runner
root = runner.ROOT.resolve()
frozen = {p.resolve() for p in runner.default_source_files()}
loaded = set()
for module in list(sys.modules.values()):
    filename = getattr(module, '__file__', None)
    if filename:
        path = Path(filename).resolve()
        if path.is_relative_to(root) and '.venv' not in path.parts and path.suffix == '.py':
            loaded.add(path)
missing = sorted(str(p.relative_to(root)) for p in loaded - frozen)
if missing:
    raise RuntimeError('Loaded source absent from manifest: ' + repr(missing))
"""
        result = subprocess.run(
            [sys.executable, "-c", check],
            cwd=debug.ROOT,
            capture_output=True,
            text=True,
            timeout=60,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_runner_freezes_luna_pricing(self):
        with tempfile.TemporaryDirectory() as td:
            runner = Task2DebugRunner(
                Path(td),
                run_id="run",
                organizer_post=lambda *_: (200, {}),
                model_post=lambda _: (200, {}),
                source_files=[],
            )
            self.assertEqual(runner.model.pricing, {MODEL: (0.1, 0.5)})

    def test_manifest_rejects_changed_config(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td)
            first = freeze_manifest(
                out, {"run_id": "run", "cap_usd": 3.0}, source_files=[]
            )
            self.assertEqual(first["config"]["run_id"], "run")
            with self.assertRaises(RuntimeError):
                freeze_manifest(
                    out, {"run_id": "other", "cap_usd": 3.0}, source_files=[]
                )

    def test_manifest_rejects_changed_frozen_source(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            out = root / "out"
            source = root / "source.py"
            source.write_text("VERSION = 1\n")
            freeze_manifest(out, {"run_id": "run"}, source_files=[source])
            source.write_text("VERSION = 2\n")
            with self.assertRaises(RuntimeError):
                freeze_manifest(out, {"run_id": "run"}, source_files=[source])


class MainTests(unittest.TestCase):
    def test_receipt_only_start_recovery_allows_zero_remaining_quota(self):
        class Response:
            status_code = 200

            def __init__(self, body):
                self.body = body

            def json(self):
                return self.body

        class Session:
            def get(self, path, **_kwargs):
                if path.endswith("/auth/verify"):
                    return Response({"team_id": debug.TEAM_ID})
                return Response({"debug": {debug.TASK_NAME: {"remaining": 0}}})

        with tempfile.TemporaryDirectory() as td:
            out = Path(td)
            organizer_calls = []
            model_calls = []

            def organizer_post(path, payload):
                organizer_calls.append((path, payload))
                return 200, start_body()

            def model_post(request):
                model_calls.append(request)
                raise AssertionError("zero-turn recovery called the model")

            runner = Task2DebugRunner(
                out,
                run_id="run",
                organizer_post=organizer_post,
                model_post=model_post,
                max_total_turns=0,
                source_files=[],
            )
            start_payload = {
                "run_id": runner.run_id,
                "task_name": debug.TASK_NAME,
                "description": runner.description,
                "team_id": runner.team_id,
            }
            runner._organizer_call("start", "/task2/debug/start", start_payload)
            organizer_calls.clear()
            with (
                mock.patch.object(debug, "_read_secret", return_value="synthetic"),
                mock.patch.object(
                    debug,
                    "_live_transports",
                    return_value=(organizer_post, model_post, Session()),
                ),
                mock.patch.object(debug, "Task2DebugRunner", return_value=runner),
                mock.patch("builtins.print"),
            ):
                debug.main(["--run", "--output-dir", str(out), "--run-id", "run"])
            self.assertEqual(organizer_calls, [])
            self.assertEqual(model_calls, [])
            state = json.loads(runner.state_path.read_text())
            self.assertEqual(state["status"], "halted")
            self.assertEqual(state["current"]["item"]["conversation_id"], "c1")


if __name__ == "__main__":
    unittest.main()
