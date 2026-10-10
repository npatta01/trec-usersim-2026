import tempfile
import unittest
from pathlib import Path
from usersim.task2.model import CheckpointedModel

REQ = {"messages": [{"role": "user", "content": "Synthetic"}]}


def result():
    return {
        "choices": [{"finish_reason": "stop", "message": {"content": "reply"}}],
        "usage": {"cost": 0.0001},
    }


class TransportTests(unittest.TestCase):
    def test_cached_call_never_repeats(self):
        with tempfile.TemporaryDirectory() as d:
            calls = []

            def post(req):
                calls.append(req)
                return 200, result()

            c = CheckpointedModel(Path(d), 0.1, post)
            self.assertEqual(c.call("one", REQ), "reply")
            self.assertEqual(c.call("one", REQ), "reply")
            self.assertEqual(len(calls), 1)

    def test_timeout_blocks_resume(self):
        with tempfile.TemporaryDirectory() as d:

            def post(req):
                raise TimeoutError()

            c = CheckpointedModel(Path(d), 0.1, post)
            with self.assertRaises(TimeoutError):
                c.call("one", REQ)
            with self.assertRaisesRegex(RuntimeError, "Uncertain"):
                c.call("one", REQ)

    def test_changed_request_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            c = CheckpointedModel(Path(d), 0.1, lambda req: (200, result()))
            c.call("one", REQ)
            with self.assertRaisesRegex(RuntimeError, "changed"):
                c.call("one", {"messages": []})

    def test_budget_blocks_before_transport(self):
        with tempfile.TemporaryDirectory() as d:
            c = CheckpointedModel(
                Path(d), 0.00001, lambda req: self.fail("Network call")
            )
            with self.assertRaisesRegex(RuntimeError, "budget"):
                c.call("one", REQ)
