#!/usr/bin/env python3
"""Hand-built cases with known answers for review_0nse_check.py; decides nothing.

Usage: python -I selftest_0nse.py
"""

from __future__ import annotations

import importlib.util
import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("review_0nse_check", HERE / "review_0nse_check.py")
check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check)

E = "1/1000000000000000000000000000000"  # 1e-30
EPS = Fraction(1, 10**30)


def lit(r: Fraction) -> str:
    return f"{r.numerator}/{r.denominator}"


CASES = []

# 1-2: two axis-aligned squares side by side, touching; then overlapping by 1e-30.
CASES.append(("side by side, touching", "2 2\n1/2 1/2 0\n3/2 1/2 0\n", True, {"touching": 1, "gap": 0}))
CASES.append(
    ("side by side, 1e-30 overlap", f"2 2\n1/2 1/2 0\n{lit(Fraction(3, 2) - EPS)} 1/2 0\n", False, {"gap": -EPS})
)
# 3-4: a (3/5, 4/5) square (t = 1/2) touching all four walls; then the side 1e-30 short.
CASES.append(("t = 1/2 square in its box", "1 7/5\n7/10 7/10 1/2\n", True, {"wall": 0}))
CASES.append(("t = 1/2 square, side 1e-30 short", f"1 {lit(Fraction(7, 5) - EPS)}\n7/10 7/10 1/2\n", False, {"wall": -EPS}))
# 5-6: a tilted square's corner on an axis square's edge; then 1e-30 further in.
CASES.append(("corner on edge", "2 12/5\n1/2 3/5 0\n17/10 7/10 1/2\n", True, {"touching": 1, "gap": 0}))
CASES.append(
    ("corner 1e-30 past edge", f"2 12/5\n1/2 3/5 0\n{lit(Fraction(17, 10) - EPS)} 7/10 1/2\n", False, {"gap": -EPS})
)
# 7: a duplicated square; 8: a square outside; 9: t = 1 is a quarter turn, axis-aligned.
CASES.append(("duplicate", "2 2\n1/2 1/2 0\n1/2 1/2 0\n", False, {"gap": -1}))
CASES.append(("outside", "2 2\n1/2 1/2 0\n7/2 1/2 0\n", False, {}))
CASES.append(("t = 1 and t = -1", "2 2\n1/2 1/2 1\n3/2 1/2 -1\n", True, {"touching": 1, "gap": 0}))
# 10-14: malformed texts.
CASES.append(("decimal literal", "1 1\n0.5 1/2 0\n", False, {"format": True}))
CASES.append(("plus sign", "1 1\n+1/2 1/2 0\n", False, {"format": True}))
CASES.append(("row count", "2 2\n1/2 1/2 0\n", False, {"format": True}))
CASES.append(("zero denominator", "1 1\n1/0 1/2 0\n", False, {"format": True}))
CASES.append(("blank line", "1 1\n\n1/2 1/2 0\n", False, {"format": True}))
CASES.append(("comment then header", "# c\n1 1\n1/2 1/2 0\n", True, {}))


def main() -> int:
    bad = 0
    for name, text, expected, facts in CASES:
        result = check.decide_text(text)
        ok = result["accepted"] == expected
        if facts.get("format"):
            ok = ok and "format_error" in result
        if "route_Z" in result:
            z = result["route_Z"]
            ok = ok and result["routes_agree"]
            if "gap" in facts and result["n"] > 1:
                ok = ok and Fraction(z["least_gap"]) == facts["gap"]
            if "touching" in facts:
                ok = ok and z["touching_pairs"] == facts["touching"]
                ok = ok and result["route_C"]["touching_pairs"] == facts["touching"]
            if "wall" in facts:
                ok = ok and Fraction(z["least_wall_clearance"]) == facts["wall"]
            if not expected and "format" not in facts and "gap" in facts and facts["gap"] < 0:
                ok = ok and result["route_C"]["positive_area_pairs"] >= 1
        bad += not ok
        print(f"{'ok ' if ok else 'BAD'} {name}: accepted={result['accepted']}", end="")
        if "route_Z" in result:
            print(
                f" gap={result['route_Z']['least_gap']} wall={result['route_Z']['least_wall_clearance']}"
                f" touching={result['route_Z']['touching_pairs']}/{result['route_C']['touching_pairs']}"
                f" areas>0={result['route_C']['positive_area_pairs']}"
            )
        else:
            print(f" format_error={result.get('format_error')!r}")
    print(f"{len(CASES) - bad} of {len(CASES)} as expected")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
