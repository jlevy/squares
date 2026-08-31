#!/usr/bin/env python3
"""Replay Göbel's five-square construction with exact algebraic predicates."""

from __future__ import annotations

from cases.gobel5.packing import build
from sqpack.verify import Report, exact_sign, verify_packing

CERTIFIES = (5,)
"""The sizes this module decides by exact predicate.

`devtools.check_certificate_citations` requires the frontier record for each of these to
cite this package as a certificate. See `D-398`: three records once declared a
mathematical blocker while their certificate sat in the gate unnamed.
"""


def verify() -> Report:
    """Return the exact separating-axis report for the named witness."""
    squares, side, _field = build()
    return verify_packing(squares, side, sign=exact_sign)


def main() -> int:
    report = verify()
    print(report)
    if not report.valid or report.n != 5 or report.pairs_tested != 10:
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
