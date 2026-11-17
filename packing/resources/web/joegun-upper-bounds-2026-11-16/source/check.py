"""An exact checker for a Witness/v2 file with rational corners. Written apart from jlevy/squares' code; needs only pyyaml.

python3 check.py n-127-candidate.yaml [...]   ->  VALID or INVALID per file, exit 1 on any INVALID

In Fraction arithmetic, with no tolerance and no distance filter, it decides that
- every square is a unit square: four corners in order, each edge of squared length 1, adjacent edges perpendicular;
- every corner lies in [0, side] x [0, side];
- every two squares have disjoint interiors: one of the four edge directions of the pair separates them
  (the projections may touch, they may not overlap). For two convex polygons that test is exact.
"""
import sys
from fractions import Fraction as F
from itertools import combinations

import yaml


def check(path):
    w = yaml.safe_load(open(path))["witness"]
    assert w["representation"] == "corners" and w["scalar"]["kind"] == "rational" and F(str(w["square_size"])) == 1
    side, sq = F(str(w["side"])), [[(F(str(x)), F(str(y))) for x, y in s["corners"]] for s in w["squares"]]
    bad = []
    if len(sq) != w["n"]:
        bad.append(f"{len(sq)} squares, n is {w['n']}")
    axes = []
    for i, c in enumerate(sq):
        e = [(c[(k + 1) % 4][0] - c[k][0], c[(k + 1) % 4][1] - c[k][1]) for k in range(4)]
        if len(c) != 4 or any(x * x + y * y != 1 for x, y in e) or any(e[k][0] * e[k + 1][0] + e[k][1] * e[k + 1][1] != 0 for k in range(3)):
            bad.append(f"square {i + 1} is not a unit square")
        if any(not (0 <= x <= side and 0 <= y <= side) for x, y in c):
            bad.append(f"square {i + 1} leaves the box")
        axes.append(e[:2])
    for i, j in combinations(range(len(sq)), 2):
        for ax, ay in axes[i] + axes[j]:
            a, b = [x * ax + y * ay for x, y in sq[i]], [x * ax + y * ay for x, y in sq[j]]
            if max(a) <= min(b) or max(b) <= min(a):
                break
        else:
            bad.append(f"squares {i + 1} and {j + 1} overlap")
    print(f"{'INVALID' if bad else 'VALID'} {path}: n {w['n']}, side {float(side):.15f} (exact {side.numerator.bit_length()}-bit over {side.denominator.bit_length()}-bit), "
          f"{len(sq) * (len(sq) - 1) // 2} pairs, exact rational" + "".join(f"\n  {b}" for b in bad[:10]))
    return not bad


if __name__ == "__main__":
    sys.exit(0 if all([check(p) for p in sys.argv[1:]]) else 1)
