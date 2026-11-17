"""Lane L109's band measure, written after the findings were frozen.

Usage: python -I -B l109_band.py CERT.yaml TWIN.json HOUSE.yaml N070.yaml OUT.json

Decides nothing. Measures the tilted squares (beyond 0.5 degree from upright) of the new
packing, of the house at 237, and of the registry's n = 70 packing, whose number-field
witness it evaluates at 60 digits (the root found by bisection in the stated isolating
interval; the minimal polynomial read highest power first and each scalar as
coefficients of ascending powers, a reading held to the case record's side). For each
it reports the angles modulo 90 degrees, and the line through the tilted centres with
the centres' spread about it.

It then builds the seed the issue states: the 70 packing's tilted squares reflected in
the anti-diagonal of its box at shift (0, 0), and reflected in the main diagonal at
shift (7, 7). The issue says both copies were then rotated rigidly "to a lean of 2.0
degrees" and does not say about which point, so the measure scans rotations of each copy
from -3 to +3 degrees in steps of 0.05 degree about three pivots (the copy's centroid,
the origin, the box centre) and reports, unrotated and at the best rotation, how many
new tilted squares lie within 0.05, 0.1 and 0.25 of a seed square. Last, it fits each
copy by a rigid motion to the new tilted centres (nearest points, from the stated
placement), and reports the fitted rotation and translation.
"""

from __future__ import annotations

import json
import math
import os
import sys
from fractions import Fraction as Q

import mpmath
import numpy as np
import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import l109_check as C  # noqa: E402
import l109_reader as R  # noqa: E402

PROGRAMS = ["l109_reader.py", "l109_check.py", "l109_band.py"]
mpmath.mp.dps = 60


def wrap90(a: float) -> float:
    return (a + 45.0) % 90.0 - 45.0


def new_packing(cert: str, twin: str) -> tuple[float, list[tuple[float, float, float]]]:
    rd = R.read_files(cert, twin)
    out = []
    for sq in rd.corners:
        pts = [(Q(*x), Q(*y)) for x, y in sq]
        cx = float(sum((p[0] for p in pts), Q(0)) / 4)
        cy = float(sum((p[1] for p in pts), Q(0)) / 4)
        ux, uy = float(pts[1][0] - pts[0][0]), float(pts[1][1] - pts[0][1])
        out.append((cx, cy, wrap90(math.degrees(math.atan2(uy, ux)))))
    return float(Q(*rd.side)), out


def house(path: str) -> tuple[float, list[tuple[float, float, float]]]:
    with open(path, encoding="utf-8") as f:
        w = yaml.safe_load(f)["witness"]
    out = []
    for sq in w["squares"]:
        c, s = float(Q(sq["basis"][0])), float(Q(sq["basis"][1]))
        out.append((float(Q(sq["center"][0])), float(Q(sq["center"][1])), wrap90(math.degrees(math.atan2(s, c)))))
    return float(Q(w["side"])), out


def numberfield(path: str) -> tuple[float, list[tuple[float, float, float]], str]:
    with open(path, encoding="utf-8") as f:
        w = yaml.safe_load(f)["witness"]
    sc = w["scalar"]
    poly = [mpmath.mpf(Q(c).numerator) / Q(c).denominator for c in sc["minimal_polynomial"]]
    lo = mpmath.mpf(Q(sc["isolating_interval"][0]).numerator) / Q(sc["isolating_interval"][0]).denominator
    hi = mpmath.mpf(Q(sc["isolating_interval"][1]).numerator) / Q(sc["isolating_interval"][1]).denominator

    def p(x: mpmath.mpf) -> mpmath.mpf:
        return mpmath.polyval(poly, x)  # highest power first

    flo = p(lo)
    for _ in range(400):
        mid = (lo + hi) / 2
        fm = p(mid)
        if (fm < 0) == (flo < 0):
            lo, flo = mid, fm
        else:
            hi = mid
    alpha = (lo + hi) / 2

    def ev(v: object) -> mpmath.mpf:
        if isinstance(v, list):
            return mpmath.fsum((mpmath.mpf(Q(c).numerator) / Q(c).denominator) * alpha**k for k, c in enumerate(v))
        q = Q(str(v))
        return mpmath.mpf(q.numerator) / q.denominator

    side = ev(w["side"])
    out = []
    for sq in w["squares"]:
        cx, cy = ev(sq["center"][0]), ev(sq["center"][1])
        c, s = ev(sq["basis"][0]), ev(sq["basis"][1])
        out.append((float(cx), float(cy), wrap90(float(mpmath.degrees(mpmath.atan2(s, c))))))
    return float(side), out, mpmath.nstr(side, 25)


def line_fit(pts: list[tuple[float, float, float]]) -> dict[str, object]:
    if len(pts) < 2:
        return {}
    xy = np.array([(p[0], p[1]) for p in pts])
    c = xy.mean(axis=0)
    u, s, vt = np.linalg.svd(xy - c)
    d = vt[0]
    ang = math.degrees(math.atan2(d[1], d[0])) % 180
    resid = (xy - c) @ vt[1]
    return {
        "direction_degrees": round(ang, 2),
        "spread_about_line_std": round(float(resid.std()), 3),
        "x_plus_y": [round(float((xy[:, 0] + xy[:, 1]).min()), 2), round(float((xy[:, 0] + xy[:, 1]).max()), 2)],
        "x_minus_y": [round(float((xy[:, 0] - xy[:, 1]).min()), 2), round(float((xy[:, 0] - xy[:, 1]).max()), 2)],
    }


def tilted(pts: list[tuple[float, float, float]]) -> list[tuple[float, float, float]]:
    return [p for p in pts if abs(p[2]) > 0.5]


