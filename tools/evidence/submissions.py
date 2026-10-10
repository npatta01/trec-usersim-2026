"""Build a public aggregate inventory from a verified private evidence snapshot.

No transcript, prompt, response text, key or HTTP body is written to the index.
The fixed run list is the canonical organizer-run inventory, not model experiments.
"""
from __future__ import annotations

import argparse
import csv
from decimal import Decimal
import json
from pathlib import Path

from .archive import digest, encoded, verify

RUNS = (
    (1, "debug", "official-data-and-development", "task1-debug-luna",
     "np-labs-luna-task1-debug-20261005-v1", "complete"),
    (1, "debug", "organizer-and-model-runs", "task1-debug-style-20261006-v1",
     "np-labs-luna-style-task1-debug-20261006-v1", "complete"),
    (1, "official", "organizer-and-model-runs", "task1-official-fidelity-20261006-v1",
     "np-labs-luna-fidelity-task1-official-20261006-v1", "complete"),
    (2, "debug", "official-data-and-development", "task2-debug-luna",
     "np-labs-luna-task2-debug-20261006-v1", "halted"),
    (2, "debug", "organizer-and-model-runs", "task2-debug-luna-20261006-v2",
     "np-labs-luna-task2-debug-20261006-v2", "halted"),
    (2, "debug", "organizer-and-model-runs", "task2-debug-luna-20261007-v3",
     "np-labs-luna-task2-debug-20261007-v3", "halted"),
    (2, "debug", "organizer-and-model-runs", "task2-debug-luna-v4",
     "np-labs-luna-task2-debug-v4", "halted"),
    (2, "debug", "organizer-and-model-runs", "task2-debug-luna-v5",
     "np-labs-luna-task2-debug-v5", "intentionally_paused"),
    (2, "official", "organizer-and-model-runs", "task2-official-luna-20261009-v1",
     "np-labs-luna-style-task2-official-20261009-v1", "complete"),
)


def read(path: Path) -> dict:
    return json.loads(path.read_text()) if path.exists() else {}


def money(value) -> str:
    rounded = Decimal(str(value or 0)).quantize(Decimal("0.000000001"))
    return format(abs(rounded) if rounded == 0 else rounded, "f")


