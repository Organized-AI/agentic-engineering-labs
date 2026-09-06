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

## Guide website source

The complete source for [guide.organizedai.vip/agentic-eng](https://guide.organizedai.vip/agentic-eng/)
is versioned in [`guide-site/`](guide-site/). It includes chapter Markdown,
static-site source, build and verification scripts, generated deployment assets,
research audit records, local font licenses, and the Cloudflare Worker config.

```sh
cd guide-site
npm ci
npm run build
npm run check
```

`node_modules/` and `.wrangler/` are intentionally excluded because they are
reproducible dependency caches and machine-local Cloudflare state.

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
| 01 | [Experimentation](https://guide.organizedai.vip/agentic-eng/chapters/experimentation/) | [Paired experiment ledger](projects/01-experimentation/) | Compare the same cases and explain regressions |
| 02 | [Engineering foundations](https://guide.organizedai.vip/agentic-eng/chapters/engineering-foundations/) | [Tenant-safe event service](projects/02-engineering-foundations/) | Validate contracts and reject stale writes |
| 03 | [Jobs & events](https://guide.organizedai.vip/agentic-eng/chapters/jobs-and-events/) | [Leased job runner](projects/03-jobs-and-events/) | Deduplicate, recover, and fence stale workers |
| 04 | [LLM gateways](https://guide.organizedai.vip/agentic-eng/chapters/llm-gateways/) | [Policy-aware model router](projects/04-llm-gateways/) | Preserve policy and budget during fallback |
| 05 | [Agent design](https://guide.organizedai.vip/agentic-eng/chapters/agent-design/) | [Bounded tool agent](projects/05-agent-design/) | Prevent untrusted text from expanding authority |
| 06 | [Evaluations](https://guide.organizedai.vip/agentic-eng/chapters/evaluations/) | [Outcome evaluation harness](projects/06-evaluations/) | Grade state, repeats, and release gates |
| 07 | [Inference infrastructure](https://guide.organizedai.vip/agentic-eng/chapters/inference-infrastructure/) | [Memory and hosting planner](projects/07-inference-infrastructure/) | Estimate weights/KV cache and compare ownership |
| 08 | [Load testing](https://guide.organizedai.vip/agentic-eng/chapters/load-testing/) | [Queueing workload simulator](projects/08-load-testing/) | Find the goodput saturation point |
| 09 | [Data retention](https://guide.organizedai.vip/agentic-eng/chapters/data-retention/) | [Synthetic canary audit](projects/09-data-retention/) | Find persistence across success and failure paths |
| 10 | [Kernels & performance](https://guide.organizedai.vip/agentic-eng/chapters/kernels-and-performance/) | [Vector-kernel benchmark](projects/10-kernels-and-performance/) | Prove correctness before claiming speedup |
| 11 | [Ontologies & semantics](https://guide.organizedai.vip/agentic-eng/chapters/ontologies/) | [Source-backed domain graph](projects/11-ontologies/) | Resolve canonical facts with provenance |
| 12 | [Cost of cognition](https://guide.organizedai.vip/agentic-eng/chapters/cost-of-cognition/) | [Accepted-outcome ledger](projects/12-cost-of-cognition/) | Include retries, review, and utilization |

## Progress

Use [PROGRESS.md](PROGRESS.md) as a repository checklist. The [website progress
dashboard](https://guide.organizedai.vip/agentic-eng/progress/) tracks four
milestones per chapter in browser storage and can export/import a JSON progress
file. The repository and website use the same stable project slugs.

## Scope

These are instructional simulations, not production templates or compliance
certifications. Passing the tests proves only the named invariants in a small,
controlled environment. Re-check provider behavior, security requirements,
licenses, and retention agreements for a real deployment.
