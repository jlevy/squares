#!/usr/bin/env python3
"""Verify Walter Trump's 11-square packing exactly, and report what it took."""

import time

from sqpack.verify import verify_packing, exact_sign
from sqpack.packings import trump11


def main() -> int:
    squares, side, field = trump11.build()

    start = time.time()
    report = verify_packing(squares, side, sign=exact_sign)
    elapsed = time.time() - start

    print("Exact verification of Trump's 11-square packing")
    print(report)
    print(f"  field:     Q(u), degree {field.degree}, u = tan(a/2)")
    print(f"  interval refinements needed: {field.refinements}")
    print(f"  wall time: {elapsed:.3f} s")
    ok_poly = trump11.side_satisfies_published_polynomial(side, field)
    print(f"  P(s) == 0 for the published degree-8 polynomial: {ok_poly}")
    print(f"  s = {field.decimal(side, 40)}")
    print("  published (Ellsworth, 33 digits):")
    print("      3.87708359002281417730789706010096")
    return 0 if (report.valid and ok_poly) else 1


if __name__ == "__main__":
    raise SystemExit(main())
