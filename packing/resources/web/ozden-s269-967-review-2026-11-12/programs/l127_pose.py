"""The certificate against its decimal pose, at 60 digits. Written and run after the freeze.

Lane L127, clean room; decides nothing. Usage:

    python -I -B l127_pose.py CERT.yaml TWIN.json POSE.yaml OUT.json

Reads the decimal pose (centre and angle in degrees per square) with PyYAML's safe loader,
and the certificate with this lane's reader. Measures the translation and turn between
them, the pose's own extent and side, each near pair's margin relative to the centres'
separation along the binding normal, and the tilts.
"""

from __future__ import annotations

import json
import statistics
import sys
from fractions import Fraction as F
from pathlib import Path
from typing import Any

import mpmath as mp
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))

import l127_reader as rd  # noqa: E402
import l127_sat as ma  # noqa: E402

mp.mp.dps = 60


def mpf_of(x: F) -> mp.mpf:
    return mp.mpf(x.numerator) / x.denominator


def fold(a: mp.mpf) -> mp.mpf:
    """An angle in degrees folded to (-45, 45]."""
    r = mp.fmod(a + 45, 90)
    if r <= 0:
        r += 90
    return r - 45


def main(argv: list[str]) -> int:
    cert, twin, posep, outp = (Path(a) for a in argv[1:5])
    doc = rd.read_certificate(cert.read_text(encoding="utf-8"), twin.read_text(encoding="utf-8"))
    pose = yaml.safe_load(posep.read_text(encoding="utf-8"))["witness"]
    side = F(*doc["side"])
    psq = pose["squares"]
    assert len(psq) == len(doc["squares"])
    tx, ty, turns = [], [], []
    tilts: list[tuple[int, mp.mpf, mp.mpf, mp.mpf]] = []
    pminx = pminy = mp.inf
    pmaxx = pmaxy = -mp.inf
    for k, (c, p) in enumerate(zip(doc["squares"], psq, strict=True)):
        assert p["id"] == k + 1
        pts = [(F(*x), F(*y)) for x, y in c]
        ccx = mpf_of((pts[0][0] + pts[2][0]) / 2)
        ccy = mpf_of((pts[0][1] + pts[2][1]) / 2)
        ux, uy = pts[1][0] - pts[0][0], pts[1][1] - pts[0][1]
        cang = mp.degrees(mp.atan2(mpf_of(uy), mpf_of(ux)))
        pcx, pcy = mp.mpf(p["center"][0]), mp.mpf(p["center"][1])
        pang = mp.mpf(p["angle"])
        tx.append(ccx - pcx)
        ty.append(ccy - pcy)
        turns.append(abs(fold(cang - pang)))
        tilts.append((k + 1, fold(cang), ccx, ccy))
        rad = mp.radians(pang)
        cs, sn = mp.cos(rad), mp.sin(rad)
        for lx, ly in ((-0.5, -0.5), (0.5, -0.5), (0.5, 0.5), (-0.5, 0.5)):
            x = pcx + cs * lx - sn * ly
            y = pcy + sn * lx + cs * ly
            pminx, pmaxx = min(pminx, x), max(pmaxx, x)
            pminy, pmaxy = min(pminy, y), max(pmaxy, y)
    pose_side = mp.mpf(pose["side"])
    sidef = mpf_of(side)

    # near pairs: margin over the centres' separation along the binding normal
    sq = [ma.make_square(c) for c in doc["squares"]]
    cen = [((F(*c[0][0]) + F(*c[2][0])) / 2, (F(*c[0][1]) + F(*c[2][1])) / 2) for c in doc["squares"]]
    ratios: list[float] = []
    n = len(sq)
    for i in range(n):
        for j in range(i + 1, n):
            m = ma.pair_margin(sq[i], sq[j])
            if m[0] * 10**12 >= m[1]:
                continue
            mv = F(m[0], m[1])
            dx, dy = cen[j][0] - cen[i][0], cen[j][1] - cen[i][1]
            best = None
            for s_, axis in ((sq[i], sq[i].u), (sq[i], sq[i].w), (sq[j], sq[j].u), (sq[j], sq[j].w)):
                a = (F(axis[0], s_.d), F(axis[1], s_.d))
                sep = abs(dx * a[0] + dy * a[1])
                own = sq[i] if s_ is sq[i] else sq[j]
                other = sq[j] if own is sq[i] else sq[i]
                g = ma._gap_on_axis(own, axis, own.lo_u if axis == own.u else own.lo_w, other)
                gv = F(g[0], g[1])
                if best is None or gv > best[0]:
                    best = (gv, sep)
            assert best is not None and best[0] == mv
            ratios.append(float(mv / best[1]))
    med = statistics.median(ratios)

    tilted = [(k, float(t), float(x), float(y)) for k, t, x, y in tilts if abs(t) > 0.5]
    neg = [t for t in tilted if t[1] < 0]
    clusters: dict[float, list[int]] = {}
    for k, t, _, _ in tilted:
        clusters.setdefault(round(t, 2), []).append(k)
    near_upright = [float(t) for _, t, _, _ in tilts if abs(t) <= 0.5]
    exactly_upright = [k for k, t, _, _ in tilts if t == 0]
    out: dict[str, Any] = {
        "program": "l127_pose.py",
        "translation_x": {"mean": mp.nstr(mp.fsum(tx) / n, 6), "spread": mp.nstr(max(tx) - min(tx), 3)},
        "translation_y": {"mean": mp.nstr(mp.fsum(ty) / n, 6), "spread": mp.nstr(max(ty) - min(ty), 3)},
        "largest_turn_degrees": mp.nstr(max(turns), 3),
        "pose_least_corner": [mp.nstr(pminx, 6), mp.nstr(pminy, 6)],
        "pose_side": str(pose["side"]),
        "pose_side_minus_certificate_side": mp.nstr(pose_side - sidef, 6),
        "certificate_side_minus_pose_extent_y": mp.nstr(sidef - (pmaxy - pminy), 3),
        "certificate_side_minus_pose_extent_x": mp.nstr(sidef - (pmaxx - pminx), 3),
        "pose_extent_y_minus_pose_side": mp.nstr((pmaxy - pminy) - pose_side, 3),
        "near_pair_relative_gaps": {
            "count": len(ratios),
            "least": f"{min(ratios):.4e}",
            "greatest": f"{max(ratios):.4e}",
            "median": f"{med:.4e}",
            "within_5pc_of_median": sum(1 for r in ratios if abs(r - med) <= 0.05 * med),
        },
        "tilts": {
            "beyond_0.5": len(tilted),
            "positive": sum(1 for t in tilted if t[1] > 0),
            "negative": len(neg),
            "negative_squares": [{"square": k, "tilt": round(t, 3), "centre": [round(x, 3), round(y, 3)]} for k, t, x, y in neg],
            "positive_range": [round(min(t for _, t, _, _ in tilted if t > 0), 3), round(max(t for _, t, _, _ in tilted if t > 0), 3)],
            "clusters_0.01": sorted(({"tilt": c, "count": len(v)} for c, v in clusters.items()), key=lambda d: -d["count"])[:5],
            "positive_mean": round(statistics.fmean(t for _, t, _, _ in tilted if t > 0), 3),
            "exactly_upright_squares": exactly_upright,
            "near_upright": len(near_upright),
            "near_upright_beyond_1e-3": sum(1 for t in near_upright if abs(t) > 1e-3),
            "near_upright_beyond_1e-6": sum(1 for t in near_upright if abs(t) > 1e-6),
            "near_upright_largest": round(max(abs(t) for t in near_upright), 4),
        },
    }
    outp.write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
