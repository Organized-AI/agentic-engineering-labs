> **The question:** When your runtime restarts tomorrow morning, what does it remember - and who decided?

Chapter 26 ended with a restart policy that works. What it quietly assumed is that restarting is safe - that whatever the process held in memory was either disposable or saved. That assumption is the most expensive one in agent systems, because agents accumulate state by nature: the conversation so far, the session the tool server assigned, the half-finished plan, the memory it was supposed to write down. Statelessness is not the absence of state. It is the discipline of putting every piece of state in a place you chose, with an owner, a lifetime, and a recovery story.

## The mental model

Every piece of agent state lives in exactly one of three places, and the places have different physics. **Context** is the model's working memory: fast, lossy, bounded by the window, and rebuilt from scratch every process start. **Session** is a server's working memory: the tool connection, the auth handshake, the in-flight subscriptions - state someone else's process holds on your behalf, keyed by an ID you must present. **Stores** are the only durable home: the transcripts, checkpoints, and memory types of chapter 16, written atomically and readable after any restart.

The discipline is a default and a burden of proof. Default to stateless: every request self-contained, every restart free, every component replaceable. Take on session state only when a capability genuinely needs it - a pushed subscription, a held database connection - and treat that need as a cost you argued for, not a convenience you drifted into.

## The stateless default

Chapter 24 made the case at the protocol layer: a stateless MCP server assigns no session ID, so each request stands alone and a hung server is a failed request, not a hung capability. The same default applies one layer up, to the runtime itself. A stateless runtime turn reads its state from stores, acts, and writes its state back; the process holding it is interchangeable. That buys the operational properties chapter 26 promised: restarts become free, scaling becomes adding copies, and a wedged process is a retry instead of an incident.

The test is brutal and simple: kill the runtime between any two lines of code, start a fresh process, and the turn completes correctly. Whatever fails that test is state living in the wrong place.

## When sessions earn their keep

Some capabilities are stateful by nature, and pretending otherwise costs more than it saves. A database connection pool avoids a login per call. A subscription pushes updates the agent would otherwise poll for. A long tool workflow holds intermediate artifacts no store schema anticipates. The honest pattern is to contain the session, not to spread it: the session lives inside one supervised component (chapter 26), never leaks its ID into the model's context as a fact to reason about, and always has a rebuild path - if the session dies, the component re-establishes it from stores and replays from the last checkpoint, per chapter 03's at-least-once discipline.

```python
# Pseudocode: the state audit, run per component.
def audit(component):
    for state in component.state_inventory():
        match state.home:
            case "context":  assert state.rebuildable_from("stores")
            case "session":  assert state.has_rebuild_path and state.owned_by_one_component
            case "stores":   assert state.atomic_write and state.has_lifetime
            case None:       raise StateLeak(component, state)  # found by accident, owned by nobody
```

The last case is the one that bites: state nobody inventoried. The model's plan half-finished in a local variable, the recipient list cached in a module global. Chapter 16 gave memory types names; this audit gives everything else a name too, or deletes it.

## Resumability is the acceptance test

The proof of the discipline is resumability: a fresh process reconstructs a useful agent from stores alone. Context rebuilds from transcript and checkpoint. Sessions re-establish on demand. In-flight work resumes idempotently - chapter 03's outbox means the briefing send happens exactly once even if the restart lands between commit and ack. When resumability holds, statelessness stops being a purity argument and becomes what it actually is: the cheapest possible failure mode.

## Lab: one service, both ways

Build the event assistant's calendar service twice. First stateful: a session ID assigned at connect, subscriptions held in process memory, reads served from a per-session cache. Then stateless: no session ID, every request carrying what it needs, reads served from a shared store. Kill each mid-operation and record what the client must do to recover: for the stateful build, detect the dead session, re-authenticate, re-subscribe, and discover which reads were stale; for the stateless build, retry the request. The delta between those two recovery procedures is the true price of the session - measure it before you argue for one.

## Failure drills

Kill the runtime mid-turn and list what was lost - anything on that list without a store home is a finding. Expire the tool session server-side and watch whether the client rebuilds or errors out. Restart the stateful build twice in a row and check whether subscriptions double up. Corrupt the checkpoint and confirm the runtime refuses to resume rather than resuming wrong. Replay chapter 26's wedged-server drill against both builds and compare the blast radius.

## Ship gate

Every component has a state inventory; every entry names its home (context, session, or stores), its owner, its lifetime, and its recovery path. The default is stateless, and every session in the system has a written justification and a rebuild path. The kill-between-any-two-lines test passes. Resumability from stores alone is demonstrated, not assumed. With state disciplined, the runtime can finally be left running - which means it needs to know when to wake up: [scheduling and event-driven agents](/agentic-eng/chapters/scheduling-event-driven-agents/).
