> **The question:** When the agent did something weird last Tuesday, which of your three signals tells you why?

Agent systems produce three kinds of evidence: **logs** (structured events - what happened), **traces** (causal spans - why it happened), and **evals** (scores - whether it went well). Teams usually have one, partly. This chapter is about running all three as one system, because each answers a question the other two cannot.

## The mental model

A log line says the send tool ran at 14:02:11 and returned 200. A trace says it ran because the model chose it after reading the organizer's note, which came from record version 7. An eval says the resulting brief was wrong about the venue. The Tuesday question - "why did it do that" - is only answerable when the three join on one identifier: the task id in the log line is the trace id is the eval case's subject.

Chapter 02 specified structured logs; chapter 06 built the graders. This chapter is the plumbing that connects them to the agent's reasoning.

## Logs: events with joins, not prose

Every component emits structured events with the task id, the principal, and the record versions it touched - the same fields chapter 02 put in contracts. The agent's own events join the same stream: model calls with token counts, tool calls with outcomes, policy checks with their verdicts. A log you cannot join to a trace is a diary; a joined one is evidence.

## Traces: the reasoning layer, as spans

Trace one span per model call, tool call, and retrieval, parented under the task. OpenTelemetry's GenAI semantic conventions - already in this guide's sources - standardize the names, so staging and production traces mean the same things. Langfuse (open source) and LangSmith are the common stacks; the convention matters more than the vendor.

Spans carry prompts and outputs only by deliberate choice. Chapter 09's retention rules apply to telemetry with full force: default to metadata (token counts, latency, tool names, input hashes) and capture content per environment, under the persistence inventory.

## Evals: scores attached to live traffic

The move most teams miss: evals are not only the pre-release gate of chapter 06. Attach graders to sampled production traces, score live work continuously, and feed failures back into the offline suite so every production surprise becomes a permanent regression test.

```python
# Pseudocode: the three signals join on the task id.
for trace in sample(production_traces, rate=0.02):
    score = graders.run(trace)                        # eval
    log.event("eval.scored", task_id=trace.task_id,   # log
              score=score.value, grader=score.grader)
    metrics.record(score, tags=trace.tags)
    if score.failed():
        eval_suite.add_case(trace.to_case())          # surprise becomes a test
```

Alert on behavior, not just crashes: tool success rates, policy rejections per check, grader drift, retry storms, and chapter 12's cost per accepted outcome. Each alert names an owner before launch.

## Lab: join the three signals

Instrument the event assistant: structured logs with task ids, spans for model and tools (metadata-only), and one grader sampled onto live traces. Run chapter 05's adversarial cases and answer three questions, one per signal: what happened (log), why (trace), and was it good (eval). Then inject a failure class the offline suite lacks and watch it become a case automatically.

Measure the time from "something looks off" to the span that explains it. That latency is what this chapter exists to shrink.

## Failure drills

Lose a span's parent and check the trace stays readable. Emit content where only metadata belongs and confirm redaction catches it. Let a grader silently stop running and confirm the absence alarms. Produce a log line without a task id and let the join check reject it. Drop 90% of spans under load and verify error rates stay visible.

## Ship gate

Any task can be reconstructed from its three signals without capturing content by default, and sampled production scores flow into the offline suite automatically. Seeing the system is half of operating it; constraining what passes through it is next: [guardrails in the request path](/agentic-eng/chapters/guardrails/).
