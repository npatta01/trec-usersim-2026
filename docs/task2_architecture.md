# Task 2: how our researcher simulator works

We generate the **researcher’s side** of a conversation. The organizer supplies
the dataset-search assistant. These are two separate systems.

## Task 1 versus Task 2

| | Task 1 | This Task 2 runner |
|---|---|---|
| Starting point | A supplied conversation prefix | A new persona and goal |
| Our output | One next researcher message | Repeated researcher messages and a stop decision |
| History | Supplied for each prediction | Built from our messages and organizer replies |
| End of work | That prediction is returned | Organizer says the full run is finished |

## One conversation, from start to finish

```mermaid
flowchart TD
    A[Organizer gives persona and research goal] --> B[Reset persona, goal and history]
    B --> C[Generate the next researcher message]
    C --> D[Send message and stop decision to organizer]
    D --> E{Organizer response}
    E -->|Assistant reply| F[Add both messages to history]
    F --> C
    E -->|Next scenario| B
    E -->|Run finished| G[Save completion]
    E -->|Saved HTTP500 or HTTP502| R[Verify exact server session]
    E -->|Classified original ReadTimeout| W[Poll for delayed reply]
    W -->|Matching reply| F
    W -->|Exact unanswered turn for 30 minutes| R
    W -->|Unknown or changed evidence| H[Halt and preserve evidence]
    R -->|Delayed matching reply| F
    R -->|Fresh exact check and outage limits allow| K[Send one operational final message]
    K -->|New scenario confirmed| J[Record error-driven closure separately]
    J --> B
    R -->|Mismatch, uncertainty or outage bound| H
    K -->|Closing request fails| H
    E -->|Other error or uncertain outcome| H
```

Each new scenario supplies a new persona and goal. The history resets completely.
Within a conversation we retain all available messages. We do not compact or
summarize them in the current baseline.

An operational close sends `is_final=true` from the researcher to end a
conversation blocked by an observed backend error. It does not erase that
conversation or represent a natural researcher decision. We count these as
skips separately from completed conversations and model-generated stops.

## What happens inside one researcher turn?

```mermaid
flowchart TD
    A[Persona + goal + full conversation] --> B[Draft call: Luna]
    B --> C[Validate text and boolean stop decision]
    C --> D[Style-edit call: Luna]
    A --> D
    D --> E[Validate nonempty edited text]
    E --> F[Researcher text + original stop decision]
```

The first call produces the next message and decides whether this researcher
would stop: because they have enough help, or because the search is unproductive.
The second call compares the wording with their last two messages and persona.
It may leave the draft unchanged. It preserves the original stop boolean; the
prompt also asks it to preserve the meaning and closure, but code does not prove
semantic preservation. This is not a repeated judge/retry loop.

Chat API roles are mapped from the simulator’s viewpoint:

| Conversation speaker | Model API role | Why |
|---|---|---|
| Instructions, persona and goal | system | Defines whom to simulate |
| Earlier researcher messages | assistant | The model continues this speaker |
| Dataset-search assistant messages | user | These are incoming replies to react to |
| Fixed opening cue, when history is empty | user | Requests the first researcher message |

Opening turns use the supplied scenario without an observed speaking history.
The model does not receive future human messages or reference answers. Each
model request resends the needed context explicitly; there is no hosted
conversation-memory API or automatic compaction behind this diagram.

## Code boundaries

```text
scripts/                 Thin command-line entry points
  run_task2_debug.py
  run_task2_recovery.py   Explicit debug/official mode and recovery policy
usersim/                 Reusable code; no experiment imports
  prompts.py             Persona/history and style-editor prompts
  requests.py            Model payload and response validation
  checkpoints.py         JSON persistence and request hashes
  task2/
    core.py              Conversation and researcher-turn types
    generator.py         Draft and optional style edit
    protocol.py          Organizer response and transition validation
    model.py             Model receipts and spending safeguards
    debug.py             Run lifecycle and injected transports
    recovery.py          Policy, CLI, known HTTP errors and official gate
    reconciliation.py    Shared evidence checks and progress accounting
    timeout.py           Original-timeout polling and durable recovery
experiments/             Historical replays and unselected variants
tests/                   Offline tests and synthetic parity fixtures
simulator/               Original organizer implementation
```

```mermaid
flowchart TD
    CLI[scripts/run_task2_recovery.py] --> W[task2.recovery: verified recovery]
    W --> R[task2.debug: run lifecycle]
    W --> X[task2.timeout: delayed-reply grace]
    W --> Q[task2.reconciliation: evidence and outage limits]
    X --> Q
    R --> V[task2.protocol: validate organizer transitions]
    R --> C[task2.core: conversations and turns]
    R --> G[task2.generator: draft then style edit]
    G --> P[prompts + requests: pure builders]
    R --> K[task2.model: checkpoints and cost cap]
    G -. Injected call function .-> K
    K --> MC[Private model receipts]
    K --> O[OpenRouter: OpenAI-only Luna]
    R --> T[Injected organizer transport]
    T --> A[Explicit debug or official organizer routes]
    R --> S[Private organizer receipts and state]
```

