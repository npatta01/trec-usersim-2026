# Organizer recovery request — draft, not sent

> Historical unsent support draft for the first failure. It was not sent and
> is not a current recovery procedure. Current state is in the
> [handoff](../project-handoff.md) and [recovery record](task2-recovery-plan.md).

Subject: Task 2 debug: HTTP500 after user message persisted — safe recovery?

Hi organizers,

Our NP Labs Task 2 debug runs both stopped while generating an agent response:

- `np-labs-luna-task2-debug-20261006-v1`: four researcher messages saved, three assistant replies.
- `np-labs-luna-task2-debug-20261006-v2`: five researcher messages saved, four assistant replies.

In each case, `/task2/debug/continue` returned HTTP500 with an error generating
the agent response. Repeated GET `/debug/session` checks show that our submitted
user message was persisted, but its assistant reply is missing. The last message
in the second run has `is_final=false`.

We have not reposted those messages. Our requests are sequential (about 15–25
seconds between submissions), with a 180-second client timeout. Both runs retain
all local request/response checkpoints.

Can you repair the pending assistant turn, or confirm a supported way to resume
the same run without duplicating its already-saved user message? Specifically,
is resending the exact continue payload idempotent, or is a server-side action
needed? If recovery is impossible, could you advise whether the failed debug
allowance can be restored?

Thanks,
NP Labs
