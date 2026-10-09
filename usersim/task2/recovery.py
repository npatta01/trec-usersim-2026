"""Explicit, checkpointed backend-error closure; never resend a persisted turn."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from requests.exceptions import ReadTimeout
from pathlib import Path

from usersim.checkpoints import atomic, digest
from .debug import (
    BASE,
    CAP_USD,
    MAX_TOTAL_TURNS,
    TEAM_ID,
    Task2DebugRunner,
    _RunLock,
    _live_transports,
    default_source_files,
    ROOT,
    _preflight,
    _read_secret,
)
from .reconciliation import (
    _advance,
    _verify_message_fields,
    _verify_raw_prefix,
    check_skip_bounds,
    persist_reply_event,
    OPERATIONAL_POLICY,
)
from .timeout import TIMEOUT_POLICY, recover_timeout
from .protocol import (
    build_continue_payload,
    is_completion,
    normalize_item,
    same_json,
    validate_continue_response,
)

BACKEND_ERRORS = {500, 502}
DEBUG_RECOVERY_DESCRIPTION = "Debug Task 2 Luna full-history simulation with style editor; verified backend failures may be closed operationally and recorded separately as skipped conversations."
POLICY = {
    "policy": "verified_persisted_turn_operational_close_v2",
    **OPERATIONAL_POLICY,
    "timeout": TIMEOUT_POLICY,
}


class Task2OfficialRunner(Task2DebugRunner):
    """Same runtime with an explicit official-only organizer boundary."""

    start_path = "/task2/run/start"
    continue_path = "/task2/run/continue"
    allowed_routes = {start_path, continue_path}

    def __init__(self, out, **kwargs):
        kwargs.setdefault(
            "description",
            "GPT-6 Luna full-history researcher simulator with one style edit; structured text and stop decision. Verified backend failures are closed operationally and logged separately as skipped conversations.",
        )
        super().__init__(out, **kwargs)


def verify_official_gate(debug_dir, review_file):
    """Require completed debug evidence and a review tied to exact final state."""
    if debug_dir is None or review_file is None:
        raise RuntimeError(
            "Official start requires completed debug evidence and review"
        )
    debug_dir, review_file = Path(debug_dir), Path(review_file)
    try:
        state = json.loads((debug_dir / "state.json").read_text())
        manifest = json.loads((debug_dir / "manifest.json").read_text())
        review = json.loads(review_file.read_text())
    except (OSError, ValueError) as exc:
        raise RuntimeError("Official debug gate evidence is unavailable") from exc
    if (
        state.get("status") != "complete"
        or state.get("completed_conversations", 0) <= 0
    ):
        raise RuntimeError("Debug run is not complete")
    if manifest.get("config", {}).get("run_id") != state.get("run_id"):
        raise RuntimeError("Debug manifest and state refer to different runs")
    if manifest.get("config", {}).get("routes") != [
        "/task2/debug/continue",
        "/task2/debug/start",
    ]:
        raise RuntimeError("Evidence is not from a debug runner")
    if (
        (debug_dir / "organizer/inflight.json").exists()
        or (debug_dir / "model/inflight.json").exists()
        or (debug_dir / "error.json").exists()
    ):
        raise RuntimeError("Unresolved debug request/error blocks official run")
    receipts = sorted((debug_dir / "organizer").glob("continue-*.json"))
    if not receipts:
        raise RuntimeError("No debug completion receipt")
    final = json.loads(receipts[-1].read_text())
    if final.get("path") != "/task2/debug/continue" or not is_completion(
        final.get("status"), final.get("body")
    ):
        raise RuntimeError("Debug completion not confirmed by organizer")
    if final.get("payload", {}).get("run_id") != state.get("run_id"):
        raise RuntimeError("Debug completion receipt belongs to another run")
    if digest(final["payload"]) != final.get("request_sha256"):
        raise RuntimeError("Debug completion receipt hash mismatch")
    if (
        review.get("run_id") != state.get("run_id")
        or review.get("state_sha256") != digest(state)
        or review.get("approved_for_official") is not True
        or not review.get("reviewed_conversation_ids")
    ):
        raise RuntimeError("Debug review does not approve this exact completed run")
    if (
        manifest.get("config", {}).get("model") != "openai/gpt-6-luna"
        or manifest.get("config", {}).get("style_postedit") is not True
    ):
        raise RuntimeError(
            "Debug simulator configuration differs from official baseline"
        )
    try:
        policy = json.loads((debug_dir / "recovery-policy.json").read_text())
    except (OSError, ValueError) as exc:
        raise RuntimeError("Debug recovery policy missing") from exc
    if policy != {**POLICY, "mode": "debug"}:
        raise RuntimeError("Debug did not verify the selected recovery policy")
    if review.get("manifest_sha256") != digest(manifest) or review.get(
        "completion_receipt_sha256"
    ) != digest(final):
        raise RuntimeError(
            "Debug review is not bound to the frozen code and completion receipt"
        )
    source_hashes = manifest.get("source_hashes", {})
    frozen_sources = manifest.get("frozen_sources", {})
    for source in default_source_files():
        relative = str(source.relative_to(ROOT))
        expected = source_hashes.get(str(source))
        try:
            current_hash = hashlib.sha256(source.read_bytes()).hexdigest()
            frozen_hash = hashlib.sha256(
                (debug_dir / "frozen" / relative).read_bytes()
            ).hexdigest()
        except OSError as exc:
            raise RuntimeError("Debug frozen source unavailable") from exc
        if (
            expected != current_hash
            or expected != frozen_hash
            or frozen_sources.get(relative) != expected
        ):
            raise RuntimeError("Official source differs from reviewed debug source")
    return {
        "debug_run_id": state["run_id"],
        "state_sha256": digest(state),
        "review": review,
    }


def recover_backend_error(runner, get_session, *, max_skips=24):
    """Reconcile one saved 5xx; close only an exactly verified unanswered turn.

    get_session is read-only and injectable. A durable closing receipt permits
    crash recovery without another GET or POST; all uncertain markers block.
    """
    if runner.pending_path.exists() or runner.model.has_pending():
        raise RuntimeError("Uncertain request blocks backend recovery")
    state = runner._load_state()
    if state["status"] not in {"running", "halted"}:
        raise RuntimeError("No active failed turn to recover")
    index = state["total_user_turns"]
    failed_path = runner.organizer_dir / f"continue-{index:04d}.json"
    if not failed_path.exists():
        raise RuntimeError("No backend failure receipt at current turn")
    failed = json.loads(failed_path.read_text())
    if failed["status"] not in BACKEND_ERRORS or failed["path"] != runner.continue_path:
        raise RuntimeError("Only saved backend failures can be recovered")
    payload = failed["payload"]
    if (
        digest(payload) != failed["request_sha256"]
        or payload.get("run_id") != runner.run_id
    ):
        raise RuntimeError("Failed request integrity mismatch")
    current = runner._current_item(state)
    if payload["user_utterance"]["conversation_id"] != current["conversation_id"]:
        raise RuntimeError("Failed request conversation mismatch")
    logdir = runner.out / "recovery"
    logdir.mkdir(exist_ok=True)
    intent_path = logdir / f"{index:04d}-intent.json"
    close_name = f"continue-{index + 1:04d}"
    closing_receipt = runner.organizer_dir / f"{close_name}.json"
    closing = None
    if intent_path.exists():
        intent = json.loads(intent_path.read_text())
        if intent["failed_request_sha256"] != failed["request_sha256"]:
            raise RuntimeError("Recovery intent changed")
        closing = intent["closing_payload"]
    if closing_receipt.exists():
        if closing is None:
            raise RuntimeError("Closing receipt without recovery intent")
        status, body = runner._organizer_call(close_name, runner.continue_path, closing)
        result = validate_continue_response(status, body, current, closing)
        skipped = True
    else:
        remote = get_session()
        atomic(logdir / f"{index:04d}-server-session.json", remote)
        try:
            normalized = normalize_item(remote)
        except ValueError as exc:
            raise RuntimeError("Malformed server session blocks recovery") from exc
        if normalized["conversation_id"] != current["conversation_id"]:
            if not payload["user_utterance"]["is_final"] or normalized["chat_messages"]:
                raise RuntimeError("Server advanced unexpectedly")
            body = {**normalized, "utterance": None}
            result = validate_continue_response(200, body, current, payload)
            skipped = False
        else:
            if not same_json(normalized["scenario"], current["scenario"]):
                raise RuntimeError("Server scenario changed")
            _verify_raw_prefix(
                runner, index, remote["chat_messages"], current["conversation_id"]
            )
            expected = current["chat_messages"] + [
                {"participant_name": "user", "text": payload["user_utterance"]["text"]}
            ]
            if same_json(normalized["chat_messages"], expected):
                check_skip_bounds(runner, state, max_skips=max_skips)
                if closing is None:
                    closing = build_continue_payload(
                        runner.run_id,
                        current["conversation_id"],
                        "I'll stop here.",
                        True,
                    )
                    atomic(
                        intent_path,
                        {
                            "reason": "backend_failure",
                            "natural_user_stop": False,
                            "failed_request_sha256": failed["request_sha256"],
                            "closing_payload": closing,
                        },
                    )
                status, body = runner._organizer_call(
                    close_name, runner.continue_path, closing
                )
                result = validate_continue_response(status, body, current, closing)
                skipped = True
            else:
                # Accept a delayed reply only if the ordinary protocol validator
                # proves it preserves the exact prefix and adds one agent turn.
                try:
                    result = validate_continue_response(200, remote, current, payload)
                except ValueError as exc:
                    raise RuntimeError(
                        "Server history cannot safely be reconciled"
                    ) from exc
                skipped = False
    if skipped and result["kind"] not in {"new_conversation", "complete"}:
        raise RuntimeError("Operational close did not confirm advancement")
    if not skipped and result["kind"] == "continue":
        persist_reply_event(
            runner, index, payload, remote, origin=f"HTTP{failed['status']}"
        )
    recovered = _advance(
        state, result, is_final=payload["user_utterance"]["is_final"], skipped=skipped
    )
    runner._store_model_totals(recovered)
    atomic(
        logdir / f"{index:04d}-result.json",
        {
            "kind": result["kind"],
            "skipped": skipped,
            "previous_state": state,
            "recovered_state": recovered,
        },
    )
    runner._save_state(recovered)
    error = runner.out / "error.json"
    if error.exists():
        error.replace(logdir / f"{index:04d}-previous-error.json")
    return recovered


def run_with_recovery(runner, get_session, *, now=None, wait=None):
    def recover_current():
        state = runner._load_state()
        index = state["total_user_turns"]
        timeout_proof = (
            runner.organizer_dir / f"transport-error-continue-{index:04d}.json"
        )
        if runner.pending_path.exists() or timeout_proof.exists():
            return recover_timeout(
                runner, get_session, max_skips=POLICY["max_skips"], now=now, wait=wait
            )
        return recover_backend_error(runner, get_session, max_skips=POLICY["max_skips"])

    state = runner._load_state()
    if state["status"] == "halted":
        recover_current()
    while True:
        try:
            return runner.run()
        except (ValueError, ReadTimeout):
            runner.record_failure()
            recover_current()


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Explicit Task 2 run with verified backend-error closure"
    )
    parser.add_argument("--run", action="store_true")
    parser.add_argument("--mode", choices=["debug", "official"], required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument(
        "--cap-usd",
        type=float,
        default=CAP_USD,
        help="Authorized total model-reservation ceiling (default: %(default)s)",
    )
    parser.add_argument(
        "--max-total-turns",
        type=int,
        default=MAX_TOTAL_TURNS,
        help="Authorized total user-turn guard (default: %(default)s)",
    )
    parser.add_argument("--debug-evidence-dir", type=Path)
    parser.add_argument("--debug-review-file", type=Path)
    args = parser.parse_args(argv)
    if not args.run:
        parser.error("Explicit --run is required")
    if not math.isfinite(args.cap_usd) or args.cap_usd <= 0:
        parser.error("--cap-usd must be finite and positive")
    if args.max_total_turns <= 0:
        parser.error("--max-total-turns must be a positive integer")
    gate = None
    if args.mode == "official":
        gate = verify_official_gate(args.debug_evidence_dir, args.debug_review_file)
    os.umask(0o077)
    out = args.output_dir
    out.mkdir(parents=True, exist_ok=True)
    org_key = _read_secret(Path.home() / ".config/trec-usersim/organizer.key")
    model_key = _read_secret(Path.home() / ".config/trec-usersim/openrouter.key")
    post, model_post, session = _live_transports(org_key, model_key)
    mode = "run" if args.mode == "official" else "debug"
    cls = Task2OfficialRunner if mode == "run" else Task2DebugRunner
    with _RunLock(out / "run.lock"):
        options = {}
        if mode == "debug":
            manifest_path = out / "manifest.json"
            options["description"] = (
                json.loads(manifest_path.read_text())["config"]["description"]
                if manifest_path.exists()
                else DEBUG_RECOVERY_DESCRIPTION
            )
        runner = cls(
            out,
            run_id=args.run_id,
            organizer_post=post,
            model_post=model_post,
            cap_usd=args.cap_usd,
            max_total_turns=args.max_total_turns,
            **options,
        )
        policy = {**POLICY, "mode": mode}
        if gate is not None:
            policy["debug_gate"] = gate
        policy_path = out / "recovery-policy.json"
        if policy_path.exists() and json.loads(policy_path.read_text()) != policy:
            raise RuntimeError("Recovery policy changed")
        atomic(policy_path, policy)

        def get_session():
            response = session.get(
                BASE + f"/{'run' if mode == 'run' else 'debug'}/session",
                params={"run_id": args.run_id},
                timeout=60,
                allow_redirects=False,
            )
            if response.status_code != 200:
                raise RuntimeError(f"Session reconciliation HTTP{response.status_code}")
            return response.json()

        try:
            runner.freeze()
            budget = _preflight(
                session,
                mode=mode,
                require_available=not (out / "organizer/start.json").exists(),
            )
            atomic(out / "recovery-budget-before.json", budget)
            result = run_with_recovery(runner, get_session)
            atomic(
                out / "recovery-budget-after.json",
                _preflight(session, mode=mode, require_available=False),
            )
            print(
                json.dumps(
                    {k: v for k, v in result.items() if k != "current"}, indent=2
                ),
                flush=True,
            )
        except Exception as exc:
            runner.record_failure()
            atomic(
                out / "error.json",
                {
                    "type": type(exc).__name__,
                    "message": str(exc)
                    if isinstance(exc, (RuntimeError, ValueError))
                    else "Runner failed; inspect private receipts",
                },
            )
            raise


if __name__ == "__main__":
    main()
