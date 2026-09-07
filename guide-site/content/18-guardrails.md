> **The question:** What checks every request and response, no matter what the model decided?

Chapters 04 and 05 put policy in the gateway and the harness. Guardrails are the productized version of that instinct: input screening, output validation, topic boundaries, PII redaction, jailbreak detection - as infrastructure with a named owner, a latency budget, and a failure mode, not as a paragraph in the system prompt.

## The mental model

A guardrail is a check in the request path with three properties: it runs on every call it covers, its decision is logged, and its failure mode is chosen in advance. **Input rails** screen what enters: injection patterns, off-topic requests, PII that should never reach the model. **Output rails** screen what leaves: schema validation, forbidden content, leaked tenant data. Productized options exist (NVIDIA's NeMo Guardrails, the Llama Guard family), but the architecture question comes first, because it determines what the rails can see and what they cost.

## Placement is the design decision

Rails can sit in the application, at the gateway of chapter 04, or both. Gateway placement wins on coverage: every provider call passes through one policy point, and the rail config becomes part of the gateway's policy document rather than scattered app code. Application placement wins on context: the app knows the task, the tenant, and the record being drafted, so its checks can be semantic instead of generic.

The common 2026 shape is layered: cheap, generic rails at the gateway (injection signatures, PII patterns), semantic checks in the application (is this brief about the right event, does it cite the approved records), and chapter 05's approval gate for effects. Each layer catches what the others cannot see.

## Budget the latency honestly

Every rail adds milliseconds and its own failure rate. A jailbreak classifier on every input and an LLM-based output check on every response can double the tail latency chapter 08 taught you to measure. So: run cheap rails inline, expensive rails on sampled or high-risk traffic, and never let a rail's timeout become an open door - choose fail-closed for consequential paths, fail-open-with-alerting for the rest, and write the choice down.

```python
# Pseudocode: rails compose, and each failure mode is explicit.
def guarded_call(request):
    if not input_rails.check(request):        # cheap, inline
        return reject("input rail", log=True)
    response = model.call(request)
    verdict = output_rails.check(response)    # semantic, app-side
    if verdict.timeout:
        return fail_closed(response) if request.consequential else alert_and_pass(response)
    return verdict.apply(response)
```

Two operational rules complete the picture. Version the rulesets like code: every logged decision names the ruleset version, so a false positive from three weeks ago can be reproduced against the rules that fired it. And review the logs on a cadence - rails that never fire are either perfectly tuned or checking nothing, and you cannot tell which from the dashboard alone. When in doubt, replay last month's traffic against the current ruleset offline and count what would have fired.

## Lab: rails with receipts

Add two rails to the event assistant: a gateway-pattern input rail that flags injection phrases and attendee PII in prompts, and an application-side output rail that validates every brief against the approved-record schema of chapter 02. Log every decision.

Measure the latency each rail adds at the chapter 08 harness's p50 and p99, then decide which stays inline. Finally, make the output rail time out and confirm the consequential path fails closed while the dashboard draft path fails open with an alert.

## Failure drills

Feed a jailbreak string the input rail misses and confirm the output rail or the approval gate still stops the effect. Inject PII into a tool result, bypassing the input rail entirely. Time out a rail mid-request. Update a rail's ruleset and check that old logs still name the version that decided.

## Ship gate

Every covered call passes named rails with logged decisions, each rail has a measured latency cost and a written failure mode, and no rail's absence silently opens a path. Rails constrain behavior; the next chapter prices the alternatives for changing it: [adaptation economics](/agentic-eng/chapters/adaptation-economics/).
