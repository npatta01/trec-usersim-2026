"""Checkpointed Task 2 debug runner.

This module keeps the organizer transport separate from the tested Task 2
generator.  It intentionally exposes only the two debug routes.  A live run
is resumable after completed requests, but an in-flight request is treated as
uncertain and requires manual reconciliation rather than being replayed.
"""

from __future__ import annotations

import argparse
import copy
import datetime as _dt
import fcntl
import hashlib
import json
import math
import os
from pathlib import Path
from typing import Any, Callable

import requests

from run_single_call_prompt_comparison import atomic, digest
from task2_core import Conversation
from task2_generator import generate_turn
from task2_model import CheckpointedModel


ROOT = Path(__file__).resolve().parents[1]
BASE = "http://f03-iim-lin1.cit-f03.fh-koeln.de/api"
TEAM_ID = "NP Labs"
TASK_NAME = "end_to_end_conversation_generation"
RUN_ID = "np-labs-luna-task2-debug-20261006-v1"
MODEL = "openai/gpt-6-luna"
CAP_USD = 3.0
MAX_TOTAL_TURNS = 500
MAX_CONVERSATION_TURNS = 30
DEBUG_ROUTES = {"/task2/debug/start", "/task2/debug/continue"}


def _write_json(path: Path, value: Any) -> None:
    """Write private JSON atomically, including an fsync before replacement."""

    atomic(path, value)


def _canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _same_json(left: Any, right: Any) -> bool:
    return _canonical(left) == _canonical(right)


def _utc_timestamp() -> str:
    return _dt.datetime.now(_dt.timezone.utc).isoformat()


def _message_role(value: Any) -> str:
    if not isinstance(value, str):
        raise ValueError("Message participant_name must be a string")
    role = value.strip().lower()
    if role == "user":
        return "user"
    if role in {"agent", "assistant"}:
        return "agent"
    raise ValueError("Unknown participant role")


def _validate_scenario(value: Any) -> dict:
    if not isinstance(value, dict) or not isinstance(value.get("goal"), dict):
        raise ValueError("Expected scenario with a goal object")
    return copy.deepcopy(value)


def _validate_message(value: Any) -> dict:
    if not isinstance(value, dict):
        raise ValueError("Chat message must be an object")
    role = _message_role(value.get("participant_name"))
    text = value.get("text")
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Chat message must contain nonempty text")
    # Retain only the semantic fields consumed by the generator.  Timestamps,
    # sources and annotations are organizer metadata and are not history text.
    return {"participant_name": role, "text": text}


def _agent_final(value: Any) -> bool:
    """Read the transport's optional assistant closure marker strictly."""

    return isinstance(value, dict) and _message_role(value.get("participant_name")) == "agent" and value.get("is_final") is True


def _normalize_history(messages: Any) -> list[dict]:
    if messages is None:
        return []
    if not isinstance(messages, list):
        raise ValueError("chat_messages must be a list")
    normalized = [_validate_message(message) for message in messages]
    expected = "user"
    for message in normalized:
        if message["participant_name"] != expected:
            raise ValueError("Chat history has invalid speaker alternation")
        expected = "agent" if expected == "user" else "user"
    return normalized


def _normalize_item(body: Any, *, allow_missing_history: bool = False) -> dict:
    if not isinstance(body, dict):
        raise ValueError("Organizer response must be a JSON object")
    conversation_id = body.get("conversation_id")
    if not isinstance(conversation_id, str) or not conversation_id:
        raise ValueError("Organizer response has no conversation_id")
    scenario = _validate_scenario(body.get("scenario"))
    messages = body.get("chat_messages")
    if messages is None and not allow_missing_history:
        raise ValueError("Organizer response has no chat_messages")
    if isinstance(messages, list):
        for message in messages:
            if isinstance(message, dict) and "conversation_id" in message:
                if message.get("conversation_id") != conversation_id:
                    raise ValueError("Chat message conversation_id differs from response")
    return {
        "conversation_id": conversation_id,
        "scenario": scenario,
        "chat_messages": _normalize_history(messages),
    }


def validate_start_response(status: int, body: Any) -> dict:
    """Validate and normalize a successful debug start response."""

    if status not in (200, 201):
        raise ValueError(f"Unexpected Task 2 debug start HTTP status {status}")
    item = _normalize_item(body, allow_missing_history=True)
    if "utterance" in body and body["utterance"] is not None:
        raise ValueError("Start response unexpectedly contains an utterance")
    if item["chat_messages"]:
        raise ValueError("Start response unexpectedly contains history")
    return item


