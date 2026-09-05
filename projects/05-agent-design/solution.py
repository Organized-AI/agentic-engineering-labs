from dataclasses import dataclass

@dataclass(frozen=True)
class Proposal:
    kind: str
    tool: str | None = None
    args: dict | None = None
    answer: str | None = None

def run_agent(model, tools: dict, principal: str, max_steps=4) -> dict:
    trace=[]; seen=set()
    for _ in range(max_steps):
        proposal=model.propose(tuple(trace))
        if proposal.kind == "final":
            return {"status":"complete","answer":proposal.answer,"trace":trace}
        if proposal.kind == "question":
            return {"status":"needs_input","answer":proposal.answer,"trace":trace}
        if proposal.kind != "tool" or proposal.tool not in tools or not isinstance(proposal.args, dict):
            return {"status":"blocked","reason":"invalid proposal","trace":trace}
        signature=(proposal.tool, tuple(sorted(proposal.args.items())))
        if signature in seen:
            return {"status":"blocked","reason":"repeated call","trace":trace}
        seen.add(signature)
        tool=tools[proposal.tool]
        if not tool.authorized(principal, proposal.args):
            return {"status":"blocked","reason":"not authorized","trace":trace}
        observation=tool.call(proposal.args)
        trace.append({"tool":proposal.tool,"args":proposal.args,"observation":observation})
    return {"status":"blocked","reason":"step limit","trace":trace}

class EventTool:
    def __init__(self, records): self.records=records
    def authorized(self, principal, args):
        row=self.records.get(args.get("event_id")); return bool(row and row["tenant"] == principal)
    def call(self, args):
        row=self.records[args["event_id"]]
        return {"venue":row["venue"],"source_id":args["event_id"]}

class ScriptedModel:
    def __init__(self, proposals): self.proposals=iter(proposals)
    def propose(self, trace): return next(self.proposals)

if __name__ == "__main__":
    tools={"read_event":EventTool({"a":{"tenant":"org-a","venue":"Hall A"}})}
    model=ScriptedModel([Proposal("tool","read_event",{"event_id":"a"}),Proposal("final",answer="Hall A")])
    print(run_agent(model,tools,"org-a"))
