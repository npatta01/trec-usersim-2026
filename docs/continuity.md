# Continue without the original chat

This is the durable starting point for a new agent or collaborator. Project
continuation should use the repository and saved evidence, not the archived
conversation. The chat is not the source of truth for run counts, method choices
or permission to execute a historical command.

## Start here

1. Read the [current handoff](project-handoff.md), then the
   [architecture](task2_architecture.md) and [method decisions](research/method-decisions.md).
2. Use the [submission ledger](submission-ledger.md) and
   [run manifest](../submissions/manifest.json) for run IDs, coverage, costs,
   remaining allowances and the distinction between natural stops and error closures.
3. Use the [paper evidence map](paper/README.md), [outline](paper/outline.md),
   [experiment ledger](research/experiment-ledger.md) and detailed private notes
   for writing. Official scores, author information and venue requirements are
   still unresolved; absence from these records does not prove scores were never released.
4. Use the [GitHub release and restore guide](artifacts.md) to obtain
   exact records, and the [recovery guide](research/task2-recovery-plan.md) before
   any future authenticated work. Historical instructions are not current run authorization.

Public source and documentation are in
[npatta01/trec-usersim-2026](https://github.com/npatta01/trec-usersim-2026).
The documentation, viewer and paper pack from [PR #3](https://github.com/npatta01/trec-usersim-2026/pull/3)
were verified merged on October 10, 2026. Check HEAD and working-tree status when
entering an older checkout; stale worktrees need not reflect GitHub `main`.

## Decisions and user requirements to retain

- We implement a researcher simulator for both tasks, not a synthetic training
  dataset. It must react to the supplied goal, persona and actual history across
  unseen situations, rather than hard-code fixes for specific training failures.
- Fidelity means a plausible reaction, knowledge, stance, needs and voice.
  Conciseness and correct speaker alone are insufficient. Preserve reasonable
  changes of mind; do not turn every goal preference into a mandatory checklist.
- The official training export is separate from the supplementary collection.
  Its profiles are not verified participant IDs, turns within a conversation
  are correlated, and assistant end flags are not human-stop supervision.
- The selected method, editor-policy distinction and unselected ideas are in
  the method decisions. Full available utterance history is retained; compaction,
  retrieval, planning and repeated critic/retry remain unselected alternatives.
- Prompts, code, controls and contextual judgments must be checked before
  drawing conclusions. Small repeated or unblinded screens cannot establish
  general human realism. Provider/runtime failure is not model-quality evidence.
- Both official baselines are complete. Debug v5 is deliberately paused.
  Completed submissions must not be restarted to reconstruct evidence; never
  replay an accepted or uncertain POST. Frozen sources and terminal reconciliations
  take precedence over current public code when describing executed behavior.
- Local models were an initial development preference, not a track restriction.
  Paid hosted calls and official runs were later explicitly authorized and
  recorded. This continuity task authorizes preservation, not more inference
  or submissions. Future work follows its current user instruction and recorded scope.
- Public docs contain source, synthetic examples and aggregates. Keep exact
  participant/model records and credentials private. Public advisor lanes may
  receive public-shareable source/design and newly synthetic material; provider
  reuse permissions are not blanket permission to share participant records.

## Private records survive outside this machine

The [GitHub evidence release](artifacts.md) is the durable artifact copy.
It contains all available run/development records, the supplied official export,
three rendered readers and pinned source. A fresh download and standalone restore
verified every one of its 7,408 evidence files. Source and current handoff docs
are versioned in the main repo; cloning it alone does not fetch release assets.
The owner authorized consolidation into this repository’s public release on November 7, 2026. See [migration verification](evidence/migration-verification.json).

The stable local evidence root is:

```text
/home/npatta01/data/competitions/trec-usersim-2026/data/private-evidence/
  2026-10-10-paper-evidence/      all available run/development records
  2026-10-10-thread-continuity/   saved rendered readers and continuity diagnostics
```

The first snapshot contains 7,403 files, with the official export, all nine run
directories, original experiment notes/scripts, source snapshots and environment
provenance. The addendum preserves five files / 2,905,467 bytes: three rendered
readers and two task-scoped provenance files. The [addendum index](thread-continuity-evidence.json)
contains aggregate counts/hashes only. Both snapshots are ignored by git and
outside `.codex/worktrees` and `/tmp`. These local directories are caches of the
release, and neither is needed to restore on another machine. They are inspection
copies, not runnable resume directories.

The first Task 1 debug's missing per-prediction organizer receipts and the
debug-v3 checkpoint accounting gap remain explicit in the ledger. Preservation
does not recreate missing records. Credentials are deliberately excluded:
their locations are `~/.config/trec-usersim/organizer.key` and
`~/.config/trec-usersim/openrouter.key`. Both files existed with mode `0600` at
this audit; contents were not read and token validity was not tested. A new host
can restore the authorized private data from GitHub, but obtains credentials
separately from the organizer and provider accounts. No key from this chat is
needed to inspect or restore the research record.

The [private viewer guide](run_viewer.md) retains exact links and rebuilding
instructions. The [official run reader](https://npatta01-framework.tail481212.ts.net/plans/trec-usersim-run-viewer/)
contains 62 Task 1 cases and one complete Task 2 conversation. The
[older debug reader](https://npatta01-framework.tail481212.ts.net/plans/trec-usersim-conversations/)
and [synthetic walkthrough](https://npatta01-framework.tail481212.ts.net/plans/trec-usersim-demo/)
are separate. All three live pages matched their saved files during this audit;
the existing Serve mapping remained tailnet-only. Archived HTML is self-contained
and can be inspected privately if that service later changes.

## Archival check and next action

The evidence indexes, exact saved records, unresolved questions, chosen and
rejected methods, credential locations and rendered readers are all recorded
outside this conversation. Raw chat/session logs and credential values are not
copied into the project. No project inference/recovery Python process was found
at this check; there is no active run to continue simply because this chat is archived.

Next work is the paper: obtain organizer score reports and confirmed notebook
instructions, then write around the submitted method. Use the paper checklist
for author metadata, example rights and evaluation limits. No new model or
organizer calls were made for this preservation audit.

No useful preserved research artifact depends solely on this thread, its
attachments, a temporary worktree or this host. Credentials remain outside git
and release assets by design. Do not treat local cleanup as authorization to
delete the GitHub release, frozen checkpoints or source worktrees.
