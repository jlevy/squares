"""Lifted primitives that case 2095 does not exercise, held to their frozen originals.

The faster covers, the closed degenerate cover, self-hull cuts, the rational and integer
universal collision, the support outer domain and the common-core output check are
compared with the frozen n11 modules on inputs drawn from case 2095's published rows and
on small exact controls, outputs and refusals alike. The sweep's slice predicate is the
one exception: it is held to the corrected closed-interval cover of the n11 review's
finding C2, not to the frozen routine it was copied from.
"""

from __future__ import annotations

import time
from collections.abc import Sequence
from fractions import Fraction
from itertools import combinations_with_replacement
from typing import Any

import pytest

from devtools import check_hull_kernel_case2095 as tool
from devtools import check_n11_capture_transition_pilot as frozen_pilot
from devtools import check_n11_closed_degenerate_cover as frozen_degenerate
from devtools import check_n11_generic_fresh as frozen
from devtools import check_n11_optimality_field_mask0 as frozen_geometry
from devtools import n11_closed_interval_cover as closed_interval
from devtools import n11_fast_exact_cover as frozen_fast
from devtools import n11_indexed_exact_cover as frozen_indexed
from devtools import n11_integer_collision as frozen_integer
from sqpack.hull_kernel import Budget, RefusalError, collision, covers, node
from sqpack.hull_kernel.frame import Frame
from sqpack.hull_kernel.geometry import Polygon, intersect
from sqpack.hull_kernel.induction import convex, forbidden_regions, hull, wall_lines
from sqpack.hull_kernel.rational import Q, as_fraction
from sqpack.hull_kernel.sweep import covers_vertical, exact_union_cover

type RowInputs = tuple[Polygon, list[Polygon], dict[str, Any], Polygon]


@pytest.fixture(scope="module")
def sources() -> tool.Sources:
    return tool.load_sources()


@pytest.fixture(scope="module")
def frame(sources: tool.Sources) -> Frame:
    return tool.library_frame(sources)


@pytest.fixture(scope="module")
def first_row(sources: tool.Sources, frame: Frame) -> RowInputs:
    """Step 0, row 0 of case 2095: its domain, cover regions, JSON row and core."""
    prior = {
        owner: hull(node.points(sources.seed["groups"][str(owner)])) for owner in frozen.MASK
    }
    row = sources.source["steps"][0]["rows"][0]
    world = frame.world(6)
    domain = intersect(world, wall_lines(frame, Q(0), Q(1, 32)))
    core = convex(node.points(row["core_vertices"]))
    residual = [convex(node.points(value)) for value in row["residual_polygons"]]
    return domain, forbidden_regions(prior, 6, core) + residual, row, core


def fractions_of(polygon: Sequence[tuple[Q, Q]]) -> list[tuple[Fraction, Fraction]]:
    """A kernel polygon as the frozen checkers' `Fraction` points, value for value."""
    return [(as_fraction(x), as_fraction(y)) for x, y in polygon]


def budget() -> Budget:
    return Budget(time.monotonic() + 30, 50_000)


def frozen_budget() -> frozen_geometry.Budget:
    return frozen_geometry.Budget(time.monotonic() + 30, 50_000)


def test_the_fast_and_indexed_covers_agree_with_theirs_and_the_reference(
    first_row: RowInputs,
) -> None:
    domain, regions, _, _ = first_row
    reference = exact_union_cover(domain, regions, budget=budget())
    assert reference == {"events": 87, "probes": 173, "edge_segments": 242}
    assert covers.fast_union_cover(domain, regions, budget=budget()) == reference
    assert covers.indexed_union_cover(domain, regions, budget=budget()) == reference
    frozen_domain, frozen_regions = fractions_of(domain), [fractions_of(r) for r in regions]
    assert (
        frozen_fast.exact_union_cover(frozen_domain, frozen_regions, budget=frozen_budget())
        == reference
    )
    assert (
        frozen_indexed.exact_union_cover(frozen_domain, frozen_regions, budget=frozen_budget())
        == reference
    )
    with pytest.raises(RefusalError, match="uncovered"):
        covers.fast_union_cover(domain, regions[:-3], budget=budget())
    with pytest.raises(RefusalError, match="uncovered"):
        covers.indexed_union_cover(domain, regions[:-3], budget=budget())


