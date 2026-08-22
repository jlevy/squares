#!/usr/bin/env python3
"""Does the verifier actually reject bad packings, and where does float64 stop?

An "OK" from a verifier that never says no carries no information.  This
slides one square into its neighbour by a decreasing offset and asks each
verifier whether the result is still valid.

The exact verifier rejects every positive offset.  The float64 verifier has
a blind spot exactly the size of its tolerance, and setting the tolerance to
zero makes it reject the *valid* packing -- so no tolerance is safe.
"""

from fractions import Fraction

from sqpack.verify import verify_packing, exact_sign, float_sign
from sqpack.packings import trump11

# Squares 3 and 5 in the reconstruction are stacked: [0,1]x[s-1,s] sits
# directly on [0,1]x[s-2,s-1].  Sliding 5 up by any delta > 0 is an overlap.
SLIDING_SQUARE = 5
EXACT_DELTAS = (6, 12, 15, 18, 30, 100)
FLOAT_DELTAS = (6, 9, 12, 15, 18)


def slide(squares, index, delta, add):
    out = [list(sq) for sq in squares]
    out[index] = [(x, add(y, delta)) for x, y in squares[index]]
    return out


def main() -> int:
    squares, side, field = trump11.build()
    K = field.rational

    baseline = verify_packing(squares, side, sign=exact_sign)
    print(f"exact verifier, unperturbed packing: {'accept' if baseline.valid else 'REJECT'}")
    failures = 0
    for k in EXACT_DELTAS:
        moved = slide(squares, SLIDING_SQUARE, K(Fraction(1, 10 ** k)), lambda y, d: y + d)
        report = verify_packing(moved, side, sign=exact_sign, check_shapes=False)
        verdict = "accept" if report.valid else "REJECT"
        print(f"  delta = 1e-{k:<4} {verdict}")
        if report.valid:
            failures += 1

    print("\nfloat64 separating-axis test:")
    as_float = [[(float(x), float(y)) for x, y in sq] for sq in squares]
    side_f = float(side)
    for tol in (1e-9, 1e-12, 0.0):
        sign = float_sign(tol)
        base = verify_packing(as_float, side_f, sign=sign, check_shapes=False)
        row = []
        for k in FLOAT_DELTAS:
            moved = slide(as_float, SLIDING_SQUARE, 10.0 ** -k, lambda y, d: y + d)
            r = verify_packing(moved, side_f, sign=sign, check_shapes=False)
            row.append(f"1e-{k}: {'accept' if r.valid else 'REJECT'}")
        print(f"  tol={tol:<8g} valid packing: {'accept' if base.valid else 'REJECT'}"
              f"   {'  '.join(row)}")

    print("\nA float verifier that accepts the true packing also accepts overlaps")
    print("below its tolerance; one that rejects those overlaps also rejects the")
    print("true packing. That is why exactness here is about representation, not precision.")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
