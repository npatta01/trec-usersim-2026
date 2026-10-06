"""Checkpointed Task 1 runner for debug and official organizer modes."""

from __future__ import annotations

import argparse
import copy
import fcntl
import hashlib
import json
import math
import os
import re
from pathlib import Path
from typing import Any, Callable

import requests

from usersim.checkpoints import atomic, digest
from usersim.prompts import build_messages, editor_messages
from usersim.requests import model_payload, validate
from usersim.task2.model import CheckpointedModel
from usersim.task2.protocol import is_completion, utc_timestamp


ROOT = Path(__file__).resolve().parents[1]
BASE = "http://f03-iim-lin1.cit-f03.fh-koeln.de/api"
TEAM_ID = "NP Labs"
TASK_NAME = "next_utterance_prediction"
MODEL = "openai/gpt-6-luna"
CAP_USD = 1.0
MAX_CASES = 1000
MODE_ROUTES = {
    "debug": {
        "start": "/task1/debug/start",
        "continue": "/task1/debug/continue",
    },
    "official": {
        "start": "/task1/run/start",
        "continue": "/task1/run/continue",
    },
}
DESCRIPTION = (
    "GPT-6 Luna simulates the researcher from supplied persona, goal and full "
    "utterance history; researcher mapped to assistant role. "
)


def _source_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def default_source_files() -> list[Path]:
    """Return every repository source loaded by the Task 1 runtime."""

    return [
        ROOT / name
        for name in (
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
        )
    ]


def freeze_manifest(
    out: Path, config: dict, *, source_files: list[Path] | None = None
) -> dict:
    """Copy and hash the exact configuration and source used by a run."""

    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    sources = source_files if source_files is not None else default_source_files()
    source_hashes = {}
    frozen_sources = {}
    frozen_dir = out / "frozen"
    for source in sources:
        source = Path(source)
        if not source.is_file():
            raise ValueError(f"Missing Task 1 source file: {source}")
        current_hash = _source_hash(source)
        source_hashes[str(source)] = current_hash
        try:
            relative = source.relative_to(ROOT)
        except ValueError:
            relative = Path(source.name)
        frozen_path = frozen_dir / relative
        frozen_path.parent.mkdir(parents=True, exist_ok=True)
        if frozen_path.exists():
            if _source_hash(frozen_path) != current_hash:
                raise RuntimeError(f"Frozen Task 1 source changed: {frozen_path}")
        else:
            temporary = frozen_path.with_name(frozen_path.name + ".tmp")
            temporary.write_bytes(source.read_bytes())
            with temporary.open("rb") as handle:
                os.fsync(handle.fileno())
            temporary.replace(frozen_path)
        frozen_sources[str(relative)] = current_hash

    manifest = {
        "config": copy.deepcopy(config),
        "source_hashes": source_hashes,
        "frozen_sources": frozen_sources,
    }
    path = out / "manifest.json"
    if path.exists():
        saved = json.loads(path.read_text())
        if saved != manifest:
            raise RuntimeError("Frozen Task 1 configuration/source changed")
        return saved
    atomic(path, manifest)
    return manifest


def _semantic_history(item: dict) -> list[tuple[str, str]]:
    """Return the organizer target history without incidental message metadata."""

    messages = item.get("chat_messages")
    if not isinstance(messages, list):
        raise RuntimeError("Task 1 scenario must include a chat_messages list")
    history = []
    for message in messages:
        if not isinstance(message, dict):
            raise RuntimeError("Invalid Task 1 chat_messages entry")
        role = message.get("participant_name")
        text = message.get("text")
        if not isinstance(role, str) or not isinstance(text, str):
            raise RuntimeError("Invalid Task 1 chat_messages entry")
        role = role.lower()
        if role == "user":
            normalized_role = "user"
        elif role in ("agent", "assistant"):
            normalized_role = "agent"
        else:
            raise RuntimeError("Invalid Task 1 chat_messages participant")
        history.append((normalized_role, text))
    return history


