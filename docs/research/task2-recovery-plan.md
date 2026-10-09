# Task 2 backend-error recovery plan

## October 9: debug paused by choice; official baseline readiness

The user chose to stop debug and proceed toward one official Task 2 baseline.
v5 is intentionally paused at a clean boundary: **886 saved turns, 129 normal
researcher endings, 38 separately recorded server-error closures, and one
unfinished conversation**. Actual model cost is $0.664036040 across 1,696 model
calls; $6.629295600 is cumulative reservation accounting, not dollars spent.
No organizer/model request or error is pending. The service's failed state is
from deliberate operator termination after proving a safe pause, not a new
server failure. No researcher stop message was sent to pause that conversation.

A source-reviewed, read-only prefix audit reproduces every one of the 848
generated submission pairs, verifies all retained original/closing/delayed-reply
evidence and matches a fresh server GET. It explicitly records **no HTTP428 and
no debug completion claim**. The pause intent, original running state, source
snapshot and receipt are retained privately. Seven pause tests and two focused
proof tests pass; the successful live pause validates the actual process boundary.

Independent conversation review covers four purposive cases / 32 researcher
messages, including eleven- and seven-turn histories. Primary review also
inspected all researcher replies in eight purposive cases / 56 messages. The
review supports a candid baseline submission while recording knowledge leakage,
weak differentiation of Basic-English personas, polished wording and excessive
persistence. It supplies no whole-run realism rate or competitive-quality claim.

The normal official CLI still requires completed debug. This operator decision
uses a separate, reviewed private launcher that binds the exact intentionally
paused state, manifest, audit, pause and quality decision before credentials or
POSTs. It copies and freezes its evidence. The generator, full history and editor
remain unchanged. Official recovery retains default 24 absolute / 25% / 3 consecutive
closures; it does not inherit debug's 48 override. The selected official guards
are $6 cumulative model reservations, 1,000 total turns and 30 per conversation.

Ten operator-launch tests pass, including end-to-end completion, no-POST completed
replay, source/evidence/snapshot/ID tampering, temp-write residue and preservation
of the original launch failure if recording also fails. Independent review
cleared exact launcher SHA 4fbd7b3c before use. The private operator launcher and
its evidence are frozen alongside the unchanged runtime; they are not a new
ordinary CLI mode.

Official run `np-labs-luna-style-task2-official-20261009-v1` started with HTTP200.
The first exchange is saved and the same run is continuing. Fresh GET confirms
Task 2 official 3, debug 5 remain. No official completion claim yet: require explicit
HTTP428 plus a separate final integrity audit. Keep v5 paused. This decision
supersedes the older instructions below to continue debug until completion.


## Objective and authorization

User authorizes recovering conversations blocked by backend failures in the existing debug
run, then trying one official Task 2 run if debug verifies this procedure.
Same Luna generator, full history and editor; recovery is a transport policy,
not a researcher behavior. The original $3 reservation ceiling was raised
to $6 under the user's October 9 instruction to increase budget and continue
through the end. At the later 799-turn reservation pause it was raised to $12,
with the same generator and explicitly reviewed continuation evidence.
No new debug allowance is required to resume v5. No external message is sent.

## Design

Recovery reads persisted failed request and current server session before writes.
For 500/502 or an exactly classified conversation-bound503 agent-unavailable
response, if the exact failed user message is persisted after the exact
local prefix and no reply exists, send one distinct is_final operational close.
Keep original failure and close receipts. A new empty scenario or explicit run
completion confirms success; then advance request index past both messages and
increment skipped_conversations, not completed_conversations or user_stops.
If a delayed reply exists, reconcile it and continue normally. If a final turn
already advanced the session, reconcile the new empty scenario normally.
For a durably classified original `ReadTimeout`, preserve the original in-flight
request and read the server session. The 30-minute grace starts at the first
durable observation proving that exact request is persisted unanswered. Poll
read-only every 30 seconds, bounded to 65 observations per invocation. A matching
delayed reply is reconciled without a POST. Only after the grace and another
fresh exact session check may one distinct operational close be sent. Its
receipt is separate from the absent original POST response. A timeout during
that close cannot trigger another automatic close.

