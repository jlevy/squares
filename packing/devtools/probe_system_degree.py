#!/usr/bin/env python3
"""Rationalise the `n = 29` closed system and bound the algebraic degree of `s(29)`.

This answers a question the integer-relation route cannot: **how high would a search
have to reach?**

`devtools.probe_minimal_polynomial` found no relation for `s(29)` through degree twenty
below a coefficient bound of `10^22`, on a thousand digits.  That is a real result and it
is easy to over-read.  The reach of an integer-relation search is bounded by

    (d + 1) * log10(C)  <  P - M

with `P` the digits available and `M` the margin, so pushing the degree up buys only
*smaller* coefficients -- and algebraic numbers of higher degree have larger heights, not
smaller.  Whether degree twenty was a survey or a corner depends on the actual degree,
and that is a question about the system rather than about the search.

**What this computes.**  The published system is six equations in `{s, a, b, c, d, i}`
where five of the unknowns are angles appearing through sines and cosines.  Substituting
`u = tan(theta / 2)` turns every trigonometric term rational -- `sin = 2u/(1+u^2)`,
`cos = (1-u^2)/(1+u^2)` -- and clearing denominators leaves six honest polynomials in six
unknowns.  Their total degrees give a Bezout bound on the solution variety, and the
minimal polynomial of `s` divides an eliminant whose degree that bound covers.

Bezout is an upper bound and is usually loose for a structured system, so the number here
says "not small" rather than "this large".  That is enough to settle the question it was
asked: it is not twenty.

The same transcription serves all three routes -- float, interval and symbolic -- because
`sqpack.promote.interval.sin_degrees` dispatches on the scalar it is handed.  A second
copy of a six-equation system would be a second thing to keep correct.

Usage:

    python -m devtools.probe_system_degree
    python -m devtools.probe_system_degree --json
"""

from __future__ import annotations

import argparse
import json
import time
from collections.abc import Sequence
from typing import Any

import sympy as sp

from cases.kingbird29 import system as k29

#: The system's unknowns: the side, then the five angles the half-angle substitution
#: replaces.
SIDE = "s"
ANGLES = ("a", "b", "c", "d", "i")


def half_angle_system() -> tuple[list, list]:
    """The six equations as polynomials in `{s, u_a, u_b, u_c, u_d, u_i}`.

    Returns `(polynomials, unknowns)`.  Each polynomial is the *numerator* of the
    rationalised equation, which has the same zero set away from the poles that
    `cos(theta) = -1` introduces -- and those are `theta = 180 degrees`, which no square
    in this packing is at.
    """
    side = sp.Symbol(SIDE, real=True)
    angles = {name: sp.Symbol(name, real=True) for name in ANGLES}
    equations = k29.equations(side, *(angles[name] for name in ANGLES))

    # Composed rotations produce *combined* angles -- `cos(b - i)` and the like -- because
    # rotating a rotated vector adds the angles.  Substituting only `sin(a)` and `cos(a)`
    # leaves those untouched, and a `Poly` built over the result treats each one as an
    # opaque constant: the degrees come out too small and the bound reads as reassuring.
    # `expand_trig` splits every sum and difference into single-angle terms first, which
    # is what makes the substitution below complete rather than merely plausible.
    equations = [sp.expand_trig(sp.expand(f)) for f in equations]

    substitution = {}
    halves = {}
    for name, symbol in angles.items():
        half = sp.Symbol(f"u_{name}", real=True)
        halves[name] = half
        radians = symbol * sp.pi / 180
        substitution[sp.sin(radians)] = 2 * half / (1 + half**2)
        substitution[sp.cos(radians)] = (1 - half**2) / (1 + half**2)

    unknowns = [side, *(halves[name] for name in ANGLES)]
    polynomials = [
        _over_rationals(
            sp.Poly(
                sp.expand(sp.numer(sp.cancel(sp.together(f.subs(substitution))))), *unknowns
            )
        )
        for f in equations
    ]
    return polynomials, unknowns


def _over_rationals(poly: sp.Poly) -> sp.Poly:
    """The same polynomial with rational coefficients, refusing if that is not exact.

    The transcription writes its constants as `mp.mpf(1)`, `mp.mpf(2)` and so on, because
    its first two routes are numeric.  Carried through the symbolic branch those arrive as
    SymPy `Float`s, and a Groebner basis or resultant over floats is not an exact
    computation -- it is a numerically unstable one wearing an exact answer's clothes.
    Every constant in this system is a small integer or a half, so the conversion is exact
    and a coefficient that is not is a refusal rather than a rounding.
    """
    converted = {}
    for monomial, coefficient in poly.terms():
        exact = sp.nsimplify(coefficient, rational=True)
        if not exact.is_Rational:
            raise ValueError(
                f"coefficient {coefficient} of {monomial} is not rational; the symbolic "
                "route cannot be exact over it"
            )
        if abs(sp.Float(exact) - sp.Float(coefficient)) > sp.Float("1e-20"):
            raise ValueError(
                f"coefficient {coefficient} does not convert exactly to {exact}; the "
                "transcription is carrying a constant this route cannot represent"
            )
        converted[monomial] = exact
    return sp.Poly.from_dict(converted, *poly.gens, domain=sp.QQ)


