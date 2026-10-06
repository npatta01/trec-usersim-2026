"""Checkpointed model calls, independent of Task 2 prompts and conversation state."""

import json
import math
import os
import re
from pathlib import Path
from run_single_call_prompt_comparison import atomic, digest, validate


class CheckpointedModel:
    """Caller must hold a run-level process lock for this directory."""

    def __init__(self, out, cap_usd, post, *, pricing=None):
        if not math.isfinite(cap_usd) or cap_usd <= 0:
            raise ValueError("Invalid model budget")
        self.out = Path(out)
        self.cap = cap_usd
        self.post = post
        self.pricing = None if pricing is None else dict(pricing)
        if self.pricing is not None:
            for rates in self.pricing.values():
                if len(rates) != 2 or any(type(v) not in (int, float) or not math.isfinite(v) or v <= 0 for v in rates):
                    raise ValueError("Invalid per-million token prices")
        os.umask(0o077)
        self.out.mkdir(parents=True, exist_ok=True)

    def reservation(self, request):
        input_rate, output_rate = 0.1, 0.5
        output_limit = 4096
        if self.pricing is not None:
            if request.get("model") not in self.pricing:
                raise ValueError("Model has no frozen price")
            input_rate, output_rate = self.pricing[request["model"]]
            limits = [request[k] for k in ("max_tokens", "max_completion_tokens") if k in request]
            if len(limits) != 1 or type(limits[0]) is not int or not 0 < limits[0] <= 4096:
                raise ValueError("Expected one bounded output token limit")
            output_limit = limits[0]
            provider = request.get("provider", {})
            if provider.get("max_price") != {"prompt": input_rate, "completion": output_rate}:
                raise ValueError("Provider caps differ from reserved prices")
        return ((len(json.dumps(request, ensure_ascii=False).encode()) + 4096)
                * input_rate / 1e6 + output_limit * output_rate / 1e6)

    def _valid(self, saved):
        if saved["status"] != 200:
            raise RuntimeError("Model HTTP failure")
        text = validate(saved["response"])
        cost = saved["response"].get("usage", {}).get("cost")
        if (
            not isinstance(cost, (int, float))
            or not math.isfinite(cost)
            or not 0 <= cost <= saved["reserve_usd"]
        ):
            raise RuntimeError("Missing or out-of-reservation model cost")
        return text

    def call(self, name, request):
        if not re.fullmatch(r"[a-zA-Z0-9_-]+", name):
            raise ValueError("Invalid checkpoint name")
        pending = self.out / "inflight.json"
        dest = self.out / (name + ".json")
        if pending.exists():
            raise RuntimeError("Uncertain model request; reconcile before resuming")
        h = digest(request)
        if dest.exists():
            saved = json.loads(dest.read_text())
            if saved["request_sha256"] != h:
                raise RuntimeError("Checkpoint request changed")
            return self._valid(saved)
        used = sum(
            json.loads(f.read_text())["reserve_usd"] for f in self.out.glob("*.json")
        )
        reserve = self.reservation(request)
        if used + reserve > self.cap:
            raise RuntimeError("Model budget cap reached")
        atomic(pending, {"name": name, "request": request, "reserve_usd": reserve})
        status, raw = self.post(request)
        saved = {
            "request": request,
            "request_sha256": h,
            "status": status,
            "response": raw,
            "reserve_usd": reserve,
        }
        atomic(dest, saved)
        text = self._valid(saved)
        pending.unlink()
        return text
