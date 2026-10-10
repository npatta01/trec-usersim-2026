# Data inspection and corrections to the proposed approaches

> Historical supplementary-only audit. The official export was supplied later;
> its current [coverage and limits](official-data-evidence.md) supersede the
> original access uncertainty below. These two collections remain separate.

Inspected October 3, 2026. **This audit covers the public supplementary collection, not the official TREC training logs.** Neither local checkout contained those logs; scoped searches of local data/download folders did not locate them. The official participant-page request returned HTTP 401. A path or authorized access configuration is still needed before claims about our official training data are possible.

## Evidence inspected

Downloaded the [organizer-linked supplementary archive](https://next.hessenbox.de/index.php/s/TanNCrw6mZm7b6Q) and read its README and transcription rules. Programmatically checked all 32 transcript files and both workbook sheets. Read all 151 bounded prompt spans, reviewed the ending speech across all sessions, and inspected malformed tag boundaries and representative contextual passages. This is not a full semantic annotation of every assistant reply or spoken thought.

The [executed audit notebook](notebooks/supplementary-data-audit.ipynb) contains the aggregate checks and source checksum. Raw files are stored outside the repository. No transcript quotations or raw participant records are committed here. The [official guidelines](https://trec.usersim.ai/guidelines) explicitly distinguish this collection from participant-sourced training logs and note that the assistants differ.

## What is actually available

| Check | Observed result | Consequence |
| --- | --- | --- |
| Released transcripts | 32 sessions, 16 participants, two sessions each | Only 16 independent people; treating every turn as an independent training example overstates coverage. |
| Workbook coverage | 32 participant rows and 64 session rows; only 16/32 match released transcripts | Filter the workbook to available transcripts before calculating dataset statistics. |
| Prompt volume | 151 opening prompt tags; all per-session counts match the workbook | This validates inventory counts, not conversational alignment. |
| Session size | 2–11 prompts, median 4 | Too little independent coverage to justify substantial task-specific training from this collection alone. This is an inference, not a universal minimum-size rule. |
| Assistant assignment | 8 included people used Perplexity; 8 used ChatGPT Scholar GPT | Assistant behavior is a potential confound when comparing user behavior. |
| Raw prompt-span length | 1–131 whitespace-delimited words, median 11; annotations retained | Real utterances range from a bare entity name to a detailed research request. A fixed verbosity target would erase that variation. |
| Naive extraction | A simple opening-to-closing prompt regex returns 147 matches instead of 151 | Some matches swallow other turns. A raw regex dump is not suitable training data. |
| Boundary defects | Unexpected prompt/output boundaries in four files | Review TN13_1, TN22_1, TN38_1, and TN39_2 before constructing conversations. |

The study's first session is unguided. In its second session, **the assistant is prompted to act as a coworker named Leslie**. These are not two human-personality conditions. The README says assistant preprompting is omitted from the transcripts; a replay constructed only from visible turns would miss that condition.

## Findings that change the suggestions

### Do not learn stopping from the final recorded turn

Endings have different causes. TN12_1 and TN33_2 contain spoken indications that the person has enough information. TN19_1 and TN38_2 end with interviewer time limits; TN38_1 is interrupted while the participant is considering another question. TN17_2 combines apparent satisfaction with time expiration. This is qualitative review, not a completed stop-label census.

**Correction:** withdraw the suggestion that we can straightforwardly fit a stopping model from session lengths or last turns in this collection. Mark externally truncated endings as censored, meaning the natural stopping time was not observed. A Task 2 stop decision is still necessary, but its training evidence is unresolved.

### Think-aloud speech is not an extra chat channel

The transcription rules distinguish typed PROMPT, assistant OUTPUT, spoken PARTICIPANT commentary, and INTERVIEWER speech. They also state that speech during generation is placed after the output. Thus file position does not precisely establish when every thought occurred.

**Correction:** do not concatenate spoken commentary with typed user messages, treat it as verbatim internal cognition, or feed hindsight into next-turn prediction. It may support carefully aligned manual interpretation. It does not yet justify automated state/action supervision.

### Replies depend on the actual previous answer

Prompt sequences include requests for direct links, corrections to wrongly interpreted concepts, rejection of sources already checked, brief answers to numbered questions, and requests for a single concrete item. For example, TN12_1 distinguishes disambiguation datasets from bibliographic databases; TN15_2 distinguishes collective from individual resilience; TN38_2 excludes previously checked sources.

**Correction:** retrieval must preserve the assistant context that elicited a reaction. Similar topics alone are not sufficient, but we have not demonstrated enough repeated situations here to justify a complex situation classifier. Start by assessing coverage manually and retain no-example and random-example controls.

### The collection is broader than a clean dataset-search benchmark

Some sequences move into literature discovery, implementation help, metrics, data compilation, and methods discussion. TN33 and TN37 include such requests. Several long initial prompts disclose a detailed research goal immediately, while others start minimally.

**Correction:** neither short, gradual goal disclosure nor a narrow menu of dataset-search actions should be imposed on every user. Determine how the official training goals and conversations differ before filtering this supplementary material or selecting examples.

### Metadata does not supply the full proposed user state

The workbook contains academic background, assistant assignment, usage frequency, and session-level experience/workload measures. It does not provide per-turn labels for known datasets, trust updates, unmet needs, or a frustration threshold. Session-level experience ratings cannot simply be used as attributes known before the session.

**Correction:** withdraw any implication that we already have labels to train the proposed personality/state controller. Inferring state from visible history remains an experimental hypothesis; copying post-session ratings into initial personas would introduce hindsight.

### Pairing prompts and outputs requires repair

TN19_2 contains a regenerated assistant response. TN38_1 contains two alternative outputs, and the transcription rules explain how alternatives are recorded. Other files contain late or missing closing tags that encompass speech and later turns.

**Correction:** one prompt does not always correspond to exactly one raw OUTPUT block. Preserve regeneration and selected-alternative provenance, separate speech, and validate sequences before building retrieval examples or training pairs. The notebook intentionally stops at profiling instead of silently repairing ambiguity.

## Revised position

The earlier diagrams remain illustrations of possible architectures, not a data-supported implementation choice. From this supplementary collection alone, the defensible immediate work is extraction review, evidence-linked behavioral examples, and a small held-out feasibility comparison. Substantial fine-tuning, learned state alignment, a fitted stopping policy, and fine-grained persona mixtures are not justified yet.

Direct prompting and an existing UserLM remain possible external-model comparisons, but this audit does not establish their suitability or relative performance. Before choosing among methods, inspect the official training logs: schema, independent participant/goal coverage, initial scenario fields, next-turn targets, and session termination semantics. The missing official data remains the next required input.
