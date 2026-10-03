"""The kernel's exact rational type: gmpy2's `mpq`, required.

Every module of `sqpack.hull_kernel` takes `Q` from here and computes in it. `mpq`
carries the same `numerator` and `denominator`, hashes and compares as
`fractions.Fraction` does, parses and prints the same `"p/q"` strings, rounds ties to
even and converts to `float` by correct rounding, so every serialised value and every
float the producer locates with is the one `Fraction` would give;
`tests/test_hull_kernel_rational.py` holds the evidence, and the byte-identical
blind-pair digests in `tests/test_hull_kernel_octagon.py` are the end-to-end check.
`Rational` is what the frame constructors accept, since the cover tools hand them
`Fraction` values; they convert to `Q` at the boundary. `Z` is an exact integer, `int`
or gmpy2's `mpz`, which the numerators and denominators of an `mpq` are.

Two cautions. The verifiers under `devtools/` stay on CPython's integers and `Fraction`,
so the two sides of an admission share no arithmetic library. And `Fraction(mpq)` is a
`Fraction` whose numerator and denominator are `mpz`, which gmpy2 later refuses with
`SystemError` when it meets one in arithmetic; a caller handing kernel values to code
that wants `Fraction` by type uses `as_fraction`, which goes through `int`. `BACKEND`
names what ran, for receipts.
"""

from __future__ import annotations

from fractions import Fraction

import gmpy2
from gmpy2 import mpq, mpz

Q = mpq
type Rational = mpq | Fraction | int
type Z = int | mpz

BACKEND: dict[str, str] = {
    "library": "gmpy2",
    "version": gmpy2.version(),
    "mp": gmpy2.mp_version(),
}


def as_fraction(value: Rational) -> Fraction:
    """The value as a `Fraction` with `int` parts, for code that wants that exact type."""
    return Fraction(int(value.numerator), int(value.denominator))


__all__ = ["BACKEND", "Q", "Rational", "Z", "as_fraction"]
