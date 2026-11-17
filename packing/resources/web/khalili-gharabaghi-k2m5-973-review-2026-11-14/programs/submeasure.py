"""Is cover A a sub-measure of cover B?  (review of #973, L144)  Exact, per elementary piece and per rectangle.

usage: python -I submeasure.py A B
Every piece of A must carry at most B's weight at the same place (weights summed per piece, common denominator),
and A's Lebesgue rectangle must equal B's (same density).  Also reports where A's pieces lie.
"""
import json
import os
import sys
from fractions import Fraction as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from k2m5_cover import read_board, key_of, add  # noqa: E402


def meas(path):
    b = read_board(path)
    m = {}
    for x0, y0, x1, y1, w in b["segs"]:
        add(m, key_of(x0, y0, x1, y1), F(w, b["wden"]))
    return m, b["polys"], b["wden"]


a, pa, wa = meas(sys.argv[1])
b, pb, wb = meas(sys.argv[2])
over = [(k, str(v), str(b.get(k, 0))) for k, v in a.items() if v > b.get(k, 0)]
xs = [k[1] if k[0] == "v" else k[2] for k in a] + [k[2] + 1 if k[0] == "h" else k[1] for k in a]
ys = [k[1] if k[0] == "h" else k[2] for k in a] + [k[2] + 1 if k[0] == "v" else k[1] for k in a]
rect_a = [(p[0], F(p[1], wa), p[2:]) for p in pa]
rect_b = [(p[0], F(p[1], wb), p[2:]) for p in pb]
print(json.dumps(dict(pieces=len(a), exceeding=len(over), first_exceeding=over[:3], rect_equal=rect_a == rect_b,
                      x_range_tenths=[min(xs), max(xs)], y_range_tenths=[min(ys), max(ys)],
                      submeasure=not over and rect_a == rect_b), default=str))
