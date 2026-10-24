"""Self-test of capture.py's cell bound against the second exact method.

Usage: python3 -I bound_selftest.py CANDIDATE OUTPUT.json [CELLS]

For directions 0, 1, 296 and 2072 and CELLS random cells each (seeded; half-widths from
1/2^12 to 1/2^5 of the quadrant's width, some placed on the source's tightest boxes'
neighbourhoods by chance only), it computes the exact cell bound of capture.py
(Direction.exact_lb, divided by its threshold) and, by n31_brute with the unrounded
densities, the exact capture at the cell's four corners, its centre and two random
points of it. The bound is a lower bound for every centre of the cell, so it must not
exceed any of these captures; it also reports how close the bound comes to the least of
them (the slack the branch and bound has to close). Prints PASS or the first violation.
"""

from __future__ import annotations

import json
import random
import sys
import time
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import capture as cp  # noqa: E402
import n31_exact as nx  # noqa: E402


def main() -> int:
    start = time.process_time()
    cand = nx.read_candidate(Path(sys.argv[1]))
    out_path = Path(sys.argv[2])
    cells = int(sys.argv[3]) if len(sys.argv) > 3 else 6
    merged = nx.expand(cand["rectangles"], cand["L"])
    rng = random.Random(20261023)
    rows = []
    worst_gap = None
    for j in (0, 1, 296, 2072):
        d = cp.Direction(cand, merged, j, Fraction(1))
        for _ in range(cells):
            dx = rng.randint(5, 12)
            dy = dx + rng.choice((0, 0, 1)) if dx < 12 else dx
            ax = rng.randrange(2**dx)
            ay = rng.randrange(2**dy)
            px, py, hx, hy = d.cell_int(ax, dx, ay, dy)
            val = d.exact_lb(px, py, hx, hy)
            bound = None if val is None else Fraction(val, d.threshold)
            g = d.G
            pts = [(px - hx, py - hy), (px + hx, py - hy), (px - hx, py + hy),
                   (px + hx, py + hy), (px, py)]
            pts += [(px + rng.randint(-hx, hx), py + rng.randint(-hy, hy)) for _ in range(2)]
            caps = [d.point_capture(Fraction(x, g), Fraction(y, g)) for x, y in pts]
            least = min(caps)
            ok = bound is None or bound <= least
            row = {"j": j, "cell": [ax, dx, ay, dy],
                   "bound": None if bound is None else float(bound),
                   "least_capture_at_points": float(least),
                   "bound_at_most_every_capture": ok}
            if bound is not None:
                gap = least - bound
                row["gap"] = float(gap)
                worst_gap = gap if worst_gap is None or gap < worst_gap else worst_gap
            rows.append(row)
            if not ok:
                print("VIOLATION", row)
                out_path.write_text(json.dumps({"status": "FAIL", "rows": rows}, indent=1))
                return 1
    out = {"kind": "review-2026-10-23-n31-bound-selftest/v1", "status": "PASS",
           "cells": len(rows), "points_per_cell": 7,
           "least_gap": None if worst_gap is None else float(worst_gap), "rows": rows,
           "program_sha256": nx.sha256_file(Path(__file__)),
           "capture_sha256": nx.sha256_file(Path(cp.__file__)),
           "cpu_seconds": round(time.process_time() - start, 3)}
    out_path.write_text(json.dumps(out, indent=1) + "\n")
    print("PASS", len(rows), "cells", f"least gap {out['least_gap']}",
          f"cpu {out['cpu_seconds']} s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
