# Task 2 second debug attempt — October 6, 2026

> Historical second debug attempt. Current completion and paused-debug state
> are in the [handoff](../project-handoff.md) and [submission ledger](../submission-ledger.md).
> This record does not authorize retrying or starting another run.

## Authorization and decision

The user authorized one fresh debug run if the existing conversation could not
be safely continued. Live OpenAPI still exposes start/continue/session, but no
reply-only retry or rollback. ContinueRequest requires both run_id and a new
user_utterance. The old session still contains four user messages and three agent
replies, ending with our already-saved message. This does not establish that
reposting is idempotent. No POST was made to the old run.

Run: `np-labs-luna-task2-debug-20261006-v2`.
Frozen source checkout at `af57368`, same Task 2 Luna/full-history/stop-decision
and style-editor behavior; no compaction or prompt experiment. One sequential
conversation, 180-second HTTP timeout, $3 reservation ceiling. All 87 offline
tests passed before launch. No official Task 2 submission was authorized or made.

## Verified result

**Halted again on organizer HTTP500.** Four continue calls returned HTTP200.
The fifth returned an internal error while generating the agent response.
The submitted fifth message had `is_final=false`. Two read-only session checks
confirmed five saved researcher messages and four assistant replies, ending with
that exact fifth message. Complete conversations: **0**. Nothing was resent.

All 10 model calls succeeded: five drafts and five edits. Actual cost
**$0.00512328**; reserved upper bound **$0.0430428**, not an additional charge.
The state has been explicitly reconciled to halted; original state, error,
request/response receipts and both session reads remain private.

Submission timestamps were spaced 14.75, 20.45, 24.64 and 18.65 seconds apart.
Requests were sequential, roughly 0.05 per second. The error was 500, not 429;
there is no observed evidence that a high client request rate caused it.
This does not diagnose the server's internal failure or rule out backend load.
Adding an arbitrary delay cannot be claimed to fix it.

Remaining allowances confirmed after this attempt: Task 1 debug 8/official 3;
Task 2 debug 8/official 4. Exactly one fresh debug allowance was consumed.
No further run will be started automatically.

## Private evidence and recovery

Artifacts:
`/home/npatta01/data/trec-usersim-runs/task2-debug-luna-20261006-v2/`.
Key files: `state.json`, `state_before_reconciliation.json`, `recovery.json`,
`error.json`, `manifest.json`, `frozen/`, `model/`, `organizer/`,
`session_after_500.json`, `session_after_500_recheck.json`, and
`budget_after_500.json`.

The old run remains intact in its original directory. Neither partial
conversation has an available assistant response to continue from. An organizer
repair or confirmed idempotent retry procedure could allow same-run continuation;
the API contract alone does not establish one. The next action is organizer
recovery guidance, not another blind retry or another debug allowance.
See the [updated unsent support draft](task2-debug-recovery-request.md).
