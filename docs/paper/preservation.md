# Private paper evidence preservation

Snapshot created October 10, 2026. **All available artifacts from the nine
recorded organizer runs are now inside the stable local repository directory.**
They are intentionally ignored by git and absent from GitHub. Public git contains
the [run manifest](../../submissions/manifest.json), aggregate evidence hashes,
method descriptions and offline preservation tools.

## Location and contents

```text
/home/npatta01/data/competitions/trec-usersim-2026/
  data/private-evidence/2026-10-10-paper-evidence/
    manifest.json                   private file/source inventory
    SHA256SUMS                      per-file content hashes
    organizer-and-model-runs/        newer organizer runs and editor studies
    official-data-and-development/  export, older runs and development studies
    research-notes-original/        dated notes and reviews from original checkout
    research-scripts-original/      historical experiment implementations
    research-tools-original/        historical helper tools
    research-starter-original/      original organizer adapter source
    provenance/                    source tar, checkout pins/status, environment
```

The verified snapshot contains **7,403 files / 130,615,399 bytes**. Its
[public aggregate index](evidence-manifest.json) binds component counts, sizes
and inventory hashes to the private manifest and checksum file. Its seven source
components preserve the detailed evidence behind the research summaries, not
only the selected submissions. Original records were checked against their
copies and remain unchanged in their original locations.

For each newer run, preserve input/scenario/history, exact model request and raw
response, generated and selected text, organizer request/received response,
cost, state/configuration, frozen sources and recovery/audit evidence when saved.
Do not fabricate a successful receipt for a timeout. Older formats differ: the
first Task 1 debug stores model requests/responses in `case-NNNN.json`, and has
only its final organizer request/receipt. See the [run index](../../submissions/README.md).

The provenance source tar pins public commit
`57772288db3476cadbed28da7008900a596154ae`, immediately before the paper-pack
changes. Historical experiment sources include uncommitted files, so original
checkout status is recorded; a Git revision alone cannot identify them.
Run-specific manifests and `frozen/` snapshots take precedence for executed code.
The frozen runner's package/Python versions were observed during preservation,
not necessarily recorded at original execution. Historical hardware utilization,
latency distributions and an independently frozen hosted model version are not
established by that environment file.

## Verify or inspect without making calls

From a checkout containing the preservation tools:

```bash
python scripts/archive_paper_evidence.py verify \
  /home/npatta01/data/competitions/trec-usersim-2026/data/private-evidence/2026-10-10-paper-evidence
```

This verifies inventory, sizes, every SHA256 and `SHA256SUMS` using only local
files. Add `--check-sources` to compare the original sources as well; it should
fail if originals later change or disappear, while the standalone snapshot
continues to verify. The manifest's absolute original paths are private.

Regenerate the public run index from the snapshot:

```bash
python scripts/index_submission_evidence.py \
  --archive /home/npatta01/data/competitions/trec-usersim-2026/data/private-evidence/2026-10-10-paper-evidence \
  --output submissions/manifest.json \
  --official-csv docs/paper/submission-results.csv
```

For a new snapshot, use `archive_paper_evidence.py archive --help`, explicitly
name the task-scoped source directories and choose a **new**, ignored private
destination outside every source. Existing archives cannot be overwritten. Do
not point an API runner at a copied checkpoint: source/path pins and lifecycle
semantics are retained for inspection, not migrated or reset.

## Privacy and durability

The archive uses restrictive directory/file permissions. Credential files,
environment files, symlinks and cache/runtime directories were excluded;
readable content was checked for recognized credential patterns without printing
values. Provider-encrypted reasoning blobs are preserved intact but excluded
from text-pattern scanning: random encrypted strings can resemble keys. This
scan does not decrypt those blobs or guarantee detection of every possible
credential format. Actual keys under `~/.config/trec-usersim/` were never read
or copied for this task. Codex session histories are not part of the snapshot.

`/data/private-evidence/` is excluded in the PR's `.gitignore` and the common
local git exclude file, protecting the older stable checkout before merge.
Never use `git add -f` on this archive. Keeping exact participant/model records
locally does not authorize pushing them to GitHub or including them in a public
paper. Any future examples need the appropriate publication rights.

This is a single-machine snapshot, **not an off-host backup**. The immutable
archive should remain intact while run state and later results evolve. A future
authorized encrypted/private backup and future organizer score reports should
be indexed separately, without overwriting this evidence.
