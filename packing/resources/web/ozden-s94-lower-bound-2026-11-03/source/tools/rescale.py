#!/usr/bin/env python3
"""Rescale a published rectangle-density certificate by lambda = L'/L (similarity about the origin):
rectangles x lambda, B' = lambda*B, same masses, same net.  Valid iff B'(1+D) < 1 and the full coverage check passes
(each new core maps to an old core of side B; only the centre domain grows by rho*(1-1/lambda), so we re-check everything).
  rescale.py CAND.json.gz NEW_L OUT.json.gz [NEW_STEP NEW_LAST]   (optionally a finer uniform half-angle net)"""
import sys, json, gzip
from fractions import Fraction as Fr
d = json.load(gzip.open(sys.argv[1], 'rt'), parse_float=str, parse_int=str)
L = Fr(d['L']); L2 = Fr(sys.argv[2]); lam = L2 / L
B = Fr(d['B']); B2 = B * lam
D = Fr(d['proof_net']['step']) if 'proof_net' in d else Fr(83, 40000)
out = dict(d); out['L'] = str(L2); out['B'] = str(B2)
if len(sys.argv) > 5:
    D = Fr(sys.argv[4]); out['proof_net'] = {'step': str(D), 'last': int(sys.argv[5])}
out['rectangles'] = [{'rectangle': [str(Fr(v) * lam) for v in r['rectangle']], 'mass': r['mass']} for r in d['rectangles']]
out['n'] = int(d['n'])
out.pop('scaling_source_digest', None); out.pop('scaling_factor', None)
out['derived_from'] = f"published certificate at L={d['L']} scaled by lambda={lam}"
print(json.dumps(dict(L=str(L2), Lf=float(L2), lam=str(lam), B=str(B2), Bf=float(B2), shrink=str(B2 * (1 + D)), shrink_f=float(B2 * (1 + D)), ok=B2 * (1 + D) < 1)))
with gzip.open(sys.argv[3], 'wt') as f: json.dump(out, f)
