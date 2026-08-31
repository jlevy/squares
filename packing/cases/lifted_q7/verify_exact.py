#!/usr/bin/env python3
"""Replay the lifted `n = 18` and `n = 86` witnesses with exact algebraic predicates.

Every pair and wall decided by an exact sign over `Q(sqrt 7)` at the published sides
`(7 + sqrt(7))/2` and `(17 + sqrt(7))/2`, with the shared tilt's cosine and sine exact
in the field and checked against the circle identity inside `build` itself. A duplicated
square is refused at both sizes, and the side lift is pinned to the published form so a
drifted witness fails loudly.

This is the repository's first exact verification outside `Q(sqrt 2)`.

Nothing is promoted here and nothing about optimality is claimed.

Usage:
    uv run --frozen python -m cases.lifted_q7.verify_exact
"""

from __future__ import annotations

from cases.lifted_q7.packing import SIDES, build
from sqpack.verify import exact_sign, verify_packing

CERTIFIES = (18, 86)
"""The sizes the lift decides. See `CERTIFIES` in `cases/gobel5`."""


def main() -> int:
    for n in sorted(SIDES):
        squares, side, _field = build(n)
        report = verify_packing(squares, side, sign=exact_sign)
        print(report)
        if not report.valid or report.n != n:
            return 1
        if report.pairs_tested != n * (n - 1) // 2:
            print(f"n={n}: {report.pairs_tested} pairs tested, expected all of them")
            return 1

        duplicate = verify_packing([*squares, squares[0]], side, sign=exact_sign)
        if duplicate.valid:
            print(f"n={n}: negative control failed, duplicated square was accepted")
            return 1
        print(f"n={n}: negative control rejected a duplicated square")
    print("field preconditions: x^2-7 irreducible; (2,3) isolates its positive root")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
