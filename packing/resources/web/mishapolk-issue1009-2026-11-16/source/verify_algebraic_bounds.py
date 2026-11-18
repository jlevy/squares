#!/usr/bin/env python3
"""Exact rational comparison of certified container sides against algebraic
bounds on `jlevy/squares` `main` and competing open registration requests.

Uses Python standard-library `fractions.Fraction` only (no floating-point arithmetic).
"""
from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path


def read_side(cert_path: Path) -> tuple[int, Fraction]:
    for line in cert_path.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if s and not s.startswith("#"):
            n_s, side_s = s.split()
            return int(n_s), Fraction(side_s)
    raise ValueError(f"Missing header in {cert_path}")


def main() -> int:
    base = Path(__file__).resolve().parent / "certificates" / "0000-0999"

    n262, s262 = read_side(base / "n262.cert")
    assert n262 == 262
    # Main bound: 16 + sqrt(2)/2. Since s262 > 16, s262 < 16 + sqrt(2)/2 <=> 2*(s262 - 16)^2 < 1.
    assert s262 > 16 and 2 * (s262 - 16) ** 2 < 1, "Failed exact comparison vs 16 + sqrt(2)/2"
    s262_issue1007 = Fraction("166996934419035177/10000000000000000")
    assert s262 < s262_issue1007, "Failed exact comparison vs #1007 (n=262)"
    print(f"VERIFIED n=262: S < 16 + sqrt(2)/2 (2*(S-16)^2 < 1) and S < #1007 by {float(s262_issue1007 - s262):.6e}")

    n295, s295 = read_side(base / "n295.cert")
    assert n295 == 295
    # Main bound: (22 + 22*sqrt(2))/3. Since 3*s295 > 22, s295 < (22 + 22*sqrt(2))/3 <=> (3*s295 - 22)^2 < 968.
    assert 3 * s295 > 22 and (3 * s295 - 22) ** 2 < 968, "Failed exact comparison vs (22 + 22*sqrt(2))/3"
    s295_issue1007 = Fraction("35399386883430443/2000000000000000")
    assert s295 < s295_issue1007, "Failed exact comparison vs #1007 (n=295)"
    print(f"VERIFIED n=295: S < (22 + 22*sqrt(2))/3 ((3S-22)^2 < 968) and S < #1007 by {float(s295_issue1007 - s295):.6e}")

    n292, s292 = read_side(base / "n292.cert")
    assert n292 == 292
    s292_issue1006 = Fraction("33872522175917279266554668306659248043633029180856810473/1925667453806884053962316529711800854170000000000000000")
    assert s292 < s292_issue1006, "Failed exact comparison vs #1006 (n=292)"
    print(f"VERIFIED n=292: S < #1006 exact rational side by {float(s292_issue1006 - s292):.6e}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
