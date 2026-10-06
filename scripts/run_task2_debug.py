"""CLI entry point for the checkpointed Task 2 debug runner."""

import sys
from pathlib import Path

# Support `python scripts/run_task2_debug.py` from an uninstalled checkout.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from usersim.task2.debug import main

if __name__ == "__main__":
    main()
