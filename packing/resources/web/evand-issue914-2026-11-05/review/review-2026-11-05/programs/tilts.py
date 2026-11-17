"""Tilt angles of each new packing and its house: the groups, and which angles they share.

Usage (from packing/, Python 3.14):
  python -I tilts.py CANDIDATES_DIR HOUSES_DIR OUT.json

A measurement in binary64; it decides nothing. Angles are taken modulo 90 degrees in
(-45, 45], and up to sign (the box's reflections reverse a tilt), so |angle| is compared.
A tilted square is one turned by more than 1 degree. Two packings share a tilt angle when
some tilted square of each has |angle| within 0.01 degree of the other's.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from identity import HOUSE_T, NAMES, from_cert, from_witness  # noqa: E402


def groups(a: np.ndarray) -> list[list]:
    t = np.sort(np.abs(a[np.abs(a) > 1.0]))
    out: list[list] = []
    for v in t:
        if out and v - out[-1][1] <= 0.01:
            out[-1][1] = float(v)
            out[-1][2] += 1
        else:
            out.append([float(v), float(v), 1])
    return [[round(g[0], 3), round(g[1], 3), g[2]] for g in out]


def main() -> None:
    cand, houses, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    res = {}
    for n, name in NAMES.items():
        new = from_cert(cand / f"{name}.cert")
        house = from_witness(houses / f"W-known-best-n{n}.yaml")
        an = np.abs(new["a"][np.abs(new["a"]) > 1.0])
        ah = np.abs(house["a"][np.abs(house["a"]) > 1.0])
        shared_new = int(sum(1 for v in an if np.any(np.abs(ah - v) <= 0.01)))
        shared_house = int(sum(1 for v in ah if np.any(np.abs(an - v) <= 0.01)))
        gn, gh = groups(new["a"]), groups(house["a"])
        r = {
            "house": HOUSE_T[n],
            "tilted_new": int(len(an)),
            "tilted_house": int(len(ah)),
            "new_signs": {"positive": int((new["a"] > 1).sum()), "negative": int((new["a"] < -1).sum())},
            "house_signs": {"positive": int((house["a"] > 1).sum()), "negative": int((house["a"] < -1).sum())},
            "new_groups_largest": sorted(gn, key=lambda g: -g[2])[:5],
            "house_groups_largest": sorted(gh, key=lambda g: -g[2])[:5],
            "new_range": [round(float(an.min()), 3), round(float(an.max()), 3)] if len(an) else None,
            "house_range": [round(float(ah.min()), 3), round(float(ah.max()), 3)] if len(ah) else None,
            "new_tilted_sharing_a_house_angle": shared_new,
            "house_tilted_sharing_a_new_angle": shared_house,
        }
        res[str(n)] = r
        print(n, r["house"], "tilted", r["tilted_new"], "/", r["tilted_house"], "signs", r["new_signs"], r["house_signs"],
              "range", r["new_range"], r["house_range"], "shared", shared_new, shared_house)
        print("    new groups", r["new_groups_largest"], "| house groups", r["house_groups_largest"])
    out.write_text(json.dumps(res, indent=1) + "\n")


if __name__ == "__main__":
    main()
