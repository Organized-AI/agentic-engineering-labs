import unittest
from solution import Profile, classify, assign, map_artifacts

class GovernanceTests(unittest.TestCase):
    def test_strictest_matching_class_wins(self):
        p = Profile("x", scores_people=True, manipulates=False, generates_content=True)
        self.assertEqual(classify(p), "high")
        dark = Profile("y", scores_people=True, manipulates=True, generates_content=True)
        self.assertEqual(classify(dark), "unacceptable")
        quiet = Profile("z", scores_people=False, manipulates=False, generates_content=False)
        self.assertEqual(classify(quiet), "minimal")

    def test_duties_follow_class_and_role(self):
        duties = assign("limited", role="deployer")
        self.assertEqual(duties, [{"duty": "transparency disclosure", "role": "deployer"}])
        self.assertEqual(assign("minimal", role="provider"), [])

    def test_every_duty_maps_to_an_artifact_or_fails(self):
        index = map_artifacts(assign("high", role="deployer"))
        self.assertEqual(len(index), 4)
        with self.assertRaises(KeyError):
            map_artifacts([{"duty": "invented duty", "role": "deployer"}])

if __name__ == "__main__": unittest.main()
