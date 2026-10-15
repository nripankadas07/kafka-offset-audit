import copy,json,unittest
from pathlib import Path
import kafka_offset_audit as m

class Behavior(unittest.TestCase):
    def setUp(self):
        self.d=json.loads((Path(__file__).parent/'example.json').read_text())
    def bad(self):
        with self.assertRaises(m.InputError):m.analyze(self.d)
    def test_unknown_field_rejected(self):
        self.d['unknown']=True;self.bad()

    def test_next_offset_and_distance(self):
        r=m.analyze(self.d);self.assertEqual(r['partitions'][0]['offset_distance_to_end'],7);self.assertEqual(r['findings'],[])
    def test_end_boundary_is_valid(self):
        self.d['partitions'][0]['committed']=27;self.assertEqual(m.analyze(self.d)['partitions'][0]['offset_distance_to_end'],0)
    def test_start_boundary_is_valid(self):
        self.d['partitions'][0]['committed']=12;self.assertEqual(m.analyze(self.d)['findings'],[])
    def test_retention_gap_no_reset(self):
        self.d['partitions'][0]['committed']=3;r=m.analyze(self.d)['partitions'][0];self.assertEqual(r['status'],'retention_gap');self.assertIsNone(r['hypothetical_start'])
    def test_earliest_is_hypothetical(self):
        self.d['reset']='earliest';self.d['partitions'][0]['committed']=None;r=m.analyze(self.d);self.assertEqual(r['partitions'][0]['hypothetical_start'],12);self.assertTrue(r['findings'])
    def test_latest_ahead_commit(self):
        self.d['reset']='latest';self.d['partitions'][0]['committed']=99;self.assertEqual(m.analyze(self.d)['partitions'][0]['hypothetical_start'],27)
    def test_requested_skip(self):
        self.d['partitions'][0]['requested']=24;self.assertEqual(m.analyze(self.d)['partitions'][0]['movement'],{'kind':'skip','offset_distance':4})
    def test_requested_replay(self):
        self.d['partitions'][0]['requested']=12;self.assertEqual(m.analyze(self.d)['partitions'][0]['movement'],{'kind':'replay','offset_distance':8})
    def test_unknown_commit_requested_needs_review(self):
        self.d['partitions'][0].update(committed=None,requested=12);self.assertEqual(len(m.analyze(self.d)['findings']),2)
    def test_duplicate_partition(self):
        self.d['partitions']*=2;self.bad()
    def test_inverted_bounds(self):
        self.d['partitions'][0]['log_start']=28;self.bad()
    def test_bad_request(self):
        self.d['partitions'][0]['requested']=28;self.bad()
    def test_boolean_offset(self):
        self.d['partitions'][0]['committed']=True;self.bad()

if __name__ == '__main__':unittest.main()
