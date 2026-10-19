#!/usr/bin/env python3
"""Exact mu at every corner of the uncertified boxes zmx2 lists for one root (k2m5_review.py's evaluator).
usage: corner_scan.py COVER ZMX2_LOG ROOT_ID"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import k2m5_review as K  # noqa: E402

cover, log, rid = sys.argv[1], sys.argv[2], int(sys.argv[3])
cv = K.Cover(K.read_bytes(cover))
ev = K.Evaluator(cv)
k = int(cv.side)
zl = K.read_zmx2_log(log, k, '%016x' % K.fnv1a64(K.read_bytes(cover)))
best = None
for b in zl['_unc'].get(rid, []):
    for cx in (b[0], b[1]):
        for cy in (b[2], b[3]):
            for u in (b[4], b[5]):
                if K.adm_f(ev, cx, cy, u):
                    m = K.mass_f(ev, cx, cy, u)
                    if best is None or m < best[0]:
                        best = (m, (cx, cy, u))
print('root', rid, 'boxes', len(zl['_unc'].get(rid, [])), 'lowest corner mu %.12f' % float(best[0]),
      'at', ','.join(str(v) for v in best[1]))
