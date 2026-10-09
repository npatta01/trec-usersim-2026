# Task 2 post-outage debug attempt — October 7, 2026

User authorized checking the organizer update and trying debug again.
Organizer Marcel reports an internal service outage is resolved, quoted in
[the participant reply](https://mail.google.com/mail/u/0/#all/1a115bab4c94d7a5).
The deadline is extended to October 9 AoE. This is an organizer statement,
not yet proof our full debug run will succeed. No safe replay contract for
already-persisted user turns was supplied; both older partial runs are preserved.

Started one fresh debug run `np-labs-luna-task2-debug-20261007-v3` using the
unchanged Task 2 generator and style editor, sequential requests, $3 reservation
cap, and stop-on-error guards. No official run. Preflight: 87 tests and 40
subtests passed. Source commit c6525aa.

Private receipts: `/home/npatta01/data/trec-usersim-runs/task2-debug-luna-20261007-v3/`.
Persistent service: `trec-usersim-task2-debug-20261007-v3.service`.
Status: launched; inspect state and organizer receipts before reporting results.
Do not start another run automatically. Never replay a persisted turn blindly.

First start and continue returned HTTP200; one full exchange confirmed.
Service remains active. This is initial progress, not a completed-run result.

### October 7 status reconciliation

Third Task 2 debug attempt halted on HTTP500 generating the fourth agent reply.
Three successful exchanges; GET debug/session confirms seven messages ending
in the fourth saved researcher message. Zero completed conversations. Service
failed and local state reconciled to halted; no repost or new run. GET budget
confirms Task2 debug7, official4; Task1 debug8, official3. Organizer outage
announcement did not establish resolution for this attempt. Private receipts
include session_status_check.json and budget_status_check.json.

### Client-versus-server audit

Checked all four continue receipts against the saved live OpenAPI schema and
organizer client serializer. Required fields/types and endpoint match; all
four use the same conversation ID, participant user, is_final=false, empty
sources and annotations. Server session text matches every submitted user
message in order, with no duplicate or omitted user turns. Successful text
lengths: 602, 553, 660 characters; failed: 844. Our timestamps include UTC
offset, unlike the reference client's naive timestamps; both conform to the
documented datetime field and our format succeeded on earlier turns.

This rules out the inspected obvious envelope/history errors, not every
client bug or content-triggered server error. HTTP500 alone cannot establish
root cause. Server-side traceback or a controlled organizer-supported replay
is still needed. No additional requests consuming quota were made for this audit.

### Full offline differential replay

Replayed all three saved runs with network transports replaced by saved receipts.
All 13 continue payloads validate against the saved live OpenAPI using JSON Schema
with datetime format checking. Executed the organizer reference client's actual
continue_run serializer against an intercepted transport: all 13 JSON payloads
and endpoint paths equal ours when supplying the same timestamp. This checks
serialization, not just visual similarity; it does not test timestamp behavior
inside the server.

Re-executed our full runner from empty temporary directories: all 26 model
requests match saved requests exactly, and all 16 organizer requests (including
three starts) match saved requests after excluding newly generated timestamps.
The replay reaches the saved HTTP500 in each case. This establishes deterministic
request/history construction and guards against missing or duplicated local
turns; replay of saved failures is not independent server reproduction.
Aggregate audit: private v3/client-audit.json. Audit script: /tmp/audit_task2_client.py.
No live POST, model call, or debug quota consumed. Remaining possibilities include
content-triggered backend failure, undocumented server constraints, timestamp or
header sensitivity, and a continuing backend outage. Server traceback remains
necessary to identify which.