def build_index(archive: Path) -> dict:
    proof = verify(archive)
    inventory = read(archive / "manifest.json")
    runs = []
    for task, mode, component, folder, run_id, status in RUNS:
        root = archive / component / folder
        if not root.is_dir():
            raise ValueError(f"Missing run: {run_id}")
        state_file = "state.json" if (root / "state.json").exists() else "result.json"
        state = read(root / state_file)
        manifest = read(root / "manifest.json")
        config = manifest.get("config", {})
        if state.get("run_id", config.get("run_id")) != run_id:
            raise ValueError(f"Wrong run identity: {folder}")
        if status != "intentionally_paused" and state.get("status") != status:
            raise ValueError(f"Unexpected run status: {folder}")
        if status == "intentionally_paused" and state.get("status") != "halted":
            raise ValueError(f"Paused run checkpoint is not halted: {folder}")
        receipts = sorted((root / "model").glob("*.json")) if (root / "model").exists() else sorted(root.glob("case-*.json"))
        costs, models, caps, responses = [], set(), set(), 0
        for file in receipts:
            record = read(file)
            response = record.get("response")
            if not isinstance(response, dict):
                continue
            responses += 1
            usage = response.get("usage", {})
            if usage.get("cost") is None:
                raise ValueError(f"Unaccounted response cost: {folder}/{file.name}")
            costs.append(Decimal(str(usage["cost"])))
            request = record.get("request", {})
            if request.get("model"):
                models.add(request["model"])
            if request.get("max_completion_tokens") is not None:
                caps.add(request["max_completion_tokens"])
        prefix = f"{component}/{folder}/"
        files = [f for f in inventory["files"] if f["path"].startswith(prefix)]
        organizer = sorted((root / "organizer").glob("*.json"))
        terminal = [f.name for f in organizer if read(f).get("status") == 428]
        if read(root / "last_http_response.json").get("status") == 428:
            terminal.append("last_http_response.json")
        cost = sum(costs, Decimal(0))
        record = {
            "run_id": run_id, "task": task, "mode": mode, "status": status,
            "checkpoint_status": state.get("status"), "archive_relative_directory": prefix[:-1],
            "artifact_files": len(files), "artifact_bytes": sum(f["bytes"] for f in files),
            "inventory_sha256": digest(encoded([
                {k: f[k] for k in ("path", "bytes", "sha256")} for f in files])),
            "state_file": state_file, "state_sha256": digest((root / state_file).read_bytes()),
            "model_call_receipts": responses, "model_receipt_cost_usd": money(cost),
            "checkpoint_model_calls": state.get("model_calls", state.get("submitted")),
            "checkpoint_model_cost_usd": money(state.get("spent_usd")),
            "receipt_minus_checkpoint_cost_usd": money(cost - Decimal(str(state.get("spent_usd", 0)))),
            "requested_models": sorted(models), "max_completion_tokens_values": sorted(caps),
            "frozen_source_files": len(manifest.get("frozen_sources", {})),
            "organizer_receipt_files": len(organizer), "terminal_http428_files": terminal,
            "official_evaluation_score": None, "whole_run_realism_rate": None,
        }
        for key in ("submitted", "total_user_turns", "completed_conversations", "user_stops",
                    "server_cutoffs", "skipped_conversations", "operational_closing_turns", "accepted_error_turns"):
            if key in state:
                record[key] = state[key]
        record["organizer_receipt_note"] = (
            "Only final accepted request/HTTP428 retained; per-prediction POST receipts and start receipt absent. All 64 input/model request/response records retained."
            if folder == "task1-debug-luna" else
            "Saved received HTTP/transport-error receipts and recovery evidence retained; counts are not necessarily accepted turns."
        )
        if folder == "task2-debug-luna-20261007-v3":
            record["accounting_note"] = "Eight priced response receipts include the fourth attempted turn. Checkpoint tracks only six calls / three turns; original state preserved."
        runs.append(record)
    return {"schema_version": 1, "evidence_manifest_sha256": proof["manifest_sha256"],
            "snapshot_utc": proof["snapshot_utc"], "organizer_runs": len(runs),
            "official_runs": sum(r["mode"] == "official" for r in runs),
            "debug_runs": sum(r["mode"] == "debug" for r in runs),
            "official_model_receipt_cost_usd": money(sum(
                Decimal(r["model_receipt_cost_usd"]) for r in runs if r["mode"] == "official")),
            "runs": runs,
            "limitations": ["Local snapshot; no organizer calls during indexing.",
                            "Different debug/official pools are not one independent evaluation set.",
                            "No transcript-bearing records distributed in public git.",
                            "Not an off-host backup; never resume from the archive."]}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--official-csv", type=Path,
                        help="Optional coverage/cost table for the two official runs")
    args = parser.parse_args()
    result = build_index(args.archive)
    for output in (args.output, args.official_csv):
        if output and (output.resolve() == args.archive.resolve()
                       or args.archive.resolve() in output.resolve().parents):
            parser.error("Output must be outside the immutable archive")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(encoded(result))
    if args.official_csv:
        args.official_csv.parent.mkdir(parents=True, exist_ok=True)
        columns = ["task", "run_id", "status", "predictions", "processed_conversations",
                   "normal_endings", "administrative_closures", "submitted_turns",
                   "model_call_receipts", "model_receipt_cost_usd", "official_evaluation_score"]
        with args.official_csv.open("w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=columns, lineterminator="\n")
            writer.writeheader()
            for run in result["runs"]:
                if run["mode"] != "official":
                    continue
                row = {key: run.get(key) for key in columns}
                row["predictions"] = run.get("submitted")
                if run["task"] == 2:
                    row["normal_endings"] = run["completed_conversations"]
                    row["administrative_closures"] = run["skipped_conversations"]
                    row["processed_conversations"] = row["normal_endings"] + row["administrative_closures"]
                    row["submitted_turns"] = run["total_user_turns"]
                writer.writerow(row)
    print(f"Indexed {result['organizer_runs']} runs ({result['official_runs']} official); no API calls.")


if __name__ == "__main__":
    main()
