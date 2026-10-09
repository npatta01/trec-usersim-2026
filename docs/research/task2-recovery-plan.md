# Task 2 backend-error recovery plan

## Objective and authorization

User authorizes recovering conversations blocked by backend failures in the existing debug
run, then trying one official Task 2 run if debug verifies this procedure.
Same Luna generator, full history and editor; recovery is a transport policy,
not a researcher behavior. Existing $3 model-reservation ceiling remains.
No new debug allowance is required to resume v5. No external message is sent.

## Design

Recovery reads persisted failed request and current server session before writes.
For 500/502, if the exact failed user message is persisted after the exact
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
server history. No blind repost. A failed close halts. Policy v2 permits at most
24 operational skips, at most 25% of terminal conversations, and at most three
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
handles saved 500/502 and classified original ReadTimeouts. The official CLI requires
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

## Latest live evidence

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
