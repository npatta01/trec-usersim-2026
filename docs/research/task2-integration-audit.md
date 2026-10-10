# Task 2 integration audit

> Dated HTTP200/null-transition investigation. This is a bounded earlier audit,
> not the final completion check. See the [current handoff](../project-handoff.md),
> [runner guide](../task2_debug_runner.md) and [recovery record](task2-recovery-plan.md).

No live requests or new runs were made for this audit. This is a bounded audit,
not a guarantee that every server behavior has been discovered.

## Confirmed defect and fix

The fourth debug run returned HTTP200 with a NEW conversation ID, supplied
scenario and explicit null utterance after our final message. The subsequent
saved GET confirmed that exact new scenario with empty history. The documented
workflow says HTTP201; our tests inherited that assumption.

The parser now accepts HTTP200 with a new valid ID, valid scenario, explicit null
utterance and empty/absent history as a transition. Same-ID null replies, missing
transition evidence, nonempty new history and contradictory replies remain errors.
No simulated final turn or dropped message is invented to bypass an error.
The same transition shape after a non-final request is supported as a server
cutoff, but that particular variant is synthetic coverage, not live evidence.

## Coverage matrix

| Boundary | Verification | Limit |
|---|---|---|
| Start and scenario | Existing tests for empty/omitted history, bad IDs/history; live starts succeeded | Start with preexisting history remains rejected |
| Normal reply | Full-history and incremental fixtures; exact ID, scenario, prefix and role checks | Undocumented mixed responses fail closed |
| User stop | New HTTP200 transition regression plus existing HTTP201 | Live v4 evidence supports new form |
| Server cutoff | HTTP200/201 transition fixtures and accounting | HTTP200 cutoff not observed live |
| Final completion | Explicit HTTP428 success and negative/partial/malformed completion tests | Exact service wording variants beyond known messages unverified |
| Whole lifecycle | Two-conversation HTTP200 transition to HTTP428, counts, new ID, cached completion | Synthetic, no completed live debug run yet |
| Crash at transition | HTTP200 added to receipt-before-state-crash replay; zero repeated external calls | Changed frozen source still blocks automatic resume |
| Timeout/5xx | Existing saved-response and pending-marker replay tests | No proof retry of persisted turn is idempotent; never auto-retry |
| Model boundary | Invalid/empty/truncated outputs, pending calls, budget and receipts tests | Provider behavior outside recorded contract remains uncertain |
| Auth/quota | Preflight team identity, available quota, receipt-only recovery tests | Quota changes require current read-only check |
| Operational limits | Per-conversation/total bounds halt without fabricated user stop | Hitting a bound is not successful completion |
| Source integrity | Config/source hash guards, frozen dependency coverage | Migration must explicitly preserve old manifests |
| Data integrity | Three-run full offline replay: 13 schema-valid/reference-equal payloads, 26 model requests | Replay is not independent backend execution |

## Saved live regression

Replayed all five v4 continue receipts through the fixed parser offline: four
ordinary replies then one new conversation. Recovered conversation ID, scenario,
and empty history match the saved GET exactly. No closing turn was resent.
Fixtures committed to tests are synthetic; private logs stay outside git.

## Remaining integration gaps and launch gate

- The CLI exception handler writes error.json but may leave state.json marked
  running and cost totals one turn behind. Service state/error/receipts must be
  consulted together; the live v4 state was manually marked halted. This is an
  observability gap, not evidence a process remains active.
- v4 is frozen to the old source and manually halted. Do NOT simply restart it
  with the changed parser. Resume requires an explicit migration preserving the
  old manifest/state, deriving state from receipts, refreshing costs, and checking
  that the server still matches the next scenario. No migration performed here.
- Remote timeouts, persisted-turn HTTP500 and undocumented completion variants
  remain fail-closed. We cannot establish server idempotence from local tests.
- No complete live multi-conversation run yet: passing synthetic coverage must
  not be described as full live integration validation.

Next action: verify and migrate the existing v4 checkpoint, then resume that same
run only after the gate above is satisfied. Do not spend a new debug allowance.

## v4 checkpoint migration and same-run resume

91 tests / 50 subtests pass after the transition and failure-status fixes.
Archived original manifest, frozen source, state and error in private
`migration-before-transition-fix/`. Replayed all five receipts; live GET matches
the new empty scenario exactly. State: one completed conversation, five user
turns, ten model calls, $0.004555995. Read-only budget confirms six debug
allowances remain. Same v4 service restarted; no new run or closing-message
resend. Generator/editor/model configuration unchanged. On later failures the
CLI now marks state halted and refreshes costs without clearing retry guards.
Check private state/receipts for current progress.
