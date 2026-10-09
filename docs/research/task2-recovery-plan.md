# Task 2 backend-error recovery plan

## Objective and authorization

User authorizes skipping conversations blocked by HTTP500/502 in the existing debug
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
No recovery for malformed model output, bad response schemas, uncertain in-flight
requests, authentication/quota failures or mismatched server history. No blind
repost. A failed close halts. Maximum 12 automatic skips per invocation policy;
this limit is operational and must not be interpreted as human behavior.

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
Only observed 500/502 are recovered automatically. The official CLI requires
completed debug evidence, an explicit organizer completion receipt and a review
artifact bound to the exact final state before credentials or API access.

Existing v5 started before recovery was enabled, so its organizer description
cannot retroactively disclose skips. The local policy, recovery receipts and
ledger disclose this limitation. Fresh recovery-enabled debug and official run
descriptions disclose operational closures. No generator change.

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
