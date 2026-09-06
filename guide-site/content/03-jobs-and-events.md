> **The question:** How does a task finish correctly when messages repeat, workers disappear, or acknowledgments are lost?

A job expresses intent: generate this brief. An event records a fact: this brief was generated. Separating those meanings helps you decide who owns execution, what can be replayed, and which side effects must be deduplicated.

The goal is not to promise that every line of code runs once. It is to preserve a clearly defined business outcome despite retries.

## Delivery is not completion

Amazon SQS standard queues provide at-least-once delivery and can deliver messages out of order. Other systems have different contracts; read the exact queue’s guarantees. A message acknowledgment only describes the queue interaction, not whether the downstream business effect happened exactly once. [SQS reference](/agentic-eng/sources/#sqs)

Consider a worker that saves a brief and crashes before acknowledging its message. The queue may redeliver it. If the worker treats the second delivery as new intent, the application may create another brief or send another notification.

Design the logical operation separately from delivery attempts. A useful operation identity is `(tenant, caller_operation_key)`. A delivery ID belongs to the transport; it may change on redelivery and is not necessarily the correct business deduplication key.

## Idempotency is a contract

For a given operation key, define how the system behaves when the same request returns. Store a normalized input fingerprint with the key and reject a reuse with different intent. A caller must be able to request two intentionally identical operations using different keys. These distinctions are central to AWS’s [idempotent API discussion](/agentic-eng/sources/#idempotency).

Suggested contract:

```text
Same tenant + same key + same input → return existing operation.
Same tenant + same key + different input → conflict.
Different key + same input → a new logical operation.
Completed operation replay → return its existing result.
```

Use a unique database constraint or equivalent atomic mechanism. A separate “check whether it exists” followed by “insert” is vulnerable to two workers racing. State how long the key remains meaningful; deleting deduplication records can make late retries behave like new work.

## Leases and fencing

Give active work a lease: a temporary claim owned by a worker. If it expires, another worker may recover the task. Recovery alone is insufficient, because the original worker may still finish late.

Attach a new fencing token to each claim. Finalization must atomically verify that the token still owns the task before writing the result. A stale worker can consume compute, but it cannot overwrite the accepted result.

An illustrative state machine:

```text
queued → running(lease, token) → succeeded
                  ↓
             retryable → queued
                  ↓
          terminal failure / manual review

expired running lease → running(new token)
```

Perform slow external work outside the claim transaction. Re-enter a short transaction for finalization, validate the token and source version, then commit. A lease does not cancel external side effects; those need their own idempotency or reconciliation design.

## The dual-write problem

Suppose you commit a brief and then publish `brief_ready`. A crash between the two leaves a saved brief with no event. Publishing first creates the opposite risk: an event referring to a result that never committed.

A transactional outbox writes the business result and an event record in the same database transaction. A relay later publishes committed outbox entries. If publication succeeds but marking the entry delivered fails, the relay may publish it again; consumers still need deduplication. [Transactional outbox reference](/agentic-eng/sources/#outbox)

For our project, the transaction contains the brief, the operation’s terminal state, and an outbox row. It does not contain an email send. Keep that external effect in a separate consumer with its own operation identity.

## Retry policy and backpressure

Classify failures before retrying. A temporary network failure may be retryable. Invalid input, denied access, or a deterministic schema mismatch usually needs a different action. Repeating every failure wastes capacity and can amplify an outage.

Give retries a maximum attempt count, an overall deadline, and delayed scheduling. Add jitter to avoid synchronizing many workers. Set a maximum queue age so an old request cannot quietly produce a stale brief hours after it stopped being useful.

Backpressure is the decision to slow or reject incoming work when downstream capacity is constrained. A queue buys time; it does not create processing capacity. Track oldest-job age alongside queue length, because long tasks and short tasks consume different amounts of work.

## Lab: replay and recover

Use the downloadable SQLite starter for a small, local demonstration of operation keys, leases, and atomic finalization. It is not a distributed broker.

1. Submit the same event twice with the same key; confirm one operation exists.
2. Reuse the key with a different event; expect a conflict.
3. Claim a job, allow its lease to expire using the test clock, and claim it again.
4. Try finalizing with the old token; expect rejection.
5. Finalize with the current token; inspect the brief and outbox records.
6. Repeat the completed request and confirm that no additional brief appears.

Then sketch how an outbox relay would acknowledge delivery. Deliberately place a crash after external publication but before the delivered marker, and explain how the consumer deduplicates that replay.

## Failure drills

Run two workers against one operation. Inject a slow upstream response. Replay a message after completion. Change authorization while a job waits. Exhaust the retry limit. Each test should produce an understandable state, not merely “an exception occurred.”

## Ship gate

You can explain the duplicate, crash, stale-worker, and dual-write cases using actual tests. You have bounded retries, queue-age visibility, and a manual recovery path. Next, apply the same discipline to model calls in [LLM gateways](/agentic-eng/chapters/llm-gateways/).
