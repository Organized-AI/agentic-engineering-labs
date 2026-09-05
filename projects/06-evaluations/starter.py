from dataclasses import dataclass

@dataclass(frozen=True)
class Task:
    id: str
    expected_venue: str
    forbidden_effect: str | None = None

def evaluate(tasks: list[Task], agent, trials=1) -> dict:
    """TODO: run all trials and grade saved outcome plus forbidden effects."""
    raise NotImplementedError

def release_gate(report: dict, minimum_rate=.8) -> bool:
    """TODO: hard-gate violations fail; otherwise check accepted/all attempts."""
    raise NotImplementedError
