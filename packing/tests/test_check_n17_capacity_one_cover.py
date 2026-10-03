"""Exact controls for the H-266 capacity-one cover checker."""

from __future__ import annotations

import hashlib
import itertools
import json
from dataclasses import replace
from fractions import Fraction as Q
from functools import cache
from math import comb
from pathlib import Path

from devtools import check_n17_capacity_one_cover as cover
from devtools.check_n17_capacity_one_cover import (
    CERTIFICATE,
    ENDPOINT,
    GRID_25,
    RECIPE_BOX,
    TABBED_24,
    TRIANGLE,
    UNIQUE_24,
    VORONOI_24,
    Cell,
    Design,
    Endpoint,
    build_cover,
    burnside,
    capacity_proof,
    coverage,
    d4_apply,
    d4_permutations,
    domain_containment,
    endpoint,
    falsifier_control,
    family_state,
    load_root_box,
    poly_value,
    ring_cells,
    side_spans,
    sturm_root_count,
    unique_state,
    wall_bound,
    wall_lemma,
    wall_polynomial,
)


@cache
def cells_of(design: Design) -> tuple[Cell, ...]:
    return tuple(build_cover(design))


@cache
def root_point() -> Endpoint:
    t, b, _ = load_root_box(CERTIFICATE)
    return endpoint(t, b)


def inside(cell: Cell, point: tuple[Q, Q]) -> bool:
    count = len(cell.vertices)
    return all(
        cover.cross(cell.vertices[i], cell.vertices[(i + 1) % count], point) >= 0
        for i in range(count)
    )


def test_wall_polynomial_is_the_cleared_bound() -> None:
    depth, width = Q(911, 1000), Q(529, 750)
    polynomial = wall_polynomial(depth, width)
    for tau in (Q(0), Q(1, 7), Q(1, 3), Q(5, 8), Q(1)):
        cleared = poly_value(polynomial, tau) / (1 + tau * tau) ** 2
        assert cleared == wall_bound(depth, width, tau)


def test_wall_lemma_accepts_the_design_and_the_h259_case() -> None:
    for depth, width in ((Q(39, 50), Q(39, 50)), (Q(911, 1000), Q(529, 750)), (Q(3, 4),) * 2):
        record = wall_lemma(depth, width)
        assert record["passed"], (depth, width)
        assert record["sturm_roots_in_0_1"] == 0
        assert Q(record["max_G_upper_bound"]) < 0


def test_wall_lemma_refuses_wide_cells_with_an_exact_witness() -> None:
    for depth, width in ((Q(4, 5), Q(4, 5)), (Q(911, 1000), Q(3, 4)), (Q(1), Q(0))):
        record = wall_lemma(depth, width)
        assert not record["passed"]
        assert Q(record["G_at_refuting_tau"]) >= 0


def test_sturm_counts_a_double_root_and_a_simple_pair() -> None:
    # -(tau - 1/2)^2 touches zero once; (tau - 1/4)(tau - 3/4) crosses twice.
    assert sturm_root_count([Q(-1, 4), Q(1), Q(-1)], Q(0), Q(1)) == 1
    assert sturm_root_count([Q(3, 16), Q(-1), Q(1)], Q(0), Q(1)) == 2
    assert not wall_lemma(Q(1), Q(0))["sturm_negative"]


def test_every_design_cell_has_a_capacity_proof() -> None:
    records = [capacity_proof(cell, {}) for cell in cells_of(TABBED_24)]
    assert all(record["passed"] for record in records)
    by_kind = {cell.kind: [] for cell in cells_of(TABBED_24)}
    for cell, record in zip(cells_of(TABBED_24), records, strict=True):
        by_kind[cell.kind].append(record)
    assert {record["wall"] for record in by_kind["corner"]} == {"W", "E"}
    assert all(record["argument"] == "wall-lemma" for record in by_kind["side"])
    assert all(record["argument"] == "diameter" for record in by_kind["interior"])
    assert max(Q(record["squared_diameter"]) for record in by_kind["interior"]) == Q(
        976625, 1000000
    )


