import tempfile
import unittest
from pathlib import Path
from pipeline import Store, Conflict, LeaseError, AttemptLimit


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='agentic-eng-test-')
        self.path = Path(self.tmp.name)/'test.sqlite'
        self.store = Store(self.path)

    def tearDown(self):
        self.store.close()
        self.tmp.cleanup()

    def job(self):
        return self.store.submit('org_a', 'key-1', 'event_a')

    def test_duplicate_submit_is_one_operation(self):
        self.assertEqual(self.job(), self.job())
        self.assertEqual(self.store.counts()['jobs'], 1)

    def test_changed_input_conflicts(self):
        self.job()
        with self.assertRaises(Conflict):
            self.store.submit('org_a', 'key-1', 'event_a2')

    def test_foreign_event_is_inaccessible(self):
        with self.assertRaises(PermissionError):
            self.store.submit('org_a', 'key-1', 'event_b')
        self.assertEqual(self.store.counts()['jobs'], 0)

    def test_job_status_is_scoped_and_hides_token(self):
        job = self.job()
        self.store.claim(job, now=0)
        with self.assertRaises(PermissionError):
            self.store.get_job('org_b', job)
        self.assertNotIn('token', self.store.get_job('org_a', job))

    def test_active_lease_prevents_second_claim(self):
        job = self.job()
        self.assertIsNotNone(self.store.claim(job, now=0))
        self.assertIsNone(self.store.claim(job, now=1))

    def test_expired_lease_is_recoverable_and_fenced(self):
        job = self.job()
        old = self.store.claim(job, now=0, lease_seconds=10)
        current = self.store.claim(job, now=11, lease_seconds=10)
        self.assertNotEqual(old, current)
        with self.assertRaises(LeaseError):
            self.store.complete(job, old, self.store.fake_model(job), now=12)
        self.store.complete(job, current, self.store.fake_model(job), now=12)
        self.assertEqual(self.store.counts(), {'jobs': 1, 'briefs': 1, 'outbox': 1})

    def test_expired_worker_cannot_finalize_without_reclaim(self):
        job = self.job()
        token = self.store.claim(job, now=0, lease_seconds=10)
        with self.assertRaises(LeaseError):
            self.store.complete(job, token, self.store.fake_model(job), now=10)

    def test_completion_is_idempotent_and_outbox_is_atomic(self):
        job = self.job()
        token = self.store.claim(job, now=0)
        brief = self.store.fake_model(job)
        self.assertEqual(self.store.complete(job, token, brief, now=1), brief)
        self.assertEqual(self.store.complete(job, token, brief, now=2), brief)
        self.assertIsNone(self.store.claim(job, now=3))
        self.assertEqual(self.store.counts(), {'jobs': 1, 'briefs': 1, 'outbox': 1})

    def test_invalid_result_does_not_partially_commit(self):
        job = self.job()
        token = self.store.claim(job, now=0)
        brief = self.store.fake_model(job)
        brief['venue'] = 'Invented venue'
        with self.assertRaises(ValueError):
            self.store.complete(job, token, brief, now=1)
        brief = self.store.fake_model(job)
        brief['source_version'] = True
        with self.assertRaises(ValueError):
            self.store.complete(job, token, brief, now=1)
        self.assertEqual(self.store.counts(), {'jobs': 1, 'briefs': 0, 'outbox': 0})

    def test_source_change_blocks_stale_result(self):
        job = self.job()
        token = self.store.claim(job, now=0)
        brief = self.store.fake_model(job)
        self.store.db.execute("UPDATE events SET version=2 WHERE id='event_a'")
        with self.assertRaises(Conflict):
            self.store.complete(job, token, brief, now=1)
        self.assertEqual(self.store.counts()['briefs'], 0)

    def test_revoked_source_blocks_completion(self):
        job = self.job()
        token = self.store.claim(job, now=0)
        brief = self.store.fake_model(job)
        self.store.db.execute("UPDATE events SET enabled=0 WHERE id='event_a'")
        with self.assertRaises(PermissionError):
            self.store.complete(job, token, brief, now=1)

    def test_attempt_limit_is_persisted(self):
        job = self.job()
        for now in (0, 11, 22):
            self.store.claim(job, now=now, lease_seconds=10)
        with self.assertRaises(AttemptLimit):
            self.store.claim(job, now=33, lease_seconds=10)
        self.assertEqual(self.store.get_job('org_a', job)['state'], 'failed')

    def test_completed_state_survives_reopen(self):
        job = self.job()
        token = self.store.claim(job, now=0)
        self.store.complete(job, token, self.store.fake_model(job), now=1)
        self.store.close()
        self.store = Store(self.path)
        self.assertEqual(self.job(), job)
        self.assertEqual(self.store.get_job('org_a', job)['state'], 'succeeded')
        self.assertEqual(self.store.counts(), {'jobs': 1, 'briefs': 1, 'outbox': 1})


if __name__ == '__main__':
    unittest.main()
