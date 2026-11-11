"""Measure the tilted bands the issue describes. Decides nothing.

Usage: python -I -B l101_band.py SOURCE_DIR KNOWN_BEST_DIR OUT.json

In binary64 (the number-field witnesses at 70 and 207 evaluated at 50 digits first): the
tilted squares (beyond 0.5 degrees from upright) of the new packing, the house at 179,
and the packings at 70 and 207; their angles modulo 90 degrees; the line their centres
lie along and how far they stray from it. Then the seed the issue states, the 70 band
where x + y <= 16 and its copy shifted by (5, 5) where x + y > 16, under each symmetry of
the 70 box, against the new band: how many new tilted squares lie within 0.05, 0.1 and
0.25 of a seed square turned by under 1 degree from it.
"""

from __future__ import annotations

import json
import math
import sys
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.set_int_max_str_digits(0)

import mpmath  # noqa: E402
import numpy as np  # noqa: E402
import yaml  # noqa: E402

from l101_identity import SYMS, apply, fold, load_house, load_new  # noqa: E402

mpmath.mp.dps = 50


def field_loader(w: dict):
    poly = [F(str(c)) for c in w["scalar"]["minimal_polynomial"]]
    lo, hi = (F(str(v)) for v in w["scalar"]["isolating_interval"])
    found = None
    for order in ("descending", "ascending"):
        coeffs = poly if order == "descending" else list(reversed(poly))
        for r in mpmath.polyroots([mpmath.mpf(c.numerator) / c.denominator for c in coeffs],
                                  maxsteps=200, extraprec=200):
            if abs(mpmath.im(r)) < mpmath.mpf(10) ** -30:
                x = mpmath.re(r)
                if mpmath.mpf(lo.numerator) / lo.denominator <= x <= mpmath.mpf(hi.numerator) / hi.denominator:
                    found = (order, x)
    assert found is not None, "no root in the isolating interval"
    alpha = found[1]

    def value(v) -> mpmath.mpf:
        if isinstance(v, list):
            return sum(mpmath.mpf(F(str(c)).numerator) / F(str(c)).denominator * alpha**k
                       for k, c in enumerate(v))
        f = F(str(v))
        return mpmath.mpf(f.numerator) / f.denominator

    return value, found[0], alpha


def load_field_witness(path: Path):
    w = yaml.safe_load(path.read_text(encoding="utf-8"))["witness"]
    value, order, alpha = field_loader(w)
    side = value(w["side"])
    cs, angs = [], []
    for sq in w["squares"]:
        cs.append((float(value(sq["center"][0])), float(value(sq["center"][1]))))
        c, s = value(sq["basis"][0]), value(sq["basis"][1])
        angs.append(float(mpmath.degrees(mpmath.atan2(s, c))))
    return float(side), np.array(cs), np.array(angs), {"order": order, "side_50": mpmath.nstr(side, 40)}


def band(cs: np.ndarray, angs: np.ndarray) -> dict:
    tilt = np.array([fold(a) for a in angs])
    idx = np.where(np.abs(tilt) > 0.5)[0]
    pts = cs[idx]
    mean = pts.mean(axis=0)
    _, _, vt = np.linalg.svd(pts - mean)
    d = vt[0]
    direction = math.degrees(math.atan2(d[1], d[0])) % 180
    normal = np.array([-d[1], d[0]])
    off = (pts - mean) @ normal
    along = (pts - mean) @ d
    return {
        "tilted": len(idx),
        "ids": [int(i) + 1 for i in idx],
        "angles_deg": sorted(round(float(t), 4) for t in tilt[idx]),
        "line_direction_deg": round(direction, 3),
        "line_mean": [round(float(x), 4) for x in mean],
        "offsets_from_line_max": round(float(np.abs(off).max()), 4),
        "offsets_from_line_std": round(float(off.std()), 4),
        "extent_along_line": round(float(along.max() - along.min()), 4),
        "centre_x_plus_y_range": [round(float((pts[:, 0] + pts[:, 1]).min()), 4),
                                  round(float((pts[:, 0] + pts[:, 1]).max()), 4)],
        "centre_x_minus_y_range": [round(float((pts[:, 0] - pts[:, 1]).min()), 4),
                                   round(float((pts[:, 0] - pts[:, 1]).max()), 4)],
    }


