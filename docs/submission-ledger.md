# Submission ledger

Last reconciled: October 10, 2026. This is the canonical inventory of organizer
runs. It is separate from the [experiment ledger](research/experiment-ledger.md),
which also records model-only comparisons that consume no organizer allowance.

## What the numbers mean

A **run** is one complete attempt covering the organizer's supplied cases. A
**prediction** is one researcher message submitted within that run. Our Task 1
official run contained 62 predictions and used **one**, not 62, official allowances.
Two model calls per prediction (draft and editor) produced 124 model calls; those
are not 124 organizer runs either. Dollar costs below are reported model API
usage, separate from the organizer's run quota.

## Training, debug and official coverage are different counts

| Collection / run | Count | Meaning |
|---|---:|---|
| Supplied official training export | 64 | Human conversation records available for development |
| Task 1 official test pool | 62 over 10 goals | Turn-prediction cases; our completed official run submitted 62 predictions |
| Task 2 official test pool | 57 over 11 goals | Official end-to-end conversations, as defined by the organizers |
| Current Task 2 debug prefix | 129 normal endings + 38 error closures + 1 unfinished = 168 opened | Intentionally paused development run; not the full debug pool or an official run |

The [organizer guidelines](https://trec.usersim.ai/guidelines) explicitly separate
the two official test pools. The reported 57-conversation official Task 2 run
is therefore compatible with our larger debug run. Read-only inspection of our
debug prefix at 835 saved turns found 158 conversation IDs across 53 exact
scenario records: 52 records appeared three times and one appeared twice.
Those are scenario-agent conversations, not 158 original human training logs,
158 participants or 158 organizer allowances. This snapshot is not the final
debug pool size. Only one v5 debug run was being continued; it is now intentionally paused. One official Task 2
run completed with explicit HTTP428 and a final integrity audit.

## Allowances

| Task / mode | Initially available | Runs started | Remaining |
|---|---:|---:|---:|
| Task 1 official | 4 | 1 | **3** |
| Task 1 debug | 10 | 2 | **8** |
| Task 2 official | 4 | 1 | **3** |
| Task 2 debug | 10 | 5 | **5** |

Initial counts were verified before the first debug run. Latest saved HTTP200
`/budget/check` agrees with this table (`task2-official-luna-20261009-v1/final-budget.json`). Debug and official allowances are separate,
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
| Oct 7 | Task 2 debug | `np-labs-luna-task2-debug-20261007-v3` | halted: 0 completed, 0 operational skips; 3 checkpointed turns; 8 priced model receipts including the fourth attempted turn | 0.003852275 |
| Oct 8 | Task 2 debug | `np-labs-luna-task2-debug-v4` | halted: 3 completed, 0 operational skips; 17 checkpointed turns | 0.014966260 |
| Oct 8–9 | Task 2 debug | `np-labs-luna-task2-debug-v5` | **Intentionally paused:** 886 saved turns, 129 normal endings, 38 administrative closures, 1 unfinished conversation; audited prefix, no HTTP428 | 0.664036040 |
| Oct 9–10 | Task 2 official | `np-labs-luna-style-task2-official-20261009-v1` | **Complete: 57/57 processed**; 49 normal stops, 8 administrative closures; 266 submitted turns, 258 generated pairs / 516 model calls; explicit HTTP428 and final audit | 0.173554630 |

There are exactly **two official runs started, both complete**: one for Task 1
and one for Task 2. The two Task 1 debug runs each
contain 64 predictions, but should not be added to the 62 official predictions as
one 190-example official evaluation or treated as 190 independent examples.
Model-only editor comparisons, synthetic probes and offline replays are not
additional organizer submissions. Run-name proposals in historical notes are not
runs unless listed here with start evidence.

Costs use saved response usage, not only checkpoint accounting. The October 10
paper-preservation audit found two priced model calls for debug-v3's fourth
attempted turn omitted from its checkpoint counters. All eight receipts sum to
$0.003852275; the unchanged checkpoint records six calls / $0.002196115. The
[$0.001656160 accounting difference](../submissions/README.md#evidence-gaps-and-accounting)
is exposed in the machine-readable inventory. Other listed run costs reconcile
to their retained model receipts. This correction is not another organizer run.

Official Task 2 is remotely complete: fresh status has no current conversation,
and team summary reports 57 done / zero remaining. The final audit independently
replays every cached model request and submitted text/stop flag, preserving the
49 normal stops separately from eight administrative closures (five backend,
three timeout). Three delayed replies required neither repost nor close.

The final HTTP428 used exact run-ID-bound wording that our Task 2 parser initially
rejected. A reviewed local reconciliation archived the original halted state and
masked secondary error, retained the frozen runtime and manifest, and advanced
that accepted final message once. No original POST was repeated, model called or
additional allowance consumed. All 91 audit controls pass; the saved final report
binds receipt, reconciliation, GET, source and state hashes. This establishes
completion/integrity, not an official score or whole-run quality rating.

Model receipts sum to $0.173554630 actual Task 2 cost. Cumulative reservation
accounting is $1.908891500. Debug v5 remains paused at 886 turns; its cost and
coverage are separate. The frozen 30-minute timeout grace was preserved for this
run. Observed delayed replies arrived roughly 31–92 seconds after the POST
timeout; a shorter future grace is a proposal, not an applied or proven limit.


## Exact inputs and outputs are retained privately

All available run records are now also preserved in a checksum-verified archive
**inside the stable local repository directory**, ignored by git and absent from
GitHub. The [public run index](../submissions/manifest.json) covers all nine runs;
the [paper preservation guide](paper/preservation.md) records location, original
sources, hashes and verification commands. The archive includes detailed
development evidence as well as submissions, but cannot recreate missing
historical receipts. The [paper evidence map](paper/README.md) tracks remaining
score/venue/author gaps.

For the completed Task 1 official run, all 62 cases and 124 model-call receipts were audited again
when this ledger was added. Each case retains:

- Organizer input: persona, goal and complete supplied conversation prefix.
- Exact draft and editor API request payloads, including system instructions and roles.
- Raw model responses, usage/cost, generated draft and selected final response.
- Exact organizer submission payload and corresponding HTTP receipt; model
  response timestamps and original file metadata where available. These do not
  establish a measured end-to-end latency distribution.
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
| Third Task 2 debug | `$RUNS/task2-debug-luna-20261007-v3/` |
| Fourth Task 2 debug | `$RUNS/task2-debug-luna-v4/` |
| Current paused Task 2 debug | `$RUNS/task2-debug-luna-v5/` |
| Task 2 official | `$RUNS/task2-official-luna-20261009-v1/` |

In the Task 1 official directory:

| File pattern | Contents |
|---|---|
| `case-NNNN.json` | Input, draft, selected response and exact submission payload |
| `model/case-NNNN-draft.json` | Full draft request and raw response/cost |
| `model/case-NNNN-edit.json` | Full editor request and raw response/cost |
| `organizer/start.json`, `organizer/continue-NNNN.json` | Exact organizer requests and replies |
| `manifest.json`, `frozen/`, `recovery/` | Reproducibility and source-amendment evidence |
| `result.json`, `audit.json` | Completion, counts, cost and integrity audit |
| `final-status.json`, `final-summary.json`, `final-budget.json` | Read-only organizer confirmation and remaining quota |

In the Task 2 official directory:

| File pattern | Contents |
|---|---|
| `model/turn-NNNN-{draft,edit}.json` | Exact full requests, raw outputs and usage/cost for all 258 generated pairs |
| `organizer/start.json`, `organizer/continue-NNNN.json` | Saved start and received continuation request/response receipts |
| `organizer/transport-error-continue-NNNN.json` | Transport failures; no fabricated successful POST receipt |
| `recovery/`, `reconciliation/` | Verified delayed replies and original/closing administrative evidence |
| `terminal-reconciliation/` | Original halted state and secondary error, bound terminal intent and result |
| `manifest.json`, `frozen/`, `readiness/`, `recovery-policy.json` | Unchanged runtime/configuration and audited paused-prefix readiness |
| `completion-audit-tools/`, `completion-terminal-audit-source-review.json` | Exact separately reviewed audit/reconciliation source and review pins |
| `integrity-audit.json`, `final-status.json`, `final-summary.json`, `final-budget.json` | Full replay and read-only completion/coverage/quota confirmation |

Earlier runners used different filenames: the first debug run's `case-NNNN.json`
contains `item`, `request`, `response` and reservation together. Do not assume all
historical runs use the current file layout.

The first Task 1 debug retains all 64 input/model request/response records and
its final accepted organizer request plus HTTP428 completion. Its start and
per-prediction organizer POST receipts were not saved. Both later Task 1 runs
retain their per-prediction organizer receipts; the archival inventory makes
this historical evidence gap explicit.

## Decisions and next action

Both official tasks are submitted and complete. Task 1 has 62 predictions; Task 2
has 57 processed conversations (49 normal endings and eight administrative
closures). No further submission is needed for this baseline. Review organizer
results when available; no competition score or whole-run realism rate is
claimed. Keep debug v5 intentionally paused and retain private inputs/outputs,
receipts, frozen sources and reconciliation evidence. Never resend an accepted
or uncertain original message. See the [recovery plan](research/task2-recovery-plan.md).

Update this ledger whenever an organizer run starts, halts, resumes or completes.
Record a new quota snapshot after the transition; distinguish predictions, model
calls, whole conversations and run allowances. Keep private transcripts and keys
out of this public-shareable summary.

## Historical checkpoints

The [full dated submission history](research/archive/2026-10-10-submission-history.md)
preserves older progress reports, quota snapshots, outages and migrations.
Those checkpoints are superseded by the current inventory above.
