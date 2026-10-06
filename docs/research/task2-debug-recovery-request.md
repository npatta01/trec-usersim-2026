# Organizer recovery request — draft, not sent

Subject: Task 2 debug run: HTTP500 after user message persisted

Hello,

Our team, NP Labs, started Task 2 debug run
`np-labs-luna-task2-debug-20261006-v1` on October 6, 2026.
After three successful exchanges, the fourth `/task2/debug/continue` request
returned HTTP500 with an error generating the agent response.

Two read-only `/debug/session` checks show that the fourth user message was
persisted, but no assistant response was added: seven messages ending in the
submitted user message. We have not retried the request or started another run.

Could you restore the missing assistant response, roll back the partial turn,
or provide a supported recovery procedure that avoids duplicating the user
message? The published API does not appear to expose an agent-retry or rollback
operation. We have the timestamped request and response saved privately if needed.

Thank you.
