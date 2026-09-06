> **The question:** If the model were perfect, what could still make the service fail?

Incorrect permissions, stale records, broken transactions, unbounded retries, and failed deployments remain possible even with a perfect model. Treat the model as an unreliable dependency inside a normal software system. The surrounding service should make its requests and consequences understandable.

This chapter proposes the minimum engineering envelope for the event-operations assistant. You do not need eight languages. You need to understand the boundaries of the system you are building.

## The mental model

Give each layer a job. The HTTP layer authenticates and validates. Domain code decides what an operation means. Storage preserves invariants. A model adapter translates a provider’s response into an internal type. The worker coordinates execution. None of these boundaries should rely on the model inventing the correct behavior.

For example, a model can draft a venue description. It should not decide which organization the requester belongs to. Resolve identity from the authenticated session and enforce access before retrieving records.

Keep the first implementation in one codebase if that makes these boundaries easier to test. A separate module is often enough; a separate network service introduces additional failure modes and is a later design choice.

## Contracts before prompts

Define the input, result, and error contract before tuning language:

```json
{
  "event_id": "event_demo_01",
  "brief_version": 1,
  "facts": [
    {"field": "venue", "value": "Hall A", "source_id": "venue_17"}
  ],
  "unresolved": [],
  "status": "draft"
}
```

This is an illustrative internal schema, not a provider API. Validate allowed fields, types, lengths, identifiers, and status values. A valid JSON document can still contain false facts or unauthorized data; syntax validation and domain validation are separate checks.

Define errors such as `not_found`, `not_authorized`, `upstream_timeout`, `budget_exceeded`, and `needs_clarification`. Decide what the user can retry and what requires a different input. Do not expose raw provider errors or secrets through the public interface.

## Transactions and concurrent changes

A transaction groups state changes; its isolation level determines which concurrent behaviors are possible. PostgreSQL’s default Read Committed isolation uses a new snapshot for each statement, so two reads within a transaction can observe different committed states. Serializable execution can reject transactions that must then be retried as a whole. [PostgreSQL isolation reference](/agentic-eng/sources/#postgres)

For the brief service, decide whether a job uses an immutable snapshot or current records. If it uses a snapshot, preserve a version identifier. If it must use the latest approved schedule, revalidate that version before publishing the result. Otherwise, a factually correct draft may become operationally wrong between generation and delivery.

Do not keep a database transaction open during a slow model call. Read or claim the work, release the transaction, compute, then commit the result with a version or lease check. Chapter 3 develops that pattern.

## Tenant isolation and least privilege

Use server-derived tenant scope in every data-access path, including searches, caches, exports, and job status endpoints. An opaque identifier is not an authorization check.

PostgreSQL row-level security can provide another enforcement layer. However, superusers and roles with `BYPASSRLS` bypass it, and table owners normally do too. Tests using an administrative database account can therefore miss a broken policy. [Row security reference](/agentic-eng/sources/#rls)

Suggested test: create events for organizations A and B, authenticate as A, then request B’s event through the ordinary API, search interface, cache, and background-job lookup. Verify that no prompt is sent before authorization fails.

## Deadlines and observability

Give the user-facing task one overall deadline. Suboperations must consume the remaining budget rather than each starting a fresh full timeout. Also bound input size, output size, tool calls, and retry attempts.

Record a correlation ID across API, queue, worker, model adapter, and result. Distinguish operational metadata from content: duration, outcome, model route, attempt count, and token usage are useful without always recording the prompt. OpenTelemetry’s GenAI conventions provide an evolving vocabulary for spans, metrics, and events; pin the convention version you implement. [OpenTelemetry reference](/agentic-eng/sources/#otel)

Treat cancellation as a state transition, not as proof that an upstream provider stopped charging. Reconcile uncertain outcomes separately.

## Lab: build a deterministic vertical slice

Use the [offline starter](/agentic-eng/capstone/) or your own small service.

1. Accept an event ID and an operation key. Supply the authenticated principal separately from the model-facing input.
2. Read a synthetic, authorized event and produce a deterministic draft—no model yet.
3. Validate the result against authoritative facts and save it with source versions.
4. Add a model-adapter interface while keeping the deterministic implementation as a test double.
5. Make provider failure, malformed output, and timeout explicit test cases.
6. Document a clean installation, test command, deployment procedure, and rollback.

The point of the test double is to separate orchestration defects from model variability. It does not predict how a real model will behave.

## Failure drills

Change the source version while a draft is being generated. Confirm the finalization rule catches the conflict. Request another tenant’s job identifier. Confirm the status endpoint does not reveal it. Remove a required configuration value and ensure startup fails clearly. Simulate a provider timeout and inspect logs for accidental prompt capture.

For deployment practice, add a backward-compatible field before switching readers to require it. Record how to undo the release without destroying data written by the newer version.

## Ship gate

The service has explicit contracts, authorized data access, deterministic tests, bounded execution, interpretable telemetry, and a recovery procedure. A model swap does not require rewriting your business rules. Next, make the work durable in [jobs and events](/agentic-eng/chapters/jobs-and-events/).
