# Task 1 validation and conditional submission — October 6

## Authorization and scope

User requested local/debug testing and, if the results look right, an official
Task 1 submission. This supersedes the older debug-only restriction for this
specific sequence. Use the selected Luna + one style-editor default. One new
debug run, then at most one official run if the quality review passes. Existing
completed debug runs and the halted Task 2 run remain untouched.

Model budget: $1 reservation cap per run, existing OpenAI-only routing and
owner-only credential files. Never log credentials or commit private outputs.

## Initial evidence

Read-only organizer checks returned HTTP200 for NP Labs. Remaining allowances:
Task 1 debug 9, official 4; Task 2 debug 9, official 4. Official team summary is
empty. Earlier Task 1 debug completed 64 predictions with draft-only prompting;
it does not verify the selected editor-enabled integration.

## Acceptance checks before official start

1. Offline lifecycle, routing, context replacement, checkpoint replay, strict
   completion and cost-cap tests pass, with independent runner review.
2. The debug run completes with explicit organizer confirmation; all supplied
   contexts and exact requests/outputs are preserved locally.
3. Review outputs against their actual requests: correct speaker, latest-reply
   relevance, persona/observed-voice fit, continuity of constraints/objections,
   no invented actions or expertise, and no material meaning damage from editing.
   Include opening/early/late and longest inputs. Report weaknesses honestly;
   lexical matching or conciseness is not the quality metric.
4. Proceed only if no unresolved integration errors or recurring material
   researcher-fidelity failures emerge. Do not claim this is a held-out score.

## Status

One shared runner now supports explicit debug/official modes. All 74 offline tests
pass normally and under optimized Python. All 64 prior debug inputs reproduce
exact draft requests; a full injected-transport replay completed 64 cases and 128
stubbed model stages with no calls or spend (hypothetical reservation $0.408231).
The editor stub returns the draft unchanged: this is integration evidence, not a
new quality result. Independent pre-live review found and verified fixes for stale targets and missing
history. No code blockers remain. The latest code also passed the 64-case replay.

Planned new IDs and private artifact directories:
- `np-labs-luna-style-task1-debug-20261006-v1`:
  `/home/npatta01/data/trec-usersim-runs/task1-debug-style-20261006-v1`
- Conditional official: `np-labs-luna-style-task1-official-20261006-v1`:
  `/home/npatta01/data/trec-usersim-runs/task1-official-style-20261006-v1`

The new debug run started and accepted its first prediction. Its HTTP200 reply
contained a different conversation ID and an eight-message history. A client
validation guard incorrectly assumed that only HTTP201 could change conversation
IDs, so execution stopped after saving the successful response. No request is
uncertain and no pending marker remains. This was a client assumption bug.

The corrected guard accepts both success statuses without inferring conversation
identity, while rejecting an unchanged semantic target. A private copy of the
actual receipts replayed through the first accepted case with **zero organizer
POSTs**, then reached exactly the model request for the returned next target.
Recovery preserves the original source manifest and snapshots with an audit
record, then resumes the same run ID; it does not start another debug allowance
or resend the accepted prediction. Contextual quality review remains pending.
