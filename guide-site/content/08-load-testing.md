> **The question:** How much useful work can the system complete before latency, reliability, or quality becomes unacceptable?

A performance test is not a screenshot of tokens per second. It is a reproducible workload, a declared measurement boundary, a configuration, and an interpretation. The most useful capacity number is the load at which the complete service still meets its requirements.

Use synthetic or approved data, set an explicit spending cap, and define stop conditions before testing paid endpoints or rented hardware.

## The mental model

Separate latency, throughput, and **goodput**. Latency describes elapsed time for a request. Throughput counts completed work per unit time. In this guide, goodput means accepted outcomes completed within the required constraints per unit time.

A system can increase throughput by producing shorter, lower-quality answers. It can improve reported latency by excluding failed requests. Goodput resists those shortcuts only if acceptance rules and the denominator are fixed.

Measure at the client for user experience and at internal stages for diagnosis. Do not subtract queueing from the headline latency simply because it occurs outside the model runtime.

## Know the token metrics

vLLM’s benchmark documentation distinguishes these measurements and cautions that metric names alone do not ensure comparability across tools. [Benchmark reference](/agentic-eng/sources/#vllm-bench)

| Metric | What it tells you | What it does not tell you |
| --- | --- | --- |
| Time to first token/output | Delay until the first streamed response reaches the client | Time until a usable answer is complete |
| Inter-token or inter-output latency | Gaps between streamed outputs | Whole-task latency or answer quality |
| Time per output token | A per-request generation-rate measure under the tool’s definition | Identical behavior to the distribution of all inter-output gaps |
| End-to-end latency | Total elapsed request time at the measurement boundary | Which internal stage caused the delay |
| Output-token throughput | Generated output per second | Accepted business outcomes per second |

Record streaming chunk behavior and formulas. A chunk can contain multiple tokens, so a gap between chunks is not necessarily a gap between individual tokens.

## Use a realistic workload shape

Construct a distribution of input length, output length, tool usage, and arrival rate. For event briefs, some requests may have a short agenda while others involve many sessions and unresolved records. A test using only short prompts may miss the workload that causes saturation.

A closed-loop test sends another request after a previous one finishes; it is useful for controlled concurrency. An open-loop test schedules arrivals independently of completion; it better exposes backlog growth when demand continues during slow responses. Label which you use.

Separate cold starts, warm operation, and cache-assisted operation. If cache hits make the benchmark faster, record the hit pattern and check whether that pattern resembles production. Do not compare a cold baseline to a warm candidate as if the runtime alone caused the difference.

## Worked example: capacity versus goodput

Consider hypothetical 60-second runs on the same task mix:

| Offered load | Completed | Accepted within deadline | Goodput |
| --- | ---: | ---: | ---: |
| Low | 120 | 114 | 1.90 accepted tasks/s |
| Medium | 240 | 220 | 3.67 accepted tasks/s |
| High | 300 | 170 | 2.83 accepted tasks/s |

The highest completed count does not produce the highest goodput. At high load, queue delay or other failures may cause more work to miss the requirement. Inspect queue time, running requests, cache pressure, and per-stage latency to find the cause. [Serving metrics](/agentic-eng/sources/#vllm-metrics)

For a stable system, average in-flight work is approximately arrival rate multiplied by average time in the system. Use that relationship as a consistency check, not a p95 estimator or a model of a continuously growing queue. If arrivals exceed sustainable completions, the steady-state assumption no longer describes the run.

## Report distributions and failures

Show p50 and p95 end-to-end latency with sample size and test duration. Do not make confident tail claims from a tiny sample. Report rejected, timed-out, cancelled, and malformed requests separately, and explain whether they are included in each metric.

Keep the offered rate, achieved completion rate, and acceptance rate distinct. Include the client machine and network boundary when comparing different environments. A local benchmark and a remote benchmark may measure different transport costs.

Pin runtime, model, tokenizer, quantization, prompt template, limits, hardware, and parallelism configuration. Without those details, a result is difficult to reproduce or compare after an upgrade.

## Lab: find the saturation knee

1. Select a bounded sample of short, typical, and long event requests.
2. Run a low-load baseline and check that outputs still meet the quality gate.
3. Increase offered load in steps, holding the task mix constant.
4. At each step record end-to-end latency, queue delay, completions, failures, and goodput.
5. Repeat near the point where queue delay or missed deadlines grows sharply.
6. Add a burst test and one controlled dependency failure.
7. Publish the largest tested operating region that met all requirements, plus its headroom assumptions.

Your report should include raw results and the exact command/configuration. The output is an operating envelope, not a universal claim about a GPU or model.

## Failure drills

Throttle the model dependency. Mix long and short requests. Force cold starts. Make the load generator itself CPU-bound and verify that you notice. Stop new arrivals and observe how long the queue drains. Confirm that spending and error stop conditions actually end the test.

## Ship gate

The capacity claim includes workload distribution, sample size, measurement boundaries, failures, quality, and configuration. You know the saturation point and how admission control protects users before reaching it. Next, audit what these requests leave behind in [data retention](/agentic-eng/chapters/data-retention/).
