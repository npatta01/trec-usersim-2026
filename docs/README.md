# Documentation

Start with the [illustrated architecture](task2_architecture.md) to understand
what we generate and how the two tasks differ. Both official baselines are
complete; current status and next action are in the [project handoff](project-handoff.md).

## Understand the project

- [Continue without the original chat](continuity.md): a fresh-thread reading path, decisions and durable private artifacts.
- [Artifact custody and restore](artifacts.md): private GitHub release, download verification and recovery without this machine.
- [Architecture](task2_architecture.md): tasks, model roles, draft/edit pipeline
  and recovery images.
- [Rendered input/prompt/response reader](run_viewer.md): inspect exact requests
  privately and explore a complete conversation. Public screenshots use invented examples.
- [Submission ledger](submission-ledger.md): actual runs, costs, allowances and
  private input/output locations.
- [Research status](research/README.md): selected method, evidence and open gaps.

## Run or test the code

- [Task 1 runner](task1_runner.md): independent prefixes, preview, editor selection.
- [Task 2 runner](task2_debug_runner.md): setup, execution gates and safeguards.
- [Recovery guide](research/task2-recovery-plan.md): verified delayed replies,
  administrative closes and frozen checkpoints.
- Organizer contracts: [Task 1](task1_workflow.md), [Task 2](task2_workflow.md).
- [Original starter guide](organizer-starter.md) and [experiment modules](../experiments/README.md).

## Assess the evidence

- [Paper preparation](paper/README.md): writing plan, claims, evidence, result table and remaining gaps.
- [Private preservation](paper/preservation.md): all available submission/research records, immutable inventories and offline verification.
- [Official-data inspection](research/official-data-evidence.md): schema, coverage,
  stopping signals, provenance and leakage limits.
- [Method decisions](research/method-decisions.md): tested ideas, controls, results
  and reasons for keeping or rejecting variants.
- [Experiment ledger](research/experiment-ledger.md): dated decisions and study inventory.
- [Task 1 fidelity study](research/task1-fidelity-fix.md): selected narrow repair.
- [Source refresh](research/2026-10-03-research-refresh.md): literature inspection.

## Maintain the record

Keep status in the research index, run accounting in the submission ledger, and
experiment decisions in the experiment ledger. Update diagrams when behavior
changes. Preserve historical evidence in the [archive](research/archive/README.md).
Historical next actions do not authorize a new run.

Public docs contain source, synthetic examples and aggregate findings. Raw
participant data, exact requests/outputs, receipts and keys remain private.
Software checks establish integration, not researcher realism.

See [documentation maintenance](maintenance.md) for image sources, regeneration
and the cleanup's verification record.
