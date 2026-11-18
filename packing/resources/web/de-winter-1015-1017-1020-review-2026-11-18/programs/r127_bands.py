"""Describe the near pairs and near walls of each certificate, and check the issues'
stated numbers; it decides nothing.

Lane r127-1118.  Written after the checker was frozen and before the findings were
frozen; it uses the frozen readers and method A, and prints exact values truncated.

    python -I -B r127_bands.py LABEL=FILE [LABEL=FILE ...] --out OUT.json
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # -I drops the script dir

import argparse
import json
from fractions import Fraction

import r127_axes as A
import r127_decide as D
import r127_read as R

E = Fraction


def bands(p) -> dict:
    sq = [A.prepare(c) for c in p.corners]
    n = len(sq)
    ms = sorted((A.margin(sq[i], sq[j]), i + 1, j + 1) for i in range(n) for j in range(i + 1, n))
    # the near band: every pair below 1e-9; its least, largest and median; the next pair
    near = [m for m in ms if m[0] < E(1, 10**9)]
    nxt = ms[len(near)] if len(near) < len(ms) else None
    out = {"pairs": len(ms), "below_1e-9": len(near)}
    if near:
        out.update({
            "least": [D.sci(near[0][0]), near[0][1], near[0][2]],
            "second": [D.sci(near[1][0]), near[1][1], near[1][2]] if len(near) > 1 else None,
            "largest_in_band": [D.sci(near[-1][0]), near[-1][1], near[-1][2]],
            "median_in_band": D.sci(near[len(near) // 2][0]),
            "distinct_values_in_band": len({m[0] for m in near}),
        })
    if nxt:
        out["next_after_band"] = [D.sci(nxt[0]), nxt[1], nxt[2]]
    decades = {}
    for m, _, _ in near:
        k = 0
        while m < E(1, 10 ** (k + 1)):
            k += 1
        decades[f"[1e-{k + 1}, 1e-{k})"] = decades.get(f"[1e-{k + 1}, 1e-{k})", 0) + 1
    out["band_by_decade"] = decades
    walls = []
    for i, s in enumerate(sq):
        for k, c in enumerate(A.walls(s, p.side)):
            if c < E(1, 10**9):
                walls.append((c, i + 1, D.WALLS[k]))
    walls.sort()
    out["walls_below_1e-9"] = [[D.sci(c), i, w] for c, i, w in walls]
    return out


def issue_numbers(sides: dict) -> dict:
    """The arithmetic of the issues' stated comparisons, exactly."""
    s15, s17, s20, t305 = sides["#1015"], sides["#1017"], sides["#1020"], sides["T-305"]
    kag15 = E("11.800793726618")  # #1015: Cvetkovic's Kaggle value as #1015 states it
    kag = E("11.800793726617185")  # #1017 and #1020 state it so
    page = E("11.8017538904864874")  # the case page's print of T-305 the issues quote
    return {
        "#1015: claim 11.800795682214 less Kaggle 11.800793726618 (issue: 0.0000020)":
            D.sci(E("11.800795682214") - kag15),
        "#1015: case page 11.8017538904864874 less claim (issue: gain 0.00096)":
            D.sci(page - E("11.800795682214")),
        "#1017: Kaggle 11.800793726617185 less exact side (issue: 2.04e-12)": D.sci(kag - s17),
        "#1017: case page less exact side (issue: gain 0.00096)": D.sci(page - s17),
        "#1020: Kaggle 11.800793726617185 less exact side (issue: 2.2e-12)": D.sci(kag - s20),
        "#1020: case page less claim 11.800793726615 (issue: gain 0.00096)":
            D.sci(page - E("11.800793726615")),
        "case page print of T-305 less T-305's exact side": D.sci(page - t305),
        "T-305 to 16 places, rounded up": D.dec(-((-t305 * 10**16).__floor__()) / E(10**16), 16),
        "#1015 exact side less Kaggle 11.800793726618": D.sci(s15 - kag15),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("inputs", nargs="+")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    res: dict = {"program": "r127_bands.py", "decides": "nothing", "packings": {}}
    sides = {}
    for spec in a.inputs:
        label, path = spec.split("=", 1)
        p = R.read_path(path)
        sides[label] = p.side
        res["packings"][label] = {"file": path, **bands(p)}
        print(label, json.dumps(res["packings"][label])[:900])
    res["issue_numbers"] = issue_numbers(sides)
    for k, v in res["issue_numbers"].items():
        print(f"  {k}: {v}")
    json.dump(res, open(a.out, "w"), indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
