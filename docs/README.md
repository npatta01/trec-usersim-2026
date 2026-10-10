# Documentation map

Start with the [project handoff](project-handoff.md): both official baselines are
complete, and no further run is needed. This map distinguishes current guides
from historical research and recovery checkpoints.

| Need | Read |
|---|---|
| Current status, selected behavior, next action | [Project handoff](project-handoff.md), then [research index](research/README.md) |
| Runs, remaining allowances, costs, private receipt locations | [Submission ledger](submission-ledger.md) |
| How the system works, including diagrams and module boundaries | [Task 2 architecture](task2_architecture.md) |
| Task 1 setup, preview, editor selection and safeguards | [Task 1 runner](task1_runner.md) |
| Task 2 setup, execution gates and recovery | [Task 2 runner](task2_debug_runner.md), then [recovery plan](research/task2-recovery-plan.md) |
| Organizer task and endpoint contract | [Task 1 workflow](task1_workflow.md), [Task 2 workflow](task2_workflow.md) |
| What the official training export actually supports | [Official-data evidence](research/official-data-evidence.md) |
| Methods tested, rejected variants, uncertainties | [Method decisions](research/method-decisions.md), then [experiment ledger](research/experiment-ledger.md) |
| Task 1 narrow fidelity repair and its limits | [Fidelity comparison](research/task1-fidelity-fix.md) |
| Source layout and historical experiment entry points | [Code structure](research/code-structure-plan.md), [experiments](../experiments/README.md) |
| Literature and earlier proposals | [October 3 source refresh](research/2026-10-03-research-refresh.md), [implementation proposals](research/implementation-options.md) |
| Supplementary collection, distinct from official training | [October 3 supplementary inspection](research/2026-10-03-data-inspection.md) |

The research index is the canonical status; the submission ledger is the
canonical run inventory; the experiment ledger preserves dated evidence.
Historical handoffs describe what was known on their date, not current work to
execute. The diagrams explain the implemented baseline; candidate diagrams in
the proposal document are explicitly historical.

## Maintaining the record

When behavior changes, update the relevant runner guide and architecture before
handoff. Record the experiment's inputs, controls, result, limitations and decision
in the experiment ledger; revise the method summary when the decision changes.
When a run starts or its state changes, reconcile its saved receipts and update
the submission ledger and research index. Distinguish normal stops from
administrative closures and reservations from money spent.

Verification commands and known legacy-test failures are in the
[execution guide](task2_debug_runner.md#setup-and-offline-verification). Use CLI
`--help` and Task 1 preview for offline inspection; Task 2 execution commands have
no preview mode. Source checks and synthetic tests do not establish user realism.

Public documentation contains source, synthetic examples and aggregate results.
Training transcripts, exact model requests/outputs, API receipts, personal data
and keys stay in the private locations listed in the submission ledger. Those
files are needed to reproduce historical experiments; this public checkout alone
does not contain them. Never copy credentials into commands, docs or review packets.

## Documentation verification — October 10

The public documentation was reconciled against current source, the official
export's aggregate checksum/schema, private submission state and saved final
audit/GET records. Old access uncertainty and launch checkpoints are marked
historical; their original evidence is preserved rather than silently replaced.

Repository-relative Markdown paths/anchors and whitespace were checked. All
139 runtime tests passed in the existing development environment. Both Task 2
CLIs and Task 1 `--help` were exercised; Task 1 preview created no run directory,
and Task 2 refused execution without `--run`. The clean checkout does not include
private artifacts; no new model or organizer calls were made for this update.
The dependency installation recipe was reviewed, not reinstalled from scratch.