def angle_summary(pts: list[tuple[float, float, float]]) -> dict[str, object]:
    a = sorted(round(p[2], 4) for p in pts)
    return {"count": len(a), "min": a[0] if a else None, "max": a[-1] if a else None, "positive": sum(1 for v in a if v > 0)}


def rotate(xy: np.ndarray, deg: float, pivot: np.ndarray) -> np.ndarray:
    t = math.radians(deg)
    r = np.array([[math.cos(t), -math.sin(t)], [math.sin(t), math.cos(t)]])
    return (xy - pivot) @ r.T + pivot


def match(new_xy: np.ndarray, seed_xy: np.ndarray) -> dict[str, int]:
    d = np.sqrt(((new_xy[:, None, :] - seed_xy[None, :, :]) ** 2).sum(axis=2)).min(axis=1)
    return {"within_0.05": int((d < 0.05).sum()), "within_0.1": int((d < 0.1).sum()), "within_0.25": int((d < 0.25).sum())}


def icp(src: np.ndarray, dst: np.ndarray, rounds: int = 50) -> dict[str, object]:
    """Fit src to its nearest points of dst by a rigid motion, from the stated placement."""
    cur = src.copy()
    total_r = np.eye(2)
    total_t = np.zeros(2)
    for _ in range(rounds):
        d = np.sqrt(((cur[:, None, :] - dst[None, :, :]) ** 2).sum(axis=2))
        j = d.argmin(axis=1)
        keep = d[np.arange(len(cur)), j] < 0.5
        if keep.sum() < 3:
            break
        a, b = cur[keep], dst[j[keep]]
        ca, cb = a.mean(axis=0), b.mean(axis=0)
        h = (a - ca).T @ (b - cb)
        u, _, vt = np.linalg.svd(h)
        r = vt.T @ u.T
        if np.linalg.det(r) < 0:
            vt[1] *= -1
            r = vt.T @ u.T
        t = cb - r @ ca
        cur = cur @ r.T + t
        total_r = r @ total_r
        total_t = r @ total_t + t
    d = np.sqrt(((cur[:, None, :] - dst[None, :, :]) ** 2).sum(axis=2)).min(axis=1)
    return {
        "rotation_degrees": round(math.degrees(math.atan2(total_r[1, 0], total_r[0, 0])), 3),
        "translation": [round(float(total_t[0]), 3), round(float(total_t[1]), 3)],
        "seed_squares_within_0.05": int((d < 0.05).sum()),
        "seed_squares_within_0.1": int((d < 0.1).sum()),
        "seed_squares_within_0.25": int((d < 0.25).sum()),
        "seed_squares": int(len(src)),
    }


def main() -> int:
    cert, twin, house_path, n070_path, out = sys.argv[1:6]
    S, newp = new_packing(cert, twin)
    Lh, hp = house(house_path)
    L70, p70, side70 = numberfield(n070_path)
    nt, ht, t70 = tilted(newp), tilted(hp), tilted(p70)
    # the seed: copy A reflected in the anti-diagonal, shift (0, 0); copy B in the main diagonal, shift (7, 7)
    a_xy = np.array([(L70 - y, L70 - x) for x, y, _ in t70])
    b_xy = np.array([(y + 7.0, x + 7.0) for x, y, _ in t70])
    seed_angle = sorted({round(wrap90(-p[2]), 4) for p in t70})
    new_xy = np.array([(p[0], p[1]) for p in nt])
    unrot = match(new_xy, np.vstack([a_xy, b_xy]))
    best: dict[str, object] = {}
    for pivot_name in ("copy centroid", "origin", "box centre"):
        top = None
        for ka in range(-60, 61):
            for kb in range(-60, 61):
                da, db = ka * 0.05, kb * 0.05
                if pivot_name == "copy centroid":
                    pa, pb = a_xy.mean(axis=0), b_xy.mean(axis=0)
                elif pivot_name == "origin":
                    pa = pb = np.array([0.0, 0.0])
                else:
                    pa = pb = np.array([S / 2, S / 2])
                seed = np.vstack([rotate(a_xy, da, pa), rotate(b_xy, db, pb)])
                m = match(new_xy, seed)
                key = (m["within_0.1"], m["within_0.05"], m["within_0.25"])
                if top is None or key > top[0]:
                    top = (key, {"rotation_a_degrees": round(da, 2), "rotation_b_degrees": round(db, 2), **m})
        assert top is not None
        best[pivot_name] = top[1]
    receipt = {
        "program": "l109_band.py",
        "programs_sha256": C.program_digests(PROGRAMS),
        "decides": "nothing",
        "n070": {"side_60_digits": side70, "tilted": angle_summary(t70), "line": line_fit(t70)},
        "new_237": {"tilted": angle_summary(nt), "line": line_fit(nt)},
        "house_237": {"tilted": angle_summary(ht), "line": line_fit(ht)},
        "seed": {
            "squares": int(len(a_xy) + len(b_xy)),
            "angles_after_reflection": seed_angle,
            "copy_a_x_plus_y": [round(float(a_xy.sum(axis=1).min()), 2), round(float(a_xy.sum(axis=1).max()), 2)],
            "copy_b_x_plus_y": [round(float(b_xy.sum(axis=1).min()), 2), round(float(b_xy.sum(axis=1).max()), 2)],
            "unrotated": unrot,
            "copy_a_unrotated": match(new_xy, a_xy),
            "copy_b_unrotated": match(new_xy, b_xy),
            "copy_a_rigid_fit": icp(a_xy, new_xy),
            "copy_b_rigid_fit": icp(b_xy, new_xy),
            "best_rotation_by_pivot": best,
        },
    }
    with open(out, "w", encoding="utf-8") as f:
        json.dump(receipt, f, indent=1)
        f.write("\n")
    print(json.dumps(receipt, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
