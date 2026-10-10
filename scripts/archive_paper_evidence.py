"""Thin entry point for offline, private evidence preservation."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.evidence.archive import main

if __name__ == "__main__":
    main()
