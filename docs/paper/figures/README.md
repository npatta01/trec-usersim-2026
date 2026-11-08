# Paper figures

- `architecture-overview.png`: built-in image generation; checked and integrated.
  The researcher illustration represents a simulated role, not a real participant.
  The feedback loop is Task 2 only. Both model calls see original context.
- `sample-conversation.tex`: deterministic vector timeline. All dialogue and
  decision rationales are invented, not model outputs or observed human states.
- `editor-flow.tex`: deterministic vector branches for narrow Task 1 fidelity editing.
- `preview.tex`: standalone wrapper for conversation previews. From this folder:
  `xelatex -output-directory=../build preview.tex`, then
  `pdftoppm -r 130 -singlefile -png ../build/preview.pdf sample-conversation`.

## Image-generation prompts

Built-in tool, no private inputs. Initial generation prompt:

> Create a restrained professional scientific infographic for an information retrieval research paper, landscape 3:2, white background, crisp high-resolution typography, minimal palette navy / teal / muted violet. No childish cartoon, no robots, no glossy 3D, no decorative background. Main title exactly 'Simulating the researcher'. Three visual zones: LEFT a simple elegant line illustration of researcher at desk beside a stack of labeled documents 'Persona', 'Goal', 'Dialogue'. CENTRE two sequential circular model-call symbols with exact short labels '1 Draft' and '2 Edit', connected by a right arrow. Caption directly under circles 'Same context in both calls'. RIGHT a simple search interface illustration labeled 'Organizer search assistant' and a small generated chat bubble labeled 'Researcher message'. Show clear arrows: input documents to Draft; Draft to Edit; Edit to Researcher message; Researcher message to search interface; search interface returning an arrow along the bottom toward Dialogue, labelled exactly 'Reply updates dialogue'. A separate narrow bottom strip shows two task labels with spacious typography: 'Task 1: one supplied prefix → one prediction' and 'Task 2: repeat until continue / stop decision ends the session'. Ensure continued dialogue arrow only refers to Task 2. Prominent note by circular model calls exactly 'GPT-6 Luna'. Important scientific constraints: model generates researcher side, organizer handles dataset search; both calls see original available context; no model retrieval or fine tuning. Use diagrams with meaningful pictograms and open space, not a row of rectangular boxes. All text must be legible at half-page print size. Do not include additional wording, fabricated scores, flags, or technical components.

Final edit prompt:

> Keep this scientific infographic exactly as is except replace these two text labels for technical accuracy and readability. Bottom-right footer must read exactly 'Task 2: interact until the researcher chooses to stop'. Label on bottom feedback arrow must read exactly 'Task 2 only: reply updates dialogue'. Preserve all other wording, illustration, typography, palette, layout, arrows, and white background. Do not add any elements.

The final asset is copied into this repository; it does not depend on the original
Codex-generated image directory. The paper uses it as a schematic, not empirical
or participant evidence. The exact method is stated in the surrounding prose.

## Organizer result comparison

`results-comparison.pdf` is the vector paper figure; `results-comparison.png` is its preview. Rebuild with `python figures/build-results-comparison.py` from the paper directory. The script reads only the public aggregate preliminary-results JSON. Separate axes retain original units, bars start at zero, and direct labels give the means. Human-likeness ratings are excluded because no human-reference mean was supplied.

## Real submitted replies — current Figure 2

`real-submitted-replies.tex` shows two own-model outputs from the official Task 2 run, with organizer human-likeness labels. `../real-examples.json` records the exact excerpt text and aggregate provenance. Private source locators remain outside git. This figure replaces both unused constructed heat-data figures in the current manuscript; it does not quote a human participant or claim a controlled length effect. The user expressly requested real examples.

## Current submitted-only paper figures

- `submitted-control-flow.tex`: exact draft/edit/text/stop data flow, checked
  against the submitted generator behavior. Replaces the earlier illustration.
