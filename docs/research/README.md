# TREC UserSim research notes

Updated October 3, 2026. This is the canonical research status and proposed experiment sequence for this repository. Our objective is to simulate how human researchers look for datasets, including their reactions, variation, and decisions to stop. No approach has been validated on this task in our work so far.

## Start here

- [October 3 evidence refresh](2026-10-03-research-refresh.md): current sources, version corrections, newly found papers, and limitations.
- [September 27 advisor reassessment](archive/trec-usersim-advisor-reassessment-2026-09-27.md): Astra and Opus challenged the original ranking; no new advisor consultation was performed for this refresh.
- [Original research directions](archive/trec-usersim-winning-directions-2026-09-27.md): historical proposal, superseded where it conflicts with this summary.
- [Original Opus advice](archive/trec-usersim-opus-advice-2026-09-27.md): preserved opinion, including claims subsequently qualified in the reassessment.

The archived notes were imported from the previous research workspace. They preserve the reasoning history, not an approved implementation plan. The current summary and dated refresh take precedence. The research PR changes documentation only.

## What we are predicting

Task 1 gives us a persona, goal, and conversation prefix; we produce the next human message. Task 2 asks us to keep playing the person across a conversation with the organizers' assistant. See the [official task definition](https://trec.usersim.ai/guidelines).

Illustrative example, not a dataset quotation:

> Researcher needs naturally occurring dialogue data. The assistant recommends scripted role-play data. A plausible next message is: “I need real conversations, not assigned role-play. Any alternatives?”

There is no unique correct wording. We need to evaluate whether the reaction fits the context, whether the same person behaves consistently, and whether the simulated population varies plausibly.

## Approaches worth comparing

The order below is a proposed experimental sequence, not a performance ranking. Evidence is detailed in the [refresh](2026-10-03-research-refresh.md).

| Approach | Plain-language mechanism | Requirements and main uncertainty |
| --- | --- | --- |
| Direct prompting | Give a capable general-purpose LLM the scenario and history and ask for the next user message. | Fast reference system; may produce implausibly polished, cooperative users. |
| Human-example retrieval | Include real conversation excerpts showing comparable situations before generating. | Clean training-only examples; distinguish topic similarity from similar reactions. Small data may give poor coverage. |
| Existing UserLM | Use a model trained to write human turns instead of assistant answers. | Verify its input template, stopping token, runtime and license. Transfer to dataset search and persona control are unknown. |
| Task-specific supervised fine-tuning | Train on a conversation prefix paired with the observed next human turn. | Enough independent conversations and goals for development and evaluation. Turn count alone is not data sufficiency. |
| Learned state alignment | Learn intermediate descriptions of user beliefs or reactions, then generate responses. | HumanLM supplies relevant evidence, but its training procedure is more involved than adding a memory prompt. |

Optional additions should be tested separately: a compact record of unresolved needs and rejected suggestions; persistent session style; a mixture of generators selected per session; or generating several replies and selecting among them. Each can also hurt. State descriptions are inferred hypotheses, not observed human thoughts. A rigid single action label can suppress messages with multiple intentions.

Stopping belongs in every Task 2 comparison. An interviewer ending a recorded session is not evidence that the participant chose to stop.

## Current evidence and data status

- **Verified locally on October 3:** repository base `e04d2ae6c0c91071dc869d17ba9f337fd5ec8c3a`; the [complete-run example](../../simulator/examples/complete_run.py) selects `RandomStrategy`; the [simulator loop](../../simulator/src/user_simulator.py) passes `is_final=False`. These are inspected source facts, not runtime test results.
- **Historical observation, not remeasured here:** the September chat reported 32 supplementary sessions from 16 people and 151 user messages in the spreadsheet; only examples from three sessions were read. That was a partial data inspection, not a complete quality audit.
- **Unknown:** official training-log availability locally, independent participant/goal coverage, usable stopping labels, compute budget, and measured simulator performance. The previous unauthenticated download returned 401; that does not establish that authorized local access is unavailable.
- The supplementary data and official logs are separate collections. No participant transcripts, credentials, raw chat histories, or private model outputs are included in these notes.

## Proposed experiment sequence

1. Locate authorized official logs and inventory conversations, goals, participants, assistant variants, missing fields, and how sessions ended. Record provenance and permissible use.
2. Build held-out splits by whole conversation, and by participant/goal where possible. Keep all validation targets and future turns out of prompts, retrieval, training, and inferred profiles. Document any overlap that the data cannot avoid.
3. Compare direct prompting, random examples, relevant examples, and an existing UserLM on identical prefixes. Treat random examples as a control for whether retrieval adds value beyond extra context.
4. Inspect reactions to vague, repeated, irrelevant, and constraint-violating assistant replies. Controlled edits are robustness probes; they are not human ground truth unless corresponding human responses exist.
5. Add one component at a time to a promising method. An ablation is this comparison with a component removed. For memory, compare full-history-only against a derived state summary while recording context budgets.
6. Evaluate Task 2 separately, including session resets, stopping, diversity, and response latency. Offline next-turn gains do not establish whole-session realism.

Use message-length and session-length distributions, clarification behavior, repetition, within-session consistency, and blind human comparisons. Exact next-message matching is insufficient. Report uncertainty at conversation/goal level; compare human groups to estimate natural variation. Automated human-likeness detectors should remain independent of any selector optimized against them.

For persona tests, change one attribute while keeping the goal and history fixed, then inspect unintended changes to knowledge and preferences. This is a proposed diagnostic motivated by the new persona-control paper, not an official TREC metric.

## Decisions and next action

**Decision:** retain direct prompting, retrieval, and UserLM as competing initial approaches. Give learned state alignment a place in the literature and later experiments; do not infer that a hand-written state/action pipeline is superior. Defer substantial new training until the data inventory and inexpensive comparisons justify it.

**Next action:** locate and inspect official training logs, then define reproducible splits and the smallest offline comparison. These notes do not authorize paid runs, official submissions, or uploading participant data to external providers.

## Verification of this documentation change

Primary sources were rechecked on October 3; the scope and reading depth are recorded in the refresh. Local Markdown links, whitespace, documentation-only scope, and accidental credential/host-path inclusion were checked before the research commit. No simulator tests or experiments were run for this documentation change.
