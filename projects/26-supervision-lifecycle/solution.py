"""Supervisor Tree - reference solution."""
import time


class WedgedServer:
    """Accepts calls, never answers within the deadline."""

    def request(self, payload, timeout):
        raise TimeoutError("wedged")


class FlakyServer:
    def __init__(self):
        self.restarts = 0

    def request(self, payload, timeout):
        return {"events": ["standup at 9"]}

    def restart(self):
        self.restarts += 1


class CircuitOpen(Exception):
    pass


def health_check(server, timeout=0.5):
    """Health is a definition: a real read inside a deadline, not a ping."""
    try:
        server.request({"op": "known_event_read"}, timeout=timeout)
        return True
    except TimeoutError:
        return False


class Supervisor:
    def __init__(self, failure_threshold=3, restart_limit=3, window_s=60):
        self.failure_threshold = failure_threshold
        self.restart_limit = restart_limit
        self.window_s = window_s
        self.failures = {}
        self.restarts = {}
        self.breakers = set()

    def record_failure(self, name, server):
        self.failures[name] = self.failures.get(name, 0) + 1
        if self.failures[name] >= self.failure_threshold:
            self.failures[name] = 0
            self._restart(name, server)

    def _restart(self, name, server):
        now = time.monotonic()
        stamps = [t for t in self.restarts.get(name, []) if now - t < self.window_s]
        stamps.append(now)
        self.restarts[name] = stamps
        if len(stamps) > self.restart_limit:
            self.breakers.add(name)  # flapping: the agent can read this
            return
        if hasattr(server, "restart"):
            server.restart()

    def call(self, name, server, payload):
        if name in self.breakers:
            raise CircuitOpen(f"{name}: circuit open, degrade honestly")
        try:
            return server.request(payload, timeout=0.5)
        except TimeoutError:
            self.record_failure(name, server)
            raise


if __name__ == "__main__":
    sup = Supervisor()
    wedged = WedgedServer()
    for attempt in range(13):
        try:
            sup.call("calendar", wedged, {"op": "read"})
        except (TimeoutError, CircuitOpen) as e:
            last = str(e)
    print(f"after 13 wedged calls: {last}")
