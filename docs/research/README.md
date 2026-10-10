# TREC UserSim research notes

## October 9: stop debug and submit one baseline

v5 is intentionally paused at a clean boundary: 886 saved turns, 129 normal
endings, 38 server-error closures and one unfinished conversation. Actual cost
$0.664036040; no request/error is pending. A reviewed prefix audit reproduces
all 1,696 model calls and 848 generated submission pairs and matches fresh server
history. Debug is **not complete** and no HTTP428 is claimed.

Independent selective review supports a candid baseline submission, with
knowledge leakage, polished/weakly differentiated persona style and excessive
persistence recorded as limitations. The generator and editor stay unchanged.
A separately reviewed operator launcher binds the paused evidence and review
before official access, retaining default 24/25%/3 outage limits; the ordinary CLI
completion gates stay intact. Ten operator-launch tests and independent source
review pass. Official run `np-labs-luna-style-task2-official-20261009-v1` started
with HTTP200; a fresh quota check confirms three official Task 2 allowances remain.
Monitor this same run through explicit HTTP428 and final audit. Keep v5 paused. See [readiness evidence and limits](task2-recovery-plan.md) and the
[submission ledger](../submission-ledger.md). This supersedes the older next
actions below to continue debug until HTTP428.

A separate, independently reviewed background watcher waits for successful
official service exit, then runs the pinned read-only completion audit. Seventy-four
audit controls and four watcher controls pass. It replays all cached requests and
submissions, requires 57 unique conversations and explicit final HTTP428, and
checks fresh organizer status, team summary and quota. It sends no POST or model
request. Proven ReadTimeout replies recovered through GET are audited separately
from POST receipts. Verified backend-error closures are replayed against exact
server history, separate closing intent, both original and closing receipts,
frozen outage limits and reconstructed counters. Normal completions and
administrative closures remain separate; unrecognized recovery variants halt
confirmation for a separate review. No completion or quality score is manufactured.

Active monitoring observed two consecutive original request timeouts. Both
recovered delayed replies without a repost or administrative closure; the same
official run continued. A matching synthetic consecutive-timeout test exposed
an empty optional observation proof bypass, now rejected by the reviewed final
checker. Generator, editor, runtime and frozen recovery policy are unchanged.

Monitoring also verified a backend HTTP502 followed by one distinct administrative
close. The original message was not resent, and the close used no model call or
researcher-stop counter. Mixed synthetic checks cover delayed replies before
and after closures, consecutive closures and a closing HTTP428. Independent
review caught a missing original-error receipt digest in the final report;
the replacement audit now binds that receipt too, with status/body mutation
controls. The reviewed v5 watcher replaces earlier watchers; it cannot restart or modify the run.

An original ReadTimeout is currently in the unchanged 30-minute grace. The final
checker now also supports a proven grace-period closure if one is necessary:
ordered transport/observation/closing timestamps, exact unanswered history,
archived original, intent, separate closing receipt and reconstructed state.
Twenty synthetic controls include early-close rejection, fully rebound invalid
timestamps and an interruption after a durable closing receipt with no repeated
POST on resume. An optional confirmed closing-pending archive is verified and
hashed. Unbound archived error diagnostics require separate review. This proves
local evidence consistency against the frozen runtime, not independent network
timing. The live generator, editor, runtime and waiting policy remain unchanged.

## Coverage terminology

