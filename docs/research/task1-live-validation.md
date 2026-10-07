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


### Recovery verification

Commit `2fd6cad` corrects only next-target validation. All 74 tests pass normally
and under optimized Python, and independent review found no blocker. The original
run manifest and source snapshots are preserved under its private
`recovery/001-http200-next-target/` directory with receipt hashes. Configuration,
model requests, and previously accepted predictions are unchanged. The same run
resumed from the cached response; a read-only quota check confirmed Task 1 debug
8 and official 4 remaining. This consumes only the single authorized debug run.


### Debug outcome and submission decision

The organizer accepted **64 predictions** across **10 goals** (21 openings,
43 follow-ups). The final HTTP428 explicitly said no more open goals remained
for this run and that the run was finished. All 128 draft/editor calls returned
nonempty text with `finish_reason=stop` through the selected OpenAI provider.
Actual model cost: **$0.0376755**; 16 of 64 drafts changed during editing.
The longest draft input was 5,286 tokens; maximum supplied history was 8 messages.
Every saved context, model request, chosen output and organizer payload matched
in the local audit. No uncertain request remains.

The exact completion response included a run-specific explanatory sentence that
the conservative parser did not yet accept. The receipt is definitive evidence;
completion is reconciled locally without another organizer or model request.

**Do not start official submission yet.** Contextual review found two substantive
fidelity concerns, both already present in drafts and retained by the style editor:
- Case 0027 explicitly makes requested vendor metadata optional. Location/country
  requirements remain intact; the concern is the vendor requirement alone.
- Case 0036 speaks as if the researcher checked for reliable external evidence,
  although no such check is present in the supplied history. Its broader skepticism
  is plausible given the moderately familiar persona and known datasets.

These are qualitative reviewer judgments, not official scores or proof of the
unique human response. Some other replies are more polished than observed speech.
The current style-only editor cannot be counted on to correct content problems.
A targeted follow-up should test preserving explicitly stated requirements and
avoiding claims of unobserved checks, using the same cases plus successful controls.
Do not silently change the frozen generation prompt within this debug run.

Remaining allowances after this run: Task 1 debug **8**, official **4**;
Task 2 debug **9**, official **4**. No official submission was started.


### Final local verification

Commit `89adde7` accepts the exact observed completion template only when it
names the current run. Wrong IDs, negative prefixes, suffixes and extra fields
are rejected. Task 2 parsing is unchanged. All **75 tests** pass normally and
under optimized Python; independent review found no actionable issue.
A copy of all 64 receipts replayed to completion with both transports forbidden,
then the actual run was reconciled the same way: **zero additional API calls**.
The second original source manifest is preserved under
`recovery/002-completion-template/` with receipt hashes; `result.json` now records
64 submitted predictions, 128 model calls, $0.0376755 actual spend and $0.4083422
reserved upper bound. The reservation is not an additional charge.

All 64 cases received contextual review. Primary adjudication: **55 acceptable,
7 minor concerns, 2 substantive concerns**. Minor concerns include polished voice,
recap and a low-impact inferred situation. No material editor reversal was found.
These judgments are not an official metric or a human-ground-truth pass rate.
Private per-case reports and the consolidated review remain outside git.


### Narrow repair and official run (recovery in progress)

The [editor-repair study](task1-fidelity-fix.md) tested two candidates, rejected
broad goal enforcement and selected a narrow action-provenance clarification.
This supersedes the earlier categorical judgment of the vendor compromise: it
can be a plausible human adjustment. Some voice concerns remain; the study
documents reviewer disagreement and an uncorrected synthetic requirement waiver.

After 83 passing offline tests, the 64-case zero-network integration replay and
contextual regression review, the user's conditional single official run started:
`np-labs-luna-fidelity-task1-official-20261006-v1`. Source commit `6a69e2a`, explicit
`--mode official --editor-policy fidelity`, $1 reservation cap. Private artifacts:
`/home/npatta01/data/trec-usersim-runs/task1-official-fidelity-20261006-v1`.

This is a new official run, not a resubmission of debug predictions. Each fresh
organizer prefix receives the frozen draft-plus-editor policy; no official output
is used to retune it mid-run. Task2 remains halted and untouched.


The official run accepted 30 predictions, then safely stopped when the next
HTTP200 target contained one researcher message and no assistant reply. The
client incorrectly required every nonempty prefix to end with the search
assistant. No draft was generated for target 31 and no request is uncertain.
Read-only `/run/status` confirms the same active target, and `/run/session`
confirms the same researcher-only history. Budget: Task 1 debug 8/official 3;
Task 2 debug 9/official 4. No new run is needed.

The [official Task1 definition](https://trec.usersim.ai/guidelines) and bundled
workflow describe a partial conversation without requiring an assistant-ending
prefix. Independent source review therefore identifies a client assumption,
not proof of a malformed organizer target. The bundled parser also tolerates
histories with no assistant, though its empty-message fallback is not copied.
Mailing-list email searches found no matching explanation of this boundary case.

Recovery plan: preserve all supplied speakers/text and continue as the researcher
without inventing an intervening assistant turn. Existing empty/assistant-ending
requests must remain byte-identical. Test synthetic boundaries and provider
acceptance; replay 30 cached submissions to the first unseen model request with
organizer writes forbidden. Archive the original frozen manifest/sources and
receipt hashes before any reviewed source amendment. This is content-agnostic
schema recovery, not prompt selection based on official model outputs. The
intended reason for a researcher-ending prefix remains undocumented.


The boundary repair now passes 87 offline tests (normal and optimized), including
request parity for earlier input shapes, full speaker/order preservation and a
Task1 transition into a researcher-ending target. Two newly synthetic real-provider
examples generated researcher continuations without inventing an assistant reply;
four draft/editor calls cost $0.0005505 (reserved $0.0110674). This is a protocol
smoke test, not an official-content quality experiment. A copied-checkpoint replay
reached exactly the first unseen model request after all 30 cached submissions and
verified all 60 prior model payloads unchanged, with zero live calls.
