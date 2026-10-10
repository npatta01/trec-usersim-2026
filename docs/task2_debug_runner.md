# Task 2 execution guide

The runner repeatedly generates researcher messages against the organizer's
search assistant. Read the [illustrated architecture](task2_architecture.md)
first. Both official baselines are complete; debug v5 is intentionally paused.
This guide is not authorization to resume them or start another run.

## Setup and offline verification

From the repository root:

```bash
python -m venv .venv
.venv/bin/pip install -r simulator/requirements-dev.txt
.venv/bin/python -m unittest discover -s tests -p 'test_*.py'
```

The runtime suite has 139 tests / 92 subtests (October 10). Inputs/transports are
synthetic; no credentials, training export, paid inference or organizer access
are needed. Historical studies live in [experiments](../experiments/README.md)
and are not runtime dependencies.

The legacy command `.venv/bin/python -m pytest simulator/tests` cannot collect
`test_response_strategies.py` and `test_user_simulator.py`: both import removed
`PersonaDefinition`. These pre-existing starter failures reproduce on base
`45de4e1`; they are separate from the runtime `tests/` suite.

## Inspecting the CLI without execution

```bash
.venv/bin/python scripts/run_task2_debug.py --help
.venv/bin/python scripts/run_task2_recovery.py --help
```

Neither Task 2 CLI has a preview. Without `--run`, it refuses execution. Task 1
has a separate [offline preview](task1_runner.md#preview-and-modes).

## Authenticated execution

Only for a separately authorized new run: store owner-readable keys outside
this checkout at `~/.config/trec-usersim/organizer.key` and
`~/.config/trec-usersim/openrouter.key`. Verify NP Labs team identity and quota.

```bash
.venv/bin/python scripts/run_task2_debug.py --run \
  --run-id YOUR_AUTHORIZED_UNIQUE_RUN_ID \
  --output-dir data/official/YOUR_PRIVATE_RUN_DIRECTORY
```

A new start consumes one debug allowance. The default runner uses only
`/task2/debug/start` and `/task2/debug/continue`; it halts on server failures.
Default guards are $3 cumulative reservations, 500 total researcher turns and
30 per conversation. Hitting a guard halts the run; it does not invent a natural
researcher stop. Private outputs are excluded from public git.

## Explicit recovery wrapper

`scripts/run_task2_recovery.py --run` adds narrowly verified backend-error and
original-timeout recovery. It never blindly reposts a saved researcher turn.
See the [recovery guide](research/task2-recovery-plan.md) before using it.

| Selector | Behavior |
|---|---|
| `--mode debug` or `--mode official` | Required; selects isolated organizer routes |
| `--run-id ID --output-dir DIR` | Required; binds a unique new run or its original frozen directory |
| `--cap-usd AMOUNT` | Finite positive reservation ceiling; default $3 |
| `--max-total-turns COUNT` | Positive integer; default 500 |
| `--max-operational-skips COUNT` | Positive absolute closure bound; default 24 |
| `--debug-evidence-dir DIR --debug-review-file FILE` | Required for ordinary official mode; completed debug and quality review must bind state, source, completion and policy |

The fixed outage circuits remain 25% with denominator floor 8 and three
consecutive closures. Original-timeout polling is every 30 seconds with a
1,800-second first-observation grace. Unknown outcomes or uncertain closes halt.
All selected limits/policies are frozen; a larger flag does not amend a run.
Official mode requires separate submission authorization and cannot adopt a
debug run ID/directory. The actual baseline's private paused-prefix operator
exception is explained in the [handoff](project-handoff.md).

## Resume safeguards and private evidence

Preserve exact requests, model responses/costs, organizer receipts, timestamps,
pending markers, manifest and source snapshots. Completed receipts are reused;
an uncertain pending marker blocks automatic retry. A source/configuration hash
mismatch or changed absolute source path blocks resume. Do not recover a run
by using its old ID in an empty directory or by clearing evidence.

The current public source cannot directly resume the older frozen runs. A
reviewed migration must archive original bytes, replay saved requests/outcomes,
verify current server history and enable state last. Paths and receipt patterns
are in the [submission ledger](submission-ledger.md#private-artifact-locations).

HTTP428 is completion only with recognized wording; a run-bound variant must
match the selected ID exactly. Unclassified protocol errors remain visible;
only durable classified evidence enters recovery. The final official receipt
was reconciled locally without another POST, as recorded in the
[completion guide](research/task2-recovery-plan.md#october-10-completion-reconciliation).

The [previous execution guide](research/archive/2026-10-10-runner-history.md)
preserves detailed historical migration and verification notes.
