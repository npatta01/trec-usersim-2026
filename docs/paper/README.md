# Paper preparation

Updated November 7, 2026. The paper is for fellow UserSim participants and now
includes only the submitted system, a recorded conversation flow and preliminary
organizer results. Development experiments and detailed evidence inventories stay
in repository notes, outside the manuscript. Author details are complete; venue format, page-limit and submission-route
confirmation remain open. The final manuscript is [usersim2026.pdf](usersim2026.pdf).

Current layout: task explanation on page 1, submitted method on page 2,
organizer results on page 3, aligned conversation excerpts on page 4, and discussion
with references on page 5.

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
| Figures and real examples | [Excerpt provenance](real-examples.json), [figure sources](figures/README.md), [private reader instructions](../run_viewer.md) | Two own-model submitted replies with organizer ratings, a pipeline overview and human-reference result comparison |
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

Coverage and cost describe integration, not quality. The effectiveness column
reports the separate preliminary organizer evaluation; coverage/cost fields are
also available as [CSV](submission-results.csv).

| Official task | Prediction/session coverage | Model calls | Receipt cost (USD) | Effectiveness |
|---|---|---:|---:|---|
| Task 1 | 62 next-message predictions over 10 goals | 124 | 0.029373225 | Preliminary JSD 0.106; human-likeness 2.38/4 |
| Task 2 | 57 conversations processed: 49 normal endings, 8 administrative closures; 266 submitted turns | 516 | 0.173554630 | Preliminary JSD 0.158; human-likeness 2.31/4 |

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

- [x] Download the preliminary Task 1/Task 2 results, preserve the original ZIP
  locally and add scores, metric definitions and sample sizes to the paper.
  [Result notes](organizer-results-2026-11-07.md) record the November 4 release.
- [ ] Preserve this new result archive in a dated private off-host release;
  the earlier evidence release does not contain it.
- [ ] Confirm the 2026 notebook deadline, template, length, submission location
  and later proceedings revision rules from the participant instructions.
- [ ] Supply the author order, affiliations, contact details and acknowledgments.
- [ ] Select the paper's bounded claims and qualitative examples. Real
  participant excerpts require verified publication rights; the current public
  examples are invented and cannot serve as measured human comparisons.
- [ ] If reporting realism preferences quantitatively, document the review
  sample, rubric, reviewer identities/independence, blinding and uncertainty.
  Existing small or unblinded screens should retain those limitations.
- [x] Preserve the evidence off-host in the [GitHub release](../artifacts.md).
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
2. **Drafted:** task, data, method, selected development checks, submission
   accounting and limitations in [the manuscript](usersim2026-draft.tex).
3. **Incorporated:** preliminary organizer scores and human-reference comparison.
4. **Pending:** author metadata and confirmed notebook instructions; preserve
   preliminary status until final organizer evaluation. Real examples remain
   excluded without verified publication rights.

The first Task 1 debug run lacks per-prediction organizer POST receipts; all
64 input/model request/response records and its final accepted request/HTTP428
are retained. Task 2 debug-v3 has eight priced model receipts while its unchanged
checkpoint counts six calls. The public index and ledger expose both gaps.
Neither affects the reconciled official-run totals.

## Local manuscript — October 10, 2026

- Objective: an approachable, evidence-bounded notebook draft of the submitted
  baseline. Scope excludes new live experiments and submissions.
- Source: [usersim2026-draft.tex](usersim2026-draft.tex); local PDF:
  [usersim2026-draft.pdf](usersim2026-draft.pdf) (5 pages, no appendices; references at the end). Rebuild from this directory with
  `latexmk -xelatex -interaction=nonstopmode -halt-on-error -outdir=build usersim2026-draft.tex`.
- Style: short paragraphs and concrete explanations, an architecture overview,
  two actual submitted replies with contrasting ratings, and a result comparison.
- Format: provisional 11-point US Letter article, not an organizer template.
- [Venue check and claim map](draft-evidence.md) records sources and open gaps.
- Preliminary scores are included. Author details, acknowledgments, exact
  deadline, template, length and submission location remain pending.
  No participant excerpts are used.

### Visual revision — historical October 10 draft

Replaced the dense first layout after user feedback. The first three pages now
explain tasks, a five-turn sample conversation and editing through figures. Larger
11-point text and more paragraph spacing improve reading; detailed development
comparisons and provenance remain in appendices. The figures are deterministic
TikZ sources under `figures/`, not generated photographs or participant records.
All conversation text and illustrative draft/editor outputs are invented.

### Section audit and figure redesign

The October 10 section audit used five sections: submitted approach, method/development choices, diagnostic conversation,
submission evidence, and limitations/conclusion. Merged repeated stopping and
input discussions into the method; moved recovery and provider details into
provenance. Kept detailed development checks in the appendix.

