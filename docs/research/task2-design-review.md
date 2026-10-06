# Task 2 architecture and panel review

## Subsequent structural refactor

The user subsequently requested the helper extraction. See the
[refactor record](code-structure-plan.md): runtime and experiments are separated,
12 synthetic pre-refactor cases protect exact requests, and the earlier decision
to defer extraction is now superseded. The panel findings below refer to the
previous source layout; the current architecture guide takes precedence.

## Objective and scope

Make [PR #2](https://github.com/npatta01/trec-usersim-2026/pull/2) easy to
understand and assess its modularity and correctness before another live attempt.
Preserve the selected model, prompt behavior, and private halted run. This review
makes no organizer calls, paid inference experiments, or outbound messages.

The [architecture guide](../task2_architecture.md) is the design entry point:
four Mermaid diagrams explain the conversation loop, two model calls, ownership
of modules, and request recovery. They are rendered and visually inspected, not
just checked as Markdown text.

## Panel evidence and decisions

A standard project-advisor panel reviewed the same frozen source-and-diagram
packet. All four lanes completed successfully and requested changes before merge.
The packet contained task-scoped source, synthetic tests, and aggregate findings;
no participant transcripts, private outputs, credentials, or raw session logs.

| Reviewer | Main finding | Decision |
|---|---|---|
| GPT-6 Sol | Loose completion matching; receipt-only start recovery blocked when quota reaches zero | Fix both with regressions |
| GPT-6 Astra | Fresh starts accepted nonempty history; crash-boundary tests and docs needed | Reject unexpected history; add transition/recovery tests |
| Opus | Recovery diagrams overclaimed behavior; test the actual saved-500 failure; keep prompt helpers stable | Correct diagrams, add failure replay tests, preserve prompt construction |
| Gemini 3.8 Flash High | Diagram ownership inaccurate; historical experiment imports obscure boundaries | Correct ownership and improve model boundary; defer wholesale prompt extraction |

The panel disagreed on extraction: Gemini treated historical helper coupling as
a merge concern; Opus explicitly advised against extracting those helpers here
because it could alter request bytes. We retain the known prompt builders and
document their dependency rather than claiming a fully independent package.
A separate extraction needs request-parity tests and should not be mixed with
recovery of a frozen live run. No new framework or behavioral prompt variant is
introduced in this PR.

The frozen packet omitted some existing core/transport tests to fit its size
limit. Claims of absent coverage are checked against the complete checkout;
existing tests are retained and only missing regressions are added.

## Verification status

The completion allowlist, empty-start check, and quota-0 receipt recovery are
implemented. The runner now uses the model module’s public pending/totals API,
enforces frozen model pricing, and freezes both previously omitted helper modules.
Known model error receipts are retained without resend; transport uncertainty
continues to block retries. Prompt builders and generator instructions are unchanged.

The script suite passes 56 tests, including all 56 under optimized Python in
the independent follow-up review (35 are protocol tests). Four diagrams render
successfully; local links, secret checks, compilation, and whitespace checks pass.
An independent Sol code reviewer rechecked the corrected source and strengthened
regressions and reported no actionable findings. The four-model panel reviewed
the earlier snapshot, not this final revision; its findings are dispositioned above.
Power-loss durability remains unproven: the atomic helper flushes the file but
does not fsync the parent directory after replacement. The unchanged legacy simulator suite fails collection in two
modules importing missing `PersonaDefinition`; the same errors reproduce at
remote base `45de4e1`. This does not establish human realism or live Task 2
completion: the previous live run still has only three complete exchanges.

## Review provenance

Profile: `standard`; data class: `private`; provider training reuse: disabled.
Sol and Astra used Codex subscription authentication, Opus used Claude
subscription authentication, and Gemini used agy account OAuth. The Gemini CLI's
billing tier was not independently known. No OpenCode lanes were selected, so no
OpenCode cleanup was required. All four selected lanes returned valid reviews;
none were silently replaced. Private review artifacts remain outside git.

## Next action

PR #2 contains the verified corrections and design guide. Keep the historical
organizer run frozen until recovery is resolved; no automatic retry is authorized
by this review. Future cleanup should extract prompt helpers with request-parity
tests before introducing concurrency.
