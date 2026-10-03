> Historical note from September 27, 2026. Preserved for provenance; recommendations and source versions may be superseded. Start with the [current research summary](../README.md) and [October 3 refresh](../2026-10-03-research-refresh.md). Advisor opinions are not experimental results.

# TREC UserSim: Astra and Opus reassessment

Date: 2026-09-27. Supersedes the confidence and prioritization in the earlier focused review. Status: advice and expanded literature checking only; no implementation or experimental results. This is not an exhaustive systematic review.

## What changed

The initial list mixed complete modeling approaches with engineering requirements and possible data sources. Neither advisor endorses retrieval plus a rigid state/action pipeline as an established best approach. Stopping belongs in every credible Task 2 baseline; think-aloud is a possible supervision source, not a validated winning method. Small model size is not the hypothesis: learning user-turn behavior is.

## Independent advisor conclusions

### Astra — GPT-6 Astra, xhigh

Successful native-agent review after the CLI attempt failed. Read the same frozen public packet as Opus, without independent browsing or other files. Recommendations: establish a correctly wired capable baseline; compare retrieval with conditional supervised imitation before committing; model persistent between-user variation and infer style from Task 1 prefixes; use conditional realism diagnostics; test minimal state separately from a forced action bottleneck. Retrieval is supported only by adjacent-domain evidence. A discrete action can suppress mixed-intent turns. Matching aggregate statistics does not guarantee coherent individuals or appropriate reactions. Candidate selection may collapse diversity. Full literature leads were clearly marked recalled, not verified.

Astra's falsification tests: random versus semantic versus situation retrieval at comparable context budget; same training pool for SFT versus retrieval; direct generation versus minimal state versus state/action pipeline; persistent session style versus turn-wise resampling; reactions to altered assistant replies compared against observed human behavior where available.

### Opus — Claude Opus alias, max

Successful first-party subscription CLI review of the frozen public packet, tools disabled. Full response is in [the Opus artifact](trec-usersim-opus-advice-2026-09-27.md). Prioritizes human examples plus calibration of observable behavior; proposes generating candidates and selecting against empirical behavior targets and an independent realism diagnostic. Explicit state machinery is not supported as the main competitive bet. Identified UserLM as missing literature and cautioned against uninspected think-aloud data and premature fine-tuning.

Important disagreement: Opus gives candidate selection high near-term priority; Astra is more cautious because selection can suppress diversity or exploit detector artifacts. Astra treats conditional SFT as a serious peer of retrieval once data sufficiency is known. Neither establishes that any method wins TREC.

## Source verification after advice

