"""Lane L117, after the freeze: the certificate against its decimal pose, its relative gaps
and its tilts. Decides nothing.

Reads the certificate (frozen reader) and the decimal pose n-269-decimal-pose.yaml as
data (centre and angle in degrees per square). Measures at 60 digits: the translation
from pose to certificate and its spread over the squares, each square's turn between
them, the pose's side less the certificate's, the pose's extents; for every pair below
1e-12, its relative gap rho, the margin over the centres' separation along the binding
normal (l117_geom's closed form); and the tilt of each square with its clusters.

Usage: python -I -B l117_pose.py CERT.yaml TWIN.json POSE.yaml OUT.json
"""

from __future__ import annotations

import json
import os
import sys
from fractions import Fraction as F

import mpmath
import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import l117_check as ck  # noqa: E402
import l117_geom as g  # noqa: E402
import l117_reader as rd  # noqa: E402

mpmath.mp.dps = 60


def mpf(x: F) -> mpmath.mpf:
    return mpmath.mpf(x.numerator) / x.denominator


def tilt_deg(u: g.Pt) -> float:
    """Angle of edge direction u, reduced to (-45, 45] degrees."""
    a = mpmath.degrees(mpmath.atan2(mpf(u[1]), mpf(u[0])))
    while a > 45:
        a -= 90
    while a <= -45:
        a += 90
    return float(a)


def main(argv: list[str]) -> int:
    ypath, jpath, ppath, opath = argv[1:5]
    rec = rd.read_files(ypath, jpath)
    side = rec["side"]
    sq = rec["squares"]
    assert isinstance(side, tuple) and isinstance(sq, list)
    S = F(side[0], side[1])
    pts = [g.from_rat(c) for c in sq]
    n = len(pts)
    with open(ppath, encoding="utf-8") as fh:
        pose = yaml.safe_load(fh)["witness"]
    pside = mpmath.mpf(pose["side"])
    pc = [(mpmath.mpf(s["center"][0]), mpmath.mpf(s["center"][1])) for s in pose["squares"]]
    pa = [mpmath.mpf(s["angle"]) for s in pose["squares"]]
    assert len(pc) == n

    # translation and turn, pose to certificate
    tx, ty, turns = [], [], []
    for k in range(n):
        c, u, _ = g.pose(pts[k])
        tx.append(mpf(c[0]) - pc[k][0])
        ty.append(mpf(c[1]) - pc[k][1])
        th = mpmath.radians(pa[k])
        d = mpmath.atan2(mpf(u[1]) * mpmath.cos(th) - mpf(u[0]) * mpmath.sin(th),
                         mpf(u[0]) * mpmath.cos(th) + mpf(u[1]) * mpmath.sin(th))
        q = mpmath.pi / 2
        d = d - q * mpmath.nint(d / q)
        turns.append(abs(d))
    # pose corners and extents
    xs, ys = [], []
    for k in range(n):
        th = mpmath.radians(pa[k])
        cx, cy = pc[k]
        for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
            xs.append(cx + (sx * mpmath.cos(th) - sy * mpmath.sin(th)) / 2)
            ys.append(cy + (sx * mpmath.sin(th) + sy * mpmath.cos(th)) / 2)
    ext_x = max(xs) - min(xs)
    ext_y = max(ys) - min(ys)

    # relative gaps of the near pairs
    rows = []
    for i in range(n):
        for j in range(i + 1, n):
            terms = g.axes_terms(pts[i], pts[j])
            m = max(ad - h for ad, h in terms)
            if m < F(1, 10**12):
                ad = max(ad for ad, h in terms if ad - h == m)
                rows.append((m / ad, i + 1, j + 1))
    rows.sort()
    rhos = [r for r, _, _ in rows]
    med = rhos[len(rhos) // 2]
    within5 = sum(1 for r in rhos if abs(r - med) <= med / 20)

    # tilts
    tilts = [tilt_deg(g.pose(p)[1]) for p in pts]
    beyond05 = [(round(t, 4), k + 1) for k, t in enumerate(tilts) if abs(t) > 0.5]
    beyond1 = [t for t in tilts if abs(t) > 1]
    clusters: dict[str, list[int]] = {}
    for t, k in beyond05:
        clusters.setdefault(f"{t:.2f}", []).append(k)
    top = sorted(clusters.items(), key=lambda kv: -len(kv[1]))[:8]
    exactly_upright = sum(1 for p in pts if g.pose(p)[1][1] == 0 or g.pose(p)[1][0] == 0)

    out = {
        "program": "l117_pose.py",
        "pose_side": pose["side"],
        "pose_side_less_certificate_side": mpmath.nstr(pside - mpf(S), 6),
        "pose_least_corner": [mpmath.nstr(min(xs), 6), mpmath.nstr(min(ys), 6)],
        "translation_mean": [mpmath.nstr(sum(tx) / n, 15), mpmath.nstr(sum(ty) / n, 15)],
        "translation_spread": [mpmath.nstr(max(tx) - min(tx), 3), mpmath.nstr(max(ty) - min(ty), 3)],
        "largest_turn_degrees": mpmath.nstr(mpmath.degrees(max(turns)), 3),
        "certificate_side_less_pose_extent": {"y": mpmath.nstr(mpf(S) - ext_y, 3), "x": mpmath.nstr(mpf(S) - ext_x, 3)},
        "near_pairs": len(rows),
        "rho_min": [rows[0][1], rows[0][2], ck.sci(rows[0][0], 5)],
        "rho_max": [rows[-1][1], rows[-1][2], ck.sci(rows[-1][0], 5)],
        "rho_median": ck.sci(med, 5),
        "rho_within_5pct_of_median": within5,
        "tilted_beyond_0.5_degrees": len(beyond05),
        "tilted_beyond_1_degree": len(beyond1),
        "tilted_positive_beyond_0.5": sum(1 for t, _ in beyond05 if t > 0),
        "tilted_negative_beyond_0.5": sum(1 for t, _ in beyond05 if t < 0),
        "exactly_upright": exactly_upright,
        "largest_tilt_clusters_0.01_degree": [[a, len(ks), ks] for a, ks in top],
        "tilts_beyond_0.5": sorted(beyond05),
    }
    with open(opath, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1)
        fh.write("\n")
    for k, v in out.items():
        if k != "tilts_beyond_0.5":
            print(k, v)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
