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
    """A weighted site in the container. Coordinates and weight are exact."""

    label: str
    x: Fraction
    y: Fraction
    weight: Fraction


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
