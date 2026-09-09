"""Geometry and receipt controls for the conditional residual-cover pilot."""

from __future__ import annotations

import json
from fractions import Fraction
from itertools import pairwise
from pathlib import Path

import numpy as np

from devtools.run_residual_cover_pilot import (
    ANGLE_LIMIT,
    exact_minimum_covered_mass,
    placement_cells_on_pieces,
    point_in_closed_polygon,
    residual_domain_pieces,
    run_pair,
    unrestricted_domain_pieces,
)
from sqpack.fractional.colgen import site_set_from_grids
from sqpack.fractional.generate import direction_net, net_half_tangents, placement_cells
from sqpack.fractional.model import Atom, Direction, rotation_from_half_tangent

SIDE = Fraction(96, 25)
SHRINK = Fraction(9977, 10000)
AXIS = rotation_from_half_tangent("axis", Fraction(0))


def _uv(direction: Direction, x: Fraction, y: Fraction) -> tuple[Fraction, Fraction]:
    return (
        direction.ux * x + direction.uy * y,
        direction.vx * x + direction.vy * y,
    )


def _in_pieces(point: tuple[Fraction, Fraction], pieces: tuple) -> bool:
    return any(point_in_closed_polygon(point, polygon) for polygon in pieces)


def _sat_admissible(
    direction: Direction,
    centre: tuple[Fraction, Fraction],
    outer_side: Fraction = SIDE,
    square_side: Fraction = SHRINK,
) -> bool:
    """Independent exact four-axis SAT against each fixed corner square."""

    x, y = centre
    cosine, sine = direction.ux, direction.uy
    half = square_side / 2
    extent = half * (cosine + sine)
    if not (extent <= x <= outer_side - extent and extent <= y <= outer_side - extent):
        return False
    axes = (
        (Fraction(1), Fraction(0)),
        (Fraction(0), Fraction(1)),
        (cosine, sine),
        (-sine, cosine),
    )
    obstacles = (
        (Fraction(1, 2), Fraction(1, 2)),
        (outer_side - Fraction(1, 2), Fraction(1, 2)),
        (Fraction(1, 2), outer_side - Fraction(1, 2)),
        (outer_side - Fraction(1, 2), outer_side - Fraction(1, 2)),
    )
    for obstacle_x, obstacle_y in obstacles:
        separated = False
        for axis_x, axis_y in axes:
            core_radius = half * (
                abs(axis_x * cosine + axis_y * sine) + abs(-axis_x * sine + axis_y * cosine)
            )
            obstacle_radius = (abs(axis_x) + abs(axis_y)) / 2
            gap = abs(axis_x * (x - obstacle_x) + axis_y * (y - obstacle_y))
            if gap >= core_radius + obstacle_radius:
                separated = True
                break
        if not separated:
            return False
    return True


def test_axis_domain_is_the_exact_central_cross_and_keeps_tangency() -> None:
    pieces = residual_domain_pieces(SIDE, SHRINK, AXIS)
    domain_low, strip_low = Fraction(9977, 20000), Fraction(29977, 20000)
    strip_high, domain_high = Fraction(46823, 20000), Fraction(66823, 20000)
    coordinates = (
        domain_low,
        strip_low - Fraction(1, 10000),
        strip_low,
        Fraction(2),
        strip_high,
        strip_high + Fraction(1, 10000),
        domain_high,
    )
    for x in coordinates:
        for y in coordinates:
            expected = (
                domain_low <= x <= domain_high
                and domain_low <= y <= domain_high
                and (strip_low <= x <= strip_high or strip_low <= y <= strip_high)
            )
            assert _in_pieces(_uv(AXIS, x, y), pieces) == expected, (x, y)
            assert _sat_admissible(AXIS, (x, y)) == expected, (x, y)
    # The core tangent to the bottom-left obstacle is retained; moving it toward the
    # obstacle by one rational step creates strict overlap and is rejected.
    assert _in_pieces(_uv(AXIS, strip_low, domain_low), pieces)
    assert not _in_pieces(_uv(AXIS, strip_low - Fraction(1, 10000), domain_low), pieces)


