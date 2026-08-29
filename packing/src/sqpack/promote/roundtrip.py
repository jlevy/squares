"""Close the exact route: from a minimal polynomial back to a verified packing.

[`solve.discharge`](solve.py) takes a recovered relation as far as an algebraic claim
about the *side* -- irreducible over `Q`, with an isolating interval containing the
refined value -- and stops there, saying so in its own docstring.  What it cannot say is
that the number it isolated is the side of a packing that exists.  A wrong contact
structure can yield a valid but *suboptimal* packing, and verification alone does not
catch that: it catches infeasibility.  Only rebuilding the packing from the recovered
field and comparing the reconstructed side against the input closes the loop.

**The obstacle, and why it is not fatal.**  The pose unknowns include angles, and an
angle is transcendental: `t_i` has no representation in `Q(s)` at all, so "solve every
pose unknown exactly" is unsatisfiable while the pose is parameterised by angles.  What
makes `n = 11` reachable is that its retained construction is not.  `cases.trump11` is
already written over `Q(u)` with `u = tan(a/2)`, so every coordinate is built from
`+ - * /` alone, and the whole question becomes whether `u` can be recovered from `s`.

**It can, and by derivation rather than by search.**  `Q(s) = Q(u)` -- both are degree
eight -- so `u` is a rational combination of powers of `s`, and finding it is an exact
linear solve over `Q` rather than an integer-relation guess.  Write each `s^i` in the
power basis of `Q(u)`, and solve the resulting square rational system for the
coefficients that reproduce `u`.  :func:`generator_in_powers_of` does that and refuses,
rather than returning a least-squares answer, when the matrix is singular -- which is
exactly the case `Q(s)` is a proper subfield and no such combination exists.

An integer-relation search would have found the same coefficients and would have had to
be believed.  This derives them, and then still checks: the recovered `u` is required to
satisfy `u`'s own minimal polynomial exactly, in the new field, which a wrong answer
cannot do.

**Why the side comparison is exact here rather than approximate.**  Rebuilding inside
`Q(s)` makes the reconstructed side an element of the same field as the generator, so
"the reconstruction has the side it started from" is `(side - alpha).is_zero()` -- one
exact identity, with no cross-field comparison and no tolerance.  That is the spec's
mandatory side comparison, and it is the step that would catch a structure yielding a
valid-but-suboptimal packing.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass
from fractions import Fraction

from sqpack.field import FieldElement, NumberField
from sqpack.verify import exact_sign, verify_packing


class RoundTripError(ValueError):
    """A stage of the round trip refused, with a kind naming which one."""

    def __init__(self, kind: str, detail: str) -> None:
        super().__init__(f"{kind}: {detail}")
        self.kind = kind
        self.detail = detail


@dataclass(frozen=True)
class Certificate:
    """A packing rebuilt from a recovered field, and what was checked of it."""

    #: Degree of the field the packing was rebuilt in.
    degree: int
    #: Coefficients expressing the construction's generator in powers of the side,
    #: lowest power first.  Derived, not searched.
    generator_in_side: tuple[Fraction, ...]
    #: Whether the recovered generator satisfies its own minimal polynomial exactly.
    generator_certified: bool
    #: Whether the rebuilt packing passed `verify_packing` under `exact_sign`.
    packing_valid: bool
    #: Whether the reconstructed side equals the field generator exactly.
    side_matches: bool
    squares_verified: int
    touching_pairs: int
    refusal: str | None = None

    @property
    def closed(self) -> bool:
        return (
            self.generator_certified
            and self.packing_valid
            and self.side_matches
            and self.refusal is None
        )


def _solve_exact(matrix: list[list[Fraction]], target: list[Fraction]) -> list[Fraction]:
    """Gauss-Jordan over `Q`, refusing a singular system rather than approximating it.

    Singular here is not a numerical accident; it is the statement that the element the
    caller is trying to express does not lie in the subfield it named.
    """
    size = len(target)
    augmented = [[*row, target[index]] for index, row in enumerate(matrix)]
    for column in range(size):
        pivot = next((row for row in range(column, size) if augmented[row][column] != 0), None)
        if pivot is None:
            raise RoundTripError(
                "subfield-too-small",
                f"the power basis is singular at column {column}, so the generator is "
                "not a rational combination of powers of the element supplied; the "
                "element generates a proper subfield",
            )
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        scale = augmented[column][column]
        augmented[column] = [value / scale for value in augmented[column]]
        for row in range(size):
            if row != column and augmented[row][column] != 0:
                factor = augmented[row][column]
                augmented[row] = [
                    a - factor * b
                    for a, b in zip(augmented[row], augmented[column], strict=True)
                ]
    return [augmented[index][size] for index in range(size)]


def generator_in_powers_of(field: NumberField, element: FieldElement) -> tuple[Fraction, ...]:
    """Express `field.alpha` as a rational combination of powers of `element`.

    Returns the coefficients lowest power first, so that
    `sum(c[i] * element**i) == field.alpha`.  Refuses when `element` generates a proper
    subfield, which is the honest answer rather than a nearest fit.
    """
    degree = field.degree
    columns: list[list[Fraction]] = []
    power = field.one
    for _ in range(degree):
        coefficients = list(power.coeffs) + [Fraction(0)] * (degree - len(power.coeffs))
        columns.append(coefficients[:degree])
        power = power * element
    matrix = [[columns[column][row] for column in range(degree)] for row in range(degree)]
    target = [Fraction(0)] * degree
    target[1] = Fraction(1)
    return tuple(_solve_exact(matrix, target))


def _horner(
    coefficients: Sequence[int], value: FieldElement, field: NumberField
) -> FieldElement:
    accumulator = field.zero
    for coefficient in coefficients:
        accumulator = accumulator * value + field.rational(coefficient)
    return accumulator


def certify(
    *,
    side_min_poly: Sequence[int],
    side_interval: tuple[str, str],
    generator_min_poly: Sequence[int],
    generator_in_side: Sequence[Fraction],
    build: Callable[[NumberField, FieldElement], tuple[list, FieldElement]],
) -> Certificate:
    """Rebuild a packing inside `Q(side)` and check every claim the rebuild makes.

    `build` receives the new field and the recovered generator and returns
    `(squares, side)` in that field, using the same closed forms the retained
    construction uses.  Nothing here trusts it: the generator is certified against its
    own minimal polynomial first, the packing is verified with `exact_sign`, and the
    side it reconstructs is required to be the field generator exactly.
    """
    field = NumberField(side_min_poly, side_interval)
    # A running product rather than exponentiation: FieldElement carries no __pow__,
    # and adding one for this would be a wider change than the round trip needs.
    generator = field.zero
    power = field.one
    for coefficient in generator_in_side:
        generator = generator + field.rational(coefficient) * power
        power = power * field.alpha

    certified = _horner(generator_min_poly, generator, field).is_zero()
    if not certified:
        return Certificate(
            degree=field.degree,
            generator_in_side=tuple(generator_in_side),
            generator_certified=False,
            packing_valid=False,
            side_matches=False,
            squares_verified=0,
            touching_pairs=0,
            refusal=(
                "the recovered generator does not satisfy its own minimal polynomial in "
                "the rebuilt field, so it is not the number the construction needs"
            ),
        )

    squares, side = build(field, generator)
    report = verify_packing(squares, side, sign=exact_sign)
    matches = (side - field.alpha).is_zero()
    refusal = None
    if not matches:
        refusal = (
            "the reconstructed side is not the root the field was built on; the "
            "reconstruction is a different packing, which validity alone would not catch"
        )
    return Certificate(
        degree=field.degree,
        generator_in_side=tuple(generator_in_side),
        generator_certified=True,
        packing_valid=bool(report.valid),
        side_matches=bool(matches),
        squares_verified=report.n,
        touching_pairs=report.touching_pairs,
        refusal=refusal,
    )
