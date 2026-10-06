import contextlib
import copy
import datetime
import io
import json
import tempfile
import unittest
from pathlib import Path

from usersim.task1 import (
    MODE_ROUTES,
    MODEL,
    Task1Runner,
    _is_task1_completion,
    default_source_files,
    main,
)


ITEM = {
    "conversation_id": "one",
    "scenario": {
        "goal": {"context": "Find letters", "topic": "Latin letters"},
        "persona": {},
        "persona_goal_interaction": {},
    },
    "chat_messages": [
        {"participant_name": "user", "text": "Need letters"},
        {"participant_name": "agent", "text": "Here are scans"},
    ],
}


def model_response(text, *, cost=0.0001):
    return {
        "choices": [{"finish_reason": "stop", "message": {"content": text}}],
        "usage": {"cost": cost},
    }


def runner(out, organizer_post, model_post, **kwargs):
    return Task1Runner(
        Path(out),
        run_id="test-run",
        organizer_post=organizer_post,
        model_post=model_post,
        source_files=[],
        **kwargs,
    )


class Task1FlowTests(unittest.TestCase):
    def test_observed_completion_template_is_exact_and_bound_to_run_id(self):
        detail = 'No more open goals for run "test-run". Run was finished!'
        self.assertTrue(_is_task1_completion(428, {"detail": detail}, "test-run"))
        for body in (
            {
                "detail": 'No more open goals for run "another-run". '
                "Run was finished!"
            },
            {"detail": "Not complete: " + detail},
            {"detail": detail + " Extra text"},
            {"detail": detail, "extra": True},
        ):
            with self.subTest(body=body):
                self.assertFalse(_is_task1_completion(428, body, "test-run"))

        with tempfile.TemporaryDirectory() as td:
            def organizer_post(path, _payload):
                if path.endswith("/start"):
                    return 200, copy.deepcopy(ITEM)
                return 428, {"detail": detail}

            result = runner(
                td,
                organizer_post,
                lambda _request: (200, model_response("Researcher reply")),
                style_postedit=False,
            ).run()
            self.assertEqual(result["status"], "complete")
            self.assertEqual(result["submitted"], 1)

    def test_debug_and_official_routes_edit_and_complete_replay(self):
        for mode in ("debug", "official"):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as td:
                organizer_calls = []
                model_calls = []

                def organizer_post(path, payload):
                    organizer_calls.append((path, copy.deepcopy(payload)))
                    if path == MODE_ROUTES[mode]["start"]:
                        return 200, copy.deepcopy(ITEM)
                    self.assertEqual(path, MODE_ROUTES[mode]["continue"])
                    self.assertEqual(
                        payload["user_utterance"]["text"], "Edited researcher reply"
                    )
                    return 428, {"detail": "Run completed"}

                def model_post(request):
                    model_calls.append(copy.deepcopy(request))
                    text = (
                        "Draft researcher reply"
                        if len(model_calls) == 1
                        else "Edited researcher reply"
                    )
                    return 200, model_response(text)

                task = runner(td, organizer_post, model_post, mode=mode)
                result = task.run()
                self.assertEqual(result["status"], "complete")
                self.assertEqual(result["mode"], mode)
                self.assertEqual(result["submitted"], 1)
                self.assertEqual(result["model_calls"], 2)
                self.assertLessEqual(result["spent_usd"], result["reserved_usd"])
                self.assertEqual(
                    [path for path, _ in organizer_calls],
                    [MODE_ROUTES[mode]["start"], MODE_ROUTES[mode]["continue"]],
                )
                self.assertEqual(model_calls[0]["model"], MODEL)
                editor = json.loads(model_calls[1]["messages"][1]["content"])
                self.assertEqual(editor["draft"], "Draft researcher reply")
                self.assertEqual(
                    editor["researcher_last_two_messages"], ["Need letters"]
                )

                case = json.loads((Path(td) / "case-0000.json").read_text())
                receipt = json.loads(
                    (Path(td) / "organizer" / "continue-0000.json").read_text()
                )
                self.assertEqual(case["submission_request"], receipt["payload"])
                stamp = case["submission_request"]["user_utterance"]["timestamp"]
                self.assertIsNotNone(datetime.datetime.fromisoformat(stamp).tzinfo)

                before = (len(organizer_calls), len(model_calls))
                self.assertEqual(task.run(), result)
                self.assertEqual((len(organizer_calls), len(model_calls)), before)

    def test_201_distinct_nonempty_target_replaces_context_without_id_inference(self):
        with tempfile.TemporaryDirectory() as td:
            second = copy.deepcopy(ITEM)
            second["scenario"]["goal"]["context"] = "NEW GOAL"
            second["chat_messages"] = [
                {"participant_name": "user", "text": "New question"},
                {"participant_name": "agent", "text": "New assistant reply"},
            ]
            organizer_count = 0
            model_requests = []

            def organizer_post(path, _payload):
                nonlocal organizer_count
                if path.endswith("/start"):
                    return 200, copy.deepcopy(ITEM)
                organizer_count += 1
                if organizer_count == 1:
                    return 201, copy.deepcopy(second)
                return 428, {"detail": "Run was finished!"}

            def model_post(request):
                model_requests.append(copy.deepcopy(request))
                return 200, model_response("Researcher reply")

            result = runner(td, organizer_post, model_post, style_postedit=False).run()
            self.assertEqual(result["submitted"], 2)
            rendered = json.dumps(model_requests[1], ensure_ascii=False)
            self.assertIn("NEW GOAL", rendered)
            self.assertIn("New assistant reply", rendered)
            self.assertNotIn("Need letters", rendered)
            self.assertNotIn("Here are scans", rendered)

    def test_missing_history_is_rejected_before_model_call(self):
        with tempfile.TemporaryDirectory() as td:
            missing = copy.deepcopy(ITEM)
            missing.pop("chat_messages")
            model_calls = []

            task = runner(
                td,
                lambda _path, _payload: (200, missing),
                lambda request: model_calls.append(request) or (200, {}),
                style_postedit=False,
            )
            with self.assertRaisesRegex(RuntimeError, "chat_messages"):
                task.run()
            self.assertEqual(model_calls, [])

    def test_stale_200_target_ignores_message_metadata(self):
        with tempfile.TemporaryDirectory() as td:
            organizer_calls = []
            model_calls = []
            stale = copy.deepcopy(ITEM)
            stale["chat_messages"][0]["timestamp"] = "metadata-only-change"
            stale["chat_messages"][1]["annotations"] = {"new": True}

            def organizer_post(path, _payload):
                organizer_calls.append(path)
                if path.endswith("/start"):
                    return 200, copy.deepcopy(ITEM)
                return 200, copy.deepcopy(stale)

            def model_post(_request):
                model_calls.append(True)
                return 200, model_response("OUR PREDICTION")

            task = runner(
                td, organizer_post, model_post, style_postedit=False
            )
            with self.assertRaisesRegex(RuntimeError, "advance"):
                task.run()
            self.assertEqual(len(organizer_calls), 2)
            self.assertEqual(len(model_calls), 1)
            self.assertFalse(task.result_path.exists())

    def test_200_new_conversation_id_accepts_identical_context(self):
        with tempfile.TemporaryDirectory() as td:
            second = copy.deepcopy(ITEM)
            second["conversation_id"] = "two"
            organizer_count = 0
            model_calls = []

            def organizer_post(path, _payload):
                nonlocal organizer_count
                if path.endswith("/start"):
                    return 200, copy.deepcopy(ITEM)
                organizer_count += 1
                if organizer_count == 1:
                    return 200, copy.deepcopy(second)
                return 428, {"detail": "Run completed"}

            def model_post(request):
                model_calls.append(copy.deepcopy(request))
                return 200, model_response("Researcher reply")

            result = runner(
                td, organizer_post, model_post, style_postedit=False
            ).run()
            self.assertEqual(result["submitted"], 2)
            self.assertEqual(len(model_calls), 2)

    def test_200_extension_uses_actual_human_turn_not_prediction(self):
        with tempfile.TemporaryDirectory() as td:
            extended = copy.deepcopy(ITEM)
            extended["chat_messages"][0]["timestamp"] = "old-user-time"
            extended["chat_messages"][1]["annotations"] = {"helpful": True}
            extended["chat_messages"].extend(
                [
                    {"participant_name": "user", "text": "HUMAN ACTUAL"},
                    {"participant_name": "agent", "text": "New agent reply"},
                ]
            )
            organizer_count = 0
            model_requests = []

            def organizer_post(path, _payload):
                nonlocal organizer_count
                if path.endswith("/start"):
                    return 200, copy.deepcopy(ITEM)
                organizer_count += 1
                if organizer_count == 1:
                    return 200, copy.deepcopy(extended)
                return 428, {"detail": "Run completed"}

            def model_post(request):
                model_requests.append(copy.deepcopy(request))
                text = "OUR PREDICTION" if len(model_requests) == 1 else "SECOND"
                return 200, model_response(text)

            result = runner(
                td, organizer_post, model_post, style_postedit=False
            ).run()
            self.assertEqual(result["submitted"], 2)
            second_request = json.dumps(model_requests[1], ensure_ascii=False)
            self.assertIn("HUMAN ACTUAL", second_request)
            self.assertIn("New agent reply", second_request)
            self.assertNotIn("OUR PREDICTION", second_request)

    def test_invalid_completion_is_saved_and_replayed_without_calls(self):
        with tempfile.TemporaryDirectory() as td:
            organizer_calls = []
            model_calls = []

            def organizer_post(path, _payload):
                organizer_calls.append(path)
                if path.endswith("/start"):
                    return 200, copy.deepcopy(ITEM)
                return 428, {"detail": "Run not completed"}

            def model_post(_request):
                model_calls.append(True)
                return 200, model_response("Researcher reply")

            first = runner(td, organizer_post, model_post, style_postedit=False)
            with self.assertRaises(RuntimeError):
                first.run()
            self.assertFalse((Path(td) / "result.json").exists())
            before = (len(organizer_calls), len(model_calls))

            def unexpected(*_args):
                raise AssertionError("saved invalid response made an external call")

            second = runner(td, unexpected, unexpected, style_postedit=False)
            with self.assertRaises(RuntimeError):
                second.run()
            self.assertEqual((len(organizer_calls), len(model_calls)), before)

    def test_uncertain_continue_blocks_retry_and_preserves_timestamp(self):
        with tempfile.TemporaryDirectory() as td:
            calls = []

            def organizer_post(path, payload):
                calls.append((path, copy.deepcopy(payload)))
                if path.endswith("/start"):
                    return 200, copy.deepcopy(ITEM)
                raise TimeoutError("unknown organizer outcome")

            def model_post(_request):
                return 200, model_response("Researcher reply")

            first = runner(td, organizer_post, model_post, style_postedit=False)
            with self.assertRaises(TimeoutError):
                first.run()
            out = Path(td)
            pending = json.loads((out / "organizer" / "inflight.json").read_text())
            case = json.loads((out / "case-0000.json").read_text())
            self.assertEqual(pending["payload"], case["submission_request"])

            def unexpected(*_args):
                raise AssertionError("uncertain request was retried")

            with self.assertRaisesRegex(RuntimeError, "Uncertain organizer"):
                runner(td, unexpected, unexpected, style_postedit=False).run()
            self.assertEqual(len(calls), 2)

    def test_wrong_mode_route_is_rejected_before_transport(self):
        with tempfile.TemporaryDirectory() as td:
            calls = []
            task = runner(
                td,
                lambda *args: calls.append(args) or (200, {}),
                lambda _request: (200, {}),
                mode="official",
            )
            with self.assertRaises(ValueError):
                task._organizer_call("bad", "/task1/debug/start", {})
            self.assertEqual(calls, [])


