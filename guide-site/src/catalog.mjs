export const base = '/agentic-eng';
export const origin = 'https://guide.organizedai.vip';
export const updated = 'September 5, 2026';
export const chapters = [
  { slug:'experimentation', file:'01-experimentation.md', title:'Experimentation', subtitle:'Turn curiosity into evidence.', group:'01 · Foundations', level:'Foundation', summary:'Hypotheses, paired comparisons, confounders, uncertainty, and a decision log that compounds.' },
  { slug:'engineering-foundations', file:'02-engineering-foundations.md', title:'Engineering foundations', subtitle:'Build the service around the model.', group:'01 · Foundations', level:'Foundation', summary:'Contracts, tenant isolation, transactions, deadlines, observability, and deployable boundaries.' },
  { slug:'jobs-and-events', file:'03-jobs-and-events.md', title:'Jobs & events', subtitle:'Make work survive failure.', group:'01 · Foundations', level:'Intermediate', summary:'At-least-once delivery, idempotency, leases, transactional outboxes, backpressure, and recovery.' },
  { slug:'llm-gateways', file:'04-llm-gateways.md', title:'LLM gateways', subtitle:'Make model access governable.', group:'02 · Orchestration', level:'Intermediate', summary:'Policy-first routing, fallback eligibility, spend reservations, caching, and failure containment.' },
  { slug:'agent-design', file:'05-agent-design.md', title:'Agent design', subtitle:'Autonomy with explicit boundaries.', group:'02 · Orchestration', level:'Intermediate', summary:'Harnesses, tool contracts, bounded loops, memory, prompt injection, and approval-bound actions.' },
  { slug:'evaluations', file:'06-evaluations.md', title:'Evaluations', subtitle:'Grade outcomes, not confidence.', group:'02 · Orchestration', level:'Intermediate', summary:'Task suites, outcome graders, human calibration, repeated trials, holdouts, and release gates.' },
  { slug:'inference-infrastructure', file:'07-inference-infrastructure.md', title:'Inference infrastructure', subtitle:'Understand the machine underneath.', group:'03 · Runtime', level:'Advanced', summary:'Prefill and decode, weights and KV cache, batching, quantization, parallelism, and hosting decisions.' },
  { slug:'load-testing', file:'08-load-testing.md', title:'Load testing', subtitle:'Find the useful capacity limit.', group:'03 · Runtime', level:'Advanced', summary:'Arrival patterns, queueing, tail latency, goodput, reproducibility, and defensible capacity reports.' },
  { slug:'data-retention', file:'09-data-retention.md', title:'Data retention', subtitle:'Privacy across the entire path.', group:'03 · Runtime', level:'Intermediate', summary:'ZDR scope, persistence inventories, ephemeral processing, deletion evidence, and incident handling.' },
  { slug:'kernels-and-performance', file:'10-kernels-and-performance.md', title:'Kernels & performance', subtitle:'Optimize the proven bottleneck.', group:'03 · Runtime', level:'Advanced', summary:'Profiling, arithmetic intensity, roofline reasoning, fusion, correctness, and honest GPU timing.' },
  { slug:'ontologies', file:'11-ontologies.md', title:'Ontologies & semantics', subtitle:'Give the system a business model.', group:'04 · Meaning & economics', level:'Intermediate', summary:'Canonical entities, provenance, temporal facts, RAG versus graphs, formal semantics, and policy.' },
  { slug:'cost-of-cognition', file:'12-cost-of-cognition.md', title:'Cost of cognition', subtitle:'Optimize for accepted outcomes.', group:'04 · Meaning & economics', level:'Intermediate', summary:'Unit economics, retry costs, review time, break-even utilization, routing experiments, and budgets.' }
].map((c,i)=>({...c,number:String(i+1).padStart(2,'0'),href:`${base}/chapters/${c.slug}/`}));

