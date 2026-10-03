# User simulation research refresh

Checked October 3, 2026. This focused refresh asks which approaches merit a controlled comparison for TREC UserSim. It updates the September 27 notes using primary sources and a targeted search for work around September 27 through October 3. It is not an exhaustive systematic review or a replication of published experiments.

**Conclusion:** the initial direct-prompt, retrieval, and UserLM comparison remains useful. New-to-us evidence strengthens the case for testing learned state models and weakens any assumption that memory or persona prompts provide reliable control automatically. None of the reviewed sources establishes a winning TREC solution.

“Verified” below means that the cited source or local code supports the statement. Published performance claims remain authors' results, not independently reproduced findings. Practical implications are our inferences.

## Official guidance rechecked

The [guidelines](https://trec.usersim.ai/guidelines) still display September 23, 2026 and list October 7 as the submission close, with up to four official runs per task. They describe human discrimination judgments and behavioral-distribution comparisons. The independently collected test set has 119 conversations across 21 goals, split into 62/10 for Task 1 and 57/11 for Task 2. Training and test user populations differ. The page provides no exact score aggregation weights.

The [research agenda](https://trec.usersim.ai/research-agenda) defers outcome-based metrics in year one. **Inference:** successful dataset discovery alone is insufficient evidence of realism. Goal progress can still affect realistic behavior, so it should not be dismissed as irrelevant.

## Core evidence and version corrections

| Source and version | Verified source claim | Implication and limitation |
| --- | --- | --- |
| [ConvApparel, EACL 2026](https://aclanthology.org/2026.eacl-long.244/) | Published abstract reports a realism gap across simulators and better behavior from data-driven approaches than prompted baselines, including reactions to unseen assistant behavior. | Relevant precedent for human examples and robustness testing; shopping differs from dataset search. Abstract and publication metadata rechecked; detailed metric counts remain historical notes, not newly reproduced results. |
| [Flipping the Dialogue v2](https://arxiv.org/abs/2510.06552v2), March 22, 2026; accepted at ICLR 2026 | Purpose-built user models improve behavioral alignment and robustness in the authors' evaluations. | Update the previous v1 reference. Compare an existing model against general assistant prompting; no demonstrated TREC transfer. Abstract/version history checked. |
| [Microsoft UserLM-8b model card](https://huggingface.co/microsoft/UserLM-8b) | Documents task-intent conditioning, opening and follow-up turns, and an end-of-conversation token. | A concrete implementation candidate. Integration must follow its template and map its stopping signal to the API; no download or execution performed. |
| [Distributional Gap v1](https://arxiv.org/abs/2605.07847v1), May 8, 2026 | Examines 24 simulators on coding/writing; complementary combinations can better approximate human behavior distributions. | Supports testing population variation. It does not imply arbitrary ensembles help or that per-turn switching preserves an individual. No newer version appears in the checked history. |
| [DIAL v4](https://arxiv.org/abs/2512.20773v4), May 6, 2026 | Alternates simulator and discriminator improvements; reports improved realism and failure-pattern alignment in mental-health dialogue. | Correct current title: “Direct Iterative Adversarial Learning for Realistic Multi-Turn Dialogue Simulation.” Previous notes cited v1 and an earlier title. Training a simulator this way is not the same as reranking candidates. Different domain; only current abstract/history rechecked. |

UserLM v2 and DIAL v4 predate the September notes: these are corrections to the versions we used, not releases from the last week. No freshly released successor to the core shortlist was established by this search.

The [Google publication page](https://research.google/pubs/convapparel-a-benchmark-dataset-and-validation-framework-for-user-simulators-in-conversational-recommenders-2/) for ConvApparel describes an RL approach, whereas the ACL abstract and our earlier reading of the published comparison differ. Keep the ACL paper as the reference for that comparison; do not silently combine claims across those descriptions. Resolving the exact relationship would require a version-level full-text comparison.

## Relevant work missing from our earlier shortlist

### HumanLM and learned user states

[HumanLM, ICML 2026 proceedings](https://proceedings.mlr.press/v306/wu26k.html) and the [author project](https://humanlm.stanford.edu/) describe generating intermediate natural-language states, aligning them with observed responses through reinforcement learning, then generating user replies. The proceedings abstract reports improvements on its benchmark and a human study.

**Inference:** state modeling deserves a serious experiment. This evidence supports a learned alignment procedure; it does not validate our earlier hand-written state/action pipeline. The proceedings and [arXiv abstract](https://arxiv.org/abs/2603.03303) report different human-study sizes, so this note deliberately avoids pooling their quantitative claims. Scope here: proceedings abstract and project description, not a full methods audit. This is previously missed work, not a newly published September result.

### Memory in conversational search

[Do Simulated Users Need to Remember?](https://downloads.webis.de/publications/papers/mirzakhmedova_2026a.pdf), SIGIR 2026, studies memory variants in conversational-search evaluation. Its introduction reports that short-term memory does not consistently improve robustness and can introduce ranking variability; its discussion finds long-term-memory variants closer to human scores in the studied settings.

**Inference:** compare memory variants rather than assuming a state summary improves simulation. The paper studies system-evaluation fidelity, which differs from TREC's human-likeness objective. Other user-model components were held fixed, limiting generalization. Abstract, introduction, and conclusion/discussion passages were inspected; no results reproduced. This paper also predates our September notes.

## Newly published or same-week leads

### Persona control can change unintended attributes

[Persona Following Is Not Selective Control v1](https://arxiv.org/abs/2609.35036v1) was submitted September 28, after our September 27 review. The authors report that changing one prompted trait also shifts unspecified preferences across the tested models; declaring a preference neutral does not reliably eliminate the effect.

**Inference for TREC:** changing patience should trigger checks for unintended shifts in expertise, goal requirements, and known datasets. Treat this as a motivation for controlled probes, not proof of the same failure in our simulator. This is a preprint. We inspected the abstract and HTML outline; full experimental and causal assumptions still need review before adopting a mitigation or quantitative target.

### Evaluation needs independent human checks

[Designing Reliable LLM-as-a-Judge Measurement Systems for Multi-Turn Business Agents v1](https://arxiv.org/abs/2609.33955v1), submitted September 27, describes versioned evaluation evidence, simulator stability checks, and independent human audits. Its abstract explicitly limits the production studies to observational evidence.

**Inference:** keep our judge versions and human comparisons traceable. This is adjacent business-agent evaluation work, not a new simulator shown to improve TREC realism. Abstract and submission history checked; retain as an evaluation lead rather than a main modeling recommendation.

## Search scope and unresolved questions

Searches included user simulation and conversational search with September 2026 terms, exact titles of the core papers, and a September 27–October 3 date-filtered query. Search snippets and aggregators were used to discover leads; retained claims were checked against organizer pages, publisher proceedings, author-hosted papers, arXiv records, or the official model card. IIRSim Studio was screened as tooling, not promoted as evidence for a better generation method.

This refresh did not rerun the supplementary-data inventory, access protected training logs, inspect every earlier paper's latest version, or read every full text. In particular, USP, TraitBasis, RealUserSim, SimulatorArena, and DuetSim remain historical literature leads in the archived reassessment, not newly audited evidence. No lack-of-results claim should be read as proof that no other recent work exists.

The main unanswered question remains empirical: which method reproduces appropriate reactions and human variation on held-out dataset-search conversations? The [canonical research status](README.md) records the proposed comparison, controls, and next action.
