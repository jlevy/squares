"""Exact Theorem 3 source controls, never H-036's perturbed-angle target."""

from __future__ import annotations

import subprocess
import sys
from fractions import Fraction

import pytest

from cases.stromquist.restricted_orientation import (
    Stratum,
    cell_witness,
    clip_polygon,
    cover_replay,
    direct_membership,
    direction,
    event_cells,
    source_field,
    source_replay,
    unproject,
)


def test_singleton_domain_keeps_a_closed_boundary_hit() -> None:
    field = source_field()
    result = cover_replay(field.one, 0, ((field.one, field.one),))
    assert result.escape is None
    assert result.reachable_by_dimension == (1, 0, 0)


def test_escape_and_all_event_dimensions_are_retained() -> None:
    field = source_field()
    side = field.rational(4)
    points = ((field.rational(2), field.rational(2)),)
    result = cover_replay(side, 0, points)
    half = field.rational(Fraction(1, 2))
    assert result.escape == (half, half)
    assert result.reachable_by_dimension == (16, 24, 9)
    assert result.escape is not None
    assert direct_membership(side, 0, result.escape, points) == 0


def test_closed_clipping_keeps_line_and_point_intersections() -> None:
    field = source_field()
    zero, one = field.zero, field.one
    polygon = ((zero, zero), (one, zero), (one, one), (zero, one))
    line = clip_polygon(polygon, (one, zero, zero))
    assert set(line) == {(zero, zero), (zero, one)}
    u, v = Stratum(zero, zero), Stratum(zero, one)
    assert cell_witness(line, u, v) == (zero, one / 2)
    point = clip_polygon(line, (zero, one, zero))
    assert point == ((zero, zero),)
    assert cell_witness(point, u, u) == (zero, zero)
    assert cell_witness(point, u, v) is None


def test_rotated_masks_match_corner_determinants_and_guards_refuse() -> None:
    field = source_field()
    side = field.rational(2)
    offset = field.alpha / 4
    points = (
        (field.one + offset, field.one + offset),
        (field.one - offset, field.one + offset),
    )
    dimensions = set()
    for cell in event_cells(side, 45, points):
        dimensions.add(cell.dimension)
        center = unproject(cell.witness, direction(side, 45))
        assert direct_membership(side, 45, center, points) == cell.covered
    assert dimensions == {0, 1, 2}
    for angle in (1, 44, 46, True):
        with pytest.raises(ValueError, match="exactly 0 or 45"):
            cover_replay(side, angle, points)
    with pytest.raises(ValueError, match="empty"):
        cover_replay(field.one, 45, points)
    with pytest.raises(ValueError, match="one exact field"):
        cover_replay(side, 0, ((source_field().one, field.one),))
    with pytest.raises(ValueError, match="containment"):
        direct_membership(side, 0, (field.zero, field.zero), points)


def test_original_theorem_three_closed_unit_obligations() -> None:
    result = source_replay()
    assert result["obstructions"] == []
    assert result["complete"] is True


def test_larger_open_square_contains_closed_unit_boundary_points() -> None:
    field = source_field()
    side = field.rational(2)
    center = (field.one, field.one)
    point = ((field.rational("3/2"), field.rational("3/2")),)
    assert direct_membership(side, 0, center, point) == 1
    assert direct_membership(side, 0, center, point, closed=False) == 0
    assert (
        direct_membership(side, 0, center, point, square_side=Fraction(6, 5), closed=False) == 1
    )


def test_command_refuses_target_options() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "cases.stromquist.restricted_orientation", "--side", "1939/500"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "unrecognized arguments" in result.stderr
    assert not result.stdout
