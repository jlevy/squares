#!/usr/bin/env python3
"""Hand the `n = 29` system to an external eliminator, and check what comes back.

[`probe_system_degree`](probe_system_degree.py) rationalised the published system and
bounded the degree of `s(29)` by Bezout at `1,039,500`, which settled that the
integer-relation refusal through degree twenty surveyed a corner of the space.  It did
not attempt the elimination.  This tool does, by writing the system in a form an external
Groebner engine reads and by checking whatever that engine returns.

**Why an external engine.**  SymPy's Buchberger implementation is not the state of the
art and the failure mode here is coefficient swell rather than step count, so
"intractable in SymPy" would not have been evidence about the problem.  `msolve`
implements F4 with multi-modular arithmetic and rational reconstruction, which attacks
swell directly.  Reaching for it is part of the measurement, not a shortcut around it.

**Why the emitted text is re-parsed before it is trusted.**  The first attempt at this
export wrote negative coefficients as `(-2)*x`, which is a form `msolve` accepts without
complaint and reads as something else: the system came back with a Groebner basis of
`{1}` -- no solutions -- for a system whose solution this repository has refined to a
thousand digits.  Nothing in the export was checked against what was actually written,
so an encoding bug read as a mathematical result.

So :func:`msolve_input` re-parses its own output and requires two things of it: that the
re-parsed polynomial vanishes at the retained pose, and that it equals the original
exactly.  A guard that checks what was written rather than what was meant is the only
one that could have caught this.

**What an eliminant is worth.**  The roots of an eliminant in `s` are the sides of
*every* complex solution of the system, so a returned polynomial is not yet the minimal
polynomial of `s(29)`: the irreducible factor carrying our root still has to be
identified, and that needs the high-precision value back again.  The two routes compose
rather than compete.  :func:`verify_eliminant` does that half.

Usage:

    python -m devtools.probe_elimination --emit system.ms
    python -m devtools.probe_elimination --emit system.ms --reduced
    python -m devtools.probe_elimination --verify eliminant.txt
"""

from __future__ import annotations

import argparse
import json
import time
from collections.abc import Sequence
from pathlib import Path
from typing import Any

import mpmath as mp
import sympy as sp

from cases.kingbird29 import system as k29
from cases.kingbird29.layout import DEFAULT_SOURCE
from devtools.probe_system_degree import ANGLES, half_angle_system
from sqpack.promote.refine import refine

#: Digits to refine the retained pose to before using it as a witness point.  The guards
#: below ask a polynomial to vanish there; they can only ask that to the precision the
#: point is known to.
WITNESS_DIGITS = 100

#: How far below the largest monomial at the witness point a residual must sit before the
#: polynomial counts as vanishing there.  This is a *relative* bar on purpose: the
#: reduced equations have degree twenty and their terms are not O(1).
VANISHING_DECADES = 60


class EliminationError(ValueError):
    """The export or the returned eliminant did not survive its own check."""

    def __init__(self, kind: str, detail: str) -> None:
        super().__init__(f"{kind}: {detail}")
        self.kind = kind
        self.detail = detail


def witness_point() -> tuple[dict[str, Any], list[str]]:
    """The retained `n = 29` pose in half-angle coordinates, refined and named.

    Returns `(values, names)` with `values` keyed by the half-angle symbol names and by
    `s`.  The pose comes from the source's own serialized entities and is sharpened by
    Newton against the closed system, so it is this repository's value rather than the
    published digits.
    """
    mp.mp.dps = WITNESS_DIGITS + 20
    refined = refine(
        k29.equations,
        k29.seed(DEFAULT_SOURCE),
        WITNESS_DIGITS,
        names=list(k29.UNKNOWNS),
    )
    degrees = {
        name: mp.mpf(value) for name, value in zip(k29.UNKNOWNS, refined.values, strict=True)
    }
    values: dict[str, Any] = {
        f"u_{name}": mp.tan(mp.radians(degrees[name]) / 2) for name in ANGLES
    }
    values["s"] = degrees["s"]
    return values, [f"u_{name}" for name in ANGLES] + ["s"]


