"""Exact primitives for weighted fractional unavoidable-set certificates.

Deliberately independent of `cases.n17_weighted_certificate`, which holds the
frozen replay of one published certificate. Sharing types with the frozen
package would make the n = 17 positive control a check of a module against
itself; keeping them apart makes it a check of two implementations against a
published number.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True, slots=True)
class Atom:
    """A weighted site in the container. Coordinates and weight are exact.

    The value type admits any rational weight so that a caller can build a
    forgery and watch it refused; the theorem does not. Every proof entry
    point runs ``require_nonnegative_atom_weights`` before it decides anything.
    """

    label: str
    x: Fraction
    y: Fraction
    weight: Fraction


def require_nonnegative_atom_weights(atoms: tuple[Atom, ...]) -> None:
    """Refuse a signed weight: the counting argument needs every weight >= 0.

    The proof bounds the mass of pairwise disjoint inner squares by the total
    mass of the atoms. That step is monotonicity of the measure, and it fails
    the moment a weight is negative: five atoms -- +2 at the centre of a side
    11/10 container and -1 at each corner -- carry total mass -2 < 1, cover
    every admissible 3/5-square with mass at least 1, and would "prove"
    s(1) >= 11/10. Found by the adversarial review of PR 78 (its F1).
    """

    for atom in atoms:
        if atom.weight < 0:
            raise ValueError(
                f"atom {atom.label} has weight {atom.weight} < 0; the certificate theorem "
                "needs every weight nonnegative"
            )


@dataclass(frozen=True, slots=True)
class Direction:
    """An exact rotation, as the image of the two axes."""

    label: str
    ux: Fraction
    uy: Fraction
    vx: Fraction
    vy: Fraction

    def __post_init__(self) -> None:
        if self.ux * self.vy == self.uy * self.vx:
            raise ValueError("direction axes must be linearly independent")
        if self.ux * self.ux + self.uy * self.uy != 1:
            raise ValueError("direction must be exactly unit length")


def rotation_from_half_tangent(label: str, tangent: Fraction) -> Direction:
    """The exact rotation by ``2 arctan(tangent)``.

    The half-angle parametrisation is what keeps a direction net rational: no
    angle in this file is ever a float, and the unit-length check in
    ``Direction`` is an equality rather than a tolerance.
    """
    denominator = 1 + tangent * tangent
    cosine = (1 - tangent * tangent) / denominator
    sine = 2 * tangent / denominator
    return Direction(label, cosine, sine, -sine, cosine)
