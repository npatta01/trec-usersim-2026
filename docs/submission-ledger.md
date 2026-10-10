# Submission ledger

Last reconciled: October 9, 2026. This is the canonical inventory of organizer
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
run has started with HTTP200 and is still in progress.

## Allowances

| Task / mode | Initially available | Runs started | Remaining |
|---|---:|---:|---:|
| Task 1 official | 4 | 1 | **3** |
| Task 1 debug | 10 | 2 | **8** |
| Task 2 official | 4 | 1 | **3** |
| Task 2 debug | 10 | 5 | **5** |

Initial counts were verified before the first debug run. Latest saved HTTP200
`/budget/check` agrees with this table (`task2-official-luna-20261009-v1/budget-after-start.json`). Debug and official allowances are separate,
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
| Oct 7 | Task 2 debug | `np-labs-luna-task2-debug-20261007-v3` | halted: 0 completed, 0 operational skips; 3 checkpointed turns | 0.002196115 |
| Oct 8 | Task 2 debug | `np-labs-luna-task2-debug-v4` | halted: 3 completed, 0 operational skips; 17 checkpointed turns | 0.014966260 |
| Oct 8–9 | Task 2 debug | `np-labs-luna-task2-debug-v5` | **Intentionally paused:** 886 saved turns, 129 normal endings, 38 administrative closures, 1 unfinished conversation; audited prefix, no HTTP428 | 0.664036040 |
| Oct 9 | Task 2 official | `np-labs-luna-style-task2-official-20261009-v1` | **In progress:** HTTP200 start, first exchange saved; Luna full history plus style edit, default 24/25%/3 outage policy | Pending final accounting |

There are exactly **two official runs started**: Task 1 is complete, Task 2 is
still in progress. The two Task 1 debug runs each
contain 64 predictions, but should not be added to the 62 official predictions as
one 190-example official evaluation or treated as 190 independent examples.
Model-only editor comparisons, synthetic probes and offline replays are not
additional organizer submissions. Run-name proposals in historical notes are not
runs unless listed here with start evidence.

Official Task 2 continues in a background service. A separate reviewed watcher
will confirm successful completion by replaying retained inputs/outputs and
checking fresh organizer status after explicit final HTTP428. Its current audit
also verifies proven delayed ReadTimeout replies, retaining GET evidence separately
from POST receipts. Monitoring observed consecutive delayed replies recovered
without resends, and a separately verified HTTP502 administrative closure. The
independently reviewed replacement audit verifies original/closing receipts,
exact server history, intent, limits and counters; normal endings and error
closures are reported separately. Seventy-four audit tests and four watcher
controls pass, including mixed delayed/closure paths, grace-period closure
proofs and confirmed receipt-before-pending-removal replay without another POST.
The new checker retains a full 30-minute grace and validates ordered recorded
timestamps; it does not change live recovery. Unbound archived diagnostics and unrecognized recovery
variants require a separate review. No completion or
whole-run quality claim is made while it runs.

## Exact inputs and outputs are retained privately

For the completed Task 1 official run, all 62 cases and 124 model-call receipts were audited again
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

Earlier runners used different filenames: the first debug run's `case-NNNN.json`
contains `item`, `request`, `response` and reservation together. Do not assume all
historical runs use the current file layout.

## Decisions and next action

Task 1 is submitted. The user chose to pause Task 2 v5 and proceed toward one
official baseline. The exact 886-turn prefix, pause boundary and current server
history pass read-only audit. Independent selective review approves baseline
readiness with explicit persona/knowledge/persistence limitations. A separately
reviewed private operator launcher binds that evidence; the ordinary CLI's
completed-debug requirement remains unchanged. Keep v5 paused. Independent source
review cleared the private operator launcher and 10 synthetic tests pass. One
official run has started with HTTP200, using default 24/25%/3 recovery limits, $6 cumulative
model reservations, 1,000 total turns and 30 turns per conversation. Preserve every
input, model call, submitted message and response privately; require explicit
HTTP428 and a final audit. Never blindly resend a persisted failed message.
See the [recovery plan](research/task2-recovery-plan.md).

Update this ledger whenever an organizer run starts, halts, resumes or completes.
Record a new quota snapshot after the transition; distinguish predictions, model
calls, whole conversations and run allowances. Keep private transcripts and keys
out of this public-shareable summary.

## October 7 active Task 2 debug attempt

Run `np-labs-luna-task2-debug-20261007-v3` started after organizer outage-resolution
notice and explicit user authorization. Start and first continue returned HTTP200;
one exchange confirmed, run still active. Before-start budget: Task 2 debug8.
Expected remaining7 after this start; post-start quota not independently checked yet.
This section supersedes the older Task 2 debug count while this run is active.
Receipts: `/home/npatta01/data/trec-usersim-runs/task2-debug-luna-20261007-v3/`.
See [handoff](research/task2-debug-third-attempt.md). No official Task 2 run.

### October 7 status reconciliation

