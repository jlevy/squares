"""Sharp controls for rv_check's two routes on one certificate (think-ikku review).

For each certificate: (1) the side lowered by the least far-wall clearance, at contact
and EPS past it; (2) the square with the least left clearance moved left by it, at
contact and EPS past; (3) the tightest pair's second square moved along the axis of
its largest separating gap by that gap, at contact and EPS past; (4) a duplicated
square. Both routes must accept every contact mutant and refuse every past one.

Usage: python -I rv_controls.py CERT [CERT...]
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction as F

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from rv_check import area2, ccw, clip, corners, extent, pair_margin, read_cert, route_a, route_b  # noqa: E402

EPS = F(1, 10**60)


def axis_of_gap(a, b):
    xa, ya, ca, sa = a
    xb, yb, cb, sb = b
    dx, dy = xb - xa, yb - ya
    best = None
    for (ax, ay) in ((ca, sa), (-sa, ca), (cb, sb), (-sb, cb)):
        proj = dx * ax + dy * ay
        ra = (abs(ca * ax + sa * ay) + abs(-sa * ax + ca * ay)) / 2
        rb = (abs(cb * ax + sb * ay) + abs(-sb * ax + cb * ay)) / 2
        g = abs(proj) - ra - rb
        sgn = 1 if proj > 0 else -1
        if best is None or g > best[0]:
            best = (g, ax * sgn, ay * sgn)
    return best


def decide(side, sq):
    return route_a(side, sq)[0], route_b(side, sq)[0]


def run(path):
    n, side, sq = read_cert(path)
    ok, w, least, where, _ = route_a(side, sq)
    res = {"cert": path.rsplit("/", 1)[-1], "n": n}
    far = min(w["right"], w["top"])
    res["side_at_contact"] = decide(side - far, sq)
    res["side_past"] = decide(side - far - EPS, sq)
    k = min(range(n), key=lambda i: sq[i][0] - extent(sq[i][2], sq[i][3]))
    clr = sq[k][0] - extent(sq[k][2], sq[k][3])
    for tag, d in (("wall_at_contact", clr), ("wall_past", clr + EPS)):
        m = list(sq)
        m[k] = (sq[k][0] - d, sq[k][1], sq[k][2], sq[k][3])
        res[tag] = decide(side, m)
    i, j = where
    g, ax, ay = axis_of_gap(sq[i], sq[j])
    for tag, d in (("pair_at_contact", g), ("pair_past", g + EPS)):
        m = list(sq)
        m[j] = (sq[j][0] - d * ax, sq[j][1] - d * ay, sq[j][2], sq[j][3])
        res[tag] = decide(side, m)
        pa = pair_margin(m[i], m[j]) >= 0
        inter = clip(ccw(corners(*m[j])), ccw(corners(*m[i])))
        pb = (area2(inter) if len(inter) >= 3 else 0) == 0
        res[tag + "_pair_only"] = (pa, pb)
    m = list(sq)
    m[1] = sq[0]
    res["duplicate"] = decide(side, m)
    want = {"side_at_contact": (True, True), "side_past": (False, False),
            "wall_at_contact": (True, True), "wall_past": (False, False),
            "pair_at_contact_pair_only": (True, True), "pair_past_pair_only": (False, False),
            "duplicate": (False, False)}
    res["as_required"] = all(res[k2] == v for k2, v in want.items())
    return res


if __name__ == "__main__":
    for p in sys.argv[1:]:
        print(json.dumps(run(p)), flush=True)
