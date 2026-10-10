# Official training export: evidence and limits

Aggregate structural audit, rechecked October 10, 2026. This describes the
user-supplied `final_dataset_curation_v1.jsonl`, not the supplementary collection.
The user supplied it as the official training export after the initial access
check. Its identity is pinned locally; an independent organizer download,
curation history and redistribution terms have not been verified.

The export remains private. Public documentation contains counts and schema,
not participant utterances or profiles. The local-git exception for this file
does not authorize pushing or publishing it.

| Property | Observed value |
|---|---|
| Size | 1,094,237 bytes |
| SHA256 | `288f0f4ec7404bca0807567ba15a42ca50bae8c3d01b5416c60b6de7d5eac53f` |
| Conversation records | 64 |
| Distinct complete goal objects | 10; counts 5, 5, 6, 6, 6, 6, 7, 7, 7, 9 |
| Distinct complete persona profiles | 12; not 12 independently verified people |
| Messages | 532: 266 researcher (`User`), 266 search assistant (`Agent`) |
| Researcher turns per conversation | Minimum 1, median 4, maximum 9 |
| Next-message development targets | 266: 64 openings and 202 follow-ups |
| Positive `is_final` flags | 56 assistant messages; zero researcher messages |

Names are always generic `User`/`Agent`; there is no stable participant ID or
assistant-model identifier. Persona duplicates cannot prove participant identity.
Ten goal objects are limited coverage, not the complete space of possible
evaluation goals. Turn targets from one conversation are correlated.

## Schema

| Level | Fields and interpretation |
|---|---|
| Record | `record_id`, `scenario`, `conversation_id`, `chat_messages` |
| Scenario | `persona`, `goal`, `persona_goal_interaction` |
| Persona general information | Gender, age, highest education, English proficiency |
| Persona AI experience | Trust in AI, perceived human-likeness |
| Persona traits | Frustration threshold, interaction style |
| Goal | `type`, `context`, `topic`, `discipline`, `stage`, `know_datasets`, `dataset_examples`, `description` |
| Persona/goal interaction | Domain familiarity and known-dataset list |
| Message | Timestamp, conversation ID, participant name, text, sources, annotations, boolean `is_final` |

All 532 source lists are empty, even where text contains links. Researcher
annotations are empty. Assistant annotations on 262 messages contain
helpfulness, dataset quality and feedback; four assistant annotation dictionaries
are empty. The helpfulness values are 199 true and 63 false. Annotation author
and collection timing are not established, so these are not validated real-time
user-state labels or safe next-turn input features.

## What the model receives

The raw export/API input and the actual prompt are different representations.
The current builders in [prompts.py](../../usersim/prompts.py) use the following
projection. Exact original inputs and requests are retained privately.

| Supplied material | Prompt behavior |
|---|---|
| Persona | All fields represented by the starter's general-info, AI-experience and traits classes; missing groups default to empty |
| Goal | Context, topic and discipline; ancillary goal metadata is not rendered |
| Persona/goal interaction | Domain familiarity and known datasets; missing values receive builder defaults |
| Available conversation | All utterance text in order, with normalized researcher/search-assistant roles |
| Timestamps, source lists and annotations | Kept in private input evidence, not rendered as conversational text |
| Future researcher message or reference target | Excluded |
| Prior generated reply from a different Task 1 case | Excluded; each supplied prefix replaces the preceding input |

Researcher utterances map to model `assistant` messages, search-assistant
utterances to model `user`, and persona/goal instructions to model `system`.
Task 2 repeats the request with current history and resets on a new conversation.
"Full history" means full available utterance text, not every raw metadata field.

## Conversation inspection and stopping

Earlier private inspection reviewed openings, clarification, skepticism,
rejection and acceptance of recommendations. Those examples showed that valid
researcher reactions vary in detail and tone; a concise reply is not inherently
more faithful. Some assistant recommendations were disputed by the human, so
assistant claims must not become facts about the researcher's knowledge or
completed external actions. Public examples elsewhere are illustrative, not
verbatim export excerpts.

All 56 positive assistant stop flags occur at conversation ends. Eight records
end without any positive stop flag. No researcher message has `is_final=true`.
A terminal assistant flag or absence of another recorded turn is not proof that
the researcher independently chose to stop; collection may be censored. This
export therefore does not directly supervise a human stop classifier. The
current Task 2 generator infers satisfaction or abandonment from context, with
administrative error closures accounted for separately.

## Supported approaches

"Feasible now" means implementable and testable with available evidence, not
demonstrated competitive performance. See [method decisions](method-decisions.md)
for actual comparisons and the selected baseline.

| Approach | Classification | Concrete reason |
|---|---|---|
| Scenario/history prompting | Feasible now; selected baseline | Inputs and next-turn prefixes exist; no new training needed. Voice and invented knowledge still need review. |
| One conditional style edit; narrow action-fidelity repair | Feasible now | Uses the same supplied evidence. Task 1 narrow repair was tested; broad content correction and Task 2 transfer are not established. |
| Training-only few-shot examples/retrieval | Feasible now as a comparison | 266 targets can supply examples, but coverage is small and tested variants showed no recurring gain. Prevent same-conversation/future-target leakage. |
| Full history plus reminders or explicit labels | Feasible now as a comparison | Requires no new labels. Tested variants were mixed; prompt length is not a proven causal explanation. |
| Summarize older history, retain recent text | Feasible now as an experiment; needs more evidence for adoption | A small screen reduced draft-input tokens; it did not establish better realism or whole-pipeline savings. Summaries can erase voice or attribute claims incorrectly. |
| Existing user-turn model such as UserLM | Needs more evidence | Its template, stopping representation and domain/persona transfer must be tested; a published checkpoint is not a validated TREC solution. |
| Task-specific fine-tuning | Needs more evidence | 64 conversations over 10 goals with unverifiable participant separation are insufficient to assert robust generalization. A bounded pilot is possible, not an established solution. |
| Learned latent user-state alignment | Needs more evidence | No observed per-turn beliefs/emotions or validated state supervision; an inferred prompt summary is a different method. |
| Fit human stopping from final assistant flags | Unsuitable with this export | Zero positive researcher-stop labels; assistant endings and missing turns are not human stop ground truth. |
| Treat persona profiles as independent participant IDs | Unsuitable | No stable participant identifier; 12 profile objects do not establish 12 people. |
| Substitute supplementary conversations for official logs | Unsuitable for official-data claims | Different collection, parsing and stopping conditions; its audit cannot establish official coverage. |

Split evaluation by whole conversation. Report goal overlap and uncertainty;
verified participant-disjoint splitting is impossible without additional IDs.
Keep reference targets, later turns and hindsight annotations out of prompts,
retrieval, summaries and inferred profiles. Synthetic counterfactuals help find
fragility but do not provide human realism labels.

Private inspection provenance: the original workspace's
`docs/research/2026-10-03-official-data-inspection.md` and the export checksum above.
The separate [supplementary audit](2026-10-03-data-inspection.md) remains historical
evidence about that collection only.
