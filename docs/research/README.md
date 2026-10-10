# Research status

Updated October 10, 2026. **Both official baselines are complete.** Task 1 has
62 predictions; Task 2 processed 57 conversations, with 49 normal endings and
eight administrative closures. Debug v5 is intentionally paused. The
[submission ledger](../submission-ledger.md) owns run IDs, costs and allowances.

## Selected method

Luna receives the baseline persona/goal representation and full available
utterance text, generates a researcher reply, then makes one editor call.
Task 1 official uses narrow fidelity editing; Task 2 uses style editing and keeps
the draft stop boolean. See the [illustrated architecture](../task2_architecture.md).
Compaction, retrieval, planning and repeated critic/refinement are not enabled.

The [method decisions](method-decisions.md) document local/hosted-model tests,
reminders, turn modes, few-shot examples, editors, summaries, planning and
literature adaptations. Most were small development screens. Mixed results or
near-ties did not establish recurring gains sufficient to change the broader
default; this does not prove every alternative is ineffective.

## What the data supports

The [official export audit](official-data-evidence.md) found 64 conversations,
10 goal objects, 12 distinct persona profiles and 266 researcher-message targets.
Profiles are not verified participant IDs. No researcher message has a positive
stop flag. The [supplementary collection](2026-10-03-data-inspection.md) is separate
and does not substitute for the official logs.

Keep whole conversations together in evaluation, exclude future targets from
prompts/retrieval, and report goal overlap. The export supports prompting and
bounded comparisons; human-stop supervision, independent participant splits
and robust training claims need additional evidence.

## What we know and what remains open

- Saved request/output replay and organizer completion establish submission
  integrity. They do not establish user realism or competitive performance.
- Some replies remain overly polished, weakly differentiated by persona,
  overconfident about researcher knowledge, or too persistent.
- Conciseness, correct speaker and successful structured output are diagnostics,
  not the objective. Evaluate the reaction against the actual request, persona,
  history and latest assistant answer.
- Task 2's terminal parser defect was fixed and the completed run reconciled
  locally without reposting. See the [recovery record](task2-recovery-plan.md).

## Next action

Review organizer evaluation when available. No further run is needed to finish
this baseline; keep debug v5 paused and preserve private inputs/outputs,
receipts, frozen source and reconciliation evidence.

The [paper preparation map](../paper/README.md) records the writing plan and
missing official scores/venue/author information. All available run and detailed
development artifacts and rendered readers are preserved in a
[private GitHub evidence release](../artifacts.md), verified by a fresh download
and standalone restore. [Preservation instructions](../paper/preservation.md)
explain the immutable snapshots and evidence limits; local copies are caches.

For future research, use matched hard cases and successful controls, evaluate
knowledge attribution and voice separately, and include repeated draws and
context-aware blind review where practical. The backlog does not authorize a
new paid experiment, submission or participant-data publication.

## Evidence and history

- [Experiment ledger](experiment-ledger.md): study inventory and dated decisions.
- [Task 1 fidelity study](task1-fidelity-fix.md): selected narrow repair and limits.
- [October 3 source refresh](2026-10-03-research-refresh.md): primary-source review.
- [Implementation proposals](implementation-options.md): historical candidates.
- [Archive index](archive/README.md): old research, run and architecture checkpoints.

The [full research chronology](archive/2026-10-10-research-history.md) preserves
all dated progress reports. Current status here supersedes historical next actions.
