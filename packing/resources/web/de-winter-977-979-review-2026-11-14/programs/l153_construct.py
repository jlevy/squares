"""Lane L153, after the freeze: the 332 and 409 constructions against the 297 packing.

Clean-room: written for this review, importing nothing from this repository or the
source, and reusing no code of any earlier review. It decides nothing about the bounds,
which the frozen checker decided; it compares the files exactly.

For each larger file it finds the translation (dx, dy) that carries the 297 file's
square 1 onto its square 1, tests that every one of the 297 squares maps to the same
index exactly (centre translated, edge direction equal), compares the sides
(S_n - S_297), lists the added squares (their centres and edge directions, upright or
not), and says which region of the box they fill.

Usage: l153_construct.py N297.json N332.json N409.json OUT.json
"""

from __future__ import annotations

import json
import math
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import l153_geom as G  # noqa: E402
import l153_reader as reader  # noqa: E402
from l153_check import sci  # noqa: E402


def load(path: str):
    data = reader.read(path)
    return Fraction(*data["side"]), [G.decode(s) for s in data["squares"]]


def describe_added(added: list[G.FSquare], side: Fraction) -> dict:
    upright = [s for s in added if (s[2] == 0 or s[3] == 0)]
    tilted = [s for s in added if not (s[2] == 0 or s[3] == 0)]
    xs = Counter(str(s[0]) for s in upright)
    ys = Counter(str(s[1]) for s in upright)
    out = {
        "count": len(added),
        "upright": len(upright),
        "tilted": [
            {
                "centre": [str(s[0]), str(s[1])],
                "basis": [str(s[2]), str(s[3])],
                "degrees": round(math.degrees(math.atan2(float(s[3]), float(s[2]))), 6),
                "c_minus_s": str(s[2] - s[3]),
            }
            for s in tilted
        ],
        "upright_x_values": len(xs),
        "upright_y_values": len(ys),
        "x_range": [sci(min(s[0] for s in added) - Fraction(1, 2), 12), sci(max(s[0] for s in added) + Fraction(1, 2), 12)],
        "y_range": [sci(min(s[1] for s in added) - Fraction(1, 2), 12), sci(max(s[1] for s in added) + Fraction(1, 2), 12)],
        "far_edge_equals_side": max(max(s[0], s[1]) for s in added) + Fraction(1, 2) == side,
        "upright_centre_values_not_half_integers": sorted(
            {sci(v, 8) for s in upright for v in (s[0], s[1]) if (v * 2).denominator != 1}
        ),
    }
    return out


def main(argv: list[str]) -> int:
    s297, sq297 = load(argv[1])
    report: dict = {"program": "l153_construct.py", "files": {}}
    for path in argv[2:4]:
        side, sq = load(path)
        n = len(sq)
        dx = sq[0][0] - sq297[0][0]
        dy = sq[0][1] - sq297[0][1]
        same = all(
            sq[k] == (sq297[k][0] + dx, sq297[k][1] + dy, sq297[k][2], sq297[k][3])
            for k in range(297)
        )
        added = sq[297:]
        entry = {
            "n": n,
            "translation": [str(dx), str(dy)],
            "squares_1_to_297_are_the_297_file_translated_exactly": same,
            "side_minus_297_side": str(side - s297),
            "added": describe_added(added, side),
        }
        # Where the added squares sit: below or left of the translated 297 box.
        lower = sum(1 for s in added if s[1] + Fraction(1, 2) <= dy)
        left = sum(1 for s in added if s[0] + Fraction(1, 2) <= dx)
        entry["added_below_y_dy"] = lower
        entry["added_left_of_x_dx"] = left
        entry["added_in_both"] = sum(
            1 for s in added if s[1] + Fraction(1, 2) <= dy and s[0] + Fraction(1, 2) <= dx
        )
        if n == 409:
            corner = [s for s in added if s[0] < Fraction(4) and s[1] < Fraction(4)]
            entry["corner_block"] = {
                "count": len(corner),
                "squares": [[str(v) for v in s] for s in corner],
                "extent": [
                    sci(max(s[0] for s in corner) + Fraction(1, 2), 8),
                    sci(max(s[1] for s in corner) + Fraction(1, 2), 8),
                ],
            }
            arms_x = sorted({s[0] for s in added if s[1] < 3 and s[0] > 4})
            arms_y = sorted({s[1] for s in added if s[0] < 3 and s[1] > 4})
            entry["bottom_arm"] = {
                "columns": len(arms_x),
                "x_from": sci(arms_x[0] - Fraction(1, 2), 10),
                "x_to": sci(arms_x[-1] + Fraction(1, 2), 10),
                "squares": sum(1 for s in added if s[1] < 3 and s[0] > 4),
            }
            entry["left_arm"] = {
                "rows": len(arms_y),
                "y_from": sci(arms_y[0] - Fraction(1, 2), 10),
                "y_to": sci(arms_y[-1] + Fraction(1, 2), 10),
                "squares": sum(1 for s in added if s[0] < 3 and s[1] > 4),
            }
        report["files"][str(n)] = entry
        print(n, "translation", entry["translation"], "contains the 297 exactly:", same,
              "side - S297 =", entry["side_minus_297_side"], "added", len(added))
    Path(argv[-1]).write_text(json.dumps(report, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
