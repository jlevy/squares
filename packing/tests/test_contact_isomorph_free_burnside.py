#!/usr/bin/env python3
"""Independent Burnside oracle for the uniform wall-free contact-scaffold slice."""

from __future__ import annotations

import math
from itertools import combinations, permutations

from sqpack.contact_assembly import enumerate_isomorph_free_scaffolds

COLORS = ((-1, 0), (1, 0), (0, -1), (0, 1))
COLOR_INDEX = {vector: index for index, vector in enumerate(COLORS)}
D4_MATRICES = (
    (1, 0, 0, 1),
    (0, -1, 1, 0),
    (-1, 0, 0, -1),
    (0, 1, -1, 0),
    (1, 0, 0, -1),
    (-1, 0, 0, 1),
    (0, 1, 1, 0),
    (0, -1, -1, 0),
)


def _mapped_pair(edge: tuple[int, int], relabeling: tuple[int, ...]) -> tuple[int, int]:
    left, right = relabeling[edge[0]], relabeling[edge[1]]
    return (left, right) if left < right else (right, left)


def _connected(size: int, edges: tuple[tuple[int, int], ...]) -> bool:
    reached = {0}
    frontier = [0]
    while frontier:
        vertex = frontier.pop()
        for left, right in edges:
            neighbor = right if left == vertex else left if right == vertex else None
            if neighbor is not None and neighbor not in reached:
                reached.add(neighbor)
                frontier.append(neighbor)
    return len(reached) == size


def _topologies(size: int) -> tuple[tuple[tuple[int, int], ...], ...]:
    pairs = tuple(combinations(range(size), 2))
    relabelings = tuple(permutations(range(size)))
    representatives = set()
    for mask in range(1 << len(pairs)):
        edges = tuple(pair for index, pair in enumerate(pairs) if mask & (1 << index))
        if _connected(size, edges):
            representatives.add(
                min(
                    tuple(sorted(_mapped_pair(edge, relabeling) for edge in edges))
                    for relabeling in relabelings
                )
            )
    return tuple(sorted(representatives, key=lambda edges: (len(edges), edges)))


def _burnside_orbits(size: int, edges: tuple[tuple[int, int], ...]) -> int:
    edge_index = {edge: index for index, edge in enumerate(edges)}
    edge_set = set(edges)
    automorphisms = [
        relabeling
        for relabeling in permutations(range(size))
        if {_mapped_pair(edge, relabeling) for edge in edges} == edge_set
    ]
    fixed_total = 0
    for relabeling in automorphisms:
        for xx, xy, yx, yy in D4_MATRICES:
            targets = []
            color_maps = []
            for left, right in edges:
                mapped_left, mapped_right = relabeling[left], relabeling[right]
                targets.append(edge_index[_mapped_pair((left, right), relabeling)])
                endpoint_sign = -1 if mapped_left > mapped_right else 1
                color_maps.append(
                    tuple(
                        COLOR_INDEX[
                            (
                                endpoint_sign * (xx * x + xy * y),
                                endpoint_sign * (yx * x + yy * y),
                            )
                        ]
                        for x, y in COLORS
                    )
                )

            unseen = set(range(len(edges)))
            cycle_factors = []
            while unseen:
                start = min(unseen)
                cycle = []
                current = start
                while current not in cycle:
                    cycle.append(current)
                    unseen.discard(current)
                    current = targets[current]
                assert current == start
                fixed_colors = 0
                for initial in range(len(COLORS)):
                    transformed = initial
                    for edge_index_in_cycle in cycle:
                        transformed = color_maps[edge_index_in_cycle][transformed]
                    fixed_colors += transformed == initial
                cycle_factors.append(fixed_colors)
            fixed_total += math.prod(cycle_factors)

    group_order = len(automorphisms) * len(D4_MATRICES)
    assert fixed_total % group_order == 0
    return fixed_total // group_order


def test_burnside_oracle_independently_matches_direct_quotient_through_size_five() -> None:
    burnside_counts = []
    direct_counts = []
    for size in range(1, 6):
        burnside_counts.append(
            sum(_burnside_orbits(size, topology) for topology in _topologies(size))
        )
        direct = enumerate_isomorph_free_scaffolds(
            size,
            maximum_colorings=2_000_000,
            maximum_emitted_scaffolds=100_000,
        )
        assert direct.status == "completed"
        direct_counts.append(len(direct.scaffolds))

    assert burnside_counts == direct_counts == [1, 1, 7, 124, 11_013]
