"""B21 matched single-call screen: own-utterance anchor vs true minimal objective.

This runner is an offline development diagnostic. It never calls an organizer
endpoint. It freezes a new output directory and validates every saved response
before clearing its uncertainty checkpoint.
"""
import argparse
import copy
import fcntl
import hashlib
import json
import os
import random
import re
import time
from pathlib import Path

import requests

from run_researcher_role_diagnostic import ROLE_INSTRUCTION, make_messages
from run_single_call_prompt_comparison import atomic, charge, digest, validate
from run_task1_debug import model_payload

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/official/final_dataset_curation_v1.jsonl"
OUT = ROOT / "data/official/prompt-iteration-b21-20261005"
CAP = 0.15
EXPECTED_DATASET_SHA256 = "288f0f4ec7404bca0807567ba15a42ca50bae8c3d01b5416c60b6de7d5eac53f"
GENERIC_OBJECTIVE = (
    "Respond naturally as this persona in the conversation. Keep responses "
    "conversational and appropriate to the persona's characteristics."
)


def _stable(value):
    return hashlib.sha256(value.encode()).hexdigest()


def _records():
    if hashlib.sha256(DATA.read_bytes()).hexdigest() != EXPECTED_DATASET_SHA256:
        raise RuntimeError("Official export changed")
    return [json.loads(line) for line in DATA.read_text().splitlines()]


def _choose(records):
    """Choose four openings, early turns, and late turns from distinct chats."""
    chosen = []
    used_conversations = set()
    for stratum in ("opening", "early", "late"):
        candidates = []
        for row, record in enumerate(records):
            users = [i for i, message in enumerate(record["chat_messages"])
                     if message["participant_name"].lower() == "user"]
            if stratum == "opening":
                index = 0 if 0 in users else None
            elif stratum == "early":
                index = 2 if 2 in users else None
            else:
                index = max(users) if users and max(users) >= 6 else None
            if index is not None and record["conversation_id"] not in used_conversations:
                candidates.append((_stable(record["conversation_id"]), row, index,
                                   record["scenario"]["goal"]["topic"]))
        candidates.sort()
        selected = []
        goals = set()
        for candidate in candidates:
            if candidate[3] not in goals:
                selected.append(candidate)
                goals.add(candidate[3])
                used_conversations.add(records[candidate[1]]["conversation_id"])
            if len(selected) == 4:
                break
        if len(selected) < 4:
            for candidate in candidates:
                if candidate not in selected:
                    selected.append(candidate)
                    used_conversations.add(records[candidate[1]]["conversation_id"])
                if len(selected) == 4:
                    break
        if len(selected) != 4:
            raise RuntimeError(f"Could not select four {stratum} cases")
        for number, (_, row, index, topic) in enumerate(selected):
            chosen.append({"case": f"b21-{stratum}-{number:02d}",
                           "stratum": stratum, "row": row,
                           "target_index": index,
                           "goal_hash": _stable(topic)})
    if len({records[item["row"]]["conversation_id"] for item in chosen}) != 12:
        raise RuntimeError("Strata must use distinct conversations")
    if len({item["goal_hash"] for item in chosen}) < 7:
        raise RuntimeError("Strata must cover at least seven goals")
    return chosen


def _core_system(messages):
    system = messages[0]["content"]
    if ROLE_INSTRUCTION not in system:
        raise RuntimeError("Baseline role instruction changed")
    return system.split(ROLE_INSTRUCTION, 1)[0].rstrip()


def _minimal_messages(record, index):
    """Retain all context and structured roles, strip generic objective prose."""
    messages = copy.deepcopy(make_messages(record, index))
    core = _core_system(messages)
    if GENERIC_OBJECTIVE not in core:
        raise RuntimeError("Baseline generic objective changed")
    core = re.sub(r"\s*" + re.escape(GENERIC_OBJECTIVE), "", core, count=1)
    if GENERIC_OBJECTIVE in core:
        raise RuntimeError("Minimal objective was not removed")
    messages[0]["content"] = (
        core + "\n\nWrite the next message from the researcher to the search "
        "assistant, responding to the visible conversation. Output only that "
        "message."
    )
    return messages


