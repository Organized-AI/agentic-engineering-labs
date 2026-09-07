"""Five Walls Bench - implement the Sandbox policy methods, mint(), and run_generated_report()."""
import time


class Denied(Exception):
    pass


class Token:
    def __init__(self, scope, ttl_s):
        self.scope = scope
        self.expires_at = time.monotonic() + ttl_s
        self.revoked = False


def mint(scope, ttl_s=300):
    """Scoped, single-purpose, short-lived - nothing ambient."""
    return Token(scope, ttl_s)


class Sandbox:
    """The edge, enforced: own filesystem, deny-by-default egress, caps, teardown."""

    def __init__(self, owner, allowlist=(), cpu_s=60, mem_mb=512):
        self.owner = owner
        self.allowlist = set(allowlist)
        self.cpu_s = cpu_s
        self.mem_mb = mem_mb
        self.destroyed = False
        self.log = []

    def egress(self, host):
        raise NotImplementedError

    def read_file(self, path):
        if not path.startswith("/scratch/"):
            self.log.append(("deny-fs", path))
            raise Denied(f"outside scratch: {path}")
        return "sandbox-local data"

    def exec(self, code, env=None, cpu_s_used=1):
        if self.destroyed:
            raise Denied("sandbox is destroyed")
        if cpu_s_used > self.cpu_s:
            self.log.append(("deny-resource", cpu_s_used))
            raise Denied("resource cap exceeded")
        return {"output": f"ran: {code}", "success": True}

    def destroy(self):
        self.destroyed = True


class Store:
    def __init__(self):
        self.data = {}

    def write(self, key, value):
        self.data[key] = value


def run_generated_report(task_id, code, tenant, store):
    sb = Sandbox(owner=tenant, allowlist=["api.venue-db.internal"])
    creds = mint(scope="venue:read", ttl_s=300)
    raise NotImplementedError


