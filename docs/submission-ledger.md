# Submission ledger

Last reconciled: October 6, 2026. This is the canonical inventory of organizer
runs. It is separate from the [experiment ledger](research/experiment-ledger.md),
which also records model-only comparisons that consume no organizer allowance.

## What the numbers mean

A **run** is one complete attempt covering the organizer's supplied cases. A
**prediction** is one researcher message submitted within that run. Our Task 1
official run contained 62 predictions and used **one**, not 62, official allowances.
Two model calls per prediction (draft and editor) produced 124 model calls; those
are not 124 organizer runs either. Dollar costs below are reported model API
usage, separate from the organizer's run quota.

## Allowances

| Task / mode | Initially available | Runs started | Remaining |
|---|---:|---:|---:|
| Task 1 official | 4 | 1 | **3** |
| Task 1 debug | 10 | 2 | **8** |
| Task 2 official | 4 | 0 | **4** |
| Task 2 debug | 10 | 2 | **8** |

Initial counts were verified before the first debug run. Latest saved HTTP200
`/budget/check` agrees with this table (`task2-debug-luna-20261006-v2/budget_after_500.json`). Debug and official allowances are separate,
and each task has its own allowance. A halted run still uses an allowance.
Resuming the same run did not start another run or resend accepted predictions.

## Runs actually started

| Date | Task / mode | Run ID | Status and submitted work | Model cost (USD) |
|---|---|---|---|---|---:|
| Oct 5 | Task 1 debug | `np-labs-luna-task1-debug-20261005-v1` | Complete: 64 predictions; direct Luna, no editor | 0.016750475 |
| Oct 6 | Task 1 debug | `np-labs-luna-style-task1-debug-20261006-v1` | Complete: 64 predictions; Luna plus style editor | 0.037675500 |
| Oct 6 | Task 1 official | `np-labs-luna-fidelity-task1-official-20261006-v1` | **Complete: 62 predictions across 10 goals**; Luna plus narrow fidelity editor | 0.029373225 |
| Oct 6 | Task 2 debug | `np-labs-luna-task2-debug-20261006-v1` | **Halted:** 4 researcher messages saved, 3 assistant replies, 0 complete conversations; organizer HTTP500 | 0.004248240 |
| Oct 6 | Task 2 debug | `np-labs-luna-task2-debug-20261006-v2` | **Halted:** 5 researcher messages saved, 4 assistant replies, 0 complete conversations; organizer HTTP500 | 0.005123280 |

There is exactly **one official submission**, for Task 1. The two Task 1 debug runs each
contain 64 predictions, but should not be added to the 62 official predictions as
one 190-example official evaluation or treated as 190 independent examples.
Model-only editor comparisons, synthetic probes and offline replays are not
additional organizer submissions. Run-name proposals in historical notes are not
runs unless listed here with start evidence.

## Exact inputs and outputs are retained privately

For the official run, all 62 cases and 124 model-call receipts were audited again
when this ledger was added. Each case retains:

- Organizer input: persona, goal and complete supplied conversation prefix.
- Exact draft and editor API request payloads, including system instructions and roles.
- Raw model responses, usage/cost, generated draft and selected final response.
- Exact organizer submission payload, timestamp and corresponding HTTP receipt.
- Frozen configuration and source snapshots, plus the original source and receipt
  hashes retained before the researcher-ending-prefix recovery.

The integrity audit matched every draft/editor request to its input and every
submitted message to the selected output. The organizer's completion response,
read-only run status and team summary confirm completion. This verifies record
integrity and completion, not an official realism score.

### Private artifact locations

These are local directories, not published transcript links. Do not commit their
contents. Let `RUNS=/home/npatta01/data/trec-usersim-runs` and
`OLD=/home/npatta01/.codex/worktrees/21de/trec-usersim-2026/data/official`.

| Run | Artifact directory |
|---|---|
| First Task 1 debug | `$OLD/task1-debug-luna/` |
| Second Task 1 debug | `$RUNS/task1-debug-style-20261006-v1/` |
| Task 1 official | `$RUNS/task1-official-fidelity-20261006-v1/` |
| First Task 2 debug | `$OLD/task2-debug-luna/` |
| Second Task 2 debug | `$RUNS/task2-debug-luna-20261006-v2/` |

In the official directory:

| File pattern | Contents |
|---|---|
| `case-NNNN.json` | Input, draft, selected response and exact submission payload |
| `model/case-NNNN-draft.json` | Full draft request and raw response/cost |
| `model/case-NNNN-edit.json` | Full editor request and raw response/cost |
| `organizer/start.json`, `organizer/continue-NNNN.json` | Exact organizer requests and replies |
| `manifest.json`, `frozen/`, `recovery/` | Reproducibility and source-amendment evidence |
| `result.json`, `audit.json` | Completion, counts, cost and integrity audit |
| `final-status.json`, `final-summary.json`, `final-budget.json` | Read-only organizer confirmation and remaining quota |

Earlier runners used different filenames: the first debug run's `case-NNNN.json`
contains `item`, `request`, `response` and reservation together. Do not assume all
historical runs use the current file layout.

## Decisions and next action

Task 1 is submitted; do not restart its completed run or spend another allowance
without a new decision. Task 2 remains halted; do not blindly resend its persisted
fourth or fifth message. See [Task 1 completion/recovery](research/task1-live-validation.md)
and [Task 2 second-attempt evidence](research/task2-debug-second-attempt.md).

Update this ledger whenever an organizer run starts, halts, resumes or completes.
Record a new quota snapshot after the transition; distinguish predictions, model
calls, whole conversations and run allowances. Keep private transcripts and keys
out of this public-shareable summary.