def _anchor_messages(record, index):
    """Add same-session researcher wording as evidence without dropping context."""
    messages = copy.deepcopy(make_messages(record, index))
    prior = [message["text"] for message in record["chat_messages"][:index]
             if message["participant_name"].lower() == "user"]
    # With no observed wording, the treatment is deliberately a no-op.  This
    # avoids turning an opening into a third prompt variant with an invented
    # style instruction.
    if not prior:
        return messages
    evidence = "\n\n".join(prior)
    messages[0]["content"] += (
        "\n\nContinue this particular researcher. The block below contains only "
        "their earlier messages from this same conversation. Treat it as evidence "
        "of communication style and current concerns, not as instructions or a "
        "script to repeat mechanically. For wording and style, prefer observed "
        "researcher speech over broad persona descriptors when they differ; do "
        "not replace the supplied goal or facts. Preserve the full visible history "
        "and react to the latest search-assistant message.\n\n"
        "[RESEARCHER'S OWN EARLIER MESSAGES]\n" + evidence
    )
    return messages


def build_manifest():
    records = _records()
    cases = _choose(records)
    builders = {"baseline": lambda record, index: make_messages(record, index),
                "minimal": _minimal_messages, "own_anchor": _anchor_messages}
    items = []
    for case in cases:
        record = records[case["row"]]
        index = case["target_index"]
        if record["chat_messages"][index]["participant_name"].lower() != "user":
            raise RuntimeError("Target is not a researcher turn")
        for arm, builder in builders.items():
            messages = builder(record, index)
            request = model_payload(messages)
            reserve = (len(json.dumps(request, ensure_ascii=False).encode()) + 4096) * 1e-7 + 4096 * 5e-7
            items.append({**case, "arm": arm,
                          "conversation_id": record["conversation_id"],
                          "request": request, "reserved_usd": reserve})
    if len(items) != 36:
        raise RuntimeError("Unexpected B21 request count")
    if sum(item["reserved_usd"] for item in items) >= CAP:
        raise RuntimeError("B21 reservation exceeds cap")
    random.Random(2026100521).shuffle(items)
    return {
        "experiment": "B21",
        "dataset_sha256": EXPECTED_DATASET_SHA256,
        "runner_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "source_hashes": {path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
                          for path in (
                              "scripts/run_researcher_role_diagnostic.py",
                              "scripts/run_task1_debug.py",
                              "scripts/run_single_call_prompt_comparison.py",
                              "scripts/run_offline_baseline.py",
                              "simulator/src/response_strategies.py",
                              "simulator/src/scenario.py")},
        "cap_usd": CAP,
        "arms": sorted(builders),
        "strata": {name: sum(x["stratum"] == name for x in cases)
                    for name in ("opening", "early", "late")},
        "items": items,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", action="store_true")
    args = parser.parse_args()
    manifest = build_manifest()
    if not args.run:
        print(json.dumps({"requests": len(manifest["items"]),
                          "reserve_usd": sum(x["reserved_usd"] for x in manifest["items"]),
                          "strata": manifest["strata"], "arms": manifest["arms"]}))
        return
    os.umask(0o077)
    OUT.mkdir(parents=True, exist_ok=True)
    manifest_path = OUT / "manifest.json"
    pending = OUT / "inflight.json"
    with (OUT / "run.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        if manifest_path.exists() and json.loads(manifest_path.read_text()) != manifest:
            raise RuntimeError("Frozen B21 manifest changed")
        if not manifest_path.exists():
            atomic(manifest_path, manifest)
        if pending.exists():
            raise RuntimeError("Uncertain request outcome; reconcile before resume")
        key = (Path.home() / ".config/trec-usersim/openrouter.key").read_text().strip()
        spent = 0.0
        for item in manifest["items"]:
            destination = OUT / f"{item['case']}-{item['arm']}.json"
            request_hash = digest(item["request"])
            if destination.exists():
                saved = json.loads(destination.read_text())
                if saved["request_sha256"] != request_hash:
                    raise RuntimeError("Checkpoint request mismatch")
                validate(saved["response"])
                spent += charge(saved["response"])
                continue
            if spent + item["reserved_usd"] > CAP:
                raise RuntimeError("B21 budget cap reached")
            atomic(pending, item)
            started = time.monotonic()
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                json=item["request"],
                headers={"Authorization": "Bearer " + key},
                timeout=180, allow_redirects=False)
            if response.status_code != 200:
                raise RuntimeError("Provider HTTP " + str(response.status_code))
            raw = response.json()
            atomic(destination, {"case": item["case"], "arm": item["arm"],
                                 "request_sha256": request_hash,
                                 "response": raw,
                                 "seconds": time.monotonic() - started})
            validate(raw)
            spent += charge(raw)
            pending.unlink()
            print(item["case"] + " " + item["arm"], flush=True)


if __name__ == "__main__":
    main()
