import unittest
from solution import Fact, resolve_venue

class OntologyTests(unittest.TestCase):
    def setUp(self):
        self.tenants={"event-a":"org-a","event-b":"org-b"}
        self.facts=[
            Fact("event-a","takesPlaceAt","venue-1","approved-event",True,10),
            Fact("event-a","takesPlaceAt","venue-old","old-announcement",True,0,10),
            Fact("venue-1","label","Hall A","approved-venue",True,0),
            Fact("venue-1","label","The Secret Hall","model-summary",False,0),
        ]
    def test_temporal_approved_resolution(self):
        result=resolve_venue("event-a","org-a",self.tenants,self.facts,10)
        self.assertEqual(result,{"venue_id":"venue-1","label":"Hall A","link_source":"approved-event","label_source":"approved-venue"})
    def test_authorization_is_separate(self):
        with self.assertRaises(PermissionError): resolve_venue("event-a","org-b",self.tenants,self.facts,10)
    def test_ambiguity_is_not_smoothed_over(self):
        ambiguous=self.facts+[Fact("event-a","takesPlaceAt","venue-2","other",True,10)]
        with self.assertRaises(ValueError): resolve_venue("event-a","org-a",self.tenants,ambiguous,10)

if __name__ == "__main__": unittest.main()
