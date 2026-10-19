"""Triage diagnostic for #594: compare the corner region [0, 2.5)^2 of the s(76) cover with
wand125's s(59) cover (the source says its corners are that cover's, unchanged apart from the
band insertion). Atoms are compared as measures: points by position, segments by
(line, endpoints), each mass as an exact fraction of total weight.

usage: python -I corner_compare.py S59_COVER S76_COVER [CUT]
"""

import sys
from fractions import Fraction as F


def read(path):
    toks = [ln.split() for ln in open(path) if ln.strip() and not ln.startswith("#")]
    assert toks[0] == ["mixed", "1"]
    s = F(int(toks[1][0]), int(toks[1][1]))
    D, W, m = int(toks[2][0]), int(toks[3][0]), int(toks[4][0])
    pts = {}
    for t in toks[5:5 + m]:
        x, y, w = (int(v) for v in t)
        key = (F(x, D), F(y, D))
        pts[key] = pts.get(key, 0) + F(w, W)
    k = int(toks[5 + m][0])
    segs = {}
    for t in toks[6 + m:6 + m + k]:
        x0, y0, x1, y1, w = (int(v) for v in t)
        a, b = sorted(((F(x0, D), F(y0, D)), (F(x1, D), F(y1, D))))
        segs[(a, b)] = segs.get((a, b), 0) + F(w, W)
    return s, pts, segs


cut = F(sys.argv[3]) if len(sys.argv) > 3 else F(5, 2)
s59, p59, g59 = read(sys.argv[1])
s76, p76, g76 = read(sys.argv[2])


def corner_pts(p):
    return {k: v for k, v in p.items() if k[0] < cut and k[1] < cut and v != 0}


def corner_segs(g):
    return {k: v for k, v in g.items() if max(k[0][0], k[1][0]) < cut and max(k[0][1], k[1][1]) < cut and v != 0}


a, b = corner_pts(p59), corner_pts(p76)
sa, sb = corner_segs(g59), corner_segs(g76)
same_p = sum(1 for k in a if b.get(k) == a[k])
same_s = sum(1 for k in sa if sb.get(k) == sa[k])
print(f"cut {cut}: s59 corner points {len(a)} mass {float(sum(a.values())):.9f}; "
      f"s76 corner points {len(b)} mass {float(sum(b.values())):.9f}; identical {same_p}")
print(f"segments: s59 {len(sa)} mass {float(sum(sa.values())):.9f}; s76 {len(sb)} mass "
      f"{float(sum(sb.values())):.9f}; identical {same_s}")
only59 = set(a) - set(b)
only76 = set(b) - set(a)
diffw = [k for k in set(a) & set(b) if a[k] != b[k]]
print(f"points only in s59 {len(only59)}, only in s76 {len(only76)}, same place other mass {len(diffw)}")
if diffw:
    ratios = sorted({b[k] / a[k] for k in diffw})
    print("mass ratios s76/s59 at shared places (first five):", [str(r) for r in ratios[:5]], "count", len(ratios))
