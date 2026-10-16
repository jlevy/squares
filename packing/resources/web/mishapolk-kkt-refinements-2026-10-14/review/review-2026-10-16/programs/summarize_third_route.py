"""Print the third route's report as the review's tables (decides nothing, reads JSON only).

Usage: python -I summarize_third_route.py REPORT.json
"""

from __future__ import annotations

import json
import math
import sys
from decimal import Decimal
from fractions import Fraction


def sci(text: str) -> str:
    value = Fraction(text) if "/" in text or text.isdigit() else None
    if value is None:
        number = Decimal(text)
    else:
        if value == 0:
            return "0"
        number = Decimal(value.numerator) / Decimal(value.denominator)
    if number == 0:
        return "0"
    exponent = math.floor(math.log10(abs(number)))
    mantissa = number / Decimal(10) ** exponent
    return f"{float(mantissa):.4g}e{exponent}"


def main(path: str) -> int:
    report = json.load(open(path, encoding="utf-8"))
    print("command:", report["command"])
    print("started", report["started_utc"], "finished", report["finished_utc"], "wall", report["wall_seconds"])
    total_pairs = sum(row["pairs"] for row in report["rows"])
    clipped = sum(row["clipped_pairs"] for row in report["rows"])
    controls = sum(sum(row["controls"].values()) for row in report["rows"])
    of = sum(len(row["controls"]) for row in report["rows"])
    print(f"{len(report['rows'])} certificates, {total_pairs} pairs ({clipped} clipped), controls {controls}/{of}")
    for row in report["rows"]:
        print(
            f"  {row['issue']:10s} n={row['n']:3d} passed={row['passed']} wall={sci(row['wall_clearance'])}"
            f" contacts={row['wall_contacts']} dist={sci(row['least_distance'])} pairs={row['pairs']}"
            f" ({row['clipped_pairs']}) {row['wall_seconds']}s controls={sum(row['controls'].values())}/{len(row['controls'])}"
        )
    print("upstream:", report["upstream"], "sum", sum(report["upstream"].values()))
    print("receipts:")
    for name, total in report["receipts"].items():
        print("  ", name, total)
    print("arrangements:")
    for name, gap in report["arrangements"].items():
        if "unmatched" in gap:
            un = gap["unmoved"]
            print(f"  {name}: UNMATCHED; side diff {sci(gap['side_difference'])}; unmoved k={un['symmetry']} within={un['within']} one_to_one={un['one_to_one']}")
            continue
        moved = gap["moved_beyond"]
        sine = float(gap["largest_orientation_sine"])
        turn = math.degrees(math.asin(min(1.0, sine)))
        un = gap["unmoved"]
        print(
            f"  {name}: k={gap['symmetry']} moved>1e-9/1e-6/1e-3/1e-2/1e-1="
            f"{moved['1e-9']}/{moved['1e-6']}/{moved['1e-3']}/{moved['1e-2']}/{moved['1e-1']}"
            f" largest={sci(gap['largest_displacement'])} turn={turn:.3g}deg turned>1e-6={gap['turned_beyond_1e-6']}"
            f" sidediff={sci(gap['side_difference'])} | unmoved k={un['symmetry']} within={un['within']} 1:1={un['one_to_one']}"
        )
    print("problems:", len(report["problems"]))
    for problem in report["problems"]:
        print("  ", problem)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1]))
