"""B22 bounded single-call act-awareness comparison.

This runner compares the unchanged B21 baseline with one short, silent
context-aware next-act instruction. It preserves supplied persona/goal fields
and visible utterance text and
never sends an organizer request. B21's known spend plus its unresolved-call
reserve is held inside the combined Luna cap.
"""
import argparse
import copy
import fcntl
import hashlib
import json
import os
import random
import time
from pathlib import Path

import requests

from experiments.run_prompt_iteration_b21 import EXPECTED_DATASET_SHA256, _records
from experiments.run_researcher_role_diagnostic import make_messages
from experiments.run_single_call_prompt_comparison import atomic, charge, digest, validate
from experiments.run_task1_debug import model_payload

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/official/final_dataset_curation_v1.jsonl"
OUT = ROOT / "data/official/prompt-iteration-b22-20261005"
TOTAL_CAP = 0.15
B21_MAX_USD = 0.01528152
CAP = TOTAL_CAP - B21_MAX_USD

ACT_INSTRUCTION = (
    "\n\nBefore writing, silently consider what this researcher would most naturally "
    "do next in response to the latest search-assistant message, using the full "
    "visible conversation, goal, and persona. A context-supported next move may "
    "be to open, verify or challenge, narrow or clarify, acknowledge or accept, "
    "continue or expand, change scope, disengage or stop, or do something else. "
    "Choose what fits this exchange; do not seek variety, force progress or an "
    "ending, contradict supplied facts, or claim unobserved external actions. "
    "If the history is empty, introduce the research need naturally. Output only "
    "the next researcher message, with no act label, analysis, or metadata."
)


def _stable(value):
    return hashlib.sha256(value.encode()).hexdigest()


def _manifest_ids(path):
    if not path.exists():
        return set()
    data = json.loads(path.read_text())
    return {item["conversation_id"] for item in data.get("items", [])
            if item.get("conversation_id")}


def _excluded_conversations():
    return (_manifest_ids(ROOT / "data/official/prompt-iteration-20261005/manifest.json")
            | _manifest_ids(ROOT / "data/official/prompt-iteration-b21-20261005/manifest.json"))


def _category(record, index):
    """Classify only the visible latest search-assistant reply for sampling."""
    text = record["chat_messages"][index - 1]["text"].lower() if index else ""
    if any(term in text for term in (
            "sorry", "apolog", "cannot", "can't", "do not have", "don't have",
            "not available", "unable", "limitation", "no dataset", "none of")):
        return "limitation"
    if any(term in text for term in (
            "verified", "download", "here is", "here are", "available", "link",
            "citation")):
        return "answered"
    if any(term in text for term in ("wrong", "incorrect", "not sure", "actually", "mismatch")):
        return "correction"
    if "?" in text:
        return "question"
    return "other"


def _real_cases(records):
    """Select eight new prefixes from visible context, not future targets."""
    excluded = _excluded_conversations()
    used = set()

    def candidates(stratum):
        result = []
        for row, record in enumerate(records):
            conversation_id = record["conversation_id"]
            if conversation_id in excluded or conversation_id in used:
                continue
            users = [i for i, message in enumerate(record["chat_messages"])
                     if message["participant_name"].lower() == "user"]
            if stratum == "opening":
                index = 0 if 0 in users else None
            elif stratum == "early":
                index = 2 if 2 in users else None
            else:
                index = max(users) if users and max(users) >= 6 else None
            if index is not None:
                result.append((_stable(conversation_id), row, index,
                               _category(record, index)))
        return sorted(result)

    chosen = []
    for candidate in candidates("opening")[:2]:
        chosen.append(("opening", candidate))
        used.add(records[candidate[1]]["conversation_id"])

    for wanted in ("limitation", "answered"):
        match = next((item for item in candidates("early") if item[3] == wanted), None)
        if match is None:
            raise RuntimeError("Could not find requested early visible-context category")
        chosen.append(("early", match))
        used.add(records[match[1]]["conversation_id"])

    late_wanted = ["answered", "limitation", "question", "answered"]
    for wanted in late_wanted:
        match = next((item for item in candidates("late") if item[3] == wanted), None)
        if match is None:
            raise RuntimeError("Could not find requested late visible-context category")
        chosen.append(("late", match))
        used.add(records[match[1]]["conversation_id"])

    if len(chosen) != 8 or len(used) != 8:
        raise RuntimeError("B22 real-prefix selection is not distinct")
    return [{
        "case": f"b22-{stratum}-{number:02d}",
        "kind": "real",
        "stratum": stratum,
        "row": candidate[1],
        "target_index": candidate[2],
        "visible_category": candidate[3],
        "conversation_id": records[candidate[1]]["conversation_id"],
        "goal_hash": _stable(records[candidate[1]]["scenario"]["goal"]["topic"]),
    } for number, (stratum, candidate) in enumerate(chosen)]


