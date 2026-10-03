> Historical note from September 27, 2026. Preserved for provenance; recommendations and source versions may be superseded. Start with the [current research summary](../README.md) and [October 3 refresh](../2026-10-03-research-refresh.md). Advisor opinions are not experimental results.

> Reassessment: the initial ranking below was based on a focused, non-exhaustive review. See [Astra/Opus reassessment](trec-usersim-advisor-reassessment-2026-09-27.md) for corrected confidence, competing approaches, and expanded sources.

# TREC UserSim: competitive research directions

Date: 2026-09-27. Status: evidence review and proposed experiments, not a tested system or approved implementation plan. Scope: both 2026 tasks; prioritize improvements feasible before October 7. No training runs, API submissions, or private-data access performed.

## Recommendation (inference)

Build a simulator grounded in human examples, with a small explicit state describing unmet needs, acquired knowledge, trust, frustration, and willingness to continue. Choose a dialogue action before generating its wording. Compare this against a strong direct-prompt baseline; keep the simpler system if the added state does not improve held-out results.

## Evidence matrix

| Source | Verified finding | Implication / limitation |
|---|---|---|
| [Official guidelines](https://trec.usersim.ai/guidelines), September 23, 2026 | Human judgments and behavioral distributions are evaluated; four runs per task; October 7 submission deadline. | No precise aggregation weights established by the reviewed page. |
| [Research agenda](https://trec.usersim.ai/research-agenda), retrieved September 27 | Outcome metrics are deferred for year one. | Optimize behavioral fidelity, not just successful dataset discovery. |
| [ConvApparel, EACL 2026](https://aclanthology.org/2026.eacl-long.244.pdf), sections 5–6 and appendix B.2 | Retrieval uses three similar human conversations. ICL improves over static prompting on 9/11 behavioral metrics for a good recommender and 10/11 for a bad one. All methods remain detectably synthetic. | Strong precedent for example retrieval and tests of reactions to poor responses, but shopping is not dataset search. Use the published paper: the Google publication-page abstract mentions RL that is not part of the published three-baseline comparison. |
| [USP, ACL 2025](https://aclanthology.org/2025.acl-long.1025.pdf) | Combines inferred profiles, conditional fine-tuning, profile sampling, and cycle-consistency RL. Reports improved authenticity/diversity; acknowledges limited cross-dataset validation. | Supports history-based behavioral inference, not proof that its full training recipe transfers here. |
| [Parameterized behavior, SIGIR-AP 2024](https://www.sigir-ap.org/sigir-ap-2024//proceedings/) | Uses in-context behavioral traits in conversational user simulation. | Persona/trait prompting alone is prior work; novelty must be more specific. |
| [Official starter](https://github.com/npatta01/trec-usersim-2026/tree/e04d2ae6c0c91071dc869d17ba9f337fd5ec8c3a) | Previously inspected snapshot: random default, prompt-based LLM strategy, complete-run loop sends is_final=False. | Repair and validate the API/history/scenario path before attributing results to modeling. |

## Ranked hypotheses

1. Human-example retrieval: retrieve training-only examples of similar interaction situations, starting with k=3 and comparing against random examples. Prevent topic-specific facts from leaking into the new goal. Best near-term risk/reward.
2. State then action then utterance: update unresolved requirements, what the user plausibly knows, perceived answer usefulness, and repeated failures; select ask/clarify/correct/compare/accept/abandon; render in a consistent style. Best differentiating hypothesis.
3. Explicit stopping: estimate probability of stopping from satisfaction, frustration, recent progress, and session length, conditioned on supplied traits. Fit to real sessions rather than arbitrary fixed patience.
4. Think-aloud supervision: use the organizers' supplemental verbal reports to define or supervise state/action labels. Treat verbal reports as noisy observations, not complete internal cognition. Retain only if an ablation helps.
5. Small-model fine-tuning: train on human next-user turns if there are enough distinct sessions and held-out gains. Defer RL until simpler baselines have been measured.

## Task-specific behavior

Task 1: infer state from each supplied prefix independently; avoid contamination from earlier generated predictions. Extract additional speaking-style cues only from the available prefix, never the target or future turns.

Task 2: retain state across turns within a session, reset for each scenario, and implement a stop decision. Test with useful, repetitive, irrelevant, and contradictory assistant replies. These are controlled robustness probes, not ground-truth human responses unless matching observations exist.

## Proposed evaluation

Split by goal and participant where identifiers/data volume permit; never randomly split turns from the same conversation. Hold out agents if feasible. Keep training examples out of validation retrieval. Bootstrap uncertainty at conversation or goal level, not at individual-turn level.

Measure user-length distributions, question and clarification rates, dialogue-action transitions, repeated requests, persona consistency, and stopping/session-length distributions. Use blind human comparisons plus at least one independent automated diagnostic; a single LLM judge is insufficient. Compare human groups against each other to estimate sampling variation. Avoid forcing every persona to match a global average.

Four candidate run slots per task: direct prompt; human-example retrieval; retrieval plus behavioral state/action selection; best validated variant with stopping calibration or think-aloud supervision. The slots are a proposed experimental portfolio, not a reason to submit a weaker system.

## Next action and unknowns

First obtain authorized training logs and inspect session count, participant/goal coverage, annotations, and supplemental think-aloud format locally. Data sufficiency, compute budget, API access, and exact score aggregation remain unknown. Then run offline next-turn comparisons before paid training or official submissions. Do not upload participant data to model providers without checking authorization.
