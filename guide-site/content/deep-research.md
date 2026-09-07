
*Companion to “Agentic Engineering - The Field Guide” · Research date: September 6, 2026*

This report takes each of the guide’s 12 chapters and maps the next layer down: the canonical papers, production playbooks, and current (2026) state of the art that a 5-minute chapter cannot carry. It then maps the connected topics the guide does not cover yet, with a suggested set of new chapters. Every claim that matters is tied to a source URL at the end of its section.

How to read it: each chapter section starts with what the guide already teaches, then “Go deeper” (the concepts to learn next), “Frontier” (what changed or is changing in 2026), and “Sources.” The gap analysis at the end is the answer to “what did I miss.”

---

## 01 · Experimentation

[Read chapter 01 →](/agentic-eng/chapters/experimentation/)

**Guide baseline:** hypotheses, paired comparisons, confounders, decision logs.
**Go deeper:**

* **Non-deterministic treatments break classical A/B assumptions.** Even at temperature 0, serving-side batching makes LLM outputs vary run to run; accuracy swings up to 15% on repeated identical calls have been measured, and providers ship silent model updates mid-experiment. The fixes: pin model snapshots where possible, log the model version on every call so a mid-window update becomes a difference-in-differences problem instead of a dead experiment, and average 3-5 runs per prompt in offline calibration.
* **CUPED variance reduction is close to mandatory for LLM features.** LLM output variance stacks on user-behavior variance, inflating minimum detectable effect. CUPED (subtract the pre-experiment-predictable component) routinely cuts variance 20-40%. Requirements: at least two weeks of pre-experiment data and strong pre/post correlation; fallback is cohort stratification.
* **Always-valid (anytime-valid) inference replaces peeking.** Standard p-values are invalid if you monitor and stop early; sequential statistics let you stop on strong evidence without inflating false positives. This is the default method on mature experimentation platforms and matters more when each experiment day has a real inference bill.
* **Interleaving for ranking/retrieval features.** Present both rankers’ results to the same user and let clicks decide. Airbnb documented ~50x speedup over A/B with 82% directional alignment. It ranks relative preference only; follow with A/B for absolute impact.
* **Switchback designs for shared-capacity systems.** When treatment users consume shared premium-model capacity, user-level randomization contaminates the control group (SUTVA violation). Randomize time slots instead of users, then handle carryover (warm caches, in-flight sessions), demand stationarity, and autocorrelated errors (HAC standard errors, bootstrap CIs).
* **Novelty effects are strong for AI features.** Segment by days-since-first-exposure; a lift concentrated in days 1-3 that decays is novelty, not improvement. Plan 3-4 week windows.

**Frontier (2026):** the tooling conversation has shifted from “how to A/B test an LLM feature” to designing experiments where the treatment itself mutates (model updates, prompt iterations) and the unit of randomization is often time or cluster, not user.
**Sources:**

