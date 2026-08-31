"""The retained `n = 19` and `n = 66` witnesses, lifted exactly into `Q(sqrt 2)`.

Wainwright's 19 (1979) and Stenlund's 66 (1980) are diagonal-strip packings of width two
and three whose published sides are `3 + (4/3) sqrt(2)` and `3 + 4 sqrt(2)`, but for which
`[Friedman DS7]` states no generating rule -- only the figures and, for 66, the sentence
that the diagonal squares touch only the corner squares of the staircases. So unlike
`cases/gobel_strip`, there is no construction to derive. What there is instead is a
witness whose every coordinate lies in the field the published side names, at small
height: each centre lifts to `(p + q sqrt(2)) / d` with `d <= 3` at `n = 19` and `d = 1`
or `2` at `n = 66`, agreeing with the retained decimal to its full declared precision.

The lift is a candidate generator, not a proof: the proof is `verify_packing` under
`exact_sign` on the lifted pose, whose verdict is independent of where the candidate came
from. A feasible packing at side `s`, decided exactly, is a proof that `s(n) <= s`
(`D-398`), so these two certificates carry exactly that and nothing else.

This is the operation `D-402` does **not** foreclose: the field is known from the
published exact side, so the question is expressing coordinates in a fixed
two-dimensional basis at small height -- not recovering an unknown minimal polynomial
from decimals, which `BC-049` measured at reach zero and which stays out of reach.

The lift re-runs from the witness file at every verification, deterministically
(round-half-even, tolerance `1e-24`, denominators to 48), so the witness stays the single
source of truth and a changed witness changes the verdict rather than silently diverging
from an embedded copy. The side's lift is additionally pinned to the published exact form
by literal `(p, q, d)` triples, so a witness edit cannot quietly move the certified bound.

Nothing here claims optimality.
"""

from __future__ import annotations

from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path

from cases.gobel40.packing import corners
from sqpack.field import FieldElement, NumberField
from sqpack.witness import load_witness

SOURCE = "[Friedman DS7] sections 2 and 4: Wainwright's 19 and Stenlund's 66"
SOURCE_URL = "https://kingbird.myphotos.cc/packing/"

ROOT = Path(__file__).resolve().parent.parent.parent
WITNESSES = ROOT / "witnesses" / "known-best"
WITNESS_SCHEMA = ROOT / "witnesses" / "witness.schema.yaml"

MAX_DENOMINATOR = 48
LIFT_TOLERANCE = Decimal("1e-24")

#: The published exact side as a lift triple (p, q, d) meaning (p + q sqrt(2)) / d.
SIDES: dict[int, tuple[int, int, int]] = {
    19: (9, 4, 3),  # 3 + (4/3) sqrt(2)
    66: (3, 4, 1),  # 3 + 4 sqrt(2)
}


def lift(value: Decimal) -> tuple[int, int, int] | None:
    """The unique small `(p + q sqrt(2)) / d` within tolerance of `value`, or None.

    Uniqueness within the search box is a property of the box: two distinct candidates
    `(p + q sqrt(2)) / d` at these heights differ by at least about `1e-4`, far above
    the tolerance, so the first hit is the only hit.
    """
    with localcontext() as context:
        context.prec = 50
        root = Decimal(2).sqrt()
        for d in range(1, MAX_DENOMINATOR + 1):
            target = value * d
            for q in range(-12 * d, 12 * d + 1):
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

    field = NumberField((1, 0, -2), (1, 2))
    root = field.alpha
    q = field.rational
    half = q(1) / q(2)
    diagonal = root / q(4)

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
        elif angle == "45.0":
            squares.append(
                corners((centre[0], centre[1]), (diagonal, diagonal), (-diagonal, diagonal))
            )
        else:
            raise AssertionError(f"n={n}: unexpected angle {angle}; the lift covers 0 and 45")

    assert len(squares) == n, (len(squares), n)
    return squares, side, field
