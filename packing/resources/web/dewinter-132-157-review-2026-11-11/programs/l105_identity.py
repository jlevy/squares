"""Lane L105, after the freeze: the new packing at 132 against the house. Decides nothing.

Usage: python -I -B l105_identity.py SOURCE_DIR HOUSE_YAML OUT_JSON

Reads the 132 packing through the frozen reader and the house witness
(`packing/witnesses/known-best/n-132.yaml`, center-basis rational) with PyYAML, both
in binary64. Under each of the eight symmetries of the house's box, with the house's
image anchored at each corner of the new box and at the centres, it measures nearest-
centre pairing (one to one or not), and the optimal assignment of least summed move
(scipy), with the squares moved beyond 1e-3, 0.05 and 0.1 and the largest move; and
counts each packing's tilted squares.
"""

from __future__ import annotations

import json
import math
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np
import yaml
from scipy.optimize import linear_sum_assignment

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import l105_reader as R  # noqa: E402


def fl(t: str) -> float:
    return float(Fraction(t))


def house(path: Path) -> tuple[np.ndarray, float]:
    w = yaml.safe_load(path.read_text())["witness"]
    assert w["representation"] == "center-basis"
    rows = [(fl(s["center"][0]), fl(s["center"][1]), math.atan2(fl(s["basis"][1]), fl(s["basis"][0]))) for s in w["squares"]]
    return np.array(rows), fl(w["side"])


def sym(arr: np.ndarray, L: float, k: int) -> np.ndarray:
    x, y, a = arr[:, 0].copy(), arr[:, 1].copy(), arr[:, 2].copy()
    if k >= 4:
        x, a = L - x, math.pi - a
    for _ in range(k % 4):
        x, y, a = L - y, x, a + math.pi / 2
    return np.stack([x, y, a], axis=1)


def tilted(arr: np.ndarray) -> int:
    t = np.mod(np.degrees(arr[:, 2]), 90.0)
    t = np.minimum(t, 90 - t)
    return int((t > 1e-9).sum())


def main() -> None:
    src, hp, outp = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    pk = R.read_json(src / "n132" / "n132_exact.json")
    new = np.array([(x[0] / x[1], y[0] / y[1], math.atan2(s[0] / s[1], c[0] / c[1])) for x, y, c, s in pk["squares"]])
    Ln = pk["side"][0] / pk["side"][1]
    hs, Lh = house(hp)
    rows: list[dict[str, Any]] = []
    for k in range(8):
        h = sym(hs, Lh, k)
        dL = Ln - Lh
        for anchor, (ox, oy) in {"lower-left": (0, 0), "lower-right": (dL, 0), "upper-left": (0, dL), "upper-right": (dL, dL), "centre": (dL / 2, dL / 2)}.items():
            hx, hy = h[:, 0] + ox, h[:, 1] + oy
            d = np.hypot(hx[:, None] - new[None, :, 0], hy[:, None] - new[None, :, 1])
            ri, ci = linear_sum_assignment(d)
            m = d[ri, ci]
            nearest = d.argmin(axis=0)
            rows.append({
                "symmetry": k,
                "anchor": anchor,
                "summed_move": round(float(m.sum()), 4),
                "beyond_1e-3": int((m > 1e-3).sum()),
                "beyond_0.05": int((m > 0.05).sum()),
                "beyond_0.1": int((m > 0.1).sum()),
                "largest_move": round(float(m.max()), 4),
                "nearest_house_squares_distinct": int(len(set(nearest.tolist()))),
            })
    rows.sort(key=lambda r: r["summed_move"])
    out = {
        "program": "l105_identity.py",
        "house_side": Lh,
        "new_side": Ln,
        "tilted_new": tilted(new),
        "tilted_house": tilted(hs),
        "best": rows[0],
        "one_to_one_anywhere": any(r["nearest_house_squares_distinct"] == 132 for r in rows),
        "least_beyond_0.1": min(r["beyond_0.1"] for r in rows),
        "rows": rows,
    }
    outp.write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps({k: v for k, v in out.items() if k != "rows"}))


if __name__ == "__main__":
    main()
