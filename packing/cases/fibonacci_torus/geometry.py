"""Exact reconstruction of two clearances in Trump's eleven-square contact family.

This checks an explicitly defined parameter rectangle independently of the manuscript
shown in the Fibonacci-torus screenshot. It does not construct that manuscript's
torus, identify its parameter domain, or replace unrestricted global capture.

Run from ``packing/`` with ``python -m cases.fibonacci_torus.geometry``. The JSON
receipt contains rational Bernstein bounds, with no numerical sampling as evidence.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from functools import cache
from itertools import combinations
from math import comb
from pathlib import Path
from typing import Any

import sympy as sp

from cases.trump11.packing import S_MIN_POLY, U_MIN_POLY

REPO = Path(__file__).resolve().parents[3]
CONTACT_ATLAS = REPO / "packing/atlas/known-best/contact-structures.json"
U, SIDE = sp.symbols("u L", real=True)
U_INTERVAL = (sp.Rational(9, 25), sp.Rational(37, 100))
SIDE_INTERVAL = (sp.Rational(387, 100), sp.Rational(389, 100))
REFERENCE = {U: sp.Rational(73, 200), SIDE: sp.Rational(97, 25)}
Point = tuple[Any, Any]
Square = tuple[Point, Point, Point]


@dataclass(frozen=True)
class ContactFamily:
    """Each square is an origin and two unit edge vectors, ordered counterclockwise."""

    cosine: Any
    sine: Any
    squares: tuple[Square, ...]
    gaps: tuple[Any, Any]


def family() -> ContactFamily:
    """Free the side in ``trump11.packing.build_in`` while keeping its contact chart."""
    c, s = (1 - U**2) / (1 + U**2), 2 * U / (1 + U**2)
    r = 1 - (SIDE - 3) * c
    b = ((1 + r) * c - 1) / s
    v = c - s
    h = (SIDE - 1) / s - r - (3 + b) * c / s
    x = 1 + 2 / c - (SIDE - 2) * s / c
    aligned_origins = (
        (0, 0),
        (SIDE - 1, 0),
        (x, SIDE - 1),
        (0, SIDE - 1),
        (1, SIDE - 1),
        (0, SIDE - 2),
    )
    squares: list[Square] = [(origin, (1, 0), (0, 1)) for origin in aligned_origins]
    for p, q in ((0, 0), (b, -1), (1, v), (b + 1, v - 1), (b + 2, -h)):
        squares.append(((1 + c * p - s * (q - r), 1 + s * p + c * (q - r)), (c, s), (-s, c)))
    return ContactFamily(
        c,
        s,
        tuple(squares),
        ((SIDE - 2) * (c + s) - 2 - s, -s * x + c * (SIDE - 2) - 1 + h + r),
    )


@cache
def bernstein_coefficients(expression: Any) -> tuple[Any, ...]:
    """Convert a rational polynomial on ``U_INTERVAL`` to the Bernstein basis.

    For power coefficients a_j on [0,1], b_k=sum_{j<=k} a_j C(k,j)/C(n,j).
    The Bernstein basis is nonnegative and sums to one, so min(b_k) is a bound
    throughout the closed interval, including both endpoints.
    """
    t = sp.Symbol("bernstein_t")
    lo, hi = U_INTERVAL
    polynomial = sp.Poly(sp.expand(expression.subs(U, lo + (hi - lo) * t)), t)
    if polynomial.is_zero:
        return (sp.Integer(0),)
    degree = int(polynomial.degree())
    return tuple(
        sum(
            (
                polynomial.nth(j) * sp.Rational(comb(k, j), comb(degree, j))
                for j in range(k + 1)
            ),
            sp.Integer(0),
        )
        for k in range(degree + 1)
    )


def certify_nonnegative(expression: Any, *, strict: bool = False) -> dict[str, Any]:
    """Bound a rational function whose numerator is affine in the enclosing side.

    The denominator must be independent of the side and strictly positive after
    a possible overall sign change. Affinity then makes the two side endpoints
    sufficient; positivity in u is proved by rational Bernstein coefficients.
    A failed bound is a refusal, not a claim that the expression changes sign.
    """
    numerator, denominator = sp.fraction(sp.cancel(expression))
    if denominator.has(SIDE) or sp.Poly(numerator, SIDE).degree() > 1:
        raise ValueError("expected an affine side numerator and side-independent denominator")
    if denominator.subs(U, U_INTERVAL[0]).is_negative:
        numerator, denominator = -numerator, -denominator
    denominator_minimum = min(bernstein_coefficients(denominator))
    numerator_minimum = min(
        coefficient
        for side in SIDE_INTERVAL
        for coefficient in bernstein_coefficients(numerator.subs(SIDE, side))
    )
    if denominator_minimum <= 0 or numerator_minimum < 0 or (strict and numerator_minimum == 0):
        raise ValueError(f"Bernstein bound did not prove the requested sign: {expression}")
    return {
        "numerator": str(numerator),
        "denominator": str(denominator),
        "numerator_bernstein_minimum": str(numerator_minimum),
        "denominator_bernstein_minimum": str(denominator_minimum),
        "strict": strict,
    }


def _dot(a: Point, b: Point) -> Any:
    return sp.sympify(a[0] * b[0] + a[1] * b[1])


@cache
def _support(square: Square, axis: Point, construction: ContactFamily, *, upper: bool) -> Any:
    origin, first, second = square
    value = _dot(origin, axis)
    c, s = construction.cosine, construction.sine
    signs = ((0, 0), (1, 1), (-1, -1), (c, 1), (-c, -1), (s, 1), (-s, -1))
    for edge in (first, second):
        projection = sp.cancel(_dot(edge, axis))
        sign = next(
            (sign for candidate, sign in signs if sp.cancel(projection - candidate) == 0), None
        )
        if sign is None:
            raise ValueError("an edge projection has no proved sign on the angle interval")
        if (upper and sign > 0) or (not upper and sign < 0):
            value += projection
    return value


def _axes(i: int, j: int, construction: ContactFamily) -> list[Point]:
    axes: list[Point] = []
    if min(i, j) < 6:
        axes.extend(((1, 0), (0, 1)))
    if max(i, j) >= 6:
        c, s = construction.cosine, construction.sine
        axes.extend(((c, s), (-s, c)))
    return [signed for x, y in axes for signed in ((x, y), (-x, -y))]


def check_rectangle(construction: ContactFamily) -> dict[str, Any]:
    """Prove containment and all SAT alternatives on the declared closed rectangle."""
    c, s = construction.cosine, construction.sine
    if sp.cancel(c**2 + s**2 - 1) != 0:
        raise ValueError("the rotated edges are not orthonormal")
    positivity = {
        "cosine": certify_nonnegative(c, strict=True),
        "sine": certify_nonnegative(s, strict=True),
    }
    walls: list[dict[str, Any]] = []
    for i, square in enumerate(construction.squares):
        for name, axis in (
            ("left", (-1, 0)),
            ("right", (1, 0)),
            ("bottom", (0, -1)),
            ("top", (0, 1)),
        ):
            bound = SIDE if name in ("right", "top") else 0
            gap = bound - _support(square, axis, construction, upper=True)
            walls.append({"square": i, "wall": name, **certify_nonnegative(gap)})

    pair_bounds: list[dict[str, Any]] = []
    unavailable: list[dict[str, Any]] = []
    active = {(1, 9): ((-s, c), construction.gaps[0]), (2, 10): ((s, -c), construction.gaps[1])}
    for i, j in combinations(range(11), 2):
        features = [
            (
                axis,
                _support(construction.squares[j], axis, construction, upper=False)
                - _support(construction.squares[i], axis, construction, upper=True),
            )
            for axis in _axes(i, j, construction)
        ]
        if (i, j) in active:
            wanted_axis, wanted_gap = active[i, j]
            for axis, gap in features:
                if axis == wanted_axis:
                    if sp.cancel(gap - wanted_gap) != 0:
                        raise ValueError("the designated clearance is not its SAT feature")
                else:
                    unavailable.append(
                        {
                            "pair": [i, j],
                            "axis": [str(v) for v in axis],
                            **certify_nonnegative(-gap, strict=True),
                        }
                    )
        else:
            # A reference point selects a feature only. Its all-parameter bound is
            # the evidence; no sign at the reference point is accepted as a proof.
            axis, gap = max(features, key=lambda item: item[1].subs(REFERENCE))
            pair_bounds.append(
                {"pair": [i, j], "axis": [str(v) for v in axis], **certify_nonnegative(gap)}
            )
    if len(walls) != 44 or len(pair_bounds) != 53 or len(unavailable) != 14:
        raise ValueError("the complete wall/pair obligation set was not checked")
    return {
        "cosine_sine_positive": positivity,
        "wall_bounds": walls,
        "other_pair_bounds": pair_bounds,
        "unavailable_active_pair_features": unavailable,
        "feasible_iff_both_clearances_nonnegative_on_rectangle": True,
    }


def check_graph(atlas: Path = CONTACT_ATLAS) -> dict[str, Any]:
    """Prove graph asymmetry by invariant color refinement of the exact contact atlas."""
    entries = json.loads(atlas.read_text())["structures"]
    entry = next(item for item in entries if item["n"] == 11)
    if entry["arithmetic"] != "exact-algebraic":
        raise ValueError("the graph source must be the exact Trump contact entry")
    edges = sorted((int(row["left"]), int(row["right"])) for row in entry["pair_contacts"])
    if len(edges) != 14 or len(set(edges)) != 14:
        raise ValueError("expected fourteen distinct contacting pairs")
    adjacent = [
        {j if i == vertex else i for i, j in edges if vertex in (i, j)} for vertex in range(11)
    ]
    colors = [len(neighbors) for neighbors in adjacent]
    history = [colors]
    for _ in range(11):
        signatures = [
            (colors[i], tuple(sorted(colors[j] for j in adjacent[i]))) for i in range(11)
        ]
        palette = {signature: index for index, signature in enumerate(sorted(set(signatures)))}
        refined = [palette[signature] for signature in signatures]
        history.append(refined)
        if len(set(refined)) == 11:
            break
        if len(set(refined)) == len(set(colors)):
            raise ValueError("color refinement did not prove graph asymmetry")
        colors = refined
    else:
        raise ValueError("color refinement did not terminate")
    return {
        "source": atlas.relative_to(REPO).as_posix(),
        "edges": edges,
        "color_refinement": history,
        "automorphism_group_order": 1,
        "nontrivial_cell_action_preserves_original_square_contacts": False,
    }


def check() -> dict[str, Any]:
    """Produce a receipt for the bounded contact-family reconstruction and its scope."""
    construction = family()
    c, s = construction.cosine, construction.sine
    first_gap, second_gap = construction.gaps
    f1 = (6 * U + 4) / (1 + 2 * U - U**2)
    denominator = U**8 - 2 * U**7 - 2 * U**5 + 14 * U**4 + 2 * U**3 + 2 * U + 1
    f2 = 4 * (U + 1) * (U**6 - 2 * U**5 + 2 * U**4 + 7 * U**3 - 2 * U**2 + U + 1) / denominator
    polynomial = sp.Poly.from_list(list(U_MIN_POLY), U).as_expr()
    w = c * s
    determinant = sp.det(sp.Matrix(((1, w), (w, 1 + w))))
    identities = {
        "first_clearance": first_gap - (c + s) * (SIDE - f1),
        "second_clearance": second_gap - determinant / (c * s**2) * (SIDE - f2),
        "Fibonacci_determinant": determinant - (1 + w - w**2),
        "crossing_polynomial": f1
        - f2
        - 2 * U * polynomial / ((1 + 2 * U - U**2) * denominator),
    }
    for name, expression in identities.items():
        if sp.cancel(expression) != 0:
            raise ValueError(f"the exact identity failed: {name}")
    side_polynomial = sp.Poly.from_list(list(S_MIN_POLY), SIDE).as_expr()
    substituted_numerator = sp.fraction(sp.cancel(side_polynomial.subs(SIDE, f1)))[0]
    if sp.rem(substituted_numerator, polynomial, U) != 0:
        raise ValueError("the contact crossing does not imply the published side polynomial")

    slope_bounds = {
        "f1_prime_minus_quarter": certify_nonnegative(
            sp.diff(f1, U) - sp.Rational(1, 4), strict=True
        ),
        "minus_f2_prime_minus_quarter": certify_nonnegative(
            -sp.diff(f2, U) - sp.Rational(1, 4), strict=True
        ),
        "root_polynomial_prime": certify_nonnegative(sp.diff(polynomial, U), strict=True),
        "first_denominator": certify_nonnegative(1 + 2 * U - U**2, strict=True),
        "second_denominator": certify_nonnegative(denominator, strict=True),
        "clearance_side_coefficient": certify_nonnegative(
            determinant / (c * s**2), strict=True
        ),
    }
    root_signs = [polynomial.subs(U, end) for end in U_INTERVAL]
    if not root_signs[0].is_negative or not root_signs[1].is_positive:
        raise ValueError("the crossing root is not bracketed")
    side_range = [f1.subs(U, end) for end in U_INTERVAL]
    if not SIDE_INTERVAL[0] < side_range[0] < side_range[1] < SIDE_INTERVAL[1]:
        raise ValueError("the crossing point is outside the certified side rectangle")

    return {
        "schema": "fibonacci-torus-geometry/v1",
        "passed": True,
        "scope": "independent contact reconstruction on an explicit closed parameter rectangle",
        "screenshot_manuscript_theorem_fully_verified": False,
        "unrestricted_global_capture_proved": False,
        "u_interval": [str(value) for value in U_INTERVAL],
        "side_interval": [str(value) for value in SIDE_INTERVAL],
        "f1": str(f1),
        "f2": str(f2),
        "crossing_polynomial": str(polynomial),
        "identities": dict.fromkeys(identities, True),
        "side_polynomial_divisibility": True,
        "root_endpoint_values": [str(v) for v in root_signs],
        "side_root_enclosure": [str(v) for v in side_range],
        "slope_bounds": slope_bounds,
        "cusp_bound": "L - T_star >= abs(u - u_star)/4",
        "rectangle_geometry": check_rectangle(construction),
        "contact_graph": check_graph(),
    }


def main() -> None:
    """Write the complete exact receipt to stdout for retention by the caller."""
    print(json.dumps(check(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()


## Tests


def test_bernstein_refuses_interior_negative_polynomial() -> None:
    lo, hi = U_INTERVAL
    polynomial = (U - lo) * (U - hi) + sp.Rational(1, 10**8)
    assert polynomial.subs(U, lo) > 0
    assert polynomial.subs(U, hi) > 0
    try:
        certify_nonnegative(polynomial)
    except ValueError:
        pass
    else:
        raise AssertionError("positive endpoints hid a negative interior")


def test_bernstein_refuses_negative_denominator() -> None:
    lo, hi = U_INTERVAL
    try:
        certify_nonnegative(1 / ((U - lo) * (U - hi) + sp.Rational(1, 10**8)))
    except ValueError:
        pass
    else:
        raise AssertionError("a denominator with interior poles was accepted")
