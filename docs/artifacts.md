# Artifact custody and restore

Updated November 7, 2026. Useful project artifacts are preserved on GitHub;
local data directories, rendered pages and temporary worktrees are no longer
their only copies. No model calls or organizer requests were made for this work.

## Where things live

| Material | Durable location |
|---|---|
| Supported code, method decisions, diagrams, ledgers and paper plan | [Main source repository](https://github.com/npatta01/trec-usersim-2026) |
| Exact training export, all available submission records and development results | [Evidence release](https://github.com/npatta01/trec-usersim-2026/releases/tag/paper-evidence-2026-10-10) |
| Historical scripts/notes, frozen code and environment/source provenance | The same evidence release, in `paper-evidence/` |
| Three self-contained rendered readers | The same evidence release, in `thread-continuity/` |
| Release metadata, checksums and restoration verification | [Preserved companion records](evidence/), plus the [safe custody receipt](private-artifact-release.json) here |
| Organizer/provider credentials | Separate account access; deliberately absent from git and release assets |

The owner authorized consolidation into this public repository on November 7, 2026.
The four original release assets are preserved byte-for-byte, including historical
restore instructions that name the retired repository. Use the download command below.
Original companion documentation and receipts are retained under [evidence/](evidence/).
The complete companion Git history is preserved as `companion-history.bundle` in the release.
See the [migration verification](evidence/migration-verification.json).

## Release contents and verification

Release tag: `paper-evidence-2026-10-10`. The four original assets are preserved, alongside the companion Git-history bundle:

- `trec-usersim-paper-evidence-2026-10-10.tar.gz`: 35,458,724 bytes; two immutable
  evidence snapshots and a source tar pinned to merged main commit
  `60382f8950a3ab2a219c07e85b32c9ed222d4a81`.
- `artifact-index.json`: source pin, bundle hash and snapshot inventory hashes.
- `RESTORE.md`: restoration instructions that require no model or organizer key.
- `SHA256SUMS`: checksums for the bundle, index and restore guide.

The snapshots contain **7,408 evidence files / 133,520,866 bytes**: 7,403 original
paper-evidence files and five continuity files. All nine recorded organizer runs
are covered: two official and seven debug. Model-only development work is also
preserved. The archive contains exact available input, request, output, receipt,
checkpoint and frozen-source files; formats differ across older runs.

A fresh authenticated download matched all four GitHub asset digests and sizes.
The bundle was extracted into a new private directory, then its included source
verified every evidence file, inventory and checksum **without accessing the
original source paths**. The included preservation/index tests also passed
(nine tests). The [verification receipt](private-artifact-release.json) records
hashes, coverage and current repository visibility.

The first Task 1 debug's per-prediction organizer POST receipts and start receipt
were never saved. They cannot be reconstructed by archiving. The
[submission ledger](submission-ledger.md) and [run index](../submissions/README.md)
retain this and the debug-v3 checkpoint/receipt accounting difference. Completed
official counts are reconciled; completion remains separate from effectiveness.

## Restore on another machine

The release is available in this public repository.
Choose a private location outside a public repository or served directory:

```bash
umask 077
mkdir -p /private/location/trec-usersim-evidence
cd /private/location/trec-usersim-evidence
gh release download paper-evidence-2026-10-10 \
  --repo npatta01/trec-usersim-2026
sha256sum --check SHA256SUMS
tar -xzf trec-usersim-paper-evidence-2026-10-10.tar.gz
mkdir -p source/code
tar -xf source/trec-usersim-source-*.tar -C source/code
python source/code/scripts/archive_paper_evidence.py verify "$PWD/paper-evidence"
python source/code/scripts/archive_paper_evidence.py verify "$PWD/thread-continuity"
```

Both verifiers should report `status: verified`, with 7,403 and five files
respectively. Do not use `--check-sources` on a new host; absolute original paths
are provenance, not restore dependencies. The [preserved companion directory](evidence/) contains
`verify_download.py` and the saved restore report for automated offline checking.

Consult the [continuation guide](continuity.md), [project handoff](project-handoff.md)
and [paper evidence map](paper/README.md) before continuing. Frozen run-specific
sources govern what executed; current source may differ. These are research
inspection archives, not migrated runnable checkpoints. Never replay saved
accepted or uncertain messages or restart completed submissions to recover data.

## Future preservation

Keep the release tag and assets unchanged. Preserve new useful records in a new
dated release with explicitly approved visibility, and update the main repo's artifact index and handoff only
after download and standalone verification. Keep current source/docs in git;
rendered readers are derived copies. Credentials, caches and raw Codex session
histories are outside the research archive scope. Record decisions and evidence
in canonical repo docs instead of depending on a chat transcript.

Local evidence copies can remain as caches. Their original inventories retain
creation-time `off_host_backup: false`; the later remote receipt establishes
verified GitHub custody. No source, frozen checkpoint or original evidence was
deleted during preservation.