| Primary source | Verified contribution | Practical implication / limit |
|---|---|---|
| [Flipping the Dialogue, Microsoft Research](https://www.microsoft.com/en-us/research/publication/flipping-the-dialogue-training-and-evaluating-user-language-models/) and [author paper](https://arxiv.org/html/2510.06552v1) | Purpose-built user language models, trained to generate user turns, report improved behavioral alignment and simulation robustness. | Test the released UserLM family against an assistant model before training from scratch; TREC transfer and persona adherence remain unproven. |
| [Measuring and Mitigating the Distributional Gap, 2026 preprint](https://arxiv.org/html/2605.07847v1), section 7.2 | Samples one simulator per conversation from pairs; some complementary pairs improve distributional alignment, other pairs worsen it. | Population-level model mixtures deserve comparison. Learned routing is future work in that source, not an established result. Coding/writing domains and different assistants limit transfer. |
| [DIAL / Adversarial Training for Failure-Sensitive User Simulation, 2025 preprint](https://arxiv.org/html/2512.20773v1) | Alternates detector training with DPO refinement of the simulator; reports improved realism and failure prediction. | Concrete training alternative beyond prompting. Mental-health domain and unavailable sensitive training data constrain replication and transfer. Not proof that optimizing one detector improves TREC human judgments. |
| [TraitBasis, ACL 2026](https://aclanthology.org/2026.acl-long.1743.pdf) | Uses activation directions to control four user traits; reports advantages over comparison methods in trait realism/stability. | A different control mechanism to investigate, not a demonstrated match to a researcher population. Requires access to model activations; fixed trait coverage. |
| [RealUserSim, 2026 preprint](https://arxiv.org/html/2605.20204v1) | Grounds behavioral profiles in real conversations; reports improved judge-assessed fidelity. | Supports evidence-grounded styles, but its same-family judge and profile construction must be audited before importing reported gains. Not a human Turing-test win. |
| [SimulatorArena, EMNLP 2025](https://aclanthology.org/2025.emnlp-main.1786/) | 909 human–AI conversations in tutoring/document creation; evaluates profile-conditioned simulation and agreement with human assistant ratings. | Important omitted validation literature; outcome-rating agreement differs from TREC's stated first-year realism focus. |
| [DuetSim, LREC-COLING 2024](https://aclanthology.org/2024.lrec-main.481/) | Separate generator and verifier improve reported response quality/correctness on MultiWOZ. | Prior art for generator/verifier approaches; correctness is not identical to human behavioral fidelity. |
| [In-context user simulator implementation, 2023](https://github.com/telepathylabsai/prompt-based-user-simulator) | Selects relevant dialogues as prompt examples. | Retrieval is established prior art; its particular objective or transfer result must justify novelty. |
| [ConvApparel, EACL 2026](https://aclanthology.org/2026.eacl-long.244.pdf) | Retrieved examples and SFT improve many behavioral statistics but all tested methods remain detectably synthetic. | Supports comparative baselines and independent diagnostics, not a guaranteed winning architecture. |

The arXiv connector returned not-found for several newer IDs; primary arXiv HTML was available via web and used instead. Publication pages, abstracts, or selected relevant sections were inspected as appropriate; this is not a claim that all full texts, supplements, and citations were exhaustively reviewed.

## Revised experimental shortlist (our synthesis, not model consensus)

1. Correct capable direct-prompt baseline, with Task 2 stopping and Task 1 prefix handling.
2. Human examples: random, semantic, and situation retrieval.
3. Purpose-built user model, then same-task adaptation only if data supports it.
4. Persistent, persona-compatible behavioral variation; compare a calibrated mixture of generators against one generator.
5. Candidate selection or preference learning using realism evidence, with separate evaluation and diversity checks.
6. Minimal state tracker as an ablation, not a presumed central architecture. Compare state-only against a forced action stage.

Think-aloud can label hypotheses or validate inferred state; do not make it a central dependency before inspecting its alignment and sampling differences. Trait steering is a secondary research branch, not a deadline recommendation yet.

## Corrections to advisor overclaims

The Opus claim that beating the public baseline is near-certain is not established; there are no runs. Semantic role serialization may cause confusion but is not a proven failure by itself. Duplicate last-agent text and missing scenario reassignment are visible code concerns at the frozen source revision; their measured effects are unknown. Goal progress can still inform realistic behavior even though explicit outcome metrics are deferred. Do not adopt arbitrary data-volume thresholds or temperature values as empirical facts.

## First decision gate

Inspect authorized human logs and construct held-out conversation/goal splits. Compare direct prompting, retrieved examples, and a purpose-built user model, then test the best against calibration or minimal-state additions. Judge conditional appropriateness, within-session consistency, between-user diversity, and independent human realism. No official submissions, paid training, or architecture commitment are authorized by this advice request.

## Advisor provenance and data handling

Requested/effective selection: Astra and Opus only. Shared focus: critically reassess competitive directions, reject unsupported recommendations, identify missing approaches and decisive experiments. Packet: 37,671 bytes, verified public organizer source at e04d2ae6c0c91071dc869d17ba9f337fd5ec8c3a plus published-literature summaries. A preliminary private-classified packet was blocked by automatic approval review. After GitHub verified the exact public upstream revision and private project references were removed, the public-only packet was approved.

Astra CLI: GPT-6 Astra xhigh; ChatGPT subscription preflight succeeded; runtime failed without review. Same-model native retry succeeded. Opus: `opus` alias at max effort, authenticated first-party claude.ai subscription, successful. Exact underlying Opus version was not reported by the runner. No other models were substituted. Standard lane settings were used with a custom two-model selection. Runner audit declares provider data use `none` and training-use permission false; this records invocation policy, not a universal assertion about account retention settings. No OpenCode lanes ran, so their cleanup is not applicable. Raw provider-result/preflight JSON files are removed after synthesis; only advice artifacts are retained. Reviews were independent critiques of one packet, not independent exhaustive searches.
