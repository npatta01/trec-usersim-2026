# Task 2 debug handoff — October 6, 2026

## Authorization and selected behavior

The user explicitly authorized one Task 2 debug run. No official submission.
Use the existing Luna full-history generator with structured text/is_final,
researcher role mapping, and default-on style editor preserving the stop decision.
No experimental prompt treatment, compaction, or stronger-model substitution.
Model cost reservation cap: $3. Operational limits halt rather than inventing a user stop.

## Current result

**Halted on organizer HTTP500, not completed.** One debug run was started.
The server accepted four researcher messages and returned three assistant
replies in the first conversation. It saved the fourth user message, then failed
while generating its assistant reply. Two read-only `/debug/session` checks
confirmed seven alternating messages ending with that exact submitted user
message; there was no delayed assistant reply. No request was resent.

- Complete conversations: **0**. No whole-conversation or stopping validation.
- Model calls: **8** (four drafts and four edits), all successful.
- Actual model cost: **$0.00424824**; reservation **$0.0336925** under $3.
- Remaining Task2 debug allowance: **9**. Task1 debug9; official4 per task.
- Persistent service is stopped/failed. `state.json` is explicitly halted.
- `recovery.json`, both session snapshots and the original HTTP500 receipt
  preserve the reconciliation. Original local state is separately backed up.

**Next action:** obtain a supported organizer recovery for the existing partial
turn. OpenAPI exposes debug start/continue/session but no retry-agent or rollback
endpoint. Reposting the user message risks duplication; starting another debug
run spends another allowance and is not recovery. Do neither automatically. Independent recovery review confirmed this conclusion.
An [organizer support draft](task2-debug-recovery-request.md) is prepared but not sent.

## Preflight and implementation

Authenticated read-only checks returned HTTP200 for team NP Labs.
Before this run: Task2 debug10, Task1 debug9, official4 for each task.
Live OpenAPI was also inspected: unlike the Markdown workflow’s full
`chat_messages` example, its Task2 response schema exposes one nullable
`utterance`. The adapter must support both shapes without duplicating history.
The schema snapshot is saved privately alongside the quota evidence.

Live adapter implementation is complete: 137 script tests passed, including
25 new protocol/recovery tests; those 25 also pass under optimized Python.
Independent review found an inner conversation-ID validation gap; it was fixed
and regression-tested. Independent review cleared launch. The persistent user service
`trec-usersim-task2-debug-luna.service` stopped on the server failure above.
Read `recovery.json`, `error.json`, and both organizer/model checkpoint folders
before recovery. No unresolved model call exists.

Run ID: `np-labs-luna-task2-debug-20261006-v1`.
Private receipts: `data/official/task2-debug-luna/` (ignored).
Credential locations only: `~/.config/trec-usersim/organizer.key` and
`~/.config/trec-usersim/openrouter.key`; never copy values into artifacts.

## Recovery

Never start another run to recover this one. Preserve requests, timestamps,
responses and in-flight markers. Uncertain organizer/model requests require
reconciliation before resuming; do not retry automatically. Debug sessions are
not reliably exposed by official run-status endpoints. Explicit completion text
with HTTP428 is required; transport/server failures are not completion.

## Limited behavior inspection

All four generated messages speak as the researcher and track the same-community
requirement. They increasingly request substantiation after detailed assistant
recommendations. However, some wording remains more expert/polished than this
scenario’s unfamiliar, conversational-English persona; one message introduces
specific prior knowledge not supplied in the persona. This is selective inspection
of one incomplete conversation, not a pass rate or evidence of general quality.
No prompt change is made from this partial live example.


## Mailing-list evidence checked October 6

The user requested checking email/Google Groups. Gmail contains the Google
Groups discussion copies. A September 30 organizer reply says server timeouts
were increased, advises sufficient client timeouts, and asks the affected team
to retry; the participant then confirmed completion. That concerned HTTP504,
not a documented recovery for an already-persisted user turn after HTTP500.
A newer October 3 report (October 4 in the sender timezone) reports Task2
HTTP500/502/503 and asks about duplicate turns. No reply to that report was
found in the searched mailbox. Direct Google Groups web access was unavailable,
so this is not proof that the forum has no newer reply.

Sources: [organizer timeout reply](https://groups.google.com/d/msgid/trec-usersim/643ba063-a9b1-48b6-8a6e-499805d514bfn%40googlegroups.com),
[newer error report](https://groups.google.com/d/msgid/trec-usersim/CAP4uEZYAudxFMmDTWNXYAdHq%2BFB6t9Gk34N_82qa7jxpRUasMw%40mail.gmail.com).
Both were read through their email copies; no email or forum post was sent.
The evidence supports reporting our affected run rather than blindly replaying
the persisted message.
