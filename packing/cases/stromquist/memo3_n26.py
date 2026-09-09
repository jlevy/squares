"""Exact reconstruction of Stromquist's Memo III, Figure 4(b), for 26 squares.

The source prints side 5.650629 and tilt 27.583 degrees, without an equation.
David Ellsworth's 2023 SVG supplies a cubic and six translated 1-by-2 dominoes.
Here all coordinates are reconstructed in the cubic side field and every unit
edge, wall inequality, and pair is checked with exact algebraic predicates.

The six dominoes do not form a rigid 3-by-4 rectangle: their small relative
slides matter. This verifies a historical construction, not optimality, and
does not improve Friedman's smaller, already known 26-square construction.

Run from packing/: uv run --frozen python -m cases.stromquist.memo3_n26.
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path

from sqpack.cover import write_text_atomic
from sqpack.field import FieldElement, NumberField
from sqpack.verify import exact_sign, verify_packing

type Point = tuple[FieldElement, FieldElement]
type Square = tuple[Point, Point, Point, Point]

MINIMAL_POLYNOMIAL = (1, -14, 67, -112)
ISOLATING = (Fraction(5650, 1000), Fraction(5651, 1000))
SOURCE_PDF = (
    "packing/resources/papers/"
    "stromquist-1984-packing-unit-squares-inside-squares-iii-cases-through-65-"
    "and-gardner-conjecture.pdf"
)
SOURCE_SVG = "https://kingbird.myphotos.cc/packing/square-26_r2.svg"


def side_polynomial(value: FieldElement) -> FieldElement:
    """The cubic for the side; its derivative is ((3*x - 14)^2 + 5)/3 > 0."""
    return ((value - 14) * value + 67) * value - 112


def parameters(field: NumberField) -> dict[str, FieldElement]:
    """Reconstruct the SVG's trigonometric quantities without rounded angles."""
    side = field.alpha
    sine = (-(side**2) + 9 * side - 18) / 2
    cosine = (side**2 - 11 * side + 32) / 2
    tangent = sine / cosine
    if not side_polynomial(side).is_zero():
        raise ValueError("side does not satisfy its defining cubic")
    if not (sine**2 + cosine**2 - 1).is_zero():
        raise ValueError("reconstructed orientation is not a unit vector")
    if min(sine.sign(), cosine.sign()) <= 0 or (cosine - sine).sign() <= 0:
        raise ValueError("orientation is outside the source's first 45 degrees")
    if not (8 * tangent**3 - 5 * tangent**2 + 10 * tangent - 5).is_zero():
        raise ValueError("orientation does not satisfy the SVG's tangent cubic")
    x1 = 1 - (side - 2) * cosine / sine + 4 / sine
    if not (x1 - (side - 3)).is_zero():
        raise ValueError("the first domino's top-wall anchor was reconstructed incorrectly")
    x2 = 1 - (side - 5) * sine * cosine + 2 * sine
    y2 = side - 2 - (side - 5) * sine**2 - 2 * cosine
    dx = ((side - 2) * (1 + cosine / sine) - 4 / sine + cosine * (-1 + (side - 5) * sine)) / 2
    dy = 1 + sine * (-1 + (side - 5) * sine) / 2
    return {
        "side": side,
        "sin_theta": sine,
        "cos_theta": cosine,
        "tan_theta": tangent,
        "x1": x1,
        "x2": x2,
        "y2": y2,
        "dx": dx,
        "dy": dy,
    }


def build() -> tuple[list[Square], FieldElement, NumberField]:
    """Build fourteen boundary squares and twelve tilted squares exactly."""
    field = NumberField(MINIMAL_POLYNOMIAL, ISOLATING)
    values = parameters(field)
    side = values["side"]
    sine, cosine = values["sin_theta"], values["cos_theta"]
    q = field.rational

    def square(origin: Point, horizontal: Point, vertical: Point) -> Square:
        x, y = origin
        ux, uy = horizontal
        vx, vy = vertical
        return (x, y), (x + ux, y + uy), (x + ux + vx, y + uy + vy), (x + vx, y + vy)

    origins = (
        (q(0), q(0)),
        (q(1), q(0)),
        (q(0), q(1)),
        (q(0), q(2)),
        (q(0), side - 1),
        (q(1), side - 1),
        (q(0), side - 2),
    )
    boundary = [square(point, (q(1), q(0)), (q(0), q(1))) for point in origins]
    boundary += [
        square((side - x - 1, side - y - 1), (q(1), q(0)), (q(0), q(1))) for x, y in origins
    ]
    seeds = ((values["x1"], q(0)), (values["x2"], values["y2"]))
    tilted = [
        square(
            (x + column * values["dx"] - row * sine, y + column * values["dy"] + row * cosine),
            (cosine, sine),
            (-sine, cosine),
        )
        for column in range(3)
        for x, y in seeds
        for row in range(2)
    ]
    pieces = boundary + tilted
    if len(boundary) != 14 or len(tilted) != 12 or len(pieces) != 26:
        raise ValueError("construction does not contain exactly 14 + 12 unit squares")
    return pieces, side, field