def _vanishes(expression, order: Sequence[sp.Symbol], point: Sequence[Any]) -> tuple[bool, Any]:
    """Whether `expression` vanishes at `point`, relative to its own largest term."""
    value = abs(sp.lambdify(order, expression, "mpmath")(*point))
    poly = sp.Poly(expression, *order)
    largest = max(
        abs(mp.mpf(str(coefficient)))
        * mp.fprod([point[k] ** exponent for k, exponent in enumerate(monomial)])
        for monomial, coefficient in zip(poly.monoms(), poly.coeffs(), strict=True)
    )
    scale = abs(largest) if largest != 0 else mp.mpf(1)
    return bool(value / scale < mp.mpf(10) ** -VANISHING_DECADES), value / scale


def reduced_system() -> tuple[list[sp.Poly], list[sp.Symbol], sp.Expr, str]:
    """The five equations in five half-angles left once `s` is solved out.

    Every equation is degree one in `s`, so the pivot costs nothing.  Returns
    `(polynomials, unknowns, side_in_halves, pivot_name)`.
    """
    polynomials, unknowns = half_angle_system()
    side, halves = unknowns[0], list(unknowns[1:])
    pivot = min(range(len(polynomials)), key=lambda k: len(polynomials[k].terms()))
    solved = sp.solve(sp.Eq(polynomials[pivot].as_expr(), 0), side)
    if len(solved) != 1:
        raise EliminationError(
            "pivot-not-linear",
            f"solving f{pivot + 1} for s gave {len(solved)} branches, not one",
        )
    side_in_halves = sp.cancel(sp.together(solved[0]))
    reduced = []
    for index, polynomial in enumerate(polynomials):
        if index == pivot:
            continue
        substituted = polynomial.as_expr().subs(side, side_in_halves)
        numerator = sp.expand(sp.numer(sp.cancel(sp.together(substituted))))
        reduced.append(sp.Poly(numerator, *halves))
    return reduced, halves, side_in_halves, f"f{pivot + 1}"


def _term_text(monomial: Sequence[int], coefficient: int, names: Sequence[str]) -> str:
    """One signed term, in the plain form `msolve` reads.

    Deliberately not parenthesised.  `msolve` accepts `(-2)*x` and does not mean by it
    what the writer meant, which is how a Groebner basis of `{1}` was once obtained for a
    system with a known solution.
    """
    factors = []
    if abs(coefficient) != 1 or all(exponent == 0 for exponent in monomial):
        factors.append(str(abs(coefficient)))
    for name, exponent in zip(names, monomial, strict=True):
        if exponent == 1:
            factors.append(name)
        elif exponent > 1:
            factors.append(f"{name}^{exponent}")
    body = "*".join(factors) if factors else "1"
    return ("-" if coefficient < 0 else "+") + body


def msolve_input(
    polynomials: Sequence[sp.Poly], order: Sequence[sp.Symbol], point: Sequence[Any]
) -> str:
    """Render the system as `msolve` input, refusing unless the text re-parses to it.

    Coefficients are cleared to integers first, so no rational-coefficient syntax is
    exercised at all.  Then every emitted polynomial is read back with SymPy and checked
    twice: that it still vanishes at the retained pose, and that it equals the original
    exactly.  Either check failing is a refusal rather than a warning.
    """
    names = [str(symbol) for symbol in order]
    bodies = []
    for index, polynomial in enumerate(polynomials, 1):
        exact = sp.Poly(polynomial.as_expr(), *order, domain=sp.QQ)
        denominators = [sp.Rational(c).q for c in exact.coeffs()]
        multiplier = sp.ilcm(*denominators) if len(denominators) > 1 else denominators[0]
        terms = []
        for monomial, coefficient in zip(exact.monoms(), exact.coeffs(), strict=True):
            cleared = sp.Rational(coefficient) * multiplier
            if cleared.q != 1:
                raise EliminationError(
                    "coefficient-not-integral",
                    f"f{index} coefficient {coefficient} did not clear to an integer",
                )
            terms.append(_term_text(monomial, int(cleared.p), names))
        text = "".join(terms)
        bodies.append(text[1:] if text.startswith("+") else text)

        locals_ = dict(zip(names, order, strict=True))
        reparsed = sp.sympify(bodies[-1].replace("^", "**"), locals=locals_)
        vanishes, ratio = _vanishes(reparsed, order, point)
        if not vanishes:
            raise EliminationError(
                "emitted-text-does-not-vanish",
                f"f{index} as written evaluates to {mp.nstr(ratio, 5)} of its largest "
                "term at the retained pose; the export is not the system",
            )
        if sp.expand(reparsed - multiplier * polynomial.as_expr()) != 0:
            raise EliminationError(
                "emitted-text-differs",
                f"f{index} as written is not the cleared original; the encoding changed "
                "the polynomial",
            )
    return ",".join(names) + "\n0\n" + ",\n".join(bodies) + "\n"


