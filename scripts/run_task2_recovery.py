"""Explicit debug/official Task 2 CLI with verified backend-error recovery."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from usersim.task2.recovery import main

if __name__ == "__main__":
    main()
