"""Hand-built cases with known answers for review_t225_check.py.

Run: python -I selftest_t225.py   (from this directory or with it on the path)
Each case is a certificate text, the verdict expected, and the exact least wall
clearance and least pair gap expected. t = 1/2 gives (c, s) = (3/5, 4/5), half-extent 7/10.
"""

from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import review_t225_check as check  # noqa: E402

E = "1/1000000000000000000000000000000"  # 1e-30


def cert(side: str, rows: list[str]) -> str:
    return "# test\n" + f"{len(rows)} {side}\n" + "\n".join(rows) + "\n"


CASES = [
    # two axis-aligned squares side by side: contact, closed box touched on all walls
    ("touching pair", cert("2", ["1/2 1/2 0", "3/2 1/2 0"]), True, Fraction(0), Fraction(0)),
    # the second moved 1e-30 left: overlap by exactly 1e-30
    ("overlap 1e-30", cert("2", ["1/2 1/2 0", f"{Fraction(3, 2) - Fraction(1, 10**30)} 1/2 0"]), False, Fraction(0), Fraction(-1, 10**30)),
    # box 1e-30 too small on the right
    ("wall 1e-30", cert(str(Fraction(2) - Fraction(1, 10**30)), ["1/2 1/2 0", "3/2 1/2 0"]), False, Fraction(-1, 10**30), Fraction(0)),
    # a tilted square touching all four walls of a 7/5 box
    ("tilted in box", cert("7/5", ["7/10 7/10 1/2"]), True, Fraction(0), None),
    # a tilted square whose left corner (-7/10, -1/10) touches the right edge of the unit square
    ("tilted corner contact", cert("3", ["1/2 3/2 0", "17/10 3/2 1/2"]), True, Fraction(0), Fraction(0)),
    # ... and moved 1e-30 into it
    (
        "tilted corner overlap",
        cert("3", ["1/2 3/2 0", f"{Fraction(17, 10) - Fraction(1, 10**30)} 3/2 1/2"]),
        False,
        Fraction(0),
        Fraction(-1, 10**30),
    ),
    # a duplicated square: gap -1
    ("duplicate", cert("2", ["1/2 1/2 0", "1/2 1/2 0"]), False, Fraction(0), Fraction(-1)),
    # a negative tangent, rotated the other way, centred
    ("negative t", cert("7/5", ["7/10 7/10 -1/2"]), True, Fraction(0), None),
]

REFUSED = [
    ("float literal", cert("2", ["0.5 1/2 0"])),
    ("leading zero", cert("2", ["01/2 1/2 0"])),
    ("zero denominator", cert("2", ["1/0 1/2 0"])),
    ("short row", cert("2", ["1/2 1/2"])),
]


def main() -> int:
    bad = 0
    for name, text, verdict, wall, gap in CASES:
        n = int(text.split("\n")[1].split(" ")[0])
        r = check.decide(text, n)
        wi = Fraction(r["route_integers"]["least_wall_clearance"]["exact"])
        wf = Fraction(r["route_fraction"]["least_wall_clearance"]["exact"])
        ok = r["passed"] == verdict and r["route_integers"]["passed"] == verdict and r["route_fraction"]["passed"] == verdict
        ok = ok and wi == wall and wf == wall
        if gap is not None:
            gi = Fraction(r["route_integers"]["least_pair_gap"]["exact"])
            gf = Fraction(r["route_fraction"]["least_pair_gap"]["exact"])
            ok = ok and gi == gap and gf == gap
        if name in ("tilted corner overlap", "overlap 1e-30", "duplicate"):
            ok = ok and r["route_fraction"]["clip_positive_pairs"] == [(0, 1)]
        if name in ("touching pair", "tilted corner contact"):
            ok = ok and r["route_integers"]["contacts"] == 1 and r["route_fraction"]["contacts"] == 1
        print(f"{'ok  ' if ok else 'FAIL'} {name}: passed={r['passed']} wall={wi} gap={r['route_integers']['least_pair_gap']['exact']}")
        bad += not ok
    for name, text in REFUSED:
        try:
            check.decide(text, 1)
            print(f"FAIL {name}: read")
            bad += 1
        except check.Refused as error:
            print(f"ok   {name}: refused ({error})")
    print("selftest", "passed" if not bad else f"FAILED {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