- `real-conversation-flow.tex`: researcher outputs quoted verbatim from one
  official conversation. Assistant turns are visibly labeled summaries, and
  three intervening exchanges are marked as omitted. Exact quote hashes and
  source message indices are in `../real-conversation-flow.json`; private record
  locators remain with the evaluation archive.
- `results-comparison.pdf`: same verified values, with the gray series renamed
  Human conversations (organizer mean). This is not a graph of human answer texts.

Previous figure assets and their provenance are retained as revision history,
but are not referenced by the current manuscript.

## Custom overview and low-rated conversation — current revision

`submitted-overview-illustrated.png` replaces Figure 1 with a custom illustration
made using the built-in image-generation tool. Its exact prompt is saved in
[submitted-overview-prompt.txt](submitted-overview-prompt.txt). Only public method
facts were supplied; no conversation text was sent to image generation. Checked
shared-context arrows, two model calls, editing path, copied stop decision and
Task 1/Task 2 policy notes against the runner. The project copy is self-contained.

`speaker-icons.tex` defines small vector researcher/search icons. They accompany
explicit labels in both recorded flows; they do not imply that simulator text
was written by a human. `real-bad-conversation-flow.tex` shows a contiguous late
segment from a second official conversation. Simulator turns are exact outputs;
assistant turns are labeled summaries. `../real-bad-conversation-flow.json` keeps
quote hashes and ratings; private locators remain with the evaluation archive.

## Inline annotations and descriptive comparison

Current conversation TeX sources use breakable highlights from the `soul` LaTeX
package. Green marks the better-rated direct request and explicit outcome.
Numbered amber/purple highlights in the poor exchange connect to margin notes.
The original text in both flow JSON files is unchanged; annotation numbers,
colors and comparison notes are editorial additions. Notes 1/3 express our
reading, while note 2 reflects the annotator's punctuation/Markdown criticism.
`../conversation-comparison.json` stores the verified lengths and ratings for
both pairs. No rewritten or hypothetical 'better response' is presented.

## Current aligned excerpt figure

`conversations-side-by-side.tex` replaces the two separate comparison figures.
Both columns use amber for follow-up openings and teal for closing emphasis;
purple identifies literal Markdown only where it occurs. Follow-up and closing
rows align, with true lengths and human ratings shown in the headers. Assistant
messages remain labeled summaries; the left column's three omitted exchanges
are explicit. No quoted researcher wording was rewritten. Generated overview
and quantitative result-chart assets are unchanged.

## Current simpler task and method illustrations

- [task-overview-spacious.png](task-overview-spacious.png): single prediction in
  Task 1 versus simulator/organizer dialogue in Task 2. Newly generated from
  public task facts with the built-in image tool.
- [draft-edit-spacious.png](draft-edit-spacious.png): a simplified companion to
  the older combined overview. Keeps only drafting, editing and the Task 2
  decision bypass; shared inputs and task policy details are in nearby prose.
- [Exact prompts](spacious-figure-prompts.json) record the built-in generation
  and referenced original. Both new assets are preserved in the repository.

These replace the cramped combined image in the current PDF. Old image and
vector sources remain as history. No private conversation was used as image input.

## Current paper-native diagrams

After the user's rejection of the generated illustrations, the manuscript uses
`task-overview-clean.tex` and `draft-edit-clean.tex`. Both are editable vector
sources with the paper's font, simple outlines, consistent labels and a single
accent color. The task diagram describes two evaluation tasks, not two different
simulation approaches. The method diagram distinguishes shared input, text
editing and the copied Task 2 decision. Generated image assets and their prompts
remain historical, unused by the current manuscript.

## Moderate visual styling — November 7

Restyled both native diagrams with soft panel backgrounds, rounded boxes, role
icons, teal drafting and purple editing emphasis, and stronger flow arrows.
Task wording and method semantics retained. Rendered and inspected pages 1-2;
pages 3-5 render byte-identically to the previously inspected version. Clean
five-page build with no warnings or overfull boxes; delivered PDF matches build.

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