The architecture now uses an illustrated overview (`figures/architecture-overview.png`)
generated with the built-in image tool from public method facts. The conversation
is an editorial timeline with a decision column, and the editor figure shows
supported versus unsupported action claims. [Figure provenance](figures/README.md)
records assets and prompts. No private transcript was sent to image generation.

### Audience correction: participating teams

The notebook is for fellow UserSim participants. Assume task/API familiarity.
The main narrative now leads with our submitted configuration and policy scope,
then selection evidence and unresolved failures. Removed elementary task exposition;
the constructed conversation is now a diagnostic of acceptance versus completed
verification, rather than an introduction to conversational search.
The main comparison table reports selection evidence with explicit sample and
confounding boundaries, not an ablation or official score claim.

## November 7 preliminary results update

Organizer results are now downloaded and incorporated in the manuscript. See [result interpretation](organizer-results-2026-11-07.md) for metrics, rated sample sizes, provenance and limitations. Earlier pending-score statements are historical. Paper format and author metadata remain unresolved. Debug v5 stays paused.

### Results visual and readability revision

Added a two-panel comparison with humans: reply lengths for both tasks and Task 2 user turns. Results now lead with three short interpretations; the compact table retains JSD, ratings and sample sizes. Detailed rating counts and run accounting moved to an evaluation appendix. No new organizer or model calls.

### Whole-paper readability revision — before annotation feedback

Current structure: (1) submitted simulator, (2) development lessons, (3) preliminary
organizer evaluation. Keep all four explanatory visuals. The main text now gives
the editing boundary, the reason broader goal enforcement was rejected, the
limits of partial-pipeline comparisons, and the remaining verbosity/stopping gap.
Provider settings, exact run IDs, sample sizes and development controls are in
two concise appendices. Hashes, transport-recovery chronology and archive counts
remain in the repository evidence notes rather than the manuscript.

The previous manuscript and figures are recoverable in ignored
`build/before-whole-paper-readability/`. The final PDF retains 11-point type;
reduction comes from removing repeated details, not shrinking the text.

### Current annotated revision — November 7

Three main sections: how the simulator works, two replies from the official run,
and preliminary organizer evaluation. Five pages with the same 11-point type.
The two invented heat-data figures are no longer included. New Figure 2 quotes
two non-identifying simulator-generated requests in full: 568 characters rated
0/4 and 148 characters rated 4/4, both returned unchanged by the style editor.
The examples were selected to contrast ratings within the same broad NER topic;
they are not a controlled test of length. No human participant message, profile,
raw annotator reason or session identifier is quoted. The user expressly asked
for a real good/bad example. Exact text, hashes and ratings are in
[real-examples.json](real-examples.json); private locators remain beside the
original organizer ZIP. Both quotes were checked against draft, edit, accepted
POST payload and evaluation records. The abstract is split into two paragraphs,
and GPT-6 Luna has a verified official model-documentation reference.

### Current scope — submitted system only

The latest user annotations supersede the earlier development-focused brief.
The paper now contains three sections: submitted system, a conversation from the
official run, and preliminary organizer results. Both appendices and all
unsubmitted variants have been removed. Previous drafts remain under ignored
`build/before-submitted-only-review/`; research evidence remains canonical in
the existing method-decision and preservation notes.

Figure 1 is a vector control-flow diagram showing shared context, edited text
and the Task 2 stop decision copied from the draft. Figure 2 follows the same
real conversation as earlier excerpt B: opening, summarized assistant reply,
verbatim researcher follow-up, marked omitted exchanges, summarized assistant
reply, and verbatim stop message. Public excerpt provenance is in
`real-conversation-flow.json`; private IDs and source records remain off git.
Figure 3 explicitly labels human conversations as organizer-reported means.
The result ZIP includes annotations for our own runs and human aggregate means,
not the held-out human reply texts. Human training logs were supplied separately.

### Current paired conversations and custom overview

The manuscript now includes both a highly rated recorded flow and a poorly rated
recorded exchange from the submitted Task 2 run. The latter has 568- and
509-character simulator replies rated 0/4 and 1/4, both unchanged by the editor.
Its analysis concerns human-likeness and presentation, not a verified factual
failure. Different personas/histories prevent a causal length comparison.
Speaker labels now have vector icons. Figure 1 uses a custom built-in-generated
illustration, with exact prompt and provenance under figures/. Only public method
facts were sent to image generation. Exact quote provenance is in
`real-bad-conversation-flow.json`; source records and private locators stay with
the evaluation archive. Previous PDF is recoverable under ignored
`build/before-bad-conversation/`. No new experiment or submission is included.

### Inline contrast for readers