export const sources = [
  ['post','The source post','Shep Bryan · LinkedIn','https://www.linkedin.com/posts/shepbryan_when-i-started-penumbra-last-year-i-still-activity-7482858594674163712-cq6F/','Topic selection and the author’s self-reported experience; not independent deployment evidence.'],
  ['agents','Building effective agents','Anthropic','https://www.anthropic.com/engineering/building-effective-agents','Workflow/agent distinction, simple composable patterns, and tool design.'],
  ['evals','Demystifying evals for AI agents','Anthropic','https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents','Trials, task outcomes, graders, regression suites, and evaluation design.'],
  ['sqs','Amazon SQS standard queues','AWS','https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/standard-queues.html','At-least-once delivery and potential reordering.'],
  ['idempotency','Making retries safe with idempotent APIs','AWS Builders’ Library','https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/','Caller-supplied request identifiers and retry semantics.'],
  ['outbox','Transactional outbox pattern','AWS Prescriptive Guidance','https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html','Database/message dual writes, outbox relays, and duplicate handling.'],
  ['postgres','Transaction isolation','PostgreSQL','https://www.postgresql.org/docs/current/transaction-iso.html','Isolation levels, concurrent transactions, and serialization retries.'],
  ['rls','Row security policies','PostgreSQL','https://www.postgresql.org/docs/current/ddl-rowsecurity.html','Row-level security behavior and privileged-role caveats.'],
  ['litellm','Getting started','LiteLLM','https://docs.litellm.ai/docs/','Gateway capabilities, routing, virtual keys, usage, and budgets.'],
  ['routing','Routing, load balancing, and fallbacks','LiteLLM','https://docs.litellm.ai/docs/routing','Routing and retry/fallback configuration; verify against your installed version.'],
  ['injection','LLM prompt injection prevention','OWASP','https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html','Untrusted content, least privilege, validation, and human oversight.'],
  ['otel','Generative AI semantic conventions','OpenTelemetry','https://github.com/open-telemetry/semantic-conventions-genai','Current home of the GenAI conventions; maturity and content capture need review.'],
  ['vllm-metrics','Production metrics','vLLM','https://docs.vllm.ai/en/stable/usage/metrics/','Queue, prefill, decode, cache, and request latency metrics.'],
  ['vllm-bench','Benchmark CLI','vLLM','https://docs.vllm.ai/en/stable/benchmarking/cli/','Latency definitions, request workloads, and benchmark reporting.'],
  ['vllm-parallel','Parallelism and scaling','vLLM','https://docs.vllm.ai/en/stable/serving/parallelism_scaling/','Single- and multi-GPU serving choices and distributed deployment.'],
  ['paged-attention','Efficient memory management for large language model serving with PagedAttention','Kwon et al. · SOSP 2023','https://arxiv.org/abs/2309.06180','KV-cache memory management and the serving motivation behind vLLM.'],
  ['retention','API and data retention','Anthropic','https://platform.claude.com/docs/en/manage-claude/api-and-data-retention','Provider-specific ZDR scope, feature eligibility, and retention distinctions.'],
  ['triton','Vector addition tutorial','Triton','https://triton-lang.org/main/getting-started/tutorials/01-vector-add.html','Kernel programming, boundary masks, validation, and benchmarking.'],
  ['gpu-performance','Matrix multiplication background','NVIDIA','https://docs.nvidia.com/deeplearning/performance/dl-performance-matrix-multiplication/index.html','Arithmetic intensity and math-bound versus memory-bound reasoning.'],
  ['owl','OWL 2 document overview','W3C','https://www.w3.org/TR/owl2-overview/','Formalized vocabularies, relationships, and ontology semantics.'],
  ['shacl','Shapes Constraint Language','W3C','https://www.w3.org/TR/shacl/','Validating RDF data graphs against explicit shapes.'],
  ['finops','FinOps for AI Overview','FinOps Foundation','https://www.finops.org/wg/finops-for-ai-overview/','AI cost management, allocation, and business-value considerations.']
].map(([id,title,organization,url,note])=>({id,title,organization,url,note}));
