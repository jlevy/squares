#!/usr/bin/env python3
"""Re-derive the exact field named by the public n=54 source serialization.

The live Kingbird SVG carries exact expressions in XML comments but renders from finite
decimal entities. This tool checks that the side, tangent, and algebraic orientation
vector used by those expressions lie in one quartic field. The angle itself is an exact
arctangent expression, not a claimed algebraic field element. The tool deliberately does
not fetch the SVG, infer poses from decimals, or test packing geometry.

A derivation that only ever agrees with itself proves nothing about the checks, so the
receipt is refusable on demand. Two named negative controls perturb exactly one input
each and must be refused by two different guards:

`perturbed-side-basis` replaces the side's basis expansion `15/2 + p - p^2/2` with
`15/2 + p - p^2/3`. It must fail the `side basis` identity, which is the guard that would
catch a mistranscribed basis coefficient, and no receipt may be printed.

`changed-minimal-polynomial` changes one coefficient of the expected side polynomial. It
must fail the minimal-polynomial comparison, which is the independent guard: the basis
identities and the `minpoly` computation could in principle agree on a wrong field, and
this control shows the second gate is load-bearing rather than decorative.

Neither control can move the default receipt, because both are injected downstream of the
frozen expressions and only ever widen a refusal. The `--check` bytes are unchanged.

Usage:
    uv run --frozen --all-extras --group dev python -m devtools.audit_n54_source_formula --check
    uv run --frozen --all-extras --group dev python -m devtools.audit_n54_source_formula \
        --mutate perturbed-side-basis
"""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence

import sympy as sp

#: Named negative controls, each perturbing one input and refused by a different guard.
NEGATIVE_CONTROLS: dict[str, str] = {
    "perturbed-side-basis": "side basis expansion uses -p^2/3 instead of -p^2/2",
    "changed-minimal-polynomial": "expected side polynomial constant term 8897 becomes 8896",
}


def _require_zero(name: str, value: sp.Expr) -> None:
    if sp.simplify(value) != 0:
        raise ValueError(f"n=54 source identity failed: {name}")


def _polynomial_coefficients(value: sp.Expr, variable: sp.Symbol) -> list[int]:
    polynomial = sp.Poly(sp.minpoly(value, variable), variable)
    return [int(coefficient) for coefficient in polynomial.all_coeffs()]