def _synthetic_record(name, answer):
    if answer:
        assistant = (
            "I found the fictional RiverWatch Monthly Temperature Archive. It has "
            "monthly CSV records from 2010 through 2020 for six European river "
            "stations, with station IDs and water-temperature measurements. The "
            "download page includes a data dictionary and license."
        )
        topic = "A monthly CSV dataset of European river water temperatures from 2010-2020 is needed, with station IDs and a usable data dictionary."
    else:
        assistant = (
            "The only candidate I found is a proprietary North American collection "
            "with annual values from 2019. It has no station IDs, no monthly data, "
            "and no public download."
        )
        topic = "A public monthly CSV dataset of European river water temperatures from 2010-2020 is needed, with station IDs and a usable data dictionary."
    return {
        "record_id": f"synthetic-b22-{name}",
        "conversation_id": f"synthetic-b22-{name}",
        "synthetic": True,
        "scenario": {
            "persona": {
                "general_info": {"gender": "Non-binary", "age": "35-54",
                                  "highest_education": "Master's Degree",
                                  "proficiency_in_english": "Proficient"},
                "experience_with_ai": {"trust": "Neutral",
                                        "perceived_human_likeness": "Medium anthropomorphism"},
                "individual_traits": {"frustration_threshold": "Moderately quickly",
                                       "interaction_style": "Concise"},
            },
            "goal": {"context": "A fictional environmental monitoring project needs a reusable public dataset.",
                     "topic": topic, "discipline": "Environmental science"},
            "persona_goal_interaction": {"domain_familiarity": "Slightly familiar",
                                          "known_datasets": []},
        },
        "chat_messages": [
            {"participant_name": "User", "text": "I need a dataset matching those requirements for my project."},
            {"participant_name": "Agent", "text": assistant},
            # Placeholder target is outside the visible prefix and never enters a request.
            {"participant_name": "User", "text": ""},
        ],
    }


def _cases(records):
    cases = _real_cases(records)
    for name, answer in (("answered", True), ("unresolved", False)):
        record = _synthetic_record(name, answer)
        cases.append({"case": f"b22-synthetic-{name}", "kind": "synthetic",
                      "stratum": "synthetic", "row": None, "target_index": 2,
                      "visible_category": "answered" if answer else "limitation",
                      "conversation_id": record["conversation_id"],
                      "goal_hash": _stable(record["scenario"]["goal"]["topic"]),
                      "record": record})
    return cases


def _record_for_case(records, case):
    return case["record"] if case["kind"] == "synthetic" else records[case["row"]]


def _act_messages(record, index):
    messages = copy.deepcopy(make_messages(record, index))
    messages[0]["content"] += ACT_INSTRUCTION
    return messages


def build_manifest():
    if hashlib.sha256(DATA.read_bytes()).hexdigest() != EXPECTED_DATASET_SHA256:
        raise RuntimeError("Official export changed")
    records = _records()
    cases = _cases(records)
    builders = {"baseline": lambda record, index: make_messages(record, index),
                "act_aware": _act_messages}
    items = []
    for case in cases:
        record = _record_for_case(records, case)
        index = case["target_index"]
        if record["chat_messages"][index]["participant_name"].lower() != "user":
            raise RuntimeError("B22 target is not a researcher turn")
        for arm, builder in builders.items():
            messages = builder(record, index)
            request = model_payload(messages)
            if request["messages"] != messages:
                raise RuntimeError("B22 payload changed the captured messages")
            if request["provider"]["data_collection"] != "deny":
                raise RuntimeError("B22 provider data collection is not denied")
            reserve = ((len(json.dumps(request, ensure_ascii=False).encode()) + 4096) * 1e-7
                       + 4096 * 5e-7)
            items.append({**{k: v for k, v in case.items() if k != "record"},
                          "arm": arm, "request": request, "reserved_usd": reserve})
    if len(items) != 20:
        raise RuntimeError("Unexpected B22 request count")
    if len({x["conversation_id"] for x in items}) != 10:
        raise RuntimeError("B22 cases must use ten distinct conversations")
    if sum(item["reserved_usd"] for item in items) >= CAP:
        raise RuntimeError("B22 reservation exceeds remaining combined cap")
    random.Random(2026100622).shuffle(items)
    source_paths = [
        "experiments/run_researcher_role_diagnostic.py",
        "experiments/run_prompt_iteration_b21.py",
        "experiments/run_task1_debug.py",
        "experiments/run_single_call_prompt_comparison.py",
        "experiments/run_offline_baseline.py",
        "simulator/src/response_strategies.py",
        "simulator/src/scenario.py",
    ]
    for relative in (
        "data/official/prompt-iteration-20261005/manifest.json",
        "data/official/prompt-iteration-b21-20261005/manifest.json",
    ):
        if (ROOT / relative).exists():
            source_paths.append(relative)
    return {
        "experiment": "B22",
        "dataset_sha256": EXPECTED_DATASET_SHA256,
        "runner_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "source_hashes": {path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
                          for path in source_paths},
        "total_cap_usd": TOTAL_CAP,
        "held_b21_max_usd": B21_MAX_USD,
        "cap_usd": CAP,
        "arms": sorted(builders),
        "real_cases": 8,
        "synthetic_cases": 2,
        "requests": len(items),
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
                          "real_cases": manifest["real_cases"],
                          "synthetic_cases": manifest["synthetic_cases"],
                          "held_b21_max_usd": B21_MAX_USD,
                          "combined_worst_case": B21_MAX_USD + sum(x["reserved_usd"] for x in manifest["items"]),
                          "arms": manifest["arms"]}))
        return
    os.umask(0o077)
    OUT.mkdir(parents=True, exist_ok=True)
    manifest_path = OUT / "manifest.json"
    pending = OUT / "inflight.json"
    with (OUT / "run.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        if manifest_path.exists() and json.loads(manifest_path.read_text()) != manifest:
            raise RuntimeError("Frozen B22 manifest changed")
        if not manifest_path.exists():
            atomic(manifest_path, manifest)
        if pending.exists():
            raise RuntimeError("Uncertain B22 request outcome; reconcile before resume")
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
            if B21_MAX_USD + spent + item["reserved_usd"] > TOTAL_CAP:
                raise RuntimeError("Combined B21+B22 budget cap reached")
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
                                 "request_sha256": request_hash, "response": raw,
                                 "seconds": time.monotonic() - started})
            validate(raw)
            spent += charge(raw)
            pending.unlink()
            print(item["case"] + " " + item["arm"], flush=True)


if __name__ == "__main__":
    main()
