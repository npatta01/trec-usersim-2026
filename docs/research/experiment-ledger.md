# Experiment ledger for the Task 2 integration

## October 9: absolute recovery-limit continuation

Engineering change only; no new simulator hypothesis or model experiment.
At request 635, HTTP500 and the 24-closure guard paused v5: 90 normal endings,
1,224 model calls, $0.482075295 actual cost. A reviewed frozen selector and
checkpoint migration permit 48 absolute closures for this same run while
preserving the 25% and three-consecutive-error circuits and all generation inputs.
130 runtime tests / 79 subtests pass; 9 selected-policy tests / 15 subtests pass
under optimized Python. Exact historical replay and fresh GET passed. The policy
write was last; original state/error/source/policy are archived privately.

At restart, one distinct close at 636 returned HTTP200 and advanced to 637:
90 normal endings, 25 administrative server-error closures. No original turn
was resent, no model call was used for the close and no new run allowance was
consumed. Debug is still in progress; no official Task 2 start or quality score.
[Continuation evidence](task2-recovery-plan.md).

Organizer submissions and remaining allowances are tracked separately in the
[submission ledger](../submission-ledger.md). Model-only experiments below do not
consume an organizer run allowance.

## October 9: total-turn continuation

Operational adjustment, not a new simulator variant. The clean 500-turn halt
had 72 normal completions, 19 backend-error closures and 962 model calls costing
$0.369902385. The user authorized finishing the same run. A reviewed selector
and explicit checkpoint migration raise only its total-turn guard to 1,000;
other runs default to 500. Cap $6, conversation limit 30, generator and outage
policy remain unchanged.

All 962 cached model requests, outcomes and counters replay unchanged; fresh
GET matches the current server history. Archives, exact source/policy checks and
final state enablement passed independent review and post-apply verification.
126 runtime tests / 73 subtests pass. The same service resumed with no new start,
repeated submission or allowance. Completion and semantic quality remain separate
checks; this adjustment supplies no quality score.
[Recovery evidence](task2-recovery-plan.md).

## October 9: budget continuation

Operational change, not a new simulator comparison. Recovery advanced v5 to 403
turns (58 completed,16 operational closures) before the $3 cumulative reservation
guard blocked the editor after its draft was saved. Actual cost: $0.293755280;
reservations: $2.998644; 775 successful model calls. The user authorized increasing
budget and continuing through the end. Select $6 total reservations for the same
run. No generator, style, provider or recovery-policy change.

A finite positive `--cap-usd` option preserves the $3 default and frozen-manifest
checks. Full runtime 124 tests / 69 subtests pass; optimized focused 39 / 19 pass.
The migration dry run replayed all 775 cached model requests and verified exact
current server history, without POSTs. Independent review cleared the corrected
final-write boundary. Applied archive/refreeze/configuration verification passed;
same-run service restarted with the cached draft retained. No new allowance.

## October 9: automatic original-timeout recovery

Engineering correction, with generator and style-editor requests unchanged.
The old wrapper recovered known HTTP500/502 but halted on original ReadTimeouts;
v5 required manual closures at 0198 and 0288, then halted again at 0327. The generic
controller records the exact transport error, waits for delayed replies, and
requires 30 minutes from the first exact persisted-turn observation plus a
fresh final check before one distinct operational close. Delayed replies are
stored separately from POST receipts and remain available to future prefix checks.
Closing uncertainty cannot recursively trigger another close. Policy v2 adds
24 absolute skips, a 25% fraction with denominator floor 8, and 3 consecutive skips.

Synthetic tests cover the actual full recovery loop, receipt replay, reply arrival
at the final check, evidence corruption, missing persistence and outage bounds.
A fail-first test and reviewer both identified a missing direct link from
delayed-reply evidence to its original timeout proof; fixed before migration.
A second fail-first test reproduced the durable-close-receipt/pending-marker
crash boundary; verified receipt replay now clears only an exact matching marker.
This is software verification, not a new semantic-quality experiment. See the
[recovery plan](task2-recovery-plan.md) for verification and current status.

