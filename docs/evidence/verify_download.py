"""Offline restore check for the immutable private evidence release.

Downloads are supplied separately with gh release download. No provider keys,
model calls or organizer calls are used. The source verifier is loaded only from
the included, hash-checked source tar.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tarfile


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def extract(archive, destination):
    destination.mkdir(mode=0o700, parents=True)
    with tarfile.open(archive) as handle:
        handle.extractall(destination, filter="data")
    for child in destination.rglob("*"):
        child.chmod(0o700 if child.is_dir() else 0o600)


def main():
    os.umask(0o077)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("download", type=Path)
    parser.add_argument("restore", type=Path, help="new private directory")
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    root = args.download.resolve()
    restore = args.restore.resolve()
    if restore.exists():
        raise ValueError("Use a new restore directory; existing data is not overwritten")
    checks = []
    for line in (root / "SHA256SUMS").read_text().splitlines():
        expected, name = line.split("  ", 1)
        if Path(name).name != name:
            raise ValueError("Invalid asset path")
        actual = digest(root / name)
        if actual != expected:
            raise ValueError("Downloaded asset checksum mismatch: " + name)
        checks.append({"name": name, "bytes": (root / name).stat().st_size,
                       "sha256": actual})
    index = json.loads((root / "artifact-index.json").read_text())
    asset = index["artifact"]
    bundle = root / asset["name"]
    if digest(bundle) != asset["sha256"] or bundle.stat().st_size != asset["bytes"]:
        raise ValueError("Bundle does not match release index")
    extract(bundle, restore)
    source_tar = restore / index["source_tar"]["path_in_bundle"]
    if digest(source_tar) != index["source_tar"]["sha256"]:
        raise ValueError("Included source archive checksum mismatch")
    code = restore / "source" / "code"
    extract(source_tar, code)
    snapshots = []
    for snapshot in index["snapshots"]:
        target = restore / snapshot["directory_in_bundle"]
        output = subprocess.run(
            [sys.executable, str(code / "scripts/archive_paper_evidence.py"),
             "verify", str(target)], check=True, capture_output=True, text=True)
        result = json.loads(output.stdout)
        if (result["manifest_sha256"] != snapshot["manifest_sha256"]
                or result["files"] != snapshot["evidence_files"]
                or result["bytes"] != snapshot["evidence_bytes"]):
            raise ValueError("Snapshot differs from release index")
        if result["original_sources_checked"]:
            raise ValueError("Restore must verify without original source paths")
        snapshots.append({"directory": snapshot["directory_in_bundle"], **result})
    tests = []
    for pattern in ("test_evidence_archive.py", "test_submission_evidence.py"):
        result = subprocess.run(
            [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", pattern],
            cwd=code, check=True, capture_output=True, text=True)
        tests.append({"pattern": pattern, "exit_code": result.returncode,
                      "output": result.stdout + result.stderr})
    report = {
        "verified_utc": datetime.now(timezone.utc).isoformat(),
        "status": "verified",
        "downloaded_assets": checks,
        "bundle_sha256": asset["sha256"],
        "source_commit": index["source_commit"],
        "source_tar_sha256": index["source_tar"]["sha256"],
        "snapshots": snapshots,
        "evidence_files_verified": sum(item["files"] for item in snapshots),
        "original_paths_required": False,
        "credentials_required": False,
        "model_or_organizer_calls": 0,
        "offline_tests": tests,
    }
    args.report.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"status": "verified", "evidence_files": report["evidence_files_verified"],
                      "report": str(args.report)}))


if __name__ == "__main__":
    main()
