"""Independent finite oracles for conditional incidence arguments."""

from __future__ import annotations

from fractions import Fraction

from sqpack.incidence import (
    IncidenceProblem,
    allocations,
    convexly_closed_masks,
    occupancy_bound,
)


def _assignment_oracle(problem: IncidenceProblem, count: int) -> set[tuple[int, ...]]:
    """Assign sites to numbered blocks or zero, without the producer's site/mask search."""
    found: set[tuple[int, ...]] = set()
    allowed = set(problem.allowed_masks)
    conflicts = {frozenset(pair) for pair in problem.incompatible_masks}

    def visit(index: int, groups: tuple[int, ...]) -> None:
        if index == len(problem.labels):
            if (
                len(groups) == count
                and all(group in allowed for group in groups)
                and not any(pair <= set(groups) for pair in conflicts)
            ):
                found.add(tuple(sorted(groups)))
            return
        if len(groups) + len(problem.labels) - index < count:
            return
        visit(index + 1, groups)
        for slot in range(len(groups)):
            changed = (*groups[:slot], groups[slot] | (1 << index), *groups[slot + 1 :])
            visit(index + 1, changed)
        if len(groups) < count:
            visit(index + 1, (*groups, 1 << index))

    visit(0, ())
    return found


def test_allocations_keep_unused_sites_and_match_independent_oracle() -> None:
    problem = IncidenceProblem(("a", "b", "c", "d"), (1, 2, 3, 4, 5, 6, 8), ((1, 4),))
    for count in range(5):
        assert set(allocations(problem, count)) == _assignment_oracle(problem, count)
    assert (1, 2) in allocations(problem, 2)


def test_convex_closure_includes_boundary_sites_and_degenerate_hulls() -> None:
    points = tuple((Fraction(x), Fraction(y)) for x, y in ((0, 0), (2, 0), (1, 0), (1, 1)))
    masks = set(convexly_closed_masks(points))
    assert 1 in masks
    assert 3 not in masks  # The segment between the endpoints contains the third site.
    assert 11 not in masks  # Its triangular hull contains that site on an edge.
    assert 7 in masks
    assert 15 in masks


def test_weighted_capacity_counts_distinct_forced_boxes_and_refuses_overlap() -> None:
    assert occupancy_bound((Fraction(1),) * 8, (15,)) == 5
    assert occupancy_bound((Fraction(1),) * 12, (7,)) == 10
    assert occupancy_bound((Fraction(1, 2),) * 8, (7,), minimum_weight=Fraction(1)) == Fraction(
        7, 2
    )
    assert occupancy_bound((Fraction(1),) * 8, (3, 12)) == 6
    assert occupancy_bound((Fraction(1),) * 8, ()) == 8
    try:
        occupancy_bound((Fraction(1),) * 8, (3, 6))
    except ValueError as error:
        assert "overlap" in str(error)
    else:
        raise AssertionError("overlapping forced groups were counted as distinct boxes")


def test_invalid_inventories_do_not_silently_change_the_finite_problem() -> None:
    for masks in ((0,), (4,), (1, 1)):
        try:
            IncidenceProblem(("a", "b"), masks)
        except ValueError:
            pass
        else:
            raise AssertionError(f"invalid mask inventory accepted: {masks}")
    try:
        IncidenceProblem(("a", "b"), (1, 2), ((1, 3),))
    except ValueError:
        pass
    else:
        raise AssertionError("a conflict named an absent mask")