def _checked_item(status: int, body: Any, *, previous: dict | None = None) -> dict:
    if status not in (200, 201):
        raise RuntimeError("Organizer did not supply the next Task 1 scenario")
    if (
        not isinstance(body, dict)
        or not isinstance(body.get("conversation_id"), str)
        or not body["conversation_id"]
        or not isinstance(body.get("scenario"), dict)
    ):
        raise RuntimeError("Invalid organizer Task 1 scenario")
    history = _semantic_history(body)
    messages = build_messages(body)
    if previous is not None:
        previous_history = _semantic_history(previous)
        previous_messages = build_messages(previous)
        current_target = (body["conversation_id"], messages, history)
        previous_target = (
            previous["conversation_id"],
            previous_messages,
            previous_history,
        )
        if current_target == previous_target:
            raise RuntimeError("Organizer response did not advance the Task 1 target")
    return copy.deepcopy(body)


def _is_task1_completion(status: int, body: Any, run_id: str) -> bool:
    """Recognize shared completions or the exact Task 1 run-specific response."""

    return is_completion(status, body) or (
        status == 428
        and body
        == {
            "detail": f'No more open goals for run "{run_id}". Run was finished!'
        }
    )


class _Task1Model(CheckpointedModel):
    """Use the shared checkpoint engine with strict Task 1 cost validation."""

    def _valid(self, saved):
        if saved.get("status") != 200:
            raise RuntimeError("Model HTTP failure")
        text = validate(saved.get("response"))
        cost = saved.get("response", {}).get("usage", {}).get("cost")
        reserve = saved.get("reserve_usd")
        if (
            type(cost) not in (int, float)
            or not math.isfinite(cost)
            or type(reserve) not in (int, float)
            or not math.isfinite(reserve)
            or not 0 <= cost <= reserve
        ):
            raise RuntimeError("Missing or out-of-reservation model cost")
        return text


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
            raise RuntimeError("Another Task 1 runner is active")
        return self

    def __exit__(self, *_exc):
        if self.handle is not None:
            fcntl.flock(self.handle.fileno(), fcntl.LOCK_UN)
            self.handle.close()
            self.handle = None


