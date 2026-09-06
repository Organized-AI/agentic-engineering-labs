# Agentic Engineering — Offline Starter

Requires Python 3.9 or newer. Uses only the standard library. No network calls,
API keys, real model, paid services, or third-party packages are required.

Download `pipeline.py` and `test_pipeline.py` into the same directory, then run:

```sh
python3 pipeline.py
python3 -m unittest -v test_pipeline.py
```

The demo creates temporary SQLite state, prints one synthetic brief, and cleans
up that temporary state. To preserve synthetic data between runs, opt in:

```sh
python3 pipeline.py --db demo.sqlite
```

Running that command again reuses the same operation instead of duplicating it.

## What it demonstrates

- A tenant-scoped caller operation key with an input fingerprint.
- Duplicate submission and changed-input conflicts.
- Scoped fixture access and job-status reads.
- Temporary worker leases with stale-worker fencing.
- An attempt cap, atomic finalization, and a transactional outbox record.
- Source-version checks, revoked-source checks, and durable restart behavior.
- Thirteen automated tests, including failure paths.

## What it does not demonstrate

This is a teaching simulation, not a deployable agent service. The tenant is a
trusted input from the test harness, not actual authentication. Internal worker
methods assume a trusted worker. SQLite fixtures are not a distributed queue.
There is no outbox relay, distributed clock/lease service, lease renewal,
real model, prompt-injection test, gateway, rate limiter, cost reservation,
retention enforcement, production observability, or complete policy system.

It intentionally persists synthetic input references and generated brief data.
It is not zero-data-retention software. Do not use personal or customer data.
Output verification matches the small fixture contract; it does not prove
factuality or safety of a real model. A brief cannot be regenerated after source
changes with the same operation key; review and submit a new operation instead.

## Exercises

1. Explain every test in business terms before changing the code.
2. Add a failing test before implementing a new behavior.
3. Design an outbox relay and a deduplicating consumer; draw the crash windows.
4. Add a fake provider that fails deterministically on its first attempt.
5. Add a bounded retry scheduler and a task-wide deadline.
6. Add a versioned domain contract, then evaluate an optional real-model adapter
   separately with synthetic data and explicit spending limits.