Follow-up review cleared the corrected code and the separate legacy migration.
121 runtime tests / 64 subtests pass; 34 focused tests / 14 subtests pass under
optimized Python. All 634 saved model requests replayed unchanged. The original
frozen source and checkpoint evidence were archived before installing v2.
Same-run service resumed into read-only timeout reconciliation at 15:26 UTC,
October 9. No new debug allowance or official start; no close yet at that snapshot.

This checkout records the Task 2 PR work. Earlier private experiment outputs and
local-only research records are not published by this PR.

## October 6: architecture and recovery review

This is an engineering review, not a simulator-quality experiment. Four standard
advisor lanes reviewed one frozen packet. They identified completion matching,
start-receipt recovery, diagram accuracy, and missing crash-boundary regressions.
See [review decisions](task2-design-review.md) and the
[architecture diagrams](../task2_architecture.md). Prompt behavior remains fixed;
no organizer calls or new model experiments were made for this review.

Status: corrections verified by 56 passing script tests and an independent
follow-up review with no actionable findings. The historical live
run remains frozen after organizer HTTP500; [recovery evidence](task2-debug-handoff.md).

## October 6: behavior-preserving code structure

Extracted runtime helpers and Task 2 modules into `usersim/`, moved historical
studies into `experiments/` and tests into `tests/`. Twelve synthetic fixtures
captured at commit `946aacf` preserve exact model requests. This removes live
dependence on experiment code and the module-global completion monkeypatch.
See [refactor verification](code-structure-plan.md). No new simulator experiment
or organizer request is part of this change.

## October 6: Task 1 selected-baseline live validation

User authorized local/debug validation and conditional official submission.
Luna plus the default style editor completed 64 debug predictions across 10 goals,
for $0.0376755 (128 model calls). Exact context/request/output receipts were audited;
16 drafts changed. Live responses corrected two client assumptions: HTTP200 can
supply a new conversation, and completion can include a run-specific explanatory
sentence. Recovery reuses durable receipts without duplicate predictions.

Contextual review identified vendor-requirement relaxation and an unobserved
external-check claim; both survive unchanged from draft through style editing.
Official submission is deferred under the user's quality condition. Test content
fidelity separately from style: preserve explicit needs and distinguish researcher
knowledge from claims of performed actions, with successful controls to detect
regressions. No prompt change or new experiment is implied by this hypothesis.
[Full evidence, review limits and remaining quota](task1-live-validation.md).


## October 6: narrow Task 1 editor repair

[Plan and advisor disposition](task1-fidelity-fix.md). Four standard advisor lanes
challenged both initial failure labels and advised a narrow edit rather than goal
enforcement. V1 applied a broad fidelity editor to64 saved drafts plus8 synthetic
paired controls (80 calls, $0.0289408). Masked review found newly hardened
preferences, so reject V1. V2 preserves compromises and optionality and permits
local repair of unsupported performed-action claims; it completed the same-input comparison without newly introduced material harm
in contextual review. Targeted repeats support the action-provenance repair;
requirement enforcement remains outside its demonstrated scope. Both variants
and repeats cost $0.055381045 total (172 model calls). Neither comparison contacts
the organizer. Task 2 is unchanged. V2 is selected for the authorized conditional
Task 1 official baseline after 83 tests and exact 64-case offline replay.


## October 6: official Task 1 completion and schema recovery

The selected narrow editor baseline completed 62 official predictions across 10
goals, cost $0.029373225. After 30 accepted predictions, a researcher-only prefix
exposed an undocumented client restriction. The generic builder now preserves
researcher-ending histories and asks for a researcher continuation, without
fabricating an assistant reply. Existing requests remain unchanged. 87 tests,
a two-case synthetic provider check (four calls, $0.0005505) and a zero-network
replay verified recovery; original source snapshots and receipt hashes are kept.
The same run resumed without duplicate predictions or another run allowance.
[Completion and remaining quotas](task1-live-validation.md). No Task 2 change.