class Task1Runner:
    """Run or resume one Task 1 organizer session through injected transports."""

    def __init__(
        self,
        out: Path,
        *,
        run_id: str,
        organizer_post: Callable[[str, dict], tuple[int, Any]],
        model_post: Callable[[dict], tuple[int, Any]],
        mode: str = "debug",
        style_postedit: bool = True,
        cap_usd: float = CAP_USD,
        max_cases: int = MAX_CASES,
        team_id: str = TEAM_ID,
        source_files: list[Path] | None = None,
    ):
        if not isinstance(run_id, str) or not run_id or len(run_id) > 256:
            raise ValueError("Invalid run_id")
        if mode not in MODE_ROUTES:
            raise ValueError("Task 1 mode must be debug or official")
        if type(style_postedit) is not bool:
            raise ValueError("style_postedit must be a boolean")
        if (
            type(cap_usd) not in (int, float)
            or not math.isfinite(cap_usd)
            or not 0 < cap_usd <= CAP_USD
        ):
            raise ValueError("Invalid Task 1 model budget cap")
        if type(max_cases) is not int or max_cases <= 0:
            raise ValueError("Invalid Task 1 case limit")

        os.umask(0o077)
        self.out = Path(out)
        self.out.mkdir(parents=True, exist_ok=True)
        self.run_id = run_id
        self.mode = mode
        self.routes = copy.deepcopy(MODE_ROUTES[mode])
        self.style_postedit = style_postedit
        self.cap_usd = float(cap_usd)
        self.max_cases = max_cases
        self.team_id = team_id
        self.description = DESCRIPTION + (
            "One conditional style-edit pass uses recent researcher speech and "
            "persona; no retrieval."
            if style_postedit
            else "Direct generation; no post-editing or retrieval."
        )
        self.organizer_post = organizer_post
        self.organizer_dir = self.out / "organizer"
        self.organizer_dir.mkdir(parents=True, exist_ok=True)
        self.source_files = source_files
        self.model = _Task1Model(
            self.out / "model",
            self.cap_usd,
            model_post,
            pricing={MODEL: (0.1, 0.5)},
        )

    @property
    def pending_path(self) -> Path:
        return self.organizer_dir / "inflight.json"

    @property
    def result_path(self) -> Path:
        return self.out / "result.json"

    def _config(self) -> dict:
        return {
            "run_id": self.run_id,
            "mode": self.mode,
            "team_id": self.team_id,
            "task_name": TASK_NAME,
            "description": self.description,
            "model": MODEL,
            "style_postedit": self.style_postedit,
            "cap_usd": self.cap_usd,
            "max_cases": self.max_cases,
            "routes": copy.deepcopy(self.routes),
        }

    def freeze(self) -> dict:
        return freeze_manifest(self.out, self._config(), source_files=self.source_files)

    def _organizer_call(self, name: str, path: str, payload: dict) -> tuple[int, Any]:
        if path not in set(self.routes.values()):
            raise ValueError(f"Task 1 {self.mode} runner rejected organizer route")
        if not re.fullmatch(r"[a-zA-Z0-9_-]+", name):
            raise ValueError("Invalid organizer checkpoint name")
        if self.pending_path.exists():
            raise RuntimeError("Uncertain organizer request; reconcile before resuming")
        receipt = self.organizer_dir / f"{name}.json"
        request_hash = digest(payload)
        if receipt.exists():
            saved = json.loads(receipt.read_text())
            if saved.get("path") != path or saved.get("request_sha256") != request_hash:
                raise RuntimeError("Organizer checkpoint request changed")
            return int(saved["status"]), saved["body"]
        if self.model.has_pending():
            raise RuntimeError("Uncertain model request; reconcile before resuming")
        atomic(
            self.pending_path,
            {"path": path, "payload": payload, "request_sha256": request_hash},
        )
        status, body = self.organizer_post(path, payload)
        atomic(
            receipt,
            {
                "path": path,
                "payload": payload,
                "request_sha256": request_hash,
                "status": status,
                "body": body,
            },
        )
        self.pending_path.unlink()
        return status, body

    def _case(self, index: int, item: dict, draft: str, selected: str) -> dict:
        path = self.out / f"case-{index:04d}.json"
        if path.exists():
            saved = json.loads(path.read_text())
            if (
                saved.get("item") != item
                or saved.get("draft") != draft
                or saved.get("selected") != selected
            ):
                raise RuntimeError("Task 1 case checkpoint changed")
            return saved
        request = {
            "run_id": self.run_id,
            "user_utterance": {
                "timestamp": utc_timestamp(),
                "conversation_id": item["conversation_id"],
                "participant_name": "user",
                "text": selected,
                "sources": [],
                "annotations": {},
                "is_final": False,
            },
        }
        saved = {
            "item": copy.deepcopy(item),
            "draft": draft,
            "selected": selected,
            "submission_request": request,
        }
        atomic(path, saved)
        return saved

    def _run_locked(self) -> dict:
        self.freeze()
        if self.pending_path.exists():
            raise RuntimeError("Uncertain organizer request; reconcile before resuming")
        if self.model.has_pending():
            raise RuntimeError("Uncertain model request; reconcile before resuming")
        if self.result_path.exists():
            return json.loads(self.result_path.read_text())

        start_payload = {
            "run_id": self.run_id,
            "team_id": self.team_id,
            "task_name": TASK_NAME,
            "description": self.description,
        }
        status, body = self._organizer_call(
            "start", self.routes["start"], start_payload
        )
        item = _checked_item(status, body)

        for index in range(self.max_cases):
            messages = build_messages(item)
            draft = self.model.call(f"case-{index:04d}-draft", model_payload(messages))
            selected = draft
            if self.style_postedit:
                selected = self.model.call(
                    f"case-{index:04d}-edit",
                    model_payload(editor_messages(messages, draft)),
                )
            case = self._case(index, item, draft, selected)
            status, body = self._organizer_call(
                f"continue-{index:04d}",
                self.routes["continue"],
                case["submission_request"],
            )
            if _is_task1_completion(status, body, self.run_id):
                result = {
                    "status": "complete",
                    "mode": self.mode,
                    "submitted": index + 1,
                    **self.model.totals(),
                }
                atomic(self.result_path, result)
                return result
            item = _checked_item(status, body, previous=item)
        raise RuntimeError("Task 1 case safety limit reached without completion")

    def run(self) -> dict:
        with _RunLock(self.out / "run.lock"):
            return self._run_locked()


