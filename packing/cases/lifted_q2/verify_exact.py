#!/usr/bin/env python3
"""Replay the lifted `n = 19` and `n = 66` witnesses with exact algebraic predicates.

The lift is the candidate generator and this is the proof: every pair and wall decided
by exact sign over `Q(sqrt 2)` at the published sides `3 + (4/3) sqrt(2)` and
`3 + 4 sqrt(2)`. A duplicated square is refused at both sizes, and the side lift is
pinned to the published exact form inside `build` itself, so a drifted witness fails
loudly rather than certifying something else.

Nothing is promoted here and nothing about optimality is claimed.

Usage:
    uv run --frozen python -m cases.lifted_q2.verify_exact
"""

from __future__ import annotations

from cases.lifted_q2.packing import SIDES, build
from sqpack.verify import exact_sign, verify_packing

CERTIFIES = (19, 66)
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
    print("field preconditions: x^2-2 irreducible; (1,2) isolates its positive root")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
