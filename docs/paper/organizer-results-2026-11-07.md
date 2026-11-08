# Preliminary organizer evaluation — November 7, 2026

Downloaded the November 4 release using the organizer GET /api/run/team-runs-eval endpoint. No submission or inference was run. Exact ZIP, extracted annotations and the pre-edit manuscript are retained privately under the dated preliminary-results directory. Raw participant text and rating reasons are not copied here.

Archive SHA256: `b4f3ca11e86151d2569d25db25a1bbb638fe42b8304c83fbc214928cc2e469c4`.

See `preliminary-results-2026-11-07.json` for run-bound aggregates. Task 1: JSD 0.106, mean human-likeness 2.375 from 16 user turns in 16 conversations. Task 2: JSD 0.158, mean 2.3134328358208953 from 67 user turns in 14 conversations. Ratings use the numeric `humanity` field, whose 0–4 mapping agrees with the accompanying category labels. No missing rating was treated as zero.

Organizer-reported mean user lengths: 563 vs human 313 chars (Task 1), 382 vs 199 (Task 2). Task 2 user turns: 4.7 vs 3.6; all turns: 8.2 vs 6.9. Ratios use rounded organizer aggregates. JSD uses base 2 and lower means closer, with dialogue acts assigned by majority vote from three LLMs. Human-reference rating mean, cross-team leaderboard, sampling design, agreement and uncertainty are absent. No competitive rank or parity claim is supported. Task 2 includes administrative closures; no adjusted score is provided.

Next: confirm paper format and submission requirements; retain preliminary status until final organizer release. New raw evidence is local/private; it has not yet been preserved in a new off-host release.

## Post-hoc editor audit (our analysis, not organizer scores)

Checked all 258 preserved generated Task 2 draft/edit pairs using exact text
comparison, with editor input drafts verified against the parsed first-call
outputs. 245 were unchanged (94.96%), two shorter and eleven longer. No changed
pair had equal character length. Administrative closures are outside this
population. `submitted-editor-audit.json` binds counts to a hash of the receipt
inventory. This is not a new model run or a controlled realism evaluation: the
original drafts lack matched human ratings, so editor benefit/harm remains
unidentified. The conservative editor instruction explicitly says not to
shorten automatically. In Task 2, the last two voice examples are the simulator's
own earlier turns, so reinforcing its generated register is a plausible mechanism,
not a measured causal explanation. The stop decision is prompted, not calibrated
against positive researcher stop labels in the supplied training export.
