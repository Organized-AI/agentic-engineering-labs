> **The question:** When the agent calls an API, who is calling?

Chapter 02 gave services contracts and tenant isolation; chapter 05 kept the model from expanding its own authority. Both assume something quietly: that the system can tell who is acting. For an agent, that is genuinely hard. It acts for a user, inside an organization, as a piece of software, sometimes all three in one call.

## The mental model

Separate three identities that are easy to blur. The **agent's own authority** is what the software itself may do: read the event store, write to its scratch space. **User-delegated authority** is what the agent may do because a specific person asked it to: send email as the organizer, within the scope they granted. **Machine-to-machine authority** is service-to-service client credentials, with no user in the picture at all.

Most agent incidents are category errors between these three. An agent that holds the organizer's inbox token and also answers attendee questions has mixed delegated authority with untrusted input - the exact confusion chapter 13's gate exists to reject.

## Issue identity to the workload, not the machine

The traditional answer is a shared service account: one credential, every instance, no way to tell which agent did what. The current direction is per-workload identity. SPIFFE-style systems issue each running agent instance its own short-lived, verifiable credential (an X.509 document bound to that workload), so a credential cannot be lifted off one agent and replayed by another. Google Cloud's Agent Identity follows this model: per-agent credentials that cannot be shared or impersonated like a service account key.

For the event assistant, the payoff is an audit trail that answers "which agent sent this?" instead of "which of the twelve things using this API key sent this?"

## Delegate user authority explicitly

When the agent acts for a person, use a delegated grant, not the person's session. OAuth token exchange is the pattern: the agent presents proof of its own identity plus evidence of the user's consent, and receives a token scoped to the specific action - send this brief, to this organizer, for this long.

```python
# Pseudocode: delegated calls carry both identities.
token = oauth.exchange(
    actor=agent_identity,          # who is calling
    subject=organizer,             # on whose behalf
    scope=["brief:send"],
    audience="mail.internal",
)
mail.send(token, brief_id=brief.id)
```

An IETF working draft is standardizing this shape for agents specifically. Until it settles, the design rule is stable: a delegated token names actor, subject, scope, and expiry, and the receiving service checks all four.

Never let the model supply any of them. The principal comes from the authenticated job, as chapter 05 established; identity claims that arrive as model arguments are untrusted content.

## Authenticate once, authorize everywhere

Authentication answers who; authorization answers what they may do, and it belongs at every tool execution, not at the session boundary. Chapter 02's contracts are the natural home: each tool checks the caller's capability when it runs, because a grant may have narrowed since the job started. Keep the policy in the application or a policy engine, never in the prompt. A model that has read the words "you are authorized" has learned nothing about authorization.

## Lab: three kinds of authority

Model a small directory of principals: the agent itself, an organizer who delegates brief-sending, and a billing service with machine credentials. Give each a credential format and write the verifier that accepts or rejects calls.

Show the category error concretely: let the attendee-facing agent present the organizer's delegated token and confirm the verifier rejects it, because actor and subject do not match the grant. Then expire the grant mid-task and confirm the next call fails closed.

## Failure drills

Replay a stolen token from a different workload. Present a valid agent credential with no delegation for a user-scoped action. Let a delegated grant expire between approval and execution. Supply a forged subject claim. Each case should end in rejection with the failed check named.

## Ship gate

Every effect names an actor, and every user-scoped effect names a subject and scope verified at call time. No shared service-account key stands in for identity. With who settled, the next question is when a human must be in the loop: [human oversight operations](/agentic-eng/chapters/human-oversight/).
