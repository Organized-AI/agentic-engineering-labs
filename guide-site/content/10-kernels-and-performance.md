> **The question:** When is low-level optimization the right next move, and how do you prove that it helped?

The source post mentions writing kernels without identifying which kind. This chapter chooses GPU kernels as a learning path because they connect naturally to inference. It is not a description of Bryan’s implementation.

Kernel work is optional for most readers of this guide. Understanding how to judge an optimization is useful even if you never write one.

## Start with the whole-system profile

Measure the complete task and divide its time into stages: admission, queue, retrieval, network, prefill, decode, validation, and persistence. If the model computation is only a small part of the task, improving one kernel has a limited effect on the user’s experience.

Amdahl-style reasoning gives a useful bound for a fixed workload:

```text
overall speedup = 1 / ((1 - f) + f / s)

f = fraction of original runtime improved
s = speedup of that fraction
```

If a stage takes 20% of the time and becomes four times faster, the total speedup is `1 / (0.8 + 0.2/4) ≈ 1.18×`, not 4×. The calculation assumes the other work stays unchanged and ignores added overhead; use it to challenge expectations before investing engineering time.

## The mental model of a GPU kernel

A kernel is a function executed across many pieces of data on a GPU. Useful concerns include how work is divided, which memory is accessed, whether accesses are efficient, and whether neighboring computations can reuse data.

Triton’s vector-addition tutorial introduces a concrete example: each program instance handles a block of elements, loads inputs, adds them, and stores the result. A mask prevents out-of-bounds access when the input size is not a multiple of the block size. [Triton tutorial](/agentic-eng/sources/#triton)

Do not remove the mask merely because a benchmark happens to use convenient dimensions. Real workloads include awkward shapes, empty or tiny inputs, and sizes that cross block boundaries.

## Arithmetic intensity and the roofline idea

Arithmetic intensity is approximately operations performed per byte moved at the memory level being considered. A simple performance bound is:

```text
attainable operations/s ≤ min(
    peak compute operations/s,
    memory bandwidth bytes/s × arithmetic intensity operations/byte
)
```

This is a model, not a promise of achieved performance. NVIDIA’s matrix-multiplication guide explains how arithmetic intensity helps distinguish math-limited and memory-limited work. [NVIDIA reference](/agentic-eng/sources/#gpu-performance)

For illustrative float32 vector addition, reading two inputs and writing one output moves about 12 bytes per addition, ignoring cache effects and additional traffic. Increasing available arithmetic alone may not help much if data movement is the bottleneck.

Matrix multiplication can reuse values across many operations, so its behavior depends strongly on dimensions, data type, tiling, and implementation. Do not generalize one vector-add result to an entire language model.

## Fusion and its tradeoffs

Fusion combines work that would otherwise run as separate operations. It can avoid intermediate memory traffic and launch overhead, but may increase register pressure, reduce scheduling flexibility, or complicate correctness and maintenance.

Treat fusion as a candidate change: identify the intermediate traffic you expect to remove, predict the likely gain, then measure. Also compare against the current framework/compiler path, because an existing implementation may already perform useful fusion.

For inference, shape distributions matter. A kernel optimized for one batch size or sequence length can be worse elsewhere. Keep a representative set rather than selecting only the dimension where the custom implementation wins.

## Correctness before performance

Check outputs against a trusted reference for multiple sizes and data types. Floating-point operations can change rounding when their order changes, so define tolerances appropriate to the operation rather than assuming exact equality everywhere.

Test boundaries, noncontiguous layouts if supported, large and small magnitudes, and special values relevant to the contract. If the optimized operation changes precision, re-run model-level and task-level checks too. Numerical agreement at one isolated operation is not the same as unchanged end-to-end quality.

Use the framework’s supported benchmark tools, warm up compilation and allocation paths, and ensure the timing method accounts for asynchronous GPU execution. Triton’s tutorial demonstrates comparison with a native reference and benchmark utilities; use those patterns instead of timing a dispatch with a naïve wall-clock call.

## Lab: vector addition, then a decision memo

On supported hardware:

1. Reproduce the official Triton vector-addition tutorial in an isolated environment.
2. Add sizes just below and above a block boundary, not only powers of two.
3. Verify results before collecting timings.
4. Record warmup, data type, device, software versions, and benchmark method.
5. Compare with the current native implementation over the full shape set.
6. Write down where the custom kernel wins, ties, or loses.

Then profile a real application and estimate its maximum plausible end-to-end benefit before integrating anything. Without suitable hardware, complete the profiling and arithmetic-intensity analysis as a paper exercise; do not rent a large cluster to satisfy this chapter.

## Failure drills

Benchmark without warmup and compare the result. Omit synchronization in a deliberately incorrect timing harness and explain the misleading number. Test a nonmultiple input length. Change precision. Introduce a shape the optimized path does not support and confirm that the fallback remains correct.

## Ship gate

The optimized path passes correctness tests, improves a representative workload, and produces a measured end-to-end benefit worth its maintenance cost. The original implementation remains available as a reference or rollback. Next, optimize the information architecture rather than the arithmetic in [ontologies and semantics](/agentic-eng/chapters/ontologies/).
