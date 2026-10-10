# Project handoff — October 10, 2026

**Both official baselines are complete.** Debug v5 is intentionally paused.
No further submission is needed for this baseline; this document does not
authorize another run. Next: review organizer evaluation when available.

| Official task | Completed work | Model cost |
|---|---|---:|
| Task 1 | 62 predictions, 124 model calls | $0.029373225 |
| Task 2 | 57 processed: 49 normal stops + 8 administrative closures; 266 submitted turns, 516 model calls | $0.173554630 |

The [submission ledger](submission-ledger.md) owns run IDs, quotas and private
input/output locations. Debug v5 paused at 886 saved turns, with 129 normal
endings, 38 administrative closures and one unfinished conversation; it is not
a completed debug run.

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
