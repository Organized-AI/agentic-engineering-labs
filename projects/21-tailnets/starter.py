def load_policy(rules):
    """rules: iterable of (src_tag, dst_tag, ports) grants. Default is deny."""
    return tuple((src, dst, frozenset(ports)) for src, dst, ports in rules)

def allows(policy, device_tags, dst_tag, port):
    """TODO: True only if a rule grants one of the device's tags access."""
    raise NotImplementedError

def audit(policy, devices, services):
    """TODO: report every (device, service, port) path and whether it is allowed."""
    raise NotImplementedError