- [https://tianpan.co/blog/2026/04/19/ab-testing-llm-features-non-deterministic](https://tianpan.co/blog/2026/04/19/ab-testing-llm-features-non-deterministic)
- [https://www.freecodecamp.org/news/switchback-experiments-for-ai-platform-features-in-python/](https://www.freecodecamp.org/news/switchback-experiments-for-ai-platform-features-in-python/)
- [https://arxiv.org/html/2606.18750v1](https://arxiv.org/html/2606.18750v1) — “Ensuring Trustworthy Online A/B Testing: Addressing Five Key Questions on CUPED”
- [https://assets.amazon.science/c1/4d/7945330e47539fdd870cb5c73613/interleaved-online-testing-in-large-scale-systems.pdf](https://assets.amazon.science/c1/4d/7945330e47539fdd870cb5c73613/interleaved-online-testing-in-large-scale-systems.pdf) — Amazon, interleaved online testing
- [https://pubsonline.informs.org/doi/abs/10.1287/mnsc.2022.4583](https://pubsonline.informs.org/doi/abs/10.1287/mnsc.2022.4583) — “Design and Analysis of Switchback Experiments,” Management Science
- [https://jamwithai.substack.com/p/the-production-aiml-engineers-guide](https://jamwithai.substack.com/p/the-production-aiml-engineers-guide)

---

## 02 · Engineering foundations

[Read chapter 02 →](/agentic-eng/chapters/engineering-foundations/)

**Guide baseline:** contracts, tenant isolation, transactions, deadlines, observability, deployable boundaries.
**Go deeper:**

* **Cell-based architecture is the production answer to tenant isolation at scale.** Partition the workload by a tenant-aligned key into independent cells behind a thin routing layer; a failure or bad deploy in one cell leaves the others untouched. AWS’s Well-Architected guidance covers the router/control-plane split and poison-pill containment; GitLab’s public Cells design docs are a real-world walkthrough of retrofitting cells onto a monolith.
* **Sagas replace distributed transactions.** Once each service owns its database, 2PC is off the table; a saga is a sequence of local transactions with compensating transactions for rollback. Know both coordinations: choreography (events trigger the next step; simple, decoupled, hard to trace) and orchestration (a coordinator drives participants; explicit, testable, a new component to operate). microservices.io (Chris Richardson) is the canonical pattern reference; Microsoft’s Azure Architecture Center has a solid pattern page too.
* **Contract testing (consumer-driven contracts)** is the natural extension of the guide’s “contracts before prompts”: Pact-style tests catch breaking API changes before deploy, which is exactly the failure mode an agent tool contract has.
* **Shuffle sharding** is the complement to cells for noisy-neighbor isolation without full partition count.

**Frontier (2026):** “deployable boundaries” increasingly means blast-radius engineering - cells, shuffle sharding, and per-tenant throttles - rather than just clean module APIs.
**Sources:**

- [https://docs.aws.amazon.com/wellarchitected/latest/reducing-scope-of-impact-with-cell-based-architecture/what-is-a-cell-based-architecture.html](https://docs.aws.amazon.com/wellarchitected/latest/reducing-scope-of-impact-with-cell-based-architecture/what-is-a-cell-based-architecture.html)
- [https://handbook.gitlab.com/handbook/engineering/architecture/design-documents/cells/iterations/cells-1.0/](https://handbook.gitlab.com/handbook/engineering/architecture/design-documents/cells/iterations/cells-1.0/)
- [https://microservices.io/patterns/data/saga.html](https://microservices.io/patterns/data/saga.html)
- [https://learn.microsoft.com/en-us/azure/architecture/patterns/saga](https://learn.microsoft.com/en-us/azure/architecture/patterns/saga)

---

## 03 · Jobs & events

[Read chapter 03 →](/agentic-eng/chapters/jobs-and-events/)

**Guide baseline:** at-least-once delivery, idempotency, leases, outboxes, backpressure, recovery.
**Go deeper:**

* **“Exactly-once” in Kafka is three mechanisms wearing one name.** The idempotent producer kills retry-duplicates within one producer session per partition (PID + epoch + sequence numbers; on by default in modern Kafka). Transactions kill reprocessing-duplicates by making writes plus the offset commit atomic and fencing zombie producers via transactional.id. Read-committed isolation makes the first two visible to consumers. They fail differently and are configured differently; most “we have exactly-once but see duplicates” bugs come from relying on the wrong one.
* **Durable execution (Temporal, Restate, DBOS) subsumes most hand-rolled job machinery.** Temporal’s model: the server persists an event history per workflow; workers poll task queues and replay history to reconstruct state after any crash. Leases, retries, timers, and exactly-once-effect semantics come from the framework instead of your code. For agent systems, this is the natural home for multi-step tool workflows - the guide’s leased job runner is what you build when you can’t adopt one.
* **The outbox/inbox pair generalizes to “transactional state transitions with side effects”** - the dual-write problem appears any time a database commit and an external effect (queue publish, API call, email send) must be atomic.

**Frontier (2026):** agent frameworks are converging with durable execution engines; expect “agent workflow \= durable workflow with LLM activities” to become the default production shape.
**Sources:**

- [https://petascalelabs.com/blog/kafka-exactly-once-idempotence-transactions-read-committed](https://petascalelabs.com/blog/kafka-exactly-once-idempotence-transactions-read-committed)
- [https://docs.temporal.io/encyclopedia/architecture/how-temporal-works](https://docs.temporal.io/encyclopedia/architecture/how-temporal-works)
- [https://docs.temporal.io/workflows](https://docs.temporal.io/workflows)
- [https://cwiki.apache.org/confluence/display/KAFKA/KIP-447:+Producer+scalability+for+exactly+once+semantics](https://cwiki.apache.org/confluence/display/KAFKA/KIP-447:+Producer+scalability+for+exactly+once+semantics)

---

## 04 · LLM gateways

[Read chapter 04 →](/agentic-eng/chapters/llm-gateways/)

**Guide baseline:** policy-first routing, fallback eligibility, spend reservations, caching, failure containment.
**Go deeper:**

* **What a gateway actually centralizes:** one API shape across providers, per-request routing by cost/latency/availability, retry and fallback chains, key management, rate limits per team/customer, cost attribution, caching, guardrails (PII redaction, output scanning), and audit logging. The 2026 consensus: building this yourself is usually a mistake; the build-vs-buy line has moved.
* **The current option set and their shapes:** LiteLLM (open-source Python proxy, 100+ providers, virtual keys with budgets, self-hosted; you own operations), Portkey (hosted control plane with semantic caching, guardrails, and observability), Kong AI Gateway (extends an existing API-gateway estate with LLM plugins, good when you already run Kong), Cloudflare AI Gateway (edge-native, cheap caching/analytics layer), OpenRouter (managed multi-provider routing and fallback as a service - you trade data-path control for zero ops).
* **Semantic caching** is the step beyond exact-match caching: embed the request, serve a cached answer when similarity crosses a threshold. Big cost lever for repeated-question workloads, but needs staleness and wrong-hit policies.
* **Fallback without policy drift** (the guide’s phrase) maps to a real design decision: fallback chains must respect per-use-case constraints (data residency, ZDR eligibility, capability floor), so the gateway config is a policy document, not just a list of models.
* **Spend reservations need concurrency semantics** because token usage is only known after the response; production gateways implement per-key budgets with in-flight estimate-and-settle accounting.

**Frontier (2026):** gateways are absorbing adjacent functions - guardrails, eval hooks, and FinOps attribution - and the comparison axis has shifted from “does it route” to “does it give you policy, audit, and cost control in one place.”
**Sources:**

- [https://turion.ai/blog/llm-gateway-patterns-litellm-portkey-kong/](https://turion.ai/blog/llm-gateway-patterns-litellm-portkey-kong/)
- [https://apiscout.dev/guides/openrouter-vs-litellm-vs-portkey-llm-fallbacks-2026](https://apiscout.dev/guides/openrouter-vs-litellm-vs-portkey-llm-fallbacks-2026)
- [https://developer.konghq.com/cookbooks/llm-cost-optimization/](https://developer.konghq.com/cookbooks/llm-cost-optimization/)
- [https://portkey.ai/docs/product/ai-gateway](https://portkey.ai/docs/product/ai-gateway)

---

## 05 · Agent design

[Read chapter 05 →](/agentic-eng/chapters/agent-design/)

**Guide baseline:** harnesses, tool contracts, bounded loops, memory, prompt injection, approval-bound actions.
**Go deeper:**

* **Context engineering is the discipline above prompt engineering.** Anthropic’s framing: curate the optimal set of tokens at every inference call - system prompt, tool definitions, retrieved docs, memory, history - because attention is a finite budget and “context rot” (recall degrading as the window fills) shows up in every model. The practical craft: smallest high-signal token set, system prompts at the right “altitude” (neither brittle if-else logic nor vague vibes), compaction and note-taking strategies for long horizons.
* **Prompt-injection defense has a real design-pattern literature now.** “Design Patterns for Securing LLM Agents against Prompt Injections” (Beurer-Kellner et al., 2025; IBM, Invariant Labs, ETH Zurich, Google, Microsoft) lays out six patterns: Action-Selector (no tool output flows back), Plan-Then-Execute (fix the plan before seeing untrusted content), LLM Map-Reduce (untrusted content only touches per-item sub-agents), Dual LLM (privileged planner + quarantined reader with symbolic memory), Code-Then-Execute, and Context-Minimization. Shared principle: once an agent ingests untrusted input, that input must be unable to trigger consequential actions.
* **CaMeL (Google DeepMind)** extends this to system-level enforcement: separate control flow and data flow, with a policy engine checking capability-tagged data before effects. The 2026 follow-on work applies it to computer-use agents.
* **Harness engineering** (the loop, tools, context, and control around the model) is now a named specialty; the model is increasingly the interchangeable part.

**Frontier (2026):** the security consensus has hardened - no model-level defense makes a general-purpose agent safe against injection, so architectural constraint (patterns above, sandboxing, approvals) is the only credible mitigation.
**Sources:**

- [https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [https://sourcegraph.com/blog/context-engineering](https://sourcegraph.com/blog/context-engineering)
- [https://simonwillison.net/2025/Jun/13/prompt-injection-design-patterns/](https://simonwillison.net/2025/Jun/13/prompt-injection-design-patterns/)
- [https://arxiv.org/html/2506.08837v2](https://arxiv.org/html/2506.08837v2) — the design-patterns paper
- [https://arxiv.org/html/2601.09923v3](https://arxiv.org/html/2601.09923v3) — “CaMeLs Can Use Computers Too: System-level Security for Computer Use Agents”

---

## 06 · Evaluations

[Read chapter 06 →](/agentic-eng/chapters/evaluations/)

**Guide baseline:** task suites, outcome graders, human calibration, repeated trials, holdouts, release gates.
**Go deeper:**

* **Judge bias is measurable, directional, and correctable.** The per-bias map: position bias (run order swaps, keep only verdicts consistent both ways), verbosity bias (length-control; one public leaderboard’s human correlation went 0.94 to 0.98 after length correction), self-preference (mask authorship, use a cross-family jury), bandwagon and authority cues (strip popularity signals and citations from what the judge sees), format/style bias (the largest measured surface bias, above position bias for every judge), and sentiment bias. Report the corrected ranking with an interval, not a point score.
* **85% human agreement is not the bar that matters.** A judge that agrees with humans 85% on average can still misorder exactly the close pairs a release decision turns on. Audit the pairs your decision depends on.
* **Benchmarks measure orthogonal axes, not difficulty levels.** SWE-bench grades a verifiable artifact (execution-based, repo tests); GAIA grades chained tool use to one exact answer; tau-bench grades policy adherence across multi-turn conversations, and its pass^k metric (success across ALL k trials) is the one number that maps to production reliability. SOTA function-calling agents that look fine at pass^1 fall below 25% at pass^8 in retail. The guide’s “repeated trials” instinct is exactly right; pass^k is the formal version.
* **SWE-bench Verified is saturating and contaminated**; the field is moving to SWE-bench Pro (contamination-resistant, long-horizon) and tau2-bench (dual-control domains where the user also has tools).
* **Eval-driven release gates:** wire your own harness to run many trials per task and gate on the reliability number, not the capability number.

**Frontier (2026):** post-saturation benchmark design (contamination resistance, reliability metrics like pass^k, execution-based grading) is where evaluation research is concentrating.
**Sources:**

- [https://latenteval.ai/research/llm-as-a-judge-bias](https://latenteval.ai/research/llm-as-a-judge-bias)
- [https://dreaming.press/posts/swe-bench-vs-tau-bench-vs-gaia.html](https://dreaming.press/posts/swe-bench-vs-tau-bench-vs-gaia.html)
- [https://github.com/sierra-research/tau2-bench](https://github.com/sierra-research/tau2-bench)
- [https://arxiv.org/html/2604.23178](https://arxiv.org/html/2604.23178) — “Judging the Judges: A Systematic Evaluation of Bias Mitigation Strategies in LLM-as-a-Judge Pipelines”

---

## 07 · Inference infrastructure

[Read chapter 07 →](/agentic-eng/chapters/inference-infrastructure/)

**Guide baseline:** prefill/decode, weights and KV cache, batching, quantization, parallelism, hosting decisions.
**Go deeper:**

* **The KV cache is the highest-impact optimization target.** It is the largest GPU-memory consumer after weights and grows linearly with context length and batch size (batch x seq_len x layers x kv_heads x head_dim x 2 x bytes). The levers, cheapest first: FP8 KV cache (roughly doubles capacity on H100 with minimal accuracy loss), prefix caching (reuse shared prompt prefixes; ~2.7x throughput at 90% hit rate in measured serving benchmarks), PagedAttention (already in the guide’s sources), and architectural reductions (GQA, MLA) when you control the model.
* **Engine choice has no universal winner; it flips with operating point.** A June 2026 reproducible benchmark (Llama-3.1-8B, H100/L40S, open-sourced harness): TensorRT-LLM had the lowest TTFT at moderate load (235 ms vs vLLM 514 ms at concurrency 32); vLLM had the highest saturation throughput (5,333 tok/s on one H100) and lowest cost ($0.158/1M tokens at FP8); SGLang tracked vLLM within a few percent. Notably, the cheaper L40S costs about twice as much per token as the H100. Also: Hugging Face’s TGI went into maintenance mode in March 2026, so many teams are re-choosing now.
* **Speculative decoding** (small draft model proposes, target verifies) gives 2-3x inter-token-latency reduction at 60-80% acceptance, with the benefit concentrated at low utilization.
* **Disaggregated serving** - splitting prefill and decode onto separate pools - is the production answer to prefill/decode interference (see chapter 08’s tail-latency numbers).

**Frontier (2026):** FP4 on Blackwell, disaggregated prefill/decode, and cache-aware routing are the active frontier; engine benchmarks now publish reproducible harnesses, so treat any non-reproducible comparison as marketing.
**Sources:**

- [https://www.hyperstack.cloud/technical-resources/tutorials/how-to-optimise-the-kv-cache-a-guide-to-faster-cheaper-llm-inference](https://www.hyperstack.cloud/technical-resources/tutorials/how-to-optimise-the-kv-cache-a-guide-to-faster-cheaper-llm-inference)
- [https://runinfra.ai/news/vllm-vs-sglang-vs-tensorrt-llm-benchmark](https://runinfra.ai/news/vllm-vs-sglang-vs-tensorrt-llm-benchmark)
- [https://developer.nvidia.com/blog/optimizing-inference-for-long-context-and-large-batch-sizes-with-nvfp4-kv-cache/](https://developer.nvidia.com/blog/optimizing-inference-for-long-context-and-large-batch-sizes-with-nvfp4-kv-cache/)
- [https://inferenceengineering.tech/chapters/techniques/](https://inferenceengineering.tech/chapters/techniques/)

---

## 08 · Load testing

[Read chapter 08 →](/agentic-eng/chapters/load-testing/)

**Guide baseline:** arrival patterns, queueing, tail latency, goodput, reproducibility, capacity reports.
**Go deeper:**

* **LLM latency is structurally heavy-tailed, and the standard playbook makes it worse.** Output length is a random variable with max/median ratios of 2-4x; queueing delay scales with the SECOND moment of service time, so a few runaway generations inflate everyone’s wait. Batching past the compute-saturation knee trades P99 for throughput. Naive retries on slow-but-alive requests duplicate in-flight load onto a saturated system. LRU eviction can flush the KV cache of a long conversation right before it resumes. Eager prefill scheduling stalls ongoing decodes (measured: up to 28x inter-token-latency inflation from naive hybrid batching).
* **What actually fixes P99:** chunked prefill (interleave prompt chunks with decode steps; P99 ITL dropped 1.08s to 0.29s in one production measurement, now default in major frameworks), length-aware request routing (separate short/long requests; 25-69% P99 reduction, ~3x throughput; a lightweight classifier predicts output length at ~5% error), and speculative decoding at low utilization.
* **Goodput is the metric that makes capacity reports defensible.** NVIDIA GenAI-Perf defines it as completed requests per second that meet SLO constraints (e.g. TTFT < X, ITL < Y) - throughput that users would actually accept. Pair it with kubernetes-sigs/inference-perf for cluster-level testing.
* **Agentic workloads compound tails.** Five sequential LLM calls convolve each step’s tail; a 3x per-call ratio becomes 15x+ end to end. Load-test the workflow, not the single call.
* **Measurement bias is real:** a 2026 arXiv paper catalogs systemic biases in production LLM benchmarks - worth reading before publishing any capacity number.

**Sources:**

- [https://tianpan.co/blog/2026/05/07/llm-tail-latency-p99-heavy-tailed-distributions](https://tianpan.co/blog/2026/05/07/llm-tail-latency-p99-heavy-tailed-distributions)
- [https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/perf_analyzer/genai-perf/docs/goodput.html](https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/perf_analyzer/genai-perf/docs/goodput.html)
- [https://github.com/kubernetes-sigs/inference-perf/](https://github.com/kubernetes-sigs/inference-perf/)
- [https://arxiv.org/html/2605.24217v2](https://arxiv.org/html/2605.24217v2) — “Identifying and Mitigating Systemic Measurement Bias in Production LLM Inference Benchmarks”
- [https://arxiv.org/html/2407.05347v1](https://arxiv.org/html/2407.05347v1) — “A Queueing Theoretic Perspective on Low-Latency LLM Inference”

---

## 09 · Data retention

[Read chapter 09 →](/agentic-eng/chapters/data-retention/)

**Guide baseline:** ZDR scope, persistence inventories, ephemeral processing, deletion evidence, incident handling.
**Go deeper:**

* **“Zero data retention” is a contract path, not a settled legal term.** No statute defines it across providers; the governing text is services agreements, DPAs, help-center commitments, and BAAs. Key distinctions a lawyer (and your persistence inventory) should check: “no training” is not “no retention” (both OpenAI and Google promise the former; the second question - are prompts, outputs, classifier signals, and abuse-monitoring artifacts stored - is where providers diverge). Every ZDR promise is subordinate to law-enforcement, abuse-prevention, and safety carveouts. ZDR often functions as a gateway condition: Anthropic’s Claude Code via API is eligible only with ZDR enabled for qualified accounts; OpenAI’s healthcare addendum ties PHI to ZDR-eligible endpoints.
* **Confidential computing is the technical complement to contractual ZDR.** GPU TEEs (NVIDIA H100 confidential compute, and 2025-2026 research systems like OpenPcc and EnclaveX) encrypt data in use, so retention guarantees rest on hardware attestation rather than policy. Performance/cost overhead across CPU vs GPU TEEs is now measured and published.
* **The guide’s “telemetry without default content capture”** pairs with the emerging practice of canary records (already in the guide) plus signed deletion evidence - some providers now expose retention attestations in their trust centers.

**Frontier (2026):** cross-provider ZDR comparison matrices exist (OpenAgreements maintains one from primary contract text), and enforcement is shifting from policy documents to verifiable technical controls.
**Sources:**

- [https://openagreements.org/practice-guides/ai-vendors/zdr-cross-provider-comparison](https://openagreements.org/practice-guides/ai-vendors/zdr-cross-provider-comparison)
- [https://developers.openai.com/api/docs/guides/your-data](https://developers.openai.com/api/docs/guides/your-data)
- [https://arxiv.org/html/2606.11145v1](https://arxiv.org/html/2606.11145v1) — “OpenPcc: Open and Confidential LLM Serving on Commodity TEEs”
- [https://images.nvidia.com/aem-dam/en-zz/Solutions/data-center/HCC-Whitepaper-v1.0.pdf](https://images.nvidia.com/aem-dam/en-zz/Solutions/data-center/HCC-Whitepaper-v1.0.pdf) — NVIDIA Hopper confidential computing

---

## 10 · Kernels & performance

[Read chapter 10 →](/agentic-eng/chapters/kernels-and-performance/)

**Guide baseline:** profiling, arithmetic intensity, roofline reasoning, fusion, correctness, honest GPU timing.
**Go deeper:**

* **FlashAttention is the canonical case study, and it keeps evolving.** FA2 (better parallelism and work partitioning), FA3 (NeurIPS 2024: asynchrony, warp specialization, and FP8 on Hopper), and now FA4 (MLSys 2026: algorithm and kernel pipelining co-designed for asymmetric hardware scaling). Reading the FA sequence teaches the guide’s roofline chapter better than any textbook: each version is a case of measuring which bound (compute, bandwidth, occupancy) the hardware actually hits.
* **Blackwell FP4 is the current kernel-engineering frontier.** Hardware capability is only half the story: a January 2026 Hugging Face benchmark of three MoE backends on a B200 (GPT-OSS-20B, 32 experts, top-4) showed SGLang at 1262 TFLOPS and FlashInfer CuteDSL at 1225 TFLOPS at peak, with a tuned implementation reaching 3.54x over BF16 and 1.32x over vLLM through kernel fusion and expert-aware computation. Same hardware, same model, different kernels - the gap is the engineering.
* **Triton is the right first tool** (the guide’s vector-add lab is the correct starting point); the next rungs are FlashInfer’s CuteDSL and CUTLASS for production-grade fused kernels, and ThunderKittens for tile-based primitives.
* **Honest GPU timing details that bite:** CUDA event timing vs wall clock, warmup and clock-throttling effects, and never timing a single kernel launch in isolation.

**Frontier (2026):** FP4 (NVFP4) kernels, MoE expert-aware fusion, and DSL-based kernel authoring (CuteDSL) are where published results concentrate.
**Sources:**

- [https://huggingface.co/blog/apsys/blackwell-nvfp4-comparison](https://huggingface.co/blog/apsys/blackwell-nvfp4-comparison)
- [https://proceedings.mlsys.org/paper_files/paper/2026/file/ae8b0b5838ba510daff1198474e7b984-Paper-Conference.pdf](https://proceedings.mlsys.org/paper_files/paper/2026/file/ae8b0b5838ba510daff1198474e7b984-Paper-Conference.pdf) — FlashAttention-4
- [https://pytorch.org/blog/flashattention-3/](https://pytorch.org/blog/flashattention-3/)
- [https://github.com/NVIDIA/TensorRT-LLM/blob/main/docs/source/blogs/tech_blog/blog3_Optimizing_DeepSeek_R1_Throughput_on_NVIDIA_Blackwell_GPUs.md](https://github.com/NVIDIA/TensorRT-LLM/blob/main/docs/source/blogs/tech_blog/blog3_Optimizing_DeepSeek_R1_Throughput_on_NVIDIA_Blackwell_GPUs.md)

---

## 11 · Ontologies & semantics

[Read chapter 11 →](/agentic-eng/chapters/ontologies/)

**Guide baseline:** canonical entities, provenance, temporal facts, RAG vs graphs, formal semantics, policy.
**Go deeper:**

* **GraphRAG vs vector RAG is a question-shape decision, not an architecture decision.** Vector RAG answers local lookups (the answer lives in a few chunks). Microsoft GraphRAG was built for global, sensemaking questions (“what are the themes across all incident reports?”) where the answer is spread across the corpus. Classic GraphRAG pays its cost at index time - an LLM reads the whole corpus, roughly 1000x vector-RAG indexing cost. LightRAG drops community detection for a lighter graph; Microsoft’s own LazyGraphRAG defers LLM work to query time and answers global queries 700x+ cheaper at vector-RAG indexing cost. Most teams asking “should I use a graph?” actually need better chunking, a reranker, and metadata filters; reach for a graph when global questions provably exist in your query logs, or the domain is intrinsically relational (legal, supply chain, biomedical).
* **Entity resolution is its own discipline** (deduplication, blocking, similarity joins); it is where canonical identity projects actually succeed or fail. Graph-native approaches and tools like Zep’s Graphiti (temporal knowledge graph for agent memory) are the 2026 state of practice.
* **Formal semantics still matters where policy bites:** OWL 2 for ontology semantics, SHACL for validating instance data against shapes - the guide cites both; the next step is running SHACL validation as a pipeline gate on extracted facts before they reach the graph or the model.

**Frontier (2026):** the GraphRAG family has collapsed the cost objection; temporal knowledge graphs (facts valid from/to) are becoming the standard memory substrate for agents.
**Sources:**

- [https://dreaming.press/posts/2026-06-21-graphrag-vs-vector-rag.html](https://dreaming.press/posts/2026-06-21-graphrag-vs-vector-rag.html)
- [https://venturebeat.com/orchestration/stop-graphing-everything-when-graphrag-actually-beats-vector-rag](https://venturebeat.com/orchestration/stop-graphing-everything-when-graphrag-actually-beats-vector-rag)
- [https://github.com/getzep/graphiti](https://github.com/getzep/graphiti)
- [https://dl.acm.org/doi/fullHtml/10.1145/3533016](https://dl.acm.org/doi/fullHtml/10.1145/3533016) — unsupervised graph-based entity resolution

---

## 12 · Cost of cognition

[Read chapter 12 →](/agentic-eng/chapters/cost-of-cognition/)

**Guide baseline:** unit economics, retry costs, review time, break-even utilization, routing experiments, budgets.
**Go deeper:**

* **The inference-cost paradox is the 2026 headline.** Token unit prices fell ~99.7% over two years, yet average AI bills roughly tripled: cheaper tokens enabled larger agentic workflows (Jevons-style), and 60-80% of real cost now sits OUTSIDE the model invoice - orchestration overhead, retries and fallback loops, idle overprovisioned concurrency, retrieval and vector-store spend, observability and guardrails tax, and human operations. The guide’s “accepted-outcome cost ledger” is exactly the right unit; the data now backs it.
* **FinOps for AI is a named, maturing practice.** The FinOps Foundation has an AI working group (the guide cites it); practitioner frameworks converge on visibility (per-token, per-feature metering), allocation (map spend to teams/products/customers), and optimization (model routing, caching, right-sizing) in a crawl-walk-run maturity model.
* **Model routing is the biggest single lever:** published practitioner results show 40-70% cost reduction from routing policies that send easy requests to small models, with quality held by routing on evidence (the guide’s chapter-12 instinct) rather than reputation.
* **Cost-per-task, not cost-per-token,** is the comparison unit that survives contact with reality: reproducible cost-per-task comparisons across providers now exist and routinely reorder the “cheap model” ranking.

**Sources:**

- [https://www.navyaai.com/reports/ai-cost-report-token-prices-vs-ai-bill](https://www.navyaai.com/reports/ai-cost-report-token-prices-vs-ai-bill)
- [https://www.finout.io/blog/finops-for-ai-the-definitive-overview](https://www.finout.io/blog/finops-for-ai-the-definitive-overview)
- [https://finops.aivyuh.com/blog/model-routing-cost-savings/](https://finops.aivyuh.com/blog/model-routing-cost-savings/)
- [https://intuitionlabs.ai/articles/llm-api-pricing-cost-per-task-comparison](https://intuitionlabs.ai/articles/llm-api-pricing-cost-per-task-comparison)
- [https://www.institutepm.com/knowledge-hub/ai-inference-cost-paradox](https://www.institutepm.com/knowledge-hub/ai-inference-cost-paradox)

---

## Gap analysis: what the guide does not cover yet

The guide’s 12 chapters run experimentation -> engineering -> orchestration -> runtime -> meaning/economics. These are the adjacent topics that connect directly to chapters you already have, ranked by how naturally they extend the existing arc. Each is a candidate chapter 13+.

### 1. Agentic security beyond prompt injection (extends ch. 05)

The guide covers prompt injection as a trust-boundary problem. The full 2026 threat surface is bigger: OWASP now publishes a Top 10 for Agentic Applications (peer-reviewed, 100+ contributors), covering goal hijacking, tool misuse, memory poisoning, and multi-agent trust exploitation. MCP has its own security literature (server sandboxing, tool poisoning, rug pulls via tool-description updates). Sandboxing practice has standardized on microVMs, egress allowlists, and least-privilege credentials per tool. Sources: [https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) , [https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/](https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/) , [https://sandboxreview.com/posts/mcp-server-sandboxing-isolation-requirements](https://sandboxreview.com/posts/mcp-server-sandboxing-isolation-requirements) , [https://www.practical-devsecops.com/mcp-security-guide/](https://www.practical-devsecops.com/mcp-security-guide/)

### 2. Agent identity, authentication, and authorization (extends ch. 02, 05)

Who is the agent when it calls an API? This is a live standards effort: IETF drafts on agent authN/authZ, SPIFFE-based workload identity for agents (Google Cloud’s Agent Identity issues per-agent X.509-bound credentials that can’t be impersonated or shared like service accounts), and OAuth token-exchange patterns for user-delegated (on-behalf-of) authority. The key design distinction: agent’s own authority vs user-delegated authority vs machine-to-machine client credentials. Sources: [https://docs.cloud.google.com/iam/docs/agent-identity-overview](https://docs.cloud.google.com/iam/docs/agent-identity-overview) (fetched), [https://www.ietf.org/ietf-ftp/internet-drafts/draft-klrc-aiagent-auth-03.html](https://www.ietf.org/ietf-ftp/internet-drafts/draft-klrc-aiagent-auth-03.html) , [https://developer.pingidentity.com/blog/securing-agentic-workflows-with-token-exchange-and-workload-identity/](https://developer.pingidentity.com/blog/securing-agentic-workflows-with-token-exchange-and-workload-identity/) , [https://codebasing.com/posts/oauth-and-spiffe-for-ai-agent-identity](https://codebasing.com/posts/oauth-and-spiffe-for-ai-agent-identity)

### 3. Human-in-the-loop operations (extends ch. 05, 06)

The guide has “approval-bound actions” as a design principle; the operational version is a whole architecture: intent classifier and policy engine routing actions by risk, confidence-threshold escalation, durable approval queues with payload-locked storage, operator review surfaces showing reasoning traces, and immutable audit trails. There is a compliance clock too: the EU AI Act’s human-oversight obligations for high-risk systems took effect August 2, 2026, with penalties up to 7% of global turnover. Sources: [https://www.agentnative.dev/patterns/human-in-the-loop-approval-flow-pattern](https://www.agentnative.dev/patterns/human-in-the-loop-approval-flow-pattern) (fetched), [https://developers.cloudflare.com/agents/concepts/agentic-patterns/human-in-the-loop/](https://developers.cloudflare.com/agents/concepts/agentic-patterns/human-in-the-loop/) , [https://www.agentpatternscatalog.org/patterns/approval-queue/](https://www.agentpatternscatalog.org/patterns/approval-queue/)

### 4. Context engineering and memory systems (extends ch. 05)

The guide covers memory as “no hidden authority.” The positive discipline is context engineering (Anthropic’s and Sourcegraph’s guides, fetched for ch. 05) plus the research line on long-horizon memory: MemGPT-style paged memory, agentic memory management papers, and documented “context rot.” Also practical: compaction, note-taking, sub-agent context isolation. Sources: [https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) , [https://arxiv.org/pdf/2607.23809](https://arxiv.org/pdf/2607.23809) (Agentic Context Management), [https://aclanthology.org/2026.acl-long.981.pdf](https://aclanthology.org/2026.acl-long.981.pdf) (Agentic Memory)

### 5. Agent observability (extends ch. 02 observability, ch. 06 evals)

OpenTelemetry’s GenAI semantic conventions (in the guide’s sources) are the spec; the practice is agent tracing - spans per LLM call, tool call, and retrieval, with evals attached to traces in production. Langfuse (open source), LangSmith, and OTel-native pipelines are the standard stack; the eval-observability loop (online scores feeding offline suites) is the part most teams miss. Sources: [https://langfuse.com/docs/observability/overview](https://langfuse.com/docs/observability/overview) , [https://langfuse.com/blog/2024-10-opentelemetry-for-llm-observability](https://langfuse.com/blog/2024-10-opentelemetry-for-llm-observability) , [https://launchdarkly.com/docs/tutorials/otel-llm-practical-guide-with-langfuse](https://launchdarkly.com/docs/tutorials/otel-llm-practical-guide-with-langfuse)

### 6. Guardrails as infrastructure (extends ch. 04, 05)

Input/output rails, topic and jailbreak detection, PII redaction, and output validation are productized (NVIDIA NeMo Guardrails, Llama Guard family) and increasingly live at the gateway layer (ch. 04) rather than in app code. Worth a chapter on where guardrails should sit in the request path and what they cost in latency. Sources: [https://github.com/NVIDIA/NeMo-Guardrails](https://github.com/NVIDIA/NeMo-Guardrails) , [https://docs.nvidia.com/nemo/guardrails/latest/configure-rails/yaml-schema/guardrails-configuration/index.html](https://docs.nvidia.com/nemo/guardrails/latest/configure-rails/yaml-schema/guardrails-configuration/index.html)

### 7. Fine-tuning vs RAG vs prompting (extends ch. 11, 12)

The third adaptation axis the guide doesn’t address: when to put knowledge in weights vs in retrieval vs in context. 2026 decision frameworks converge on: prompt first, RAG for volatile/large/private corpora, fine-tune for behavior, format, and domain style - and long-context windows have moved the boundary again. Sources: [https://chiraghasija.cc/posts/fine-tuning-vs-prompting-vs-rag-decision-framework/](https://chiraghasija.cc/posts/fine-tuning-vs-prompting-vs-rag-decision-framework/) , [https://zalt.me/blog/2026/06/rag-vs-fine-tuning-vs-prompting](https://zalt.me/blog/2026/06/rag-vs-fine-tuning-vs-prompting)

### 8. AI governance and the EU AI Act (extends ch. 09)

Retention is one compliance surface; the EU AI Act adds GPAI model-provider obligations (Article 53: technical documentation, copyright policy, training-data summaries), systemic-risk tiers (Article 55), and deployer duties for high-risk systems. Even a US-only builder shipping to EU users needs the deployer-side map. Sources: [https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-53](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-53) (fetched), [https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai) , [https://confir.eu/eu-ai-act/gpai-compliance](https://confir.eu/eu-ai-act/gpai-compliance)

### 9. Multi-agent systems (extends ch. 05)

Orchestrator-worker patterns, agent-to-agent protocols (A2A, MCP as tool layer), and the failure modes unique to agent teams (error propagation, shared-context poisoning). Evidence base is still thin; flag as emerging. Sources: [https://www.anthropic.com/engineering/building-effective-agents](https://www.anthropic.com/engineering/building-effective-agents) (already in the guide’s sources; its orchestrator-workers section is the anchor)

### 10. Prompt/model versioning and regression management (extends ch. 01, 06)

Prompt registries, canary deployments of model upgrades, provider version pinning, and shadow traffic - the operational bridge between experimentation (ch. 01) and release gates (ch. 06). Covered implicitly across the guide; deserves its own lab.

---

## Suggested new chapters, in the guide’s own format

1. **Agentic security** - OWASP Agentic Top 10, MCP sandboxing, the six injection-defense patterns (natural home: Orchestration, after ch. 05)
2. **Agent identity & delegated authority** - SPIFFE, OAuth OBO, IETF drafts (Foundations)
3. **Human oversight operations** - approval queues, audit trails, AI Act deadlines (Orchestration)
4. **Context & memory systems** - context engineering, compaction, memory architectures (Orchestration)
5. **Agent observability** - OTel GenAI conventions, tracing, online-to-offline eval loops (Runtime)
6. **Guardrails in the request path** - rails placement, latency cost, gateway integration (Runtime)
7. **Adaptation economics** - prompt vs RAG vs fine-tune as a cost/quality decision (Meaning & economics)
8. **AI Act & governance for builders** - deployer duties, documentation artifacts (Meaning & economics)

---

## Caveats and unknowns

* The guide’s own content was read in full (downloaded Markdown, September 2026 edition). All chapter baselines above reference what it actually teaches.
* 25 sources were fetched and read; a further ~30 search results were used as leads and are cited as highlight-only where not fetched. Vendor-authored comparisons (Kong, Portkey, OpenRouter, Finout, Hyperstack) are labeled by their URLs; treat their competitive claims accordingly.
* Benchmark numbers (serving engines, kernel TFLOPS, cost figures) are scoped to the hardware, model, and date in each source; they reorder frequently.
* Some 2026-dated arXiv and blog sources are very recent; the gap-analysis items marked “emerging” (multi-agent, agent identity standards) have unstable ground.
* The NavyaAI cost report’s headline figures (99.7% token price decline, 3x bill growth, 72% spend outside inference) are from a gated vendor report; directional, not audited.

## Method

* 32 targeted web searches (2 per chapter + 8 gap-analysis), 25 pages fetched and read, full text of the guide analyzed.
* Source-type coverage: official docs (AWS, Temporal, NVIDIA, Google Cloud, EU), primary papers (arXiv, NeurIPS, MLSys, Management Science), engineering blogs with reproducible artifacts, vendor comparisons, security standards (OWASP, IETF drafts), legal/contract analysis (OpenAgreements).