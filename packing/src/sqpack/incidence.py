"""Exact finite counting after geometric premises have restricted point incidences.

An incidence mask names *all* marked points in one member of a packing. Geometry
must justify the supplied allowed masks and pairwise exclusions. This module
enumerates disjoint masks, allowing unused points; it never proves that its
combinatorial allocations have geometric realizations.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

type RationalPoint = tuple[Fraction, Fraction]
type Allocation = tuple[int, ...]


def _validate_mask(mask: int, site_count: int) -> None:
    if type(mask) is not int or not 0 < mask < (1 << site_count):
        raise ValueError("each incidence mask must name a nonempty subset of the sites")


@dataclass(frozen=True)
class IncidenceProblem:
    """A caller-justified outer approximation of the possible incidence patterns."""

    labels: tuple[str, ...]
    allowed_masks: tuple[int, ...]
    incompatible_masks: tuple[tuple[int, int], ...] = ()

    def __post_init__(self) -> None:
        if not self.labels or len(set(self.labels)) != len(self.labels):
            raise ValueError("site labels must be nonempty and distinct")
        for mask in self.allowed_masks:
            _validate_mask(mask, len(self.labels))
        if len(set(self.allowed_masks)) != len(self.allowed_masks):
            raise ValueError("duplicate incidence masks")
        allowed = set(self.allowed_masks)
        seen: set[frozenset[int]] = set()
        for left, right in self.incompatible_masks:
            pair = frozenset((left, right))
            if left == right or left not in allowed or right not in allowed or pair in seen:
                raise ValueError("each exclusion must name two distinct allowed masks once")
            seen.add(pair)


def allocations(problem: IncidenceProblem, block_count: int) -> tuple[Allocation, ...]:
    """Enumerate every allocation to this many unlabelled blocks, including unused sites.

    The least undecided site is either unused or belongs to exactly one chosen
    mask. These exhaustive alternatives give each allocation one search path.
    Returning every surviving allocation makes lost cases visible to callers.
    """
    if type(block_count) is not int or block_count < 0:
        raise ValueError("block_count must be a nonnegative integer")
    site_count = len(problem.labels)
    by_site = tuple(
        tuple(mask for mask in problem.allowed_masks if mask & (1 << index))
        for index in range(site_count)
    )
    exclusions: dict[int, set[int]] = {mask: set() for mask in problem.allowed_masks}
    for left, right in problem.incompatible_masks:
        exclusions[left].add(right)
        exclusions[right].add(left)
    found: list[Allocation] = []

    def visit(available: int, chosen: Allocation) -> None:
        remaining = block_count - len(chosen)
        if remaining == 0:
            found.append(tuple(sorted(chosen)))
            return
        if available.bit_count() < remaining:
            return
        first = available & -available
        visit(available ^ first, chosen)
        for mask in by_site[first.bit_length() - 1]:
            if mask & available == mask and not exclusions[mask].intersection(chosen):
                visit(available ^ mask, (*chosen, mask))

    visit((1 << site_count) - 1, ())
    return tuple(sorted(found))


def _cross(first: RationalPoint, second: RationalPoint, third: RationalPoint) -> Fraction:
    return (second[0] - first[0]) * (third[1] - first[1]) - (second[1] - first[1]) * (
        third[0] - first[0]
    )


def _convex_hull(points: tuple[RationalPoint, ...]) -> tuple[RationalPoint, ...]:
    ordered = sorted(points)
    if len(ordered) <= 1:
        return tuple(ordered)
    lower: list[RationalPoint] = []
    upper: list[RationalPoint] = []
    for chain, values in ((lower, ordered), (upper, list(reversed(ordered)))):
        for point in values:
            while len(chain) >= 2 and _cross(chain[-2], chain[-1], point) <= 0:
                chain.pop()
            chain.append(point)
    return tuple(lower[:-1] + upper[:-1])


def _in_hull(point: RationalPoint, hull: tuple[RationalPoint, ...]) -> bool:
    if len(hull) == 1:
        return point == hull[0]
    if len(hull) == 2:
        first, second = hull
        return (
            _cross(first, second, point) == 0
            and min(first[0], second[0]) <= point[0] <= max(first[0], second[0])
            and min(first[1], second[1]) <= point[1] <= max(first[1], second[1])
        )
    return all(
        _cross(hull[index], hull[(index + 1) % len(hull)], point) >= 0
        for index in range(len(hull))
    )


def convexly_closed_masks(points: tuple[RationalPoint, ...]) -> tuple[int, ...]:
    """All nonempty site subsets containing every site in their closed convex hull.

    If an open convex block contains several sites, it contains their entire
    closed convex hull. Thus omitted sites on hull edges are forbidden too.
    This restriction is necessary, not sufficient, for a square realization.
    """
    if not points or len(set(points)) != len(points):
        raise ValueError("sites must be nonempty and have distinct coordinates")
    if any(not isinstance(coordinate, Fraction) for point in points for coordinate in point):
        raise TypeError("site coordinates must be exact Fractions")
    result: list[int] = []
    for mask in range(1, 1 << len(points)):
        hull = _convex_hull(
            tuple(point for index, point in enumerate(points) if mask & (1 << index))
        )
        if all(
            mask & (1 << index) or not _in_hull(point, hull)
            for index, point in enumerate(points)
        ):
            result.append(mask)
    return tuple(result)


def occupancy_bound(
    weights: tuple[Fraction, ...],
    forced_masks: tuple[int, ...],
    *,
    minimum_weight: Fraction = Fraction(1),
) -> Fraction:
    """Conditional upper bound on block count from distinct forced occupancy groups.

    Assume each of n disjoint blocks carries at least minimum_weight and each
    supplied mask lies in a different distinguished block. Their masses are at
    least max(minimum_weight, forced mass). All other blocks still incur their
    baseline charge. No geometry or existence of the distinguished blocks is
    inferred by this arithmetic check.
    """
    if not isinstance(minimum_weight, Fraction) or minimum_weight <= 0:
        raise ValueError("minimum_weight must be a positive Fraction")
    if any(not isinstance(weight, Fraction) or weight < 0 for weight in weights):
        raise ValueError("site weights must be nonnegative Fractions")
    used = 0
    forced_mass = Fraction(0)
    for mask in forced_masks:
        _validate_mask(mask, len(weights))
        if used & mask:
            raise ValueError("forced masks overlap; distinct blocks cannot share marked sites")
        used |= mask
        mass = sum(
            (weight for index, weight in enumerate(weights) if mask & (1 << index)),
            Fraction(0),
        )
        forced_mass += max(minimum_weight, mass)
    return len(forced_masks) + (sum(weights, Fraction(0)) - forced_mass) / minimum_weight
