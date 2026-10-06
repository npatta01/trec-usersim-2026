# Code structure refactor

## Objective

Separate the supported Task 2 runtime from historical experiments and tests,
while preserving model requests and checkpoint safety. Update PR #2. No live
organizer or model calls.

## Design

- `usersim/`: reusable prompt, request, and checkpoint helpers.
- `usersim/task2/`: conversation types, generation, protocol, model checkpointing,
  and debug orchestration.
- `scripts/run_task2_debug.py`: thin supported CLI entry point.
- `experiments/`: historical replay scripts and optional unselected generators.
- `tests/`: offline regression tests and synthetic request-parity fixtures.

Runtime imports must never depend on `experiments` or `scripts`. Preserve exact
requests on synthetic opening, follow-up, long-history, missing-field, and stop
cases, captured from pre-refactor commit `946aacf`. Retain organizer baseline
modules under `simulator/` for provenance. Historical run files remain untouched;
source hashes deliberately prevent resuming them with changed code.

## Steps and verification

1. Capture synthetic reference requests before moving code.
2. Extract pure helpers, removing global completion monkeypatch from runtime.
3. Move runtime, experiments, and tests; update imports, source freeze, CLI/docs.
4. Verify request parity, all existing recovery tests, import isolation, CLI help,
   diagrams, links, and secret checks. Obtain independent code review.
5. Commit and update PR #2. No merge or live retry.

Status: implemented and verified. Independent Sol follow-up review found no
remaining actionable issues after the two integration fixes below.

## Evidence

- 60 offline tests pass normally and under optimized Python.
- All 12 synthetic cases reproduce both model request dictionaries and generated
  result handling exactly; no participant data appears in these fixtures.
- Runtime imports load no experiment modules, runner scripts, or LiteLLM.
- The supported Task 2 CLI works from outside the checkout. Historical commands
  intentionally migrate to `python -m experiments.NAME`; all seven show help.
- Review found a test-package namespace collision during whole-repository pytest
  collection. Removing the unnecessary new `tests/__init__.py` restores collection
  to 83 collected tests and only the two previously verified `PersonaDefinition`
  errors in the organizer's unchanged legacy tests.
- Review also found historical scripts using a new request helper while hashing
  the old one. Restoring their original helper imports keeps their recorded
  provenance accurate; live runtime imports remain independent.
- Four architecture diagrams render; source freeze follows the new package.
- GitHub had no posted review comments or checks when queried. Additional feedback
  visible only in the Codex review panel needs its text to be assessed.

The prior four-model panel's helper-coupling concern is resolved. Its prior
approval/disposition record does not imply review of this new refactor; a separate
independent follow-up checks this revision. No live run was resumed.
