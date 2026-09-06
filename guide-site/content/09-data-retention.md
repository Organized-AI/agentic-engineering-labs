> **The question:** Where can a request’s content persist after the system says it is finished?

Privacy is not a property of the model endpoint alone. The application, gateway, queue, tools, observability system, caches, crash reports, and backups can each retain copies. A data-flow diagram is therefore more useful than a single “private AI” label.

This chapter is an engineering review framework, not a legal determination that a deployment meets a particular regulatory obligation.

## Separate the promises

Do not collapse distinct questions:

- Is customer content used to train models?
- Is content stored, and for how long?
- Which region or processors handle it?
- Who can access it while it exists?
- What metadata remains after content is removed?
- What happens to backups, cached results, and diagnostic copies?

Anthropic’s API documentation defines ZDR scope by endpoint and eligible feature and distinguishes other retention arrangements. That is one provider’s documented contract, not a universal definition for every service. Verify the exact organization, feature, route, and agreement in use. [Retention reference](/agentic-eng/sources/#retention)

Self-hosting changes who operates the system. It does not, by itself, prove that request content is never persisted.

## Model the complete data path

For each component, record data categories, persistence mechanism, retention period, deletion mechanism, access roles, and evidence owner. Include success, failure, retry, cancellation, and incident paths.

| Component | Possible retained material | Question to test |
| --- | --- | --- |
| API server | Request bodies, debug logs | Does validation failure log the entire input? |
| Gateway | Prompts, responses, usage callbacks | Is content capture enabled indirectly? |
| Job store | Serialized input, exception payloads | Does a retry duplicate sensitive text? |
| Model service | Content, files, feature state | Is this exact feature eligible under the policy? |
| Tools | Queries, returned records, uploaded files | Does the downstream service keep a copy? |
| Observability | Traces, spans, crash dumps | Do automatic integrations collect content? |
| Storage/backups | Results, snapshots, replicas | What does deletion mean for each copy? |

The question is not merely whether a file named `prompt.log` exists. Content can appear in a stack trace, a failed request payload, or a third-party tracing callback.

## Resolve durability versus minimization

Durable workflows often need enough state to recover. A zero-retention objective may prohibit storing the raw content required for that recovery. Make the conflict explicit rather than promising both properties without defining their scope.

One proposed design is to keep only an opaque, authorized record reference in the job and fetch content at execution time. That reduces duplicate storage but introduces other questions: what if the record changes or is deleted? Does the reference itself reveal sensitive information? Can the requester’s access be revoked while the job waits?

Another design uses an approved encrypted transient store with a bounded lifetime. That is retention, even if brief and encrypted. Describe it honestly and confirm whether the intended policy allows it.

For the event assistant, decide whether draft results are intended business records. Do not include them in an unqualified promise that “nothing is stored” while simultaneously providing a permanent brief history.

## Keep telemetry useful without default content capture

Begin with metadata: operation ID, stage, elapsed time, route, input/output size, outcome, retry count, and policy result. Only add content capture for a specifically approved diagnostic purpose with access restrictions and an expiration.

OpenTelemetry’s GenAI conventions are a useful observability reference, but enabling a convention or integration is not a privacy assessment. Review the actual payloads and maturity of the implementation you adopt. [Observability reference](/agentic-eng/sources/#otel)

Do not assume hashing private text anonymizes it. Low-entropy values can sometimes be guessed, and identifiers can remain linkable. Choose metadata based on what you need to diagnose and the sensitivity of what it reveals.

## Lab: trace a synthetic canary

Use a unique synthetic marker, never a real secret or personal record.

1. Send the marker through a normal event-brief request.
2. Repeat with a validation error, tool timeout, worker retry, and simulated crash.
3. Search the stores and logs you are authorized to inspect for the marker.
4. Check tracing callbacks, queue payloads, saved errors, and object storage.
5. Trigger the designed deletion or expiration process and verify its behavior.
6. Record components you cannot inspect and what contractual or provider evidence covers them.

A failed search is not proof that no copy exists. The canary checks known surfaces; combine it with configuration review, service documentation, access review, and provider evidence.

The offline starter persists synthetic input references and brief content in SQLite. It is intentionally **not** a ZDR implementation. Use its database to practice finding retained data before designing a different retention policy.

## Plan the exception path

Define who can authorize diagnostic capture, how it is enabled, which data is excluded, and how it expires. For an accidental disclosure, preserve the minimum incident evidence needed without making uncontrolled extra copies of the sensitive material.

Review fallback routes as part of the same data path. A compliant primary endpoint does not make an ineligible fallback acceptable. Review tool calls too: a web search query can disclose content even when the model inference itself remains inside your controlled environment.

## Failure drills

Turn on a debug integration in a test environment and inspect its output. Crash after a provider response arrives. Retry a failed job. Export a trace. Restore a test backup. Ask whether the documented policy still describes what actually happened.

## Ship gate

You have a component-by-component inventory, tested success and failure paths, explicit retention scope, and documented unknowns. A knowledgeable reviewer can trace every content copy and explain its lifecycle. After the privacy boundary is clear, continue to [kernels and performance](/agentic-eng/chapters/kernels-and-performance/) or skip ahead to [business semantics](/agentic-eng/chapters/ontologies/).