def groups(angles: list[float]) -> dict:
    return {
        "at_-40.81_within_0.02": sum(1 for a in angles if abs(a + 40.81) < 0.02),
        "in_[-41.5,-41.0]": sum(1 for a in angles if -41.5 <= a <= -41.0),
        "in_[-40.0,-39.4]": sum(1 for a in angles if -40.0 <= a <= -39.4),
        "others": [a for a in angles if not (abs(a + 40.81) < 0.02 or -41.5 <= a <= -41.0 or -40.0 <= a <= -39.4)],
    }


def seed_match(new_c, new_a, s70_side, c70, a70, new_ids) -> list[dict]:
    tilt70 = np.array([abs(fold(a)) > 0.5 for a in a70])
    out = []
    for sym in SYMS:
        pts, angs = [], []
        for (x, y), a, t in zip(c70, a70, tilt70, strict=True):
            if not t:
                continue
            x2, y2, a2 = apply(sym, x, y, s70_side, a)
            if x2 + y2 <= 16:
                pts.append((x2, y2))
                angs.append(a2)
            if x2 + y2 + 10 > 16:
                pts.append((x2 + 5, y2 + 5))
                angs.append(a2)
        if not pts:
            continue
        pts = np.array(pts)
        counts = {"0.05": 0, "0.1": 0, "0.25": 0}
        for i in new_ids:
            d = np.linalg.norm(pts - new_c[i - 1], axis=1)
            for lim in counts:
                ok = [k for k in range(len(pts)) if d[k] <= float(lim)
                      and abs(fold(new_a[i - 1] - angs[k])) < 1]
                counts[lim] += bool(ok)
        out.append({"symmetry": sym, "seed_squares": len(pts), "matched": counts})
    return out


def main() -> int:
    src, kb, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    new_side, new_c, new_a = load_new(src)
    h_side, h_c, h_a = load_house(kb / "n-179.yaml")
    s70, c70, a70, info70 = load_field_witness(kb / "n-070.yaml")
    s207, c207, a207, info207 = load_field_witness(kb / "n-207.yaml")
    new_band = band(new_c, new_a)
    b207 = band(c207, a207)
    tilt207 = [(int(i) + 1, round(fold(a), 4), round(float(c207[i][0]), 3), round(float(c207[i][1]), 3))
               for i, a in enumerate(a207) if abs(fold(a)) > 0.5]
    receipt = {
        "program": "l101_band.py",
        "new": {**new_band, "groups": groups(new_band["angles_deg"]), "side": new_side},
        "house_179": {**band(h_c, h_a), "side": h_side},
        "n70": {**band(c70, a70), "side": s70, **info70},
        "n207": {**b207, "side": s207, **info207,
                 "tilted_with_centres": tilt207},
        "seed_model_vs_new_band": seed_match(new_c, new_a, s70, c70, a70, new_band["ids"]),
    }
    out.write_text(json.dumps(receipt, indent=1) + "\n", encoding="utf-8")
    for key in ("new", "house_179", "n70", "n207"):
        r = receipt[key]
        print(key, {k: r[k] for k in ("tilted", "line_direction_deg", "offsets_from_line_max", "offsets_from_line_std",
                                       "extent_along_line", "centre_x_plus_y_range", "centre_x_minus_y_range")})
        print("   angles", r["angles_deg"][:6], "...", r["angles_deg"][-4:])
    print("groups", receipt["new"]["groups"])
    print("n70", info70, "n207", info207)
    for r in receipt["seed_model_vs_new_band"]:
        print("seed", r)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
