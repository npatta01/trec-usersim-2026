# Checkpointed Task 2 debug runner

The runner simulates the researcher through complete organizer conversations.
It sends the supplied persona, goal, and full available history to GPT-6 Luna,
then applies one style edit that preserves the generated boolean stop decision.
This integration does not change the selected prompts or enable compaction.

See the [illustrated architecture](task2_architecture.md) for the complete loop,
model calls, code boundaries, and recovery behavior.

## Setup and offline verification

From the repository root:

```bash
python -m venv .venv
.venv/bin/pip install -r simulator/requirements-dev.txt
.venv/bin/python -m unittest discover -s tests -p 'test_*.py'
.venv/bin/python -m pytest simulator/tests
```

Verification for this PR: all 60 included runtime tests pass; the 35 protocol
tests also pass under optimized Python. The unchanged legacy simulator suite
cannot collect two modules because they import the removed `PersonaDefinition`;
the same error reproduces on the remote base (`45de4e1`).

The new tests use synthetic inputs and injected transports; they do not require
credentials, the official dataset, paid inference, or organizer access.
Historical replay modules live under `experiments/` and are not imported by the
runtime. They require private local artifacts and are not part of the debug
invocation below. See [code layout](../experiments/README.md) for provenance.

## Modules

- `usersim/prompts.py`, `requests.py`, `checkpoints.py`: shared pure builders and persistence.
- `usersim/task2/core.py`: immutable conversation state and strict text/stop parsing.
- `usersim/task2/generator.py`: draft and default-on style editor.
- `usersim/task2/protocol.py`: organizer history and transition validation.
- `usersim/task2/model.py`: cached model calls and cost reservations.
- `usersim/task2/debug.py`: run lock, source/config snapshot, scenario lifecycle,
  injected transports, and recovery guards.
- `scripts/run_task2_debug.py`: thin CLI wrapper; `tests/` contains offline tests.

The only organizer write routes allowed are `/task2/debug/start` and
`/task2/debug/continue`. HTTP200 consumes a verified incremental assistant reply
or full history; HTTP201 starts a new empty scenario. HTTP428 is completion only
with explicit completion text. HTTP500 and timeouts stop the runner.

## Authenticated execution

This is a paid model/API operation and requires a separately authorized debug
run. Store credentials outside the checkout in owner-readable files:
`~/.config/trec-usersim/organizer.key` and `~/.config/trec-usersim/openrouter.key`.
The configured team is NP Labs; model routing is OpenAI-only with no fallback.

```bash
.venv/bin/python scripts/run_task2_debug.py --run \
  --run-id YOUR_AUTHORIZED_UNIQUE_RUN_ID \
  --output-dir data/official/YOUR_PRIVATE_RUN_DIRECTORY
```

Each new run consumes one debug allowance. The default reservation ceiling is
$3; operational bounds are 500 total researcher turns and 30 per conversation.
A bound halts execution; it does not invent a voluntary user stop.
All private outputs under `data/official/` are ignored by git.

## Resume and the current halted run

Do not invoke the historical default run ID from a clean checkout: its local
receipts are not in git. Use the original private run directory for recovery.
Completed receipts are reused, while an in-flight marker blocks automatic retry.
A changed source/configuration also blocks resume. The manifest currently records
absolute source paths, so moving the checkout is not a supported automatic resume.
This PR changes the frozen source and cannot directly resume the older live run.
A saved server failure is not
silently retried. Preserve timestamped requests and receipts before reconciliation.

The first live attempt accepted four researcher messages but failed generating
the fourth assistant reply. No full conversation completed. Reposting could
create a duplicate user turn. See the [handoff](research/task2-debug-handoff.md)
and [unsent support request](research/task2-debug-recovery-request.md).

The PR contains source, synthetic tests, and aggregate findings only. Official
training transcripts, model outputs, credentials, and private API receipts are
not included. Completing a debug conversation will still not establish human
realism or official evaluation performance.