def test_rotated_piece_union_matches_full_sat_and_reflects_with_the_angle() -> None:
    direction = rotation_from_half_tangent("3-4-5", Fraction(1, 3))
    cosine, sine = direction.ux, direction.uy
    assert (cosine, sine) == (Fraction(4, 5), Fraction(3, 5))
    pieces = residual_domain_pieces(SIDE, SHRINK, direction)
    radius = Fraction(37977, 28000)
    tangent = (radius, radius)
    overlap = (
        radius - cosine / 10000,
        radius - sine / 10000,
    )
    assert _in_pieces(_uv(direction, *tangent), pieces)
    assert _sat_admissible(direction, tangent)
    assert not _in_pieces(_uv(direction, *overlap), pieces)
    assert not _sat_admissible(direction, overlap)

    samples = tuple(Fraction(value, 20) for value in range(10, 68, 3))
    reflected = Direction("reflection", sine, cosine, -cosine, sine)
    reflected_pieces = residual_domain_pieces(SIDE, SHRINK, reflected)
    for x in samples:
        for y in samples:
            expected = _sat_admissible(direction, (x, y))
            assert _in_pieces(_uv(direction, x, y), pieces) == expected
            # A diagonal reflection also sends theta to pi/2-theta.
            assert _in_pieces(_uv(reflected, y, x), reflected_pieces) == expected

    # The retained endpoint lies just beyond 45 degrees.  The six-piece formulas
    # require only nonnegative cosine and sine; they do not assume cosine >= sine.
    endpoint = rotation_from_half_tangent("endpoint", ANGLE_LIMIT)
    assert endpoint.ux < endpoint.uy
    endpoint_pieces = residual_domain_pieces(SIDE, SHRINK, endpoint)
    for x in samples:
        for y in samples:
            assert _in_pieces(_uv(endpoint, x, y), endpoint_pieces) == _sat_admissible(
                endpoint, (x, y)
            )


def _axis_cross_brute(
    atoms: tuple[Atom, ...], outer_side: Fraction, square_side: Fraction
) -> tuple[Fraction, int]:
    """Independent cell enumeration for the axis-aligned central cross."""

    half = square_side / 2
    domain_low, domain_high = half, outer_side - half
    strip_low, strip_high = 1 + half, outer_side - 1 - half
    events_x = sorted(
        {domain_low, strip_low, strip_high, domain_high}
        | {atom.x + offset for atom in atoms for offset in (-half, half)}
    )
    events_y = sorted(
        {domain_low, strip_low, strip_high, domain_high}
        | {atom.y + offset for atom in atoms for offset in (-half, half)}
    )
    masses: list[Fraction] = []
    for x0, x1 in pairwise(events_x):
        x = (x0 + x1) / 2
        for y0, y1 in pairwise(events_y):
            y = (y0 + y1) / 2
            in_cross = (
                domain_low < x < domain_high
                and domain_low < y < domain_high
                and (strip_low <= x <= strip_high or strip_low <= y <= strip_high)
            )
            if in_cross:
                masses.append(
                    sum(
                        (
                            atom.weight
                            for atom in atoms
                            if abs(atom.x - x) <= half and abs(atom.y - y) <= half
                        ),
                        Fraction(0),
                    )
                )
    return min(masses), len(masses)


def test_exact_residual_sweep_agrees_with_independent_axis_cross_cells() -> None:
    atoms = (
        Atom("a", Fraction(3, 2), Fraction(2), Fraction(1, 2)),
        Atom("b", Fraction(5, 2), Fraction(2), Fraction(1, 3)),
        Atom("c", Fraction(2), Fraction(3, 2), Fraction(2, 3)),
        Atom("d", Fraction(2), Fraction(5, 2), Fraction(3, 4)),
        Atom("e", Fraction(2), Fraction(2), Fraction(5, 6)),
    )
    expected = _axis_cross_brute(atoms, Fraction(4), Fraction(1))
    assert (
        exact_minimum_covered_mass(atoms, AXIS, Fraction(4), Fraction(1), residual=True)
        == expected
    )


