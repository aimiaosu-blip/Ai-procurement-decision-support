import tempfile, unittest
from pathlib import Path
from portfolio.governance import ReviewStore
class GovernanceTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.store=ReviewStore(Path(self.tmp.name)/'audit.sqlite')
    def tearDown(self): self.store.db.close(); self.tmp.cleanup()
    def test_required_identity_and_reason(self):
        with self.assertRaises(ValueError): self.store.decide('a','approve','','')
    def test_blocked_approval(self):
        with self.assertRaises(ValueError): self.store.decide('a','approve','demo','reviewed',True)
        self.assertEqual(self.store.rows(),[])
    def test_final_and_tamper_detection(self):
        self.store.decide('a','revise','demo','Missing evidence',True)
        self.assertTrue(self.store.verify())
        with self.assertRaises(ValueError): self.store.decide('a','approve','demo','again')
        self.store.db.execute("UPDATE reviews SET reason='tampered'")
        self.assertFalse(self.store.verify())
