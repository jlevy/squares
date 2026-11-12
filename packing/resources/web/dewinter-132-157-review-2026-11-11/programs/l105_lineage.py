"""Lane L105, after the freeze: the cut-and-fill lineage 109 -> 132 -> 157.

Usage: python -I -B l105_lineage.py SEED_CSV SOURCE_DIR OUT_JSON

Decides nothing; measures in binary64. Reads the seed's n = 109 rows (id, n,
square_id, x, y, angle in radians) from Samanyu-dev/squares_in_squares@53551d7's
`best_fit_101_500.csv`, and the 132 and 157 packings from their exact JSON through
the frozen reader.

A growth step, as the READMEs state it: cut along one vertical line x = a and one
horizontal line y = b, move the parts about one unit apart, fill each gap with one
layer of squares, and re-optimize. For a parent of side L and a child of side L', the
four parts move by (0, 0), (D, 0), (0, D) and (D, D) with D = L' - L. Under each of
the eight symmetries of the parent's box, each parent square takes the shift that
brings it nearest a child square; the optimal assignment (least summed distance) then
pairs parent and child squares. The step is as stated when, under some symmetry, every
parent square pairs within a small move, the squares that took a horizontal shift are
separated from the others by a vertical line (and likewise for vertical shifts), and
the unpaired child squares lie in the two gaps.
"""

from __future__ import annotations

import csv
import json
import math
import sys
from pathlib import Path
from typing import Any

import numpy as np
from scipy.optimize import linear_sum_assignment

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import l105_reader as R  # noqa: E402


def seed_rows(path: Path, n: int) -> np.ndarray:
    rows = []
    with path.open(newline="") as fh:
        for r in csv.DictReader(fh):
            if int(r["n"]) == n:
                rows.append((float(r["x"]), float(r["y"]), float(r["angle"])))
    return np.array(rows)


def child_rows(src: Path, n: int) -> tuple[np.ndarray, float]:
    pk = R.read_json(src / f"n{n}" / f"n{n}_exact.json")
    out = []
    for (x, y, c, s) in pk["squares"]:
        fx, fy = x[0] / x[1], y[0] / y[1]
        fc, fs = c[0] / c[1], s[0] / s[1]
        out.append((fx, fy, math.atan2(fs, fc)))
    return np.array(out), pk["side"][0] / pk["side"][1]


def extent(arr: np.ndarray) -> float:
    lo, hi = math.inf, -math.inf
    for x, y, a in arr:
        h = (abs(math.cos(a)) + abs(math.sin(a))) / 2
        lo = min(lo, x - h, y - h)
        hi = max(hi, x + h, y + h)
    return hi - lo


def sym(arr: np.ndarray, L: float, k: int) -> np.ndarray:
    """The k-th symmetry of the box [0, L]^2: k = 4 * reflect + quarter turns."""
    x, y, a = arr[:, 0].copy(), arr[:, 1].copy(), arr[:, 2].copy()
    if k >= 4:
        x = L - x
        a = math.pi - a
    for _ in range(k % 4):
        x, y = L - y, x
        a = a + math.pi / 2
    return np.stack([x, y, a], axis=1)


def tilt_mod90(a: np.ndarray) -> np.ndarray:
    t = np.mod(np.degrees(a), 90.0)
    return np.where(t > 45, t - 90, t)


def candidates(v: np.ndarray) -> list[float]:
    """Cut positions: midpoints between consecutive distinct centre coordinates."""
    u = np.unique(np.round(v, 6))
    return [float((u[i] + u[i + 1]) / 2) for i in range(len(u) - 1)]


def assign(shifted: np.ndarray, child: np.ndarray) -> tuple[float, np.ndarray, np.ndarray, np.ndarray]:
    d = np.hypot(shifted[:, 0:1] - child[None, :, 0], shifted[:, 1:2] - child[None, :, 1])
    ri, ci = linear_sum_assignment(d)
    return float(d[ri, ci].sum()), ri, ci, d[ri, ci]


