"""CLI entry point for the checkpointed Task 1 runner."""

import sys
from pathlib import Path

# Support `python scripts/run_task1.py` from an uninstalled checkout.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from usersim.task1 import main


if __name__ == "__main__":
    main()
