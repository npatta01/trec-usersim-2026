# Method decisions and tested alternatives

Current aggregate summary, October 10, 2026. We want plausible researcher
reactions conditioned on the supplied persona, goal and conversation, not the
shortest message or an ideal evaluator's review. We are implementing a simulator,
not generating a synthetic training dataset.

The selected baseline is Luna with researcher-role chat messages, explicit
speaker instructions and one editor call. Task 1 official uses the narrow
`fidelity` editor; Task 2 uses the existing `style` editor and a draft stop flag.
Full available utterance text is retained. Compaction, retrieval, planning and
repeated critic/refinement loops are not enabled. The
[architecture](../task2_architecture.md) describes what actually executes.

## What the comparisons establish

Most experiments reused small training-development prefixes, saved drafts or
synthetic probes. They are not an independent held-out benchmark, and repeated
targets within a conversation are not independent participants. Some reviews
were unblinded. We report preferences and failure examples as limited evidence,
not general realism rates. A correct speaker can still be too polished, forget
an objection, invent knowledge or adopt a dubious assistant claim.

| Hypothesis / comparison | Observed result | Decision and limits |
|---|---|---|
| Role mapping and explicit researcher instruction resolve assistant-style continuation | Tiny and real-case checks exposed wrong-speaker generation; corrected roles/instruction enabled plausible researcher output, but errors remained | Keep researcher → model `assistant` and explicit role framing. Transport alone was not shown to be the cause; no claim that larger models cannot help. |
| End reminder, explicit transcript, or larger local model improve speaker fidelity | Matched 30-case screen: Qwen3-8B baseline 22 researcher / 5 assistant / 3 mixed; reminder 25/2/3; transcript 19/8/3; Qwen3-14B 24/6/0 | Reminder was promising but mixed; that transcript variant regressed. No universal ranking. Single unblinded speaker review, not persona-quality assessment. |
| Unchanged Luna handles broader Task 1 prefixes | 107 targets from 20 additional conversations across 10 goals: all correct-speaker, including 36 inputs over 2,000 tokens; no empty outputs or stray thinking markers | Training-development stress sample, unblinded. Later turns remained overly polished/technical; role success is not a quality rate. |
| Opening versus follow-up instructions improve realism | 12 calls stayed in researcher role; wording preferences were mixed, including a technical-register counterexample | Baseline retained. Conditional turn mode is feasible, not demonstrated better. |
| A critic detects style mismatch and conditionally edits | 12 critic calls returned no findings; no edit calls occurred | Tested gate was inert. This does not prove drafts were faithful or that all critics are ineffective. |
| Structured prompt or two retrieved human examples improve continuation | 36 replies across 12 contexts: all nonempty and correct-speaker; one few-shot reply falsely attributed a known dataset to the assistant | No consistent gain; baseline retained. Training-only retrieval remains feasible, without demonstrated value. |
| Shorter objective, communication-style anchoring, ownership rendering or act-aware instructions improve the next reaction | B20: 36 replies over 12 prefixes, mixed preferences and an unsupported-date regression. B21: 35 known-valid outputs, one unreplayed uncertain request; complete cases mostly tied. B22: 20 replies, all 10 contextual comparisons tied | No default promotion. A plausible unobserved disclosure is not automatically an error. Prior panel agreement and near-ties are not measured gains. |
| Observed-style prompt reduces polished wording | 11 of 12 outputs became shorter, but one introduced an unsupported personal claim | No adoption. Length reduction is descriptive and does not establish fidelity. |
| One conditional post-edit helps without rewriting the researcher's intent | 12 saved drafts: 8 unchanged, 4 edited; 2 edited late cases preferred, 10 ties, no identified material regression | Small subjective signal. User subsequently selected default-on editing; it is not a guaranteed quality gain. |
| Harder mismatches reveal editor value | 11-case screen: no clear style gain on five real cases; all three artificially distorted drafts improved; three synthetic good controls showed no gain | Useful obvious-artifact repair, not proof of broad naturalness. Synthetic distortions are not real-user ground truth. |
| Task 2 harness can stop and react over generated exchanges | Synthetic rollouts tested satisfaction, corrections, repeated failure and abandonment; a responsive follow-up probe still found a redundant retry after an exhaustive no-match reply | Supports baseline integration, not human realism. Responsive synthetic assistant replies test different evidence from fixed recorded prefixes. |
| Long official prefixes preserve researcher voice and knowledge | Eight late prefixes, 3,884–5,635 draft-input tokens, 16 draft/editor calls: all correct-speaker, seven continue and one abandons; some unsupported expertise remains | Keep full history as control. This is next-turn continuation, not eight complete generated sessions or a causal length test. |
| Grounding cue, named transcript or summary helps long history | Four long prefixes × four arms: 16 draft/editor pairs plus 4 summaries (36 calls). Grounding cue had 2 contextual preferences / 2 ties; summary cut draft-input tokens by 37–53% | Small, unblinded screen only. Editor saw full original history in every arm; not full-pipeline compaction or proven cost/latency savings. No default change. |
| Long-history context improvements survive harder cases and positive controls | Four more official prefixes + four fictional controls, 72 calls; grounding had one modest official-case preference, other comparisons mixed. An initially claimed access failure was pragmatically ambiguous and withdrawn after advisor review | No promotion. Retaining a requirement, reasoning about whether it is met, and speaking naturally are separate checks. Summary savings varied and sometimes increased short inputs. |
| Evidence reminder, recent-voice cue or balanced fictional demonstrations improve harder cases | Advisor-reviewed iterative screens included controlled ambiguity/length probes, repeated real prefixes and useful controls; no recurring arm advantage | Fix fixtures and code before conclusions. Do not mistake a rigid requirement checklist, smaller output, or script-induced repetition for better researcher realism. |
| Evidence-linked plan then fresh renderer improves grounded voice | Rewriting addressed the risk of preserving an unsupported draft claim, but did not establish recurring voice improvement | Experimental modules remain unselected. Structured intermediate state is inferred, not observed human thought. |
| Transfer TalkPlay/Spotify user-generation ideas | 32-call comparison on 4 early/late contexts with repeated draws: selective editing and same-call private progress assessment did not show recurring voice gains | Adaptations were tested, not reproductions of those pipelines. Do not import forced continuation, fixed session lengths or future planned human turns. |
| Stronger hosted model fixes voice with unchanged history | Luna versus GPT-6 Sol: 8 raw drafts each on 4 contexts; mostly ties after context-aware review, all continued | Keep Luna. Raw drafts only; Sol + editor and full sessions were not tested. No claim Sol is generally inferior. |
| Narrowly repair unsupported performed-action claims in Task 1 | V2 tested 64 development drafts + 8 synthetic probes, then repeats; local action repair worked on tested targets without broad goal hardening | Selected explicitly for official Task 1. Broad V1 was rejected; V2 does not repair every waiver or solve persona realism. See [full fidelity study](task1-fidelity-fix.md). |

