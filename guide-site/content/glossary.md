## Foundations and reliability

- **Accepted outcome:** A completed task that meets defined quality, permission, and operating requirements.
- **Baseline:** The reference system used to judge whether a change helps.
- **Trial:** One attempt at a test task; repeated trials expose variability.
- **Regression:** A change that breaks previously supported behavior.
- **Invariant:** A property the system must preserve, such as one accepted result per logical operation.
- **Idempotency:** A contract under which repeating the same logical request does not duplicate its intended effect.
- **Operation key:** A caller-supplied identifier for a logical request, scoped appropriately to avoid collisions across users or tenants.
- **Lease:** A temporary claim on work that can expire and permit recovery.
- **Fencing token:** A claim identifier checked at finalization so an obsolete worker cannot write as the current owner.
- **Transactional outbox:** Business state and an event record committed together, with a separate relay for external publication.
- **Backpressure:** Slowing or rejecting admission to keep downstream overload bounded.
- **Dead-letter queue:** A holding area for work that requires review after failing the normal processing policy.
- **Tenant:** A customer or organizational boundary within a shared service.
- **Source version:** An identifier for the specific record state used to produce a result.

## Models and agents

- **Workflow:** A predefined sequence or graph of execution steps.
- **Agent:** A system in which a model dynamically chooses some next steps or tool uses within a harness.
- **Harness:** Software that supplies context, exposes tools, enforces limits, and executes model proposals.
- **Tool contract:** A defined capability with arguments, outputs, permissions, and failure behavior.
- **Prompt injection:** An attempt to make untrusted content act as instructions or authority for the system.
- **Gateway:** A controlled entry point that mediates model access and selected operational policies.
- **Fallback:** A subsequent attempt through an alternative eligible endpoint or configuration.
- **Structured output:** A response constrained to a schema; structural validity does not establish factual correctness.
- **Trace:** A record of execution steps and observations, subject to appropriate data-retention controls.
- **Grader:** Code, a model-assisted rubric, or human procedure that evaluates an aspect of a trial or outcome.
- **Holdout:** Cases reserved for validation rather than repeated development tuning.

## Runtime and performance

- **Inference:** Executing a trained model to produce outputs.
- **Prefill:** Processing input context in a typical autoregressive model-serving flow.
- **Decode:** Generating subsequent output tokens in that flow.
- **KV cache:** Stored attention keys and values reused during generation; its size depends on the architecture and workload.
- **Quantization:** Representing numeric values with a different, often lower-precision format.
- **Tensor parallelism:** Dividing work within model operations across devices.
- **Pipeline parallelism:** Dividing model stages or layers across devices.
- **Data parallelism:** Replicating model-serving capacity for separate requests or batches.
- **Time to first token:** Client-observed delay until the first streamed output, using the benchmark’s exact definition.
- **p95 latency:** The latency at or below which 95% of observations fall in the measured sample.
- **Throughput:** Completed work per unit time, with the unit explicitly defined.
- **Goodput:** In this guide, accepted outcomes meeting required constraints per unit time.
- **Arithmetic intensity:** Operations per byte moved at the memory boundary being analyzed.
- **Kernel fusion:** Combining operations to reduce intermediate work or data movement, with implementation-dependent tradeoffs.

## Meaning, privacy, and cost

- **Ontology:** A formalized domain vocabulary with defined concepts and relationships.
- **Canonical identity:** The stable identifier that distinguishes an entity from its labels or aliases.
- **Provenance:** Where a claim or result came from and how it was produced.
- **RAG:** Retrieval-augmented generation: using retrieved information as context for generation.
- **Open-world reasoning:** Missing information is not automatically treated as false.
- **SHACL:** A W3C language for validating RDF data graphs against shapes.
- **Authorization:** An enforced decision about whether an authenticated principal may perform an operation.
- **ZDR:** A scoped zero-data-retention arrangement; exact coverage depends on the service, feature, and agreement.
- **Data minimization:** Limiting collection, processing, and retention to what the purpose requires.
- **Marginal cost:** The additional cost associated with more work under a defined operating model.
- **Fully loaded cost:** Cost including the chosen allocation of shared infrastructure, labor, and operations.
- **Cost per accepted outcome:** Total attributable cost of attempted work divided by accepted outcomes.
- **Cost of cognition:** In this guide, a lens for examining useful AI work and its total operating cost—not a standardized measurement unit.

Definitions are contextual to this guide. Consult the [primary references](/agentic-eng/sources/) for formal specifications and provider-specific contracts.
