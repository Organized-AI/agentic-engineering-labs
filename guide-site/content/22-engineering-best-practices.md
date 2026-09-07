> **The question:** What has to be true about your engineering before an agent makes it better instead of worse?

Agents amplify whatever engineering culture they land in. Give one a repo with tests, review, and rollback, and it ships faster than you could. Give one a repo with none of that, and it produces plausible breakage at machine speed. The agentic chapters in this guide assume a foundation; this chapter makes that foundation explicit. None of it is new - that is the point.

## The mental model

Every agentic practice in this guide is a load-bearing extension of a classic one. Contracts (chapter 02) are API design. Records (chapter 03) are database discipline. The harness (chapter 05) is error handling and retry policy. Evals (chapter 06) are the test suite. Staging (chapter 07) is CI/CD. Policy (chapter 08) is access control. When a team says "agents don't work for us," the usual finding is that the classic practice underneath was never built.

So the audit runs bottom-up, in dependency order, and each layer is worth doing even if you never run an agent.

## The building blocks, in order

**Version control as the source of truth.** Everything - code, prompts, policies, eval cases, runbooks - lives in git with meaningful commit messages. An agent that cannot see history cannot reason about intent. If the prompt that runs in production isn't a commit, you don't have a system; you have a habit.

**Testing that fails loudly.** Unit tests for logic, integration tests for boundaries, and a suite that runs on every change without human prodding. Chapter 06's graders are a new *kind* of test for a new kind of nondeterminism - they are not a replacement for asserting that `parse_iso8601` handles leap seconds.

**CI/CD with a reversible path.** Every merge builds, tests, and deploys the same way, and every deploy can be undone in minutes. Chapter 07's staging environments are only credible when the boring pipeline already exists. Rollback is a feature you test, not a button you hope exists.

**Code review as knowledge transfer.** Review catches defects, but its deeper job is keeping more than one brain inside every part of the system. Agents make this more important, not less: generated code arrives with no author who understood it, so review becomes the only moment understanding enters the team.

**Documentation and ADRs.** A short design doc before big work, an architecture decision record after big decisions. Agents consume these directly - a harness with access to your ADRs stops re-litigating settled questions, which is the cheapest capability gain in this entire guide.

**Observability basics.** Structured logs, metrics with names you can graph, alerts with owners. Chapters 17 and 06 extend this to traces and evals; none of that stands up if the underlying service can't say what it did.

**Operational hygiene.** Secrets in a manager, least-privilege credentials, dependency updates on a cadence, incident reviews without blame. Chapter 13's agent-security controls are this list applied to a faster adversary.

```python
# Pseudocode: the foundation audit runs before agent adoption.
foundation = [versioned_artifacts, loud_tests, reversible_deploys,
              review_coverage, adrs, service_telemetry, secrets_hygiene]
for block in foundation:
    if block.score(repo) < THRESHOLD:
        fix_first(block)   # agents amplify this gap; they don't paper over it
```

## Lab: run the audit on a real repo

Score one service you own against the seven blocks above, on evidence rather than vibes: can you roll back the last deploy? Do the tests run on a machine that isn't yours? Is the production prompt in git? Write the gap list, fix the cheapest block end to end, and note how much of chapter 05's harness got easier once it landed.

## Failure drills

Revert the last deploy using only the documented path. Break main and watch the alarm catch it before a human does. Rotate a leaked secret. Ask a teammate to explain a six-month-old decision using only the repo. Each drill that fails is a block the next agent will trip over at speed.

## Ship gate

The seven blocks hold under drills, in writing, before agent scope expands. With the foundation load-bearing, there is one thing left to do with this whole guide: [take the challenge](/agentic-eng/chapters/the-challenge/).
