"""Attribution Bench - reference solution."""
from dataclasses import dataclass


@dataclass
class Signals:
    prefill_tps_before: float
    prefill_tps_after: float
    decode_tps_before: float
    decode_tps_after: float
    endpoint_ok: bool
    agent_loop_ok: bool
    served_model_id: str
    expected_model_id: str

    @property
    def prefill_flat(self):
        return abs(self.prefill_tps_after - self.prefill_tps_before) / self.prefill_tps_before < 0.01

    @property
    def decode_moved(self):
        return abs(self.decode_tps_after - self.decode_tps_before) / self.decode_tps_before > 0.10


def diagnose(s):
    """Attribute the failure to a layer. Model is reached only by elimination."""
    if s.served_model_id != s.expected_model_id:
        return "silent model swap"
    if s.prefill_flat and s.decode_moved:
        return "serving stack"          # one phase moved, the control held
    if s.endpoint_ok and not s.agent_loop_ok:
        return "harness"                # cheap checks lie; the loop tells
    if not s.endpoint_ok:
        return "endpoint"
    return "model"


def probe_full_loop(endpoint, scripted_calls):
    """Run the real agent loop: propose, execute, verify each tool effect."""
    transcript = []
    for call in scripted_calls:
        result = endpoint.execute(call)
        transcript.append((call["name"], result["status"]))
        if result["status"] != "ok":
            return {"ok": False, "failed_at": call["name"], "transcript": transcript}
    return {"ok": True, "transcript": transcript}


class FaultyEndpoint:
    """Endpoint with a planted fault: it drops tool results silently."""

    def __init__(self, plant_fault=True):
        self.plant_fault = plant_fault

    def health(self):
        return {"status": "ok"}          # the cheap check passes regardless

    def execute(self, call):
        if self.plant_fault and call["name"].startswith("tool_"):
            return {"status": "error", "detail": "missing parser flag"}
        return {"status": "ok"}


if __name__ == "__main__":
    quiet = Signals(6266, 6249, 112.0, 160.0, True, True, "model-a", "model-a")
    print("quiet failure ->", diagnose(quiet))
    swap = Signals(6266, 6249, 112.0, 112.0, True, True, "model-b", "model-a")
    print("silent swap ->", diagnose(swap))
    ep = FaultyEndpoint(plant_fault=True)
    print("endpoint health:", ep.health())
    print("full loop:", probe_full_loop(ep, [{"name": "read_prompt"}, {"name": "tool_calendar"}]))
