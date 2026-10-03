# Working on TREC UserSim

## Project context

Before changing simulator behavior or proposing experiments, read:

Start with the [actual data inspection and corrections](docs/research/2026-10-03-data-inspection.md). Do not treat the public supplementary collection as the official training logs or assume the proposed architectures have been validated against either.

1. [Research status and next experiments](docs/research/README.md) — canonical objective, candidate approaches, decisions, data gaps, and next action.
2. [Possible implementations](docs/research/implementation-options.md) — diagrams of the shared runtime, alternative generators, training, and evaluation. These are proposals, not implemented capabilities.
3. [October 3 research refresh](docs/research/2026-10-03-research-refresh.md) — primary sources, corrected versions, reading depth, and limitations.
4. The relevant API workflow: [Task 1](docs/task1_workflow.md) or [Task 2](docs/task2_workflow.md).

## Research continuity

- Maintain the research index as the canonical status when decisions or evidence change. Keep implementation diagrams consistent with it.
- Separate verified source facts, published authors' claims, our hypotheses, and measured results from our own experiments.
- Historical [advisor reassessment](docs/research/archive/trec-usersim-advisor-reassessment-2026-09-27.md), [initial directions](docs/research/archive/trec-usersim-winning-directions-2026-09-27.md), and [Opus advice](docs/research/archive/trec-usersim-opus-advice-2026-09-27.md) preserve provenance. Current notes take precedence over superseded rankings and assumptions.
- Keep participant transcripts, credentials, and private model outputs out of documentation and commits. Preserve conversation/participant/goal separation in evaluation and prevent future-turn leakage.
- The research notes and diagrams do not authorize paid experiments, official submissions, public deployment, or sharing participant data with external providers.
