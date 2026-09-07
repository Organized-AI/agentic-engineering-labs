> **The question:** Which actions wait for a person, and how does the wait actually work?

Chapter 05 introduced approval-bound actions as a design principle. This chapter is the operational version: the queues, surfaces, and audit trails that make "a human approves this" a property of the system rather than a hope about its users.

## The mental model

Autonomy should scale with reversibility. A drafted brief costs nothing to discard; a sent email cannot be unsent. Route every action through a policy that maps risk to one of three paths: **autonomous** (reversible, low blast radius), **approval-gated** (consequential or irreversible), and **forbidden** (never, regardless of approval).

For the event assistant: retrieving records is autonomous, publishing a brief to the organizer's own dashboard might be too, but emailing 400 attendees waits for a person.

## The approval queue is a state machine

An approval is not a boolean the model passes around. It is a durable record: the exact proposed action, normalized arguments, the source versions it was based on, an expiration, and the identity of the approver - the binding chapter 05 described, now persisted so a restart cannot lose it and a retry cannot reuse it.

```python
# Pseudocode: approval binds to the exact action, then is consumed.
def execute_with_approval(action, approval_store):
    approval = approval_store.get(action.approval_id)
    if approval is None or approval.expired():
        return reject("no live approval")
    if approval.payload_hash != hash(normalize(action)):
        return reject("action changed after approval")
    approval_store.consume(approval.id)  # one approval, one execution
    return run(action)
```

The queue needs the same reliability primitives as chapter 03's jobs: at-least-once delivery to reviewers, idempotent consumption, and a dead-letter state for approvals nobody acted on.

## Build the review surface for decision speed

An approver who must reconstruct context will either stall or rubber-stamp. Show the reasoning trace that led to the action, the exact diff it will produce, and the source records behind it - with links, not summaries of links. Record the decision, the approver, and the timestamp in an immutable audit log.

There is a compliance clock as well: the EU AI Act's human-oversight obligations for high-risk systems took effect in August 2026, with penalties reaching 7% of global turnover. Even outside regulated domains, the pattern is the same: oversight must be demonstrable, which means logged, which means built.

Calibrate the volume. An agent that asks about everything trains its reviewers to approve everything; route by risk so approvals stay rare enough to mean something.

## Escalate on evidence, not vibes

Confidence thresholds are the usual trigger for escalation, and they are necessary and insufficient. Add structural triggers that do not depend on the model's self-assessment: first-time recipients, actions touching more than N records, arguments outside the historical range for this workflow, and any action whose inputs include content from a source the trust boundary marks untrusted. Chapter 06's graders apply here too - sample the autonomous path continuously, because the alternative to finding drift in a sample is finding it in an incident.

## Lab: gate the send

Add an approval queue to the event assistant's send path. Classify actions by reversibility into the three paths. Queue the attendee email with its payload hash, and build a minimal review view: proposed email, recipient count, source records, approve and reject buttons.

Then tamper: modify the recipient list after approval and confirm execution rejects. Let the approval expire. Replay a consumed approval. Measure time-to-decision on the review surface - that number, not the queue depth, is the operational health metric.

## Failure drills

Approve, then edit the action. Replay an approval. Restart the service with approvals pending. Send 50 low-risk requests in an hour and check whether the 51st got real scrutiny. Deny the audit log a write and confirm the action refuses to proceed unaudited.

## Ship gate

No consequential action executes without a live, exact, unconsumed approval, and every decision lands in the audit log first. Oversight works because context survives the handoff - which is what [context and memory systems](/agentic-eng/chapters/context-and-memory/) are for.
