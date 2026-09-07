import unittest
from solution import Telemetry, log_event, add_span, score, why

def wired():
    tel = Telemetry()
    log_event(tel, "task-7", "tool.call", tool="send_brief", outcome="ok")
    add_span(tel, "task-7", "model.call", record_version=7)
    score(tel, "task-7", "brief_correctness", 0.0)
    log_event(tel, "task-8", "tool.call", tool="read_event", outcome="ok")
    return tel

class ThreeSignalTests(unittest.TestCase):
    def test_three_signals_join_on_one_task_id(self):
        report = why(wired(), "task-7")
        self.assertEqual(len(report["logs"]), 1)
        self.assertEqual(len(report["spans"]), 1)
        self.assertEqual(len(report["scores"]), 1)
        self.assertEqual(report["scores"][0]["grader"], "brief_correctness")

    def test_join_excludes_other_tasks(self):
        report = why(wired(), "task-7")
        self.assertNotIn("read_event", [e.get("tool") for e in report["logs"]])

    def test_events_without_task_ids_fail_loudly(self):
        tel = Telemetry()
        with self.assertRaises(ValueError):
            log_event(tel, "", "x")
        with self.assertRaises(ValueError):
            add_span(tel, "", "x")
        with self.assertRaises(ValueError):
            score(tel, "", "grader", 0.0)

if __name__ == "__main__": unittest.main()
