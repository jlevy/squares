"""Identity of two packings at one count (lane r1021-1118).  A measurement; it decides no bound.

The first packing P (the predecessor) is mapped onto the second, Q, under each of
the eight symmetries of the box, in two frames: lower-left (the symmetry of
[0, S_P]^2 applied to P, Q as it stands) and box-centred (each packing's box centre
moved to the origin, the symmetry applied about it).  Centres are paired two ways:

- nearest: each square of Q takes the nearest centre of the mapped P (candidates
  found in binary64, the nearest of the four closest decided exactly); the pairing
  is one to one when every square of P is taken exactly once;
- optimal: the assignment of least summed squared move (chosen in binary64 with
  SciPy's linear_sum_assignment), every reported move then computed exactly.

For the optimal assignment it counts the squares that move beyond 1e-9, 1e-6, 1e-3,
1e-2 and 1e-1, gives the largest move, whether every index is kept, the squares
whose orientation (an edge direction modulo quarter turns, carried by the symmetry)
is kept exactly, and the largest turn in degrees (binary64, printed only).
"""

from __future__ import annotations

import os as _os
import sys as _sys

_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))  # this packet's programs/, run with -I

import math
from fractions import Fraction

import numpy as np
from scipy.optimize import linear_sum_assignment

BOUNDS = [("1e-9", Fraction(1, 10**9)), ("1e-6", Fraction(1, 10**6)), ("1e-3", Fraction(1, 10**3)),
          ("1e-2", Fraction(1, 100)), ("1e-1", Fraction(1, 10))]

# (name, point map on [0, S]^2, direction map)
SYMMETRIES = [
    ("identity", lambda x, y, s: (x, y), lambda c, d: (c, d)),
    ("rot90", lambda x, y, s: (s - y, x), lambda c, d: (-d, c)),
    ("rot180", lambda x, y, s: (s - x, s - y), lambda c, d: (-c, -d)),
    ("rot270", lambda x, y, s: (y, s - x), lambda c, d: (d, -c)),
    ("mirror-x", lambda x, y, s: (s - x, y), lambda c, d: (-c, d)),
    ("mirror-y", lambda x, y, s: (x, s - y), lambda c, d: (c, -d)),
    ("transpose", lambda x, y, s: (y, x), lambda c, d: (d, c)),
    ("antitranspose", lambda x, y, s: (s - y, s - x), lambda c, d: (-d, -c)),
]


def canonical(c: Fraction, d: Fraction):
    for cc, dd in ((c, d), (-d, c), (-c, -d), (d, -c)):
        if cc > 0 and dd >= 0:
            return cc, dd
    raise ValueError("zero direction")


def turn_degrees(a, b) -> float:
    ta = math.degrees(math.atan2(float(a[1]), float(a[0])))
    tb = math.degrees(math.atan2(float(b[1]), float(b[0])))
    t = abs(ta - tb) % 90.0
    return min(t, 90.0 - t)


def mapped(poses, side: Fraction, sym, frame: str):
    _name, fp, fd = sym
    out = []
    for x, y, c, d in poses:
        if frame == "lower-left":
            mx, my = fp(x, y, side)
        else:
            mx, my = fp(x - side / 2, y - side / 2, Fraction(0))
        mc, md = fd(c, d)
        out.append((mx, my, mc, md))
    return out


def measure_pair(p_poses, p_side, q_poses, q_side, sym, frame: str) -> dict:
    mp = mapped(p_poses, p_side, sym, frame)
    if frame == "lower-left":
        mq = list(q_poses)
    else:
        mq = [(x - q_side / 2, y - q_side / 2, c, d) for x, y, c, d in q_poses]
    n = len(mq)
    a = np.array([[float(x), float(y)] for x, y, _c, _d in mp])
    b = np.array([[float(x), float(y)] for x, y, _c, _d in mq])
    dist = ((b[:, None, :] - a[None, :, :]) ** 2).sum(axis=2)
    nearest = []
    for k in range(n):
        cand = np.argsort(dist[k])[:4]
        exact = [((mq[k][0] - mp[int(j)][0]) ** 2 + (mq[k][1] - mp[int(j)][1]) ** 2, int(j)) for j in cand]
        exact.sort()
        nearest.append(exact[0][1])
    one_to_one = len(set(nearest)) == n
    rows, cols = linear_sum_assignment(dist)
    assign = dict(zip(rows.tolist(), cols.tolist(), strict=True))
    moves2 = []
    kept = 0
    turns = []
    for k in range(n):
        j = assign[k]
        moves2.append((mq[k][0] - mp[j][0]) ** 2 + (mq[k][1] - mp[j][1]) ** 2)
        oq = canonical(mq[k][2], mq[k][3])
        op = canonical(mp[j][2], mp[j][3])
        if oq == op:
            kept += 1
        turns.append(turn_degrees(oq, op))
    counts = {name: sum(1 for m2 in moves2 if m2 > t * t) for name, t in BOUNDS}
    kmax = max(range(n), key=lambda k: moves2[k])
    return {
        "symmetry": sym[0],
        "frame": frame,
        "nearest_one_to_one": one_to_one,
        "nearest_equals_optimal": all(nearest[k] == assign[k] for k in range(n)),
        "index_kept": all(assign[k] == k for k in range(n)),
        "beyond": counts,
        "largest_move": math.sqrt(float(moves2[kmax])),
        "largest_move_square_of_second": kmax + 1,
        "orientation_kept": kept,
        "largest_turn_deg": round(max(turns), 4),
        "summed_squared_move": float(sum(moves2)),
    }


def measure(p_poses, p_side, q_poses, q_side) -> dict:
    rows = []
    for frame in ("lower-left", "box-centred"):
        for sym in SYMMETRIES:
            rows.append(measure_pair(p_poses, p_side, q_poses, q_side, sym, frame))
    nearest_sym = {}
    for frame in ("lower-left", "box-centred"):
        fr = [r for r in rows if r["frame"] == frame]
        best = min(fr, key=lambda r: r["summed_squared_move"])
        nearest_sym[frame] = best["symmetry"]
    return {"rows": rows, "nearest_symmetry": nearest_sym,
            "one_to_one_under": sorted({f"{r['frame']}:{r['symmetry']}" for r in rows if r["nearest_one_to_one"]})}
