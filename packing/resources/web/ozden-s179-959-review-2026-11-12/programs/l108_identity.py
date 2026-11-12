"""The certificate pose by pose against the house (T-174) and #954's packing.

Lane L108, blind stage 4 review of jlevy/squares#959. Written after the findings were
frozen; decides nothing. Binary64 is enough here: the thresholds are 1e-3 and up.
Each reference is placed under the eight symmetries of its own box, anchored at each
corner of the new box (the named corner of the reference's box on that of the new box)
and at the centres. For each placement: nearest centres (how many distinct reference
squares they reach) and SciPy's optimal assignment of least summed move; the moves
beyond 1e-3, 0.05 and 0.1, the largest, and the turns beyond 1 degree.

Usage: python -I -B l108_identity.py CERT.yaml REF_NAME REF.yaml [REF_NAME REF.yaml ...] OUT.json
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from typing import Any

import numpy as np
from scipy.optimize import linear_sum_assignment

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import l108_s70 as s70m  # noqa: E402  (the symmetry table and angle normalisation)
import l108_wit as wit  # noqa: E402

ANCHORS = ("lower-left", "lower-right", "upper-left", "upper-right", "centred")


def norm(d: float) -> float:
    while d > 45:
        d -= 90
    while d <= -45:
        d += 90
    return d


def placements(ref: wit.Packing, big: float) -> list[tuple[str, str, np.ndarray, np.ndarray]]:
    out = []
    off = big - float(ref.side)
    for k in range(8):
        pts = [s70m.sym(k, p.cx, p.cy, p.deg, ref.side) for p in ref.poses]
        xy = np.array([[float(x), float(y)] for x, y, _d in pts])
        deg = np.array([norm(float(d)) for _x, _y, d in pts])
        for anchor in ANCHORS:
            if anchor == "centred":
                shift = np.array([off / 2, off / 2])
            else:
                shift = np.array([off if "right" in anchor else 0.0, off if "upper" in anchor else 0.0])
            out.append((s70m.SYM_NAMES[k], anchor, xy + shift, deg))
    return out


def measure(new_xy: np.ndarray, new_deg: np.ndarray, ref_xy: np.ndarray, ref_deg: np.ndarray) -> dict[str, Any]:
    diff = new_xy[:, None, :] - ref_xy[None, :, :]
    dist = np.sqrt((diff**2).sum(axis=2))
    nearest = dist.argmin(axis=1)
    rows, cols = linear_sum_assignment(dist)
    moves = dist[rows, cols]
    turns = np.array([abs(norm(float(new_deg[i] - ref_deg[j]))) for i, j in zip(rows, cols, strict=True)])
    return {
        "summed_move": round(float(moves.sum()), 3),
        "beyond_1e-3": int((moves > 1e-3).sum()),
        "beyond_0.05": int((moves > 0.05).sum()),
        "beyond_0.1": int((moves > 0.1).sum()),
        "largest_move": round(float(moves.max()), 4),
        "turned_beyond_1_deg": int((turns > 1).sum()),
        "largest_turn_deg": round(float(turns.max()), 2),
        "nearest_distinct": len(set(nearest.tolist())),
    }


def main(argv: list[str]) -> int:
    cert = wit.load(Path(argv[1]), "certificate")
    new_xy = np.array([[float(p.cx), float(p.cy)] for p in cert.poses])
    new_deg = np.array([norm(float(p.deg)) for p in cert.poses])
    out: dict[str, Any] = {"program": "l108_identity.py", "new_tilted_beyond_0.5": int((np.abs(new_deg) > 0.5).sum()), "new_tilted_beyond_1": int((np.abs(new_deg) > 1).sum())}
    args = argv[2:-1]
    for name, path in zip(args[0::2], args[1::2], strict=True):
        ref = wit.load(Path(path), name)
        rows = []
        for sym_name, anchor, xy, deg in placements(ref, float(cert.side)):
            rows.append({"symmetry": sym_name, "anchor": anchor, **measure(new_xy, new_deg, xy, deg)})
        rows.sort(key=lambda r: r["summed_move"])
        ref_deg = np.array([norm(float(p.deg)) for p in ref.poses])
        out[name] = {
            "side": float(ref.side),
            "tilted_beyond_0.5": int((np.abs(ref_deg) > 0.5).sum()),
            "tilted_beyond_1": int((np.abs(ref_deg) > 1).sum()),
            "best_symmetry_at_each_anchor": [min((r for r in rows if r["anchor"] == a), key=lambda r: r["summed_move"]) for a in ANCHORS],
            "any_placement_nearest_one_to_one": any(r["nearest_distinct"] == cert.n for r in rows),
            "least_summed_move_overall": rows[0],
        }
    Path(argv[-1]).write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