def slab(interval: tuple[Fraction, Fraction]) -> Polygon:
    """A polygon whose closed vertical section at x = 0 is exactly `interval`."""
    lo, hi = Q(interval[0]), Q(interval[1])
    return [(Q(0), lo), (Q(1), lo), (Q(1), hi), (Q(0), hi)]


def slice_covered(
    target: tuple[Fraction, Fraction], spans: Sequence[tuple[Fraction, Fraction]]
) -> bool:
    return covers_vertical(slab(target), [slab(span) for span in spans], Q(0))


def test_the_sweep_slice_is_the_corrected_closed_interval_cover() -> None:
    """Finding C2 of the n11 adversarial review: the frozen slice predicate accepted a
    one-point section from a span ending below it. The sweep's copy now skips such spans,
    as the compiled one does; on the review's 12,180 cases (every target and family of at
    most two of the 28 closed intervals with integer ends in -3..3) it agrees with the
    corrected reference, and it meets the review's acceptance cases."""
    ends = [Fraction(value) for value in range(-3, 4)]
    intervals = [(lo, hi) for lo in ends for hi in ends if lo <= hi]
    families: list[tuple[tuple[Fraction, Fraction], ...]] = [
        (),
        *((interval,) for interval in intervals),
        *combinations_with_replacement(intervals, 2),
    ]
    assert len(intervals) * len(families) == 12_180
    wrong = [
        (target, spans)
        for target in intervals
        for spans in families
        if slice_covered(target, spans)
        is not closed_interval.covers_closed_interval(target, spans)
    ]
    assert wrong == []
    one, half, gap = Fraction(1), Fraction(1, 2), Fraction(1, 10**50)
    assert slice_covered((one, one), [(Fraction(0), Fraction(0))]) is False
    historical = frozen_geometry.covers_vertical(
        fractions_of(slab((one, one))),
        [fractions_of(slab((Fraction(0), Fraction(0))))],
        Fraction(0),
    )
    assert historical is True
    assert slice_covered((one, one), [(Fraction(0), Fraction(0)), (half, one)]) is True
    assert slice_covered((one, one), [(one, Fraction(3))]) is True
    assert slice_covered((Fraction(0), one), [(half, one), (Fraction(0), half)]) is True
    assert slice_covered((Fraction(0), one), [(Fraction(0), half), (half + gap, one)]) is False
    assert slice_covered((Fraction(0), one), [(gap, one)]) is False


@pytest.mark.parametrize(
    "target",
    [
        [(Q(0), 0.0), (Q(1), 0.0), (Q(1), 1.0), (Q(0), 1.0)],
        [(Q(0), Q(0)), (Q(1), Q(0)), (Q(1), float("nan")), (Q(0), float("nan"))],
        [(Q(0), False), (Q(1), False), (Q(1), True), (Q(0), True)],
    ],
)
def test_the_sweep_slice_refuses_an_inexact_endpoint(target: Any) -> None:
    with pytest.raises(RefusalError, match="inexact coverage endpoint"):
        covers_vertical(target, [slab((Fraction(-1), Fraction(2)))], Q(0))