Third Task 2 debug attempt halted on HTTP500 generating the fourth agent reply.
Three successful exchanges; GET debug/session confirms seven messages ending
in the fourth saved researcher message. Zero completed conversations. Service
failed and local state reconciled to halted; no repost or new run. GET budget
confirms Task 2 debug7, official4; Task 1 debug8, official 3. Organizer outage
announcement did not establish resolution for this attempt. Private receipts
include session_status_check.json and budget_status_check.json.

## Fourth Task 2 debug attempt

User explicitly authorized another endpoint check. Run: `np-labs-luna-task2-debug-v4`.
Same unchanged Task 2 simulator (source c6525aa), sequential requests, $3 reservation
ceiling, halt on server failure. No official submission and no retry of old turns.
Persistent service: `trec-usersim-task2-debug-v4.service`.
Private receipts: `/home/npatta01/data/trec-usersim-runs/task2-debug-luna-v4/`.
Status: launched; check receipts and service before claiming completion or quota.
Latest mailbox search found no newer general repair instructions beyond the
previous outage notice; a newer reply grants a different team replacement access,
which does not authorize use of that team's credentials.

## v4 checkpoint migration and same-run resume

91 tests / 50 subtests pass after the transition and failure-status fixes.
Archived original manifest, frozen source, state and error in private
`migration-before-transition-fix/`. Replayed all five receipts; live GET matches
the new empty scenario exactly. State: one completed conversation, five user
turns, ten model calls, $0.004555995. Read-only budget confirms six debug
allowances remain. Same v4 service restarted; no new run or closing-message
resend. Generator/editor/model configuration unchanged. On later failures the
CLI now marks state halted and refreshes costs without clearing retry guards.
Check private state/receipts for current progress.

## Fifth Task 2 debug attempt — October 8

User explicitly authorized another debug allowance after read-only recovery
check found v4 still ending with the persisted unanswered user message.
Started `np-labs-luna-task2-debug-v5` with the tested HTTP200 transition fix and
failure-status accounting; generator/model/style policy unchanged. Sequential
requests, $3 reservation ceiling, stop on errors. No official submission.
Private artifacts: `/home/npatta01/data/trec-usersim-runs/task2-debug-luna-v5/`.
Service: `trec-usersim-task2-debug-v5.service`. Inspect live state for progress.
v4 remains halted with three completed conversations; no saved turn was resent.

## v5 user-authorized skip and same-run resume

Read-only reconciliation confirmed the fourth conversation ended with the
already-persisted failed user turn. User explicitly authorized trying a skip.
Sent one distinct operational closing message with is_final=true, checkpointed
as continue-0021; no failed message resend. HTTP200 confirmed a new empty
scenario. State preserves three completed conversations and separately records
one skipped conversation, one accepted error turn and one operational close.
The closing text is not counted as a natural researcher stop. Next request index
is22 to avoid reusing failed-turn model receipts. Original state, intent, server
response and before/after budget are saved privately. Five debug allowances
remain: no new allowance consumed. Same v5 service resumed; no automatic skip
policy enabled. If another failure occurs, halt and reconcile again.

## v5 resume after HTTP502

User requested resuming. Read-only session confirmed the failed turn saved with
no agent reply. Applied the previously successful explicit closing procedure;
continue-0065 returned HTTP200/new empty scenario. Nine completed conversations,
two separately recorded operational skips. No failed message resent. Source and
model policy unchanged; same service restarted at next index66. Five debug
allowances remain, verified after close. Private skip-502-intent/result and
pre/post-skip-502 checkpoints preserve this recovery. No automatic future skip.

Existing v5 organizer description predates operational recovery; it cannot be
retroactively changed. Skips are fully recorded in this ledger and private
recovery-policy/receipts. Fresh recovery runs disclose skips at start.

## v5 recovery-wrapper progress and timeout

The reviewed wrapper advanced v5 to 28 completed conversations and seven
separately recorded operational closes. It halted on a ReadTimeout for request
0198, after 198 checkpointed outcomes. The original pending request and all
receipts are retained. GET debug/session returned HTTP200 with matching scenario,
matching conversation and the exact persisted user turn, but no assistant reply.
This differs from a received HTTP500/502: the client has no final POST response.
No request was resent and no closing message was sent for this timeout.
Private `recovery/0198-timeout-session.json` and `0198-timeout-budget.json` preserve
the observation. Budget check still shows Task 2 debug 5/official4 and Task 1
debug8/official 3. Model cost is $0.147200385 in 384 calls. Official Task 2 remains
gated on completed debug evidence and conversation review.

## v5 manual timeout closure and resume

Fresh GET session, following two earlier observations, confirmed the exact
unanswered request 0198 after more than 45 minutes. A reviewed one-off recovery
archived the original in-flight marker and state, verified all raw message fields
and the unchanged source, then sent one distinct final message at 0199. HTTP200
confirmed a new empty scenario. State advanced to 200 with 28 completed and 8 skips;
no new debug run or model call was needed for closure. Same recovery service was
restarted. The automatic 500/502 policy is unchanged; this is a manual timeout
exception, not evidence that arbitrary uncertain requests can be retried.
Private `recovery/0198-timeout-*` artifacts retain observations, original pending
request, intent, exact closing payload/receipt linkage, result, reviewed script
and review hash. No response receipt was fabricated for the original timed-out
POST. Official Task 2 remains unstarted.

