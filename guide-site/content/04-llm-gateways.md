> **The question:** How do you let applications use multiple models without scattering policy, credentials, and cost controls through every application?

An LLM gateway is a controlled entry point for model requests. It can normalize provider interfaces and centralize selected operational policies. It is not automatically a complete security boundary, and a common API shape does not make every model interchangeable.

LiteLLM is one documented implementation, with a proxy, virtual keys, routing, fallbacks, and cost tracking. Use it as a concrete reference rather than a requirement to choose that product. [Feature overview](/agentic-eng/sources/#litellm)

## The mental model

Separate **eligibility** from **optimization**. First determine which endpoints are permitted for a request’s tenant, data class, required features, and retention policy. Only then choose among eligible endpoints based on availability, quality evidence, latency, and cost.

A cheaper endpoint that violates the data policy is not an optimization candidate. Nor is an endpoint that accepts the same JSON envelope but cannot reliably satisfy your tool or structured-output contract.

Suggested routing flow:

```text
Authenticate caller
  → derive policy from trusted application context
  → filter to eligible routes
  → reserve request budget
  → choose route using tested quality/capacity information
  → execute within deadline
  → validate response and reconcile actual usage
```

The route should not be chosen solely from a model-generated statement such as “this data is public.” Classification that controls data egress belongs to a trusted application policy or an explicitly reviewed classification process.

## Design the route contract

Represent a logical route such as `event-brief-draft` separately from a provider model name. Record the actual provider, model version, endpoint, feature flags, and fallback decision in operational metadata. Logical names make controlled changes possible; actual identities make results auditable.

Illustrative policy—not LiteLLM configuration syntax:

```yaml
route: event-brief-draft
required:
  data_class: internal
  structured_result: event_brief_v1
  allowed_tools: []
limits:
  deadline_seconds: 20
  total_attempts: 2
fallback:
  require_same_data_policy: true
  require_passed_regression_suite: true
```

Keep a compatibility test for output schemas, tool semantics, context limits, error mapping, and streaming termination. Use provider-specific adapters when normalizing these differences would otherwise conceal important behavior.

## Fallbacks without policy drift

Fallback is a new attempt, not free reliability. It can add latency and spend, and a timed-out first attempt may still complete upstream. LiteLLM documents configurable routing and retry/fallback behavior; verify your exact configuration rather than relying on defaults. [Routing reference](/agentic-eng/sources/#routing)

Before falling back, ask:

1. Is the failure transient or a deterministic request error?
2. Is there enough remaining time and budget?
3. Is the candidate route allowed to receive the same content?
4. Has the alternative passed the task’s evaluation suite?
5. Could the original attempt already have caused a side effect?

Keep model inference separate from tool execution where possible. Retrying a text-generation request is not equivalent to retrying a payment, email, or booking operation. Those effects need the operation contracts from the jobs chapter.

## Budgets need concurrency semantics

A cost dashboard describes spending after it happened. A hard admission budget must also account for simultaneous requests.

Suppose a project has $10 left and ten requests each expect to cost $2. Ten independent reads of the balance can all approve their request. Use an atomic reservation or equivalent admission mechanism, then reconcile estimated and actual cost after completion.

Keep an explicit state for unknown charges after timeouts. If the provider’s bill arrives later, reconciling usage should not erase the evidence that the system admitted too much work. A small application can begin with conservative per-request limits and one shared reservation store; distributed accounting deserves its own design review.

All dollar figures here are hypothetical examples, not provider prices.

## Caching and telemetry

Cache only where policy permits. A cache key for private results must incorporate authorization scope and relevant versions—not just the user’s text. A schedule update, role change, prompt update, or tool-version change may invalidate a previously useful result.

Decide what a cache hit means for quality, freshness, attribution, and retention. Do not let a global semantic cache return one customer’s private answer to another because their questions are similar.

For logs, prefer request IDs, route identity, elapsed time, token counts, outcome, and policy decisions. Capturing every prompt makes debugging convenient while creating a second sensitive-data store. Follow the [retention chapter](/agentic-eng/chapters/data-retention/) before enabling content-level tracing.

## Lab: build a routing test matrix

Use fake providers first: one returns a valid brief, one times out, one returns malformed output, and one is intentionally ineligible for private data.

Test an ordinary request, an exhausted budget, a timeout with an eligible fallback, a timeout with only an ineligible fallback, and a result that violates the schema. Confirm that an ineligible endpoint receives zero requests.

Add two simultaneous admissions against a nearly exhausted synthetic budget. Verify the reservation mechanism permits only the allowed amount. Record every attempt, including rejected admission and unsuccessful fallback.

The deliverable is a route policy, test matrix, and trace—not a claim that the gateway automatically solves governance.

## Failure drills

Disable the primary route during load. Change a provider’s response shape. Reuse a cache after an event version changes. Revoke a project key. Make cost reconciliation temporarily unavailable. Define when the system fails closed and when it may continue using an explicitly bounded fallback.

## Ship gate

You can prove policy eligibility, budget admission, and fallback behavior with tests. Every accepted result has a real route identity and every failed attempt remains accounted for. Next, put bounded decision-making above this infrastructure in [agent design](/agentic-eng/chapters/agent-design/).
