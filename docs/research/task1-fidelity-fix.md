# Task 1 fidelity repair — October 6

## Objective and scope

User asked to fix the two concerns found during the completed 64-target Task 1
debug run, while preserving a generic simulator and plausible researcher voice.
The target is an acceptable baseline, not exact reconstruction of a unique human
answer. Prior conditional official-submission authorization remains in effect;
no organizer call is needed to test the repair. Task 2 and historical runs stay
frozen. Candidate inference uses the existing authorized Luna/OpenAI route with a
$1 reservation ceiling for this comparison.

## Evidence and hypothesis

The style-only editor is told to preserve the draft's substance. The two flagged
drafts pass through unchanged: one makes requested vendor metadata optional;
the other implies that the researcher searched for evidence without a supplied
record of that action. Broader skepticism is plausible for the second persona.
The judgments are not unquestionable ground truth: real people may compromise,
and 'cannot find evidence' may ambiguously refer to the current answer.

Hypothesis: authorize minimal content repairs within the existing second call,
while preserving supported changes of mind, performed actions, knowledge, tone,
and useful detail. Do not make every researcher skeptical or enforce initial
requirements after the researcher explicitly changes them.

## Frozen comparison plan

1. Advisor reviews the hypothesis, labels and design using public-shareable source
   and synthetic analogs, without participant transcripts or private outputs.
2. Add an explicit editor policy. Existing shared default stays `style`; test a
   `fidelity` candidate without changing Task 2 or historical fixtures.
3. Apply the candidate to the same 64 saved drafts. Reuse the saved old editor
   outputs as paired controls. No future turns, ratings, evaluation annotations,
   or reference answers enter candidate prompts. No new draft generation in this
   comparison; it isolates editing and does not establish fresh-draft reliability.
4. Test synthetic counterexamples: supported actions, explicit relaxed needs,
   reasonable acceptance, detailed voice, opening context, and unsupported claims.
5. Mask A/B order for contextual review. Check target repair, new substantive
   errors, voice and intent preservation. Disclose prior case familiarity; this
   is development evidence, not a blind held-out score. Record unchanged outputs
   rather than manufacturing a win. No automatic lexical quality metric.
6. Promote only if the two concerns are addressed without material regressions
   on controls. Wire the tested policy into Task 1 with an explicit legacy option,
   config/source freezing and integration tests. Independent code/results review.

## V1 launch record (superseded below)

Design review was requested and still running at launch. Primary code/boundary checks and an
independent harness audit passed. To avoid blocking a cheap reversible comparison,
the frozen candidate test starts while panel advice is pending; panel disposition
is required before promotion. Current Task 1 default and completed debug artifacts
remain unchanged. No organizer calls are part of this test.

The comparison makes 80 calls: 64 candidate edits of saved official debug drafts
and eight synthetic style/fidelity pairs. Reservation estimate $0.2616346; cap $1.
Candidate prompt SHA-256:
`da1f38f68c9f14d0399e7607d49e608e95a5115e16a957b8435d5e472751badc`.

## Verification and next action

Record source/request/output hashes and actual/reserved cost privately. Commit
only code, synthetic fixtures and aggregate results. The exact inputs and outputs remain outside git; the decision and results follow below.


## Advisor critique (standard panel)

All four selected lanes answered the same frozen, source-grounded question:
GPT-6 Sol, GPT-6 Astra (Codex subscription), Opus (Claude subscription), and
Gemini 3.8 Flash High (Antigravity account OAuth; CLI does not report billing tier).
No API-key billing environment was used. Packet contained source and newly
synthetic analogs, not participant transcripts/private outputs. Data class was
unspecified (`unknown` in runner metadata), provider data use reported `none`,
and training use was not permitted. No OpenCode lanes were requested; their
cleanup is not applicable. Private result: `/tmp/trec-fidelity-panel.json`.

All support testing a narrow editor exception, not a broad correctness rewrite.
They challenge treating both original labels as certain defects: a new compromise
can be a realistic human choice, and lack-of-evidence wording can express doubt
rather than a literal search. Opus especially recommends leaving genuine
concessions to the researcher and restricting repair to grounding; Sol/Astra/Gemini
allow minimally clarifying a new tradeoff rather than silently settling it.

Disposition: retain subjective-label uncertainty. Test explicit performed-action
provenance and current-needs consistency, but do not reward rigidity, reinstating
obsolete needs, checklist expansion, or blanket skepticism. The initial candidate
is broader than the narrowest advice; review its collateral edits before promotion.
Opus recommends contemporaneous controls/repeats; add bounded targeted repeats
if the initial effect is marginal rather than making causal claims from one sample.
The original 64-case test is development evidence, not an official realism score.


## Second candidate, frozen before inference

The first candidate completed 80 model calls for $0.0289408, with no organizer
calls. Independent masked review found new requirement hardening, including
optional preferences becoming mandatory. It is rejected for promotion.

The second candidate keeps the original voice-editing contract with one narrow
exception: repair unsupported claims of already performed researcher actions.
It explicitly preserves optionality, new compromises, ordinary expertise and
skepticism. It does not try to force the vendor-metadata concession back into a
hard requirement; panel review found that judgment ambiguous and human flexibility
legitimate. This corrects our earlier overconfident failure label.

