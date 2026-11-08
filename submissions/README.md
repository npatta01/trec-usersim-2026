# Submission records

There are **nine organizer runs: two official and seven debug**. Both official
runs are complete. The [human-readable ledger](../docs/submission-ledger.md)
owns status/quota interpretation; [manifest.json](manifest.json) is the
receipt-based machine-readable inventory. Model-only experiments are separate
and are preserved with the [paper evidence](../docs/paper/README.md).

Public git contains metadata and hashes. The exact available inputs, model
requests, drafts, editor outputs, organizer requests/receipts, frozen code,
checkpoints and recovery evidence are in the
[GitHub evidence release](../docs/artifacts.md), with an ignored local
cache inside the stable repo directory. See [snapshot verification](../docs/paper/preservation.md).
Cloning the main source repo does not download release assets; use the separate
private release's restore instructions. Creation-time local inventory limitations
remain unchanged in the manifest; the [remote receipt](../docs/private-artifact-release.json)
records the later verified off-host copy.

| Task / mode | Run suffix | Status | Priced model receipts | Model cost (USD) |
|---|---|---|---:|---:|
| Task 1 debug | `task1-debug-20261005-v1` | Complete: 64 predictions | 64 | 0.016750475 |
| Task 1 debug | `style-task1-debug-20261006-v1` | Complete: 64 predictions | 128 | 0.037675500 |
| Task 1 official | `fidelity-task1-official-20261006-v1` | Complete: 62 predictions | 124 | 0.029373225 |
| Task 2 debug | `task2-debug-20261006-v1` | Halted: 3 checkpointed turns | 8 | 0.004248240 |
| Task 2 debug | `task2-debug-20261006-v2` | Halted: 4 checkpointed turns | 10 | 0.005123280 |
| Task 2 debug | `task2-debug-20261007-v3` | Halted: 3 checkpointed turns | 8 | 0.003852275 |
| Task 2 debug | `task2-debug-v4` | Halted: 17 checkpointed turns, 3 normal endings | 36 | 0.014966260 |
| Task 2 debug | `task2-debug-v5` | Intentionally paused: 886 saved turns, 129 normal endings, 38 administrative closures, 1 unfinished | 1,696 | 0.664036040 |
| Task 2 official | `style-task2-official-20261009-v1` | Complete: 57 processed, 49 normal endings + 8 administrative closures | 516 | 0.173554630 |

Full run IDs, archive-relative directories, state hashes and per-run file
inventory digests are in the manifest. Each official row consumes one organizer
allowance, regardless of predictions or model-call count. Counts across training,
debug and official pools are not one independent evaluation set.

## Evidence gaps and accounting

The first Task 1 debug run retains all 64 organizer input/model request/response
records, plus the final accepted organizer request and HTTP428 completion. Its
start receipt and per-prediction organizer POST receipts were not saved; the
archive cannot reconstruct them as historical receipts. Later Task 1 runs retain
each submission payload and organizer reply.

Task 2 debug-v3 retains eight priced model receipts, including the draft/editor
pair for the fourth attempted turn. Its checkpoint counts only six calls and
$0.002196115. The complete retained receipt sum is $0.003852275, a difference of
$0.001656160. Both values and the original state hash are preserved; the ledger
now reports the receipt sum. Checkpointed turns are not the same as attempted
or saved submissions. Receipt files can also describe transport failures,
so their count alone is not an accepted-turn count.

Official coverage and receipt costs reconcile. No official evaluation score or
whole-run realism rating is currently recorded. Administrative closures are
operational actions, not simulated natural stopping behavior. Index generation
and archive verification use no organizer or model API calls.