The training export has 64 human conversation records. Official Task 1 has 62
turn-prediction cases over 10 goals; official Task 2 has 57 end-to-end conversations
over 11 goals, according to the [organizer guidelines](https://trec.usersim.ai/guidelines).
Our paused Task 2 debug uses development scenario-agent combinations; its
observed larger conversation count is separate from those official test pools.
See the [submission ledger](../submission-ledger.md) for exact count definitions.

## October 9: second budget continuation and delayed-reply audit

v5 reached 799 submitted turns: 114 normal conversation endings, 35 administrative
server-error closures and 1,528 successful model calls. Actual model cost was
$0.599974420; cumulative reservations were $5.998019400. The next draft was absent
and the $6 reservation guard halted before another request. Under the user's
instruction to increase budget and finish, an independently reviewed migration
raised only this run's reservation cap to $12. The same run resumed with its
1,000-turn guard, 30-turn conversation guard, 48/25%/3 outage limits and unchanged
generator/editor. No new organizer start or allowance was used.

Dry-run and apply each replayed all 1,528 cached generation requests and confirmed
exact current history with a fresh GET. Old manifest, frozen source, policy,
halted state and error are archived privately in `migration-before-budget-12/`.
Configuration, source, policy and state hashes passed post-apply verification;
enabling the state was the final write. Migration made no POST.

One original timeout at request 745 received a delayed reply during the grace
period. It was reconciled as a normal continuation, with no operational close,
repost or invented original POST receipt. A separate read-only audit helper
checks its request, transport proof, archived in-flight marker, server history,
prior/resulting state, counters and model accounting. Independent review caught
and corrected an orphan-result inventory gap; six synthetic tests and primary
verification of the real event pass. The completion and future continuation
audits require exact paired evidence. This is integrity evidence, not a global
quality or human-realism score. Await explicit HTTP428, then audit the full run.
No official Task 2 run has started. [Recovery plan](task2-recovery-plan.md).

## October 9: recover an explicitly unavailable organizer agent

v5 subsequently paused at request 650 on HTTP503 explicitly identifying an
unavailable organizer agent. Fresh read-only session evidence confirmed the
exact failed message was persisted unanswered. This differs from a generic503:
the classifier requires the matching conversation ID and the nested structured
`Agent '<name>' is currently unavailable.` message. All existing integrity,
prefix, uncertain-request and outage guards still apply.

Synthetic tests first reproduced the unsupported recovery, then verified one
close, restart replay, delayed-reply proof and rejection of unrelated503/504.
135 runtime tests / 86 subtests pass. Independent review cleared code and migration after
adding explicit old/new classifier source pins. All 1,252 cached model requests
and historical outcomes replayed exactly before mutation. Old source/policy,
state and error are archived in private `migration-before-agent-unavailable/`;
state/error stayed unchanged, with the new classification policy written last.

One distinct close at 651 returned HTTP200/new scenario, advancing v5 to 652:
92 normal endings, 26 administrative closures and $0.489702915 actual model cost.
No original message was resent or model call used for the close. The same debug
continues with $6 / 1,000 turns / 48 absolute closures; 25% and three-consecutive
error circuits remain active. No new allowance or official start. Await HTTP428
and the full completion audit. [Recovery plan](task2-recovery-plan.md).

## October 9: continue the same debug run past the absolute closure guard

v5 reached a saved HTTP500 at request 635 with 90 normal conversation endings,
24 administrative server-error closures and $0.482075295 actual model cost.
Only the absolute closure guard blocked recovery. An independently reviewed
migration raised this run's frozen absolute limit to 48, retaining the 25%
fraction guard, three-consecutive-error guard, $6 reservation cap, 1,000-turn
limit and 30-turn conversation limit. Generator and editor requests are unchanged.

All 1,224 cached model requests and historical outcomes replayed exactly, and
fresh GET confirmed the failed message was persisted unanswered. Migration made
no POST. Old source, policy, state and error are archived privately. The state
and original failure stayed unchanged; the new policy was the final enabling
write. The resumed wrapper then sent one distinct administrative close at 636,
received HTTP200/new scenario and advanced to 637: 90 normal endings and 25
administrative closures. No original message was resent or model call used for
the close. No new debug allowance or official Task 2 start.

130 runtime tests / 79 subtests pass; independent source review found no remaining
blocker. This is an engineering continuation checkpoint, not API completion or
a human-realism score. Continue until explicit HTTP428, then audit all retained
requests and outputs. [Recovery plan](task2-recovery-plan.md).

## October 9: same-run continuation beyond the turn guard

v5 paused cleanly at 500 submitted turns: 72 normally completed conversations,
19 operational backend-error closures, 962 model calls and $0.369902385 actual
model cost. No error or uncertain request remained. Under the user's instruction
to continue until the end, raise this run's total-turn guard to 1,000, preserving
the $6 reservation ceiling, 30-turn conversation guard, generator and outage
policy. Other runs still default to 500 turns.

All 962 model requests and saved outcomes replayed exactly; a fresh GET matched
the complete current server history. Independent review cleared the selector
and explicit migration, including exact source/policy bindings and state
enablement last. Full runtime verification: 126 tests / 73 subtests pass.
Original manifest, frozen source and halted state are archived privately in
`migration-before-total-turns-1000/`. Post-apply configuration, counters and
archive hashes passed. The same service resumed with `--cap-usd 6
--max-total-turns 1000`. No start or saved request was repeated; no new allowance
or official run. This is a dated resume checkpoint, not completion or a quality
score. [Recovery plan](task2-recovery-plan.md).

## October 9: authorized budget increase

Automatic recovery succeeded and v5 reached 403 turns: 58 completed conversations
and 16 operational closures. The next editor call hit the original$3 cumulative
reservation limit; actual cost $0.293755280,775 successful model calls. No request
is uncertain. The user authorized increasing the budget and continuing to the
end; select a $6 total reservation ceiling for this same debug run.

The CLI now exposes a frozen, validated `--cap-usd` option; its default stays $3.
All 775 saved model requests replay unchanged, the current draft is cached, and
fresh GET exactly matches the saved history. 124 runtime tests / 69 subtests pass.
Independent review cleared the explicit archive/migration, including its
interruption boundary. Post-apply hashes passed; same v5 service restarted with
`--cap-usd 6`. No outcome count advanced during migration and no saved draft was
regenerated. No new debug allowance or official start.
[Recovery plan](task2-recovery-plan.md).

## October 9: verified backend-error recovery

Latest verified checkpoint: v5 halted on an original response timeout at request
327, with 46 completed conversations and 11 separately recorded operational
closes. Recorded model cost: $0.245687720 in 634 successful model calls.
The correction adds automatic exact-timeout reconciliation to the recovery
wrapper: wait for a delayed reply, then allow one verified operational close
after 30 minutes of observed persistence. Unknown requests and closing uncertainty
still halt. Policy v2 adds absolute, fraction and consecutive-outage bounds.
Independent review cleared the implementation and migration. All 634 saved model
requests replayed unchanged; terminal counts and current history matched exactly.
The original checkpoint/source/policy/pending/error are archived. The same service
resumed and entered read-only timeout reconciliation at 15:26 UTC, October 9;
the checkpoint remains at 327 while waiting. Task 2 debug allowances remain 5,
official 4. No new run was started. Full runtime verification: 121 tests / 64
subtests pass. See the [recovery plan](task2-recovery-plan.md).

The paragraphs below preserve the earlier checkpoints and manual recovery scope.

Earlier snapshot: v5 resumed at request 290 with 40 completed conversations and
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
confirms Task 2 debug7, official4; Task 1 debug8, official 3. Organizer outage
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
