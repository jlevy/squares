#!/usr/bin/env python3
"""Replay the finite exact controls behind the n=11 selection-routing analysis.

The checker covers exact rational arithmetic, finite availability enumeration, orbit
counts, incidence counts, and the report's synthetic one-parent and four-parent
controls. It does not solve either proposed continuous-domain surplus inequality,
establish a global owner-selection theorem, or run a scientific target.

Usage, from ``packing/``::

    uv run --frozen --all-extras --group dev python \
        -m devtools.check_n11_selection_routing
"""

from __future__ import annotations

import json
import sys
from collections.abc import Iterable, Sequence
from fractions import Fraction
from itertools import combinations, product
from math import comb

type Point = tuple[Fraction, Fraction]
type CornerPair = tuple[int, int]
type GroupElement = tuple[int, int, int]

CORNER_NAMES = ("BL", "BR", "TL", "TR")


def _require(value: object, message: str) -> None:
    if not value:
        raise AssertionError(message)


def _routes(values: Sequence[int]) -> bool:
    return all(value & 1 for value in values) or all(value & 2 for value in values)


def _reduced_lemmas(values: Sequence[int]) -> bool:
    return all(values) and not (1 in values and 2 in values)


def _included(values: Sequence[int], maximal: Sequence[int]) -> bool:
    return all((value & bound) == value for value, bound in zip(values, maximal, strict=True))


def _swap_axes(corner: int) -> int:
    return ((corner & 1) << 1) | ((corner & 2) >> 1)


def _act(pair: CornerPair, horizontal: int, vertical: int, swap: int) -> CornerPair:
    first, second = pair
    if swap:
        first, second = _swap_axes(second), _swap_axes(first)
    shift = horizontal + 2 * vertical
    return first ^ shift, second ^ shift


def _orbits(group: Iterable[GroupElement]) -> tuple[tuple[CornerPair, ...], ...]:
    elements = tuple(group)
    pairs: set[CornerPair] = {(first, second) for first in range(4) for second in range(4)}
    pending = pairs.copy()
    answer: list[tuple[CornerPair, ...]] = []
    while pending:
        pair = min(pending)
        orbit = {_act(pair, *element) for element in elements}
        _require(orbit <= pairs, "symmetry action left the corner-pair domain")
        pending -= orbit
        answer.append(tuple(sorted(orbit)))
    return tuple(answer)


def _labels(centre: Point, marks: tuple[Point, Point]) -> set[int]:
    answer: set[int] = set()
    for mark_index, mark in enumerate(marks):
        _require(
            all(centre[axis] != mark[axis] for axis in range(2)),
            "control centre lies on a mark axis",
        )
        rays = {
            0 if centre[0] > mark[0] else 2,
            1 if centre[1] > mark[1] else 3,
        }
        first = next(ray for ray in rays if (ray + 1) % 4 in rays)
        angle_eighths = 2 * first
        answer.update(
            8 * mark_index + sector % 8 for sector in (angle_eighths - 1, angle_eighths)
        )
    return answer


def _transport(point: Point, corner: int, q: Fraction) -> Point:
    return (
        q - point[0] if corner & 1 else point[0],
        q - point[1] if corner & 2 else point[1],
    )


def _dot(first: Point, second: Point) -> Fraction:
    return sum((left * right for left, right in zip(first, second, strict=True)), Fraction())


def _vertices(centre: Point, first_axis: Point, second_axis: Point) -> set[Point]:
    return {
        (
            centre[0] + first_sign * first_axis[0] / 2 + second_sign * second_axis[0] / 2,
            centre[1] + first_sign * first_axis[1] / 2 + second_sign * second_axis[1] / 2,
        )
        for first_sign, second_sign in product((-1, 1), repeat=2)
    }


def _named_orbits(orbits: Iterable[Iterable[CornerPair]]) -> list[list[list[str]]]:
    return [
        [[CORNER_NAMES[first], CORNER_NAMES[second]] for first, second in orbit]
        for orbit in orbits
    ]


