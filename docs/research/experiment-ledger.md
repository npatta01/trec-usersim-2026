# Experiment ledger

The [method decision summary](method-decisions.md) covers the earlier local and
hosted-model, prompt, few-shot, editor, long-history and literature-adaptation
screens, with their controls and limitations. [Official-data evidence](official-data-evidence.md)
records the separate training audit. Dated integration and recovery entries
below preserve execution history; the [submission ledger](../submission-ledger.md)
is the canonical organizer-run inventory.

## October 10: official Task 2 complete and reconciled

Official run `np-labs-luna-style-task2-official-20261009-v1` reached the organizer's
explicit HTTP428 completion. Fresh GET status is complete with no current
conversation; the team summary confirms **57 processed and zero remaining**.
Final accounting: **49 normal researcher stops, eight administrative closures**
(five backend-error and three unanswered-timeout closures), **266 submitted
turns**, 258 generated draft/editor pairs and 516 model calls. Actual model cost
is **$0.173554630**; $1.908891500 is reservation accounting, not spending. Three
earlier delayed replies were recovered without reposting. Three official Task 2
allowances and five debug allowances remain. Debug v5 stays intentionally paused.

The last POST was accepted, but our Task 2 parser rejected the organizer's exact
run-ID-bound completion wording, already supported by Task 1. Recovery then
masked that protocol error. A source-reviewed local reconciliation preserved the
frozen runtime/manifest, prior halted checkpoint and secondary error, bound the
original receipt to fresh GET evidence, replayed all cached requests and outcomes,
and advanced the last turn once as a normal stop. It made **no POST or model
request**. The last message was not resent; no additional run was started.

The final audit verifies all 57 unique conversation IDs, saved request/output
pairs, administrative evidence, counters, frozen sources and remote completion.
Its 91 synthetic controls include terminal wording/ID tampering, source and GET
request binding, mixed recovery, partial archive and interruption replay. The
public runner shares the exact run-bound completion classifier with Task 1 and
only dispatches recovery for classified timeout/backend evidence. All 139 tests
under `tests/` and 92 subtests pass. Bare repository pytest still has two existing
organizer-starter collection errors: missing `PersonaDefinition` in
`simulator/tests/test_response_strategies.py` and `test_user_simulator.py`.

Both official tasks now have one completed submission. This is submission and
integrity evidence, not a human-realism rate or competition score. Knowledge,
persona differentiation and persistence limitations remain documented. Next:
review organizer evaluation when available; no further run is needed to complete
this baseline. [Submission ledger](../submission-ledger.md).

Earlier dated checkpoints below preserve history and are superseded by this
completion record.

## October 9: reassess the timeout waiting limit

The user questioned the 30-minute wait. Local transport timestamps and saved
reply-file times show the three recovered replies were detected approximately
31, 62 and 92 seconds after the 180-second POST timeout. The two subsequent
unanswered requests produced no reply during the full 30-minute grace and were
closed distinctly. This supports a short delayed-reply wait; it does not establish
that 30 minutes is needed or that five minutes will always suffice.

Proposed operator change: 300-second first-observation grace, retaining exact
history checks, one distinct close, no original repost and existing outage limits.
Independent recovery review assessed the source-bound amendment and audit
requirements. The proposal is not applied; the current official run retains its
frozen 1,800-second policy. No model or organizer calls were made for this timing
inspection. Local file times are approximate observation evidence, not independent
network attestation or a simulator-quality result.

Reviewer recommendation: 300 seconds is reasonable for future timeout indices,
but retain the currently pending timeout's frozen policy. A change requires a
clean no-inflight boundary, explicit versioned selector, archived source/policy
lineage, per-event policy bindings, a dual-policy completion audit and a reviewed
replacement watcher. Three recovered replies do not establish the latency tail.
A constant edit would erase which policy governed earlier observations, so the
reviewed plan excludes it. Given ten remaining conversations, finishing under
the current policy may be more proportionate than a migration; the shorter option
remains a proposal.

## October 9: official monitoring and recovery verification

Operator verification only; the selected generator, editor, model and runtime
remain frozen. One official Task 2 run is in progress. Its latest verified
checkpoint has 40 normal endings and seven administrative closures:
47 of 57 conversations processed, 226 checkpointed turns, 440 model calls and
$0.146237160 actual model cost. The current unanswered request is in the existing
30-minute grace period; no completion claim or additional official start.