Repeat the same 64 fixed-draft cases and 8 synthetic pairs, with the same provider
and request settings. Review all changed outputs for regressions, retaining full
context. Targeted repetitions follow only if justified; cumulative reservations
for both comparisons and repetitions must remain below $1. No official run starts
until code and outputs pass review. Task1/Task2 defaults remain unchanged for now.

V2 prompt SHA-256, frozen in the private run manifest before its first call:
`a292b91e800c9a9171f078d612aa93bd9722ab3aa3306df043c487a842844789`.
The policy also permits local clarification of ambiguous lack-of-evidence wording,
while preserving doubt. Static review flagged this as broader than an unequivocal
action-claim trigger; actual edits to legitimate skepticism must be reviewed.


## V2 results and bounded repeat checks

V2 completed all 64 saved drafts and eight synthetic pairs: 80 model calls,
$0.024235825 actual cost, $0.2649178 reserved. Only five outputs differ from their
drafts; 17 differ from the historical style-editor outputs. Difference alone is
not improvement. The original goal/persona/history is unchanged in both requests.

The questionable search wording now locates the doubt in the supplied information,
without claiming an external search and without deleting the researcher's specific
criticisms. The vendor-metadata concession remains: the panel judged that a new
compromise can be legitimate after the assistant fails to find a complete source.
This is a correction to our earlier overly certain label, not a claimed repair.

Eight [newly synthetic probes](../../tests/fixtures/task1_editor_probes.json)
exercise invented versus supported checks, explicit relaxed needs, acceptance,
ordinary knowledge, detailed voice, opening context and a flat requirement waiver.
V2 repairs the invented check and leaves the other seven replies unchanged. It
**does not repair the flat waiver probe**: general requirement enforcement is not
part of this narrower policy. That remains a limitation, not an eight-of-eight
success claim. Do not apply a lexical pass metric or demand immutable goals.

Two additional repetitions each of the real ambiguous-evidence case, the clear
invented-check probe and the supported-check control compared fresh style/fidelity
outputs on identical frozen drafts. All four targeted new-policy edits removed
the unsupported implication; all four old-policy edits retained it. Both policies
preserved the supported check in both repetitions. Twelve calls cost $0.00220442,
reserved $0.0371258. These are selected development repetitions, not six new cases
or a held-out human-realism score.

Total repair-study spend (both candidates and repeats): **$0.055381045** across
172 model calls. Combined reservation **$0.5636782**, within the $1 study ceiling;
reservation is an upper bound, not an additional charge. No organizer requests
were made by these experiments.

## Integration verification

Task1 exposes explicit `--editor-policy fidelity`; the compatibility default is
`style`, and Task2 remains unchanged. The selected policy is frozen into run
configuration/source snapshots. Conflicting `fidelity --no-style-postedit` is
rejected before credentials or transports, following independent review.

All 83 offline tests pass normally and under optimized Python (40 subtests).
A separate injected-transport replay traverses every one of the 64 saved organizer
targets: exact parity for 64 draft and 64 editor payloads, 64 selected/submitted
texts, and independent prefix replacement. It completes via the run-specific 428
message with zero live calls. This verifies integration, not fresh generation.

Private artifacts reside in the `task1-fidelity-editor-20261006-v1`, `-v2` and
`-v2-repeats` directories under the existing private run root. Source snapshots,
inputs, request hashes, model receipts, reviews and costs are retained there.
The public fixture is newly synthetic and includes the original review checks;
the required-metadata check remains unmet by V2 as disclosed above.


## Final review and decision

All 64 real cases were covered: 48 received independent order-masked contextual
review; primary reviewed changed outputs in the remaining 16 with full context
and carried forward the earlier judgments for identical outputs. All eight
synthetic probes were independently reviewed. Reviewers found **no newly
introduced material harm from V2**. This is not a claim that every reply perfectly
matches the human's voice; polished phrasing and expert-sounding skepticism can
remain. The strongest measured gain is the narrow provenance clarification.

There is reviewer disagreement on goal fidelity. One reviewer calls an opening
with 'ideally' before species/date/location a substantive softening (case 0049).
Primary judges it a low-impact ambiguity: the opening still explicitly requests
all three, and does not accept dateless records. Likewise, cases 0023–0025 express
preferences without rejecting the underlying need. A goal description does not
provide a unique human wording or an immutable priority ordering. The synthetic
flat requirement-waiver failure remains documented rather than relabeled a pass.

Decision: use V2 as the narrow provenance-repair baseline, selected explicitly
with `--editor-policy fidelity`; reject V1. The debug integration, offline replay,
83 tests and contextual checks meet the user's baseline submission condition,
with the above limitations. No second debug allowance is needed for fixed-input
editor evaluation. Before live start, read-only checks confirmed NP Labs, Task 1
debug 8/official 4, Task 2 debug 9/official 4 and an empty official summary.

Selected single official run (now complete; do not restart): `np-labs-luna-fidelity-task1-official-20261006-v1`.
It retains the same model, provider controls and full-context draft prompt. Only
the second call uses the tested narrow policy. Cap $1; checkpointed, no automatic
retries after uncertain effects. No Task2 recovery or submission is authorized by
this decision.


The authorized official run subsequently completed 62 predictions for $0.029373225.
A generic input-boundary repair was required for a researcher-ending prefix;
87 tests, synthetic provider checks and cached-request replay verified it before
same-run recovery. [Official outcome and provenance](task1-live-validation.md).
No official outputs were used to select another prompt variant.