def build_continue_payload(
    run_id: str,
    conversation_id: str,
    text: str,
    is_final: bool,
    *,
    timestamp: str | None = None,
) -> dict:
    if not isinstance(run_id, str) or not run_id:
        raise ValueError("run_id is required")
    if not isinstance(conversation_id, str) or not conversation_id:
        raise ValueError("conversation_id is required")
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Generated text must be nonempty")
    if type(is_final) is not bool:
        raise ValueError("is_final must be a boolean")
    if not isinstance(timestamp, str) or not timestamp:
        timestamp = _utc_timestamp()
    return {
        "run_id": run_id,
        "user_utterance": {
            "timestamp": timestamp,
            "conversation_id": conversation_id,
            "participant_name": "user",
            "text": text,
            "sources": [],
            "annotations": {},
            "is_final": is_final,
        },
    }


def _expected_history(current: dict, payload: dict) -> list[dict]:
    prior = current.get("chat_messages", [])
    utterance = payload.get("user_utterance", {})
    return prior + [{"participant_name": "user", "text": utterance.get("text", "") }]


def validate_continue_response(status: int, body: Any, current: dict, payload: dict) -> dict:
    """Validate a continue response without silently rewriting organizer history.

    The 200 contract returns the complete history for the active conversation.
    The 201 contract starts a new conversation and must contain no history.  A
    response that omits, duplicates, changes, or relabels prior turns is unsafe
    to feed into the next model call and is rejected.
    """

    current = _normalize_item(current)
    if status == 428:
        if not is_completion(status, body):
            raise ValueError("428 response is not an explicit completed-run response")
        return {"kind": "complete"}
    if status not in (200, 201):
        raise ValueError(f"Unexpected Task 2 debug continue HTTP status {status}")

    if not isinstance(body, dict):
        raise ValueError("Organizer response must be a JSON object")
    has_history = "chat_messages" in body
    has_utterance = "utterance" in body
    utterance = None
    if has_utterance and body["utterance"] is not None:
        if _agent_final(body["utterance"]):
            raise ValueError("Assistant is_final requires a 201 scenario transition")
        if not isinstance(body["utterance"], dict):
            raise ValueError("Incremental utterance must be an object")
        utterance_id = body["utterance"].get("conversation_id")
        response_id = body.get("conversation_id")
        if not isinstance(utterance_id, str) or not utterance_id:
            raise ValueError("Incremental utterance has no conversation_id")
        if not isinstance(response_id, str) or utterance_id != response_id:
            raise ValueError("Incremental utterance conversation_id differs from response")
        if status == 200 and utterance_id != current["conversation_id"]:
            raise ValueError("Incremental utterance changed the active conversation ID")
        utterance = _validate_message(body["utterance"])
        if utterance["participant_name"] != "agent":
            raise ValueError("Returned incremental utterance must be an agent turn")
    if status != 201 and not has_history and not has_utterance:
        raise ValueError("Continue response has neither full history nor utterance")
    if status == 201:
        item = _normalize_item(body, allow_missing_history=True)
        if item["conversation_id"] == current["conversation_id"]:
            raise ValueError("201 response did not provide a new conversation ID")
        if item["chat_messages"]:
            raise ValueError("201 new conversation unexpectedly contains history")
        if utterance is not None:
            raise ValueError("201 new conversation unexpectedly contains an utterance")
        return {"kind": "new_conversation", "item": item}
    if has_history:
        raw_history = body.get("chat_messages")
        if isinstance(raw_history, list) and any(_agent_final(message) for message in raw_history):
            raise ValueError("Assistant is_final requires a 201 scenario transition")
        item = _normalize_item(body)
    else:
        # The currently served OpenAPI returns one incremental agent utterance
        # instead of chat_messages.  Reconstruct the full local history from
        # the exact prior item and that one returned turn.
        item = {
            "conversation_id": body.get("conversation_id"),
            "scenario": body.get("scenario"),
            "chat_messages": _expected_history(current, payload) + [utterance],
        }
        item = _normalize_item(item)
    if status == 200:
        if payload.get("user_utterance", {}).get("is_final") is True:
            raise ValueError("Final user turn must produce a 201 scenario transition")
        if item["conversation_id"] != current["conversation_id"]:
            raise ValueError("200 response changed the active conversation ID")
        if not _same_json(item["scenario"], current["scenario"]):
            raise ValueError("200 response changed the active scenario")
        expected_prefix = _expected_history(current, payload)
        actual = item["chat_messages"]
        if len(actual) != len(expected_prefix) + 1:
            raise ValueError("200 response does not contain exactly one new agent turn")
        if not _same_json(actual[:-1], expected_prefix):
            raise ValueError("200 response rewrote, omitted, or duplicated history")
        if actual[-1]["participant_name"] != "agent":
            raise ValueError("200 response does not end with an agent turn")
        if utterance is not None and not _same_json(actual[-1], utterance):
            raise ValueError("Incremental utterance conflicts with full history")
        return {"kind": "continue", "item": item}