The poorly rated exchange now has numbered highlights and margin callouts:
(1) introductory sentences before the request, (2) submitted Markdown markers
flagged by the annotator, (3) licensing qualifications repeated in the closing.
The better-rated exchange highlights its direct request and explicit outcome.
A compact comparison below the poor exchange pairs follow-ups (148 vs 568
characters; 4/4 vs 0/4) and closings (220 vs 509; 4/4 vs 1/4). Original text is
unchanged beneath presentation markup; source JSON/hashes are retained.
Annotations 1/3 are author readings, not additional organizer labels. These are
selected, different conversations and search assistants, not a controlled test.

### Current side-by-side page and editor audit

Page 2 aligns both recorded conversation excerpts: assistant context, researcher
follow-up, later/next assistant response and researcher closing. Shared colors
and numbered key compare the same functions in both columns. Original texts,
ratings and omission markers are retained. Source is
`figures/conversations-side-by-side.tex`; previous separate figure sources remain
as revision history.

A post-hoc descriptive audit of all 258 generated official Task 2 draft/edit
pairs found 245 unchanged, two shorter and eleven longer. This is our receipt
analysis, not an organizer metric or a causal realism result. Exact method and
source inventory binding are in `submitted-editor-audit.json`. This audit was
added in response to the user's question about prompt/approach gaps; no new
inference, submission or experiment was launched.

### Plain-language diagnosis requested by the user

The main text now includes "Where we fell short." It explicitly acknowledges
poor validation of human-like behavior, then distinguishes recorded facts
(245/258 unchanged; the conservative editor instruction; lack of a human-length
target) from suspected mechanisms (reinforcing its own generated voice and
uncalibrated stopping). The draft-only comparison gap remains explicit. This is
a reflection on the submitted system, not a new experiment or a restored history
of unsubmitted variants. The user specifically authorized a candid assessment.

### Current annotated task and prompt revision

Added a brief task explanation before the method. The two new large illustrations
separate task roles/outputs from the submitted two-call process. The stopping-
calibration hypothesis has been removed at the user's request; observed session
length and actual stopping mechanics remain. The two Known paragraphs are merged
as "A bad prompt for correcting verbosity," explicitly linking the instruction
not to shorten automatically with 245/258 unchanged drafts. The retained voice-
reinforcement explanation remains a hypothesis. Side-by-side quote text,
highlights, ratings and official aggregate scores are unchanged.

### Current diagram redesign after visual feedback

The current paper uses editable vector figures, not the generated illustrations.
`figures/task-overview-clean.tex` explains the two evaluation tasks;
`figures/draft-edit-clean.tex` shows shared input, draft/edit calls and the copied
Task 2 decision. Restrained outlines, paper typography and one accent color
replace clip art, oversized headlines and colored banners. No generated raster
illustration is referenced by the current manuscript. Old images/prompts remain
historical. The title-only image edit was not selected after the user's feedback.
All paper text, recorded excerpts, highlights, ratings and audit results remain.

Native-diagram revision verified: all five pages rendered and inspected; clean
LaTeX log, unchanged verbatim quotes and result values, and final PDF identical
to the checked build.

## Moderate visual styling — November 7

Restyled both native diagrams with soft panel backgrounds, rounded boxes, role
icons, teal drafting and purple editing emphasis, and stronger flow arrows.
Task wording and method semantics retained. Rendered and inspected pages 1-2;
pages 3-5 render byte-identically to the previously inspected version. Clean
five-page build with no warnings or overfull boxes; delivered PDF matches build.

## Prompt and human-rating explanation — November 7

Clarified that the markup criticism is the recorded reason attached to the
organizers human rating of the poor follow-up. Added three exact editor-prompt
excerpts and 245 unchanged / 2 shorter / 11 longer counts. Saved turn-0011 edit
request confirms the shown 568-character prior reply was supplied as a voice
reference for the closing draft. Two original openings illustrate the possible
style repetition without claiming causation. All prompt quotes checked against
the saved request; no participant profile or assistant transcript added.
Six-page clean build: inspected changed pages 3, 5 and references page 6; pages
1, 2 and 4 render identically to the previously checked version. Final PDF
copied from verified build.

## Layout and color-access revision — November 7

Moved the prompt/audit figure below the method diagram to use page 2; references
now share page 5 with the discussion. Five pages, original 11pt body type retained.
Replaced yellow/purple/green highlights with one neutral gray and a caption
explaining numbered notes rather than quality coding. Simplified diagrams to
neutral panels and a muted blue accent; explicit labels carry all meaning.
Human chart bars now use hatching versus solid simulator bars. Inspected all
five final pages (page 2 identical to inspected intermediate), plus a grayscale
render of the results chart. Clean LaTeX log; no overfull boxes or undefined
references. Final PDF matches checked build.

## Narrative revision — November 7

