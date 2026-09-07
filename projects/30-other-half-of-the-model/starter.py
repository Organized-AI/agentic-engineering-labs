"""Attribution Bench - implement diagnose() and probe_full_loop()."""
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
    raise NotImplementedError


def probe_full_loop(endpoint, scripted_calls):
    """Run the real agent loop: propose, execute, verify each tool effect."""
    raise NotImplementedError


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


