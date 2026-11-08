"""How the #924 point set relates to T-095's (squarepacker v1.1, Daniel's points dilated).

Written in the reconcile phase, after the blind findings were frozen.  Decides nothing
about the bound; it bears on credit and significance only.

Dilates every T-095 point by s_new / s_old about the origin (the containers share the
corner at the origin, and both are [0, s]^2) and reports, for each point of the new
certificate, the distance in coordinate units (1/D, D = 4000000 in both) to the nearest
dilated T-095 point; also the share of the new total weight on points within a few
units of an old one, and whether the old rows near x = 1 survive.

Usage: python -I lineage.py NEW_CERT OLD_CERT(.gz)
"""

import gzip
import json
import sys
from collections import Counter
from fractions import Fraction


def read(path):
    raw = open(path, "rb").read()
    if path.endswith(".gz"):
        raw = gzip.decompress(raw)
    toks = [int(t) for t in raw.split()]
    sn, sd, d, w, m = toks[:5]
    body = toks[5:]
    pts = [tuple(body[3 * i : 3 * i + 3]) for i in range(m)]
    return Fraction(sn, sd), d, w, pts


def main():
    s_new, d_new, w_new, new = read(sys.argv[1])
    s_old, d_old, w_old, old = read(sys.argv[2])
    assert d_new == d_old
    lam = s_new / s_old
    dil = [(Fraction(x) * lam, Fraction(y) * lam, wt) for x, y, wt in old]
    cell = 2000
    grid = {}
    for i, (x, y, _) in enumerate(dil):
        grid.setdefault((int(x) // cell, int(y) // cell), []).append(i)

    def nearest(x, y):
        best = None
        cx, cy = x // cell, y // cell
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for i in grid.get((cx + dx, cy + dy), ()):
                    ox, oy, _ = dil[i]
                    dist = max(abs(ox - x), abs(oy - y))
                    if best is None or dist < best[0]:
                        best = (dist, i)
        return best

    bands = Counter()
    weight_near = 0
    matched_old = set()
    for x, y, wt in new:
        b = nearest(x, y)
        dist = float(b[0]) if b else None
        if dist is None or dist > cell:
            bands["> 2000 units"] += 1
            continue
        for lim in (1, 10, 100, 1000, 2000):
            if dist <= lim:
                bands[f"<= {lim} units"] += 1
                break
        if dist <= 10:
            weight_near += wt
            matched_old.add(b[1])
    # rows near x = 1: T-095 had 112 points on x = (141/560) s_old
    alpha_new = Fraction(141, 560) * s_new * d_new
    row_new = sum(1 for x, _, _ in new if abs(x - alpha_new) <= 50)
    xs = Counter(x for x, _, _ in new)
    out = {
        "new": {"side": str(s_new), "points": len(new), "W": w_new},
        "old": {"side": str(s_old), "points": len(old), "W": w_old},
        "dilation": str(lam),
        "new_points_by_distance_to_nearest_dilated_old_point": dict(bands),
        "old_points_matched_within_10_units": len(matched_old),
        "share_of_new_total_weight_on_points_within_10_units": float(Fraction(weight_near, sum(p[2] for p in new))),
        "alpha_new_D_units": float(alpha_new),
        "new_points_within_50_units_of_x_eq_alpha_new": row_new,
        "most_common_x_values": xs.most_common(6),
    }
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
