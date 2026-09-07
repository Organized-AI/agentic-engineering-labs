import unittest
from solution import Queue, submit, decide, execute

def approved_queue():
    queue = Queue()
    rid = submit(queue, "send_brief", "hash:brief-v7", now=0)
    decide(queue, rid, approve=True, by="organizer", now=10)
    return queue, rid

class OversightTests(unittest.TestCase):
    def test_exact_approval_executes_and_audits_first(self):
        queue, rid = approved_queue()
        result = execute(queue, rid, "hash:brief-v7", lambda: "brief sent")
        self.assertEqual(result, "brief sent")
        self.assertEqual(queue.audit[0]["action"], "send_brief")
        self.assertEqual(queue.audit[0]["by"], "organizer")

    def test_approvals_are_single_use(self):
        queue, rid = approved_queue()
        execute(queue, rid, "hash:brief-v7", lambda: "brief sent")
        with self.assertRaises(PermissionError):
            execute(queue, rid, "hash:brief-v7", lambda: "replay")

    def test_changed_context_and_expiry_block_execution(self):
        queue, rid = approved_queue()
        with self.assertRaises(PermissionError):
            execute(queue, rid, "hash:brief-DOCTORED", lambda: "doctored")
        stale = submit(queue, "send_brief", "hash:old", now=0, ttl=60)
        decision = decide(queue, stale, approve=True, by="organizer", now=120)
        self.assertFalse(decision["approved"])
        with self.assertRaises(PermissionError):
            execute(queue, stale, "hash:old", lambda: "late")

if __name__ == "__main__": unittest.main()
