"""Reconstruct the Memo I finite premises without the production geometry/search."""

from __future__ import annotations

import json
import subprocess
import sys
from itertools import combinations
from pathlib import Path

from cases.stromquist.memo1 import conditional_record, d4_images, make_problem
from sqpack.incidence import allocations

type GridPoint = tuple[int, int]


def _det(a: GridPoint, b: GridPoint, p: GridPoint) -> int:
    return (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])


def _independent_allowed_masks() -> set[int]:
    """Use segments and three-point convex combinations, not a computed hull."""
    grid = tuple((i % 3, i // 3) for i in range(9))
    allowed: set[int] = set()
    for mask in range(1, 512):
        if mask == 16:
            continue
        selected = tuple(point for i, point in enumerate(grid) if mask & (1 << i))
        if len(selected) == 2:
            a, b = selected
            if abs(a[0] - b[0]) + abs(a[1] - b[1]) != 1:
                continue
        missing = tuple(point for i, point in enumerate(grid) if not mask & (1 << i))
        segment_violation = any(
            _det(a, b, p) == 0
            and min(a[0], b[0]) <= p[0] <= max(a[0], b[0])
            and min(a[1], b[1]) <= p[1] <= max(a[1], b[1])
            for p in missing
            for a, b in combinations(selected, 2)
        )
        triangle_violation = any(
            _det(a, b, c) != 0
            and (
                min(_det(a, b, p), _det(b, c, p), _det(c, a, p)) >= 0
                or max(_det(a, b, p), _det(b, c, p), _det(c, a, p)) <= 0
            )
            for p in missing
            for a, b, c in combinations(selected, 3)
        )
        if not segment_violation and not triangle_violation:
            allowed.add(mask)
    return allowed


def _independent_allocations(allowed: set[int]) -> set[tuple[int, ...]]:
    found: set[tuple[int, ...]] = set()

    def visit(index: int, groups: tuple[int, ...]) -> None:
        if len(groups) + 9 - index < 6:
            return
        if index == 9:
            if len(groups) != 6 or not all(mask in allowed for mask in groups):
                return
            singles = tuple(mask.bit_length() - 1 for mask in groups if mask.bit_count() == 1)
            if any(
                abs(a % 3 - b % 3) + abs(a // 3 - b // 3) == 1
                for a, b in combinations(singles, 2)
            ):
                return
            found.add(tuple(sorted(groups)))
            return
        # Bucket zero is always available: initial marks need not be occupied.
        visit(index + 1, groups)
        for position in range(len(groups)):
            visit(
                index + 1,
                (*groups[:position], groups[position] | (1 << index), *groups[position + 1 :]),
            )
        if len(groups) < 6:
            visit(index + 1, (*groups, 1 << index))

    visit(0, ())
    return found


def test_memo1_all_masks_and_allocations_agree_with_independent_oracle() -> None:
    problem = make_problem()
    independent = _independent_allowed_masks()
    assert set(problem.allowed_masks) == independent
    found = set(allocations(problem, 6))
    assert found == _independent_allocations(independent)
    assert len(found) == 4
    assert all(sum(allocation) == 511 for allocation in found)
    assert {min(d4_images(allocation)) for allocation in found} == {min(found)}


def test_d4_preserves_every_premise_and_closes_each_reported_orbit() -> None:
    problem = make_problem()
    allowed = set(problem.allowed_masks)
    conflicts = {tuple(sorted(pair)) for pair in problem.incompatible_masks}
    for mask in problem.allowed_masks:
        assert all(image[0] in allowed for image in d4_images((mask,)))
    for pair in problem.incompatible_masks:
        assert set(d4_images(pair)) <= conflicts
    for allocation in allocations(problem, 6):
        orbit = set(d4_images(allocation))
        assert allocation in orbit
        assert all(set(d4_images(image)) == orbit for image in orbit)


def test_every_geometric_premise_and_forced_four_change_the_finite_conclusion() -> None:
    record = conditional_record()
    retained = Path(__file__).resolve().parents[1] / "cases/stromquist/memo1-incidence.json"
    assert json.loads(retained.read_text()) == record
    assert record["scope"] == "conditional-combinatorial-control"
    assert record["full_geometric_proof_verified"] is False
    assert record["new_packing_bound"] is False
    # conditional_record refuses a control that does not enlarge the allocation set.
    assert record["allocation_count"] == 4
    assert record["d4_orbit_count"] == 1


def test_cli_retains_exactly_the_machine_readable_output(tmp_path: Path) -> None:
    output = tmp_path / "memo1.json"
    completed = subprocess.run(
        [sys.executable, "-m", "cases.stromquist.memo1", "--output", str(output)],
        cwd=Path(__file__).resolve().parents[1],
        check=True,
        capture_output=True,
        text=True,
    )
    assert completed.stdout == output.read_text()
    assert json.loads(completed.stdout)["full_geometric_proof_verified"] is False
