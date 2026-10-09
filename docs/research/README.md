# TREC UserSim research notes

## October 9: verified backend-error recovery

Latest verified checkpoint: v5 halted on an original response timeout at request
327, with 46 completed conversations and 11 separately recorded operational
closes. Recorded model cost: $0.245687720 in 634 successful model calls.
The correction adds automatic exact-timeout reconciliation to the recovery
wrapper: wait for a delayed reply, then allow one verified operational close
after 30 minutes of observed persistence. Unknown requests and closing uncertainty
still halt. Policy v2 adds absolute, fraction and consecutive-outage bounds.
Independent implementation review and explicit frozen-checkpoint migration
precede same-run resume. No new debug allowance or official Task 2 start is part
of this correction. See the [recovery plan](task2-recovery-plan.md).

The paragraphs below preserve the earlier checkpoints and manual recovery scope.

Current snapshot: v5 resumed at request 290 with 40 completed conversations and
11 operational closes; recorded model cost $0.219581060. A second timeout at 0288
remained unanswered after 118 minutes. The same reviewed one-off procedure closed
it once at 0289, with HTTP200 confirming a new empty scenario. No original
request was resent. Source, prompts, editor and automatic 500/502 policy remain
unchanged. The frozen operational skip limit is 12. No official Task 2 start.

User authorizes continuing debug with explicit operational closes after verified
backend failures, then one official Task 2 run if debug verifies the approach.
[Recovery plan](task2-recovery-plan.md). Five Task 2 debug allowances remain;
Task 2 official4. No official Task 2 run yet. Generator and editor unchanged.
107 tests / 60 subtests pass; independent review cleared the recovery implementation.
The original v5 manifest, source and checkpoint were archived before migration.
Saved receipts were replayed and compared with a read-only server session.
The recovery wrapper reached 28 completed conversations and seven operational
closes before a response timeout at request 0198. Two read-only observations
confirmed the exact saved message was still unanswered after 45 minutes.
An independently reviewed one-off recovery archived the original pending request
and sent a distinct final close at 0199. HTTP200 confirmed a new empty scenario.
v5 has resumed at 200: 28 completed conversations and eight operational closes,
with $0.147200385 in 384 model calls at restart. No original message was resent
and no missing POST response was fabricated. The automatic policy remains limited
to known HTTP500/502; this timeout recovery is recorded as a manual exception.
No official Task 2 run has started.
Operational closes send `is_final=true` as the researcher, but are not modeled
researcher satisfaction or abandonment. Quota remains debug five / official four.


[Submission ledger](../submission-ledger.md): every organizer run, quota used,
status, model cost and private input/output artifact locations.

## October 6: Task 1 official submission complete

The authorized Task 1 official run completed **62 predictions across 10 goals**
(36 openings, 26 follow-ups), for **$0.029373225** in 124 model calls. Organizer
completion, read-only run status and team summary agree. All exact requests,
outputs and submitted texts passed local integrity checks. Remaining Task 1
allowances: debug 8, official 3. [Run evidence and recovery](task1-live-validation.md).

The [editor repair](task1-fidelity-fix.md) uses a narrow action-provenance exception
while preserving voice and legitimate compromises. The broad first candidate
was rejected for requirement hardening. The selected candidate was checked on
64 saved debug drafts, synthetic controls and repeats, with reviewer disagreement
and limitations recorded. This is an acceptable baseline submission, not proof
of perfect human style or an official quality score.

The run also exposed an unsupported client assumption about the last speaker.
A generic researcher-ending-prefix path preserves all supplied turns without
inventing an assistant reply. 87 tests and cached-request replay passed; recovery
resumed the same run without duplicate submissions. [Runner safeguards](../task1_runner.md).
Task 2 remains halted and untouched. Next: await Task 1 evaluation; any additional
official run or Task 2 recovery is a separate decision.

## October 6: second Task 2 debug attempt

The user authorized a fresh attempt because the old pending assistant reply could
not be safely recovered through the documented API. The new run again halted on
organizer HTTP500: five researcher messages saved, four assistant replies, no
complete conversation. Ten model calls cost $0.00512328. No messages were retried.
Task 2 debug allowance is now 8; official 4 remains untouched. Requests were already
sequential and 15–25 seconds apart. [Evidence and next action](task2-debug-second-attempt.md).
The [support draft](task2-debug-recovery-request.md) covers both runs and is not sent.
Do not consume another allowance automatically.

## October 6: Task 2 debug integration

The [illustrated architecture](../task2_architecture.md) explains the researcher
loop, model calls, module boundaries, and why uncertain requests halt.
The [four-model design review](task2-design-review.md) records panel findings,
our decisions, and verification limits. The subsequent [code-structure refactor](code-structure-plan.md)
separates the runtime from historical experiments and preserves captured model requests.

The [Task 2 runner](../task2_debug_runner.md) is implemented with checkpointed
transport, scenario resets, full-history or incremental reply handling, and
explicit stopping. The first live debug attempt halted on organizer HTTP500
after four accepted researcher messages and three assistant replies; no complete
conversation or official submission. [Evidence and recovery](task2-debug-handoff.md).
The entries below are historical research proposals; this update takes precedence
for current Task 2 implementation status.


Updated October 3, 2026. This is the canonical research status and proposed experiment sequence for this repository. Our objective is to simulate how human researchers look for datasets, including their reactions, variation, and decisions to stop. No approach has been validated on this task in our work so far.

**Data evidence takes precedence over the architecture shortlist.** The [supplementary-data inspection](2026-10-03-data-inspection.md) identifies extraction defects, externally truncated sessions, and missing state labels. It also establishes that the study's persona intervention affects the assistant, not the human. Official training logs remain unlocated/inaccessible; no implementation choice is validated against them.