The local full Qwen3-8B development generation covered all 266 next-message
targets. Completion without empty outputs or stray thinking markers is an output
integrity result, not a reliable quality pass rate. Manual inspection found
wrong-speaker, tone and objection-handling failures. Later/larger inputs were
associated with errors in a small screen, but there is no established 1,000- or
2,000-token cutoff or proof that length caused them.

## Why this baseline remains selected

Luna produced plausible researcher turns in the inspected cases at low cost;
the editor sometimes repaired expression, and Task 1 narrow fidelity repair
targets a concrete unsupported-action failure. Broader prompting, few-shot,
planning and stronger-model screens did not establish recurring benefits strong
enough to promote another default. This is a baseline choice under limited
evidence, not a claim that all useful ideas have been exhausted.

Some advisor lanes failed at provider/runtime execution. A failed invocation or
empty result is not evidence about that model's user-simulation quality. Advice
and code review informed experiment design; they are not independent participant
ratings. Public advisor packets used source/design and synthetic material; no
private participant transcript or output was included in those packets.

Remaining issues include overly polished or weakly differentiated voice,
unsupported researcher knowledge/actions, questionable recommendation acceptance
and excessive persistence. Preserving a stop boolean in code does not prove an
editor preserved its meaning. Official submission completion does not resolve
these issues; evaluation results are still unavailable.

