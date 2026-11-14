"""Lane L159's comparison of the certificate with its decimal pose: decides nothing.

Written after the findings were frozen, for the stage 4 review of issue #983. It reads
the certificate through the reader, the decimal pose `n-228-decimal-pose.yaml` (centres
and angles in degrees) and the search record `hit-n228-114-0.txt` as data, and works at
60 digits with mpmath: the translation and turn from pose to certificate, the pose's
extents against both sides, the pose's own least pair margin over the certificate's
near pairs and its least wall margin, and each near pair's margin relative to the
separation of the centres along the binding normal.

Usage: l159_pose.py CERT.yaml TWIN.json POSE.yaml HIT.txt OUT.json
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import mpmath  # noqa: E402
import yaml  # noqa: E402
from mpmath import mp, mpf  # noqa: E402

import l159_geom as geom  # noqa: E402
from l159_reader import read_paths  # noqa: E402

mp.dps = 60
Loader = getattr(yaml, "CSafeLoader", yaml.SafeLoader)


def q(x: Fraction) -> mpf:
    return mpf(x.numerator) / mpf(x.denominator)


def fold(deg: mpf) -> mpf:
    while deg > 45:
        deg -= 90
    while deg <= -45:
        deg += 90
    return deg


def frame(theta_deg: mpf) -> tuple[tuple[mpf, mpf], tuple[mpf, mpf]]:
    t = mpmath.radians(theta_deg)
    c, s = mpmath.cos(t), mpmath.sin(t)
    return (c, s), (-s, c)


def closed_margin(ca, ua, wa, cb, ub, wb) -> tuple[mpf, mpf]:
    """Margin and |offset . binding normal| from centres and frames."""
    d = (cb[0] - ca[0], cb[1] - ca[1])
    best = None
    for n, (u, w) in ((ua, (ub, wb)), (wa, (ub, wb)), (ub, (ua, wa)), (wb, (ua, wa))):
        r = abs(d[0] * n[0] + d[1] * n[1])
        h = (abs(n[0] * u[0] + n[1] * u[1]) + abs(n[0] * w[0] + n[1] * w[1])) / 2
        g = r - mpf(1) / 2 - h
        if best is None or g > best[0]:
            best = (g, r)
    return best  # type: ignore[return-value]


def s6(x: mpf) -> str:
    return mpmath.nstr(x, 6, min_fixed=0, max_fixed=0)


def main(argv: list[str]) -> int:
    cert, twin, pose_path, hit_path, out_path = (Path(a) for a in argv[1:6])
    w = read_paths(cert, twin)
    side = Fraction(*w.side)
    pw = yaml.load(pose_path.read_text(encoding="utf-8"), Loader=Loader)["witness"]
    assert pw["representation"] == "center-angle" and pw["coordinates"]["angle_unit"] == "degrees"
    pose_side = mpf(pw["side"])
    out: dict[str, object] = {"program": "l159_pose.py", "pose_id": pw["id"], "pose_n": pw["n"], "pose_side": pw["side"]}
    cert_frames = [geom.centre_frame(c) for c in w.squares]
    pose = []
    dx, dy, turns = [], [], []
    for sq, (cc, cu, _) in zip(pw["squares"], cert_frames, strict=True):
        pc = (mpf(sq["center"][0]), mpf(sq["center"][1]))
        th = mpf(sq["angle"])
        u, v = frame(th)
        pose.append((pc, u, v))
        dx.append(q(cc[0]) - pc[0])
        dy.append(q(cc[1]) - pc[1])
        tc = mpmath.degrees(mpmath.atan2(q(cu[1]), q(cu[0])))
        turns.append(abs(fold(tc - th)))
    out["translation_x"] = {"min": s6(min(dx)), "max": s6(max(dx)), "spread": s6(max(dx) - min(dx))}
    out["translation_y"] = {"min": s6(min(dy)), "max": s6(max(dy)), "spread": s6(max(dy) - min(dy))}
    out["largest_turn_degrees"] = s6(max(turns))
    xs, ys = [], []
    for pc, u, v in pose:
        for a in (-1, 1):
            for b in (-1, 1):
                xs.append(pc[0] + (a * u[0] + b * v[0]) / 2)
                ys.append(pc[1] + (a * u[1] + b * v[1]) / 2)
    out["pose_least_corner"] = [s6(min(xs)), s6(min(ys))]
    out["pose_extent_x"] = s6(max(xs) - min(xs))
    out["pose_side_less_extent_x"] = s6(pose_side - (max(xs) - min(xs)))
    out["pose_side_less_extent_y"] = s6(pose_side - (max(ys) - min(ys)))
    out["certificate_side_less_pose_extent_x"] = s6(q(side) - (max(xs) - min(xs)))
    out["certificate_side_less_pose_extent_y"] = s6(q(side) - (max(ys) - min(ys)))
    out["pose_side_less_certificate_side"] = s6(pose_side - q(side))
    # Pose wall margins at its own side.
    walls = []
    for k, (pc, u, v) in enumerate(pose, start=1):
        cx = [pc[0] + (a * u[0] + b * v[0]) / 2 for a in (-1, 1) for b in (-1, 1)]
        cy = [pc[1] + (a * u[1] + b * v[1]) / 2 for a in (-1, 1) for b in (-1, 1)]
        walls += [(min(cx), k, "left"), (min(cy), k, "bottom"), (pose_side - max(cx), k, "right"), (pose_side - max(cy), k, "top")]
    least_wall = min(walls)
    out["pose_least_wall_margin"] = [s6(least_wall[0]), least_wall[1], least_wall[2]]
    # Pose pair margins over the certificate's pairs below 1e-3, and relative gaps.
    check = json.loads((out_path.parent / "check-n228.json").read_text(encoding="utf-8"))
    pose_margins = []
    for i, j, _ in check["near_pairs"]:
        (ci, ui, vi), (cj, uj, vj) = pose[i - 1], pose[j - 1]
        g, _ = closed_margin(ci, ui, vi, cj, uj, vj)
        pose_margins.append((g, i, j))
    pm = min(pose_margins)
    out["pose_least_pair_margin_over_near_pairs"] = [s6(pm[0]), pm[1], pm[2]]
    rel = []
    for i, j, _ in check["near_pairs"]:
        ca, ua, wa = cert_frames[i - 1]
        cb, ub, wb = cert_frames[j - 1]
        terms = geom.axis_terms(ca, ua, wa, cb, ub, wb)
        g, r = max(terms)
        if g < Fraction(1, 10**12):
            rel.append(g / r)
    rel.sort()
    med = rel[len(rel) // 2]
    out["relative_gap_near_pairs"] = {
        "count": len(rel),
        "min": geom.sci(rel[0], 6),
        "max": geom.sci(rel[-1], 6),
        "median": geom.sci(med, 6),
        "within_5_percent_of_median": sum(1 for x in rel if abs(x - med) <= med / 20),
    }
    # The search record against the pose, in binary64.
    lines = [ln.split() for ln in hit_path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    rows = lines[1:]
    same = sum(
        1
        for row, sq in zip(rows, pw["squares"], strict=True)
        if float(row[0]) == float(sq["center"][0]) and float(row[1]) == float(sq["center"][1]) and float(row[2]) == float(sq["angle"])
    )
    out["hit_header"] = " ".join(lines[0])
    out["hit_rows"] = len(rows)
    out["hit_rows_equal_pose_in_binary64"] = same
    out["hit_side_binary64_equals_pose_side"] = float(lines[0][1]) == float(pw["side"])
    out_path.write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    for key, value in out.items():
        print(key, value)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