def _read_secret(path: Path) -> str:
    value = path.read_text().strip()
    if not value:
        raise RuntimeError(f"Credential file is empty: {path}")
    return value


def _live_transports(organizer_key: str, model_key: str):
    session = requests.Session()
    session.headers.update(
        {
            "Authorization": f"Bearer {organizer_key}",
            "Content-Type": "application/json",
        }
    )

    def organizer_post(path: str, payload: dict):
        response = session.post(
            BASE + path, json=payload, timeout=180, allow_redirects=False
        )
        try:
            body = response.json()
        except ValueError:
            body = {"detail": "Non-JSON organizer response"}
        return response.status_code, body

    def model_post(payload: dict):
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            json=payload,
            headers={
                "Authorization": f"Bearer {model_key}",
                "Content-Type": "application/json",
            },
            timeout=180,
            allow_redirects=False,
        )
        try:
            body = response.json()
        except ValueError:
            body = {"detail": "Non-JSON model response"}
        return response.status_code, body

    return organizer_post, model_post


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--mode", choices=tuple(MODE_ROUTES), default="debug")
    parser.add_argument(
        "--style-postedit", action=argparse.BooleanOptionalAction, default=True
    )
    parser.add_argument("--max-cases", type=int, default=MAX_CASES)
    parser.add_argument(
        "--run", action="store_true", help="perform the authenticated Task 1 run"
    )
    args = parser.parse_args(argv)
    preview = {
        "dry_run": not args.run,
        "run_id": args.run_id,
        "mode": args.mode,
        "routes": copy.deepcopy(MODE_ROUTES[args.mode]),
        "model": MODEL,
        "style_postedit": args.style_postedit,
        "model_calls_per_case": 2 if args.style_postedit else 1,
        "cap_usd": CAP_USD,
        "max_cases": args.max_cases,
    }
    if not args.run:
        print(json.dumps(preview))
        return None

    key_dir = Path.home() / ".config/trec-usersim"
    organizer_key = _read_secret(key_dir / "organizer.key")
    model_key = _read_secret(key_dir / "openrouter.key")
    organizer_post, model_post = _live_transports(organizer_key, model_key)
    task = Task1Runner(
        args.output_dir.resolve(),
        run_id=args.run_id,
        organizer_post=organizer_post,
        model_post=model_post,
        mode=args.mode,
        style_postedit=args.style_postedit,
        cap_usd=CAP_USD,
        max_cases=args.max_cases,
    )
    try:
        result = task.run()
    except Exception as exc:
        raise RuntimeError(
            f"Task 1 {args.mode} run stopped; inspect private checkpoints "
            f"({type(exc).__name__})"
        ) from None
    print(json.dumps(result))
    return None


__all__ = [
    "CAP_USD",
    "MODE_ROUTES",
    "MODEL",
    "Task1Runner",
    "default_source_files",
    "freeze_manifest",
    "main",
]