| Responsibility | Module | What it does not decide |
|---|---|---|
| Represent conversations and validate text/stop types | `usersim/task2/core.py` | HTTP behavior or wording |
| Construct model requests and edit one draft | `usersim/task2/generator.py` | Retries, quota, or session transitions |
| Save/reuse model results and reserve spend | `usersim/task2/model.py` | Researcher personality or when to stop |
| Validate incoming history and transitions | `usersim/task2/protocol.py` | Network calls or persistence |
| Advance the run and coordinate transports | `usersim/task2/debug.py` | Whether a recommendation is good |
| Reconcile saved backend failures and close blocked conversations | `usersim/task2/recovery.py` | Whether the researcher naturally wants to stop |
| Wait for delayed replies and reconcile classified original timeouts | `usersim/task2/timeout.py` | Generator wording or recursive closing retries |
| Verify raw evidence and count operational outcomes | `usersim/task2/reconciliation.py` | Network calls or researcher satisfaction |

The runner owns the checkpointed model and injects its call function into the
generator. Prompt construction is pure: it no longer imports experiment runners,
loads LiteLLM, or temporarily replaces a global completion function. Scenario
classes remain shared with the organizer baseline to preserve their exact prompt
representation. Twelve synthetic fixtures preserve pre-refactor requests across
openings, follow-ups, longer histories, missing persona fields, and stop decisions.
The runtime remains sequential; this refactor does not add concurrent execution.

## Why we stop on an uncertain request

```mermaid
sequenceDiagram
    participant R as Our runner
    participant D as Private checkpoints
    participant A as Organizer
    R->>D: Save request before sending
    R->>A: Submit researcher message
    alt Response received
        A-->>R: Reply or HTTP error
        R->>D: Save response receipt
        R->>R: Validate response
        alt Valid reply or transition
            R->>D: Advance conversation state
        else Invalid response or server failure
            R->>D: Preserve evidence and halt
        end
    else Original request raises ReadTimeout
        R->>D: Keep pending request and classify exact ReadTimeout
        R->>A: Read session; wait for delayed reply
        alt Exact original turn remains unanswered for 30 minutes
            R->>A: Fresh session check
            R->>A: One distinct final close, if outage limits allow
            A-->>R: New scenario or explicit completion
            R->>D: Save separate close receipt and operational skip
        else Matching delayed reply
            R->>D: Save GET-derived reconciliation event
        else Unknown, changed evidence or closing uncertainty
            R->>D: Halt without another POST
        end
    else Other uncertain transport outcome
        R->>D: Retain pending request and halt
    end
```

A request can reach the server even when its reply fails. Repeating it could add
the same researcher message twice. We reuse completed local receipts, block
uncertain calls, and never treat HTTP500 or a timeout as successful completion.
This prevents blind retries; it does not guarantee exactly-once delivery or
repair a server-side partial turn.

| Response | Action |
|---|---|
| 200 + valid assistant reply | Append the exchange and generate the next researcher turn |
| 201 or strictly validated 200 + new empty scenario | Record the ending and reset persona, goal, and history |
| 428 + explicit run-finished message | Mark the entire run complete |
| Saved 500/502 with exact persisted unanswered turn | Recovery wrapper sends one distinct final message, verifies advancement, and records a skip |
| Classified original ReadTimeout with exact persisted unanswered turn | Wait for a delayed reply; after 30 minutes and a fresh check, allow one distinct close within outage bounds |
| Other errors, mismatched IDs, invalid history, uncertain transport | Halt for inspection |

The limits ($3 reservation, 500 total researcher turns, 30 per conversation) are
operational safeguards. Hitting one persists `status="halted"` and stops the
whole run without sending an artificial user-stop message. Protocol or transport
errors preserve the last validated progress and private evidence with
`status="halted"`. The recovery wrapper reconciles only the narrow observed
backend-error and classified-original-timeout cases described above. It permits
at most 24 skips, at most 25% of terminal conversations with a denominator floor 8,
and at most 3 consecutive operational skips. A close timeout never enters that
automatic path again.

A saved error receipt is replayed locally and fails again without resending. A
pending marker blocks resume even if a receipt also exists: that crash boundary
requires reconciliation. CLI resume still performs read-only authentication and
budget checks. Source/configuration hashes must match the frozen run; this updated
PR cannot directly resume the older live run. Its frozen code and receipts must
remain intact until recovery is explicitly resolved.

## What is demonstrated, and what is still open?

Synthetic tests cover the lifecycle, resets, stop propagation, budget guards,
safe receipt replay, metadata mismatches, timeout polling, delayed-reply evidence,
outage limits and official-route isolation. At the October 9 migration checkpoint,
v5 had 46 completed conversations and 11 operational closes and was halted on an
original timeout. No official Task 2 submission had started.
Official launch requires completed debug evidence and a conversation review bound
to the final state, completion receipt, frozen code and recovery policy.
Persona realism, natural voice, and semantic editor fidelity still need behavioral
evaluation; passing software tests does not establish them.

See the [runner guide](task2_debug_runner.md) for commands and the
[recovery handoff](research/task2-debug-handoff.md) for the actual run status.
