"""Weighted fractional unavoidable-set certificates for square packing.

A certificate is the Burns--Massaccesi object: an outer side ``L``, a shrunken
square side ``B``, rational-weight atoms in the container, and a rational
direction net reaching pi/4. It proves ``s(n) >= L / B`` when four conditions
hold together, so the conditions are named here rather than left to a caller:

``C1``  the total atom mass is strictly below ``n``.
``C2``  the direction net reaches pi/4, which the container's D4 symmetry needs
        in order to reduce every angle to the net's arc.
``C3``  ``B (1 + D) < 1`` for ``D`` the largest half-gap tangent of the net.
        A unit square at any angle then contains a ``B``-square at some net
        angle, because ``cos d + sin d <= 1 + tan d``.
``C4``  every event cell the ``B``-square sweep can reach, at every net
        direction, carries mass at least 1.

Given all four: ``n`` disjoint unit squares would contain ``n`` disjoint
``B``-squares at net angles, each covering mass at least 1 by ``C4``, for a
total of at least ``n`` -- which ``C1`` forbids. So ``n`` unit squares do not
fit in a container of side ``L / B``.

The arithmetic is exact throughout. Every quantity is a ``Fraction``; nothing
here rounds, samples an angle, or compares against a tolerance.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction
from itertools import pairwise

from sqpack.fractional.model import Atom, Direction, rotation_from_half_tangent
from sqpack.fractional.sweep import minimum_covered_mass

#: tan(pi/8), the half-angle tangent at pi/4. A net reaching this reaches pi/4.
HALF_ANGLE_LIMIT_SQUARED = Fraction(2)


@dataclass(frozen=True, slots=True)
class ConditionReport:
    """One condition's verdict, with the numbers it was decided on.

    ``holds`` is keyword-only: a bare ``True`` sitting between two strings at a
    call site reads as noise, and this value is the verdict.
    """

    name: str
    detail: str
    holds: bool = field(kw_only=True)


@dataclass(frozen=True, slots=True)
class Verdict:
    conditions: tuple[ConditionReport, ...]
    total_mass: Fraction
    minimum_cell_mass: Fraction | None
    worst_direction: str | None

    @property
    def accepted(self) -> bool:
        return all(condition.holds for condition in self.conditions)

    @property
    def failures(self) -> tuple[str, ...]:
        return tuple(c.name for c in self.conditions if not c.holds)


@dataclass(frozen=True, slots=True)
class Certificate:
    """A candidate weighted fractional unavoidable set at one (n, L, B)."""

    n: int
    outer_side: Fraction
    square_side: Fraction
    atoms: tuple[Atom, ...]
    half_tangents: tuple[Fraction, ...]
    symmetry: str = "D4"

    def __post_init__(self) -> None:
        if self.n < 1:
            raise ValueError("n must be positive")
        if self.outer_side <= 0 or self.square_side <= 0:
            raise ValueError("sides must be positive")
        if len(self.half_tangents) < 2:
            raise ValueError("the direction net needs at least two directions")
        if list(self.half_tangents) != sorted(set(self.half_tangents)):
            raise ValueError("half-angle tangents must be strictly increasing")
        if self.half_tangents[0] != 0:
            raise ValueError("the direction net must start at angle zero")

    @property
    def total_mass(self) -> Fraction:
        return sum((atom.weight for atom in self.atoms), start=Fraction(0))

    @property
    def bounded_side(self) -> Fraction:
        """The side the certificate bounds: ``L`` itself.

        ``B`` does not divide out here, and getting that wrong inflates the
        result. The shrunken square is not a rescaling of the container; it
        sits *inside* a unit square that is itself inside the side-``L``
        container, and it exists only so that ``C3`` can absorb the net's
        angular gap. So the contradiction is about ``n`` unit squares in side
        ``L``, and what the certificate proves is ``s(n) > L``. Reported as
        ``>= L``, which is what a bound register carries.

        Checked against the retained n = 17 certificate: ``L = 22529/5000`` is
        exactly Massaccesi's published 4.5058, while ``L / B`` would claim
        4.51799 and overstate a published result.
        """
        return self.outer_side

    @property
    def directions(self) -> tuple[Direction, ...]:
        """The net as exact unit rotations, via the half-angle parametrisation."""
        return tuple(
            rotation_from_half_tangent(str(index), tangent)
            for index, tangent in enumerate(self.half_tangents)
        )

    @property
    def largest_half_gap_tangent(self) -> Fraction:
        """``D``: the largest ``tan`` of a half-gap between adjacent net angles.

        With ``t = tan(theta / 2)``, the angle between two net directions has
        ``tan = (t2 - t1) / (1 + t1 t2)``, which stays rational; the half-gap is
        half of an adjacent pair's separation, so the tangent of the half-gap is
        that same expression on the pair's midpoint split. Taking the whole gap
        is the conservative choice and is what this returns.
        """
        return max(
            (right - left) / (1 + left * right) for left, right in pairwise(self.half_tangents)
        )


def _condition_mass_below_n(certificate: Certificate) -> ConditionReport:
    total = certificate.total_mass
    return ConditionReport(
        "C1 total mass below n",
        f"total {total} against n = {certificate.n}",
        holds=total < certificate.n,
    )


def _condition_arc_reaches_eighth_turn(certificate: Certificate) -> ConditionReport:
    """The net must reach pi/4, i.e. its last half-tangent reaches tan(pi/8).

    ``tan(pi/8) = sqrt(2) - 1`` is irrational, so the test is the exact
    equivalent ``t^2 + 2t - 1 >= 0`` on the final tangent.
    """
    last = certificate.half_tangents[-1]
    slack = last * last + 2 * last - 1
    return ConditionReport(
        "C2 net reaches pi/4",
        f"final half-tangent {last}, t^2 + 2t - 1 = {slack}",
        holds=slack >= 0,
    )


def d4_images(
    x: Fraction, y: Fraction, outer_side: Fraction
) -> tuple[tuple[Fraction, Fraction], ...]:
    """The eight images of a point under the container's symmetry group."""
    far_x, far_y = outer_side - x, outer_side - y
    return (
        (x, y),
        (far_x, y),
        (x, far_y),
        (far_x, far_y),
        (y, x),
        (far_y, x),
        (y, far_x),
        (far_y, far_x),
    )


