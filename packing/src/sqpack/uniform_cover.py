"""A complete flat SAT cover of one closed two-square pose domain.

The only case split is the eight directed edge-normal alternatives for the one pair.
Every leaf has exactly the root's center boxes, actual half-angle charts and side box.
Overlapping alternatives and touching seams are retained. No symmetry reduction,
restricted-family lemma, reference or recursive case graph is part of this format.

An accepted cover excludes only its declared two-square root. It does not establish a
complete eleven-square cover or inclusion of a retained contact-feature family.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import product

from sqpack.exact_lp import DEFAULT_PIVOT_BUDGET, ExactLPError, prove_infeasible, rational_sign
from sqpack.uniform_cell import (
    PairChoice,
    PoseBox,
    RationalInterval,
    UniformCell,
    UniformCellDescriptor,
    build_uniform_cell,
)
from sqpack.uniform_cell_check import check_uniform_cell

# Two normals owned by either square, each taken in both directed orders.
TWO_SQUARE_ALTERNATIVES = tuple(product(range(4), (-1, 1)))


@dataclass(frozen=True, slots=True)
class TwoSquareRoot:
    """The exact requested domain, supplied separately to the certificate reader."""

    poses: tuple[PoseBox, PoseBox]
    side: RationalInterval

    def __post_init__(self) -> None:
        _validate_root(self)


@dataclass(frozen=True, slots=True)
class UniformCoverLeaf:
    """Untrusted leaf data; acceptance requires the independent uniform-cell reader."""

    cell: UniformCell
    multipliers: tuple[Fraction, ...]


@dataclass(frozen=True, slots=True)
class TwoSquareCover:
    """A flat proof packet, whose shape and arithmetic are checked at acceptance."""

    root: TwoSquareRoot
    leaves: tuple[UniformCoverLeaf, ...]


def _validate_interval(interval: RationalInterval) -> None:
    if type(interval) is not RationalInterval:
        raise ExactLPError("bad-cover", "root bounds must be closed rational intervals")
    if type(interval.lower) is not Fraction or type(interval.upper) is not Fraction:
        raise ExactLPError("bad-cover", "stored root endpoints must be Fractions")
    if interval.lower > interval.upper:
        raise ExactLPError("bad-cover", "root interval endpoints are reversed")


def _validate_root(root: TwoSquareRoot) -> None:
    if type(root) is not TwoSquareRoot:
        raise ExactLPError("bad-cover", "expected a TwoSquareRoot")
    if type(root.poses) is not tuple or len(root.poses) != 2:
        raise ExactLPError("bad-cover", "the root must contain exactly two labelled poses")
    _validate_interval(root.side)
    if root.side.lower <= 0:
        raise ExactLPError("bad-cover", "root side interval must be strictly positive")
    for pose in root.poses:
        if type(pose) is not PoseBox:
            raise ExactLPError("bad-cover", "root poses must be PoseBox objects")
        for interval in (pose.x, pose.y, pose.half_angle):
            _validate_interval(interval)
        for interval in (pose.x, pose.y):
            if interval.lower < 0 or interval.upper > root.side.upper:
                raise ExactLPError("bad-cover", "root centers exceed the container envelope")


def _leaf_alternative(leaf: UniformCoverLeaf, root: TwoSquareRoot) -> tuple[int, int]:
    if type(leaf) is not UniformCoverLeaf or type(leaf.cell) is not UniformCell:
        raise ExactLPError("bad-cover", "every leaf must contain a uniform cell")
    descriptor = leaf.cell.descriptor
    if type(descriptor) is not UniformCellDescriptor:
        raise ExactLPError("bad-cover", "leaf has no uniform geometry descriptor")
    if descriptor.poses != root.poses or descriptor.side != root.side:
        raise ExactLPError("root-mismatch", "a leaf changes the root pose or side domain")
    if type(descriptor.choices) is not tuple or len(descriptor.choices) != 1:
        raise ExactLPError("cover-alternatives", "each leaf must choose exactly one pair axis")
    choice = descriptor.choices[0]
    if type(choice) is not PairChoice:
        raise ExactLPError("cover-alternatives", "leaf has no directed pair choice")
    values = (choice.first, choice.second, choice.axis_position, choice.orientation)
    if any(type(value) is not int for value in values):
        raise ExactLPError(
            "cover-alternatives", "directed pair choices must be strict integers"
        )
    alternative = (choice.axis_position, choice.orientation)
    if (choice.first, choice.second) != (0, 1) or alternative not in TWO_SQUARE_ALTERNATIVES:
        raise ExactLPError("cover-alternatives", "leaf chooses an unsupported pair alternative")
    if type(leaf.multipliers) is not tuple or any(
        type(value) is not Fraction for value in leaf.multipliers
    ):
        raise ExactLPError("bad-cover", "stored leaf multipliers must be a tuple of Fractions")
    return alternative


def check_two_square_cover(
    expected_root: TwoSquareRoot, cover: TwoSquareCover
) -> tuple[Fraction, ...]:
    """Return independently checked positive gaps only for the complete requested root.

    The separately supplied root prevents a valid proof for a substituted or reflected
    domain from certifying the caller's original claim. Leaf order is immaterial, but
    all directed alternatives must occur exactly once with identical closed domains.
    """
    _validate_root(expected_root)
    if type(cover) is not TwoSquareCover:
        raise ExactLPError("bad-cover", "expected a flat TwoSquareCover proof packet")
    _validate_root(cover.root)
    if cover.root != expected_root:
        raise ExactLPError("root-mismatch", "the proof root differs from the requested root")
    if type(cover.leaves) is not tuple or len(cover.leaves) != len(TWO_SQUARE_ALTERNATIVES):
        raise ExactLPError(
            "cover-alternatives", "the cover must contain all eight alternatives"
        )
    alternatives = tuple(_leaf_alternative(leaf, expected_root) for leaf in cover.leaves)
    if set(alternatives) != set(TWO_SQUARE_ALTERNATIVES):
        raise ExactLPError(
            "cover-alternatives", "a directed alternative is missing or duplicated"
        )
    return tuple(check_uniform_cell(leaf.cell, leaf.multipliers) for leaf in cover.leaves)


def prove_two_square_cover(
    root: TwoSquareRoot, *, pivot_budget: int = DEFAULT_PIVOT_BUDGET
) -> TwoSquareCover:
    """Propose every leaf's exact dual and check the whole cover independently.

    A feasible or unresolved leaf propagates its typed refusal, so a partial cover is
    never returned as complete. ``pivot_budget`` applies separately to each leaf.
    """
    _validate_root(root)
    leaves: list[UniformCoverLeaf] = []
    for axis, orientation in TWO_SQUARE_ALTERNATIVES:
        descriptor = UniformCellDescriptor(
            root.poses, root.side, (PairChoice(0, 1, axis, orientation),)
        )
        cell = build_uniform_cell(descriptor)
        certificate = prove_infeasible(cell.lp, rational_sign, pivot_budget=pivot_budget)
        leaves.append(UniformCoverLeaf(cell, certificate.multipliers))
    cover = TwoSquareCover(root, tuple(leaves))
    check_two_square_cover(root, cover)
    return cover