No recovery for malformed model output, bad response schemas, unclassified
in-flight requests, model uncertainty, authentication/quota failures or mismatched
server history. No blind repost. A failed close halts. Policy v2 defaults to at most
24 operational skips (the selected v5 limit is now 48), at most 25% of terminal conversations, and at most three
consecutive skips. The fraction denominator has a floor of eight conversations,
allowing at most two early skips while preserving the outage circuit. Existing
per-conversation, total-turn and model-spend limits also apply. These limits are
operational and must not be interpreted as human behavior.

A recovery wrapper keeps debug and official routes explicit and distinct. The
wrapper persists its own policy and frozen source. Tests use synthetic sessions,
not participant logs. Live debug completion and reviewed conversations gate the
first official run. All operational skips must be disclosed in the run description
and aggregate ledger. Evaluation treatment of outage skips remains unknown.

## Verification and next action

Test saved failure -> delayed reply/operational skip, exact-prefix mismatch,
closing failure, crash after closing receipt, completion on closing and route
separation. Independently review before API writes. Preserve original v5 frozen
source/state during explicit checkpoint migration; resume same run and monitor.

## Review corrections

Recovery verifies all available raw message fields, including stop flag and
timestamp; UTC Z and +00:00 spellings are compared as the same instant. Both
per-conversation and total frozen bounds apply to operational close messages.
The standalone debug runner still halts on errors; the explicit recovery wrapper
handles saved 500/502, narrowly classified503 and original ReadTimeouts. The official CLI requires
completed debug evidence, an explicit organizer completion receipt and a review
artifact bound to the exact final state before credentials or API access.

Existing v5 started before recovery was enabled, so its organizer description
cannot retroactively disclose skips. The local policy, recovery receipts and
ledger disclose this limitation. Fresh recovery-enabled debug and official run
descriptions disclose operational closures. No generator change.

Delayed replies have separate GET-derived reconciliation events, bound to the
original request and transport evidence. Future raw-prefix checks consume these
events. Recovery observations, intent, closing receipt and resulting state are
hash-bound; state is committed last. Cached receipts permit replay after a crash
without posting again. A matching closing pending marker can be archived and
cleared only when its bound intent and durable receipt confirm advancement.
An unknown or uncertain closing request remains blocked.

## October 9 automatic-timeout correction

The prior wrapper halted at every original ReadTimeout, requiring two reviewed
manual closures. That was an integration gap, not a generator failure. A third
timeout halted v5 at request 0327: 46 completed conversations, 11 operational
closes, 634 successful model calls and $0.245687720 recorded model cost.

The new timeout controller is verified with synthetic full-loop tests, delayed
reply arrival during the final check, receipt-before-unlink crash replay, closing
uncertainty, changed metadata, missing or altered proof, model uncertainty, and
outage bounds. Independent review checks the implementation before live migration.
Preserve the legacy manifest, source, policy, state, error and pending bytes;
replay all confirmed outcomes and reconstruct consecutive skips before resuming.
New classification evidence must separately record its migration provenance.

Independent follow-up review found no remaining actionable blocker after both
corrections. Full runtime verification: 121 tests / 64 subtests pass; 34 focused
tests / 14 subtests pass under optimized Python. Formatting, new-module lint and
diff checks pass. Bare pytest still fails collection of two unchanged organizer
test modules importing the removed `PersonaDefinition`, as previously observed
on the base. No claim that the legacy organizer suite passes.

Migration was independently reviewed, then applied without organizer/model POSTs.
Replay verified all 634 model requests, 46 natural terminal conversations,
11 operational closures, current history and consecutive-skip count 0. A fresh
GET verified the exact persisted original turn. Old pending/error files are
archived byte-for-byte in private `migration-before-timeout-v2/`, alongside old
manifest, frozen source, state, policy, session and reviewed migration script.
New manifest, policy, proof and archive hashes passed post-apply verification.