def check_n11_selection_routing() -> dict[str, object]:
    """Run every finite exact control and return its deterministic summary."""
    q = Fraction(96, 25)
    core_side = Fraction(9977, 10000)
    a = Fraction(3152, 3175)
    b = Fraction(2336, 3175)
    mass = Fraction(22524199, 2000000)
    mark_weight = Fraction(106251, 800000)
    epsilon = mass - 11

    _require(epsilon == Fraction(524199, 2000000), "epsilon mismatch")
    _require(
        2 * mark_weight - epsilon == Fraction(441, 125000),
        "two-missing-mark margin mismatch",
    )
    missing_mark_allowance = epsilon - mark_weight
    _require(
        missing_mark_allowance == Fraction(517143, 4000000),
        "one-missing-mark allowance mismatch",
    )
    shrink = core_side * (1 + Fraction(207107, 90000000))
    _require(
        shrink == Fraction(899996306539, 900000000000) and shrink < 1,
        "strict core shrink mismatch",
    )

    maximal_products: list[tuple[int, ...]] = []
    for missing_zero, missing_fifteen in product(range(4), repeat=2):
        values = [3] * 4
        values[missing_zero] &= 2
        values[missing_fifteen] &= 1
        maximal_products.append(tuple(values))
    _require(len(set(maximal_products)) == 16, "maximal products are not distinct")

    avoiding_count = 0
    for values in product(range(4), repeat=4):
        routed = _routes(values)
        _require(routed == _reduced_lemmas(values), "two-lemma reduction mismatch")
        _require(
            (not routed) == any(_included(values, maximal) for maximal in maximal_products),
            "maximal avoiding-product cover mismatch",
        )
        avoiding_count += int(not routed)
    for maximal in maximal_products:
        _require(not _routes(maximal), "listed maximal product routes into G0")
        for corner in range(4):
            for bit in (1, 2):
                if not maximal[corner] & bit:
                    expanded = list(maximal)
                    expanded[corner] |= bit
                    _require(_routes(expanded), "listed avoiding product is not maximal")

    full_group: tuple[GroupElement, ...] = tuple(
        (horizontal, vertical, swap)
        for horizontal in range(2)
        for vertical in range(2)
        for swap in range(2)
    )
    full_orbits = _orbits(full_group)
    left_bottom_orbits = _orbits(((0, 0, 0), (0, 0, 1)))
    _require(
        sorted(map(len, full_orbits)) == [4, 4, 8],
        "full D4 orbit sizes mismatch",
    )
    _require(
        sorted(map(len, left_bottom_orbits)) == [1] * 4 + [2] * 6,
        "fixed-wall-chart orbit sizes mismatch",
    )
    fixed_pairs: set[CornerPair] = {
        (first, second)
        for first in range(4)
        for second in range(4)
        if _act((first, second), 0, 0, 1) == (first, second)
    }
    _require(
        fixed_pairs == {(corner, _swap_axes(corner)) for corner in range(4)},
        "fixed-wall-chart stabilizer mismatch",
    )

    incidence_counts = {
        0: [comb(4, split_pairs) for split_pairs in range(5)],
        1: [8 * comb(3, split_pairs) for split_pairs in range(4)],
    }
    _require(
        sum(map(sum, incidence_counts.values())) == 80,
        "seven-mark incidence count mismatch",
    )

    marks: tuple[Point, Point] = ((a, b), (b, a))
    centres: tuple[Point, Point, Point] = (
        (Fraction(17, 20), Fraction(17, 20)),
        (Fraction(6, 5), Fraction(9, 10)),
        (Fraction(9, 10), Fraction(6, 5)),
    )
    expected_labels = ({1, 2, 13, 14}, {0, 7, 13, 14}, {1, 2, 8, 15})
    for centre, expected in zip(centres, expected_labels, strict=True):
        _require(_labels(centre, marks) == expected, "signed-frame label mismatch")
        _require(
            all(
                abs(centre[axis] - mark[axis]) < core_side / 2
                for mark in marks
                for axis in range(2)
            ),
            "mark is outside a control core",
        )
        _require(
            all(Fraction(1, 2) < coordinate < q - Fraction(1, 2) for coordinate in centre),
            "control parent is not strictly contained",
        )
    greatest_mark_offset = max(
        abs(centre[axis] - mark[axis])
        for centre in centres
        for mark in marks
        for axis in range(2)
    )
    _require(
        greatest_mark_offset == Fraction(1474, 3175),
        "greatest mark offset mismatch",
    )
    core_containment_margin = core_side / 2 - greatest_mark_offset
    _require(
        core_containment_margin == Fraction(87879, 2540000),
        "core-containment margin mismatch",
    )
    _require(q - Fraction(12, 5) == Fraction(36, 25) > 1, "transport gap mismatch")

    for selection in product(centres, repeat=4):
        transported = [_transport(centre, corner, q) for corner, centre in enumerate(selection)]
        _require(
            all(
                max(abs(first[axis] - second[axis]) for axis in range(2)) > 1
                for first, second in combinations(transported, 2)
            ),
            "four-parent control is not pairwise interior-disjoint",
        )
    _require(
        _labels((Fraction(1, 2), Fraction(1, 2)), marks) == {3, 4, 11, 12},
        "corner parent label control mismatch",
    )
    _require((1 - core_side) / 2 == Fraction(23, 20000), "core inset mismatch")
    _require((1 + core_side) / 2 == Fraction(19977, 20000), "core span mismatch")
    _require(
        all(
            Fraction(23, 20000) < coordinate < Fraction(19977, 20000)
            for mark in marks
            for coordinate in mark
        ),
        "corner parent's core does not contain both marks",
    )
    all_marks = [(corner, _transport(mark, corner, q)) for corner in range(4) for mark in marks]
    cross_corner_least_squared_distance = min(
        sum(
            ((left - right) ** 2 for left, right in zip(first, second, strict=True)),
            Fraction(),
        )
        for (first_corner, first), (second_corner, second) in combinations(all_marks, 2)
        if first_corner != second_corner
    )
    _require(
        cross_corner_least_squared_distance == Fraction(34668544, 10080625)
        and cross_corner_least_squared_distance > 2 * core_side * core_side,
        "cross-corner core separation mismatch",
    )
    _require(q - a == Fraction(1808, 635), "distant-wall coordinate mismatch")
    distant_wall_squared_margin = (q - a) ** 2 - 8
    _require(
        distant_wall_squared_margin == Fraction(43064, 403225)
        and distant_wall_squared_margin > 0,
        "distant-wall path margin mismatch",
    )

    first_axis: Point = (Fraction(4, 5), Fraction(3, 5))
    second_axis: Point = (Fraction(-3, 5), Fraction(4, 5))
    tilted_centre: Point = (Fraction(7, 10), Fraction(7, 10))
    tilted_vertices = _vertices(tilted_centre, first_axis, second_axis)
    _require(
        tilted_vertices
        == {
            (Fraction(3, 5), Fraction()),
            (Fraction(7, 5), Fraction(3, 5)),
            (Fraction(4, 5), Fraction(7, 5)),
            (Fraction(), Fraction(4, 5)),
        },
        "tilted one-parent vertices mismatch",
    )
    _require(
        min(sum(vertex, Fraction()) for vertex in tilted_vertices) == Fraction(3, 5),
        "tilted one-parent corner margin mismatch",
    )

    first_centre: Point = (Fraction(49, 70), Fraction(99, 70))
    second_centre: Point = (Fraction(99, 70), Fraction(49, 70))
    displacement: Point = (
        second_centre[0] - first_centre[0],
        second_centre[1] - first_centre[1],
    )
    _require(
        (_dot(first_axis, displacement), _dot(second_axis, displacement))
        == (Fraction(1, 7), Fraction(-1)),
        "two-parent relative support mismatch",
    )
    _require(Fraction(74, 35) > 2, "two-parent container side is not above two")
    relative_values = (Fraction(-5, 7), Fraction(5, 7))
    relative_corners: tuple[Point, ...] = tuple(
        (first, second) for first in relative_values for second in relative_values
    )
    _require(
        max(
            abs(_dot(axis, relative))
            for axis in (first_axis, second_axis)
            for relative in relative_corners
        )
        == 1,
        "two-parent support maximum mismatch",
    )
    _require(
        all(
            sum(abs(_dot(axis, relative)) == 1 for axis in (first_axis, second_axis)) == 1
            for relative in relative_corners
        ),
        "two-parent relative corner has the wrong active-support count",
    )

    owner_minimum = Fraction(3, 5)
    owner_maximum = Fraction(11, 10)
    _require(
        owner_minimum <= Fraction(7, 10) < 1 <= owner_maximum,
        "shared-owner compatibility intervals mismatch",
    )
    artificial_mark = Fraction(27, 20)
    _require(
        max(
            abs(artificial_mark - (offset + Fraction(1, 2)))
            for offset in (owner_minimum, owner_maximum)
        )
        == Fraction(1, 4)
        < core_side / 2,
        "shared-owner artificial mark containment mismatch",
    )
    _require(Fraction(27, 10) < q, "shared-owner residual does not fit")

    return {
        "relevant_availability_profiles_checked": 4**4,
        "profiles_avoiding_G0": avoiding_count,
        "maximal_products": len(maximal_products),
        "D4_orbits": _named_orbits(full_orbits),
        "LB_orbits": _named_orbits(left_bottom_orbits),
        "incidence_counts": incidence_counts,
        "joint_four_parent_configurations_checked": 3**4,
        "labels": [sorted(_labels(centre, marks)) for centre in centres],
        "core_containment_margin": str(core_containment_margin),
        "cross_corner_least_squared_distance": str(cross_corner_least_squared_distance),
        "distant_wall_squared_margin": str(distant_wall_squared_margin),
        "missing_mark_allowance": str(missing_mark_allowance),
        "result": (
            "PASS; synthetic exact arithmetic and combinatorics only; no scientific target"
        ),
    }


def main() -> int:
    try:
        summary = check_n11_selection_routing()
    except AssertionError as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
