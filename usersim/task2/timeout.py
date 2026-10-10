"""Reconcile classified original request timeouts without reposting them."""

import json
import time
from datetime import datetime, timezone

from usersim.checkpoints import atomic, digest
from .protocol import (
    build_continue_payload,
    normalize_item,
    same_json,
    validate_continue_response,
)
from .reconciliation import (
    _advance,
    _verify_message_fields,
    _verify_raw_prefix,
    check_skip_bounds,
    persist_reply_event,
)

TIMEOUT_POLICY = {"grace_seconds": 1800, "poll_seconds": 30, "max_polls": 65}


def recover_timeout(runner, get_session, *, max_skips=24, now=None, wait=None):
    """Wait for a delayed reply, then close one proven unanswered original turn.

    Only a matching durable ReadTimeout classification is eligible. The grace
    starts at the first exact persisted-turn observation. Closing uncertainty,
    unknown inflight calls, malformed history and changed evidence always halt.
    Clock/wait and read-only session access are injected for offline verification.
    """
    now = now or (lambda: datetime.now(timezone.utc))
    wait = wait or time.sleep
    state = runner._load_state()
    if state["status"] not in {"halted", "running"} or runner.model.has_pending():
        raise RuntimeError("No eligible original organizer timeout")
    index = state["total_user_turns"]
    name = f"continue-{index:04d}"
    proof_path = runner.organizer_dir / f"transport-error-{name}.json"
    if not proof_path.exists():
        raise RuntimeError("Unknown inflight request has no timeout classification")
    proof = json.loads(proof_path.read_text())
    log = runner.out / "recovery"
    log.mkdir(exist_ok=True)
    archive = log / f"{index:04d}-timeout-original-inflight.json"
    intent_path = log / f"{index:04d}-timeout-intent.json"
    result_path = log / f"{index:04d}-timeout-result.json"
    observation_path = log / f"{index:04d}-timeout-observation.json"
    closing_pending = None
    if runner.pending_path.exists():
        pending = json.loads(runner.pending_path.read_text())
        if pending.get("checkpoint_name") == f"continue-{index + 1:04d}":
            # A durable response can precede removal of its pending marker.
            # Only the bound intent/receipt below may prove this close resolved.
            closing_pending = pending
            if not archive.exists():
                raise RuntimeError("Closing pending has no original timeout archive")
            pending = json.loads(archive.read_text())
    elif archive.exists():
        pending = json.loads(archive.read_text())
    else:
        raise RuntimeError("Original timeout request unavailable")
    payload = pending["payload"]
    request_hash = digest(payload)
    if (
        proof.get("type") != "ReadTimeout"
        or proof.get("path") != runner.continue_path
        or proof.get("checkpoint_name") != name
        or proof.get("request_sha256") != request_hash
        or pending.get("path") != runner.continue_path
        or pending.get("checkpoint_name") != name
        or pending.get("request_sha256") != request_hash
        or payload.get("run_id") != runner.run_id
    ):
        raise RuntimeError("Timeout proof mismatch or uncertain operational close")
    current = runner._current_item(state)
    if payload["user_utterance"]["conversation_id"] != current["conversation_id"]:
        raise RuntimeError("Timed-out conversation differs from checkpoint")
    binding = {
        "request_sha256": request_hash,
        "transport_sha256": digest(proof),
        "previous_state_sha256": digest(state),
    }

    def archive_pending():
        if archive.exists() and digest(json.loads(archive.read_text())) != digest(
            pending
        ):
            raise RuntimeError("Archived original timeout changed")
        atomic(archive, pending)
        if runner.pending_path.exists():
            if digest(json.loads(runner.pending_path.read_text())) != digest(pending):
                raise RuntimeError("A different request is uncertain")
            runner.pending_path.unlink()

    def commit(result, *, remote=None, closing=None):
        skipped = closing is not None
        if skipped and result["kind"] not in {"new_conversation", "complete"}:
            raise RuntimeError("Operational close did not confirm advancement")
        if not skipped and result["kind"] == "continue":
            persist_reply_event(runner, index, payload, remote, origin="ReadTimeout")
        recovered = _advance(
            state,
            result,
            is_final=payload["user_utterance"]["is_final"],
            skipped=skipped,
        )
        runner._store_model_totals(recovered)
        evidence = {
            **binding,
            "kind": result["kind"],
            "skipped": skipped,
            "server_session": remote,
            "server_session_sha256": digest(remote),
            "recovered_state": recovered,
            "recovered_state_sha256": digest(recovered),
        }
        if closing is not None:
            evidence["closing_receipt_sha256"] = digest(closing)
        atomic(result_path, evidence)
        archive_pending()
        runner._save_state(recovered)
        print(
            json.dumps(
                {
                    "event": "task2_timeout_reconciled",
                    "turn_index": index,
                    "kind": result["kind"],
                    "operational_skip": skipped,
                }
            ),
            flush=True,
        )
        error = runner.out / "error.json"
        if error.exists():
            error.replace(log / f"{index:04d}-timeout-previous-error.json")
        return recovered

    def check_binding(document):
        if any(document.get(k) != v for k, v in binding.items()):
            raise RuntimeError(
                "Timeout recovery evidence belongs to another checkpoint"
            )

    def check_observation(document):
        check_binding(document)
        content = {k: v for k, v in document.items() if k != "observation_sha256"}
        if digest(content) != document.get("observation_sha256"):
            raise RuntimeError("Timeout observation integrity mismatch")

    def read_intent():
        intent = json.loads(intent_path.read_text())
        check_binding(intent)
        observation = json.loads(observation_path.read_text())
        check_observation(observation)
        if digest(observation) != intent.get("observation_sha256") or digest(
            intent["closing_payload"]
        ) != intent.get("closing_payload_sha256"):
            raise RuntimeError("Timeout closing intent integrity mismatch")
        closing = intent["closing_payload"]
        if (
            closing.get("run_id") != runner.run_id
            or closing.get("user_utterance", {}).get("conversation_id")
            != current["conversation_id"]
            or closing["user_utterance"].get("is_final") is not True
        ):
            raise RuntimeError("Invalid operational closing intent")
        return intent

    close_name = f"continue-{index + 1:04d}"
    close_path = runner.organizer_dir / f"{close_name}.json"

    def replay_close(intent, *, expected_hash=None):
        receipt = json.loads(close_path.read_text())
        closing = intent["closing_payload"]
        closing_hash = digest(closing)
        if (
            receipt.get("path") != runner.continue_path
            or receipt.get("request_sha256") != closing_hash
            or not same_json(receipt.get("payload"), closing)
            or (expected_hash is not None and digest(receipt) != expected_hash)
        ):
            raise RuntimeError("Closing receipt changed")
        result = validate_continue_response(
            receipt["status"], receipt["body"], current, closing
        )
        if result["kind"] not in {"new_conversation", "complete"}:
            raise RuntimeError("Operational close did not confirm advancement")
        if closing_pending is not None:
            if (
                closing_pending.get("path") != runner.continue_path
                or closing_pending.get("checkpoint_name") != close_name
                or closing_pending.get("request_sha256") != closing_hash
                or not same_json(closing_pending.get("payload"), closing)
            ):
                raise RuntimeError("Closing inflight differs from durable receipt")
            pending_archive = (
                log / f"{index:04d}-timeout-confirmed-closing-inflight.json"
            )
            if pending_archive.exists() and not same_json(
                json.loads(pending_archive.read_text()), closing_pending
            ):
                raise RuntimeError("Confirmed closing archive changed")
            atomic(pending_archive, closing_pending)
            if not same_json(
                json.loads(runner.pending_path.read_text()), closing_pending
            ):
                raise RuntimeError("Closing pending changed during replay")
            runner.pending_path.unlink()
        return commit(result, closing=receipt)

    if closing_pending is not None and not close_path.exists():
        raise RuntimeError("Operational close is uncertain; no further automatic close")
    if result_path.exists():
        saved = json.loads(result_path.read_text())
        check_binding(saved)
        if (
            digest(saved["recovered_state"]) != saved["recovered_state_sha256"]
            or digest(saved["server_session"]) != saved["server_session_sha256"]
        ):
            raise RuntimeError("Timeout result integrity mismatch")
        if saved["skipped"]:
            if not intent_path.exists() or not close_path.exists():
                raise RuntimeError("Closing evidence is incomplete")
            intent = read_intent()
            return replay_close(intent, expected_hash=saved["closing_receipt_sha256"])
        remote = saved["server_session"]
        result = validate_continue_response(200, remote, current, payload)
        return commit(result, remote=remote)
    if close_path.exists():
        if not intent_path.exists():
            raise RuntimeError("Closing receipt has no bound intent")
        intent = read_intent()
        return replay_close(intent)

    expected = current["chat_messages"] + [
        {"participant_name": "user", "text": payload["user_utterance"]["text"]}
    ]
    observation = (
        json.loads(observation_path.read_text()) if observation_path.exists() else None
    )
    if observation:
        check_observation(observation)

    def classify(remote):
        normalized = normalize_item(remote)
        if normalized["conversation_id"] != current["conversation_id"]:
            if not payload["user_utterance"]["is_final"] or normalized["chat_messages"]:
                raise RuntimeError("Server advanced unexpectedly after timeout")
            result = validate_continue_response(
                200, {**remote, "utterance": None}, current, payload
            )
            return result, {**remote, "utterance": None}
        if not same_json(normalized["scenario"], current["scenario"]):
            raise RuntimeError("Timed-out scenario changed")
        _verify_raw_prefix(
            runner, index, remote["chat_messages"], current["conversation_id"]
        )
        if len(remote["chat_messages"]) <= len(current["chat_messages"]):
            raise RuntimeError("Timed-out turn is not persisted")
        _verify_message_fields(
            payload["user_utterance"],
            remote["chat_messages"][len(current["chat_messages"])],
        )
        if not same_json(normalized["chat_messages"], expected):
            result = validate_continue_response(200, remote, current, payload)
            return result, remote
        return None, remote

    for _ in range(TIMEOUT_POLICY["max_polls"]):
        result, remote = classify(get_session())
        if result is not None:
            return commit(result, remote=remote)
        observed_now = now()
        server_hash = digest(remote)
        if observation is None:
            observation = {
                **binding,
                "first_seen": observed_now.isoformat(),
                "server_session_sha256": server_hash,
                "conversation_id": current["conversation_id"],
                "server_session": remote,
            }
            observation["observation_sha256"] = digest(observation)
            atomic(observation_path, observation)
            print(
                json.dumps(
                    {
                        "event": "task2_timeout_observed",
                        "turn_index": index,
                        "grace_seconds": TIMEOUT_POLICY["grace_seconds"],
                    }
                ),
                flush=True,
            )
        if (
            server_hash != observation["server_session_sha256"]
            or digest(observation["server_session"]) != server_hash
        ):
            raise RuntimeError("Unanswered server history changed during grace")
        age = (
            observed_now - datetime.fromisoformat(observation["first_seen"])
        ).total_seconds()
        if age < 0:
            raise RuntimeError("Timeout clock moved backwards")
        if age < TIMEOUT_POLICY["grace_seconds"]:
            wait(TIMEOUT_POLICY["poll_seconds"])
            continue
        final_remote = get_session()
        result, final_remote = classify(final_remote)
        if result is not None:
            return commit(result, remote=final_remote)
        if digest(final_remote) != server_hash:
            raise RuntimeError(
                "Final timeout observation changed; reconcile before closing"
            )
        check_skip_bounds(runner, state, max_skips=max_skips)
        if intent_path.exists():
            intent = read_intent()
            closing = intent["closing_payload"]
        else:
            closing = build_continue_payload(
                runner.run_id, current["conversation_id"], "I'll stop here.", True
            )
            atomic(
                intent_path,
                {
                    **binding,
                    "reason": "verified_unanswered_timeout",
                    "natural_user_stop": False,
                    "observation_sha256": digest(observation),
                    "closing_payload": closing,
                    "closing_payload_sha256": digest(closing),
                },
            )
        archive_pending()
        status, body = runner._organizer_call(close_name, runner.continue_path, closing)
        result = validate_continue_response(status, body, current, closing)
        return commit(result, closing=json.loads(close_path.read_text()))
    raise RuntimeError("Timeout reconciliation exceeded bounded polling window")