The same `trec-usersim-task2-debug-v5-recovery.service` resumed at 15:26 UTC,
October 9, and created its first exact persisted-turn observation. It is waiting
read-only for the 30-minute grace; no close at 0328 has been sent yet. The saved
state remains halted at 327 until reconciliation completes. Future errors use
the new policy without requiring a status prompt. Task 2 debug 5 / official4
remain; no new allowance, no official start. Inspect service and private state
before treating this dated snapshot as current completion evidence.

## Latest live evidence

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

### October 9 explicit agent-unavailable response

At request 650 the organizer returned HTTP503 with a nested structured message that the
configured agent was unavailable. Primary read-only evidence confirmed exact
persistence without a reply. A shared classifier accepts this response only
when the outer session ID matches the failed payload and the inner JSON detail
full-matches `Agent '<nonempty single-line name>' is currently unavailable.`.
Generic503/504, mismatched IDs, malformed details and quota errors remain blocked.
Delayed HTTP503 reply events must revalidate that same original classified proof.
The accepted backend subset is now explicit in the frozen recovery policy.

135 runtime tests / 86 subtests pass; the five new tests and seven negative subcases also pass
under optimized Python. Independent review identified missing classifier source
pins in future cap/turn migration scripts; corrected before use. Code and all
migration/audit sources were then cleared. No generator or stopping change.

Dry-run and apply replayed 1,252 cached model requests, full organizer outcomes,
current history and counters; fresh GET exactly matched the persisted unanswered
turn. Both old and new recovery/reconciliation hashes are pinned. Original
manifest, frozen source, policy, state and error are archived in private
`migration-before-agent-unavailable/`. Configuration/state/error were retained;
only the reviewed classification sources and policy changed, policy written last.
Migration made no POST. Post-apply hashes passed. Same-run close at 651 returned HTTP200,
advanced to 652 and used no model call or original replay. Snapshot: 92 normal
endings, 26 administrative closures, $0.489702915 actual cost; no new allowance or
official start. Continue with the existing 48/25%/3 limits until explicit HTTP428.

### October 9 absolute closure limit and same-run continuation

At request 635, v5 had a saved HTTP500 with 90 normal endings, 24 administrative
closures, 1,224 model calls and $0.482075295 actual cost. The absolute guard alone
blocked one more recovery; fraction and consecutive-outage guards had headroom.
The reviewed positive-integer `--max-operational-skips` selector keeps default 24
and freezes its selected value. Passing a different flag alone is refused.
Non-default official use additionally requires a quality-review artifact bound
to the exact selected policy hash.

Full runtime verification: 130 tests / 79 subtests pass; selected-policy optimized
verification: 9 tests / 15 subtests pass. The migration replayed all saved
requests/outcomes and checked fresh server history, complete source coverage,
failed-turn/close pairing and archived evidence. Only recovery-selector source
and absolute policy24 ->48 changed; generator/run configuration, state and
original error were retained. No POST occurred during migration. Policy is the
final enabling write. Archive: private `migration-before-skip-limit-48/`.

Post-apply hash/configuration checks passed. The same service restarted with
`--cap-usd 6 --max-total-turns 1000 --max-operational-skips 48`. One distinct close
at 636 returned HTTP200/new scenario and advanced the run to 637. It used no
model call and did not replay the original turn. Keep 25%/floor8 and three
consecutive-error circuits active. No new allowance or official start; await
explicit HTTP428 and the separately reviewed full completion audit.

### October 9 total-turn pause and continuation

After the budget increase, v5 reached its 500-turn operational guard with 72
normally completed conversations and 19 backend-error closures. Model accounting:
962 calls, $0.369902385 actual cost and $3.742345800 cumulative reservations.
The service exited normally; no error, pending request or next-turn draft existed.