def is_completion(status: int, body: Any) -> bool:
    """Recognize only the organizer's explicit run-complete 428 response."""

    if status != 428 or not isinstance(body, dict):
        return False
    detail = body.get("detail", "")
    if not isinstance(detail, str):
        return False
    # Unknown prose is not a completion protocol. In particular, substring
    # matches also accept "not completed" and "completed partially".
    return detail.strip().lower().rstrip(".!") in {
        "run was finished", "run completed",
    }


def _source_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def freeze_manifest(out: Path, config: dict, *, source_files: list[Path] | None = None) -> dict:
    """Freeze run settings and source hashes; refuse a changed resumed run."""

    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    source_files = source_files if source_files is not None else default_source_files()
    hashes = {}
    frozen = {}
    frozen_dir = out / "frozen"
    for source in source_files:
        source = Path(source)
        if not source.is_file():
            raise ValueError(f"Missing source file for frozen manifest: {source}")
        source_hash = _source_hash(source)
        hashes[str(source)] = source_hash
        try:
            relative = source.relative_to(ROOT)
        except ValueError:
            relative = Path(source.name)
        frozen_path = frozen_dir / relative
        frozen_path.parent.mkdir(parents=True, exist_ok=True)
        if frozen_path.exists():
            if _source_hash(frozen_path) != source_hash:
                raise RuntimeError(f"Frozen source changed: {frozen_path}")
        else:
            temporary = frozen_path.with_name(frozen_path.name + ".tmp")
            temporary.write_bytes(source.read_bytes())
            with temporary.open("rb") as handle:
                os.fsync(handle.fileno())
            temporary.replace(frozen_path)
        frozen[str(relative)] = source_hash
    manifest = {"config": copy.deepcopy(config), "source_hashes": hashes, "frozen_sources": frozen}
    path = out / "manifest.json"
    if path.exists():
        old = json.loads(path.read_text())
        if old != manifest:
            raise RuntimeError("Frozen Task 2 debug manifest changed; refuse resume")
        return old
    _write_json(path, manifest)
    return manifest


def default_source_files() -> list[Path]:
    names = (
        "run_task2_debug.py",
        "task2_core.py",
        "task2_generator.py",
        "task2_model.py",
        "run_task1_debug.py",
        "run_style_postedit.py",
        "run_prompt_iteration_b21.py",
        "run_prompt_iteration_b22.py",
        "run_single_call_prompt_comparison.py",
        "run_researcher_role_diagnostic.py",
        "run_offline_baseline.py",
    )
    return [ROOT / "scripts" / name for name in names] + [
        ROOT / "simulator" / "src" / "scenario.py",
        ROOT / "simulator" / "src" / "response_strategies.py",
    ]


