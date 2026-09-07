export const repo = 'https://github.com/Organized-AI/agentic-engineering-labs';

const rows = [
  ['experimentation','01-experimentation','Paired Experiment Ledger',3,'Compare two configurations on the same cases and expose regressions.',`report = compare([
    Trial("conflict", "A", False, False, .04),
    Trial("conflict", "B", True, False, .07),
])
print(report["only_b"], decision(report))`],
  ['engineering-foundations','02-engineering-foundations','Tenant-Safe Event Service',3,'Validate contracts, enforce tenant scope, and reject stale facts.',`snapshot = service.read("org-a", "event-a")
brief = service.make_brief(snapshot)
service.events["event-a"].version += 1
# Raises: source version changed
service.save("org-a", brief)`],
  ['jobs-and-events','03-jobs-and-events','Leased Job Runner',3,'Recover work safely with idempotency, leases, fencing, and an outbox.',`job = jobs.submit("operation-1", "build brief")
old = jobs.claim(job, now=0)
current = jobs.claim(job, now=11)
# The obsolete worker is fenced out.
jobs.complete(job, old, "stale", now=12)`],
  ['llm-gateways','04-llm-gateways','Policy-Aware Model Router',4,'Route only to eligible endpoints and reserve spending before a call.',`endpoints = [
    Endpoint("primary", {"internal"}, .04, "timeout"),
    Endpoint("fallback", {"internal"}, .06),
]
result = route("brief", "internal", endpoints, Budget(.10))`],
  ['agent-design','05-agent-design','Bounded Tool Agent',3,'Execute model proposals only through authorized tools and bounded loops.',`result = run_agent(
    ScriptedModel([Proposal("tool", "read_event", {"event_id":"a"})]),
    {"read_event": event_tool},
    principal="org-a",
    max_steps=4,
)`],
  ['evaluations','06-evaluations','Outcome Evaluation Harness',3,'Grade saved state and forbidden effects across repeated trials.',`report = evaluate(tasks, agent, trials=3)
if not release_gate(report, minimum_rate=.80):
    raise SystemExit("release blocked")
print(report["accepted"], len(report["attempts"]))`],
  ['inference-infrastructure','07-inference-infrastructure','Inference Memory Planner',3,'Estimate weights and KV cache before selecting a serving layout.',`weights = weight_bytes(8_000_000_000, 2)
cache = kv_cache_bytes(32, 8, 128, 8192, 2, sequences=4)
required = weights + cache
print(fits(24 * GIB, required, headroom=.15))`],
  ['load-testing','08-load-testing','Queueing Workload Simulator',3,'Measure queue delay, tail latency, and accepted goodput under load.',`requests = [Request(i * .1, service_time=1) for i in range(10)]
report = simulate(requests, workers=1, deadline=2)
print(report["p95"], report["goodput"])
print(report["accepted"], report["attempted"])`],
  ['data-retention','09-data-retention','Synthetic Canary Audit',3,'Find a synthetic marker across success, failure, and expiry paths.',`marker = "SYNTHETIC-CANARY-001"
error_log.write(now=0, value="timeout " + marker)
print(audit([error_log, job_store], marker))
error_log.expire(now=30)
print(audit([error_log, job_store], marker))`],
  ['kernels-and-performance','10-kernels-and-performance','Vector Kernel Checkpoint',3,'Test partial blocks and calculate whole-system speedup honestly.',`for size in (0, 1, 7, 8, 9, 17):
    x = list(range(size))
    assert vector_add(x, [2] * size, 8) == [v + 2 for v in x]
print(overall_speedup(.20, 4))  # about 1.18x`],
  ['ontologies','11-ontologies','Source-Backed Domain Graph',3,'Resolve current approved facts with provenance and separate authorization.',`venue = resolve_venue(
    "event-a", "org-a", event_tenants, facts, at_time=10
)
print(venue["label"])
print(venue["label_source"])`],
  ['cost-of-cognition','12-cost-of-cognition','Accepted-Outcome Cost Ledger',3,'Include failed attempts, review time, and utilization in unit economics.',`report = outcome_cost(attempts, reviewer_hourly_cost=60)
print(report["cost_per_accepted"])
print(break_even(
    fixed_cost=2000, managed_unit=.05, self_variable_unit=.01
))`],
  ['agentic-security','13-agentic-security','Injection Gauntlet',3,'Run adversarial prompts through the harness and count unauthorized actions.',`report = gauntlet.run(attacks, harness)
assert report["unauthorized_actions"] == 0
print(report["blocked"], report["total"])`],
  ['agent-identity','14-agent-identity','Identity-Aware Tool Gateway',3,'Verify subject, scope, and actor on every tool call.',`token = exchange(user_token, audience="calendar", scope="event:write")
effect = gateway.call("send_update", token, payload)
# Raises: token audience does not match the tool
gateway.call("billing_charge", token, payload)`],
  ['human-oversight','15-human-oversight','Approval Queue State Machine',3,'Route consequential actions through exact, single-use approvals.',`req = queue.submit(action="send_brief", context_hash=h)
decision = queue.decide(req.id, approve=True, by="organizer")
queue.execute(req.id, decision)
# Raises: approval already consumed
queue.execute(req.id, decision)`],
  ['context-and-memory','16-context-and-memory','Typed Memory Store',3,'Keep profile, episodic, semantic, and working memory separate and inspectable.',`store.write("episodic", note, source="meeting-42", verified=True)
ctx = assemble(task, store, budget=4000)
snapshot = compact(ctx, keep=[constraints, open_loops])`],
  ['evals-traces-logs','17-evals-traces-logs','Three-Signal Debugger',3,'Join logs, traces, and eval scores on one task id.',`trace = traces.for_task("task-7")
score = graders.run(trace)
log.event("eval.scored", task_id="task-7", score=score.value)
print(why("task-7"))  # log line -> span -> grader rationale`],
  ['guardrails','18-guardrails','Rail Pipeline',3,'Measure latency and failure mode of each rail in the request path.',`result = pipeline.run(call, rails=[injection_rail, scope_rail, topic_rail])
print(result.decision, result.latency_ms)
# Fail-closed: a rail error means deny, not skip.`],
  ['adaptation-economics','19-adaptation-economics','Adaptation Lever Pricer',3,'Price prompt, retrieval, and fine-tune options on cost per accepted outcome.',`options = [prompt_v2, rag_pack, fine_tune]
report = price(options, trials=30, ledger=cost_ledger)
print(report.winner, report.cost_per_accepted)`],
  ['ai-act-governance','20-ai-act-governance','Classification Memo Builder',3,'Classify the system, assign duties, and map obligations to artifacts.',`memo = classify(system_profile, annex_rules)
duties = assign(memo.role)  # provider vs deployer
index = map_artifacts(duties, repo="field-guide")`],
  ['tailnets','21-tailnets','Mesh Policy Checker',3,'Prove the mesh allows the intended path and denies everything else.',`policy = load_acls("tailnet-policy.json")
assert allows(policy, "tag:dev-macs", "tag:services", 11434)
assert not allows(policy, "tag:mobile", "tag:services", 22)`],
  ['engineering-best-practices','22-engineering-best-practices','Foundation Audit',3,'Score the seven classic blocks on evidence before widening agent scope.',`report = audit(repo, blocks=[vcs, tests, cicd, review, adrs, telemetry, secrets])
print(report.weakest, report.evidence[report.weakest])`],
  ['the-challenge','23-the-challenge','Sprint Ledger',3,'Track the 7/30/60/90-day artifacts against the dated opening bet.',`ledger = Ledger(bet="RAG beats fine-tuning at our scale", date="2026-09-06")
ledger.ship(day=7, artifact="one-page map")
print(ledger.grade(day=30))`],
  ['mcp-vs-cli','24-mcp-vs-cli','Tool Door Router',3,'Route each capability to MCP, CLI, or a hardened script on measured cost and validation.',`report = router.measure(calendar_capability, doors=["mcp", "cli"])
print(report.discovery_tokens, report.validation_catches)
# Repeated and exact? Leave the model out entirely.
router.harden("daily-brief", into="scripts/daily_brief.sh")`],
  ['agent-runtimes','25-agent-runtimes','Turn Loop Harness',3,'Run one turn with budget enforcement, a policy choke point, and checkpointing.',`ctx = runtime.assemble(message, budget=4096)
proposal = stub_model.complete(ctx, tools=runtime.schemas())
runtime.policy.check(proposal.calls[0])  # reject unknown recipients
runtime.checkpoint(ctx)`],
  ['supervision-lifecycle','26-supervision-lifecycle','Supervisor Tree',3,'Detect a wedged tool, restart with backoff, and trip a breaker the agent can read.',`sup = Supervisor(deadline_ms=500, max_restarts=3)
sup.watch(calendar_server, health=known_event_read)
# Server hangs: breaker opens, agent degrades honestly.
print(sup.state("calendar"))  # circuit open`],
  ['state-sessions-statelessness','27-state-sessions-statelessness','State Auditor',3,'Give every piece of state a home, an owner, a lifetime, and a recovery path.',`report = audit(component)  # context / session / stores
assert report.leaks == []     # home: None is a finding
kill_process(); resume_from_stores()  # turn completes`],
  ['scheduling-event-driven-agents','28-scheduling-event-driven-agents','Durable Scheduler',3,'Claim due jobs under lease, apply missed-fire policy, and heartbeat liveness.',`job = store.due(now).first()
if lease(job, ttl=job.deadline):
    job.run() if within(job.lateness_budget) else job.skip()
scheduler.heartbeat()`],
  ['isolation-failure-containment','29-isolation-failure-containment','Containment Matrix',3,'Prove tenant walls for compromised, confused, and costly agents.',`for resource in runtime.shared_resources():
    assert resource.accessible_by(agent_a) <= policy[tenant_a]
assert not store_b.readable_by(agent_a)`],
  ['other-half-of-the-model','30-other-half-of-the-model','Attribution Bench',3,'Diagnose planted harness faults from black-box signals alone.',`if prefill.flat and decode.moved: blame("serving stack")
if endpoint.ok and not agent_loop.ok: blame("harness")
# "model" is reached only by elimination.`],
  ['sandboxing','31-sandboxing','Five Walls Bench',3,'Attack the sandbox edge: filesystem, egress, credentials, resources, lifetime.',`sb = sandboxes.create(image="report-runner", owner=tenant)
sb.policy.egress.allow_only(["api.venue-db.internal"])
result = sb.exec(task.code, env={"VENUE_TOKEN": mint(scope="venue:read")})
sb.destroy()  # teardown is total`],
];

export const projects = rows.map(([slug,path,title,tests,outcome,code]) => ({
  slug,path,title,tests,outcome,code,
  url:`${repo}/tree/main/projects/${path}`,
  starter:`${repo}/blob/main/projects/${path}/starter.py`,
  solution:`${repo}/blob/main/projects/${path}/solution.py`,
  testFile:`${repo}/blob/main/projects/${path}/test_solution.py`,
  command:`cd projects/${path}\npython3 -m unittest -v test_solution.py\npython3 solution.py`,
}));

export const milestones = [
  ['read','Read & explain','I can explain the core invariant in my own words.'],
  ['tests','Run the tests','I ran the project checkpoint locally.'],
  ['challenge','Complete the challenge','I implemented or extended the starter.'],
  ['reflect','Write a reflection','I recorded what the tests prove—and what they do not.'],
].map(([id,label,description])=>({id,label,description}));
