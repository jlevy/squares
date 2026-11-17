"""Lane L105, after the freeze: the construction statements. Decides no packing.

Usage: python -I -B l105_construct.py SOURCE_DIR OUT_JSON

For each folder, from the exact JSON through the frozen reader:
- tilt counts: axis-aligned squares ((c, s) a quarter turn of (1, 0)) and tilted ones,
  with the tilts' angles modulo 90 degrees, exact-distinct and clustered;
- the opening of the near pairs: margin / |a.d| on the binding axis, which is the same
  epsilon for every pair when the certificate is a uniform scaling by 1 + epsilon of a
  configuration whose near pairs touch;
- the wall structure: which squares lie within 1e-50 of a wall, and their tilt;
- incidences within 1e-50: a corner of one square on an edge segment of another (both
  ways, every near pair), and a corner on a wall; to set beside the README's 1,407 and
  2,024 contact equations.
"""

from __future__ import annotations

import json
import math
import sys
from fractions import Fraction as F
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import l105_check as K  # noqa: E402
import l105_reader as R  # noqa: E402
import l105_sat as A  # noqa: E402

TOL = F(1, 10**50)
HALF = F(1, 2)


def quarter_normal(c: F, s: F) -> tuple[F, F]:
    """The quarter turn of (c, s) with c > 0 and s >= 0."""
    for _ in range(4):
        if c > 0 and s >= 0:
            return c, s
        c, s = -s, c
    raise AssertionError((c, s))


def corners(q: A.SquareA) -> list[tuple[F, F]]:
    out = []
    for a, b in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
        out.append((q.x + a * q.c / 2 - b * q.s / 2, q.y + a * q.s / 2 + b * q.c / 2))
    return out


def incidences(p_sq: A.SquareA, e_sq: A.SquareA) -> int:
    """Corners of p_sq lying within TOL of an edge segment of e_sq."""
    count = 0
    u = (e_sq.c, e_sq.s)
    v = (-e_sq.s, e_sq.c)
    for px, py in corners(p_sq):
        dx, dy = px - e_sq.x, py - e_sq.y
        pu, pv = dx * u[0] + dy * u[1], dx * v[0] + dy * v[1]
        for normal, tang in ((pu, pv), (pv, pu)):
            if abs(abs(normal) - HALF) < TOL and abs(tang) <= HALF + TOL:
                count += 1
    return count