def test_diameter_one_and_the_h259_pair_are_refused() -> None:
    unit = Cell(
        "unit",
        "interior",
        cover.convex_hull(
            [(Q(2), Q(2)), (Q(13, 5), Q(2)), (Q(13, 5), Q(14, 5)), (Q(2), Q(14, 5))]
        ),
    )
    record = capacity_proof(unit, {})
    assert record["squared_diameter"] == "1"
    assert not record["passed"]
    control = falsifier_control()
    assert control["passed"]
    assert control["pair_gap_along_u"] == "1/100"


def test_the_cover_is_complete_and_a_hole_is_found() -> None:
    cells = list(cells_of(TABBED_24))
    assert coverage(cells)["passed"]
    removed = next(cell for cell in cells if cell.name == "interior-NE")
    holed = coverage([cell for cell in cells if cell is not removed])
    assert not holed["passed"]
    witness = (Q(holed["witness"][0]), Q(holed["witness"][1]))
    assert inside(removed, witness)
    assert not any(inside(cell, witness) for cell in cells if cell is not removed)


def test_a_rational_grid_of_box_points_is_covered() -> None:
    cells = cells_of(TABBED_24)
    steps = 24
    for i, j in itertools.product(range(steps + 1), repeat=2):
        point = (
            cover.LO + (cover.HI - cover.LO) * Q(i, steps),
            cover.LO + (cover.HI - cover.LO) * Q(j, steps) + Q(1, 997) * (j % 2),
        )
        point = (point[0], min(point[1], cover.HI))
        assert any(inside(cell, point) for cell in cells), point


def test_a_ring_gap_is_found() -> None:
    interior = [cell for cell in cells_of(TABBED_24) if cell.kind == "interior"]
    shallow = replace(TABBED_24, depth=TABBED_24.depth - Q(1, 1000))
    result = coverage(ring_cells(shallow) + interior)
    assert not result["passed"]


def test_d4_action_and_burnside_count() -> None:
    permutations = d4_permutations(list(cells_of(TABBED_24)))
    assert permutations is not None
    census = burnside(permutations)
    assert census["states"] == 346104
    assert census["fixed_counts"] == {
        "r0": 346104,
        "r1": 0,
        "r2": 0,
        "r3": 0,
        "f0": 660,
        "f1": 660,
        "f2": 660,
        "f3": 660,
    }
    assert census["orbits"] == 43593
    broken = list(cells_of(TABBED_24))
    broken[-1] = Cell(
        "bent", "interior", cover.convex_hull([*broken[-1].vertices, (Q(2), Q(1))])
    )
    assert d4_permutations(broken) is None


def test_burnside_matches_brute_force_on_the_ring() -> None:
    ring = ring_cells(TABBED_24)
    permutations = d4_permutations(ring)
    assert permutations is not None
    size = 5
    orbits = {
        min(
            tuple(sorted(permutation[i] for i in subset))
            for permutation in permutations.values()
        )
        for subset in itertools.combinations(range(len(ring)), size)
    }
    assert burnside(permutations, size)["orbits"] == len(orbits)


def test_d4_generators_have_the_right_orders() -> None:
    point = (Q(1), Q(3, 7))
    assert d4_apply("r1", d4_apply("r1", point)) == d4_apply("r2", point)
    assert d4_apply("r2", d4_apply("r2", point)) == point
    assert d4_apply("f0", d4_apply("f0", point)) == point
    assert len({d4_apply(action, point) for action in cover.D4}) == 8


def test_the_endpoint_family_lies_in_one_state_on_the_tabbed_cover() -> None:
    point = root_point()
    assert domain_containment(point)["passed"]
    result = family_state(list(cells_of(TABBED_24)), point, TRIANGLE)
    assert result["one_state"]
    cells = {entry["label"]: entry["cell"] for entry in result["squares"]}
    assert cells[13] == "interior-S"
    assert cells[11] == "interior-W"
    assert result["least_margin_square"] == 9
    assert Q(result["least_margin_lower_bound"]) >= Q(1, 1000)


def test_the_untabbed_cover_and_the_recipe_box_straddle_seams() -> None:
    point = root_point()
    untabbed = family_state(list(cells_of(VORONOI_24)), point, TRIANGLE)
    assert not untabbed["one_state"]
    assert untabbed["unassignable"] == [11, 13]
    recipe = family_state(list(cells_of(TABBED_24)), point, RECIPE_BOX)
    assert recipe["unassignable"] == [13]


