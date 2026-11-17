"""The #938 decimal pose against #935's pose and against the certificate; decides nothing.

Reads both poses as data (center-angle, degrees, decimal) and evaluates them with mpmath at
60 digits: whether squares 1-172 are #935's pose verbatim, where the 27 grid squares sit,
and the least gap between an old square and a grid square in the pose, by separating axes.

Run: python -I -B l77_pose.py POSE_199.yaml POSE_172.yaml CANDIDATE.yaml OUT.json
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
from fractions import Fraction as F

import mpmath
import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import l77_checker as C  # noqa: E402

mpmath.mp.dps = 60


def load(p: str) -> dict:
    node = yaml.compose(open(p).read(), Loader=yaml.SafeLoader)
    return C._plain_yaml(node)["witness"]


def corners(c: list[str], a: str) -> list[tuple[mpmath.mpf, mpmath.mpf]]:
    x, y = mpmath.mpf(c[0]), mpmath.mpf(c[1])
    t = mpmath.radians(mpmath.mpf(a))
    u = (mpmath.cos(t) / 2, mpmath.sin(t) / 2)
    v = (-u[1], u[0])
    return [(x + sx * u[0] + sy * v[0], y + sx * u[1] + sy * v[1]) for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))]


def axes(cs: list) -> list[tuple[mpmath.mpf, mpmath.mpf]]:
    ex, ey = cs[1][0] - cs[0][0], cs[1][1] - cs[0][1]
    n = mpmath.sqrt(ex * ex + ey * ey)
    ex, ey = ex / n, ey / n
    return [(ex, ey), (-ey, ex)]


def gap(a: list, b: list) -> mpmath.mpf:
    best = None
    for ax, ay in axes(a) + axes(b):
        pa = [ax * x + ay * y for x, y in a]
        pb = [ax * x + ay * y for x, y in b]
        g = max(min(pb) - max(pa), min(pa) - max(pb))
        best = g if best is None or g > best else best
    return best


def main() -> int:
    p199, p172, cand, out = sys.argv[1:5]
    w = load(p199)
    v = load(p172)
    res: dict = {"program": "l77_pose.py", "program_sha256": hashlib.sha256(open(__file__, "rb").read()).hexdigest(),
                 "pose_199_sha256": hashlib.sha256(open(p199, "rb").read()).hexdigest(),
                 "pose_172_sha256": hashlib.sha256(open(p172, "rb").read()).hexdigest()}
    sq = w["squares"]
    res["n"] = len(sq)
    res["side_pose_199"] = w["side"]
    res["side_pose_172"] = v["side"]
    res["side_199_is_172_plus_1_as_decimals"] = F(w["side"]) == F(v["side"]) + 1
    res["squares_1_172_verbatim_935_pose"] = all(sq[i] == v["squares"][i] for i in range(172))
    s172 = F(v["side"])
    grid_ok = []
    for k in range(172, 199):
        e = sq[k]
        cx, cy, ang = F(e["center"][0]), F(e["center"][1]), e["angle"]
        grid_ok.append(ang == "0" and (
            (cy == s172 + F(1, 2) and cx == (k - 172) + F(1, 2)) or (cx == s172 + F(1, 2) and cy == (k - 186) + F(1, 2))))
    res["grid_at_pose_S172_and_half_integers"] = all(grid_ok)
    old = [corners(e["center"], e["angle"]) for e in sq[:172]]
    grid = [corners(e["center"], e["angle"]) for e in sq[172:]]
    gaps = []
    for i, a in enumerate(old):
        for j, b in enumerate(grid):
            g = gap(a, b)
            gaps.append((g, i + 1, 173 + j))
    gaps.sort()
    res["pose_old_grid_least_gaps"] = [[i, j, mpmath.nstr(g, 6)] for g, i, j in gaps[:6]]
    res["pose_old_grid_overlaps"] = sum(1 for g, _, _ in gaps if g < 0)
    # certificate side against the pose's
    cw = C.read_witness(cand)
    S = F(*cw["side"])
    res["pose_side_minus_certificate_side"] = float(F(w["side"]) - S)
    with open(out, "w") as fh:
        json.dump(res, fh, indent=1)
        fh.write("\n")
    print(json.dumps(res, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
