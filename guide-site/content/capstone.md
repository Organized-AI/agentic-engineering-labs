Build an event-operations assistant that turns approved event records into a source-backed organizer brief. The system must survive retries, respect access scope, expose uncertainty, and produce enough evidence to measure reliability and cost.

This is deliberately narrower than a fully autonomous event manager. No attendee messages, bookings, payments, or public schedule changes belong in the initial scope.

The full 12-project companion repository is available at
[Organized-AI/agentic-engineering-labs](https://github.com/Organized-AI/agentic-engineering-labs).
Clone it once and run every checkpoint:

```sh
git clone https://github.com/Organized-AI/agentic-engineering-labs.git
cd agentic-engineering-labs
python3 scripts/test_all.py
```

## Start with the offline lab

Download these three files into the same folder:

- [pipeline.py — the SQLite teaching implementation](/agentic-eng/downloads/lab/pipeline.py)
- [test_pipeline.py — the automated failure-path tests](/agentic-eng/downloads/lab/test_pipeline.py)
- [README.md — setup, scope, and exercises](/agentic-eng/downloads/lab/README.md)

Requires Python 3.9 or newer and no additional packages. It makes no network calls and uses no API keys or paid resources.

```sh
python3 pipeline.py
python3 -m unittest -v test_pipeline.py
```

By default, the demo uses temporary SQLite state. To preserve the synthetic example across runs:

```sh
python3 pipeline.py --db demo.sqlite
```

The thirteen tests cover duplicate operations, changed inputs, scoped access, hidden worker tokens, active leases, stale-worker fencing, expiration, atomic/idempotent completion, invalid outputs, changed sources, revoked sources, attempt limits, and restart persistence.

This is **not** a production agent, authentication system, distributed queue, gateway, or ZDR implementation. The model is a deterministic fixture adapter. The lab persists synthetic data and does not test real-model quality. Its value is that selected orchestration invariants are small enough to inspect and execute.

## The target architecture

```text
Authenticated organizer
    ↓ server-derived scope
Request contract + operation key
    ↓ authorized canonical event lookup
Job store + worker claim
    ↓ bounded retrieval of approved source versions
Policy-eligible model route
    ↓ draft with structured facts and unresolved questions
Fact / schema / authorization / source-version checks
    ↓ short atomic transaction
Saved draft + terminal job state + outbox event
    ↓ optional review, with no automatic external sends
Accepted outcome + latency / cost / failure evidence
```

Retention rules apply across the path, not only at the model call. Authorization should be checked again when accessing a tool or finalizing an operation if relevant permissions may have changed.

## Phase 1: deterministic correctness

Begin with synthetic events, sessions, speakers, and venues. Define which records are authoritative and what counts as an unresolved conflict. Keep IDs and source versions in the output.

Use the starter to understand submission, claims, and finalization. Add a source conflict scenario before adding language generation. A correct deterministic baseline makes it easier to distinguish an orchestration bug from an uncertain model output.

**Deliverables:** domain vocabulary, fixture set, input/output contract, passing invariant tests, and a documented failure state.

**Exit criterion:** duplicate requests, foreign records, invalid results, and stale workers cannot produce an accepted brief.

## Phase 2: model integration with bounded behavior

Introduce an adapter that takes approved facts and produces the internal brief schema. Keep provider-specific behavior behind the adapter. Start with one model call rather than an autonomous tool loop.

Set maximum input and output sizes, deadline, and spending limit. Do not send real personal or customer data until the exact processing and retention path is approved. If you add a fallback, require equivalent data eligibility and a passed task suite.

**Deliverables:** versioned prompt, model configuration, response validator, timeout behavior, and a model-specific evaluation report.

**Exit criterion:** failures remain bounded and inspectable; unsupported facts are rejected or explicitly unresolved. A syntactically valid response is not automatically accepted.

## Phase 3: evaluations and adversarial cases

Create representative cases for complete events, missing confirmations, contradictory times, similar venue names, source updates, tool errors, and instructions embedded in documents. Add a cross-tenant record that is highly relevant to the query but never permitted.

Use code to check facts, source ownership, saved outcomes, and forbidden effects. Use a calibrated human or model-assisted rubric for readability. Keep failed attempts in the report.

**Deliverables:** development suite, held-out cases, grader definitions, baseline comparison, and known limitations.

**Exit criterion:** the release gate can fail a persuasive answer that violates a required fact or policy. It reports scenario-level results, not just an aggregate score.

## Phase 4: operational evidence

Run controlled low, typical, and burst workloads with synthetic data. Measure task latency, queue age, attempts, errors, and accepted-outcome cost. Test the spending stop condition before a long benchmark.

Use a synthetic canary to inspect retention on success, retry, and failure paths. Write a deployment and rollback procedure. Demonstrate one recovery rather than merely documenting that recovery should work.

**Deliverables:** load report, retention inventory, cost ledger, deployment instructions, and recovery evidence.

**Exit criterion:** you can explain the tested operating envelope, where data persists, and the cost of a useful result—including unsuccessful attempts and review.

## A six-week learning schedule

This is a suggested sequence for someone who can already build a small service; adjust to your experience and available time.

| Week | Focus | Evidence to keep |
| --- | --- | --- |
| 1 | Experiments and service contracts | Baseline, fixtures, definitions, acceptance rules |
| 2 | Durable jobs and failure recovery | Duplicate, crash, and stale-worker tests |
| 3 | Model gateway and bounded agent behavior | Policy matrix, adapter tests, execution traces |
| 4 | Evaluations and domain semantics | Graders, holdouts, provenance/conflict cases |
| 5 | Load, retention, and outcome cost | Operating envelope, data inventory, unit-cost report |
| 6 | Improve one measured weakness and document handoff | Before/after experiment and release memo |

GPU hosting and kernel work are optional advanced branches. Pursue them when the workload or learning objective justifies them, with a bounded test plan and budget.

## The final review

Answer these without relying on a demo’s happy path:

1. What exactly is the accepted business outcome?
2. Which identity and source records authorize the work?
3. What happens if a request is delivered twice?
4. What stops a stale worker from finalizing?
5. What can the model decide, and what is enforced by code?
6. Which tests check actual effects rather than the final message?
7. What is the largest load you actually tested successfully?
8. Where can content persist, including failures and backups?
9. What is the total cost per accepted outcome?
10. What evidence would make you choose a simpler design?

A strong capstone includes an honest “not tested” section. Do not claim distributed correctness from a single-process simulation, ZDR from the absence of one log file, or real-model safety from deterministic unit tests.
