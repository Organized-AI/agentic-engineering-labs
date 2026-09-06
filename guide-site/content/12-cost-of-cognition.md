> **The question:** What does it cost to produce a result that the business can actually use?

Cheap tokens do not guarantee cheap outcomes. A low-cost model that needs repeated attempts and substantial human correction can be expensive at the task level. A higher-cost model can also be wasteful if a deterministic rule would do the job.

Use business value and allocation as the frame, consistent with the [FinOps for AI discussion](/agentic-eng/sources/#finops). The formulas and numbers below are original instructional examples, not vendor prices, forecasts, or claims about Bryan’s business.

## Define the unit before counting cost

For this project, define an accepted outcome as a brief with correct approved facts, explicit unresolved questions, permitted data access, and delivery within the required time.

Then calculate:

```text
cost per accepted outcome =
  total attributable cost of all attempted work
  / number of accepted outcomes
```

Include unsuccessful attempts in the numerator. If no outcome was accepted, report the cost and zero accepted outcomes rather than inventing a finite unit cost.

Useful components include model usage, GPU/runtime cost, tool/API charges, storage, retries, human review, and an explicitly chosen allocation of operating effort. Keep marginal and fully loaded costs separate when they answer different decisions.

## Worked example: cheaper total, worse unit cost

Two configurations process the same 300 representative tasks under identical acceptance criteria:

| Configuration | Total attributable cost | Accepted outcomes | Cost per accepted outcome |
| --- | ---: | ---: | ---: |
| A | $120 | 80 | $1.50 |
| B | $300 | 290 | about $1.03 |

These hypothetical results do not prove that more expensive models are better. They show why comparing only total spend or price per token can select the wrong system.

Inspect which tasks fail. If A works well for simple events, a validated routing policy may use it for that subset and reserve B for others. Measure the combined system on the real task mix before claiming savings.

## Add retry and review costs

In a simplified model with independent failure probability `p` and at most three attempts, the expected attempt count is `1 + p + p²`. If `p = 0.2`, that is 1.24 attempts, not one. The probability of success within three attempts is `1 - p³ = 0.992` under those same assumptions.

Real failures are often correlated: an outage, invalid prompt, or missing record may cause every retry to fail. Therefore, use measured retry behavior for budgeting rather than assuming independent chances.

Human correction can dominate inference spending. At a hypothetical $60 per hour, two minutes of review costs $2. If an optimization saves $0.05 in model usage but adds a minute of correction, it increases total task cost under those assumptions.

Track review time separately from automated latency. A workflow that returns quickly but waits hours in a human queue may not satisfy the business deadline.

## Route by evidence, not model reputation

A proposed cascade might run a cheaper eligible route first and escalate difficult cases. A rough two-stage cost estimate is:

```text
expected model cost = first-route cost
                    + escalation rate × second-route cost
```

This omits review, retries, and other services. More importantly, it assumes the escalation mechanism identifies unsuitable first-stage results well enough. Confidently accepting bad cheap answers creates artificial savings.

Evaluate the selector as part of the system. Measure false acceptance, unnecessary escalation, accepted-outcome cost, and tail latency. Data-handling eligibility must be enforced before any cost-based choice, as discussed in the gateway chapter.

## Understand hosting break-even

For an illustrative comparison with equal accepted-outcome quality:

```text
managed cost = accepted outcomes × managed unit cost
self-operated cost = fixed operating cost
                   + accepted outcomes × variable unit cost

break-even outcomes = fixed operating cost
                    / (managed unit cost - variable unit cost)
```

If fixed cost is $2,000 per month, managed cost is $0.05 per accepted task, and self-operated variable cost is $0.01, the arithmetic gives 50,000 accepted tasks per month. These are invented numbers. If the denominator is zero or negative, that simple model has no positive break-even point.

The calculation is only useful if the capacity can handle the arrival distribution at the required quality and latency. Add idle time, utilization uncertainty, engineering effort, redundancy, upgrade testing, and incident handling. A theoretical break-even that assumes perfect utilization is not a deployment decision.

## Lab: build an outcome-cost ledger

For each attempted task, record task class, configuration version, all attempts, model/tool cost, runtime allocation, review time, acceptance outcome, and elapsed delivery time.

1. Run a baseline and candidate on the same representative cases.
2. Calculate both marginal and fully loaded cost per accepted outcome.
3. Break down the largest costs by stage and task class.
4. Propose one optimization: fewer irrelevant tokens, a better lookup, less retrying, or a different route.
5. Repeat the comparison with unchanged acceptance criteria.
6. Run a sensitivity analysis for demand, review time, and utilization.

The best first optimization may be fixing a business-data conflict that repeatedly causes review, rather than switching models.

## Failure drills

Remove failed attempts from a report and observe the distortion. Double review time. Cut demand in half while retaining the same reserved capacity. Introduce a provider outage that causes correlated retries. Change the accepted task mix and check whether the earlier unit-cost comparison still applies.

## Ship gate

You can explain the denominator, include the costs of failures, identify the largest controllable cost, and show that an optimization preserves quality and permissions. You can justify both what you operate and what you choose not to operate.

Now combine the chapters in the [capstone and offline starter lab](/agentic-eng/capstone/). The objective is one measurable, recoverable system—not the largest possible stack.
