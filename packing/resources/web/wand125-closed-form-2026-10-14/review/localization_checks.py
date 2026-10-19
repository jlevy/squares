#!/usr/bin/env python3
"""The inequalities that SPEC.md asserts in prose and no program of the source checks.

The localization of SPEC.md section 2.3 reduces every closed unit square in the container
[0, k + delta]^2, k >= 7, 0 < delta <= 1, to a square whose centre lies in one of four
checked regions, or inside the Lebesgue part U. Its steps rest on numerical inequalities
that validate_family.py leaves to the specification ("the localization inequalities are
in SPEC.md section 2.3"). This program decides each of them in exact rational arithmetic,
with r = 7072/10000 as the source's bound on the half-width of a unit square and
W = 2 + delta, R = 2, alpha = 9/5:

 1. a/2 + r < a - W for every k >= 7 and 0 < delta <= 1 (the top-left corner is out of
    reach), and the source's remark that k = 6 fails it for delta above about 0.586;
 2. a/2 + r < a - 2 (the lower-right corner) and a/2 + r < a - 9/5 (the far edges of U);
 3. in step (3), the shifted square with centre coordinate in [2.71, 3.71] stays strictly
    between the corner boundary 2 and the far end of the wall's periodic range, and
    inside the range of U, on both walls;
 4. every square whose centre lies in the left, straddle or top region stays inside
    [0, 24/5]^2, where the structure check establishes global = local, and every square of
    the right region stays, in original coordinates, inside the first three bottom-wall
    periods, right of the left wall and below the far edge of U;
 5. for each interval, the four regions cover [0, 19/5 + delta] x [0, 19/5] in original
    coordinates for every delta in [d0, d1], and the remainders of steps (3a) and (3b)
    land in a checked region;
 6. the u-range [-13/32, 7/16] of the published root grids covers 90 degrees:
    a_u + b_u + a_u b_u >= 1 with a_u = 13/32, b_u = 7/16;
 7. the half-width bound hmax of section 5.1: on |u| <= 2/5 the half-width (c + |s|)/2
    is nondecreasing in |u|, so its maximum over a one-sided interval is at the endpoint
    of largest |u|, and 7072/10000 exceeds sqrt(2)/2;
 8. the window identity's premise a - 9/5 >= 24/5 for every k >= 7;
 9. alpha_i <= 1.7496 for every certified line, so T_i is increasing for k >= 7.

Run from packing/ with the project interpreter:

    uv run --frozen --all-extras --group dev python -I \\
        resources/web/wand125-closed-form-2026-10-14/review/localization_checks.py

It reads the retained intervals.json.gz for the d0, d1 and alpha of each interval and
nothing else. It decides nothing about the certificate's leaves or families.
"""

from __future__ import annotations

import gzip
import hashlib
import json
import sys
from fractions import Fraction as Q
from itertools import pairwise
from pathlib import Path

sys.set_int_max_str_digits(0)

HERE = Path(__file__).resolve().parent
PACKET = HERE.parent
INTERVALS = PACKET / "square-packing" / "problems" / "closed-form" / "intervals.json.gz"
MANIFEST = PACKET / "acquisition" / "upstream-subtree.sha256"

R = Q(7072, 10000)
ALPHA = Q(9, 5)
WINDOW = Q(24, 5)
U0, U1 = Q(-13, 32), Q(7, 16)
LEFT_RIGHT_EDGE = Q(167, 100)
STRADDLE_TOP = Q(272, 100)
RIGHT_LEFT_EDGE = Q(251, 100)
TOP = Q(19, 5)
SHIFT_LO, SHIFT_HI = Q(271, 100), Q(371, 100)

CHECKS: list[tuple[str, bool, str]] = []


def emit(line: str) -> None:
    sys.stdout.write(line + "\n")


def check(name: str, *, ok: bool, detail: str = "") -> None:
    CHECKS.append((name, ok, detail))
    emit(f"{'OK ' if ok else 'NG '}{name}{': ' + detail if detail else ''}")


