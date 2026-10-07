# Experiment ledger for the Task 2 integration

Organizer submissions and remaining allowances are tracked separately in the
[submission ledger](../submission-ledger.md). Model-only experiments below do not
consume an organizer run allowance.

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
