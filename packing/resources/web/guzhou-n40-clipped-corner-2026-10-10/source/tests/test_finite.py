"""精确运算与拒证测试。
Exact-arithmetic and refusal tests.
"""
from copy import deepcopy
from fractions import Fraction as Q
import json
from pathlib import Path
import random
import sys
import unittest
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'verifier'))
from finite import (PARAMS, PIN, candidate_bytes, expand_rotations, expand_vertices,
                    finite_check, peak_scan, peak_tree, read_source, transfer, unique, validate_nodes)

class FiniteTests(unittest.TestCase):
    def test_real_measure(self):
        positive, result = finite_check(ROOT/'certificate/certified_candidate.json', PARAMS)
        self.assertEqual(result['simple_counting_margin'], '1/625')
        self.assertEqual(result['parent_side'], '335000/335427')
        derived = json.loads(candidate_bytes(positive))
        self.assertEqual(derived['certificate']['angle_count'], 401)
        self.assertEqual(derived['certificate']['D'], '83/80000')
        self.assertEqual(len(derived['weights']), 480)
        self.assertEqual(sum(map(Q, derived['weights'])), Q(3999,100))
    def test_two_sweeps(self):
        rng = random.Random(401670854)
        for _ in range(40):
            rows = []
            for _ in range(30):
                a,c = sorted(rng.sample(range(-15,20),2))
                b,d = sorted(rng.sample(range(-15,20),2))
                rows.append((Q(a),Q(b),Q(c),Q(d),Q(rng.randrange(100),13)))
            self.assertEqual(peak_tree(rows), peak_scan(rows))
    def test_open_boundary(self):
        rows = [(Q(0),Q(0),Q(1),Q(1),Q(7)),(Q(1),Q(0),Q(2),Q(1),Q(9))]
        self.assertEqual(peak_tree(rows), 9)
        self.assertEqual(peak_scan(rows), 9)
    def test_duplicate_key_refusal(self):
        with self.assertRaises(ValueError):
            unique([('n',40),('n',41)])
    def test_parameter_refusals(self):
        for key, value in [('D','83/40000'),('last',200),('tau','1'),('X','7'),('h','1/100'),('mass','40')]:
            p = dict(PARAMS); p[key] = value
            with self.assertRaises(ValueError):
                transfer(p,Q(PARAMS['H']))
    def test_peak_refusal(self):
        with self.assertRaises(ValueError):
            transfer(PARAMS,Q(PARAMS['H'])-1)
    def test_source_refusal(self):
        with self.assertRaises(ValueError):
            read_source(ROOT/'certificate/parameters.json')
    def test_direction_refusals(self):
        digest = 'finite-control'
        summary = {'kind':'sqverify-fast-summary/v1','status':'VERIFIED',
                   'refused_directions':[],'fault_injected_at_box':None,'threshold':'10001/10000',
                   'premises':{'n':40,'angle_count':401,'centre_domain':'tokoharu','net_origin':'metadata',
                               'input_sha256':digest,'L':'67/10','B':'9977/10000','D':'83/80000','mass_exact':'3999/100'}}
        rows = [{'r':r,'method':'axis-vertex-sweep' if r==0 else 'interval-branch-and-bound',
                 'verdict':'verified','threshold':'10001/10000','min_certified_lower_bound':1.001,
                 'vertices':1,'nodes':1,'leaves':1} for r in range(401)]
        self.assertTrue(validate_nodes(summary,rows,digest))
        variants = []
        s,r = deepcopy(summary),deepcopy(rows); r.pop(); variants.append((s,r))
        s,r = deepcopy(summary),deepcopy(rows); r[2]['r']=1; variants.append((s,r))
        s,r = deepcopy(summary),deepcopy(rows); r[1]['min_certified_lower_bound']=0.999; variants.append((s,r))
        s,r = deepcopy(summary),deepcopy(rows); r[1]['threshold']='1'; variants.append((s,r))
        s,r = deepcopy(summary),deepcopy(rows); r[1]['verdict']='unresolved'; variants.append((s,r))
        s,r = deepcopy(summary),deepcopy(rows); s['status']='PARTIAL'; variants.append((s,r))
        s,r = deepcopy(summary),deepcopy(rows); s['premises']['angle_count']=201; variants.append((s,r))
        s,r = deepcopy(summary),deepcopy(rows); s['premises']['centre_domain']='per-bin'; variants.append((s,r))
        s,r = deepcopy(summary),deepcopy(rows); s['premises']['input_sha256']='wrong'; variants.append((s,r))
        s,r = deepcopy(summary),deepcopy(rows); s['fault_injected_at_box']=1; variants.append((s,r))
        for s,r in variants:
            with self.assertRaises(ValueError):
                validate_nodes(s,r,digest)

if __name__ == '__main__':
    unittest.main()
