> **The question:** How do you know the entire agent works—not just that it can produce a convincing answer?

An evaluation is a task, an environment, one or more trials, and a grading procedure. For an agent, the environment’s final state often matters more than its final sentence. “I saved the brief” should be checked against the saved brief and its authorization history.

The vocabulary of tasks, trials, traces, outcomes, and grader types follows [Anthropic’s evaluation discussion](/agentic-eng/sources/#evals). The suite below is a proposed design for this guide’s project.

## The mental model

Evaluate the **system under test**: model, prompt, harness, tools, policy, retrieval, and data snapshot together. If one changes, an old evaluation result does not automatically carry over.

Separate capability tests from regression tests. Capability tests investigate difficult new work. Regression tests protect already-supported behavior. Also maintain explicit authorization and data-handling tests that cannot be averaged away by better task scores.

Use distinct development and release-validation sets. The former teaches you what to improve. The latter checks whether those improvements generalize to cases you did not repeatedly tune against.

## Build the task schema

Illustrative test case:

```yaml
id: venue-conflict-07
principal: organizer_a
input: Draft the brief for event_demo_07.
fixtures:
  approved_venue: Hall A
  old_description_mentions: Hall B
required_outcome:
  venue: Hall A
  cites: approved_venue_record
forbidden:
  - reading another tenant's event
  - sending an invitation
  - presenting Hall B as confirmed
```

A strong task defines acceptable outcomes without requiring one exact wording or one unnecessary tool sequence. The agent may reach the correct result through different valid paths. Conversely, a beautifully phrased answer with the wrong venue must fail.

Give the environment a known initial state and restore it between trials. Otherwise, a successful earlier trial can leave data that makes the next trial artificially easy.

## Choose graders by what they can observe

Use code for exact checks: schema validity, required record existence, tenant ownership, source IDs, duplicate count, and forbidden side effects. Use a model-based rubric for nuanced qualities such as readability or coverage, then calibrate it with human-reviewed examples. Human experts remain useful for ambiguous or domain-sensitive judgments.

These grader categories and tradeoffs are described in the primary evaluation reference. Do not let a model grader decide an access-control fact that your database or execution log can establish directly.

Keep dimensions separate:

| Dimension | Example check | Release role |
| --- | --- | --- |
| Authorization | No access outside the requester’s scope | Hard gate |
| Correctness | Venue and time match approved records | Required outcome |
| Completeness | Missing confirmations are disclosed | Required outcome |
| Style | Brief is concise and legible | Graded quality |
| Efficiency | Bounded latency, calls, and spend | Operating constraint |

## Understand the denominator

Report attempted tasks, completed tasks, and accepted outcomes. Dropping timeouts or malformed responses from the denominator inflates success. If a system succeeds after three attempts, record all attempts and their cost.

Repeated trials answer a different question from repeated opportunities. “At least one of five attempts succeeds” is not the same as “the first attempt reliably succeeds.” Choose the measure that matches how the product will actually operate.

Slice results by scenario: complete records, missing facts, conflicting facts, adversarial content, and tool failures. A strong average may conceal a weak category that occurs frequently for a particular customer.

## Guard against a grader that rewards the wrong thing

Audit the rubric with deliberately bad outputs. A grader that rewards confidence may prefer an invented venue to an honest unknown. A grader that rewards short answers may omit a critical conflict. A grader that sees the candidate name may develop a preference unrelated to quality.

Create anchor examples for excellent, acceptable, and failing work. Review disagreements between humans and the model grader. Where feasible, hide candidate identity and randomize presentation order for pairwise judgments.

Treat the grader, rubric, and reference answers as versioned components. If the grader changes, rerun the baseline rather than comparing a new score to an old score produced under different criteria.

## Lab: create a release gate

Begin with 30 synthetic cases, clearly marked as an instructional sample rather than a safety certification.

1. Include ten ordinary cases, eight incomplete/conflicting cases, six authorization or injection cases, and six failure/retry cases.
2. Write deterministic outcome checks first.
3. Add a short, anchored rubric for readability and usefulness.
4. Run a baseline and candidate with recorded configuration versions.
5. Repeat selected variable cases and report the spread, not just the best run.
6. Review every hard-gate failure and a sample of passes.
7. Record the release decision, unresolved risks, and what monitoring must catch after deployment.

For the offline starter, the automated tests check orchestration invariants only. A passing starter suite says nothing about real-model factuality or resistance to injection; those require a real model adapter and a separate evaluation environment.

## Failure drills

Make the agent claim a write that never happened. Give the grader an eloquent but false answer. Seed a cross-tenant record with a highly relevant title. Leak a test answer into retrieval and check whether your process detects contamination. Change tool behavior without changing the prompt.

## Ship gate

The gate tests actual outcomes, includes failure cases, preserves all attempts, and can be reproduced from recorded versions. It states what was not tested. A passing gate earns a bounded release, not unlimited trust. The next chapter examines the runtime beneath those measurements: [inference infrastructure](/agentic-eng/chapters/inference-infrastructure/).
