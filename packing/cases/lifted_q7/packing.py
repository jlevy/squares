"""The retained `n = 18` and `n = 86` witnesses, lifted exactly into `Q(sqrt 7)`.

Hämäläinen's 18 (1980) and Friedman's 86 (1997) share one tilt class, and `[Friedman
DS7]` names it exactly: `arcsin((sqrt(7) - 1)/4)`, with the 86 obtained by generalising
the 18 "and the angle is the same". No generating rule is stated for either figure, so as
at `cases/lifted_q2` there is nothing to derive -- but every retained coordinate lifts
into `Q(sqrt 7)` at small height, and the tilt's exact cosine and sine,
`(1 + sqrt(7))/4` and `(sqrt(7) - 1)/4`, satisfy the circle identity in the field:
`(1 + sqrt 7)^2 + (sqrt 7 - 1)^2 = 16`.

The lift is a candidate generator and `verify_packing` under `exact_sign` is the proof,
provenance-free (`D-398`); this is the operation `D-402` does not foreclose, because the
field is known from the published exact sides `(7 + sqrt(7))/2` and `(17 + sqrt(7))/2`.
The lift re-runs from the witness file at every verification and the side lift is pinned
to the published form, exactly as in `cases/lifted_q2`.

Nothing here claims optimality.
"""

from __future__ import annotations

from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path

from cases.gobel40.packing import corners
from sqpack.field import FieldElement, NumberField
from sqpack.witness import load_witness

SOURCE = "[Friedman DS7] sections 2 and 4: Hamalainen's 18 and Friedman's 86"
SOURCE_URL = "https://kingbird.myphotos.cc/packing/"

ROOT = Path(__file__).resolve().parent.parent.parent
WITNESSES = ROOT / "witnesses" / "known-best"
WITNESS_SCHEMA = ROOT / "witnesses" / "witness.schema.yaml"

MAX_DENOMINATOR = 48
LIFT_TOLERANCE = Decimal("1e-24")

#: The published exact side as a lift triple (p, q, d) meaning (p + q sqrt(7)) / d.
SIDES: dict[int, tuple[int, int, int]] = {
    18: (7, 1, 2),  # (7 + sqrt(7)) / 2
    86: (17, 1, 2),  # (17 + sqrt(7)) / 2
}

#: The shared tilt class, in degrees as the witnesses print it (their last digit
#: differs by one unit of their own rounding between the two files).
TILT_PREFIX = "24.295188945364570330759748906"


def lift(value: Decimal) -> tuple[int, int, int] | None:
    """The unique small `(p + q sqrt(7)) / d` within tolerance of `value`, or None."""
    with localcontext() as context:
        context.prec = 50
        root = Decimal(7).sqrt()
        for d in range(1, MAX_DENOMINATOR + 1):
            target = value * d
            for q in range(-24 * d, 24 * d + 1):
                p_decimal = target - q * root
                p = int(p_decimal.to_integral_value(rounding="ROUND_HALF_EVEN"))
                if abs(p_decimal - p) < LIFT_TOLERANCE * d:
                    return (p, q, d)
    return None


def build(
    n: int,
) -> tuple[list[list[tuple[FieldElement, FieldElement]]], FieldElement, NumberField]:
    """Exact corners, side, and the degree-two field for the lifted witness at `n`."""
    if n not in SIDES:
        raise ValueError(f"n={n}: no declared side lift; this package covers {sorted(SIDES)}")

    field = NumberField((1, 0, -7), (2, 3))
    root = field.alpha
    q = field.rational
    half = q(1) / q(2)
    cosine = (q(1) + root) / q(4)
    sine = (root - q(1)) / q(4)
    assert cosine * cosine + sine * sine == q(1), "the tilt is not on the unit circle"

    def element(triple: tuple[int, int, int]) -> FieldElement:
        p, coefficient, d = triple
        return q(Fraction(p, d)) + q(Fraction(coefficient, d)) * root

    witness = load_witness(WITNESSES / f"n-{n:03d}.yaml", fallback_schema=WITNESS_SCHEMA)
    side_triple = lift(Decimal(str(witness["side"])))
    assert side_triple == SIDES[n], (
        f"n={n}: witness side lifts to {side_triple}, expected {SIDES[n]}"
    )
    side = element(SIDES[n])

    squares = []
    for square in witness["squares"]:
        centre = []
        for coordinate in square["center"]:
            triple = lift(Decimal(str(coordinate)))
            assert triple is not None, f"n={n}: coordinate {coordinate} does not lift"
            centre.append(element(triple))
        angle = str(square["angle"])
        if angle == "0":
            squares.append(corners((centre[0], centre[1]), (half, q(0)), (q(0), half)))
        elif angle.startswith(TILT_PREFIX):
            squares.append(
                corners(
                    (centre[0], centre[1]),
                    (cosine / q(2), sine / q(2)),
                    (-sine / q(2), cosine / q(2)),
                )
            )
        else:
            raise AssertionError(f"n={n}: unexpected angle {angle}")

    assert len(squares) == n, (len(squares), n)
    return squares, side, field