class Task2DebugRunner:
    """Run Task 2 against injected organizer/model transports.

    ``organizer_post`` receives ``(debug_path, payload)`` and returns
    ``(status_code, decoded_json)``.  ``model_post`` receives an OpenRouter
    request and returns the same pair.  This injection boundary keeps the
    protocol and resume tests entirely offline.
    """

    def __init__(
        self,
        out: Path,
        *,
        run_id: str = RUN_ID,
        organizer_post: Callable[[str, dict], tuple[int, Any]],
        model_post: Callable[[dict], tuple[int, Any]],
        cap_usd: float = CAP_USD,
        max_total_turns: int = MAX_TOTAL_TURNS,
        max_conversation_turns: int = MAX_CONVERSATION_TURNS,
        style_postedit: bool = True,
        team_id: str = TEAM_ID,
        description: str = "Debug only: GPT-6 Luna Task 2 full-history simulator with the tested style post-edit; no official submission.",
        source_files: list[Path] | None = None,
    ):
        if not isinstance(run_id, str) or not run_id or len(run_id) > 256:
            raise ValueError("Invalid run_id")
        if not math.isfinite(cap_usd) or cap_usd <= 0:
            raise ValueError("Invalid model budget cap")
        if type(max_total_turns) is not int or max_total_turns < 0:
            raise ValueError("Invalid total turn limit")
        if type(max_conversation_turns) is not int or max_conversation_turns <= 0:
            raise ValueError("Invalid per-conversation turn limit")
        self.out = Path(out)
        self.out.mkdir(parents=True, exist_ok=True)
        self.run_id = run_id
        self.cap_usd = cap_usd
        self.max_total_turns = max_total_turns
        self.max_conversation_turns = max_conversation_turns
        self.style_postedit = style_postedit
        self.team_id = team_id
        self.description = description
        self.organizer_post = organizer_post
        self.organizer_dir = self.out / "organizer"
        self.organizer_dir.mkdir(parents=True, exist_ok=True)
        self._source_files = source_files
        self.model = CheckpointedModel(
            self.out / "model", cap_usd, model_post,
            pricing={MODEL: (0.1, 0.5)},
        )

    @property
    def state_path(self) -> Path:
        return self.out / "state.json"

    @property
    def pending_path(self) -> Path:
        return self.organizer_dir / "inflight.json"

    def _load_state(self) -> dict:
        if not self.state_path.exists():
            return {
                "run_id": self.run_id,
                "status": "not_started",
                "total_user_turns": 0,
                "completed_conversations": 0,
                "user_stops": 0,
                "server_cutoffs": 0,
                "spent_usd": 0.0,
                "reserved_usd": 0.0,
                "current": None,
            }
        state = json.loads(self.state_path.read_text())
        if state.get("run_id") != self.run_id:
            raise RuntimeError("Saved state belongs to a different run_id")
        if state.get("status") not in {"not_started", "running", "complete", "halted"}:
            raise RuntimeError("Invalid saved Task 2 state")
        return state

    def _save_state(self, state: dict) -> None:
        _write_json(self.state_path, state)

    def _organizer_call(self, name: str, path: str, payload: dict) -> tuple[int, Any]:
        if path not in DEBUG_ROUTES:
            raise ValueError("Task 2 runner permits debug routes only")
        if not name or "/" in name:
            raise ValueError("Invalid organizer checkpoint name")
        receipt = self.organizer_dir / f"{name}.json"
        request_hash = digest(payload)
        if self.pending_path.exists():
            raise RuntimeError("Uncertain organizer request; reconcile before resuming")
        if receipt.exists():
            saved = json.loads(receipt.read_text())
            if saved.get("path") != path:
                raise RuntimeError("Organizer checkpoint request changed")
            if saved.get("request_sha256") != request_hash:
                # A crash can occur after the response receipt is durable but
                # before state.json is advanced.  Rebuilding a continue
                # payload creates a new timestamp; reuse is safe only when
                # every semantic field is identical.
                old_payload = saved.get("payload")
                new_compare = copy.deepcopy(payload)
                old_compare = copy.deepcopy(old_payload)
                try:
                    new_compare["user_utterance"].pop("timestamp", None)
                    old_compare["user_utterance"].pop("timestamp", None)
                except (AttributeError, KeyError, TypeError):
                    raise RuntimeError("Organizer checkpoint request changed") from None
                if not _same_json(old_compare, new_compare):
                    raise RuntimeError("Organizer checkpoint request changed")
            return int(saved["status"]), saved["body"]
        if self.model.has_pending():
            raise RuntimeError("Uncertain model request; reconcile before resuming")
        # This file contains the complete timestamped payload before the
        # external side effect.  A crash leaves it as an explicit stop signal.
        _write_json(self.pending_path, {"path": path, "payload": payload, "request_sha256": request_hash})
        status, body = self.organizer_post(path, payload)
        _write_json(receipt, {"path": path, "payload": payload, "request_sha256": request_hash, "status": status, "body": body})
        self.pending_path.unlink()
        return status, body

    def _current_item(self, state: dict) -> dict:
        current = state.get("current")
        if not isinstance(current, dict) or not isinstance(current.get("item"), dict):
            raise RuntimeError("Saved state has no active conversation")
        return _normalize_item(current["item"])

    @staticmethod
    def _conversation(item: dict) -> Conversation:
        item = _normalize_item(item)
        conversation = Conversation.start(item["conversation_id"], item["scenario"])
        history = []
        for message in item["chat_messages"]:
            history.append((message["participant_name"], message["text"]))
        # Conversation.start permits an opening with no turns.  The immutable
        # object is deliberately assembled here after validating alternation.
        return Conversation(
            conversation.conversation_id,
            conversation.scenario_json,
            tuple(history),
            False,
        )

    def _store_model_totals(self, state: dict) -> None:
        state.update(self.model.totals())

    def _config(self) -> dict:
        return {
            "run_id": self.run_id,
            "team_id": self.team_id,
            "task_name": TASK_NAME,
            "description": self.description,
            "model": MODEL,
            "cap_usd": self.cap_usd,
            "max_total_turns": self.max_total_turns,
            "max_conversation_turns": self.max_conversation_turns,
            "style_postedit": self.style_postedit,
            "routes": sorted(DEBUG_ROUTES),
        }

    def freeze(self) -> dict:
        """Freeze code/configuration before a live preflight or POST."""

        return freeze_manifest(self.out, self._config(), source_files=self._source_files)

    def run(self, *, freeze: bool = True) -> dict:
        """Run or resume the debug session and return the final state."""

        if freeze:
            self.freeze()
        state = self._load_state()
        if self.pending_path.exists():
            raise RuntimeError("Uncertain organizer request; reconcile before resuming")
        if self.model.has_pending():
            raise RuntimeError("Uncertain model request; reconcile before resuming")
        if state["status"] in {"complete", "halted"}:
            return state

        if state["status"] == "not_started":
            start_payload = {
                "run_id": self.run_id,
                "task_name": TASK_NAME,
                "description": self.description,
                "team_id": self.team_id,
            }
            status, body = self._organizer_call("start", "/task2/debug/start", start_payload)
            item = validate_start_response(status, body)
            state["current"] = {"item": item, "turns": 0}
            state["status"] = "running"
            self._save_state(state)

        while True:
            if state["total_user_turns"] >= self.max_total_turns:
                state["status"] = "halted"
                state["halt_reason"] = "operational_total_turn_cap"
                self._store_model_totals(state)
                self._save_state(state)
                return state
            current = self._current_item(state)
            current_turns = int(state["current"].get("turns", 0))
            if current_turns >= self.max_conversation_turns:
                state["status"] = "halted"
                state["halt_reason"] = "operational_conversation_turn_cap"
                self._store_model_totals(state)
                self._save_state(state)
                return state

            conversation = self._conversation(current)
            checkpoint_prefix = f"turn-{state['total_user_turns']:04d}"

            def call(name: str, request: dict) -> str:
                return self.model.call(f"{checkpoint_prefix}-{name}", request)

            turn = generate_turn(conversation, call, style_postedit=self.style_postedit)
            payload = build_continue_payload(
                self.run_id,
                current["conversation_id"],
                turn.text,
                turn.is_final,
                timestamp=_utc_timestamp(),
            )
            name = f"continue-{state['total_user_turns']:04d}"
            status, body = self._organizer_call(name, "/task2/debug/continue", payload)
            result = validate_continue_response(status, body, current, payload)
            state["total_user_turns"] += 1
            if result["kind"] == "complete":
                state["status"] = "complete"
                state["completed_conversations"] += 1
                if turn.is_final:
                    state["user_stops"] += 1
                else:
                    state["server_cutoffs"] += 1
                state["current"] = None
                self._store_model_totals(state)
                self._save_state(state)
                return state
            if result["kind"] == "new_conversation":
                if turn.is_final:
                    state["user_stops"] += 1
                else:
                    state["server_cutoffs"] += 1
                state["completed_conversations"] += 1
                state["current"] = {"item": result["item"], "turns": 0}
            else:
                state["current"] = {"item": result["item"], "turns": current_turns + 1}
            state["status"] = "running"
            self._store_model_totals(state)
            self._save_state(state)


