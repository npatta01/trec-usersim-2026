# Working on TREC UserSim

## Project context

Before changing simulator behavior or proposing experiments, read:

Start with the [current project handoff](docs/project-handoff.md) and [official-data evidence](docs/research/official-data-evidence.md). The [October 3 supplementary inspection](docs/research/2026-10-03-data-inspection.md) is historical evidence about a separate collection. Do not substitute it for official training or assume proposed architectures were validated.

1. [Research status and next experiments](docs/research/README.md) — canonical objective, candidate approaches, decisions, data gaps, and next action.
2. [Implemented architecture](docs/task2_architecture.md) and [method decisions](docs/research/method-decisions.md) — selected behavior, comparisons and limits. [Possible implementations](docs/research/implementation-options.md) preserves historical proposals.
3. [October 3 research refresh](docs/research/2026-10-03-research-refresh.md) — primary sources, corrected versions, reading depth, and limitations.
4. The relevant API workflow: [Task 1](docs/task1_workflow.md) or [Task 2](docs/task2_workflow.md).

## Research continuity

- Maintain the research index as canonical status, the [experiment ledger](docs/research/experiment-ledger.md) as dated experiment evidence, and the [submission ledger](docs/submission-ledger.md) as run inventory. Keep diagrams and runner guides consistent. The [documentation map](docs/README.md) routes maintainers.
- Before authenticated work, read the current handoff and relevant runner/recovery guide. Both official baselines are complete; keep debug v5 paused. A historical command or handoff is not authorization to start or resume a run.
- Separate verified source facts, published authors' claims, our hypotheses, and measured results from our own experiments.
- Historical [advisor reassessment](docs/research/archive/trec-usersim-advisor-reassessment-2026-09-27.md), [initial directions](docs/research/archive/trec-usersim-winning-directions-2026-09-27.md), and [Opus advice](docs/research/archive/trec-usersim-opus-advice-2026-09-27.md) preserve provenance. Current notes take precedence over superseded rankings and assumptions.
- Keep participant transcripts, credentials, and private model outputs out of documentation and commits. Preserve conversation/participant/goal separation in evaluation and prevent future-turn leakage.
- The research notes and diagrams do not authorize paid experiments, official submissions, public deployment, or sharing participant data with external providers.