def step(parent: np.ndarray, Lp: float, child: np.ndarray, Lc: float) -> dict[str, Any]:
    """Search the symmetry and the two cut lines; shift the four parts; assign."""
    D = Lc - Lp
    best: dict[str, Any] | None = None
    for k in range(8):
        p = sym(parent, Lp, k)
        cand = []
        for a in candidates(p[:, 0]):
            for b in candidates(p[:, 1]):
                sh = p.copy()
                sh[:, 0] += D * (p[:, 0] > a)
                sh[:, 1] += D * (p[:, 1] > b)
                d = np.hypot(sh[:, 0:1] - child[None, :, 0], sh[:, 1:2] - child[None, :, 1])
                cand.append((float(d.min(axis=1).sum()), a, b))
        cand.sort()
        for _, a, b in cand[:25]:
            sh = p.copy()
            sh[:, 0] += D * (p[:, 0] > a)
            sh[:, 1] += D * (p[:, 1] > b)
            total, ri, ci, d = assign(sh, child)
            if best is None or total < best["total"]:
                best = {"k": k, "a": a, "b": b, "total": total, "ri": ri, "ci": ci, "d": d, "p": p}
    assert best is not None
    p, ri, ci, d, a, b = best["p"], best["ri"], best["ci"], best["d"], best["a"], best["b"]
    turned = np.abs(tilt_mod90(p[ri][:, 2]) - tilt_mod90(child[ci][:, 2]))
    turned = np.minimum(turned, 90 - turned)
    unpaired = sorted(set(range(len(child))) - set(ci.tolist()))
    gx, gy = a + D / 2, b + D / 2
    filler = []
    for u in unpaired:
        x, y, ang = child[u]
        filler.append({
            "square": u + 1,
            "x": round(float(x), 4),
            "y": round(float(y), 4),
            "dx_from_vertical_gap_centre": round(float(x - gx), 4),
            "dy_from_horizontal_gap_centre": round(float(y - gy), 4),
            "tilt_deg": round(float(tilt_mod90(np.array([ang]))[0]), 3),
        })
    in_v = [f for f in filler if abs(f["dx_from_vertical_gap_centre"]) < 0.5]
    in_h = [f for f in filler if abs(f["dy_from_horizontal_gap_centre"]) < 0.5]
    quad = {"lower-left": 0, "lower-right": 0, "upper-left": 0, "upper-right": 0}
    for x, y, _ in p:
        quad[("upper-" if y > b else "lower-") + ("right" if x > a else "left")] += 1
    counts = {f"beyond_{t}": int((d > t).sum()) for t in (1e-6, 1e-3, 1e-2, 5e-2, 1e-1)}
    return {
        "parent_side": Lp,
        "child_side": Lc,
        "D": D,
        "symmetry": best["k"],
        "cut_x_in_parent": a,
        "cut_y_in_parent": b,
        "parent_squares_per_part": quad,
        "paired": int(len(ri)),
        "summed_move": round(best["total"], 6),
        "largest_move": round(float(d.max()), 6),
        "median_move": round(float(np.median(d)), 8),
        "moves": counts,
        "largest_turn_deg": round(float(turned.max()), 6),
        "turned_beyond_1deg": int((turned > 1).sum()),
        "unpaired_child_squares": len(unpaired),
        "unpaired_in_vertical_gap": len(in_v),
        "unpaired_in_horizontal_gap": len(in_h),
        "unpaired_in_both": len([f for f in in_v if f in in_h]),
        "unpaired_in_neither": len([f for f in filler if f not in in_v and f not in in_h]),
        "unpaired_tilted": sum(1 for f in filler if abs(f["tilt_deg"]) > 1e-6),
        "unpaired_axis_aligned": sum(1 for f in filler if abs(f["tilt_deg"]) <= 1e-6),
        "unpaired_axis_aligned_within_0.7_of_a_gap_line": sum(
            1
            for f in filler
            if abs(f["tilt_deg"]) <= 1e-6
            and min(abs(f["dx_from_vertical_gap_centre"]), abs(f["dy_from_horizontal_gap_centre"])) <= 0.7
        ),
        "filler": filler,
    }


def main() -> None:
    seed_csv, src, outp = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    s109 = seed_rows(seed_csv, 109)
    L109 = extent(s109)
    c132, L132 = child_rows(src, 132)
    c157, L157 = child_rows(src, 157)
    tilt = lambda arr: int((np.abs(tilt_mod90(arr[:, 2])) > 1e-9).sum())  # noqa: E731
    out = {
        "program": "l105_lineage.py",
        "seed": {"n": len(s109), "extent": L109, "tilted": tilt(s109), "tilt_range_deg": [float(tilt_mod90(s109[:, 2]).min()), float(tilt_mod90(s109[:, 2]).max())]},
        "step_109_132": step(s109, L109, c132, L132),
        "step_132_157": step(c132, L132, c157, L157),
        "direct_109_157": step(s109, L109, c157, L157),
    }
    outp.write_text(json.dumps(out, indent=1) + "\n")
    print("seed", out["seed"])
    for k in ("step_109_132", "step_132_157", "direct_109_157"):
        print(k, json.dumps({kk: v for kk, v in out[k].items() if kk != "filler"}))


if __name__ == "__main__":
    main()