def run(src: Path, n: int) -> dict[str, Any]:
    pk = R.read_json(src / f"n{n}" / f"n{n}_exact.json")
    S = A.frac(pk["side"])
    sq = [A.build(s) for s in pk["squares"]]
    axis = [k + 1 for k, q in enumerate(sq) if q.c == 0 or q.s == 0]
    tilted = [k + 1 for k, q in enumerate(sq) if not (q.c == 0 or q.s == 0)]
    angles = {}
    for k in tilted:
        c, s = quarter_normal(sq[k - 1].c, sq[k - 1].s)
        angles[k] = (c, s, math.degrees(math.atan2(float(s), float(c))))
    exact_distinct = len({(c, s) for c, s, _ in angles.values()})
    # cluster the angles (degrees, modulo 90) by gaps above 1e-6 degree
    vals = sorted(a for _, _, a in angles.values())
    clusters: list[list[float]] = []
    for a in vals:
        if clusters and a - clusters[-1][-1] < 1e-6:
            clusters[-1].append(a)
        else:
            clusters.append([a])
    # as signed tilts in (-45, 45]
    signed = sorted(((a - 90) if a > 45 else a) for a in vals)
    # near pairs and the opening ratio
    ratios = []
    inc_pairs = 0
    near = 0
    pair_kinds = {"both_axis_aligned": 0, "one_tilted": 0, "both_tilted": 0}
    for i in range(n):
        for j in range(i + 1, n):
            m, ax = A.margin(sq[i], sq[j])
            if m >= TOL:
                continue
            near += 1
            a = [(sq[i].c, sq[i].s), (-sq[i].s, sq[i].c), (sq[j].c, sq[j].s), (-sq[j].s, sq[j].c)][ax]
            d = abs(a[0] * (sq[j].x - sq[i].x) + a[1] * (sq[j].y - sq[i].y))
            ratios.append(m / d)
            inc_pairs += incidences(sq[i], sq[j]) + incidences(sq[j], sq[i])
            ti, tj = (i + 1) in tilted, (j + 1) in tilted
            pair_kinds["both_tilted" if ti and tj else "one_tilted" if ti or tj else "both_axis_aligned"] += 1
    eps = F(1, 10**60)
    dev = [r - eps for r in ratios]
    # walls
    wall_rows = []
    inc_walls = 0
    for k, q in enumerate(sq, start=1):
        cl = A.clearances(q, S)
        for w, c in zip(("left", "bottom", "right", "top"), cl, strict=True):
            if c < TOL:
                wall_rows.append({"square": k, "wall": w, "tilted": k in tilted, "clearance_sci": K.sci(c, 8)})
        for px, py in corners(q):
            for val in (px, py, S - px, S - py):
                if abs(val) < TOL:
                    inc_walls += 1
    tilted_at_walls = sorted({r["square"] for r in wall_rows if r["tilted"]})
    # Exact spread inside each angle cluster: the largest |sin| of an angle difference.
    spreads = []
    for cl in clusters:
        members = [(c, s) for c, s, ang in angles.values() if cl[0] <= ang <= cl[-1]]
        worst = max((abs(s1 * c2 - c1 * s2) for c1, s1 in members for c2, s2 in members), default=F(0))
        spreads.append(K.sci(worst, 3))
    # The side above the configuration scaled back by 1 + eps, under the model
    # cert = (1 + eps) sol + (t, t): t from an axis-aligned square at the left wall
    # (clearance = eps/2 + t when the solution touches), the solution's side from an
    # axis-aligned square at the right wall (S_sol = x_sol + 1/2).
    eps = F(1, 10**60)
    left = [r for r in wall_rows if r["wall"] == "left" and not r["tilted"]]
    right = [r for r in wall_rows if r["wall"] == "right" and not r["tilted"]]
    model = None
    if left and right:
        kl = left[0]["square"]
        tl = A.clearances(sq[kl - 1], S)[0] - eps / 2
        kr = min(right, key=lambda r: A.clearances(sq[r["square"] - 1], S)[2])["square"]
        x_sol = (sq[kr - 1].x - tl) / (1 + eps)
        s_sol = x_sol + HALF
        model = {
            "left_square": kl,
            "t_sci": K.sci(tl, 6),
            "right_square": kr,
            "side_above_solution_sci": K.sci(S - s_sol, 6),
            "eps_times_side_plus_half_sci": K.sci(eps * (S + HALF), 6),
        }
    return {
        "n": n,
        "axis_aligned": len(axis),
        "tilted": len(tilted),
        "tilted_squares": tilted,
        "tilt_angles_mod90_exact_distinct": exact_distinct,
        "tilt_angle_clusters_deg": [
            {"count": len(c), "min": round(min(c), 9), "max": round(max(c), 9)} for c in clusters
        ],
        "tilt_cluster_exact_spread_sin": spreads,
        "side_above_scaled_back_configuration": model,
        "signed_tilt_range_deg": [round(signed[0], 6), round(signed[-1], 6)] if signed else None,
        "tilt_angle_range_mod90_deg": [round(vals[0], 6), round(vals[-1], 6)] if vals else None,
        "near_pairs_below_1e-50": near,
        "near_pair_kinds": pair_kinds,
        "opening_ratio_minus_1e-60": {"min_sci": K.sci(min(dev), 4), "max_sci": K.sci(max(dev), 4)},
        "squares_within_1e-50_of_a_wall": wall_rows,
        "tilted_squares_at_walls": tilted_at_walls,
        "incidences_corner_on_edge_segment": inc_pairs,
        "incidences_corner_on_wall": inc_walls,
        "incidences_total": inc_pairs + inc_walls,
        "unknowns_3n_plus_1": 3 * n + 1,
    }


def main() -> None:
    sys.set_int_max_str_digits(0)
    src, outp = Path(sys.argv[1]), Path(sys.argv[2])
    out = {"program": "l105_construct.py", "counts": {str(n): run(src, n) for n in (132, 157)}}
    outp.write_text(json.dumps(out, indent=1) + "\n")
    for n, r in out["counts"].items():
        brief = {k: v for k, v in r.items() if k not in ("tilted_squares", "squares_within_1e-50_of_a_wall")}
        print(n, json.dumps(brief))


if __name__ == "__main__":
    main()
