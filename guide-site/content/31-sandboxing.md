> **The question:** The agent wants to run code it wrote itself. What, exactly, do you hand it?

Chapter 29 drew the blast radius for agents that fail. This chapter is about the machine you build so that failing is affordable: the sandbox, the one component whose entire job is to make untrusted execution boring. Agents write code, run shell commands, install packages, and fetch URLs, and every one of those is a loaded capability. The sandbox is where chapter 13's threat models, chapter 14's credential scoping, and chapter 29's walls stop being policy documents and become a place.

## The mental model

A sandbox is a promise with an edge. Inside the edge, code does what code does: reads files, opens sockets, burns CPU. The promise is that none of it crosses - not to the host, not to other tenants, not to credentials it was never given, not to the network it was never allowed. Everything about sandboxing follows from holding that promise precisely: it is not "run the code somewhere safe-ish," it is a boundary you can enumerate, test, and attack.

The corollary nobody enjoys: the sandbox itself is not the security. The boundary is. A container with the host's credentials mounted, an allowlist that permits `*`, and no resource limits is a sandbox in the same way a screen door is a vault. What you audit is always the edge: filesystem, network, credentials, resources, lifetime.

## The five walls of the edge

**Filesystem** - the sandbox sees its own scratch space and nothing else. The host's disk, other tenants' workspaces, and the runtime's stores (chapter 27) are absent, not merely unlisted. **Network** - egress is deny by default with an allowlist per task, because exfiltration is the goal of every injection attack chapter 13 catalogs; an agent that can be tricked into reading secrets should have nowhere to send them. **Credentials** - nothing ambient. No host environment, no cloud metadata endpoint, no inherited tokens; the sandbox receives scoped, single-purpose, short-lived credentials per chapter 14, minted for the task and revoked at teardown. **Resources** - CPU, memory, wall-clock, and output size are capped, because the costly failure from chapter 29 applies to code the model wrote at 3 AM. **Lifetime** - sandboxes are created per task or per session, checkpointed work lands in stores outside the boundary, and teardown is total. An ephemeral sandbox turns a whole class of persistence attacks into litter.

```python
# Pseudocode: sandbox-per-task for the event assistant's report generator.
def run_generated_report(task, tenant):
    sb = sandboxes.create(image="report-runner", owner=tenant)   # fresh, empty
    sb.policy.egress.allow_only(["api.venue-db.internal"])       # deny by default
    sb.policy.resources.cap(cpu_s=60, mem_mb=512, wall_s=300)
    creds = mint(scope="venue:read", ttl=task.deadline)          # chapter 14
    try:
        result = sb.exec(task.code, env={"VENUE_TOKEN": creds.token})
        stores.write(f"reports/{task.id}", result.output)        # state leaves the box
        return result
    finally:
        creds.revoke(); sb.destroy()                             # teardown is total
```

## The Cloudflare preference

For runtimes already on Cloudflare, the Sandbox SDK is the concrete version of all five walls. Built on Workers and Containers, each sandbox is its own isolated container with a full Linux environment, and the isolation key is one line: `getSandbox(env.Sandbox, tenant_id)` hands each tenant or task a separate box. The API covers the chapter's whole checklist - executing commands and code with automatic result capture, managing files, running background processes, exposing services on purpose rather than by accident - while the Worker outside the boundary stays the policy choke point from chapter 25. Egress is handled deliberately (the docs ship a dedicated guide for outbound traffic), persistence belongs outside the sandbox in R2 or D1 rather than in the container, and the whole thing runs where the rest of this guide's runtime already lives. When the process exists on Cloudflare, preferring its sandbox over a bespoke container rig is not brand loyalty; it is fewer boundaries to draw, audit, and keep true.

## Lab: five walls, tested as five attacks

Stand up the report generator sandboxed per the pattern above, then attack each wall in turn. Read `/etc/host-config` from inside - it must not exist. Exfiltrate the task token to an unlisted host - the egress policy must deny and log. Enumerate the environment for ambient credentials - there must be none. Fork-bomb the box - the resource caps must contain it, and the runtime must survive to log the attempt. Finally, destroy the sandbox mid-run and confirm the only surviving state is what was written to the store outside. A wall that was never attacked is an assumption, not a boundary.

## Failure drills

Widen the egress allowlist to `*` for one task and watch the exfiltration drill turn green - that is how quiet a bad default is. Hand the sandbox a token with `write` scope it does not need and let chapter 13's injection use it. Leave a sandbox running past its task and inventory what accumulated in it. Restore a checkpoint from a different tenant's store namespace and check whether the sandbox notices. Mount the host filesystem read-only "just for debugging" and time how long it takes to forget it is there.

## Ship gate

Untrusted code runs only inside a sandbox with an enumerated edge: own filesystem, deny-by-default egress with a per-task allowlist, scoped and revocable credentials minted per task, hard resource caps, and a lifetime that ends in total teardown. State that must survive lives outside the boundary, and every wall has a drill that last proved it. The loop runs, the failures are contained, and the code the model writes has somewhere honest to execute - which is most of what the guide knows how to promise, and a good place to attempt [the challenge](/agentic-eng/chapters/the-challenge/).

Sources: [Cloudflare Sandbox SDK](https://developers.cloudflare.com/sandbox/), [Sandbox architecture and lifecycle](https://developers.cloudflare.com/sandbox/concepts/architecture/), [Handle outbound traffic](https://developers.cloudflare.com/sandbox/guides/handle-outbound-traffic/), [Sandboxes, generally available](https://blog.cloudflare.com/sandbox-ga/)
