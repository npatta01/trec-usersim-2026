# Experiment ledger for the Task 2 integration

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