def half_width(u: Q) -> Q:
    """(c + |s|)/2 for u = tan(theta/2)."""
    d = 1 + u * u
    return ((1 - u * u) / d + abs(2 * u / d)) / 2


def corner_margin(k: int, d: Q) -> Q:
    """(a - W) - (a/2 + r) for a = k + delta, W = 2 + delta."""
    a = k + d
    return a - (2 + d) - a / 2 - R


def main() -> int:
    data = gzip.decompress(INTERVALS.read_bytes())
    digest = hashlib.sha256(data).hexdigest()
    want = next(
        line.split("  ")[0]
        for line in MANIFEST.read_text(encoding="utf-8").splitlines()
        if line.endswith("problems/closed-form/intervals.json")
    )
    if digest != want:
        emit(f"intervals.json digest {digest} is not the manifest's {want}")
        return 1
    ivs = [
        (int(r["index"]), Q(r["d0"]), Q(r["d1"]), Q(r["certified_line"]["alpha"]))
        for r in json.loads(data, parse_float=str)["intervals"]
    ]
    d1min = min(iv[2] for iv in ivs)
    d1max = max(iv[2] for iv in ivs)

    # 1, 2: corner and edge reach. The margin is k/2 - delta/2 - 2 - r: it falls in delta
    # and rises in k, so the worst case over k >= 7, delta <= 1 is k = 7, delta = 1.
    worst = corner_margin(7, Q(1))
    check(
        "1 a/2 + r < a - W at k = 7, delta = 1 (the worst case)",
        ok=worst > 0,
        detail=f"margin {worst}",
    )
    grid = [corner_margin(k, Q(j, 10)) for k in range(7, 40) for j in range(11)]
    check(
        "1 that margin is least at k = 7, delta = 1 on a grid of k and delta",
        ok=min(grid) == worst,
    )
    k6 = [(d, corner_margin(6, d) > 0) for d in (Q(585, 1000), Q(586, 1000), Q(1))]
    check(
        "1 k = 6 holds a/2 + r < a - W at delta = 0.585 and fails at 0.586 and 1",
        ok=[ok for _, ok in k6] == [True, False, False],
        detail="threshold 2(1 - r) = " + str(2 * (1 - R)),
    )
    check(
        "2 a/2 + r < a - 2 at k = 7, delta -> 0",
        ok=Q(7) / 2 + R < 5,
        detail=f"margin {5 - Q(7, 2) - R}",
    )
    margin_u = 7 - ALPHA - Q(7, 2) - R
    check(
        "2 a/2 + r < a - 9/5 at k = 7, delta -> 0", ok=margin_u > 0, detail=f"margin {margin_u}"
    )

    # 3: the shifted square of step (3) spans at most (2.71 - r, 3.71 + r) along the wall.
    lo_span, hi_span = SHIFT_LO - R, SHIFT_HI + R
    check(
        "3 the shifted square stays above the corner boundary 2",
        ok=lo_span > 2,
        detail=f"{lo_span}",
    )
    check(
        "3 the shifted square stays below a - W = k - 2 at k = 7",
        ok=hi_span < 5,
        detail=f"{hi_span} < 5",
    )
    check(
        "3 the shifted square stays below a - 9/5 at k = 7",
        ok=hi_span < 7 - ALPHA,
        detail=f"{hi_span} < 26/5",
    )
    check(
        "3 on the bottom wall the shifted square ends below a - 2 = k - 2 + delta",
        ok=SHIFT_HI + R < 5,
    )
    check(
        "3 a shifted square with z_x >= 9/5 + r lies inside U",
        ok=lo_span > ALPHA and hi_span < 7 - ALPHA,
    )

    # 4: the checked regions' squares.
    x_reach = RIGHT_LEFT_EDGE + d1max + R
    check(
        "4 straddle and top squares stay inside [0, 24/5]^2",
        ok=x_reach <= WINDOW and TOP + R <= WINDOW,
        detail=f"x <= {x_reach}, y <= {TOP + R}",
    )
    check(
        "4 left squares stay inside [0, 24/5]^2",
        ok=LEFT_RIGHT_EDGE + R <= WINDOW and TOP + R <= WINDOW,
    )
    check(
        "4 right squares, shifted, stay inside x' < 5 (three stored periods) and y < 24/5",
        ok=TOP + R < 5,
    )
    check(
        "4 right squares, original coordinates, lie right of the left wall x <= 9/5",
        ok=RIGHT_LEFT_EDGE - R > ALPHA,
        detail=f"{RIGHT_LEFT_EDGE - R} > 9/5",
    )
    check("4 right squares do not reach the terminal line x = a - 2 at k = 7", ok=TOP + R < 5)
    check("4 right squares stay below a - 9/5 at k = 7 for every delta", ok=TOP + R < 7 - ALPHA)

    # 5: coverage of [0, 3.8 + delta] x [0, 3.8] for delta in [d0, d1].
    gaps = [f"I{i}" for i, _, d1, _ in ivs if RIGHT_LEFT_EDGE + d1 < RIGHT_LEFT_EDGE + d1]
    check(
        "5 straddle and top reach 2.51 + d1 >= 2.51 + delta, where the right region begins",
        ok=not gaps,
    )
    check(
        "5 left, straddle and top meet at x = 1.67 and y = 2.72 with no gap",
        ok=LEFT_RIGHT_EDGE > 0 and STRADDLE_TOP < TOP,
    )
    check(
        "5 the (3a) remainder y in [2.71, 2.72) with x < 9/5 + r lies in the straddle region",
        ok=RIGHT_LEFT_EDGE + d1min >= ALPHA + R and SHIFT_LO <= STRADDLE_TOP,
    )
    check(
        "5 the (3a) remainder y in [2.72, 3.71], x < 9/5 + r, lies in the top or left region",
        ok=RIGHT_LEFT_EDGE + d1min >= ALPHA + R and SHIFT_HI <= TOP,
    )
    check(
        "5 the (3b) remainder x - delta in (2.7072, 2.71) lies in the right region",
        ok=RIGHT_LEFT_EDGE <= 2 + R and SHIFT_LO <= TOP,
    )

    # 6: the angular range.
    a_u, b_u = -U0, U1
    cover = a_u + b_u + a_u * b_u
    check(
        "6 u-range [-13/32, 7/16] covers 90 degrees: a + b + ab >= 1",
        ok=cover >= 1,
        detail=f"{cover}",
    )
    check("6 |u| < 1 on the range", ok=a_u < 1 and b_u < 1)

    # 7: hmax.
    us = [Q(j, 1000) for j in range(401)]
    nondecreasing = all(half_width(x) <= half_width(y) for x, y in pairwise(us))
    check(
        "7 the half-width (c + |s|)/2 is nondecreasing on [0, 2/5] at 401 sample points",
        ok=nondecreasing,
    )
    check(
        "7 the half-width is increasing up to |u| = sqrt(2) - 1, which exceeds 2/5",
        ok=(Q(2, 5) + 1) ** 2 < 2,
    )
    check("7 7072/10000 exceeds sqrt(2)/2", ok=Q(1, 2) < R * R, detail=f"r^2 = {R * R}")
    formula = (1 - Q(4, 25) + Q(4, 5)) / (2 * (1 + Q(4, 25)))
    check(
        "7 the hmax formula at m = 2/5 equals the half-width there",
        ok=formula == half_width(Q(2, 5)),
    )

    # 8: the window premise.
    check(
        "8 a - 9/5 >= 24/5 for every k >= 7",
        ok=7 - ALPHA >= WINDOW,
        detail="26/5 >= 24/5 at k = 7",
    )

    # 9: the slopes.
    amax = max(iv[3] for iv in ivs)
    check(
        "9 every alpha_i <= 1.7496, so 2(k + delta) - 4 alpha_i > 0 for k >= 7",
        ok=amax <= Q(17496, 10000) and 14 - 4 * amax > 0,
        detail=f"max alpha = {float(amax):.7f}",
    )

    bad = [c for c in CHECKS if not c[1]]
    emit(f"{len(CHECKS)} checks, {len(bad)} failed")
    emit("LOCALIZATION OK" if not bad else "LOCALIZATION NG")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