## Start here

- [Data inspection and corrections](2026-10-03-data-inspection.md): observed supplementary-data constraints and which earlier suggestions need to be withdrawn or narrowed, with an executed audit notebook.
- [Possible implementations](implementation-options.md): visual walkthroughs of the shared runtime, alternative generators, training, and evaluation; all labeled as proposals.
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
- **Remeasured October 3:** 32 supplementary sessions from 16 people and 151 prompt openings, matching the workbook session by session. All prompt spans and session endings were reviewed; malformed boundaries and alternate/regenerated outputs mean these are not yet clean training pairs. See the [audit](2026-10-03-data-inspection.md).
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

**Decision:** treat direct prompting, retrieval, and UserLM as candidate comparisons, not a selected implementation. First inspect official logs and repair supplementary extraction. The supplementary audit does not support substantial new training, direct stop-label fitting from final turns, or a labeled personality/state controller. Keep learned state alignment in the literature without treating its prerequisites as satisfied.

**Next action:** locate and inspect official training logs, then define reproducible splits and the smallest offline comparison. These notes do not authorize paid runs, official submissions, or uploading participant data to external providers.

## Verification of this documentation change

Primary sources were rechecked on October 3; the scope and reading depth are recorded in the refresh. Local Markdown links, whitespace, documentation-only scope, and accidental credential/host-path inclusion were checked before the research commit. No simulator tests or experiments were run for this documentation change.

## October 7 post-outage debug check

A newly authorized Task 2 debug attempt is running after the organizer reported
the internal outage resolved. See [live handoff](task2-debug-third-attempt.md).
Older halted runs remain preserved; no official Task 2 submission.

### October 7 status reconciliation

Third Task 2 debug attempt halted on HTTP500 generating the fourth agent reply.
Three successful exchanges; GET debug/session confirms seven messages ending
in the fourth saved researcher message. Zero completed conversations. Service
failed and local state reconciled to halted; no repost or new run. GET budget
confirms Task 2 debug7, official4; Task1 debug8, official3. Organizer outage
announcement did not establish resolution for this attempt. Private receipts
include session_status_check.json and budget_status_check.json.

Offline client audit: all 13 Task 2 continue payloads matched the organizer
serializer and passed schema validation; full three-run replay matched 26 model
and 16 organizer calls. See [audit](task2-debug-third-attempt.md). No live retries.

## Fourth Task 2 debug attempt

User explicitly authorized another endpoint check. Run: `np-labs-luna-task2-debug-v4`.
Same unchanged Task 2 simulator (source c6525aa), sequential requests, $3 reservation
ceiling, halt on server failure. No official submission and no retry of old turns.
Persistent service: `trec-usersim-task2-debug-v4.service`.
Private receipts: `/home/npatta01/data/trec-usersim-runs/task2-debug-luna-v4/`.
Status: launched; check receipts and service before claiming completion or quota.
Latest mailbox search found no newer general repair instructions beyond the
previous outage notice; a newer reply grants a different team replacement access,
which does not authorize use of that team's credentials.

## Integration audit before further API writes

The observed HTTP200/new-scenario transition is fixed and replayed offline.
See [coverage matrix and remaining gates](task2-integration-audit.md). No live
run resumed; frozen-checkpoint migration and read-only reconciliation remain.

## v4 checkpoint migration and same-run resume

91 tests / 50 subtests pass after the transition and failure-status fixes.
Archived original manifest, frozen source, state and error in private
`migration-before-transition-fix/`. Replayed all five receipts; live GET matches
the new empty scenario exactly. State: one completed conversation, five user
turns, ten model calls, $0.004555995. Read-only budget confirms six debug
allowances remain. Same v4 service restarted; no new run or closing-message
resend. Generator/editor/model configuration unchanged. On later failures the
CLI now marks state halted and refreshes costs without clearing retry guards.
Check private state/receipts for current progress.

## Fifth Task 2 debug attempt — October 8

User explicitly authorized another debug allowance after read-only recovery
check found v4 still ending with the persisted unanswered user message.
Started `np-labs-luna-task2-debug-v5` with the tested HTTP200 transition fix and
failure-status accounting; generator/model/style policy unchanged. Sequential
requests, $3 reservation ceiling, stop on errors. No official submission.
Private artifacts: `/home/npatta01/data/trec-usersim-runs/task2-debug-luna-v5/`.
Service: `trec-usersim-task2-debug-v5.service`. Inspect live state for progress.
v4 remains halted with three completed conversations; no saved turn was resent.

## v5 user-authorized skip and same-run resume

Read-only reconciliation confirmed the fourth conversation ended with the
already-persisted failed user turn. User explicitly authorized trying a skip.
Sent one distinct operational closing message with is_final=true, checkpointed
as continue-0021; no failed message resend. HTTP200 confirmed a new empty
scenario. State preserves three completed conversations and separately records
one skipped conversation, one accepted error turn and one operational close.
The closing text is not counted as a natural researcher stop. Next request index
is22 to avoid reusing failed-turn model receipts. Original state, intent, server
response and before/after budget are saved privately. Five debug allowances
remain: no new allowance consumed. Same v5 service resumed; no automatic skip
policy enabled. If another failure occurs, halt and reconcile again.

## v5 resume after HTTP502

User requested resuming. Read-only session confirmed the failed turn saved with
no agent reply. Applied the previously successful explicit closing procedure;
continue-0065 returned HTTP200/new empty scenario. Nine completed conversations,
two separately recorded operational skips. No failed message resent. Source and
model policy unchanged; same service restarted at next index66. Five debug
allowances remain, verified after close. Private skip-502-intent/result and
pre/post-skip-502 checkpoints preserve this recovery. No automatic future skip.
