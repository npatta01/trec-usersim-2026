#!/usr/bin/env python3
"""Create an offline viewer of saved receipts, or an explicitly synthetic demo."""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.run_viewer.export import render, task1, task2


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--task1-dir', type=Path)
    parser.add_argument('--task2-dir', type=Path)
    parser.add_argument('--task2-conversation', type=int, default=1, help='1-based ordinary conversation; missing/error receipts refuse export')
    parser.add_argument('--demo', action='store_true', help='Use only invented, labeled example data')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.demo:
        if args.task1_dir or args.task2_dir:
            parser.error('Demo mode cannot read private runs')
        data = json.loads((ROOT / 'tools/run_viewer/demo.json').read_text())
    else:
        if not (args.task1_dir or args.task2_dir):
            parser.error('Choose --demo or at least one saved run directory')
        if args.output.resolve().is_relative_to(ROOT):
            parser.error('Private reading copies must be written outside the repository')
        if args.task2_conversation < 1:
            parser.error('Conversation index must be positive')
        data = {'synthetic': False, 'source': 'Saved official run receipts; exact model messages and submitted text. Credentials and unrelated artifacts excluded.', 'runs': []}
        if args.task1_dir:
            data['runs'].append(task1(args.task1_dir))
        if args.task2_dir:
            data['runs'].append(task2(args.task2_dir, args.task2_conversation))
    render(data, args.output)
    print(f"Rendered {sum(len(r['conversations']) for r in data['runs'])} examples to {args.output}")


if __name__ == '__main__':
    main()