def test_the_sweep_refuses_an_uncovered_extreme_vertex_at_the_vertex() -> None:
    """The review's triangle, whose section at x = 0 is the vertex (0, 1) and whose only
    region lies below it. The frozen sweep let the vertex through and refused at the slab
    beside it; the corrected sweep refuses the same domain at the vertex. The verdict is
    the same, as the closure argument in the module says, and only the abscissa moves."""
    domain = [(Q(0), Q(1)), (Q(1), Q(0)), (Q(1), Q(2))]
    below = [(Q(0), Q(-1)), (Q(1), Q(-1)), (Q(1), Q(0)), (Q(0), Q(0))]
    assert covers_vertical(domain, [below], Q(0)) is False
    with pytest.raises(RefusalError, match=r"row uncovered at exact x=0$"):
        exact_union_cover(domain, [below], budget=budget())
    with pytest.raises(ValueError, match=r"row uncovered at exact x=1/2$"):
        frozen_geometry.exact_union_cover(
            fractions_of(domain), [fractions_of(below)], budget=frozen_budget()
        )
    for cover in (covers.fast_union_cover, covers.indexed_union_cover):
        with pytest.raises(RefusalError, match=r"row uncovered at exact x=0$"):
            cover(domain, [below], budget=budget())


def test_the_degenerate_cover_needs_the_whole_segment() -> None:
    """The checker's cover of a zero-area row: closed regions about the ends and the
    midpoint of a segment leave the rest of it uncovered, and are refused."""
    segment = [(Q(0), Q(0)), (Q(2), Q(1))]
    marks = [
        [(x - Q(1, 4), Q(-1)), (x + Q(1, 4), Q(-1)), (x + Q(1, 4), Q(2)), (x - Q(1, 4), Q(2))]
        for x in (Q(0), Q(1), Q(2))
    ]
    with pytest.raises(RefusalError, match="uncovered degenerate"):
        covers.closed_degenerate_cover(segment, marks, budget=budget())
    wide = [
        [(x - Q(1, 2), Q(-1)), (x + Q(1, 2), Q(-1)), (x + Q(1, 2), Q(2)), (x - Q(1, 2), Q(2))]
        for x in (Q(0), Q(1), Q(2))
    ]
    assert covers.closed_degenerate_cover(segment, wide, budget=budget())["probes"] == 3


def test_the_closed_degenerate_cover_is_the_frozen_one() -> None:
    segment = [(Q(0), Q(0)), (Q(2), Q(1))]
    left = [(Q(-1), Q(-1)), (Q(1), Q(-1)), (Q(1), Q(2)), (Q(-1), Q(2))]
    right = [(Q(1), Q(-1)), (Q(3), Q(-1)), (Q(3), Q(2)), (Q(1), Q(2))]
    expected = frozen_degenerate.exact_cover_closed_degenerate(
        fractions_of(segment), [fractions_of(left), fractions_of(right)], budget=frozen_budget()
    )
    assert covers.closed_degenerate_cover(segment, [left, right], budget=budget()) == expected
    assert covers.convex_halfplanes(left) == frozen_degenerate.convex_halfplanes(
        fractions_of(left)
    )
    assert covers.convex_halfplanes(segment) == frozen_degenerate.convex_halfplanes(
        fractions_of(segment)
    )
    short = [(Q(3, 2), Q(-1)), (Q(3), Q(-1)), (Q(3), Q(2)), (Q(3, 2), Q(2))]
    with pytest.raises(RefusalError, match="uncovered degenerate"):
        covers.closed_degenerate_cover(segment, [left, short], budget=budget())
    with pytest.raises(ValueError, match="uncovered degenerate"):
        frozen_degenerate.exact_cover_closed_degenerate(
            fractions_of(segment),
            [fractions_of(left), fractions_of(short)],
            budget=frozen_budget(),
        )


