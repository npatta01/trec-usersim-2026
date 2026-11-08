> Historical companion snapshot, preserved unchanged below. The current release is
> https://github.com/npatta01/trec-usersim-2026/releases/tag/paper-evidence-2026-10-10.
> Original private-custody instructions describe the October snapshot; the owner authorized public consolidation on November 7, 2026.
> Use [current restoration instructions](../artifacts.md).

# Private TREC UserSim evidence

This repository must remain **private**. It holds release archives of participant
records and model outputs which are not distributed with the main source repo.
Do not make its releases public or copy their raw contents into documentation.

Source, method descriptions, ledgers and diagrams are in
[trec-usersim-2026](https://github.com/npatta01/trec-usersim-2026).
This companion preserves exact available run/development evidence independently
of the original chat, Codex worktrees, temporary folders and local machine.

## Evidence release

[Paper evidence, October 10, 2026](https://github.com/npatta01/trec-usersim-2026-private-evidence/releases/tag/paper-evidence-2026-10-10)
contains:

- All available records from nine organizer runs: two official and seven debug.
- The supplied official training export and detailed development outputs,
  original notes/scripts, frozen execution sources and recovery/audit evidence.
- Current official, historical debug and invented-example rendered readers.
- A source tar pinned to the main project's merged documentation/paper-pack
  commit, with the offline archive verifier.
- An artifact index, download checksums and [restoration instructions](RESTORE.md).

The two private snapshots contain 7,408 evidence files. Credentials and raw
chat/session histories are deliberately excluded. The first Task 1 debug's
per-prediction organizer receipts were not saved; this archive cannot recreate
them. Other evidence/accounting limits are recorded in the main repo's ledgers.

The release is an inspection/research backup, **not** a fresh organizer submission
or a migrated runnable checkpoint. Local files are caches after upload is
independently verified. Verification metadata and synthetic test reports are
tracked here; raw records remain in the release asset rather than Git history.

## Verified restoration

The four release assets were freshly downloaded and matched GitHub's sizes and
SHA256 digests. The included, hash-checked source verified all 7,408 evidence
files without their original paths. Nine synthetic preservation/index tests
passed. See [remote custody receipt](remote-verification.json) and
[full restore report](restore-verification.json).

For an automated offline recheck (Python 3.12 or newer), download the four
assets and run:

```bash
python verify_download.py /private/download /private/new-restore \
  --report /private/verification.json
```

The restore directory must be new. This command performs no network, model or
organizer calls. Keep the release tag and assets unchanged; add a new dated
release for future useful evidence rather than overwriting this snapshot.

## Later organizer evidence

The [submission deadline extension](announcements/submission-deadline-extension-20261007.json)
records the verified October 7 organizer announcement and its derived UTC/Eastern
cutoff. This small metadata record is kept in git; the immutable release assets
are unchanged. It does not establish the separate notebook-paper deadline.
