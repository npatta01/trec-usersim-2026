import tempfile
import unittest
from pathlib import Path

from task2_model import CheckpointedModel


def response(text="reply", cost=0.0001):
    return {
        "choices": [{"finish_reason": "stop", "message": {"content": text}}],
        "usage": {"cost": cost},
    }


REQ = {"messages": [{"role": "user", "content": "Synthetic"}]}
MODEL = "openai/gpt-6-luna"


def priced_request(model=MODEL, *, max_completion_tokens=4, max_price=None):
    return {
        "model": model,
        "messages": [{"role": "user", "content": "Synthetic"}],
        "max_completion_tokens": max_completion_tokens,
        "provider": {"max_price": max_price or {"prompt": 0.1, "completion": 0.5}},
    }


class PendingAndReceiptTests(unittest.TestCase):
    def test_http_failure_receipt_is_cached_and_pending_clears_before_validation(self):
        with tempfile.TemporaryDirectory() as td:
            calls = []

            def post(request):
                calls.append(request)
                return 503, {"detail": "temporarily unavailable"}

            client = CheckpointedModel(Path(td), 0.1, post)
            with self.assertRaisesRegex(RuntimeError, "HTTP"):
                client.call("failed", REQ)
            self.assertFalse(client.has_pending())
            with self.assertRaisesRegex(RuntimeError, "HTTP"):
                client.call("failed", REQ)
            self.assertEqual(len(calls), 1)

    def test_malformed_http_200_receipt_is_cached_and_not_reposted(self):
        with tempfile.TemporaryDirectory() as td:
            calls = []

            def post(request):
                calls.append(request)
                return 200, {"choices": []}

            client = CheckpointedModel(Path(td), 0.1, post)
            with self.assertRaises((KeyError, IndexError, ValueError, RuntimeError)):
                client.call("malformed", REQ)
            self.assertFalse(client.has_pending())
            with self.assertRaises((KeyError, IndexError, ValueError, RuntimeError)):
                client.call("malformed", REQ)
            self.assertEqual(len(calls), 1)

    def test_transport_exception_remains_uncertain(self):
        with tempfile.TemporaryDirectory() as td:
            calls = []

            def post(request):
                calls.append(request)
                raise TimeoutError("network timeout")

            client = CheckpointedModel(Path(td), 0.1, post)
            with self.assertRaises(TimeoutError):
                client.call("uncertain", REQ)
            self.assertTrue(client.has_pending())
            with self.assertRaisesRegex(RuntimeError, "Uncertain"):
                client.call("uncertain", REQ)
            self.assertEqual(len(calls), 1)

    def test_totals_match_runner_accounting(self):
        with tempfile.TemporaryDirectory() as td:
            calls = []

            def post(request):
                calls.append(request)
                if len(calls) == 1:
                    return 200, response(cost=0.0002)
                return 503, {"detail": "failure"}

            client = CheckpointedModel(Path(td), 0.1, post)
            self.assertEqual(client.call("ok", REQ), "reply")
            with self.assertRaises(RuntimeError):
                client.call("bad", REQ)
            totals = client.totals()
            self.assertEqual(totals["model_calls"], 1)
            self.assertAlmostEqual(totals["spent_usd"], 0.0002)
            expected_reserve = client.reservation(REQ) * 2
            self.assertAlmostEqual(totals["reserved_usd"], expected_reserve)

    def test_pending_marker_blocks_even_when_receipt_exists(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td)
            client = CheckpointedModel(out, 0.1, lambda request: (503, {"detail": "failure"}))
            with self.assertRaises(RuntimeError):
                client.call("failed", REQ)
            (out / "inflight.json").write_text('{"name":"failed"}')
            with self.assertRaisesRegex(RuntimeError, "Uncertain"):
                client.call("failed", REQ)


class PricingGuardTests(unittest.TestCase):
    def test_pricing_guards_fail_before_network(self):
        with tempfile.TemporaryDirectory() as td:
            calls = []

            def post(request):
                calls.append(request)
                return 200, response()

            client = CheckpointedModel(Path(td), 0.1, post, pricing={MODEL: (0.1, 0.5)})
            cases = [
                priced_request("other/model"),
                priced_request(max_price={"prompt": 0.2, "completion": 0.5}),
                priced_request(max_completion_tokens=0),
                {"model": MODEL, "messages": [], "provider": {"max_price": {"prompt": 0.1, "completion": 0.5}}},
                {"model": MODEL, "messages": [], "max_tokens": 4, "max_completion_tokens": 4, "provider": {"max_price": {"prompt": 0.1, "completion": 0.5}}},
            ]
            for request in cases:
                with self.assertRaises(ValueError):
                    client.call("guard", request)
                self.assertFalse(client.has_pending())
            self.assertEqual(calls, [])


if __name__ == "__main__":
    unittest.main()
