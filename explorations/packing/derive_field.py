#!/usr/bin/env python3
"""Derive the number field of Trump's 11-square packing from scratch.

Takes only the published minimal polynomial of the container side and the
tilted-block contact relation, and produces the minimal polynomial of
`u = tan(a/2)` that `sqpack.packings.trump11` uses.  Run this to confirm the
constant in that module rather than trusting it.

Requires SymPy (used only here, not by the verifier).
"""

import sympy as sp

from sqpack.packings.trump11 import U_MIN_POLY


def main() -> int:
    u, s = sp.symbols("u s")

    published = (
        s**8
        - 20 * s**7
        + 178 * s**6
        - 842 * s**5
        + 1923 * s**4
        - 496 * s**3
        - 6754 * s**2
        + 12420 * s
        - 6865
    )
    poly_s = sp.Poly(published, s)
    print("published minimal polynomial of s")
    print("  irreducible over Q:", poly_s.is_irreducible)
    print("  real roots:", [sp.N(r, 20) for r in sp.real_roots(poly_s)])

    # Half-angle substitution: cos a = (1-u^2)/(1+u^2), sin a = 2u/(1+u^2),
    # so s = 2 + (2 + sin a)/(cos a + sin a) becomes:
    numerator, denominator = 6 * u + 4, -(u**2) + 2 * u + 1
    print("\ns as a rational function of u: (6u + 4) / (-u^2 + 2u + 1)")

    substituted = published.subs(s, numerator / denominator)
    cleared = sp.Poly(sp.expand(sp.numer(sp.cancel(substituted))), u)
    print("cleared polynomial in u has degree", cleared.degree())

    print("\nirreducible factors over Q:")
    chosen = None
    for factor, _ in sp.factor_list(cleared.as_expr())[1]:
        fp = sp.Poly(factor, u)
        roots = [sp.N(r, 25) for r in sp.real_roots(fp)]
        print(f"  degree {fp.degree()}: {fp.all_coeffs()}")
        for r in roots:
            print(f"      real root {r}")
            if sp.Rational(36, 100) < r < sp.Rational(37, 100):
                chosen = fp

    if chosen is None:
        print("\nNo factor has a root in (0.36, 0.37); derivation failed.")
        return 1

    print("\nminimal polynomial of u = tan(a/2), highest degree first:")
    print(" ", [int(c) for c in chosen.all_coeffs()])
    match = tuple(int(c) for c in chosen.all_coeffs()) == tuple(U_MIN_POLY)
    print("matches sqpack.packings.trump11.U_MIN_POLY:", match)
    return 0 if match else 1


if __name__ == "__main__":
    raise SystemExit(main())
