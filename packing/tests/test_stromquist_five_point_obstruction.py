"""Check rational escape certificates with an independent projection predicate."""

from __future__ import annotations

import json
import subprocess
import sys
import xml.etree.ElementTree as ET
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path
from typing import cast

import pytest

from cases.stromquist.five_point_obstruction import (
    AXIS_SIDE,
    BOTTOM_DIAMOND,
    INNER_CORNERS,
    SVG_ARTIFACT,
    Point,
    Polygon,
    axis_square,
    control_record,
    control_svg,
    diamond_witnesses,
    escape_square,
    verify_escape,
)


def _assert_independent_escape(vertices: Polygon, points: tuple[Point, ...]) -> None:
    """Use dot-product intervals in the two side directions, not edge determinants."""
    origin = vertices[0]
    u = (vertices[1][0] - origin[0], vertices[1][1] - origin[1])
    v = (vertices[3][0] - origin[0], vertices[3][1] - origin[1])
    side_squared = u[0] ** 2 + u[1] ** 2
    assert side_squared >= AXIS_SIDE**2
    assert side_squared == v[0] ** 2 + v[1] ** 2
    assert u[0] * v[0] + u[1] * v[1] == 0
    assert vertices[2] == (origin[0] + u[0] + v[0], origin[1] + u[1] + v[1])
    assert all(0 <= value <= 3 for point in vertices for value in point)
    for x, y in points:
        pu = (x - origin[0]) * u[0] + (y - origin[1]) * u[1]
        pv = (x - origin[0]) * v[0] + (y - origin[1]) * v[1]
        assert pu < 0 or pu > side_squared or pv < 0 or pv > side_squared


def test_every_five_subset_of_three_by_three_grid_has_a_strict_escape() -> None:
    grid = tuple((Fraction(x, 2), Fraction(y, 2)) for x, y in product((0, 3, 6), repeat=2))
    for points in combinations(grid, 5):
        _assert_independent_escape(escape_square(points).vertices, points)


def test_closed_unit_hitting_set_and_asymmetric_extra_site_use_diamonds() -> None:
    for extra in ((Fraction(3, 2), Fraction(3, 2)), (Fraction(7, 5), Fraction(1, 3))):
        points = (*INNER_CORNERS, extra)
        escape = escape_square(points)
        assert escape.branch.startswith("diamond-")
        assert escape.record(points)["side_squared"] == "20449/20000"
        _assert_independent_escape(escape.vertices, points)


def test_four_shrunk_diamonds_avoid_inner_corners_and_have_exact_size() -> None:
    for vertices in diamond_witnesses():
        _assert_independent_escape(vertices, INNER_CORNERS)
        edge = (vertices[1][0] - vertices[0][0], vertices[1][1] - vertices[0][1])
        assert edge[0] ** 2 + edge[1] ** 2 == Fraction(20449, 20000)


def test_axis_squares_at_all_four_container_corners() -> None:
    points = ((Fraction(3, 2), Fraction(3, 2)),)
    for x, y in product((Fraction(0), 3 - AXIS_SIDE), repeat=2):
        vertices = axis_square((x, y))
        _assert_independent_escape(vertices, points)
        assert min(px for px, _ in vertices) == x
        assert max(px for px, _ in vertices) == x + AXIS_SIDE
        assert min(py for _, py in vertices) == y
        assert max(py for _, py in vertices) == y + AXIS_SIDE


def test_geometry_verifier_rejects_boundary_hit_and_corrupt_square() -> None:
    with pytest.raises(ValueError, match="on or inside"):
        verify_escape(BOTTOM_DIAMOND, (BOTTOM_DIAMOND[0],))
    bad = (*BOTTOM_DIAMOND[:3], (Fraction(0), Fraction(0)))
    with pytest.raises(ValueError, match="four sides"):
        verify_escape(bad, ())
    with pytest.raises(ValueError, match="counterclockwise"):
        verify_escape(tuple(reversed(BOTTOM_DIAMOND)), ())


def test_constructor_rejects_input_outside_the_proposition() -> None:
    with pytest.raises(ValueError, match="at most five"):
        escape_square((*INNER_CORNERS, (Fraction(0), Fraction(0)), (Fraction(3), Fraction(3))))
    with pytest.raises(ValueError, match="at most five"):
        escape_square(((Fraction(-1), Fraction(0)),))


@pytest.mark.parametrize("invalid", [(0.5, 1.0), (Fraction(1),), [Fraction(1), Fraction(2)]])
def test_public_entry_points_refuse_float_or_malformed_coordinates(invalid: object) -> None:
    bad = cast(Point, invalid)
    with pytest.raises(ValueError, match="pair of Fraction"):
        escape_square((bad,))
    with pytest.raises(ValueError, match="pair of Fraction"):
        verify_escape(BOTTOM_DIAMOND, (bad,))
    with pytest.raises(ValueError, match="pair of Fraction"):
        axis_square(bad)


def test_verifier_rejects_side_above_one_but_below_the_quantitative_claim() -> None:
    side = Fraction(201, 200)
    small = (
        (Fraction(0), Fraction(0)),
        (side, Fraction(0)),
        (side, side),
        (Fraction(0), side),
    )
    with pytest.raises(ValueError, match="at least 101/100"):
        verify_escape(small, ())


def test_cli_retains_controls_and_accepts_exact_rational_sites(tmp_path: Path) -> None:
    output = tmp_path / "obstruction.json"
    svg = tmp_path / "obstruction.svg"
    command = [sys.executable, "-m", "cases.stromquist.five_point_obstruction"]
    completed = subprocess.run(
        [*command, "--output", str(output), "--svg", str(svg)],
        cwd=Path(__file__).resolve().parents[1],
        check=True,
        capture_output=True,
        text=True,
    )
    assert completed.stdout == output.read_text()
    assert json.loads(completed.stdout) == control_record()
    retained = (
        Path(__file__).resolve().parents[1] / "cases/stromquist/five-point-obstruction.json"
    )
    assert json.loads(retained.read_text()) == control_record()
    assert svg.read_text() == SVG_ARTIFACT.read_text() == control_svg()
    drawing = ET.fromstring(svg.read_text())
    assert len(drawing.findall(".//{http://www.w3.org/2000/svg}circle")) == 5
    assert len(drawing.findall(".//{http://www.w3.org/2000/svg}polygon")) == 1
    supplied = subprocess.run(
        [*command, "--point", "1/2,2"],
        cwd=Path(__file__).resolve().parents[1],
        check=True,
        capture_output=True,
        text=True,
    )
    assert json.loads(supplied.stdout)["points"] == [["1/2", "2"]]
