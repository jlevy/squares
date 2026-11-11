"""Lane L109's comparison of the certificate with its decimal pose, after the freeze.

Usage: python -I -B l109_pose.py CERT.yaml TWIN.json POSE.yaml CHECK.json OUT.json

Decides nothing. Reads the decimal pose (centre and angle in degrees per square) with
PyYAML as data and evaluates it at 60 digits with mpmath; reads the certificate with the
frozen reader. Reports the pose's least corner coordinates and extents, the certificate
side against the pose's extent and its stated side, the largest centre and angle
differences after the translation that puts the pose's least corner coordinates at 0,
each near pair's margin in the pose against the certificate's exact margin, and each
near pair's margin relative to its centres' separation along the binding axis.
"""

from __future__ import annotations

import json
import os
import statistics
import sys
from fractions import Fraction as Q

import mpmath
import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import l109_axes as A  # noqa: E402
import l109_check as C  # noqa: E402
import l109_reader as R  # noqa: E402

PROGRAMS = ["l109_reader.py", "l109_axes.py", "l109_check.py", "l109_pose.py"]
mpmath.mp.dps = 60
HALF = mpmath.mpf(1) / 2


def mq(q: Q) -> mpmath.mpf:
    return mpmath.mpf(q.numerator) / q.denominator


def wrap90(a: mpmath.mpf) -> mpmath.mpf:
    return (a + 45) % 90 - 45


def pose_square(cx: mpmath.mpf, cy: mpmath.mpf, deg: mpmath.mpf) -> list[tuple[mpmath.mpf, mpmath.mpf]]:
    t = mpmath.radians(deg)
    c, s = mpmath.cos(t), mpmath.sin(t)
    return [(cx + c * x - s * y, cy + s * x + c * y) for x, y in ((-HALF, -HALF), (HALF, -HALF), (HALF, HALF), (-HALF, HALF))]


def axes(pts: list[tuple[mpmath.mpf, mpmath.mpf]]) -> list[tuple[mpmath.mpf, mpmath.mpf]]:
    ux, uy = pts[1][0] - pts[0][0], pts[1][1] - pts[0][1]
    n = mpmath.sqrt(ux * ux + uy * uy)
    ux, uy = ux / n, uy / n
    return [(ux, uy), (-uy, ux)]


def margin_and_axis(p: list[tuple[mpmath.mpf, mpmath.mpf]], q: list[tuple[mpmath.mpf, mpmath.mpf]]):
    best = None
    for ax in axes(p) + axes(q):
        a = [ax[0] * x + ax[1] * y for x, y in p]
        b = [ax[0] * x + ax[1] * y for x, y in q]
        g = max(min(b) - max(a), min(a) - max(b))
        if best is None or g > best[0]:
            best = (g, ax)
    assert best is not None
    return best


