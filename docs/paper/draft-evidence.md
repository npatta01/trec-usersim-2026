# Draft evidence and verification

October 10, 2026. Canonical manuscript: `usersim2026-draft.tex`.
Evidence base fast-forwarded from `77f7d07` to `2cf803a` (current fetched
`origin/main`) before drafting. No simulator behavior was changed.

## Venue check

Read the current public pages:
- [UserSim guidelines](https://trec.usersim.ai/guidelines): tasks, scenario inputs,
  test-pool counts and planned evaluation. No notebook format, page limit,
  submission location or exact paper deadline was found.
- [UserSim home](https://trec.usersim.ai/): preliminary results are planned for
  mid-late October for inclusion in notebook papers. This is not a paper deadline.
- [NIST participation guide](https://trec.nist.gov/howto.html): generic notebook
  then proceedings-revision process, not a verified 2026 UserSim deadline.
- [2026 call](https://trec.nist.gov/cfp.html): participation and conference details;
  no paper-format requirement established.

The existing October 10 authorized-email audit records an extended **run**
deadline and no found notebook announcement. This draft did not query email,
private participant pages or authenticated organizer APIs. The manuscript's
single-column, 11-point US Letter format is provisional. Do not import the
TRECVID or MAST template requirements from the user's style examples.

## Claim map

| Manuscript claim | Source |
|---|---|
| Task definitions and planned evaluation | Public organizer guidelines; `docs/task1_workflow.md`, `docs/task2_workflow.md` |
| Training counts, missing stop labels, participant-ID limits, checksum | `docs/research/official-data-evidence.md` |
| Input projection and role mapping | `usersim/prompts.py`; official-data audit |
| Model ID, route, token cap; no explicit temperature | `usersim/requests.py`; `docs/paper/README.md` |
| Editor policies and Task 2 fixed boolean | `usersim/prompts.py`, `usersim/task2/generator.py` |
| Development screen numbers and limitations | `docs/research/method-decisions.md` |
| Fidelity probes, repetitions and review coverage | `docs/research/task1-fidelity-fix.md` |
| Official coverage, costs, IDs, closures and delayed replies | `submissions/manifest.json`, `docs/paper/submission-results.csv`, `docs/submission-ledger.md` |
| Terminal reconciliation | Submission ledger, handoff, recovery guide |
| Verified evidence preservation | `docs/private-artifact-release.json`, `docs/artifacts.md` |

The worked example is newly invented, not an actual model output. No private
participant transcript or profile was copied into the draft. Development
screens are not held-out quality estimates. Official evaluation is pending in
retained evidence; completion and audit success are not effectiveness scores.

## Verification

- Receipt-index arithmetic reconciles: 124 + 516 = 640 model calls;
  $0.029373225 + $0.173554630 = $0.202927855.
- Task 2 accounting reconciles: 49 + 8 = 57 conversations;
  258 generated pairs × 2 = 516 calls; 258 + 8 = 266 submitted turns.
- XeLaTeX/latexmk build: 6 US Letter pages (4 main + 2 appendix), no warnings, undefined references
  or overfull boxes. Inspected all six final rendered pages.
- Final PDF: `usersim2026-draft.pdf`; reproducible build copy under `build/`.
- No live model/organizer call, publication, push or submission performed.

## Next action

User review of framing and author metadata. Add preserved official score reports
and confirmed participant paper instructions when available; assess related-work
coverage before a final version. The first draft focuses on the submitted system
and includes only references actually used, rather than treating historical
literature adaptations as components of this baseline.

## Visual revision

Added `figures/task-flow.tex`, `figures/sample-conversation.tex` and
`figures/editor-flow.tex`. These show the independent Task 1 input, Task 2
feedback loop, an invented five-turn dialogue with fixed stop flags, and a
constructed provenance-repair example. Real participant/model text was not used.
Moved detailed development evidence and long identifiers to appendices.

## Section audit

Main narrative reduced from eight sections to five. Stopping and prompt inputs
are method details; transport recovery and custody are appendix material. The
architecture illustration was generated from public method facts only, checked
for correct task boundaries, and saved under `figures/architecture-overview.png`.
The conversation is a constructed timeline with rationales, not inferred human
mental states from real records. Figure-generation prompts are in `figures/README.md`.

## Participant audience revision

Assumes track familiarity. Main selection table adds the matched Luna/Sol raw-draft
screen (8 drafts each over 4 contexts), four-prefix summary comparison (37–53%
draft-input reduction, editor still full history), and retained editor checks.
Source: `docs/research/method-decisions.md`. This table explains selection, not
causal component gains. The illustrative dialogue now diagnoses the distinction
between accepting a recommendation and claiming completed verification.

## November 7 result revision

Official preliminary results now replace the pending-score statements in the manuscript; see organizer-results-2026-11-07.md and preliminary-results-2026-11-07.json. Seven pages (five main, two appendix), rebuilt with XeLaTeX. Human-like means independently recomputed from numeric user-turn annotations. All final pages rendered and inspected; build has no warnings or overfull boxes. Previous layout counts above refer to the October draft.

### Results readability follow-up

Added a vector paired-bar comparison from organizer aggregates, with separate zero-based axes for characters and user turns. Main results retain three takeaways and a compact table; full rating counts and administrative accounting moved to Appendix B. Seven-page final PDF rebuilt and rendered for layout review.

## Whole-paper revision brief — November 7, 2026

Reader: fellow UserSim participants who already know the tasks and API.
Takeaway: a minimal draft/editor baseline can target specific unsupported-action errors, but voice editing and preserved stop flags do not establish human-like behavior. Official results expose much longer utterances and more user turns.

Scope: edit prose and figure captions, retain all four visuals and all official scores. No new experiment, organizer request, submission, public publication or template conversion. A recoverable copy of the previous manuscript, PDF and editable figures is under ignored `build/before-whole-paper-readability/`.

Coverage map:

| Previous content | Revised location / decision |
|---|---|
| Approach, context, role mapping, two calls, task policies | Main section 1: submitted simulator |
| Data counts and absence of researcher stop labels | Concise main implication; exact counts in configuration appendix |
| Narrow repair decision and invented conversation | Retain figures; use one heat-data example to explain repair versus acceptance |
| Repeated model/summary/style development tables | Main section 2: three practical lessons; quantitative checks consolidated in development appendix |
| Rejected broader fidelity editor | Add its preference-hardening failure as a concrete reusable lesson, grounded in task1-fidelity-fix.md |
| Organizer scores and human-comparison chart | Main section 3, preserving scales, samples and preliminary status |
| Repeated conclusion and limitations | One practical closing paragraph; study limits stated once in relevant appendix |
| Provider settings, exact run IDs, evaluation definitions | Configuration/evaluation appendix |
| Training hash, file counts, local reconciliation, debug lifecycle | Remove from manuscript; canonical paper notes, preservation guide and submission ledger retain evidence |

Verification: rebuild with XeLaTeX, inspect all final pages, check official numbers and references, and compare narrative word counts. Preserve readable 11-point type; do not compress by reducing body font.

### Whole-paper verification result

Final artifact: six US Letter pages (four main, two appendix), three main sections and four figures, using the same 11-point body type. Rebuilt with XeLaTeX; no warnings, undefined references or overfull boxes. Inspected every rendered page after the last layout edit. Freshly checked ZIP integrity/hash, recomputed both human-rating means and sample counts from the original annotations, and matched numeric result fields to the archive summary and PDF text. Final PDF is byte-identical to the verified build. No new model/organizer call or public write was made.

## Annotated feedback and real examples — November 7

User requests supersede the earlier invented-example-only brief: simplify the abstract, add a model citation, explain the editing failure plainly, remove vague development prose, remove excess whitespace, and use real good/bad examples.

- Abstract now has two short paragraphs with concrete verbs.
- Verified and fetched OpenAI's official GPT-6 Luna model page; cite it at the first model mention in the main text. The OpenRouter request ID is still preserved in Appendix A.
- Removed the invented editing decision chart and heat-data dialogue from the manuscript. Their sources remain for history.
- New Figure 2 contains only two non-identifying, simulator-generated utterances expressly requested by the user. No participant utterance, persona, name, raw annotator reason or session identifier is quoted. Named datasets are public resources mentioned in the generated text, not recommendations endorsed by this paper.
- `real-examples.json` holds exact text, lengths, ratings and hashes. Private `paper-example-locators.json` beside the original evaluation ZIP maps examples A/B to records and receipts. Both excerpts match draft response, editor response, accepted organizer payload and evaluated text exactly. Their editor outputs were unchanged; both requests have HTTP 200 organizer receipts.
- Selection is deliberately illustrative: contrasting ratings within the broad NER-documentation topic, not a matched causal comparison. Rating reasons are paraphrased, not quoted.
- Replaced the vague development introduction with the specific rejected-editor failure and explanation of its replacement. Removed the forced results-page break so text can fill the space after the examples.
- Previous PDF/source are preserved in ignored `build/before-annotated-feedback/`. No new model generation, organizer submission or public publication.

### Annotated-feedback verification

All five original comments addressed: abstract rewritten/split; official model citation added; unexplained constructed rule figure removed and rule explained in text; vague development introduction replaced; invented conversation and its blank-space layout removed. The subsequent real-example request is addressed by two accepted, evaluated model replies in Figure 2. Final PDF is five pages (three main, two appendix) with three figures. Every final page was rendered and inspected after the last edit. XeLaTeX has no warnings, undefined references or overfull boxes. Exact example hashes/lengths/ratings and unchanged-editor status verified; aggregate score values retained in PDF text. Final delivered PDF is byte-identical to the verified build. No live model call, submission or publication.

## Submitted-only scope and conversation flow — November 7

User correction: cite the model in the abstract; remove the selected-example commentary from the abstract; explain the editor visually; include an actual conversation sequence; define the human reference; remove both appendices and all unsubmitted development material.

- New method diagram shows shared context, text editing and the unchanged Task 2 decision path. Its fixed-decision input/copy behavior was checked against usersim/task2/generator.py and usersim/prompts.py.
- New real conversation flow uses the same official conversation as previous example B, with exact generated opening, follow-up and final message. Assistant messages are explicitly summarized and three intervening exchanges are marked as omitted. Private locator remains with original evaluation evidence; public flow metadata includes only source message indices, text hashes and the permitted non-identifying excerpts.
- Verified the result ZIP contains only README and our run annotations, not held-out human-reference utterances. Public guidelines distinguish the separately collected human test conversations from the training logs. Plot legend now says human conversations / organizer mean.
- Removed development comparisons, rejected variants, long identifiers, training-data audit, future experiments and appendices from the manuscript. Exact configuration, provenance and removed material remain in canonical repo notes and the recoverable prior draft under ignored build/before-submitted-only-review/.
- Model citation now appears at the first model mention in the abstract. Example-specific analysis is kept beside the conversation, not in the abstract. No new model/organizer call, submission or publication.

### Submitted-only verification

All seven comments addressed. Final manuscript has four pages, three main sections, three figures and no appendices. Read all four rendered final pages; clean XeLaTeX build with no warnings, undefined references or overfull boxes. The three real researcher turns match evaluated text, original draft text, editor output and accepted organizer POST payloads; their fixed stop decisions match the historical editor requests and final annotation. Assistant summaries are explicitly labeled and checked against their source responses. All plotted and tabulated scores retained; both rating means recomputed from original ZIP annotations. Human-reference explanation checked against ZIP contents, its README and current public organizer guidelines. Final PDF matches the verified build byte-for-byte. No new inference, organizer submission, push or publication.

## Poorly rated conversation and visual requests — November 7

Added one contiguous late official Task 2 exchange selected for low ratings. Two
simulator messages (568 and 509 characters) scored 0 and 1; both match original
draft text, editor output, evaluated text and an accepted organizer POST. They
are model-generated responses, not participant text or administrative closures.
Assistant replies are summarized without endorsing their factual claims. The
analysis distinguishes a human-likeness failure from factual correctness and
does not infer a causal length effect from different personas/histories.

Added vector speaker icons beside readable labels to both conversation figures.
Custom illustrated Figure 1 uses the built-in image tool with public method facts
only; exact prompt is in figures/submitted-overview-prompt.txt and the asset is
copied into the project. Prior draft and vector figure remain recoverable under
ignored build/before-bad-conversation/. No new competition inference, official submission,
public publication or sharing of private conversation data with image generation.

### Paired-flow verification

Final PDF: five pages, four figures, no appendices. Inspected all final rendered
pages at 900px height after the last layout edit. Clean XeLaTeX build, no warnings,
undefined references or overfull boxes. Both flows' quoted turns and ratings match
the original evaluation records; low-rated turns also match draft/edit outputs
and accepted POSTs. Historical editor instructions explicitly prohibit automatic
shortening, supporting the discussion. Generated project asset is byte-identical
to the built-in output, and the exact generation prompt is retained. Aggregate
scores remain unchanged. Delivered PDF is byte-identical to the verified build.

## Inline failure annotations and direct comparison — November 7

User requests visible highlights in the bad exchange and an easy comparison to
the better-rated conversation. Original quote JSON remains byte-unchanged.
Numbered note 1 marks the two-sentence prelude, note 2 the literal Markdown
markers, and note 3 licensing qualifications repeated in the closing message.
Notes 1/3 are expressly author interpretations; note 2 is supported by the
organizer annotator reason. Green highlights in the better-rated flow identify
the direct request and explicit outcome. A compact comparison below the poor
exchange gives both replies' true lengths and ratings. Different personas and
histories remain explicit; no causal length claim or factual-error claim.
Previous source/PDF/figures are preserved under ignored
build/before-inline-annotations/. No new model generation or organizer call.

### Inline-annotation verification

Five-page final PDF, four figures, no appendices. Rebuilt with no warnings,
undefined references or overfull boxes, and visually inspected all five final
pages. Stripping only editorial highlight/number macros from each quoted turn
reconstructs the exact original wording, confirmed by stored hashes; assistant
summaries also remain unchanged. Comparison lengths/ratings match the two source
flow JSONs. Checked that every new callout, comparison number and existing score
appears in PDF text. Author readings and the annotator's stated criticism are
separated in the caption. Final PDF matches the verified build byte-for-byte.
No new image generation, inference, organizer request or publication.

## Side-by-side comparison — November 7

User requested the two recorded conversations on one page. Replaced separate
flows with one aligned two-column figure: assistant context, follow-up, assistant
response, closing. Original simulator messages remain complete and unchanged;
opening turns are excluded because the comparison pairs follow-ups and closings.
The left column's three skipped exchanges are marked. Shared highlight colors
and numbered key now denote the same functions in both columns: request opening,
literal formatting, closing emphasis. Captions distinguish editorial readings
from annotator reasons and preserve the non-causal comparison limit. Source JSON
and previous figures remain intact; prior PDF/source backed up under ignored
build/before-side-by-side/.

### Side-by-side verification and user diagnosis question

Final artifact: four pages, with the full aligned comparison on page 2. All four
quoted simulator messages reconstruct exactly after removing only editorial
highlight/number macros. Original hashes, lengths and ratings are unchanged;
left-side omitted exchanges remain explicit. Rebuilt cleanly and inspected every
final page. No warnings, undefined references or overfull boxes. Verified that
all four excerpts/lengths occur together on PDF page 2, existing organizer scores
are retained, and the delivered PDF matches the verified build byte-for-byte.

In response to the concurrent question about prompt/approach gaps, inspected
historical editor instructions and audited all 258 generated Task 2 pairs.
245 exact unchanged outputs, two shorter and eleven longer. The editor's request
draft fields match first-call parsed texts. This is a descriptive submitted-run
analysis, not new generation or an organizer metric. Added it to the abstract
and alongside the comparison with its lack-of-matched-ratings limit. The prompt
explicitly prevents automatic shortening and strong content changes. Task 2's
self-generated previous utterances as voice references and uncalibrated prompted
stopping are plausible contributors, not established causal findings. No new
model/organizer call, paid experiment or public publication.

## Plain-language prompt/approach gaps — November 7

User explicitly asked to add the diagnosis to the paper, distinguish known facts
from suspicions, and acknowledge poor work rather than soften the criticism.
Added a main-text discussion of the submitted system, without restoring the
removed development appendix or unsubmitted variants. It owns inadequate
validation, reports the exact 245/258 unchanged audit, quotes the submitted
anti-shortening instruction, and separates two hypotheses (self-generated voice
references and uncalibrated stopping) from measured effects. It does not treat
unchanged output as intrinsically wrong, infer an editor benefit/harm without
matched draft ratings, or claim a competitive rank. Moved the detailed audit
paragraph out of the example discussion to avoid duplication. Previous source
and PDF remain recoverable under ignored build/before-plain-language-gaps/.

### Plain-language discussion verification

Final PDF remains four pages, with the side-by-side comparison on page 2 and
"Where we fell short" on page 4. Two Known paragraphs distinguish the output
audit and documented prompt from two Suspected paragraphs on voice and stopping.
The section explicitly acknowledges poor validation and missing matched draft
ratings. Rechecked 245/258 arithmetic, the historical anti-shortening instruction
and the original editor input's last-two-message selection. Existing quote
lengths, ratings and organizer scores remain in the PDF. Clean XeLaTeX build;
all four final rendered pages inspected. No warnings, undefined references or
overfull boxes. Delivered PDF is byte-identical to the verified build.

## Task section, uncrowded figures and bad-prompt assessment — November 7

Four new annotated requests:

1. Replace the cramped overview with two simpler images. New Figure 1 explains
   the task setup; new Figure 2 explains our submitted two-call mechanism. Both
   use full text width, larger labels and fewer concepts than the old combined
   image. Task diagram checked against task1_workflow.md/task2_workflow.md;
   method diagram retains the text edit and copied Task 2 decision paths.
2. Remove the stopping-calibration hypothesis. Deleted that entire discussion
   paragraph and the corresponding introductory critique; actual Task 2 stopping
   mechanics and measured turn counts remain.
3. Combine the two Known paragraphs into a candid assessment titled "A bad
   prompt for correcting verbosity," connecting the historical anti-shortening
   instruction with 245/258 unchanged outputs. This judges the prompt's fit for
   the observed problem without claiming a controlled causal effect on scores.
4. Add a short task section before the method: researcher versus organizer
   roles, one next-message output in Task 1, and multi-turn interaction in Task 2.

Two new illustrations were generated with the built-in tool using only public
method/task facts. Exact prompts and mode are in figures/spacious-figure-prompts.json;
project PNGs are copied from the generated outputs. No conversation or private
profile was sent to image generation. Prior PDF/source preserved under ignored
build/before-task-and-prompt-comments/. No new competition run or public action.

### Four-comment revision verification

Five-page final PDF. Task section precedes the method; the two new full-width
illustrations are on pages 1 and 2. Both were visually checked for role/output
boundaries, two model calls, text editing and the copied Task 2 decision. Project
assets are byte-identical to built-in outputs; exact prompts are retained.
The stopping-calibration hypothesis is absent. Prompt/inactivity paragraphs are
combined under the explicit bad-prompt assessment, with 245/258 retained and
causal limits intact. All four original quote texts and ratings remain aligned
on page 3. Organizer scores unchanged. Clean XeLaTeX build with no warnings,
undefined references or overfull boxes. Inspected all five final rendered pages;
delivered PDF is byte-identical to the verified build. No new competition
inference, submission, push or public publication.

## Replace generated illustrations with paper-native diagrams — November 7

User rejected the illustrations as visually poor and corrected the misleading
"two ways to simulate" title. Replaced both generated raster assets in the
manuscript with editable TikZ diagrams: two evaluation tasks, and the submitted
model-call/control flow. Restrained lines, matching paper typography, one accent
color, no clip art or oversized titles. The corrected-label generated variant
was not selected or incorporated. All old assets remain as revision history.
No paper claims, scores, quoted messages or model behavior are changed.

### Native-diagram verification

Clean five-page XeLaTeX build with no warnings, undefined references or overfull
boxes. Inspected all five rendered pages, including both new diagrams and the
aligned real-conversation comparison. Active manuscript references only the
native task/method diagrams and the quantitative vector chart. All four quoted
replies match the preserved flow JSON verbatim after removing annotation macros;
lengths and ratings remain 148/4, 568/0, 220/4 and 509/1. Organizer scores and
245/258 unchanged pairs are retained. The delivered PDF is byte-identical to
the verified build. No competition inference, submission or publication.

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

Reframed the closing paragraph as What we would do better, using first-person
future improvements instead of advice to other participants. Only page 5 text
changed; clean five-page build and rendered final page checked.

Rewrote the selected voice-reference interpretation in direct language; removed
repeated future-test advice while retaining uncertainty and the absence of human
draft ratings. Only page 5 text changed. Clean five-page build and final-page
render inspected.

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

Added Semih Yagli after Nidhin Pattaniyil and Tanwir Zaman as requested;
spelling and independent-researcher affiliation match the prior GLEE manuscript.
Verified all three names and absence of working-draft label. First-page render
checked, five-page clean build, remaining pages have unchanged extracted text.

Added Semih's email and aligned three names with their own emails beneath.
GLEE source and output PDF contained no email; Semih's sender identity was
verified from connected Gmail correspondence. Shared Independent researchers
affiliation and Team NP Labs are labeled separately. Clean five-page build,
first-page visual QA, all names/emails checked, remaining page text unchanged.

## Final manuscript check — November 7

Read the complete manuscript and visually inspected all five rebuilt pages.
Simplified two method-diagram labels and set PDF title and author metadata.
Verified the three author names and emails, no working-draft banner, references
on the final page, and a clean LaTeX log with no overflow or undefined references.
Saved the verified build as usersim2026.pdf and refreshed usersim2026-draft.pdf
for existing annotation links. Venue submission requirements remain unconfirmed;
nothing was uploaded or submitted.