The reviewed `--max-total-turns` selector retains the default 500, rejects invalid
input before credentials and cannot silently change a frozen manifest. Full
runtime verification passes 126 tests / 73 subtests, including clean guard pause,
refused override, configuration-only migration remaining halted, and explicit
same-run resume without another start or repeated message.

Under the existing continuation authorization, a reviewed one-off migration
selected 1,000 total turns, keeping cap $6, per-conversation limit 30 and policy
v2 unchanged. Dry-run and apply each reproduced all 962 cached model requests,
outcomes and counters, then fresh GET verified the current server history.
Exact reviewed CLI source, complete frozen source coverage, unchanged policy,
start request and failure/close pairing are checked before writes. Old source,
manifest, policy and halted state are archived in private
`migration-before-total-turns-1000/`; enabling the state is the final write.
Post-apply hashes passed, and the same service resumed with the selected limits.
No model or organizer POST was made by migration. No new debug allowance or
official start. Continue monitoring until explicit HTTP428; no remaining pool
size or semantic-quality score is inferred from this checkpoint.

### October 9 budget pause and authorized continuation

Automatic timeout recovery at 0327 succeeded. The same run then reached 403 user
turns, 58 completed conversations and 16 operational closures. It stopped between
the current draft and editor when cumulative reservations reached $2.998644;
actual model cost was $0.293755280 in 775 successful calls. No organizer or model
request is uncertain. Draft 0403 is durable; editor 0403 and organizer 0403 are absent.

The user explicitly authorized increasing budget and continuing until the end.
Select a $6 total reservation ceiling, keeping prompts, model route, recovery
policy and existing turn bounds unchanged. The new `--cap-usd` option validates
finite positive input before credential access, keeps the $3 default, and cannot
silently override a frozen manifest. Explicit migration archives the old
configuration/state/error/source and checks all 775 cached generation requests,
terminal counts, history and the remaining editor reservation. Only the cap and
halted/running state change; no turn is advanced and no saved request is repeated.

Tests cover the real CLI loop with the selected cap, refusal to change a frozen
cap, invalid input before credentials, and a budget pause after draft followed
by same-run completion with one cached draft and one editor. Full runtime:
124 tests / 69 subtests pass. Focused optimized checks: 39 tests / 19 subtests pass.
Dry-run migration reproduced all 775 model requests and a fresh GET matched the
server history exactly; no POST. Independent review cleared the corrected
migration: the old state stays halted until new configuration and migration
evidence are durable, with state enablement committed last. The original
manifest, state, error and frozen source are archived privately in
`migration-before-budget-6/`. Post-apply archive/evidence/configuration hashes
passed; only cap 3 -> 6 and halted -> running changed. No outcome count advanced.
Same v5 service restarted with `--cap-usd 6`, preserving draft 0403 for reuse.

### Earlier recovery checkpoints

v5 reached 28 completed conversations and seven verified backend-error closures,
then halted on a response timeout at request 0198. GET session confirms the
request was persisted without its reply, but no final POST response is available.
The pending marker is retained; no blind resend or timeout-driven close occurred.
After repeated exact observations more than 45 minutes later, a reviewed one-off
recovery archived the original pending request and sent one distinct final close.
HTTP200 confirmed advancement; v5 resumed at 200 with 28 completed and 8 skips.
The original message was not resent and no POST response fabricated. This manual
exception remains outside the automatic known-500/502 recovery policy.
Five debug and four official allowances remain. No official Task 2 start.

A second timeout at 0288 was still unanswered after 118 minutes. The same reviewed
procedure, changed only for the index/hash/artifact names, passed offline checks
and a fresh exact-prefix session check. One final close at 0289 returned HTTP200
with a new empty scenario. v5 resumed at 290 with 40 completed and 11 operational
closes; $0.219581060 in 558 model calls at restart. Automatic recovery scope and
the frozen 12-skip bound remain unchanged. No original request resent, no new
allowance and no official Task 2 start.