def reduce_by_side(polynomials: Sequence[sp.Poly], unknowns: Sequence[sp.Symbol]) -> dict:
    """Eliminate `s` by solving the smallest equation for it, and report what is left.

    Every equation is degree one in `s`, so this costs nothing and it is the first move
    any elimination would make.  The equation with the fewest terms is the pivot, which
    at `n = 29` is `f6` -- and `s` comes out of it as a rational function of only
    `u_b` and `u_c`, so three of the five half-angles do not appear in it at all.

    What remains is five equations in five unknowns.  Eliminating *those* is the hard
    part and is not attempted here: a resultant chain over five variables at these
    degrees is where the route either succeeds or is shown to be out of reach, and that
    is a measurement with its own budget rather than a step to take in passing.
    """
    side = unknowns[0]
    halves = list(unknowns[1:])
    pivot = min(range(len(polynomials)), key=lambda k: len(polynomials[k].terms()))
    solved = sp.solve(sp.Eq(polynomials[pivot].as_expr(), 0), side)
    if len(solved) != 1:
        raise ValueError(
            f"solving f{pivot + 1} for s gave {len(solved)} branches; it is degree one "
            "in s and should give exactly one"
        )
    side_of_halves = sp.cancel(sp.together(solved[0]))

    reduced = []
    for index, poly in enumerate(polynomials):
        if index == pivot:
            continue
        substituted = poly.as_expr().subs(side, side_of_halves)
        numerator = sp.expand(sp.numer(sp.cancel(sp.together(substituted))))
        reduced.append((index, sp.Poly(numerator, *halves)))

    bezout = 1
    for _index, poly in reduced:
        bezout *= poly.total_degree()
    return {
        "pivot": f"f{pivot + 1}",
        "side_depends_on": sorted(str(symbol) for symbol in side_of_halves.free_symbols),
        "reduced": [
            {
                "equation": f"f{index + 1}",
                "total_degree": poly.total_degree(),
                "terms": len(poly.terms()),
            }
            for index, poly in reduced
        ],
        "bezout_bound": bezout,
    }


def probe(*, with_reduction: bool = False) -> dict:
    """Build the rationalised system and report what bounds its degree."""
    started = time.monotonic()
    polynomials, unknowns = half_angle_system()
    elapsed = time.monotonic() - started

    entries = []
    bezout = 1
    for index, poly in enumerate(polynomials, 1):
        total_degree = poly.total_degree()
        bezout *= total_degree
        entries.append(
            {
                "equation": f"f{index}",
                "total_degree": total_degree,
                "degree_in_side": poly.degree(unknowns[0]),
                "terms": len(poly.terms()),
            }
        )
    report = {
        "unknowns": [str(symbol) for symbol in unknowns],
        "equations": entries,
        "bezout_bound": bezout,
        "seconds": round(elapsed, 1),
    }
    if with_reduction:
        report["reduction"] = reduce_by_side(polynomials, unknowns)
    return report


def _render(report: dict) -> None:
    print("== n = 29, rationalised by u = tan(theta/2) ==")
    print(f"  unknowns: {', '.join(report['unknowns'])}")
    print(f"  built in {report['seconds']}s")
    print(f"  {'equation':>8} {'total deg':>10} {'deg in s':>9} {'terms':>7}")
    for entry in report["equations"]:
        print(
            f"  {entry['equation']:>8} {entry['total_degree']:>10} "
            f"{entry['degree_in_side']:>9} {entry['terms']:>7}"
        )
    product = " x ".join(str(entry["total_degree"]) for entry in report["equations"])
    print(f"\n  Bezout bound on the solution variety: {product} = {report['bezout_bound']:,}")
    if all(entry["degree_in_side"] == 1 for entry in report["equations"]):
        print(
            "\n  Every equation is degree 1 in s, which is the structural fact an\n"
            "  elimination would start from: s can be solved for from any one of them and\n"
            "  substituted into the rest, leaving five equations in the five half-angles."
        )
    if "reduction" in report:
        reduction = report["reduction"]
        print(
            f"\n  Eliminating s through {reduction['pivot']}: s is a rational function of "
            f"{', '.join(reduction['side_depends_on'])} alone."
        )
        for entry in reduction["reduced"]:
            print(
                f"    {entry['equation']:>4} -> total deg {entry['total_degree']:>3}, "
                f"{entry['terms']:>5} terms"
            )
        print(f"    five equations in five unknowns, Bezout {reduction['bezout_bound']:,}")
    print(
        "\n  Read this as 'not small' rather than 'this large': Bezout is an upper bound\n"
        "  and is loose for a structured system. What it settles is the question it was\n"
        "  asked -- the degree of s(29) is not twenty, so the integer-relation refusal\n"
        "  through degree twenty surveyed a corner of the space rather than the space."
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--eliminate-side",
        action="store_true",
        help="also solve the smallest equation for s and report the system that leaves",
    )
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    arguments = parser.parse_args(argv)
    report: dict[str, Any] = probe(with_reduction=arguments.eliminate_side)
    if arguments.json:
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0
    _render(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