def comparisons(field: NumberField) -> dict[str, dict[str, object]]:
    """Compare four historical sides by exact signs, with rigorous gap intervals.

    The cubic is strictly increasing on the real line. Consequently the sign
    of p(comparator) is exactly the sign of comparator minus its unique root.
    The midpoint labels are display approximations; rational endpoints and
    polynomial signs carry the comparison.
    """
    root2_field = NumberField((1, 0, -2), (1, 2))
    root2 = root2_field.alpha
    q = root2_field.rational
    candidates = {
        "gobel": ("5 + sqrt(2)/2", q(5) + root2 / 2),
        "stenlund": ("5/2 + 9*sqrt(2)/4", q(Fraction(5, 2)) + 9 * root2 / 4),
        "friedman": ("7/2 + 3*sqrt(2)/2", q(Fraction(7, 2)) + 3 * root2 / 2),
    }
    field.refine_to(40)
    root2_field.refine_to(40)
    memo_lo, memo_hi = field.root_bounds()
    result: dict[str, dict[str, object]] = {}
    for name, (formula, candidate) in candidates.items():
        evaluation = side_polynomial(candidate)
        direction = evaluation.sign()
        lo, hi = root2_field.enclose(candidate)
        gap = memo_lo - hi, memo_hi - lo
        if direction == 0 or (direction > 0 and gap[1] >= 0) or (direction < 0 and gap[0] <= 0):
            raise ValueError(f"the exact sign and gap enclosure disagree for {name}")
        result[name] = {
            "formula": formula,
            "side_decimal": root2_field.decimal(candidate, 30),
            "p_at_comparator_in_q_sqrt2": [str(value) for value in evaluation.coeffs],
            "p_at_comparator_sign": direction,
            "memo_minus_comparator_interval": [str(value) for value in gap],
            "memo_minus_comparator_approx": float(sum(gap) / 2),
            "memo_is_smaller": direction > 0,
        }
    return result


def verified_record() -> dict[str, object]:
    """Refuse an invalid construction or a passing negative control; emit evidence."""
    pieces, side, field = build()
    report = verify_packing(pieces, side, sign=exact_sign)
    if not report.valid or report.n != 26 or report.pairs_tested != 325:
        raise ValueError(f"exact geometry verification failed: {report}")
    duplicate = verify_packing([*pieces, pieces[-1]], side, sign=exact_sign)
    shrunken = verify_packing(pieces, side - Fraction(1, 1_000_000), sign=exact_sign)
    if duplicate.valid or shrunken.valid:
        raise ValueError("a duplicate or a container shrunk by 10^-6 passed verification")
    values = parameters(field)
    compared = comparisons(field)
    return {
        "schema_version": 1,
        "scope": "exact-algebraic-historical-construction",
        "n": 26,
        "construction_verified": True,
        "optimality_proved": False,
        "improves_current_best_known": compared["friedman"]["memo_is_smaller"],
        "sources": {
            "memo": {"pdf": SOURCE_PDF, "pages": [2, 5], "figure": "4(b)"},
            "coordinate_reconstruction": {
                "url": SOURCE_SVG,
                "credited_to": "David Ellsworth",
                "dated": "2023-05-31",
            },
        },
        "side_decimal": field.decimal(side, 30),
        "minimal_polynomial_high_to_low": list(MINIMAL_POLYNOMIAL),
        "field_preconditions": field.precondition_certificate(),
        "parameters_in_q_side": {
            name: [str(value) for value in scalar.coeffs] for name, scalar in values.items()
        },
        "coordinates_in_q_side": [
            [[[str(value) for value in scalar.coeffs] for scalar in point] for point in piece]
            for piece in pieces
        ],
        "checks": {
            "unit_square_count": report.n,
            "all_pairs": report.pairs_tested,
            "touching_pairs": report.touching_pairs,
            "strictly_separated_pairs": report.strict_pairs,
            "boundary_corner_coordinates": report.container_contacts,
            "duplicate_rejected": not duplicate.valid,
            "container_shrunk_by_1e_minus_6_rejected": not shrunken.valid,
        },
        "comparison_justification": "p'(x) = ((3*x - 14)^2 + 5)/3 > 0 for every real x",
        "comparisons": compared,
    }


def main() -> int:
    """Emit JSON and optionally retain exactly the same rebuilt evidence."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="retain the full verified JSON record")
    args = parser.parse_args()
    text = json.dumps(verified_record(), indent=2, sort_keys=True) + "\n"
    if args.output is not None:
        write_text_atomic(args.output, text)
    print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