def test_the_25_cell_grid_holds_the_recipe_box_above_the_threshold() -> None:
    cells = list(cells_of(GRID_25))
    result = family_state(cells, root_point(), RECIPE_BOX)
    assert result["one_state"]
    permutations = d4_permutations(cells)
    assert permutations is not None
    orbits = burnside(permutations)["orbits"]
    assert orbits == 136080
    assert orbits > cover.ORBIT_THRESHOLD == 135196
    assert 8 * orbits >= comb(25, 17)


def test_the_tabbed_cover_realises_a_second_state_through_squares_11_and_13() -> None:
    point = root_point()
    cells = list(cells_of(TABBED_24))
    centroid = unique_state(cells, point, ENDPOINT, family_state(cells, point, ENDPOINT))
    assert not centroid["unique"]
    assert centroid["squares_in_a_second_cell"] == [13]
    square = centroid["squares"][12]
    assert (square["cell"], square["nearest_other_cell"]) == ("interior-S", "side-S1")
    assert Q(square["outside_lower_bound"]) < 0  # 0.0023 inside side-S1, as reviewed
    triangle = unique_state(cells, point, TRIANGLE, family_state(cells, point, TRIANGLE))
    assert not triangle["unique"]
    assert triangle["squares_in_a_second_cell"] == [11, 13]
    assert triangle["squares"][10]["nearest_other_cell"] == "interior-SW"


def test_the_unique_cover_holds_the_family_in_exactly_one_cell_per_square() -> None:
    point = root_point()
    cells = list(cells_of(UNIQUE_24))
    family = family_state(cells, point, TRIANGLE)
    assert family["one_state"]
    assigned = {entry["label"]: entry["cell"] for entry in family["squares"]}
    assert assigned[13] == "side-S1"
    assert assigned[11] == "interior-W"
    assert assigned[6] == "side-S2"
    assert Q(family["least_margin_lower_bound"]) >= Q(1, 1000)
    result = unique_state(cells, point, TRIANGLE, family)
    assert result["unique"]
    assert result["squares_in_a_second_cell"] == []
    assert result["least_outside_square"] == 13
    assert Q(result["least_outside_lower_bound"]) >= Q(1, 1000)
    # Exactly one closed cell holds any member of the slider box, by exact containment.
    for label in (11, 13):
        for x, y in cover.family_points(point, label, TRIANGLE):
            holders = [cell.name for cell in cells if inside(cell, (x.lo, y.lo))]
            assert holders == [assigned[label]], (label, holders)


def test_the_unique_cover_keeps_capacity_coverage_and_the_orbit_count() -> None:
    cells = list(cells_of(UNIQUE_24))
    assert len(cells) == 24
    assert all(capacity_proof(cell, {})["passed"] for cell in cells)
    assert coverage(cells)["passed"]
    permutations = d4_permutations(cells)
    assert permutations is not None
    assert burnside(permutations)["orbits"] == 43593
    spans = side_spans(UNIQUE_24)
    assert [end - start for start, end, _ in spans] == [Q(529, 750), Q(257, 375), Q(529, 750)]
    assert [depth for _, _, depth in spans] == [Q(911, 1000), Q(93, 100), Q(911, 1000)]
    assert wall_lemma(Q(93, 100), Q(257, 375))["passed"]
    assert not wall_lemma(Q(93, 100), Q(529, 750))["passed"]  # S1 had to narrow
    assert spans[-1][1] == cover.HI - UNIQUE_24.corner


def test_cli_writes_a_passing_receipt(tmp_path: Path) -> None:
    output = tmp_path / "receipt.json"
    assert cover.main(["--output", str(output)]) == 0
    receipt = json.loads(output.read_text(encoding="utf-8"))
    assert receipt["design"]["name"] == UNIQUE_24.name
    assert receipt["criterion"]["passed"]
    assert receipt["criterion"]["family_unique_state_triangle"]
    assert receipt["controls"]["passed"]
    assert receipt["census"]["orbits"] == 43593
    module = Path(cover.__file__).read_bytes()
    assert receipt["module_sha256"] == hashlib.sha256(module).hexdigest()
