"""Pose-by-pose comparison of a certificate with the packing it is said to refine.

Written for the think-ikku stage 4 review. A measurement for the review's identity
reading; it decides no bound. Reads a certificate (rv_check.read_cert) and the
comparison packing either as a certificate of the same format or as a known-best
witness YAML (centre + basis). For each count it reports:

- the exact side difference, relative difference, and both sides rounded up at
  12 places (the restatement ruling's print);
- the best of the box's 8 symmetries by nearest centres, whether nearest centres pair
  one to one, the largest centre move and turn (mod 90 degrees), and counts beyond
  1e-15, 1e-9, 1e-3;
- for squares that move beyond 1e-9: their exact free play in the comparison packing
  and in the certificate (the least separating-axis margin to any wall or neighbour),
  so that a moved square that touches nothing (a rattler) is told from one that does;
- each packing's least wall clearance and least pair margin (route A of rv_check).

Usage: python -I rv_identity.py N CERT REF [REF-KIND]  (REF-KIND: cert | witness)
"""

from __future__ import annotations

import json
import math
import sys
from fractions import Fraction as F

import yaml

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from rv_check import pair_margin, read_cert, route_a, extent  # noqa: E402


def read_witness(path):
    d = yaml.safe_load(open(path))["witness"]
    side = F(d["side"])
    sq = []
    for s in d["squares"]:
        x, y = (F(v) for v in s["center"])
        c, si = (F(v) for v in s["basis"])
        assert c * c + si * si == 1
        sq.append((x, y, c, si))
    return int(d["n"]), side, sq


def ceil12(x: F) -> str:
    q = math.ceil(x * 10**12)
    return f"{q // 10**12}.{q % 10**12:012d}"


def theta(c, s):
    a = math.degrees(math.atan2(float(s), float(c))) % 90.0
    return a - 90.0 if a > 45.0 else a


SYMS = [  # (map, det)
    (lambda x, y, S: (x, y), 1), (lambda x, y, S: (S - x, y), -1),
    (lambda x, y, S: (x, S - y), -1), (lambda x, y, S: (S - x, S - y), 1),
    (lambda x, y, S: (y, x), -1), (lambda x, y, S: (S - y, x), 1),
    (lambda x, y, S: (y, S - x), 1), (lambda x, y, S: (S - y, S - x), -1),
]


def free_play(sq, side, k):
    x, y, c, s = sq[k]
    h = extent(c, s)
    best = min(x - h, side - x - h, y - h, side - y - h)
    for j, q in enumerate(sq):
        if j == k:
            continue
        dx, dy = q[0] - x, q[1] - y
        if dx * dx + dy * dy > F(9, 4):
            continue
        m = pair_margin(sq[k], q)
        if m < best:
            best = m
    return best


def main():
    n = int(sys.argv[1])
    _, s_new, new = read_cert(sys.argv[2])
    kind = sys.argv[4] if len(sys.argv) > 4 else "witness"
    _, s_ref, ref = read_cert(sys.argv[3]) if kind == "cert" else read_witness(sys.argv[3])
    assert len(new) == len(ref) == n
    out = {"n": n, "side_new": str(s_new), "side_ref": str(s_ref)}
    diff = s_ref - s_new
    out["below_by"] = float(diff)
    out["below_by_relative"] = float(diff / s_ref)
    out["print12_new"], out["print12_ref"] = ceil12(s_new), ceil12(s_ref)
    out["same_print12"] = out["print12_new"] == out["print12_ref"]
    out["below_less_than_1e-12"] = 0 < diff < F(1, 10**12)
    fn = [(float(x), float(y), theta(c, s)) for x, y, c, s in new]
    best = None
    for si, (fmap, det) in enumerate(SYMS):
        fr = []
        for x, y, c, s in ref:
            X, Y = fmap(float(x), float(y), float(s_ref))
            th = theta(c, s) * det
            th = ((th + 45.0) % 90.0) - 45.0
            fr.append((X, Y, th))
        match, tot = [], 0.0
        for (x, y, t) in fn:
            j = min(range(n), key=lambda k: (fr[k][0] - x) ** 2 + (fr[k][1] - y) ** 2)
            d = math.hypot(fr[j][0] - x, fr[j][1] - y)
            match.append((j, d, abs(((fr[j][2] - t + 45.0) % 90.0) - 45.0)))
            tot += d
        if best is None or tot < best[0]:
            best = (tot, si, match)
    _, si, match = best
    out["symmetry"] = si
    out["one_to_one"] = len({m[0] for m in match}) == n
    out["same_index_order"] = all(m[0] == i for i, m in enumerate(match))
    out["largest_move"] = max(m[1] for m in match)
    out["largest_turn_deg"] = max(m[2] for m in match)
    for e in (1e-15, 1e-9, 1e-3):
        out[f"moved_beyond_{e:g}"] = sum(1 for m in match if m[1] > e or m[2] > e)
    moved = [i for i, m in enumerate(match) if m[1] > 1e-9 or m[2] > 1e-9]
    rows = []
    for i in moved:
        j = match[i][0]
        rows.append({"new": i, "ref": j, "move": match[i][1], "turn": match[i][2],
                     "free_play_ref": float(free_play(ref, s_ref, j)),
                     "free_play_new": float(free_play(new, s_new, i))})
    out["moved"] = rows
    out["moved_all_free_in_ref_beyond_1e-9"] = all(r["free_play_ref"] > 1e-9 for r in rows)
    out["moved_all_free_in_new_beyond_1e-9"] = all(r["free_play_new"] > 1e-9 for r in rows)
    for tag, side, sq in (("new", s_new, new), ("ref", s_ref, ref)):
        ok, w, least, where, _ = route_a(side, sq)
        out[f"{tag}_route_a"] = ok
        out[f"{tag}_walls"] = {k: float(v) for k, v in w.items()}
        out[f"{tag}_least_pair"] = float(least)
    print(json.dumps(out))


if __name__ == "__main__":
    main()