def derive_receipt(*, mutation: str | None = None) -> dict[str, object]:
    """Check the source formulas and return their canonical exact-field receipt.

    `mutation` names one entry of `NEGATIVE_CONTROLS` and must raise. It is `None` for
    every real derivation, and the receipt is byte-identical to the unmutated tool.
    """
    if mutation is not None and mutation not in NEGATIVE_CONTROLS:
        raise ValueError(f"unknown n=54 negative control: {mutation}")
    variable = sp.symbols("x")
    sqrt_two = sp.sqrt(2)
    primitive = sp.sqrt(1 + sqrt_two)
    angle_auxiliary = sp.sqrt(1 + 5 * sqrt_two)
    tangent = (3 + sqrt_two + 2 * angle_auxiliary) / 7
    unit = sp.sqrt(1 + tangent**2)
    sine = tangent / unit
    cosine = 1 / unit
    side = 7 - sqrt_two / 2 + primitive

    basis = {
        "sqrt_two": primitive**2 - 1,
        "angle_auxiliary": 2 * primitive**3 - 3 * primitive,
        "side": sp.Rational(15, 2) + primitive - primitive**2 / 2,
        "tan_angle": (
            sp.Rational(2, 7)
            - sp.Rational(6, 7) * primitive
            + sp.Rational(1, 7) * primitive**2
            + sp.Rational(4, 7) * primitive**3
        ),
        "sin_angle": (sp.Rational(1, 2) - primitive + sp.Rational(1, 2) * primitive**3),
        "cos_angle": 1 + primitive / 2 - primitive**2 / 2,
    }
    if mutation == "perturbed-side-basis":
        basis["side"] = sp.Rational(15, 2) + primitive - primitive**2 / 3

    _require_zero("primitive polynomial", primitive**4 - 2 * primitive**2 - 1)
    _require_zero("sqrt(2) basis", sqrt_two - basis["sqrt_two"])
    _require_zero(
        "sqrt(1 + 5 sqrt(2)) basis",
        angle_auxiliary - basis["angle_auxiliary"],
    )
    _require_zero("side basis", side - basis["side"])
    _require_zero("tan(angle) basis", tangent - basis["tan_angle"])
    _require_zero("sin(angle) basis", sine - basis["sin_angle"])
    _require_zero("cos(angle) basis", cosine - basis["cos_angle"])
    _require_zero("unit circle", sine**2 + cosine**2 - 1)

    field_polynomial = _polynomial_coefficients(primitive, variable)
    side_polynomial = _polynomial_coefficients(side, variable)
    tangent_polynomial = _polynomial_coefficients(tangent, variable)
    sine_polynomial = _polynomial_coefficients(sine, variable)
    cosine_polynomial = _polynomial_coefficients(cosine, variable)
    minimal_polynomials = {
        "side": side_polynomial,
        "tan_angle": tangent_polynomial,
        "sin_angle": sine_polynomial,
        "cos_angle": cosine_polynomial,
    }
    expected_polynomials = {
        "field": [1, 0, -2, 0, -1],
        "side": [4, -112, 1164, -5304, 8897],
        "tan_angle": [7, -12, 6, -4, -1],
        "sin_angle": [8, -16, 16, -8, 1],
        "cos_angle": [8, -16, 0, 16, -7],
    }
    if mutation == "changed-minimal-polynomial":
        expected_polynomials["side"] = [4, -112, 1164, -5304, 8896]
    observed_polynomials = {"field": field_polynomial, **minimal_polynomials}
    if observed_polynomials != expected_polynomials:
        raise ValueError(
            "unexpected n=54 minimal polynomials: "
            f"observed={observed_polynomials}, expected={expected_polynomials}"
        )

    return {
        "field": {
            "name": "Q(p)",
            "primitive": "p = sqrt(1 + sqrt(2))",
            "minimal_polynomial_coefficients": field_polynomial,
            "embedding": "positive real root p in (1.5537, 1.5538)",
        },
        "basis_order": ["1", "p", "p^2", "p^3"],
        "basis_coefficients": {
            "sqrt_two": ["-1", "0", "1", "0"],
            "sqrt_1_plus_5sqrt2": ["0", "-3", "0", "2"],
            "side": ["15/2", "1", "-1/2", "0"],
            "tan_angle": ["2/7", "-6/7", "1/7", "4/7"],
            "sin_angle": ["1/2", "-1", "0", "1/2"],
            "cos_angle": ["1", "1/2", "-1/2", "0"],
        },
        "minimal_polynomials": minimal_polynomials,
        "decimal_check": {
            "side": str(sp.N(side, 60)),
            "angle_degrees": str(sp.N(sp.atan(tangent) * 180 / sp.pi, 60)),
        },
        "checks": [
            "source side identity",
            "source tangent and orientation identities",
            "quartic-field closure",
            "unit-circle identity",
            "minimal polynomials",
        ],
        "scope": "exact formula and field only; no source fetch, pose inference, or geometry",
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify and print the receipt")
    parser.add_argument(
        "--mutate",
        choices=sorted(NEGATIVE_CONTROLS),
        help="run one named negative control, which must be refused and print no receipt",
    )
    args = parser.parse_args(argv)
    if not args.check and args.mutate is None:
        parser.error("pass --check to run the exact derivation, or --mutate to run a control")
    if args.mutate is not None:
        try:
            derive_receipt(mutation=args.mutate)
        except ValueError as error:
            print(f"refused {args.mutate}: {error}", file=sys.stderr)
            return 1
        print(
            f"n=54 negative control was not refused: {args.mutate}",
            file=sys.stderr,
        )
        return 2
    print(json.dumps(derive_receipt(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
