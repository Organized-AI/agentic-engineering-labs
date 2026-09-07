import unittest

from solution import (Capability, Measurement, StatelessMcpServer,
                      harden, measure, route)


class TestToolDoorRouter(unittest.TestCase):
    def test_stateless_server_assigns_no_session(self):
        server = StatelessMcpServer({"ping": {"type": "object"}})
        init = server.handle({"method": "initialize"})
        self.assertIsNone(init["session"])
        tools = server.handle({"method": "tools/list"})
        self.assertEqual([t["name"] for t in tools["tools"]], ["ping"])
        # A request with no session header still succeeds: stateless.
        result = server.handle({"method": "tools/call", "name": "ping"})
        self.assertEqual(result["result"], "called ping")

    def test_routing_rules(self):
        self.assertEqual(route(Capability("db", needs_session=True)), "mcp")
        self.assertEqual(route(Capability("cal", has_complex_schema=True)), "mcp")
        self.assertEqual(route(Capability("git")), "cli")
        self.assertEqual(route(Capability("odd", already_installed=False)),
                         "cli_behind_a_wrapper")
        brief = Capability("daily-brief", repeated=True, exact=True)
        self.assertEqual(route(brief), "script")

    def test_measure_and_harden(self):
        cap = Capability("calendar", has_complex_schema=True)
        mcp = measure(cap, "mcp", schema_tokens=400, bad_calls=3)
        cli = measure(cap, "cli", help_tokens=3000, bad_calls=3)
        self.assertLess(mcp.discovery_tokens, cli.discovery_tokens)
        self.assertEqual(mcp.validation_catches, 3)
        self.assertEqual(cli.validation_catches, 0)
        brief = Capability("daily-brief", repeated=True, exact=True)
        self.assertEqual(harden(brief), "scripts/daily-brief.sh")
        with self.assertRaises(ValueError):
            harden(cap)  # not repeated/exact: stays in the model


if __name__ == "__main__":
    unittest.main()