class Task1CostAndFreezeTests(unittest.TestCase):
    def test_bool_and_over_reservation_costs_are_rejected(self):
        for cost in (False, 1.0):
            with self.subTest(cost=cost), tempfile.TemporaryDirectory() as td:
                organizer_paths = []

                def organizer_post(path, _payload):
                    organizer_paths.append(path)
                    return 200, copy.deepcopy(ITEM)

                def model_post(_request):
                    return 200, model_response("Researcher reply", cost=cost)

                task = runner(td, organizer_post, model_post, style_postedit=False)
                with self.assertRaises(RuntimeError):
                    task.run()
                self.assertEqual(organizer_paths, [MODE_ROUTES["debug"]["start"]])
                self.assertFalse(task.model.has_pending())
                self.assertTrue((Path(td) / "model" / "case-0000-draft.json").exists())

    def test_cap_is_checked_before_model_transport(self):
        with tempfile.TemporaryDirectory() as td:
            organizer_paths = []
            model_calls = []

            def organizer_post(path, _payload):
                organizer_paths.append(path)
                return 200, copy.deepcopy(ITEM)

            task = runner(
                td,
                organizer_post,
                lambda request: model_calls.append(request) or (200, {}),
                style_postedit=False,
                cap_usd=0.00001,
            )
            with self.assertRaisesRegex(RuntimeError, "budget cap"):
                task.run()
            self.assertEqual(organizer_paths, [MODE_ROUTES["debug"]["start"]])
            self.assertEqual(model_calls, [])

    def test_changed_source_refuses_resume_before_calls(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = root / "source.py"
            source.write_text("VERSION = 1\n")

            def organizer_post(path, _payload):
                if path.endswith("/start"):
                    return 200, copy.deepcopy(ITEM)
                return 428, {"detail": "Run completed"}

            task = Task1Runner(
                root / "out",
                run_id="test-run",
                organizer_post=organizer_post,
                model_post=lambda _request: (200, model_response("Reply")),
                style_postedit=False,
                source_files=[source],
            )
            task.run()
            source.write_text("VERSION = 2\n")

            def unexpected(*_args):
                raise AssertionError("changed source made an external call")

            resumed = Task1Runner(
                root / "out",
                run_id="test-run",
                organizer_post=unexpected,
                model_post=unexpected,
                style_postedit=False,
                source_files=[source],
            )
            with self.assertRaisesRegex(RuntimeError, "source changed"):
                resumed.run()

    def test_default_source_freeze_covers_import_closure(self):
        relative = {
            str(path.relative_to(Path(__file__).resolve().parents[1]))
            for path in default_source_files()
        }
        self.assertEqual(
            relative,
            {
                "scripts/run_task1.py",
                "usersim/__init__.py",
                "usersim/task1.py",
                "usersim/prompts.py",
                "usersim/requests.py",
                "usersim/checkpoints.py",
                "usersim/task2/__init__.py",
                "usersim/task2/model.py",
                "usersim/task2/protocol.py",
                "simulator/src/scenario.py",
            },
        )


class Task1CliTests(unittest.TestCase):
    def test_dry_preview_defaults_to_debug_without_creating_output(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "private-output"
            stdout = io.StringIO()
            with contextlib.redirect_stdout(stdout):
                value = main(
                    [
                        "--run-id",
                        "preview-run",
                        "--output-dir",
                        str(out),
                    ]
                )
            preview = json.loads(stdout.getvalue())
            self.assertIsNone(value)
            self.assertTrue(preview["dry_run"])
            self.assertEqual(preview["mode"], "debug")
            self.assertEqual(preview["routes"], MODE_ROUTES["debug"])
            self.assertEqual(preview["cap_usd"], 1.0)
            self.assertFalse(out.exists())


if __name__ == "__main__":
    unittest.main()
