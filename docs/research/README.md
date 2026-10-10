# TREC UserSim research notes

## October 10: both official baselines complete

Task 1 submitted 62 predictions. Task 2's final HTTP428, full saved-request replay
and fresh organizer GET agree: **57 processed, zero remaining**. Task 2 has
**49 normal endings and eight administrative closures**, 266 submitted turns,
258 generated pairs / 516 model calls and **$0.173554630 actual cost**. Three
official allowances remain for each task. Debug v5 stays intentionally paused.

Our Task 2 completion parser initially rejected exact run-ID-bound wording that
Task 1 already accepted. A reviewed local reconciliation preserved frozen sources
and original evidence and corrected the checkpoint without another POST or model
call. The public parser/recovery fix passes 139 tests / 92 subtests; all 91 audit
controls pass. Full replay and remote confirmation establish submission integrity,
not researcher realism or competition score. Existing knowledge, style and
persistence limitations remain documented.

Next: review organizer results when available. No further run is needed for this
baseline. [Completion/recovery evidence](task2-recovery-plan.md) and
[submission ledger](../submission-ledger.md). Earlier dated checkpoints below
preserve history and are superseded by this completion record.

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

Latest monitored checkpoint: **47 of 57 processed**, comprising 40 normal endings
and seven administrative closures; 226 checkpointed turns and 440 saved model
calls costing $0.146237160. Original timeouts at 188 and 208 exhausted the unchanged
grace; their distinct closes at 189 and 209 returned HTTP200/new conversations.
Bounded read-only checks rebuilt both pairs of cached requests and verified the
closure evidence, without claiming full-prefix replay. A later HTTP502 at 211
also advanced through one distinct close at 212. Timeout 226 is now awaiting a
delayed reply. No original message was reposted and no additional official run
was started.

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

The current original ReadTimeout is in the unchanged 30-minute grace. The final
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

## Current reading path and decisions

- [Project handoff](../project-handoff.md): selected pipelines, completed runs,
  frozen source versus current source, safe inspection and next action.
- [Official-data evidence](official-data-evidence.md): schema, coverage,
  participant identity limits, stopping signals and leakage boundaries.
- [Method decisions](method-decisions.md): controlled comparisons, rejected
  variants, literature adaptations and what remains unresolved.
- [Implemented architecture](../task2_architecture.md): runtime diagrams, roles,
  reset behavior, model calls and recovery.
- [Experiment ledger](experiment-ledger.md) and
  [submission ledger](../submission-ledger.md): dated experiments versus organizer
  allowances, completion, costs and private artifact provenance.

Task 1 generates one next researcher message from any supplied conversation
prefix, including an opening or an intermediate turn. Task 2 repeatedly plays
that researcher against the organizer's assistant and produces text plus a stop
flag. There is no single correct wording; evaluate context fit, continuity,
knowledge attribution and plausible voice, not conciseness alone.

The official export is locally available: 64 conversations, 10 goal objects,
12 distinct persona profiles and 266 researcher-message targets. Profiles are
not verified participant IDs. Zero researcher messages have a positive stop
flag. The public supplementary collection remains separate, with its own
[historical audit](2026-10-03-data-inspection.md).

The selected baseline uses Luna and one editor call. Task 1 official explicitly
selected narrow fidelity repair; Task 2 kept style editing, full available
utterance text and a draft stop decision. Prompt variants, few-shot examples,
long-history summaries, planning and a stronger hosted model were tested in
bounded development screens without a recurring gain sufficient to change the
broader default. Existing UserLM, robust task-specific training and learned state
alignment still need evidence; learning human stops from assistant terminal flags
is unsupported by this export. See the detailed method/data classifications.

Next: review organizer results when available. Both official baselines are
complete; keep debug v5 paused and preserve private inputs, outputs, frozen
sources and recovery evidence. No additional paid experiment, submission,
publication or transcript sharing is authorized by these notes.

## Historical research and proposals

The [October 3 index snapshot](archive/2026-10-03-research-index.md) preserves the
initial candidate sequence and data-access uncertainty before the official export
was supplied. The [source refresh](2026-10-03-research-refresh.md) records that
date's primary-source inspection and limitations. [Implementation proposals](implementation-options.md)
remain distinct from the implemented architecture.

The [September 27 reassessment](archive/trec-usersim-advisor-reassessment-2026-09-27.md),
[original directions](archive/trec-usersim-winning-directions-2026-09-27.md) and
[original Opus advice](archive/trec-usersim-opus-advice-2026-09-27.md) preserve earlier
reasoning, not approved execution plans. Earlier dated run checkpoints below are
superseded by the October 10 completion record at the top.

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
