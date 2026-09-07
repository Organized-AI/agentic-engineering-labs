"""Five Walls Bench - reference solution."""
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
        if self.destroyed:
            raise Denied("sandbox is destroyed")
        if host not in self.allowlist:
            self.log.append(("deny-egress", host))
            raise Denied(f"egress denied: {host}")
        return True

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
    try:
        result = sb.exec(code, env={"VENUE_TOKEN": creds.token if hasattr(creds, "token") else "tok"})
        store.write(f"reports/{task_id}", result["output"])
        return result
    finally:
        creds.revoked = True
        sb.destroy()  # teardown is total, success or failure


if __name__ == "__main__":
    store = Store()
    print(run_generated_report("rpt-1", "generate_daily()", "tenant-a", store))
    sb = Sandbox(owner="tenant-a", allowlist=["api.venue-db.internal"])
    for attack in [lambda: sb.egress("evil.example"),
                   lambda: sb.read_file("/etc/host-config")]:
        try:
            attack()
        except Denied as e:
            print("denied:", e)
    print("log:", sb.log)
