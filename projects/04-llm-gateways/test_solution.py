import unittest
from solution import Endpoint, Budget, route

class GatewayTests(unittest.TestCase):
    def test_eligible_fallback(self):
        a=Endpoint("a",{"internal"},.04,"timeout"); b=Endpoint("b",{"internal"},.06)
        result=route("hello","internal",[a,b],Budget(.10))
        self.assertEqual((result["endpoint"],result["attempts"]),("b",2))
    def test_ineligible_route_is_never_called(self):
        denied=Endpoint("public-only",{"public"},.01)
        with self.assertRaises(PermissionError): route("secret","internal",[denied],Budget(1))
        self.assertEqual(denied.calls,0)
    def test_budget_is_reserved_before_call(self):
        endpoint=Endpoint("expensive",{"internal"},2)
        with self.assertRaises(RuntimeError): route("x","internal",[endpoint],Budget(1))
        self.assertEqual(endpoint.calls,0)
    def test_malformed_result_can_fallback(self):
        bad=Endpoint("bad",{"internal"},.01,"malformed"); good=Endpoint("good",{"internal"},.01)
        self.assertEqual(route("x","internal",[bad,good],Budget(1))["endpoint"],"good")

if __name__ == "__main__": unittest.main()
