> **The question:** Should your agent reach the world through a protocol built for models, or through the command line it already knows?

Every tool an agent uses arrives through one of two doors. The newer door is MCP, the Model Context Protocol: a typed, discoverable interface where servers advertise tools, resources, and prompts that a client can enumerate and call with structured arguments. The older door is the CLI: the agent runs shell commands, reads stdout, and chains what it finds. Both are load-bearing choices, because the door determines the agent's context budget, its failure modes, and most of its security surface.

## The mental model

MCP is a contract; the CLI is a culture. An MCP server declares its tools with names, descriptions, and JSON schemas - the client can list them, validate arguments before sending, and get structured results back. A CLI declares nothing: the agent learns it the way you did, from `--help`, man pages, and muscle memory embedded in training data. That difference propagates everywhere. MCP spends tokens upfront on tool definitions and buys precision; the CLI spends tokens on exploration and buys ubiquity.

The honest framing: MCP answers "how does a model call this capability safely and uniformly across clients," and the CLI answers "how does this capability exist at all." Most CLIs predate agents by decades. Most MCP servers are months old.

## How the runtime sees each door

The runtime is the loop around the model: it feeds tools in, executes calls, and feeds results back. The door changes what that loop can guarantee.

With MCP, the runtime is a client. It connects to servers, holds sessions, and can treat every call as a typed operation: arguments validated against a schema before execution, results parsed into structure, server identity pinned and audited. The loop can enforce policy per tool - which servers are mounted, which tools are exposed to the model this run, which calls need approval - because every call has a name and a shape. The cost is lifecycle: the runtime must spawn, supervise, reconnect, and version servers, and a hung server is a hung capability.

The recent spec update shrinks that cost. Under the Streamable HTTP transport, session state is optional: a server that never assigns a session ID is stateless, and every request arrives self-contained, like any web API. A stateless MCP server is a plain HTTP handler - it scales horizontally behind a load balancer, restarts mid-conversation without ceremony, and a hung one is a failed request to retry, not a capability the runtime must nurse back to life. Session supervision, reconnection, and the 404-expired-session dance all dissolve on the client side. What you give up is everything that needed the session: server-pushed notifications, subscriptions, and resumable streams.

With the CLI, the runtime is a shell host. It gets one tool - run a command - and the model supplies the intelligence. The loop's guarantees drop to OS level: exit codes, timeouts, working directories, and whatever sandbox wraps the shell. Policy becomes pattern matching on command strings, which is why chapter 15's allowlists matter more here. The gain is resilience: there is no server to hang, only processes to kill, and every tool the OS already has is in reach.

A hybrid runtime does what serious runtimes now do: mount a small set of pinned MCP servers for stateful, structured services, and keep a shell for everything composable. The routing question below is run per capability, not per agent.

## Where MCP wins

**Structure at the boundary.** Typed schemas mean the harness can validate a call before it executes - the same discipline chapter 02 applies to contracts. A calendar MCP server can reject a malformed date before it becomes a wrong event.

**Discovery without exploration cost.** `tools/list` is one round trip. The CLI equivalent - run `--help`, parse prose, guess flags - burns thousands of tokens per capability and still guesses.

**State and sessions.** MCP servers hold connections, auth, and subscriptions. A database server keeps one connection pool instead of every call paying a fresh login. Resources and notifications let the server push changes instead of the agent polling. And when you need none of that, stateless mode keeps the typed boundary without the session tax.

**Uniformity across clients.** One server serves every MCP client. Write the capability once and every harness in this guide can use it with the same schemas.

## Where the CLI wins

**Zero new infrastructure.** The capability already exists, documented, tested, and installed. Wrapping `gh`, `git`, or `ffmpeg` in an MCP server is work that buys nothing when the agent already composes them fluently: pipes, exit codes, and fifty years of conventions are the interface.

**Composability the protocol can't express.** `gh pr list --json number,title | jq '.[0]'` is two tools doing something neither was designed for. MCP tools compose only through the model, one structured call at a time.

**Context economy.** Tool schemas sit in the system prompt on every call. Fifty MCP tools can eat 10,000 tokens before the conversation starts. A CLI agent carries no such tax; it discovers tools when needed and forgets them after.

**Auditability.** A shell command is a string a human can read, log, diff, and replay. Chapter 15's oversight queue approves commands a reviewer can actually evaluate.

## Best practices, per door

For MCP servers, the practices are the contract practices, applied one level down:

- Default to stateless. Take on session state only for capabilities that genuinely push or subscribe; a stateless server inherits forty years of hard-won web-operations practice.
- Pin servers by version and hash, and diff tool descriptions on upgrade - chapter 13's rug-pull drill, run as routine maintenance.
- Mount the smallest tool surface the task needs. Every unused schema is context tax and attack surface.
- Put auth and rate limits inside the server, not in prompts. A policy the model can talk its way around is not a policy.
- Return small, typed results. A server that dumps ten thousand lines through the protocol recreates the CLI's worst failure mode with extra steps.
- Supervise servers like services: health checks, restarts, and a circuit breaker the runtime can trip.

For the CLI, the practices are the shell practices, tightened for a caller that never gets tired:

