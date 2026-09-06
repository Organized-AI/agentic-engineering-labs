> **The question:** What is actually happening when a model endpoint turns your input into an answer—and which part do you need to operate?

Inference is execution of a trained model. Hosting inference means operating the runtime that receives requests, loads weights, manages memory, schedules work, and returns outputs. It is distinct from training the model or owning the physical GPUs.

Start with the business requirement. Private deployment, predictable latency, sustained utilization, specialized models, or control over dependencies may justify operating more of the stack. None follows merely from calling your product “agentic.”

## The mental model

For a typical autoregressive text model, **prefill** processes the input context and **decode** generates subsequent tokens. A serving engine also handles admission, scheduling, batching, and memory management. vLLM exposes metrics for prefill, decode, queued requests, and cache usage, which helps separate these concerns in practice. [Metrics reference](/agentic-eng/sources/#vllm-metrics)

A slow answer can therefore mean a long queue, a large input, slow token generation, a tool call, or a cold model load. “Use a faster GPU” is only one possible response and may address the wrong stage.

## Budget memory before choosing hardware

Three useful categories are model weights, attention cache, and runtime overhead. A basic unquantized weight estimate is:

```text
weight bytes ≈ parameter count × bytes per stored parameter
```

An illustrative 8-billion-parameter model stored at two bytes per parameter requires about 16 billion bytes for weights alone: roughly 14.9 GiB. That is not the total serving-memory requirement. Activations, cache, temporary buffers, runtime allocations, and the particular implementation add more.

For a conventional full-attention model with grouped-query attention, an approximate uncompressed KV-cache calculation for one sequence is:

```text
KV bytes ≈ 2 × layers × KV heads × head dimension
             × cached tokens × bytes per cache element
```

Example: `2 × 32 × 8 × 128 × 8192 × 2 = 1,073,741,824 bytes`, or 1 GiB per sequence. Ten such sequences could therefore require roughly 10 GiB of this cache before sharing, paging overhead, or other allocations.

These are explanatory tensor-size calculations, not sizing guarantees. Sliding-window attention, hybrid/recurrent architectures, quantized caches, prefix sharing, and runtime layout can change the result. The [PagedAttention paper](/agentic-eng/sources/#paged-attention) explains why efficient cache management matters in serving.

## Batching, context, and quantization

Batching can improve throughput by using hardware across more requests, while changing the latency experienced by an individual request. Continuous scheduling can admit and retire sequences as their work changes. Measure the workload rather than assuming the largest batch is best.

Context length affects both work and memory. Instead of blindly increasing the allowed context, measure how much retrieved material is useful. Removing irrelevant context may be an application-level improvement before any runtime tuning.

Quantization changes the representation of weights or other tensors. A smaller representation may reduce memory requirements, but format support, conversion overhead, kernel availability, and task-quality changes still matter. Re-run the actual task suite; a model that fits is not necessarily a model that meets your acceptance criteria.

## Understand the parallelism decision

Data parallelism replicates serving capacity across instances. Tensor parallelism splits work within model operations. Pipeline parallelism splits model layers or stages. These solve different problems and introduce different coordination costs.

vLLM’s deployment guidance discusses single-GPU serving and combinations of tensor and pipeline parallelism when larger configurations are needed. Consult its current model and hardware support before selecting a layout. [Scaling reference](/agentic-eng/sources/#vllm-parallel)

For this guide’s project, begin with the simplest compatible deployment and increase complexity only after measuring a capacity or memory constraint. Multi-GPU networking and failure recovery are operational commitments, not just configuration values.

## Choose what to own

| Option | What you operate | Questions to answer |
| --- | --- | --- |
| Managed model API | Application, policy, evaluations, provider integration | Are feature, retention, quality, and capacity terms acceptable? |
| Managed dedicated endpoint | Application plus endpoint configuration/capacity choices | What is reserved, what scales, and who handles failures? |
| Self-operated serving | Runtime, model artifacts, capacity, monitoring, rollout, recovery | Can the team maintain availability and validate upgrades? |

For bursty requests, include idle periods and cold starts. For steady demand, include usable throughput at your latency target. In both cases, account for human operating effort and incident response, not merely GPU-hour cost.

## Lab: write an inference decision memo

You can begin without renting hardware.

1. Define task quality, privacy, maximum input size, expected burst size, and latency requirements.
2. Estimate weight and cache memory for one candidate architecture, recording every assumption.
3. Establish a managed or existing-endpoint baseline using approved, synthetic data.
4. If you already have suitable hardware, test a compatible small model locally. Otherwise, design the benchmark before requesting a bounded rental.
5. Compare task quality, cold/warm latency, failures, and total cost under the same workload.
6. State the evidence that would cause you to switch hosting approaches.

The output is a defensible choice, including “continue using a managed endpoint.” Never provision a large cluster as an unbounded exploratory step.

## Failure drills

Exhaust cache capacity with long concurrent requests. Restart a serving process. Remove a model artifact. Test an incompatible quantization configuration. Increase prompt length while holding output length constant. Identify which observable stage changes and what the user sees.

## Ship gate

You can account for weights, cache, scheduling, and operational ownership. Your chosen endpoint passes the task suite and has a bounded capacity plan. Next, establish that plan with [load testing](/agentic-eng/chapters/load-testing/).
