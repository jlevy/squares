"""Which squares of E1c's packing lie within 1e-40 of each wall (lane r127b2-1118).

Written on 18 November 2026, after the findings' freeze and after review A of PR #1028,
whose A2 found that the review's F3 gives half the cause of E1p's failure at #1020.
Decides nothing. Usage, from this packet's directory or anywhere:

    python -I -B rb127_e1p_walls.py PIN RECEIPTS OUT.json

``PIN`` holds ``NNNN/n127_exact.json`` for NNNN = 1015, 1017 and 1020, the centre files
at the three pins; ``RECEIPTS`` is this packet's ``out/``, from which each
``e1p-restated-NNNN.json`` is read for comparison.

For each centre file it builds E1c's packing as ``rb127_controls.py`` does (every square
moved by the least left and bottom clearances, the side ``X`` the larger extent) and
lists, in exact rationals, the squares touching the right and the top wall, the squares
whose right or top clearance is below 1e-40, and the larger extent less the smaller.
E1p lowers the side to ``X - 1e-40``, so the squares within 1e-40 of either wall are the
ones that cross. The frozen rule named only the squares touching the wall of the larger
extent. It reads the files through ``json`` and ``fractions`` alone and imports no other
program of this packet.
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction as Fr
from pathlib import Path

STEP = Fr(1, 10**40)


def sci(x: Fr) -> str:
    """A short print of an exact value; a description only."""
    return "0" if x == 0 else f"{float(x):.7e}"


def walls(path: Path) -> dict[str, object]:
    data = json.loads(path.read_bytes())
    rows = [[Fr(v) for v in row] for row in data["squares"]]
    half = [(abs(c) + abs(s)) / 2 for (_, _, c, s) in rows]
    lo_x = [x - h for (x, _, _, _), h in zip(rows, half, strict=True)]
    hi_x = [x + h for (x, _, _, _), h in zip(rows, half, strict=True)]
    lo_y = [y - h for (_, y, _, _), h in zip(rows, half, strict=True)]
    hi_y = [y + h for (_, y, _, _), h in zip(rows, half, strict=True)]
    left, bottom = min(lo_x), min(lo_y)
    width, height = max(hi_x) - left, max(hi_y) - bottom
    side = max(width, height)
    right_clear = [side - (h - left) for h in hi_x]
    top_clear = [side - (h - bottom) for h in hi_y]
    n = len(rows)
    right = [k + 1 for k in range(n) if right_clear[k] < STEP]
    top = [k + 1 for k in range(n) if top_clear[k] < STEP]
    return {
        "width_less_height": str(width - height),
        "width_less_height_sci": sci(width - height),
        "larger_extent": "width" if width > height else "height" if height > width else "both",
        "touching_right": [k + 1 for k in range(n) if right_clear[k] == 0],
        "touching_top": [k + 1 for k in range(n) if top_clear[k] == 0],
        "right_within_step": right,
        "top_within_step": top,
        "within_step": sorted(set(right) | set(top)),
        "at_both_walls": sorted(set(right) & set(top)),
    }


def main(argv: list[str]) -> int:
    if len(argv) != 4:
        print(__doc__)
        return 2
    pin, receipts, out = Path(argv[1]), Path(argv[2]), Path(argv[3])
    report: dict[str, object] = {"program": "rb127_e1p_walls.py", "step": "1e-40"}
    for label in ("1015", "1017", "1020"):
        entry = walls(pin / label / "n127_exact.json")
        restated = json.loads((receipts / f"e1p-restated-{label}.json").read_bytes())
        entry["equals_e1p_restated_crossing"] = entry["within_step"] == restated["crossing"]
        report[label] = entry
        print(
            label,
            "right:", entry["right_within_step"],
            "top:", entry["top_within_step"],
            "equals the restated crossing:", entry["equals_e1p_restated_crossing"],
        )
    out.write_text(json.dumps(report, indent=1) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