def _condition_symmetric_atoms(certificate: Certificate) -> ConditionReport:
    """The atom set must carry the symmetry ``C2`` claims to exploit.

    ``C2`` only checks that the net *reaches* pi/4; what makes stopping there
    sound is that a square at any angle in (pi/4, pi/2) reflects to one in
    [0, pi/4] across a symmetry of both the container and the atom set. Declare
    that symmetry without holding it and every angle past pi/4 goes unchecked,
    so this decides it rather than trusting the declaration.
    """
    if certificate.symmetry != "D4":
        return ConditionReport(
            "C0 atoms carry the declared symmetry",
            f"only D4 is supported, not {certificate.symmetry!r}",
            holds=False,
        )
    weights: dict[tuple[Fraction, Fraction], Fraction] = {}
    for atom in certificate.atoms:
        key = (atom.x, atom.y)
        if key in weights:
            return ConditionReport(
                "C0 atoms carry the declared symmetry",
                f"two atoms share the site {key}",
                holds=False,
            )
        weights[key] = atom.weight
    for atom in certificate.atoms:
        for image in d4_images(atom.x, atom.y, certificate.outer_side):
            if weights.get(image) != atom.weight:
                return ConditionReport(
                    "C0 atoms carry the declared symmetry",
                    f"site ({atom.x}, {atom.y}) has no matching image at {image}",
                    holds=False,
                )
    return ConditionReport(
        "C0 atoms carry the declared symmetry",
        f"{len(certificate.atoms)} atoms closed under D4 about the centre",
        holds=True,
    )


def _condition_containment(certificate: Certificate) -> ConditionReport:
    gap = certificate.largest_half_gap_tangent
    product = certificate.square_side * (1 + gap)
    return ConditionReport(
        "C3 containment B(1 + D) < 1",
        f"B = {certificate.square_side}, D = {gap}, B(1 + D) = {float(product):.9f}",
        holds=product < 1,
    )


def sweep_direction_minimum(
    certificate: Certificate, direction: Direction
) -> tuple[Fraction, tuple[Fraction, Fraction]]:
    """The least mass any reachable ``B``-square placement covers, exactly."""

    return minimum_covered_mass(
        certificate.atoms, direction, certificate.outer_side, certificate.square_side
    )


def verify(certificate: Certificate) -> Verdict:
    """Decide all four conditions. Exact, and never short-circuits C1 to C3."""

    conditions = [
        _condition_symmetric_atoms(certificate),
        _condition_mass_below_n(certificate),
        _condition_arc_reaches_eighth_turn(certificate),
        _condition_containment(certificate),
    ]
    worst: Fraction | None = None
    worst_label: str | None = None
    for direction in certificate.directions:
        minimum, _ = sweep_direction_minimum(certificate, direction)
        if worst is None or minimum < worst:
            worst, worst_label = minimum, direction.label
    conditions.append(
        ConditionReport(
            "C4 every reachable cell carries mass 1",
            f"least cell mass {worst} at direction {worst_label}",
            holds=worst is not None and worst >= 1,
        )
    )
    return Verdict(tuple(conditions), certificate.total_mass, worst, worst_label)
