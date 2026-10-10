# Paper preparation

Updated October 10, 2026. The objective is a reproducible account of our submitted
TREC UserSim baseline, its development evidence and its limitations. **We have
enough preserved evidence to draft the method and submission account. We do not
yet have official effectiveness results or confirmed paper requirements.**

Both official baselines are complete. No additional experiment or submission is
required by this paper plan. Debug v5 remains intentionally paused.

## What is ready

| Paper material | Canonical evidence | What it supports |
|---|---|---|
| Task and submission contract | [Task 1](../task1_workflow.md), [Task 2](../task2_workflow.md), [organizer guidelines](https://trec.usersim.ai/guidelines) | Next-message prediction versus interactive simulation with a stop decision |
| Data and provenance | [Official-data audit](../research/official-data-evidence.md) | 64 supplied conversation records, 266 researcher targets, 10 goals and 12 distinct profile objects; no stable participant IDs or positive researcher-stop labels |
| Submitted method | [Architecture](../task2_architecture.md), [prompt builders](../../usersim/prompts.py), [Task 1 runner](../task1_runner.md), [Task 2 runner](../task2_debug_runner.md) | Persona/goal projection, full available utterance text, researcher-role mapping, draft and one editor call |
| Exact executed version | Private run manifests, `frozen/`, recovery policy and source-pinned audit tools | Configuration/source hashes actually used; current public code is not necessarily identical to frozen execution |
| Development comparisons | [Method decisions](../research/method-decisions.md), [experiment ledger](../research/experiment-ledger.md), private dated notes and saved model receipts | Tested controls, rejected variants and limited preferences; not independent generalization or causal claims |
| Actual submissions | [Submission ledger](../submission-ledger.md), [machine-readable run index](../../submissions/manifest.json) | Exactly two official runs and seven debug runs, with coverage, receipt costs and status |
| Transport and recovery | [Recovery guide](../research/task2-recovery-plan.md), private receipts/reconciliations and official integrity audits | Completion and request/output integrity; administrative closures separated from natural stops |
| Figures and worked example | [Existing figures](../task2_architecture.md), [illustrative viewer](../examples/run-viewer.html), [private reader instructions](../run_viewer.md) | Architecture diagrams and an explicitly invented example; private real-run inspection without publishing transcripts |
| Preserved evidence | [Private GitHub release and restore](../artifacts.md), [archive index](evidence-manifest.json), [preservation instructions](preservation.md) | Data, runs, notes, historical scripts, source/environment provenance and rendered readers; 7,408 files verified after a fresh download |

The manuscript should use `openai/gpt-6-luna` as the exact requested model ID.
Both official runs used OpenRouter, an OpenAI-only route without provider
fallback, and a 4,096 completion-token cap. Exact requests and provider/model
response metadata remain in the private archive. This is a prompted baseline,
with no fine-tuning. Task 1 official explicitly selected narrow `fidelity`
editing; Task 2 selected `style` editing and retains the draft's stop boolean.
No compaction, retrieval, structured planner or repeated judge/retry loop ran in
the selected baseline. “Full history” means available utterance text, not every
raw input metadata field.

## Submission coverage and cost

These are integration/coverage results, **not quality scores**. The receipt-based
table is also available as [CSV](submission-results.csv).

| Official task | Prediction/session coverage | Model calls | Receipt cost (USD) | Effectiveness |
|---|---|---:|---:|---|
| Task 1 | 62 next-message predictions over 10 goals | 124 | 0.029373225 | Not recorded |
| Task 2 | 57 conversations processed: 49 normal endings, 8 administrative closures; 266 submitted turns | 516 | 0.173554630 | Not recorded |

The two official runs cost **$0.202927855** in reported model usage. This excludes
development/debug runs, hosting and other operational costs. Task 2's eight
administrative closures consist of five backend failures and three timeouts;
they must not count as natural researcher stops. Three other delayed replies
were recovered without resend or closure. The official Task 2 completion proof
required a separately reviewed local terminal reconciliation after the original
parser rejected the organizer's run-ID-bound HTTP428 wording. Frozen execution,
the original failure and the reconciliation are all retained.

Training targets, debug predictions and official cases must remain separate.
There is no validated held-out training split underlying the small repeated
development screens. No whole-run human realism rating is recorded. Code
checks and receipt replay cannot establish that tone, knowledge or stopping
behavior matches real researchers.

## What remains before a final paper

- [ ] Obtain and preserve the official Task 1/Task 2 score reports, metric
  definitions and evaluation version. Add result tables with run IDs and
  evaluation provenance; do not replace them with completion counts.
- [ ] Confirm the 2026 notebook deadline, template, length, submission location
  and later proceedings revision rules from the participant instructions.
- [ ] Supply the author order, affiliations, contact details and acknowledgments.
- [ ] Select the paper's bounded claims and qualitative examples. Real
  participant excerpts require verified publication rights; the current public
  examples are invented and cannot serve as measured human comparisons.
- [ ] If reporting realism preferences quantitatively, document the review
  sample, rubric, reviewer identities/independence, blinding and uncertainty.
  Existing small or unblinded screens should retain those limitations.
- [x] Preserve the evidence off-host in the [private GitHub release](../artifacts.md).
  Fresh download, GitHub asset digests, standalone restore and all 7,408 file
  hashes passed. Credentials remain separate from this research backup.

The [NIST participation guide](https://trec.nist.gov/howto.html) describes a
notebook followed by a proceedings revision, and distinguishes participant-only
early material from later publication. Its generic schedule is **not** a
confirmed 2026 UserSim paper deadline. The [2026 call](https://trec.nist.gov/cfp.html)
and track guidelines were checked October 10; exact paper-format requirements
were not established by those public pages. No email, authenticated participant
page or organizer endpoint was queried for this audit.

In a subsequent October 10 deadline check, the organizers'
[October 7 extension announcement](https://groups.google.com/d/msgid/trec-usersim/1b15da6d-1d40-4124-9698-a89a4ea9e746n%40googlegroups.com)
was read through authorized email access. It sets the **run submission** deadline
to October 9, 2026 (Anywhere on Earth), superseding the public page's October 7.
This corresponds to October 10 at 12:00 UTC / 08:00 Eastern and has passed.
It does not establish the separate notebook-paper deadline. The scoped email
search found no UserSim notebook deadline or template announcement; obtain the
participant instructions before treating a paper date as confirmed.

For conference attendance, [NIST's event page](https://www.nist.gov/news-events/events/2026/11/trec-2026)
lists November 16–18, with in-person registration closing November 2 and virtual
registration closing November 18 at noon. This is separate from both run and
paper submission. No registration or payment was made.

## Writing plan and current status

1. **Done:** reconcile all nine run directories, archive originals byte-for-byte,
   index per-run counts/costs and preserve development evidence.
2. **Ready:** draft the task, data, method, development and integration sections
   following the [outline](outline.md), reusing existing figures.
3. **Pending:** official scores, author metadata, venue instructions, and example
   publication rights. These are explicit gaps rather than guessed content.
4. **Next action:** incorporate organizer evaluation and confirmed notebook
   instructions, then write the paper around the final submitted method.

The first Task 1 debug run lacks per-prediction organizer POST receipts; all
64 input/model request/response records and its final accepted request/HTTP428
are retained. Task 2 debug-v3 has eight priced model receipts while its unchanged
checkpoint counts six calls. The public index and ledger expose both gaps.
Neither affects the reconciled official-run totals.
