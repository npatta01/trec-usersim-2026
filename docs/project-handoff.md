# Project handoff — October 10, 2026

**Both official baselines are complete.** There is one completed official run
for each task. Task 1 submitted 62 predictions; Task 2 processed 57 conversations.
Debug v5 is intentionally paused, not complete. No further submission is needed
for this baseline, and no additional official run is authorized by this handoff.

| Work | Verified outcome | Outstanding limit |
|---|---|---|
| Task 1 official | 62 predictions, 124 model calls, $0.029373225 | No organizer score or whole-run realism rating yet |
| Task 2 official | 57 processed: 49 normal endings + 8 administrative closures; 266 submitted turns, 516 model calls, $0.173554630 | Closures are error handling, not natural user behavior |
| Task 2 debug v5 | Paused at 886 saved turns: 129 normal endings + 38 administrative closures + 1 unfinished conversation | Audited prefix; no debug-completion claim |
| Public runtime | 139 synthetic tests / 92 subtests pass | Two pre-existing organizer-starter test modules cannot collect |

The [submission ledger](submission-ledger.md) has run IDs, quotas, private artifact
locations and receipt patterns. It distinguishes training records, debug cases,
official predictions, conversations, model calls and run allowances.

## Selected implementation

We simulate the researcher seeking datasets; the organizer supplies the search
assistant. The model is `openai/gpt-6-luna`, reached through OpenRouter with
OpenAI-only routing, no provider fallback and frozen price limits. The request
sets `data_collection: "deny"`; this is a routing setting, not a blanket
data-retention guarantee.

```mermaid
flowchart LR
    I[Supplied scenario and current history] --> P[Build researcher-role messages]
    P --> D[Luna draft]
    D --> E[One Luna editor call]
    E --> S[Save request, output and intended submission]
    S --> O[Organizer API]
    O --> V[Validate reply or completion and checkpoint]
```

- **Task 1:** rebuild from each supplied prefix. The official run explicitly
  selected `--editor-policy fidelity`: voice editing plus a narrow repair of
  unsupported claims that the researcher performed an external action. The CLI's
  compatibility default remains `style`. Predictions never become evidence in
  the next supplied prefix.
- **Task 2:** generate strict JSON containing text and a boolean stop decision,
  then apply the existing style editor. Code retains the draft's stop boolean.
  Within a conversation, retain the full available utterance text; reset persona,
  goal and history on a validated new conversation.
- **Context:** render the organizer-baseline persona groups, goal
  context/topic/discipline, familiarity and known datasets. Other raw scenario
  metadata and message annotations are retained privately but are not all
  rendered. See the exact [input projection](research/official-data-evidence.md#what-the-model-receives).
- **Roles:** researcher history is model `assistant`; search-assistant history is
  model `user`; instructions and scenario are model `system`. Requests explicitly
  resend the context. There is no hosted conversation-memory API, compaction,
  state planner, few-shot retrieval or repeated judge/retry loop enabled.

See the [architecture](task2_architecture.md) for the conversation and recovery
diagrams. The [method decisions](research/method-decisions.md) explain the tested
alternatives and why they were not promoted.

## Completion and recovery evidence

Task 1 completion is confirmed by its explicit terminal receipt and saved
organizer status/summary. For Task 2, the final HTTP428, fresh organizer status
and summary agree on 57 processed and zero remaining. The final audit reproduces
all cached model requests, submitted texts/stop flags, conversation IDs,
administrative recovery evidence and counters. It passes 91 synthetic controls.

The Task 2 parser initially rejected the organizer's longer, exact run-ID-bound
completion text. Recovery then masked that protocol error. A separately reviewed
local reconciliation archived the prior halted state and secondary error, bound
the final receipt to fresh GET evidence, preserved frozen sources, and advanced
the accepted final message once. It sent no POST and made no model call. The
public parser now shares Task 1's completion classifier, and recovery dispatches
only classified evidence; unknown protocol errors remain visible.

The original official worker and watcher retain historical failed exit records
from that parser error. The reconciled local checkpoint and final audit are
complete. Do not use an old process exit alone as current run status.

### Frozen execution versus public source

The official Task 2 run remains bound to its original source paths and hashes in
`/tmp/trec-task2-debug-pr`. Updated public source is not an automatic migration of
that run. Preserve `manifest.json`, `frozen/`, recovery policy and all original
receipts. Moving a checkout or changing source/configuration blocks ordinary
resume. Never reuse a historical run ID in an empty output directory.

Private artifacts live at
`/home/npatta01/data/trec-usersim-runs/task2-official-luna-20261009-v1/`.
Key completion evidence is `integrity-audit.json`, `final-status.json`,
`final-summary.json` and `final-budget.json`. `terminal-reconciliation/` retains
the original state/error and bound reconciliation intent/result;
`completion-audit-tools/` and `completion-terminal-audit-source-review.json`
preserve the reviewed checker source and hashes. See the
[recovery record](research/task2-recovery-plan.md) for the dated sequence.

The ordinary official Task 2 CLI still requires completed, reviewed debug
evidence. The actual baseline used a separately reviewed private operator
launcher bound to the user's specific decision to submit after auditing the
paused debug prefix. This is not a general bypass of the public CLI gate.

## Safe inspection and future work

From the repository root, use the setup and offline tests in the
[Task 2 execution guide](task2_debug_runner.md). These commands do not execute a
submission:

```bash
.venv/bin/python scripts/run_task1.py --help
.venv/bin/python scripts/run_task1.py --mode debug \
  --run-id DOCUMENTATION_PREVIEW --output-dir /tmp/trec-usersim-preview-unused
.venv/bin/python scripts/run_task2_debug.py --help
.venv/bin/python scripts/run_task2_recovery.py --help
```

Only Task 1 has a preview. Task 2 without `--run` refuses execution; `--help` is
safe. Adding `--run` permits authenticated organizer/model work and is not a
documentation check. Keys remain outside git at
`~/.config/trec-usersim/organizer.key` and `openrouter.key` in the same directory.

Next, review organizer evaluation when available. No further run is required to
finish this baseline. Preserve private artifacts and keep debug v5 paused. For
future method work, use whole-conversation splits and matched comparisons that
include difficult cases and successful controls. Do not optimize brevity as a
substitute for persona/context fidelity or treat synthetic stress probes as
human ground truth.

Remaining concerns are overly polished or weakly differentiated voice, invented
researcher knowledge/actions, acceptance of questionable recommendations, and
excessive persistence. Narrow fidelity repair has evidence on Task 1 development
cases; it does not solve those broader concerns. Task 2 stopping is inferred,
because the training export has no positive researcher stop labels. Integration
completion is not a realism score, and there is no demonstrated universal
conversation-length failure threshold. A shorter timeout grace is a future
operational proposal; the completed official run retained 1,800 seconds.