def test_unrestricted_piece_separator_recovers_the_existing_float_minimum() -> None:
    sites = site_set_from_grids(Fraction(3), (5,), Fraction(1, 2))
    points = sites.points()
    membership = sites.membership()
    orbit_weights = np.arange(1, len(sites.orbits) + 1, dtype=float) / 7
    weights = orbit_weights[membership]
    expected = placement_cells(points, weights, AXIS, 3.0, 1.0, keep=100)
    actual, _ = placement_cells_on_pieces(
        points,
        weights,
        AXIS,
        Fraction(3),
        Fraction(1),
        residual=False,
        keep=100,
        max_event_cells=100_000,
    )
    expected_rows = {(mass, tuple(mask.tolist())) for mass, *_, mask in expected}
    actual_rows = {(mass, tuple(mask.tolist())) for mass, *_, mask in actual}
    assert actual_rows == expected_rows


def test_rotated_separator_recovers_cells_collapsed_by_float_geometry() -> None:
    """A rational fallback retains minima from sub-ULP residual slivers."""

    sites = site_set_from_grids(Fraction(4), (9,), Fraction(1, 2))
    direction = direction_net(net_half_tangents(ANGLE_LIMIT, 180))[93]
    points = sites.points()
    weights = np.ones(sites.size)
    expected, _ = exact_minimum_covered_mass(
        tuple(
            Atom(str(index), x, y, Fraction(1))
            for index, (x, y) in enumerate(sites.positions())
        ),
        direction,
        Fraction(4),
        Fraction(1),
        residual=True,
    )
    actual, _ = placement_cells_on_pieces(
        points,
        weights,
        direction,
        Fraction(4),
        Fraction(1),
        residual=True,
        keep=100,
        max_event_cells=500_000,
        exact_points=sites.positions(),
    )
    assert len(actual) == 100
    assert actual[0][0] == float(expected)
    assert all(mass == float(weights[covers].sum()) for mass, _, _, covers in actual)


def test_deadline_writes_both_partial_raw_arms_and_never_overwrites(tmp_path: Path) -> None:
    sites = site_set_from_grids(Fraction(4), (3,), Fraction(1, 2))
    directions = direction_net((Fraction(0),))
    output = tmp_path / "paired.json"
    support = {
        "source": "three-by-three control",
        "sha256": "control",
        "orbits": len(sites.orbits),
        "sites": sites.size,
        "coordinates": [],
    }
    record = run_pair(
        sites,
        directions,
        (0,),
        Fraction(1),
        support=support,
        output=output,
        max_rounds=2,
        rows_per_direction=1,
        deadline_seconds=1e-12,
        max_event_cells=100_000,
        max_round_cells=100_000,
        scale=1000,
    )
    assert record["status"] == "partial"
    saved = json.loads(output.read_text())
    assert set(saved["arms"]) == {"unrestricted", "residual"}
    for arm in saved["arms"].values():
        assert arm["stopped"].startswith("deadline")
        assert arm["exact_validation"] is None
        assert len(arm["orbit_weights"]) == len(sites.orbits)
    try:
        run_pair(
            sites,
            directions,
            (0,),
            Fraction(1),
            support=support,
            output=output,
            max_rounds=1,
            rows_per_direction=1,
            deadline_seconds=1,
            max_event_cells=100_000,
            max_round_cells=100_000,
            scale=1000,
        )
    except FileExistsError:
        pass
    else:
        raise AssertionError("the existing raw proposal was overwritten")


def test_domain_piece_labels_stay_in_receipt_order() -> None:
    # A lightweight shape guard: unrestricted remains one convex component while the
    # residual instrument retains all six named components, including degenerate axis
    # caps that scoring safely skips because their points lie on strip boundaries.
    assert len(unrestricted_domain_pieces(SIDE, SHRINK, AXIS)) == 1
    assert len(residual_domain_pieces(SIDE, SHRINK, AXIS)) == 6
