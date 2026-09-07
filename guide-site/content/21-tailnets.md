> **The question:** How do your agents, dev machines, and services reach each other when none of them should be on the public internet?

Every chapter so far assumed the pieces of the system can talk to each other. For a solo builder or a small team running agents across laptops, a home server, and cloud workers, that assumption is the actual infrastructure problem. A tailnet - a Tailscale network - is the cleanest current answer: a WireGuard mesh where every device gets a stable identity and address, and nothing needs a public port.

## The mental model

A tailnet flips the default. Instead of opening inbound holes in firewalls and guarding them, every device joins the mesh with its own cryptographic identity, traffic is end-to-end encrypted peer-to-peer (WireGuard), and the default posture is deny. Reaching a service means being on the tailnet and being allowed by policy - not being on the right network.

Each machine keeps one stable 100.x.y.z address and a MagicDNS name, so `ssh pi5` or `curl http://pi5:11434` works from any peer, anywhere, with no VPN client config to babysit. Tailscale SSH replaces key distribution on Linux hosts: access is decided by the tailnet policy file, not by which laptop's key got copied where.

## ACLs are the agent-security boundary from chapter 13

The policy file is where tailnets meet the rest of this guide. ACLs define which identities can reach which devices and ports, and they read like the capability rules from chapter 13: the agent-hosting Mac can reach the Pi's Ollama port and nothing else; the phone is a client, never a host; no device exposes anything publicly.

```python
# Pseudocode: mesh policy mirrors capability policy.
rules = [
    allow(src="tag:dev-macs", dst=["tag:services:11434,22"]),  # Ollama + SSH only
    allow(src="tag:mobile",   dst=["tag:services:8123"]),      # Home Assistant UI
    # everything else: denied by default
]
```

When an agent calls a mesh-local LLM endpoint - say Ollama on the services hub - the network itself enforces chapter 13's egress rules: the model endpoint has no public surface at all, so a prompt-injected agent cannot be tricked into exfiltrating to it from the internet, and the endpoint cannot be probed from outside.

## The boundary Funnel draws

Sometimes something must be public - a webhook receiver, a demo page. Tailscale Funnel exposes a single service to the internet through Tailscale's edge, and it is the exception that proves the posture: exposure is per-service, named, and visible in the same policy world, instead of a forgotten router port-forward. For teams that want the control plane in-house, Headscale is the open-source, self-hosted coordination server implementing the same protocol.

A working reference shape: a handful of dev machines sharing one synced dev surface, a low-power always-on box as the services hub (LLM inference, home automation, long-running agents), a phone as a pure client, and deploy targets living in the cloud. The mesh is the workstation; the cloud is only the publishing edge.

## Lab: bring up a three-node mesh

Create a tailnet, join two machines and one always-on box, and give the box a service (an Ollama endpoint is ideal). Write the ACL that lets the dev machines reach exactly that port. Verify with curl from inside the mesh and a failed connection from outside it.

Then add the agent: point a chapter 05 style tool at the mesh endpoint and confirm the harness treats it like any other tool - contract, timeout, provenance. Rotate a device off the tailnet and confirm its access dies with its identity, not with a firewall rule someone remembers to remove.

## Failure drills

Probe the service from the public internet. Join a new device and confirm default-deny until policy admits it. Tail-scale SSH into the hub with a device whose access the ACL doesn't grant. Expose a service with Funnel, then close it and verify the public path is gone. Lose the coordination server connection and confirm existing peer sessions keep working.

## Ship gate

Every service an agent uses is reachable only through the mesh, the policy file names each allowed path, and exposure to the public internet is a deliberate, listed exception. The network becomes part of the system's documented trust boundary. Underneath even that sits the oldest layer of all: [engineering best practices](/agentic-eng/chapters/engineering-best-practices/).

Sources: [Tailscale ACLs](https://tailscale.com/kb/1018/acls), [Tailscale SSH](https://tailscale.com/kb/1193/tailscale-ssh), [MagicDNS](https://tailscale.com/kb/1081/magicdns), [Tailscale Funnel](https://tailscale.com/kb/1223/funnel), [Headscale](https://github.com/juanfont/headscale)
