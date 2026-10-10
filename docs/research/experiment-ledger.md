# Experiment ledger

Updated October 10, 2026. This records simulator studies and decisions.
Organizer starts and allowances belong in the [submission ledger](../submission-ledger.md).
Model-only comparisons do not consume organizer-run allowances.

## Study inventory

| Study group | Evidence and decision |
|---|---|
| Local models, roles, reminder and transcript format | [Method decisions](method-decisions.md#what-the-comparisons-establish); correct speaker was insufficient for realism |
| Luna prefixes, prompt structure, turn mode, critic and few-shot | [Method decisions](method-decisions.md#what-the-comparisons-establish); no recurring broader default improvement |
| Default-on post-edit and harder repair probes | [Method decisions](method-decisions.md#what-the-comparisons-establish); modest real-case preferences, stronger synthetic-artifact repair |
| Longer histories, summaries and knowledge/voice cues | [Method decisions](method-decisions.md#what-the-comparisons-establish); limited/mixed preferences, no compaction adoption |
| Planner/renderer, progress assessment and stronger hosted model | [Method decisions](method-decisions.md#what-the-comparisons-establish); no demonstrated recurring voice gain |
| Task 1 narrow fidelity editing | [Full comparison](task1-fidelity-fix.md); selected explicitly for official Task 1 |
| Protocol, timeout and completion integration | [Recovery guide](task2-recovery-plan.md); synthetic tests plus private request/receipt replay |

These are mostly reused training-development cases, small controlled screens or
synthetic probes. They do not form a held-out human-realism benchmark. Detailed
private-note provenance is listed in the method summary; private outputs stay
outside git.

## October 10 — completed baseline and documentation consolidation

Official Task 2 reached recognized HTTP428 completion: 57 processed, zero
remaining. The final audit separates 49 normal stops from eight administrative
closures and verifies 258 generated pairs / 516 model calls. The longer
run-specific completion text initially failed parsing; a reviewed local
reconciliation advanced the accepted final message once without a POST or model
call. Both official tasks are now complete.

The generic completion classifier and recovery error visibility were corrected;
139 runtime tests / 92 subtests passed. Private audit controls verify source,
receipts, recovery evidence and counters. This is completion/integrity evidence,
not an official score or quality rate.

Documentation now separates current guides from dated history, with reproducible
images of task scope, the draft/editor pipeline and recovery. The full
[experiment chronology](archive/2026-10-10-experiment-history.md) is preserved.
No model or organizer call was made for the documentation cleanup.

## Open hypotheses

Stable human voice evidence versus generated voice, controlled retrieval,
summary retention of old objections, and stronger-model-plus-editor comparisons
remain candidates. Each needs matched controls, leakage checks and contextual
review before adoption. See the [method backlog](method-decisions.md#what-is-not-supported-and-what-remains-open).

A shorter future timeout grace is an operational proposal, not a simulator-quality
improvement. The completed official run retained 1,800 seconds. No additional
paid or organizer run is authorized by this ledger.
