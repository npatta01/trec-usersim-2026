"""Copy task-scoped evidence without credentials and verify every saved byte.

The manifest is private: it contains original paths and individual filenames.
The optional public index contains only component counts, sizes and digests.
An archive is an inspection snapshot, never a replacement runtime/checkpoint.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
from datetime import datetime, timezone

EXCLUDED_DIRS = {".git", ".venv", "venv", "node_modules", "__pycache__",
                 ".agents", ".codex", ".pytest_cache", ".mypy_cache"}
SECRET_PATTERNS = tuple(re.compile(p) for p in (
    rb"sk-or-v1-[A-Za-z0-9]{32,}",
    rb"(?<![A-Za-z0-9])sk-[A-Za-z0-9_-]{32,}",
    rb"gh[pousr]_[A-Za-z0-9]{30,}",
    rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
    rb"Bearer [A-Za-z0-9._-]{24,}",
))


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def encoded(value: object) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode()


def scan_for_secrets(data: bytes) -> int:
    """Check readable content, ignoring opaque provider-encrypted reasoning.

    Random encrypted blobs can coincidentally contain key-looking substrings.
    They are preserved byte-for-byte, but are neither decoded nor secret-scanned.
    No request fields, ordinary response text or plain reasoning are exempted.
    """
    opaque_fields = 0

    def readable(value):
        nonlocal opaque_fields
        if isinstance(value, dict):
            result = {}
            for key, child in value.items():
                if key == "data" and value.get("type") == "reasoning.encrypted":
                    opaque_fields += 1
                else:
                    result[key] = readable(child)
            return result
        if isinstance(value, list):
            return [readable(child) for child in value]
        return value

    try:
        scan = encoded(readable(json.loads(data)))
    except (ValueError, UnicodeDecodeError):
        scan = data
    if any(pattern.search(scan) for pattern in SECRET_PATTERNS):
        raise ValueError("Credential-shaped content found; no values printed")
    return opaque_fields


def excluded(path: Path) -> bool:
    return (any(part in EXCLUDED_DIRS for part in path.parts)
            or path.name == ".env" or path.name.startswith(".env.")
            or path.suffix in {".key", ".pem", ".pyc"})


def verify(destination: Path, check_sources: bool = False) -> dict:
    manifest = json.loads((destination / "manifest.json").read_text())
    expected = {entry["path"] for entry in manifest["files"]}
    actual = {p.relative_to(destination).as_posix()
              for p in destination.rglob("*") if p.is_file()}
    if actual != expected | {"manifest.json", "SHA256SUMS"}:
        raise ValueError("Archive inventory differs from manifest")
    for entry in manifest["files"]:
        path = destination / entry["path"]
        if path.is_symlink() or destination.resolve() not in path.resolve().parents:
            raise ValueError("Unsafe archive path")
        data = path.read_bytes()
        if len(data) != entry["bytes"] or digest(data) != entry["sha256"]:
            raise ValueError(f"Archive mismatch: {entry['path']}")
        scan_for_secrets(data)
        if check_sources:
            source = Path(manifest["sources"][entry["component"]])
            source = source / entry["source_relative"] if source.is_dir() else source
            if source.is_symlink() or digest(source.read_bytes()) != entry["sha256"]:
                raise ValueError(f"Original source changed: {entry['path']}")
    sums = "".join(f"{e['sha256']}  {e['path']}\n" for e in manifest["files"])
    if (destination / "SHA256SUMS").read_text() != sums:
        raise ValueError("SHA256SUMS differs from manifest")
    components = []
    for label in sorted(manifest["sources"]):
        files = [e for e in manifest["files"] if e["component"] == label]
        components.append({
            "component": label, "files": len(files),
            "bytes": sum(e["bytes"] for e in files),
            "inventory_sha256": digest(encoded([
                {k: e[k] for k in ("path", "bytes", "sha256")} for e in files])),
        })
    return {"schema_version": 1, "status": "verified",
            "snapshot_utc": manifest["snapshot_utc"],
            "manifest_sha256": digest((destination / "manifest.json").read_bytes()),
            "checksum_file_sha256": digest((destination / "SHA256SUMS").read_bytes()),
            "files": len(expected), "bytes": sum(e["bytes"] for e in manifest["files"]),
            "components": components,
            "excluded_files": len(manifest["excluded"]),
            "opaque_encrypted_fields": manifest["opaque_encrypted_fields"],
            "original_sources_checked": check_sources,
            "credentials_included": False,
            "transcripts_private": True, "off_host_backup": False}


def archive(sources: dict[str, Path], destination: Path) -> dict:
    destination = destination.absolute()
    if destination.exists():
        raise ValueError("Destination exists; archives are never overwritten")
    for label, source in sources.items():
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", label):
            raise ValueError("Component labels must be lowercase safe names")
        if not source.exists() or source.is_symlink():
            raise ValueError(f"Missing or symlink source: {label}")
        if source.is_dir() and (source.resolve() == destination.resolve()
                              or source.resolve() in destination.resolve().parents):
            raise ValueError("Destination cannot be inside a source")
    partial = destination.with_name(destination.name + ".partial")
    partial.mkdir(mode=0o700, parents=True, exist_ok=False)
    files, omissions, opaque_fields = [], [], 0
    # Failure leaves a clearly named private partial for inspection. No source is changed.
    for label, source in sorted(sources.items()):
        paths = sorted(source.rglob("*")) if source.is_dir() else [source]
        for path in paths:
            relative = path.relative_to(source) if source.is_dir() else Path(path.name)
            if path.is_symlink() or excluded(relative):
                omissions.append({"component": label, "path": relative.as_posix(),
                                  "reason": "symlink or excluded credential/cache path"})
                continue
            if not path.is_file():
                continue
            data = path.read_bytes()
            try:
                opaque_fields += scan_for_secrets(data)
            except ValueError as exc:
                raise ValueError(f"{label}/{relative}: {exc}") from exc
            target = partial / label / relative
            target.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
            target.write_bytes(data)
            target.chmod(0o600)
            files.append({"component": label, "source_relative": relative.as_posix(),
                          "path": target.relative_to(partial).as_posix(),
                          "bytes": len(data), "sha256": digest(data),
                          "source_mtime_ns": path.stat().st_mtime_ns})
    manifest = {"schema_version": 1,
                "snapshot_utc": datetime.now(timezone.utc).isoformat(),
                "sources": {label: str(path.absolute()) for label, path in sources.items()},
                "files": files, "excluded": omissions,
                "opaque_encrypted_fields": opaque_fields,
                "archive_tool_sha256": digest(Path(__file__).read_bytes()),
                "purpose": "private evidence snapshot; never resume a runner from this copy"}
    (partial / "manifest.json").write_bytes(encoded(manifest))
    (partial / "SHA256SUMS").write_text(
        "".join(f"{e['sha256']}  {e['path']}\n" for e in files))
    summary = verify(partial, check_sources=True)
    partial.rename(destination)
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    create = commands.add_parser("archive", help="Create a new private snapshot")
    create.add_argument("--source", action="append", required=True, metavar="LABEL=PATH")
    create.add_argument("--destination", type=Path, required=True)
    create.add_argument("--public-index", type=Path)
    check = commands.add_parser("verify", help="Check saved bytes, without API calls")
    check.add_argument("destination", type=Path)
    check.add_argument("--check-sources", action="store_true")
    args = parser.parse_args()
    os.umask(0o077)
    if args.command == "verify":
        result = verify(args.destination, args.check_sources)
    else:
        sources = {}
        for spec in args.source:
            label, separator, path = spec.partition("=")
            if not separator or label in sources:
                parser.error("Sources need unique LABEL=PATH arguments")
            sources[label] = Path(path)
        result = archive(sources, args.destination)
        if args.public_index:
            if (args.public_index.resolve() == args.destination.resolve()
                    or args.destination.resolve() in args.public_index.resolve().parents):
                parser.error("Public index must be outside the immutable archive")
            args.public_index.parent.mkdir(parents=True, exist_ok=True)
            args.public_index.write_bytes(encoded(result))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
