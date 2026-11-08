# Project handoff — October 10, 2026

**Both official baselines are complete.** Debug v5 is intentionally paused.
No further submission is needed for this baseline; this document does not
authorize another run. Next: review organizer evaluation when available.

Submission deadline check, October 10: the organizers extended the deadline to
**October 9, 2026 (Anywhere on Earth)** in their
[October 7 announcement](https://groups.google.com/d/msgid/trec-usersim/1b15da6d-1d40-4124-9698-a89a4ea9e746n%40googlegroups.com).
That window ended October 10 at 12:00 UTC / 08:00 Eastern. The public track page
still lists the superseded October 7 date. The separate notebook-paper deadline
and format are not yet verified; see the [paper checklist](paper/README.md).

The [thread-independent continuation guide](continuity.md) records the reading
path, retained user requirements, private readers and credential locations.
The project should be resumable from these files without the original chat.

| Official task | Completed work | Model cost |
|---|---|---:|
| Task 1 | 62 predictions, 124 model calls | $0.029373225 |
| Task 2 | 57 processed: 49 normal stops + 8 administrative closures; 266 submitted turns, 516 model calls | $0.173554630 |

The [submission ledger](submission-ledger.md) owns run IDs, quotas and private
input/output locations. Debug v5 paused at 886 saved turns, with 129 normal
endings, 38 administrative closures and one unfinished conversation; it is not
a completed debug run.

The [paper evidence map](paper/README.md) now links the method, experiments,
figures and missing results. A [verified private GitHub release](artifacts.md)
preserves all nine run directories, original development evidence and rendered
readers; [public metadata](../submissions/manifest.json) includes per-run hashes/costs.
All 7,408 evidence files were verified after a fresh download and restoration
without the original paths. Local copies are caches. Official score reports,
author metadata and confirmed paper requirements remain pending.

## Selected behavior

See the [illustrated architecture](task2_architecture.md). Luna generates the
researcher using the baseline persona/goal projection and full utterance text,
then makes one editor call. Task 1 official explicitly selected `fidelity`;
the CLI compatibility default is `style`. Task 2 uses `style` and preserves its
draft stop boolean. No compaction, retrieval or repeated judge/retry is enabled.

Exact [input projection](research/official-data-evidence.md#what-the-model-receives)
and [tested alternatives](research/method-decisions.md) are separate evidence.
The ordinary official Task 2 CLI keeps its completed-debug gate. The submitted
baseline used a separately reviewed private exception bound to the user's
specific audited paused-prefix decision; it is not a general bypass.

## Frozen execution versus public source

The completed Task 2 run is frozen to its original source paths/hashes at
`/tmp/trec-task2-debug-pr`. Updated public code is not a migration of that run.
Keep its manifest, source snapshots, recovery policy and original receipts.
Changed source/configuration or moving the checkout blocks ordinary resume.
Never reuse a historical run ID in a new empty directory.

The final HTTP428 was initially rejected by our parser. A reviewed local
reconciliation preserved original evidence and advanced the accepted final
message once, without a POST or model call. Public source now shares completion
classification and preserves unknown protocol errors. Historical worker/watcher
failed exits remain recorded; reconciled state/audit are complete.

Private Task 2 artifacts are under
`/home/npatta01/data/trec-usersim-runs/task2-official-luna-20261009-v1/`.
`integrity-audit.json`, final status/summary/budget, `terminal-reconciliation/`
and source-pinned `completion-audit-tools/` retain completion evidence. The
[recovery guide](research/task2-recovery-plan.md) explains the exact boundaries.

## Safe inspection and limits

Use the [Task 1 guide](task1_runner.md) and [Task 2 setup](task2_debug_runner.md).
Task 1 has an offline preview. Both Task 2 CLIs support `--help` but refuse
execution without `--run`. Adding that flag permits real organizer/model calls.
Keys remain outside git in `~/.config/trec-usersim/organizer.key` and
`~/.config/trec-usersim/openrouter.key`.

Runtime tests and private replay verify integration, not researcher realism.
Voice, invented knowledge/actions and excessive persistence remain concerns.
The training export has no positive researcher-stop labels. No competition score
or whole-run quality rate is recorded. Keep debug paused and private evidence
intact; future tests need matched hard cases and successful controls.

The [earlier detailed handoff](research/archive/2026-10-10-handoff-history.md)
preserves the full operator record.

## November 7 preliminary results update

Organizer results are now downloaded and incorporated in the manuscript. See [result interpretation](paper/organizer-results-2026-11-07.md) for metrics, rated sample sizes, provenance and limitations. Earlier pending-score statements are historical. Author details are complete. Paper format and submission requirements remain unconfirmed. Debug v5 stays paused.