- Allowlist commands and flag shapes; treat everything else as an approval request, per chapter 15.
- Constrain the environment: a dedicated working directory, scoped credentials, no network where none is needed, a sandbox for anything risky.
- Prefer tools with machine-readable output (`--json` flags) and set them as defaults, so the model parses structure instead of prose.
- Cap output size on every call and teach the agent to page (`head`, `--limit`, filters) before reading.
- Log every command verbatim. The audit trail is the CLI's native advantage - spend nothing to keep it.

## The decision matrix

| Dimension | MCP | CLI |
| --- | --- | --- |
| Argument validation | Schema-checked before execution | Nothing checks flags until they run |
| Discovery cost | One `tools/list` round trip | `--help` exploration, thousands of tokens |
| State and sessions | Optional; stateless mode or held sessions | Stateless by nature; state lives in files |
| Composability | Through the model, one call at a time | Pipes, scripts, fifty years of idioms |
| Context tax | Tool schemas on every call | Zero until the agent explores |
| Audit trail | Typed calls, server-side logs | A readable, replayable command string |
| Deterministic repetition | Model stays in the loop on every run | Patterns harden into scripts - model leaves the loop |
| Failure blast radius | Concentrated in pinned, named servers | Spread across everything in PATH |
| Runtime duty | Client: supervise servers (stateful only) | Shell host: timeouts, sandboxes, kill |

The determinism row deserves pressure-testing, because it decides real architectures. A stateless MCP call with fixed arguments is exactly as deterministic as a CLI command - the door creates no variance; the model generating arguments does. So the honest question for a repeated, accuracy-critical task is not which door, but whether the model should be in the loop at all. This is where the CLI pulls ahead in a way no protocol can match: a proven CLI pipeline lifts out of the model entirely into a script, a cron job, a CI step - byte-exact, testable, replayable, reviewed like any code. An MCP capability cannot make that trip; calling it always requires a client and a model, so every run re-rolls the argument generation. The flip side is real too: model-driven CLI use hallucinates flags and misparses prose, while MCP schemas catch malformed arguments before execution. The synthesis: while a pattern is still being discovered, MCP's typed boundary is the safer door; once the pattern repeats and accuracy matters, harden it into a script and let the model call the script - one CLI tool instead of fifty schema entries.

## The failure modes trade against each other

MCP's risks are the chapter 13 risks: tool-description rug pulls, poisoned servers in a registry, schemas that validate while semantics lie. The CLI's risks are older: injection through flags, unbounded shells, unstructured output parsed wrong. Neither door is safer by default - MCP concentrates trust in fewer, named servers; the CLI spreads it across everything in PATH.

```python
# Pseudocode: the routing question, asked per capability.
def door(capability):
    if capability.is_repeated and capability.must_be_exact:
        return "script"         # lift it out of the model; no door at all
    if capability.needs_session or capability.has_complex_schema:
        return "mcp"            # typed calls, held state, push updates
    if capability.already_installed and capability.composes_with_pipes:
        return "cli"            # zero new surface, readable audit trail
    return "cli_behind_a_wrapper"  # thin adapter, not a new protocol
```

## Lab: port one capability through both doors

Take the event assistant's calendar. First drive it through the CLI: list events, create one, handle an error from stderr and a nonzero exit. Then build the MCP server from scratch - a single HTTP endpoint that answers `initialize`, `tools/list`, and `tools/call` with typed schemas, and deliberately stateless: it assigns no session ID, so every request stands alone. Now watch the client side of the runtime section evaporate. There is no session to supervise, no reconnect logic to write, no expired-session 404 to handle; a crashed server is one failed request and a retry. Measure both doors: tokens spent on discovery, validation errors caught before execution, and lines of code you now maintain - the stateless build keeps MCP's typed boundary at a code cost close to the CLI wrapper it replaces. The numbers, not the discourse, pick your door.

## Failure drills

Rename a flag in the CLI version and watch the agent recover from `--help`. Change a tool description in the MCP server without changing its schema and watch the harness trust it. Kill the MCP server mid-call - first stateful, then stateless - and count the dangling state in one and the clean retry in the other. Pipe ten thousand lines into the agent's context by accident. Each drill names which door absorbed the blow - and which runtime guarantee, session supervision or process isolation, contained it.

## Ship gate

Every capability the agent uses has a chosen door, chosen on measurement: discovery cost, validation strength, session needs, determinism requirements, and audit surface are recorded per tool - and anything repeated and exact has been hardened into a script with the model out of the loop. Where MCP runs, servers are pinned, supervised, and descriptions verified per chapter 13; where the CLI runs, commands are allowlisted, sandboxed, and logged per chapter 15. The door decision is documented like any other contract - which makes it examinable in the same way the rest of the system is, right up to [the challenge](/agentic-eng/chapters/the-challenge/).

Sources: [MCP introduction](https://modelcontextprotocol.io/docs/getting-started/intro), [Anthropic: introducing the Model Context Protocol](https://www.anthropic.com/news/model-context-protocol), [MCP specification](https://modelcontextprotocol.io/specification/2025-06-18), [Streamable HTTP transport](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports), [Claude Code overview](https://code.claude.com/docs/en/overview)