def test_self_hull_cuts_match_the_transition_pilot(sources: tool.Sources, frame: Frame) -> None:
    owned = hull(node.points(sources.seed["groups"]["6"]))
    lo, hi = Q(0), Q(1, 32)
    loose = max(x for x, _ in owned) + frame.scale
    tight = min(x for x, _ in owned) + frame.scale / 4
    accepted = collision.self_hull_cuts(frame, [(Q(1), Q(0), loose)], owned, lo, hi)
    assert accepted == frozen_pilot.necessary_self_cuts(
        [{"normal": ["1", "0"], "upper": str(loose)}],
        fractions_of(owned),
        as_fraction(lo),
        as_fraction(hi),
    )
    with pytest.raises(RefusalError, match="excludes a possible square center"):
        collision.self_hull_cuts(frame, [(Q(1), Q(0), tight)], owned, lo, hi)
    with pytest.raises(ValueError, match="excludes a possible square center"):
        frozen_pilot.necessary_self_cuts(
            [{"normal": ["1", "0"], "upper": str(tight)}],
            fractions_of(owned),
            as_fraction(lo),
            as_fraction(hi),
        )


def square(centre: tuple[Q, Q], half: Q) -> Polygon:
    x, y = centre
    return [
        (x - half, y - half),
        (x + half, y - half),
        (x + half, y + half),
        (x - half, y + half),
    ]


def test_universal_collision_rational_and_integer_match_theirs() -> None:
    core = square((Q(0), Q(0)), Q(2, 5))
    partner_domain = square((Q(1), Q(1)), Q(1, 1000))
    query_domain = square((Q(1), Q(1)), Q(1, 10))
    region = square((Q(1), Q(1)), Q(1, 500))
    partners = [(partner_domain, core), (square((Q(1), Q(1)), Q(1, 2000)), core)]
    frozen_inputs = (
        fractions_of(core),
        fractions_of(query_domain),
        [(fractions_of(d), fractions_of(c)) for d, c in partners],
        fractions_of(region),
    )
    expected = frozen_pilot.universal_collision(*frozen_inputs, budget=frozen_budget())
    assert expected == 2 * 4 * 4
    assert collision.universal_collision(
        core, query_domain, partners, region, budget=budget()
    ) == (expected)
    assert collision.integer_universal_collision(
        core, query_domain, partners, region, budget=budget()
    ) == (expected)
    assert (
        frozen_integer.universal_collision(*frozen_inputs, budget=frozen_budget()) == expected
    )
    far = square((Q(9, 5), Q(1)), Q(1, 500))
    wide = square((Q(1), Q(1)), Q(1))
    for check in (collision.universal_collision, collision.integer_universal_collision):
        with pytest.raises(RefusalError, match="escapes universal collision set"):
            check(core, wide, partners, far, budget=budget())
        with pytest.raises(RefusalError, match="empty partner family"):
            check(core, query_domain, [], region, budget=budget())


def test_support_outer_domain_and_common_core_output_match_the_pilot(
    first_row: RowInputs, frame: Frame
) -> None:
    _, _, row, core = first_row
    world = frame.world(6)
    residual = [convex(node.points(value)) for value in row["residual_polygons"]]
    assert collision.support_outer_domain(residual, world) == frozen_pilot.phase2_outer(
        row, fractions_of(world)
    )
    assert collision.outward_round(Q(1, 3)) == frozen_pilot.outward_round(Fraction(1, 3))
    published = {
        **row,
        "outer_bounds": [
            {"normal": list(normal), "upper": str(bound[2])}
            for normal, bound in zip(
                collision.SUPPORT_NORMALS,
                [
                    (
                        nx,
                        ny,
                        collision.outward_round(
                            max(nx * x + ny * y for polygon in residual for x, y in polygon)
                        ),
                    )
                    for nx, ny in collision.SUPPORT_NORMALS
                ],
                strict=True,
            )
        ],
    }
    published["outer_domain"] = [
        [str(x), str(y)] for x, y in collision.support_outer_domain(residual, world)
    ]
    planes = collision.common_core_output(published, core, residual, world)
    assert planes == frozen_pilot.verify_row_output(
        published, fractions_of(core), [fractions_of(r) for r in residual], fractions_of(world)
    )
    assert planes == len(core)
    published["common_core_halfplanes"] = published["common_core_halfplanes"][1:]
    with pytest.raises(RefusalError, match="common-core output planes"):
        collision.common_core_output(published, core, residual, world)