## What is not supported, and what remains open

Reject future-turn leakage, persona stereotypes, invented external checks,
hard-coded fixes for a specific goal, unconditional brevity, and treating every
goal preference as mandatory. Do not fit a human stop classifier to assistant
endings: the [official export](official-data-evidence.md) contains no positive
researcher stop labels. Do not treat operational closures as natural stops.

Future candidate tests include stable human voice evidence versus self-generated
voice, training-only retrieval with a random-example control, summary retention
of old objections and recent verbatim speech, and stronger-model-plus-editor
comparisons. Each needs matched hard cases and successful controls, leakage
checks, repeated draws where affordable, context-aware blind review and regression
inspection. No additional model or organizer run is authorized by this backlog.

## Literature transfer boundary

The private source review inspected [TalkPlayData 2](https://arxiv.org/html/2509.09685v2)
and its [listener implementation at a pinned commit](https://github.com/talkpl-ai/talkplaydata-2/tree/8b4d47e6b3b91169f80a36ec135e5488368a470f/tp2dg/prompts/listener_llm),
[Spotify's RecSys 2026 work](https://arxiv.org/html/2609.30297v1) and the
[Microsoft UserLM-8b model card](https://huggingface.co/microsoft/UserLM-8b).
Separating the simulated user from the recommender, distinguishing private
assessment from spoken reply, and reacting to the actual assistant response
motivate our tests. Their synthetic-data pacing, forced continuation and planned
future turns do not transfer to an unconstrained TREC session. UserLM's trained
user-turn behavior is a separate model comparison, not a portable prompt trick.
The tested adaptations did not establish broad realism gains; this is not a
negative evaluation of the original systems.

## Evidence locations and reproducibility

The public [experiment ledger](experiment-ledger.md) preserves integration and
recovery chronology; the [submission ledger](../submission-ledger.md) records
organizer runs only. Historical experiment modules are separated under
[experiments](../../experiments/README.md). Their private inputs and outputs are
not distributed, so a fresh public checkout cannot replay every historical
model comparison by itself.

Detailed private notes in the original research workspace
`/home/npatta01/.codex/worktrees/21de/trec-usersim-2026/docs/research/` support this
aggregate summary:

- `2026-10-04-matched-results.md`: local-model/reminder/transcript screen.
- `2026-10-05-luna-conversation-sample.md`: broader Task 1 stress sample.
- `turn-mode-pilot.md`, `critic-style-pilot.md`, `observed-style-pilot.md`,
  `single-call-prompt-comparison.md`: turn mode, critique and prompt/few-shot tests.
- `2026-10-05-extended-public-prompt-iteration.md`,
  `2026-10-05-b21-advisor-review.md`, `2026-10-05-b22-act-aware-results.md`:
  later prompt/act screens and corrected conclusions.
- `2026-10-05-style-postedit.md`, `2026-10-05-hard-style-postedit.md`,
  `optional-style-postedit.md`: editor screens and later default-on decision.
- `2026-10-06-task2-offline-baseline.md`, `2026-10-06-task2-responsive-probe.md`,
  `2026-10-06-task2-long-history.md`, `2026-10-06-task2-harder-results.md`:
  synthetic rollouts, longer prefixes and harder controls.
- `2026-10-06-task2-context-comparison.md`,
  `2026-10-06-advisor-iteration-cycle.md`, `2026-10-06-opus-voice-review.md`:
  long-context comparisons, reviewed iterations and fixture cautions.
- `2026-10-06-transferable-user-methods.md`,
  `2026-10-06-stronger-model-comparison.md`: literature adaptation and model control.

Those paths identify evidence; they are not public transcript links. Private
receipts and frozen source/configuration are required for exact request, usage
and output reproduction. Public numeric summaries do not replace those records.
