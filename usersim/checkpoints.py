"""Shared atomic JSON persistence and request hashing."""

import hashlib
import json
import os


def digest(value):
    """Return the existing canonical JSON SHA-256 digest."""

    return hashlib.sha256(
        json.dumps(value, sort_keys=True, ensure_ascii=False).encode()
    ).hexdigest()


def atomic(path, value):
    """Write JSON through the existing same-directory replacement pattern."""

    temporary = path.with_suffix(".tmp")
    with temporary.open("w") as handle:
        json.dump(value, handle, indent=2)
        handle.flush()
        os.fsync(handle.fileno())
    temporary.replace(path)


__all__ = ["atomic", "digest"]
