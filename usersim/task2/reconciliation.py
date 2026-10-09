"""Shared verified session reconciliation and progress accounting."""

import copy
import json
from datetime import datetime

from usersim.checkpoints import atomic, digest
from .protocol import same_json

OPERATIONAL_POLICY = {
    "max_skips": 24,
    "max_skip_fraction": 0.25,
    "fraction_warmup_conversations": 8,
    "max_consecutive_skips": 3,
}


def _advance(state, result, *, is_final, skipped):
    state = copy.deepcopy(state)
    if skipped:
        state["skipped_conversations"] = state.get("skipped_conversations", 0) + 1
        state["consecutive_operational_skips"] = (
            state.get("consecutive_operational_skips", 0) + 1
        )
        state["operational_closing_turns"] = (
            state.get("operational_closing_turns", 0) + 1
        )
        state["accepted_error_turns"] = state.get("accepted_error_turns", 0) + 1
    elif result["kind"] in {"new_conversation", "complete"}:
        state["consecutive_operational_skips"] = 0
        state["completed_conversations"] += 1
        state["user_stops" if is_final else "server_cutoffs"] += 1
    state["total_user_turns"] += 2 if skipped else 1
    state["status"] = "complete" if result["kind"] == "complete" else "running"
    state.pop("halt_reason", None)
    if result["kind"] == "complete":
        state["current"] = None
    else:
        turns = (
            0 if result["kind"] == "new_conversation" else state["current"]["turns"] + 1
        )
        state["current"] = {"item": result["item"], "turns": turns}
    return state


def _verify_message_fields(expected, actual):
    """Compare available raw transport fields, allowing equivalent UTC spelling."""
    if not isinstance(actual, dict):
        raise RuntimeError("Server message is not an object")
    for key, value in expected.items():
        if key not in actual:
            raise RuntimeError(f"Server message omitted {key}")
        if key == "timestamp":
            try:
                match = datetime.fromisoformat(value) == datetime.fromisoformat(
                    actual[key]
                )
            except (ValueError, TypeError):
                match = False
        else:
            match = same_json(value, actual[key])
        if not match:
            raise RuntimeError(f"Server message changed {key}")


def _verify_raw_prefix(runner, index, remote_messages, conversation_id):
    """Verify raw submitted user fields and recorded incremental agent fields."""
    expected = []
    events = {
        p.name: p for p in (runner.out / "reconciliation").glob("continue-*.json")
    }
    paths = [
        p for p in runner.organizer_dir.glob("continue-*.json") if p.name not in events
    ]
    paths += list(events.values())
    for path in sorted(paths, key=lambda p: int(p.stem.split("-")[-1])):
        number = int(path.stem.split("-")[-1])
        if number > index:
            continue
        receipt = json.loads(path.read_text())
        if path.parent.name == "reconciliation":
            if receipt.get("kind") != "session_reply" or digest(
                receipt["server_session"]
            ) != receipt.get("server_session_sha256"):
                raise RuntimeError("Invalid delayed-reply reconciliation event")
            origin = receipt.get("origin")
            if origin not in {"ReadTimeout", "HTTP500", "HTTP502"}:
                raise RuntimeError("Unsupported delayed-reply source")
            source = runner.organizer_dir / (
                f"transport-error-{path.name}" if origin == "ReadTimeout" else path.name
            )
            if receipt.get("source_proof") != str(source.relative_to(runner.out)):
                raise RuntimeError("Unexpected delayed-reply proof path")
            if not source.is_file() or digest(
                json.loads(source.read_text())
            ) != receipt.get("source_proof_sha256"):
                raise RuntimeError("Delayed-reply original proof changed")
            proof = json.loads(source.read_text())
            if (
                proof.get("request_sha256") != receipt.get("request_sha256")
                or proof.get("path") != runner.continue_path
            ):
                raise RuntimeError("Delayed reply differs from original request")
            if origin == "ReadTimeout":
                if (
                    proof.get("type") != origin
                    or proof.get("checkpoint_name") != path.stem
                ):
                    raise RuntimeError("Delayed-reply transport proof mismatch")
            elif proof.get("status") != int(origin[4:]) or not same_json(
                proof.get("payload"), receipt.get("payload")
            ):
                raise RuntimeError("Delayed-reply HTTP proof mismatch")
            original = runner.organizer_dir / path.name
            if original.exists() and json.loads(original.read_text()).get(
                "request_sha256"
            ) != receipt.get("request_sha256"):
                raise RuntimeError("Delayed reply differs from original request")
            receipt = {**receipt, "body": receipt["server_session"]}
        if receipt["payload"]["user_utterance"]["conversation_id"] != conversation_id:
            continue
        if (
            receipt.get("path") != runner.continue_path
            or receipt["payload"].get("run_id") != runner.run_id
            or digest(receipt["payload"]) != receipt["request_sha256"]
        ):
            raise RuntimeError("Prior request integrity mismatch")
        expected.append(receipt["payload"]["user_utterance"])
        body = receipt.get("body")
        if number < index and isinstance(body, dict):
            reply = body.get("utterance")
            if isinstance(reply, dict):
                expected.append(reply)
            elif isinstance(body.get("chat_messages"), list):
                expected = body["chat_messages"]
            else:
                raise RuntimeError("No prior reply metadata available for recovery")
    if len(remote_messages) < len(expected):
        raise RuntimeError("Server prefix is incomplete")
    for old, current in zip(expected, remote_messages):
        _verify_message_fields(old, current)


def check_skip_bounds(runner, state, *, max_skips=24):
    """Circuit and evidence-quality bounds, distinct from researcher behavior."""
    skipped = state.get("skipped_conversations", 0) + 1
    total = state["completed_conversations"] + skipped
    if (
        skipped > max_skips
        or skipped / max(total, OPERATIONAL_POLICY["fraction_warmup_conversations"])
        > OPERATIONAL_POLICY["max_skip_fraction"]
    ):
        raise RuntimeError("Operational skip/evidence-quality bound reached")
    if (
        state.get("consecutive_operational_skips", 0) + 1
        > OPERATIONAL_POLICY["max_consecutive_skips"]
    ):
        raise RuntimeError("Consecutive backend-error circuit bound reached")
    if (
        state["total_user_turns"] + 2 > runner.max_total_turns
        or state["current"]["turns"] + 2 > runner.max_conversation_turns
    ):
        raise RuntimeError("Operational close would exceed frozen turn limits")


def persist_reply_event(runner, index, payload, remote, *, origin):
    """Retain a GET-derived reply separately from original POST receipts."""
    folder = runner.out / "reconciliation"
    folder.mkdir(exist_ok=True)
    event = {
        "kind": "session_reply",
        "origin": origin,
        "path": runner.continue_path,
        "payload": payload,
        "request_sha256": digest(payload),
        "server_session": remote,
        "server_session_sha256": digest(remote),
    }
    source = runner.organizer_dir / (
        f"transport-error-continue-{index:04d}.json"
        if origin == "ReadTimeout"
        else f"continue-{index:04d}.json"
    )
    event["source_proof"] = str(source.relative_to(runner.out))
    event["source_proof_sha256"] = digest(json.loads(source.read_text()))
    path = folder / f"continue-{index:04d}.json"
    if path.exists() and not same_json(json.loads(path.read_text()), event):
        raise RuntimeError("Delayed-reply evidence changed")
    atomic(path, event)
