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

## Current status

Design review requested and still running. Primary code/boundary checks and an
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
only code, synthetic fixtures and aggregate results. Next: advisor disposition,
freeze candidate and run the bounded comparison.
