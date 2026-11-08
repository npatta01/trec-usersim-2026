# Restore private research evidence

Use an account authorized to access this private repository. No model key,
organizer token, paid model call or organizer request is required to inspect it.

Choose a private directory outside any public repository or served web root:

```bash
umask 077
mkdir -p /private/location/trec-usersim-evidence
cd /private/location/trec-usersim-evidence
gh release download paper-evidence-2026-10-10 \
  --repo npatta01/trec-usersim-2026-private-evidence
sha256sum --check SHA256SUMS
tar -xzf trec-usersim-paper-evidence-2026-10-10.tar.gz
mkdir -p source/code
tar -xf source/trec-usersim-source-*.tar -C source/code
python source/code/scripts/archive_paper_evidence.py verify "$PWD/paper-evidence"
python source/code/scripts/archive_paper_evidence.py verify "$PWD/thread-continuity"
```

The checksum check binds the downloaded bundle, artifact index and this restore
guide. Each snapshot's verifier checks its inventory, file sizes, every content
hash and checksum file without requiring the original machine or source paths.
Do not add `--check-sources` on a new host: original paths are provenance, not
dependencies of standalone verification.

`artifact-index.json` identifies the source commit and both private manifest
hashes. The bundle contains:

| Path | Use |
|---|---|
| `paper-evidence/organizer-and-model-runs/` | Newer run directories and fidelity/editor comparisons |
| `paper-evidence/official-data-and-development/` | Supplied export, older runs and other development studies |
| `paper-evidence/research-*-original/` | Detailed research notes and historical implementations |
| `paper-evidence/provenance/` | Earlier source tar, checkout status and observed environment |
| `thread-continuity/` | Three self-contained readers and continuity verification notes |
| `source/` | Main-source tar pinned by the artifact index |

Read the current main repo's continuity guide, project handoff and paper evidence
map before continuing work. Frozen run-specific sources/manifests govern what
actually executed; a current source checkout may differ. Preserve normal
researcher stops separately from administrative error closures. Never replay
saved accepted or uncertain messages, reuse an old run ID as a new run, or start
another submission merely to reconstruct evidence.

Credentials were not uploaded. A new host must obtain authorized credentials
from the organizer team and model-provider account separately. No pasted chat
key is needed to restore the research record. Publication rights for real
participant excerpts remain separate from private archival access.
