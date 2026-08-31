#!/usr/bin/env python3
"""Replay Göbel's ten-square construction with exact algebraic predicates."""

from __future__ import annotations

from cases.gobel10.exact import build
from sqpack.verify import Report, exact_sign, verify_packing

CERTIFIES = (10,)
"""The sizes this module decides by exact predicate. See `CERTIFIES` in `cases/gobel5`."""


def verify() -> Report:
    """Return the exact separating-axis report for the named witness."""
    squares, side, _field = build()
    return verify_packing(squares, side, sign=exact_sign)


def main() -> int:
    report = verify()
    print(report)
    if not report.valid or report.n != 10 or report.pairs_tested != 45:
        return 1
    squares, side, _field = build()
    duplicate = verify_packing([*squares, squares[0]], side, sign=exact_sign)
    if duplicate.valid:
        print("negative control failed: duplicated square was accepted")
        return 1
    print("field preconditions: x^2-2 irreducible; (1,2) isolates its positive root")
    print("negative control: duplicated square rejected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
