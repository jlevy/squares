"""How the five certificates' rational corners are made, measured from the files (lane L64).

Usage: python -I -B l64_construct.py STATEMENTS.json SRC_DIR OUT.json

Decides nothing about any bound; describes the certificates exactly. For each count:

- each square's edge direction u = p1 - p0 = (c, s), its half-angle tangent
  t = s / (1 + c) in lowest terms (so c = (1 - t^2)/(1 + t^2) and s = 2t/(1 + t^2)),
  and the digits of t's numerator and denominator;
- the squares exactly on the axes, nearly on them (0 < |angle| < 1e-9 rad), slightly
  off (1e-9 rad to 0.5 degree) and tilted (beyond 0.5 degree);
- whether each square's corners are its centre plus or minus (u + w)/2 and (u - w)/2;
- the wall clearances by decade, wall by wall, beside the three exact contacts;
- the pair margins of every pair below 1e-9 by separating axes (method A), by decade,
  and their least and greatest values.
"""

from __future__ import annotations

import json
import math
import sys
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import l64_sat as A  # noqa: E402
from l64_reader import read_witness  # noqa: E402
from l64_util import Clock, environment, frac_str, program_digests, sci, write_receipt  # noqa: E402

HERE = Path(__file__).resolve().parent
DECADES = [F(1, 10**k) for k in (30, 20, 16, 15, 14, 13, 12, 11, 10, 9)]


def decade(x: F) -> str:
    if x == 0:
        return "0"
    for k, d in zip((30, 20, 16, 15, 14, 13, 12, 11, 10, 9), DECADES, strict=True):
        if x < d:
            return f"<1e-{k}"
    return ">=1e-9"


def main(argv: list[str]) -> int:
    if len(argv) != 4:
        print(__doc__)
        return 2
    statements = json.loads(Path(argv[1]).read_text())["counts"]
    src, out = Path(argv[2]), argv[3]
    clock = Clock()
    rows = {}
    for n_text, st in statements.items():
        n = int(n_text)
        w = read_witness(src / st["repo"] / st["certificate"], expected_n=n)
        side = F(*w["side"])
        sqs = [A.SquareA(s["id"], s["corners"]) for s in w["squares"]]
        classes = Counter()
        t_num_digits, t_den_digits = [], []
        tiny = []
        centre_form = 0
        for sq in sqs:
            c, s = sq.u
            (x0, y0), (x1, y1), (x2, y2), (x3, y3) = sq.p
            cx, cy = (x0 + x2) / 2, (y0 + y2) / 2
            wx, wy = sq.w
            expect = [
                (cx - (c + wx) / 2, cy - (s + wy) / 2),
                (cx + (c - wx) / 2, cy + (s - wy) / 2),
                (cx + (c + wx) / 2, cy + (s + wy) / 2),
                (cx - (c - wx) / 2, cy - (s - wy) / 2),
            ]
            centre_form += expect == sq.p
            if s == 0 or c == 0:
                classes["on the axes"] += 1
                continue
            t = s / (1 + c) if c != -1 else None
            if t is not None:
                t_num_digits.append(len(str(abs(t.numerator))))
                t_den_digits.append(len(str(t.denominator)))
            ang = abs(math.atan2(float(s), float(c)))
            ang = min(ang % (math.pi / 2), math.pi / 2 - ang % (math.pi / 2))
            if ang < 1e-9:
                classes["0 < angle < 1e-9 rad"] += 1
                tiny.append(ang)
            elif math.degrees(ang) <= 0.5:
                classes["1e-9 rad to 0.5 deg"] += 1
            else:
                classes["beyond 0.5 deg"] += 1
        walls = {name: Counter() for name in ("left", "bottom", "right", "top")}
        for sq in sqs:
            for name, v in A.wall_clearances(sq, side).items():
                walls[name][decade(v)] += 1
        margins = []
        for i in range(n):
            for j in range(i + 1, n):
                m, _ = A.pair_margin(sqs[i], sqs[j])
                if m < DECADES[-1]:
                    margins.append(m)
        margins.sort()
        buckets = Counter()
        for m in margins:
            buckets["[2e-13,2.1e-13)" if m < F(21, 10**14) else "[2.1e-13,3e-13)" if m < F(3, 10**13) else "[3e-13,1e-12)" if m < F(1, 10**12) else "[1e-12,1e-9)"] += 1
        rows[n_text] = {
            "squares": n,
            "angle_classes": dict(classes),
            "tiny_angles_rad": [min(tiny), max(tiny)] if tiny else None,
            "half_angle_t_digits": {
                "numerator_max": max(t_num_digits) if t_num_digits else None,
                "denominator_max": max(t_den_digits) if t_den_digits else None,
                "denominator_min": min(t_den_digits) if t_den_digits else None,
            },
            "corners_are_centre_plus_basis_form": centre_form,
            "wall_clearance_decades": {k: dict(v) for k, v in walls.items()},
            "pairs_below_1e-9": len(margins),
            "pair_margin_buckets": dict(buckets),
            "least_margin": sci(margins[0], 12) if margins else None,
            "greatest_margin_below_1e-9": sci(margins[-1], 12) if margins else None,
            "side": frac_str(side),
        }
        print(n_text, dict(classes), "t digits", rows[n_text]["half_angle_t_digits"], "tiny", rows[n_text]["tiny_angles_rad"])
        print("   walls", {k: dict(v) for k, v in walls.items()})
        print("   margins", dict(buckets), rows[n_text]["least_margin"], rows[n_text]["greatest_margin_below_1e-9"])
    receipt = {
        "program": "l64_construct.py",
        "programs_sha256": program_digests([HERE / f for f in ("l64_construct.py", "l64_sat.py", "l64_reader.py", "l64_util.py")]),
        "environment": environment(),
        "counts": rows,
        "clock": clock.report(),
    }
    write_receipt(out, receipt)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