def verify_eliminant(coefficients: Sequence[int], side_value: Any, *, digits: int) -> dict:
    """Check a returned eliminant against the value it is supposed to admit.

    An eliminant's roots are the sides of every complex solution of the system, so this
    does not claim the polynomial is minimal.  What it can say is whether `s(29)` is
    among its roots, and which irreducible factor carries it -- which is the half the
    high-precision numerics are for.
    """
    variable = sp.Symbol("s")
    polynomial = sp.Poly(list(coefficients), variable)
    mp.mp.dps = digits + 40
    value = mp.mpf(str(side_value))
    residual = abs(sp.lambdify(variable, polynomial.as_expr(), "mpmath")(value))
    largest = max(
        abs(mp.mpf(str(c))) * value ** (polynomial.degree() - k)
        for k, c in enumerate(polynomial.all_coeffs())
    )
    report: dict[str, Any] = {
        "degree": polynomial.degree(),
        "residual": mp.nstr(residual, 6),
        "relative_residual": mp.nstr(residual / largest, 6),
        "admits_value": bool(residual / largest < mp.mpf(10) ** -(digits // 2)),
    }
    factors = sp.factor_list(polynomial.as_expr())[1]
    carrying = []
    for factor, multiplicity in factors:
        at_value = abs(sp.lambdify(variable, factor, "mpmath")(value))
        entry = {
            "degree": sp.Poly(factor, variable).degree(),
            "multiplicity": multiplicity,
            "residual": mp.nstr(at_value, 6),
        }
        if at_value < mp.mpf(10) ** -(digits // 2):
            carrying.append(entry)
        report.setdefault("factors", []).append(entry)
    report["carrying_factors"] = carrying
    return report


def _emit(path: Path, *, reduced: bool) -> dict:
    started = time.monotonic()
    values, _names = witness_point()
    if reduced:
        polynomials, order, _side, pivot = reduced_system()
        point = [values[str(symbol)] for symbol in order]
        note = f"five equations in five half-angles, s eliminated through {pivot}"
    else:
        polynomials, unknowns = half_angle_system()
        order = [*unknowns[1:], unknowns[0]]
        polynomials = [sp.Poly(p.as_expr(), *order) for p in polynomials]
        point = [values[str(symbol)] for symbol in order]
        note = "six equations in six unknowns, s last so an elimination leaves it"
    text = msolve_input(polynomials, order, point)
    path.write_text(text, encoding="utf-8")
    return {
        "path": str(path),
        "bytes": len(text),
        "note": note,
        "unknowns": [str(symbol) for symbol in order],
        "degrees": [p.total_degree() for p in polynomials],
        "seconds": round(time.monotonic() - started, 1),
        "guard": "each emitted polynomial re-parsed, vanishing at the pose and equal to "
        "the cleared original",
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit", type=Path, help="write msolve input to this path")
    parser.add_argument(
        "--reduced",
        action="store_true",
        help="emit the five-unknown system rather than the six-equation one",
    )
    parser.add_argument(
        "--verify",
        type=Path,
        help="check a whitespace- or comma-separated coefficient list, highest degree first",
    )
    parser.add_argument("--digits", type=int, default=WITNESS_DIGITS)
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    arguments = parser.parse_args(argv)

    report: dict[str, Any] = {}
    if arguments.emit is not None:
        report["emit"] = _emit(arguments.emit, reduced=arguments.reduced)
    if arguments.verify is not None:
        raw = arguments.verify.read_text(encoding="utf-8").replace(",", " ").split()
        values, _names = witness_point()
        report["verify"] = verify_eliminant(
            [int(token) for token in raw], values["s"], digits=arguments.digits
        )
    if not report:
        parser.error("nothing to do: pass --emit or --verify")

    if arguments.json:
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0
    for section, body in report.items():
        print(f"== {section} ==")
        for key, value in body.items():
            print(f"  {key}: {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
