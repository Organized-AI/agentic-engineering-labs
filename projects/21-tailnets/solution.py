def load_policy(rules):
    """rules: iterable of (src_tag, dst_tag, ports) grants. Default is deny."""
    return tuple((src, dst, frozenset(ports)) for src, dst, ports in rules)

def allows(policy, device_tags, dst_tag, port):
    """True only when a rule grants one of the device's tags this exact path."""
    for src, dst, ports in policy:
        if src in device_tags and dst == dst_tag and port in ports:
            return True
    return False

def audit(policy, devices, services):
    """Report every device/service/port path as allowed or denied."""
    report = []
    for name, tags in devices.items():
        for dst_tag, ports in services.items():
            for port in ports:
                report.append({
                    "device": name, "service": dst_tag, "port": port,
                    "allowed": allows(policy, tags, dst_tag, port),
                })
    return report

if __name__ == "__main__":
    policy = load_policy([
        ("tag:dev-macs", "tag:services", (11434, 22)),   # Ollama + SSH
        ("tag:mobile", "tag:services", (8123,)),         # dashboard only
    ])
    devices = {
        "macbook": ("tag:dev-macs",),
        "iphone": ("tag:mobile",),
        "stranger": ("tag:unknown",),
    }
    services = {"tag:services": (11434, 22, 8123)}
    for row in audit(policy, devices, services):
        mark = "ALLOW" if row["allowed"] else "deny "
        print(f"{mark} {row['device']:8s} -> {row['service']}:{row['port']}")
