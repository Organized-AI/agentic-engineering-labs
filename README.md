# Agentic Engineering Labs

Twelve runnable, test-driven projects for the [Organized AI Agentic Engineering field guide](https://guide.organizedai.vip/agentic-eng/).

Every project includes:

- `README.md` — objective, concepts, worked example, build steps, and extension.
- `starter.py` — a deliberately incomplete implementation with marked TODOs.
- `solution.py` — a small reference implementation.
- `test_solution.py` — executable checkpoints for the reference and your work.

The core track uses Python 3.10+ and the standard library only. It makes no
network calls, needs no API keys, and uses synthetic data. Advanced GPU and
provider integrations are documented as optional extensions.

## Quick start

```sh
git clone https://github.com/Organized-AI/agentic-engineering-labs.git
cd agentic-engineering-labs
python3 scripts/test_all.py
```

The current reference suite contains **37 tests across 12 projects**. GitHub
Actions runs the same structure and test commands on every push and pull request.

Run one project:

```sh
cd projects/03-jobs-and-events
python3 -m unittest -v test_solution.py
python3 solution.py
```

To work from the starter, copy it outside the repository's reference path or
edit it directly, then change `test_solution.py` to import `starter` instead of
`solution`. A good rhythm is red → green → refactor: make one test fail for the
right reason, implement the smallest fix, then clean up without changing the
result.

## The projects

| # | Topic | Project | Checkpoint |
| --- | --- | --- | --- |
| 01 | Experimentation | Paired experiment ledger | Compare the same cases and explain regressions |
| 02 | Engineering foundations | Tenant-safe event service | Validate contracts and reject stale writes |
| 03 | Jobs & events | Leased job runner | Deduplicate, recover, and fence stale workers |
| 04 | LLM gateways | Policy-aware model router | Preserve policy and budget during fallback |
| 05 | Agent design | Bounded tool agent | Prevent untrusted text from expanding authority |
| 06 | Evaluations | Outcome evaluation harness | Grade state, repeats, and release gates |
| 07 | Inference infrastructure | Memory and hosting planner | Estimate weights/KV cache and compare ownership |
| 08 | Load testing | Queueing workload simulator | Find the goodput saturation point |
| 09 | Data retention | Synthetic canary audit | Find persistence across success and failure paths |
| 10 | Kernels & performance | Vector-kernel benchmark | Prove correctness before claiming speedup |
| 11 | Ontologies & semantics | Source-backed domain graph | Resolve canonical facts with provenance |
| 12 | Cost of cognition | Accepted-outcome ledger | Include retries, review, and utilization |

## Progress

Use [PROGRESS.md](PROGRESS.md) as a repository checklist. The website tracks four
milestones per chapter in browser storage and can export/import a JSON progress
file. The repository and website use the same stable project slugs.

## Scope

These are instructional simulations, not production templates or compliance
certifications. Passing the tests proves only the named invariants in a small,
controlled environment. Re-check provider behavior, security requirements,
licenses, and retention agreements for a real deployment.