Timeouts 188 and 208 exhausted that full grace; their distinct closes at 189 and
209 each returned HTTP200/new conversation. Bounded real-event checks reproduced
both pairs of cached generation requests and verified their retained closure
evidence, with no new model or organizer request. These are not independent
full-prefix replay. HTTP502 at 211 also advanced through a distinct close at 212.
Timeout 226 is now awaiting a delayed reply under the same policy.

Three earlier delayed replies were reconciled without resubmitting their original
requests. The completion checker now verifies normal receipts, continuing delayed
replies, backend-error closures and strictly proven timeout closures after the
grace period. All 74 synthetic audit checks and four watcher controls passed;
independent review cleared the exact checker and watcher before installation.
The checker distinguishes normal endings from administrative closures and will
replay cached requests, then obtain fresh read-only server confirmation only
after the run finishes. Local timestamps and retained evidence are not independent
network attestation. Unbound or uncertain recovery evidence fails closed.

These checks establish integration integrity, not realism or an official score.
[Current recovery evidence](task2-recovery-plan.md) and
[submission ledger](../submission-ledger.md) remain canonical for run accounting.

## October 9: intentional debug pause and baseline-readiness review

Operator decision, no new generator experiment. User chose to stop debug and
proceed toward one official baseline. v5 paused safely at 886 turns: 129 normal
endings, 38 administrative closures, one unfinished conversation; cost $0.664036040.
All848 generated submission pairs and 1,696 model requests replay; fresh server
history matches. No pending request, error or completion claim.

Independent review: four purposive conversations / 32 researcher turns, including
late eleven- and seven-turn histories; primary inspected 56 turns in eight cases.
Baseline readiness approved with explicit knowledge/persona/persistence limits,
not a global realism score. The private operator launch gate preserves the runtime
and official default 24 outage limit; ordinary completed-debug CLI stays unchanged.
Ten launch tests include a complete synthetic official loop, a restart that
makes no new POST, evidence/ID/snapshot tampering and failure-recording checks.
Independent source review cleared exact launcher before use. One official run
started with HTTP200; remaining official Task 2 quota 3 confirmed by GET. No official
completion claim yet.
[Canonical readiness evidence](task2-recovery-plan.md).

## October 9: budget and audit continuation; no simulator change

v5 reached 799 submitted turns: 114 normal conversation endings, 35 administrative
server-error closures and 1,528 successful model calls. Actual model cost was
$0.599974420; cumulative reservations were $5.998019400. The next draft was absent
and the $6 reservation guard halted before another request. Under the user's
instruction to increase budget and finish, an independently reviewed migration
raised only this run's reservation cap to $12. The same run resumed with its
1,000-turn guard, 30-turn conversation guard, 48/25%/3 outage limits and unchanged
generator/editor. No new organizer start or allowance was used.

Dry-run and apply each replayed all 1,528 cached generation requests and confirmed
exact current history with a fresh GET. Old manifest, frozen source, policy,
halted state and error are archived privately in `migration-before-budget-12/`.
Configuration, source, policy and state hashes passed post-apply verification;
enabling the state was the final write. Migration made no POST.

One original timeout at request 745 received a delayed reply during the grace
period. It was reconciled as a normal continuation, with no operational close,
repost or invented original POST receipt. A separate read-only audit helper
checks its request, transport proof, archived in-flight marker, server history,
prior/resulting state, counters and model accounting. Independent review caught
and corrected an orphan-result inventory gap; six synthetic tests and primary
verification of the real event pass. The completion and future continuation
audits require exact paired evidence. This is integrity evidence, not a global
quality or human-realism score. Await explicit HTTP428, then audit the full run.
No official Task 2 run has started. [Recovery plan](task2-recovery-plan.md).

## October 9: classified agent availability recovery

Engineering correction only. A new HTTP503 at650 identified an unavailable
organizer agent; exact read-only persistence checks passed. Recovery previously
rejected all503s. The new shared classifier permits only the structured,
conversation-bound agent-unavailable response, preserving all outage and uncertain
request guards. Generic503/504 still halt. A frozen policy key discloses the
accepted subset; delayed-reply evidence must revalidate original classification.

135 runtime tests / 86 subtests pass, including fail-first coverage and one-close/crash/delayed
reply/negative controls. Independent review cleared corrected source pins and
migration. All 1,252 cached generation requests replayed unchanged. A distinct
close at 651 returned HTTP200/new scenario and advanced to 652: 92 normal endings,
26 administrative closures, $0.489702915 actual cost. No original repost, model
call for the close, new allowance or official start. Continue the same debug;
this is no claim of simulator quality. [Recovery evidence](task2-recovery-plan.md).

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
