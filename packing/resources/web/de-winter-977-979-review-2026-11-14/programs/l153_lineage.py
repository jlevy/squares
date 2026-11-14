"""Lane L153, after the freeze: the issue's lineage statements against T-174's witness.

Clean-room: written for this review, importing nothing from this repository or the
source, and reusing no code of any earlier review. It decides nothing about the bounds.

For the new 297 packing and for T-174's house witness it counts the upright and the
tilted squares (beyond 1 degree), the tilted squares' lean from 45 degrees (the angle reduced to
(-45, 45], then 45 - |angle|, signed by the angle), and the blocks of upright squares:
the connected components of the graph whose edges are the pairs of squares within
1 degree of upright with a margin
below 1e-9 (method A's closed form), each with its size and centroid.

Usage: l153_lineage.py NEW.json HOUSE.yaml OUT.json
"""

from __future__ import annotations

import json
import math
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))

import l153_geom as G  # noqa: E402
import l153_reader as reader  # noqa: E402
import l153_sat as A  # noqa: E402

NEAR = Fraction(1, 10**9)


def tilt(c: Fraction, s: Fraction) -> float:
    a = math.degrees(math.atan2(float(s), float(c)))
    while a <= -45:
        a += 90
    while a > 45:
        a -= 90
    return a


def analyse(sq: list[G.FSquare], side: Fraction) -> dict:
    n = len(sq)
    upright = [k for k, s in enumerate(sq) if abs(tilt(s[2], s[3])) < 1]
    exactly_upright = sum(1 for s in sq if s[2] == 0 or s[3] == 0)
    tilted = [k for k in range(n) if k not in set(upright)]
    leans = Counter()
    for k in tilted:
        a = tilt(sq[k][2], sq[k][3])
        lean = math.copysign(45 - abs(a), a)
        leans[round(lean, 3)] += 1
    prep = {k: A.prepare(G.encode(sq[k])) for k in upright}
    parent = {k: k for k in upright}

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for a_i, i in enumerate(upright):
        for j in upright[a_i + 1 :]:
            if A.margin(prep[i], prep[j]) < NEAR:
                parent[find(i)] = find(j)
    comps: dict[int, list[int]] = {}
    for k in upright:
        comps.setdefault(find(k), []).append(k)
    blocks = []
    for members in sorted(comps.values(), key=len, reverse=True):
        cx = sum(float(sq[k][0]) for k in members) / len(members)
        cy = sum(float(sq[k][1]) for k in members) / len(members)
        blocks.append(
            {
                "size": len(members),
                "centroid": [round(cx / float(side), 3), round(cy / float(side), 3)],
                "first_ids": [k + 1 for k in sorted(members)[:3]],
            }
        )
    # Lean direction along the band: the tilted squares at the commonest lean magnitude,
    # in order of x + y (the band runs along the diagonal), and the sign changes.
    magnitude = Counter(abs(v) for v in leans.elements()).most_common(1)[0][0] if leans else None
    along = sorted(
        (float(sq[k][0] + sq[k][1]), math.copysign(1, 45 - abs(tilt(sq[k][2], sq[k][3]))) * math.copysign(1, tilt(sq[k][2], sq[k][3])))
        for k in tilted
        if magnitude is not None and abs(round(45 - abs(tilt(sq[k][2], sq[k][3])), 3)) == magnitude
    )
    signs = [int(s) for _, s in along]
    runs = []
    for s in signs:
        if not runs or runs[-1][0] != s:
            runs.append([s, 0])
        runs[-1][1] += 1
    return {
        "dominant_lean_degrees": magnitude,
        "dominant_lean_runs_along_band": runs,
        "within_1_degree_of_upright": len(upright),
        "exactly_upright": exactly_upright,
        "tilted": len(tilted),
        "lean_from_45_degrees_top": leans.most_common(8),
        "lean_values": len(leans),
        "upright_blocks": blocks,
    }


def main(argv: list[str]) -> int:
    new = reader.read(argv[1])
    new_side = Fraction(*new["side"])
    new_sq = [G.decode(s) for s in new["squares"]]
    house = yaml.safe_load(Path(argv[2]).read_text())["witness"]
    h_side = Fraction(house["side"])
    h_sq = [
        (Fraction(s["center"][0]), Fraction(s["center"][1]), Fraction(s["basis"][0]), Fraction(s["basis"][1]))
        for s in house["squares"]
    ]
    out = {
        "program": "l153_lineage.py",
        "new": analyse(new_sq, new_side),
        "T-174": analyse(h_sq, h_side),
    }
    Path(argv[3]).write_text(json.dumps(out, indent=1) + "\n")
    for key in ("new", "T-174"):
        r = out[key]
        print(key, "upright", r["within_1_degree_of_upright"], "exactly", r["exactly_upright"], "tilted", r["tilted"], "leans", r["lean_from_45_degrees_top"][:6])
        print("   blocks", [(b["size"], b["centroid"]) for b in r["upright_blocks"][:8]])
        print("   lean", r["dominant_lean_degrees"], "runs along the band", r["dominant_lean_runs_along_band"])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