Reworked the main narrative for competition participants: task, submitted
approach, aggregate results, contrasting recorded conversations, and lessons.
The abstract now states the observed weakness and the purpose of the analysis.
Moved all results and their limits onto page 3 before the conversation examples.
Removed repeated transitions and recast the final discussion around two concrete
checks: useful editing targets and the choice of voice references. Proposed
comparisons remain future work; style reinforcement remains a hypothesis.
Prior source preserved in ignored build/before-prose-revision.tex.
Verified five-page build, all rendered pages, correct section ordering, official
values, editor counts and references on page 5. No warnings or overfull boxes.
Conversation and prompt figure sources unchanged in this prose revision.

## Four-section structure and prompt-only figure — November 7

Consolidated Introduction, Method, Results (including conversation examples),
and Discussion. Added the reason for conservative editing beside the prompt.
Removed audit counts from the prompt figure and placed the complete
245 unchanged / 2 shorter / 11 longer result in discussion. Results now lead
into the examples after explaining evaluation limits. Five rendered pages
inspected; clean build, references on page 5, counts present only in discussion
and abstract summary. No score or quote changes.

Removed the API configuration footnote at the user's request. Repository
reference retained and cited in the method sentence. Clean five-page build;
page 2 visually checked, other pages have identical extracted text.

## Whole-paper participant-readability review — November 7

Reviewed all sections, figures and evidence for a competition-participant reader.
Added the missing drafting behavior (persona-consistent speech and sufficient-help
or unproductive-search stopping), verified against the saved official turn-0011
draft request. Defined dialogue acts and clarified JSD direction. Marked selected
conversations as examples rather than frequency evidence. Added a closing lesson:
an editor needs a testable purpose; shorter is not automatically better; evaluate
realism and preservation of the request on held-out conversations. Proposed human
voice references should come from separate training conversations.
Remaining gaps: author details; no matched human draft/edit ratings or controlled
voice-reference comparison, so no causal claim about editor effectiveness.
Five final pages rendered and inspected, score values and audit counts checked,
clean LaTeX log, references share final page. Prior source retained in ignored
build/before-whole-paper-review.tex. No new model run or external publication.

## Author details and final writing/layout check — November 7

Copied Nidhin Pattaniyil and npatta01@gmail.com from the MAST combined paper,
/home/npatta01/.codex/worktrees/d265/multilingual_agentic_search_2026/paper/combined.tex
(lines 19-21). Rendered affiliation as singular Independent researcher for this
single-author draft. No coauthor imported from the other project. Updated both
LaTeX author metadata and visible title block. Simplified the variance caption
and extra-turn interpretation. Read and visually checked all five final pages;
no placeholder author, warnings, undefined references or overfull boxes. Score
values and 95 percent audit retained, references on page 5, final PDF identical
to verified build. Current draft remains local; no submission or publication.

Added coauthor Tanwir Zaman at the user's request. Name and shared independent
researcher affiliation verified against worktree 5771 TRECVID draft (lines 44,
54-55); email zaman.tanwir@gmail.com verified against its speaker proposal
(line 15). Updated visible and LaTeX author blocks. Five-page clean build,
first page visually checked; extracted text on pages 2-5 unchanged.

## Full direct-language revision — November 7

Rewrote abstract, method, results prose, captions and discussion in direct
language. Replaced abstract wording about voice, preservation and causal
comparisons with concrete descriptions of messages, edits and evidence limits.
Discussion headings now state our observations; proposed improvements appear
once in the closing paragraph. Prompt excerpts and all four recorded simulator
quotes remain untouched. No changes to scores, author details or figures.
Prior source retained in ignored build/before-natural-prose.tex. All five
rendered pages inspected; clean build, scores and 245/258 audit checked,
references share final page. Verified build copied to delivered PDF.

## Participant-perspective submission-readiness review — November 7

Trimmed repeated unchanged-example wording, softened the abstract causal framing,
identified NP Labs, and removed the working-draft banner. Live GitHub CLI check
confirmed the cited repository is PRIVATE; reference now states this explicitly.
No sharing changes. Live track guidelines confirm preliminary results are intended
for notebook papers; model documentation link also resolves. Scoped organizer
email search/read found the Nov 4 results release and Oct 26 conference update,
but no UserSim paper format/page-limit/upload-deadline instruction. Other-track
deadlines were not transferred to UserSim. NIST active-participant page returned
401. Therefore content/layout is ready for a participant notebook; formal
submission compliance remains unverified.
Five final pages inspected; references, authors, scores and edit counts checked;
clean LaTeX log. Final PDF copied from verified build. Nothing submitted.

Current requirements audit: [November 7 submission requirements](submission-requirements-2026-11-07.md). Authenticated TREC participant pages checked; UserSim paper format, limit, deadline and destination still unverified. Login.gov-protected Evalbase account remains to be checked.