## v5 second timeout closure and resume

The resumed run reached 40 completed conversations and 10 operational closes,
then timed out at 0288. GET session confirmed the exact persisted unanswered
message after 118 minutes. Reused the independently reviewed one-off procedure
with only the request index, original request hash and artifact filenames changed.
Offline reconciliation and three mismatch controls passed; a fresh GET preceded
the single distinct final close at 0289. HTTP200 confirmed a new empty scenario.
State resumed at 290 with 40 completed and 11 operational closes. No original
request was resent; no missing POST receipt invented. Source and generation
behavior are unchanged. Same recovery service runs, with skip limit 12 unchanged.
Private `recovery/0288-timeout-*` records preserve the original request, observations,
intent, closing result, script and verification provenance. Cost at restart was
$0.219581060 in 558 model calls. No new allowance and no official Task 2 start.

## v5 automatic-timeout fix and same-run resume

The old runtime halted again at request 0327 after 46 completed conversations and
11 operational closures. Cost: $0.245687720 in 634 successful model calls;
reservation: $2.479191700 under the unchanged $3 ceiling. Original pending request
and error were preserved; no original response receipt was invented.

An independently reviewed generic timeout controller and explicit migration
replaced repeated manual recovery. All 634 cached model requests reproduced exactly;
receipt replay confirmed terminal counts, current history and consecutive skips 0.
Fresh GET confirmed the exact persisted original turn. The old manifest, source,
policy, state, pending/error bytes and migration provenance are archived privately
in `migration-before-timeout-v2/`; new freeze and proof hashes were verified.

Same v5 recovery service resumed at 15:26 UTC on October 9, entering read-only
timeout reconciliation. Its first durable observation starts a 30-minute grace;
no operational close 0328 had been sent at this snapshot. State remains halted
at 327 until a delayed reply or verified closure is committed. Future classified
original timeouts use this path automatically; uncertain closes still halt.

Policy v2: max 24 operational skips, max 25% of terminal conversations with a
denominator floor 8, max 3 consecutive skips. Full runtime tests 121 / 64 subtests;
optimized focused tests 34 / 14 subtests. No generator or style-policy change.
Fresh preflight still shows Task 2 debug 5 / official 4 and Task 1 debug 8 / official 3.
No new allowance and no official Task 2 start. Read live state and service before
making a newer status claim.

## v5 budget increase and same-run continuation

Automatic recovery at 0327 succeeded. The run advanced to 403 turns, 58 completed
conversations and 16 operational closures, then hit the $3 cumulative reservation
ceiling after saving draft 0403 and before editor 0403. Actual cost: $0.293755280;
reservations: $2.998644; 775 successful model calls. Neither API had an uncertain
request, and organizer 0403 had not been sent.

The user authorized increasing budget and continuing until the end. Total
reservation ceiling is now $6 for the same v5 run. The CLI flag defaults to $3
for other runs; configuration changes remain blocked without explicit migration.
No generator, model, provider, editor, stopping or recovery-policy change.

All 775 saved model requests and confirmed outcomes replayed exactly; fresh GET
matched the entire current server history. Independent review cleared the CLI
and migration after correcting the final enabling-write order. 124 runtime tests
/ 69 subtests pass; 39 focused tests / 19 subtests also pass under optimized Python.
Original manifest/state/error/source are archived in private
`migration-before-budget-6/`; reviewed script and hash-bound migration evidence
are preserved. Post-apply archive/configuration/state checks passed.
Same recovery service restarted with `--cap-usd 6`, retaining draft 0403 for reuse.
No outcome was advanced by migration; no new debug allowance or official start.
Monitor the same service until explicit organizer completion, preserving future
request/response receipts and recovery guards.

## v5 total-turn guard increase and same-run continuation

v5 paused cleanly at 500 turns with 72 normal completions, 19 operational closures,
962 model calls, $0.369902385 actual cost and $3.742345800 reservations. No error
or uncertain request remained. The user had authorized continuing until the end.
An explicit independently reviewed migration raised only this run's total-turn
guard from 500 to 1,000. Cap $6, per-conversation limit 30, generator and outage
policy are unchanged; other runs still default to 500 total turns.

All 962 cached model requests and saved outcomes replayed exactly; fresh GET
matched the current server history. Original manifest, state, source and policy
are byte-preserved privately in `migration-before-total-turns-1000/`. The new
configuration and migration evidence became durable before final state
enablement; post-apply hashes and unchanged counters passed. Same v5 service
resumed with `--cap-usd 6 --max-total-turns 1000`. No start/request repeated,
no new debug allowance, no official start. Runtime tests: 126 / 73 subtests.
This is a resume checkpoint, not explicit run completion or quality approval.