def _read_secret(path: Path) -> str:
    value = path.read_text().strip()
    if not value:
        raise RuntimeError(f"Credential file is empty: {path}")
    return value


def _live_transports(organizer_key: str, model_key: str):
    session = requests.Session()
    session.headers.update({"Authorization": f"Bearer {organizer_key}", "Content-Type": "application/json"})

    def organizer_post(path: str, payload: dict):
        response = session.post(BASE + path, json=payload, timeout=180, allow_redirects=False)
        try:
            body = response.json()
        except ValueError:
            body = {"detail": "Non-JSON organizer response"}
        return response.status_code, body

    def model_post(payload: dict):
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            json=payload,
            headers={"Authorization": f"Bearer {model_key}", "Content-Type": "application/json"},
            timeout=180,
            allow_redirects=False,
        )
        try:
            body = response.json()
        except ValueError:
            body = {"detail": "Non-JSON model response"}
        return response.status_code, body

    return organizer_post, model_post, session


class _RunLock:
    def __init__(self, path: Path):
        self.path = path
        self.handle = None

    def __enter__(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.handle = self.path.open("a+")
        try:
            fcntl.flock(self.handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            self.handle.close()
            self.handle = None
            raise RuntimeError("Another Task 2 debug runner is active")
        return self

    def __exit__(self, *_exc):
        if self.handle is not None:
            fcntl.flock(self.handle.fileno(), fcntl.LOCK_UN)
            self.handle.close()
            self.handle = None


def _preflight(session, *, require_available=True):
    def get(path):
        response = session.get(BASE + path, timeout=60, allow_redirects=False)
        if response.status_code != 200:
            raise RuntimeError(f"Organizer GET {path} failed with HTTP {response.status_code}")
        try:
            return response.json()
        except ValueError as exc:
            raise RuntimeError(f"Organizer GET {path} returned non-JSON") from exc

    verified = get("/auth/verify")
    if verified.get("team_id") != TEAM_ID:
        raise RuntimeError("Organizer credential is not for the NP Labs team")
    budget = get("/budget/check")
    document = budget.get("response", budget) if isinstance(budget, dict) else {}
    remaining = document.get("debug", {}).get(TASK_NAME, {}).get("remaining")
    if not isinstance(remaining, int) or (require_available and remaining <= 0):
        raise RuntimeError("No Task 2 debug runs remain according to organizer budget")
    return budget


def main(argv=None):
    parser = argparse.ArgumentParser(description="Run exactly one resumable Task 2 debug session")
    parser.add_argument("--run", action="store_true", help="perform the authenticated debug run")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "data/official/task2-debug-luna")
    parser.add_argument("--run-id", default=RUN_ID)
    args = parser.parse_args(argv)
    if not args.run:
        parser.error("Refusing to run without --run; this script only performs an explicit Task 2 debug run")
    out = args.output_dir
    os.umask(0o077)
    out.mkdir(parents=True, exist_ok=True)
    organizer_key = _read_secret(Path.home() / ".config/trec-usersim/organizer.key")
    model_key = _read_secret(Path.home() / ".config/trec-usersim/openrouter.key")
    organizer_post, model_post, session = _live_transports(organizer_key, model_key)
    with _RunLock(out / "run.lock"):
        runner = Task2DebugRunner(out, run_id=args.run_id, organizer_post=organizer_post, model_post=model_post)
        try:
            runner.freeze()
            existing_state = json.loads((out / "state.json").read_text()) if (out / "state.json").exists() else {}
            start_receipt = out / "organizer" / "start.json"
            starting_new = (
                existing_state.get("status", "not_started") == "not_started"
                and not start_receipt.is_file()
            )
            budget = _preflight(session, require_available=starting_new)
            if (out / "budget_before.json").exists():
                _write_json(out / "budget_resume.json", budget)
            else:
                _write_json(out / "budget_before.json", budget)
            state = runner.run()
            _write_json(out / "budget_after.json", _preflight(session, require_available=False))
            print(json.dumps({k: state.get(k) for k in ("status", "total_user_turns", "completed_conversations", "user_stops", "server_cutoffs", "spent_usd", "reserved_usd")}, indent=2), flush=True)
        except Exception as exc:
            _write_json(out / "error.json", {"type": type(exc).__name__, "message": str(exc) if isinstance(exc, (RuntimeError, ValueError)) else "Runner failed; inspect private checkpoints"})
            raise


if __name__ == "__main__":
    main()