def main() -> int:
    cert, twin, pose_path, check_path, out = sys.argv[1:6]
    rd = R.read_files(cert, twin)
    side = Q(*rd.side)
    with open(pose_path, encoding="utf-8") as f:
        pw = yaml.safe_load(f)["witness"]
    with open(check_path, encoding="utf-8") as f:
        chk = json.load(f)
    assert pw["representation"] == "center-angle" and pw["coordinates"]["angle_unit"] == "degrees"
    pose = []
    for sq in pw["squares"]:
        pose.append(pose_square(mpmath.mpf(sq["center"][0]), mpmath.mpf(sq["center"][1]), mpmath.mpf(sq["angle"])))
    pose_angles = [wrap90(mpmath.mpf(sq["angle"])) for sq in pw["squares"]]
    xs = [x for p in pose for x, _ in p]
    ys = [y for p in pose for _, y in p]
    mx, my = min(xs), min(ys)
    ext_x, ext_y = max(xs) - mx, max(ys) - my
    stated = mpmath.mpf(pw["side"])
    certq = [[(Q(*x), Q(*y)) for x, y in sq] for sq in rd.corners]
    certm = [[(mq(x), mq(y)) for x, y in sq] for sq in certq]
    dc, da = mpmath.mpf(0), mpmath.mpf(0)
    for k, (p, c) in enumerate(zip(pose, certm, strict=True)):
        pcx = sum(x for x, _ in p) / 4 - mx
        pcy = sum(y for _, y in p) / 4 - my
        ccx = sum(x for x, _ in c) / 4
        ccy = sum(y for _, y in c) / 4
        dc = max(dc, abs(pcx - ccx), abs(pcy - ccy))
        ca = wrap90(mpmath.degrees(mpmath.atan2(c[1][1] - c[0][1], c[1][0] - c[0][0])))
        da = max(da, abs(wrap90(ca - pose_angles[k])))
    sqa = [A.make(c) for c in certq]
    near = chk["pairs_below_1e-12"]
    dm = mpmath.mpf(0)
    rel = []
    for i, j, _ in near:
        exact_m = A.margin(sqa[i - 1], sqa[j - 1])
        pm, ax = margin_and_axis(pose[i - 1], pose[j - 1])
        dm = max(dm, abs(pm - mq(exact_m)))
        ci = (sum(x for x, _ in pose[i - 1]) / 4, sum(y for _, y in pose[i - 1]) / 4)
        cj = (sum(x for x, _ in pose[j - 1]) / 4, sum(y for _, y in pose[j - 1]) / 4)
        sep = abs(ax[0] * (ci[0] - cj[0]) + ax[1] * (ci[1] - cj[1]))
        rel.append(float(mq(exact_m) / sep))
    pose_walls = []
    for k, p in enumerate(pose):
        pxs = [x for x, _ in p]
        pys = [y for _, y in p]
        pose_walls.append((min(min(pxs), min(pys), stated - max(pxs), stated - max(pys)), k + 1))
    pose_walls.sort()
    tilts = [abs(a) for a in pose_angles]
    receipt = {
        "program": "l109_pose.py",
        "programs_sha256": C.program_digests(PROGRAMS),
        "decides": "nothing",
        "pose_id": pw["id"],
        "pose_least_corner": [mpmath.nstr(mx, 6), mpmath.nstr(my, 6)],
        "pose_extent_x_less_cert_side": mpmath.nstr(ext_x - mq(side), 6),
        "pose_extent_y_less_cert_side": mpmath.nstr(ext_y - mq(side), 6),
        "pose_stated_side_less_cert_side": mpmath.nstr(stated - mq(side), 6),
        "pose_stated_side_less_pose_extent": mpmath.nstr(stated - max(ext_x, ext_y), 6),
        "pose_least_wall_clearance_at_stated_side": [mpmath.nstr(pose_walls[0][0], 6), pose_walls[0][1]],
        "largest_centre_difference_after_translation": mpmath.nstr(dc, 4),
        "largest_angle_difference_degrees": mpmath.nstr(da, 4),
        "near_pairs": len(near),
        "largest_near_pair_margin_difference": mpmath.nstr(dm, 4),
        "near_margin_over_axis_separation": {
            "min": f"{min(rel):.3e}",
            "median": f"{statistics.median(rel):.3e}",
            "max": f"{max(rel):.3e}",
        },
        "pose_tilts": {
            "exactly_upright": sum(1 for t in tilts if t == 0),
            "below_1e-9_degrees": sum(1 for t in tilts if 0 < t < mpmath.mpf("1e-9")),
            "between_1e-9_and_0.5": sum(1 for t in tilts if mpmath.mpf("1e-9") <= t <= mpmath.mpf("0.5")),
            "beyond_0.5": sum(1 for t in tilts if t > mpmath.mpf("0.5")),
            "beyond_1": sum(1 for t in tilts if t > 1),
        },
    }
    with open(out, "w", encoding="utf-8") as f:
        json.dump(receipt, f, indent=1)
        f.write("\n")
    print(json.dumps(receipt, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
