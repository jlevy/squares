"""Flip regularization: the eight point maps, the rule on fixtures whose answer is known by
hand, the canonical pose's invariance on real renderings, and the record.

Three unit squares in a side-2 box end with the empty cell upper right, and a 3 x 3 grid
leaves its empty corner there and two empty cells at the right end of the top row, as the
catalogues draw the grids. One tilted square in the lower-right cell of every grid ties
until the final key and is decided by its tilt's sign. Real renderings, each drawn from
all eight of its poses, decide one picture; a symmetric one keeps its published pose, and
so does n = 11. The record's check names a count whose row the rule no longer gives.
"""

from __future__ import annotations

import json
import math
from collections.abc import Callable
from fractions import Fraction
from functools import cache
from pathlib import Path

import pytest

from devtools.flip_regularization import (
    DESCRIPTIONS,
    IDENTITY,
    POSES,
    RECORD,
    TOLERANCE,
    Decision,
    Picture,
    Pose,
    check,
    decide,
    decide_counts,
    differences,
    drawn_views,
    grid_weights,
    image_weights,
    invariant,
    orient_polygon,
    picture,
    placements,
    poses,
    quadtree_cells,
    rendering_squares,
    same_picture,
    strongest,
    text,
    totals,
)

UNIT = ((0, 0), (1, 0), (1, 1), (0, 1))
type Squares = list[list[tuple[float, float]]]

#: The module docstring's table: each pose's composite map, with side `s`.
TABLE: dict[Pose, Callable[[Fraction, Fraction, Fraction], tuple[Fraction, Fraction]]] = {
    Pose(rotate=0, flip=False): lambda x, y, _s: (x, y),
    Pose(rotate=90, flip=False): lambda x, y, s: (s - y, x),
    Pose(rotate=180, flip=False): lambda x, y, s: (s - x, s - y),
    Pose(rotate=270, flip=False): lambda x, y, s: (y, s - x),
    Pose(rotate=0, flip=True): lambda x, y, s: (s - y, s - x),
    Pose(rotate=90, flip=True): lambda x, y, s: (s - x, y),
    Pose(rotate=180, flip=True): lambda x, y, _s: (y, x),
    Pose(rotate=270, flip=True): lambda x, y, s: (x, s - y),
}


@cache
def _picture(n: int) -> Picture:
    return picture(n, drawn_views())


def _cells(filled: list[tuple[int, int]], *, tilt: float = 0.0) -> Squares:
    """Unit squares centred in the given unit cells, `(column, row)` from the lower left,
    each turned `tilt` degrees about its centre."""
    cosine, sine = math.cos(math.radians(tilt)), math.sin(math.radians(tilt))
    squares = []
    for column, row in filled:
        cx, cy = column + 0.5, row + 0.5
        squares.append(
            [
                (
                    cx + (x - 0.5) * cosine - (y - 0.5) * sine,
                    cy + (x - 0.5) * sine + (y - 0.5) * cosine,
                )
                for x, y in UNIT
            ]
        )
    return squares


def _drawn_cells(squares: Squares, pose: Pose, side: float) -> set[tuple[int, int]]:
    """The unit cells a grid picture fills once `pose` draws it."""
    return {
        (round(min(x for x, _y in image)), round(min(y for _x, y in image)))
        for image in (orient_polygon(pose, corners, side) for corners in squares)
    }


# --------------------------------------------------------------------------- poses


def test_each_pose_is_the_composite_its_table_row_states() -> None:
    side = Fraction(7, 2)
    points = [(Fraction(1, 3), Fraction(5, 4)), (Fraction(0), Fraction(7, 2)), (side, side)]
    assert tuple(TABLE) == POSES
    for pose, composite in TABLE.items():
        for x, y in points:
            assert pose.point(x, y, side) == composite(x, y, side)


def test_each_pose_reads_as_its_description() -> None:
    side = Fraction(6)
    lines = {
        "mirror left-right": lambda t: (side / 2, t),
        "mirror top-bottom": lambda t: (t, side / 2),
        "mirror across the rising diagonal": lambda t: (t, t),
        "mirror across the falling diagonal": lambda t: (t, side - t),
    }
    for pose in POSES[4:]:
        line = lines[DESCRIPTIONS[pose]]
        for t in (Fraction(0), Fraction(1, 3), Fraction(5)):
            x, y = line(t)
            assert pose.point(x, y, side) == (x, y)
    # Where each turn sends the right wall's midpoint.
    turns = {
        "unchanged": (side, side / 2),
        "quarter turn counter-clockwise": (side / 2, side),
        "half turn": (Fraction(0), side / 2),
        "quarter turn clockwise": (side / 2, Fraction(0)),
    }
    for pose in POSES[:4]:
        assert pose.point(side, side / 2, side) == turns[DESCRIPTIONS[pose]]


def test_the_poses_are_the_eight_symmetries_and_each_has_its_inverse() -> None:
    side = Fraction(7)
    assert POSES[0] is IDENTITY
    assert IDENTITY.identity
    assert len({pose.point(Fraction(1), Fraction(2), side) for pose in POSES}) == 8
    for pose in POSES:
        x, y = pose.point(Fraction(1), Fraction(2), side)
        assert pose.inverse().point(x, y, side) == (1, 2)
        assert pose.inverse().inverse() == pose
        assert pose.identity == (pose == IDENTITY)


def test_a_pose_record_round_trips_and_is_checked() -> None:
    for pose in POSES:
        assert Pose.from_record(pose.record()) == pose
    decision = Decision(Pose(rotate=90, flip=True), "grid-4", (1.0, 0.5, 0.25, 0.0))
    assert decision.record() == {
        "rotate": 90,
        "flip": True,
        "decided_by": "grid-4",
        "quadrants": [1.0, 0.5, 0.25, 0.0],
    }
    assert Pose.from_record(decision.record()) == decision.pose
    with pytest.raises(ValueError, match="rotate must be one of"):
        Pose.from_record({"rotate": 45, "flip": False})
    with pytest.raises(TypeError, match="rotate must be an integer"):
        Pose.from_record({"rotate": True, "flip": False})
    with pytest.raises(TypeError, match="flip must be a boolean"):
        Pose.from_record({"rotate": 90, "flip": "yes"})
    with pytest.raises(ValueError, match="needs flip"):
        Pose.from_record({"rotate": 90})


def test_orient_polygon_keeps_the_winding() -> None:
    side = Fraction(3)
    square = [(Fraction(x) + Fraction(1, 2), Fraction(y) + 1) for x, y in UNIT]

    def signed_area(polygon: list[tuple[Fraction, Fraction]]) -> Fraction:
        return (
            sum(
                (
                    polygon[index - 1][0] * y - x * polygon[index - 1][1]
                    for index, (x, y) in enumerate(polygon)
                ),
                Fraction(0),
            )
            / 2
        )

    assert signed_area(square) == 1
    for pose in POSES:
        image = orient_polygon(pose, square, side)
        assert signed_area(image) == 1
        assert set(image) == {pose.point(x, y, side) for x, y in square}


# --------------------------------------------------------------------------- the rule


def test_the_cells_are_read_in_quadtree_order() -> None:
    """Lower right, lower left, upper left, upper right, the quadrants first and then the
    cells inside each, so a cell's children are the four positions after its own times
    four."""
    lower_right, lower_left, upper_left, upper_right = (1, 0), (0, 0), (0, 1), (1, 1)
    assert quadtree_cells(2) == (lower_right, lower_left, upper_left, upper_right)
    assert quadtree_cells(4) == (
        (3, 0), (2, 0), (2, 1), (3, 1),  # the lower-right quadrant
        (1, 0), (0, 0), (0, 1), (1, 1),  # the lower-left quadrant
        (1, 2), (0, 2), (0, 3), (1, 3),  # the upper-left quadrant
        (3, 2), (2, 2), (2, 3), (3, 3),  # the upper-right quadrant
    )  # fmt: skip
    for cells in (2, 4, 8):
        fine = quadtree_cells(2 * cells)
        for index, (column, row) in enumerate(quadtree_cells(cells)):
            children = {(2 * column + dx, 2 * row + dy) for dx in (0, 1) for dy in (0, 1)}
            assert set(fine[4 * index : 4 * index + 4]) == children
    assert sorted(quadtree_cells(16)) == sorted((c, r) for c in range(16) for r in range(16))
    with pytest.raises(ValueError, match="power of two"):
        quadtree_cells(3)


def test_weights_clip_each_square_to_its_cells() -> None:
    diamond = _cells([(1, 1)], tilt=45.0)
    # A unit square turned 45 degrees about the centre of a side-3 box puts a quarter of
    # itself in each quadrant.
    assert grid_weights(diamond, 3.0, 2) == pytest.approx((0.25 / 2.25,) * 4, abs=1e-15)
    # About the centre of a side-2 box on the 4 x 4 grid, each of its corners pokes a
    # right triangle of area (sqrt(2)/2 - 1/2)^2 / 2 into each of the two edge cells
    # beside it, and the rest is the four central cells'.
    centred = [[(x - 0.5, y - 0.5) for x, y in corners] for corners in diamond]
    tip = (math.sqrt(2) / 2 - 0.5) ** 2 / 2
    central = {(1, 1), (2, 1), (1, 2), (2, 2)}
    edge = {(0, 1), (0, 2), (3, 1), (3, 2), (1, 0), (2, 0), (1, 3), (2, 3)}
    expected = tuple(
        (0.25 - 2 * tip) / 0.25 if cell in central else tip / 0.25 if cell in edge else 0.0
        for cell in quadtree_cells(4)
    )
    assert grid_weights(centred, 2.0, 4) == pytest.approx(expected, abs=1e-15)


def test_a_poses_weights_are_its_image_weights_permuted() -> None:
    """At every level, the weights the pose's image gives when clipped again are the
    source's permuted, in quadtree order, and each cell's weight is its four children's
    mean, the quadtree order's own structure."""
    eleven = _picture(11)
    squares, side = eleven.squares, eleven.side
    weights = {cells: grid_weights(squares, side, cells) for cells in (2, 4, 8, 16)}
    for cells, found in weights.items():
        for pose in POSES:
            image = [orient_polygon(pose, corners, side) for corners in squares]
            assert grid_weights(image, side, cells) == pytest.approx(
                image_weights(found, pose, cells), abs=1e-12
            )
        if cells < 16:
            finer = weights[2 * cells]
            for index, weight in enumerate(found):
                assert weight == pytest.approx(
                    sum(finer[4 * index : 4 * index + 4]) / 4, abs=1e-12
                )
    assert sum(weights[2]) / 4 == pytest.approx(11 / side**2, abs=1e-12)


def test_weights_within_the_tolerance_tie_and_weights_beyond_it_do_not() -> None:
    first, second = POSES[0], POSES[1]
    assert strongest([first, second], {first: (0.5,), second: (0.5 - 0.5e-9,)}) == [
        first,
        second,
    ]
    assert strongest([first, second], {first: (0.5,), second: (0.5 - 2e-9,)}) == [first]
    assert strongest([second, first], {first: (0.5 - 2e-9,), second: (0.5,)}) == [second]
    # A tie within the tolerance passes the choice to the next position.
    tied = {first: (0.5 - 0.5e-9, 0.1), second: (0.5, 0.1 + 2 * TOLERANCE)}
    assert strongest([first, second], tied) == [second]


@pytest.mark.parametrize("empty", [(0, 0), (1, 0), (0, 1), (1, 1)])
def test_three_squares_leave_the_empty_cell_upper_right(empty: tuple[int, int]) -> None:
    filled = [cell for cell in [(0, 0), (1, 0), (0, 1), (1, 1)] if cell != empty]
    squares = _cells(filled)
    decision = decide(squares, 2.0)
    assert decision.quadrants == (1.0, 1.0, 1.0, 0.0)
    assert decision.decided_by == "quadrants"
    assert _drawn_cells(squares, decision.pose, 2.0) == {(0, 0), (1, 0), (0, 1)}
    if empty == (1, 1):
        # Already there: the identity and the rising diagonal's mirror both draw it, and
        # the identity comes first.
        assert decision.pose == IDENTITY


def test_a_grid_leaves_its_empty_cells_upper_right_along_the_top_row() -> None:
    grid = {(column, row) for column in range(3) for row in range(3)}
    for corner in ((0, 0), (2, 0), (0, 2), (2, 2)):
        squares = _cells(sorted(grid - {corner}))
        assert _drawn_cells(squares, decide(squares, 3.0).pose, 3.0) == grid - {(2, 2)}
    # Two empty cells at the end of a row, from each of the eight poses: the top row's
    # right end, rows filled from the bottom as the catalogues draw a grid.
    pair = [(1, 2), (2, 2)]
    for pose in POSES:
        empty = {
            (round(x - 0.5), round(y - 0.5))
            for x, y in (pose.point(c + 0.5, r + 0.5, 3.0) for c, r in pair)
        }
        squares = _cells(sorted(grid - empty))
        decision = decide(squares, 3.0)
        assert _drawn_cells(squares, decision.pose, 3.0) == grid - set(pair), pose
        assert decision.pose == pose.inverse(), pose


def test_the_tilt_decides_between_mirror_images_that_share_every_centre() -> None:
    side = 64.0
    for tilt, expected in ((10.0, Pose(rotate=0, flip=True)), (-10.0, IDENTITY)):
        # One square inside the lower-right cell of every grid up to 16 x 16, centred on
        # the falling diagonal: only the identity and that diagonal's mirror keep it
        # there, and the weights tie.
        square = [(x + 61.5, y + 1.5) for x, y in _cells([(0, 0)], tilt=tilt)[0]]
        decision = decide([square], side)
        assert decision.decided_by == "squares"
        assert decision.pose == expected
        assert invariant([square], side)


def test_same_picture_pairs_squares_by_centre_and_tilt_modulo_a_quarter_turn() -> None:
    picture = [(0.5, 0.5, 44.9999999999), (1.5, 0.5, 0.0)]
    assert same_picture(picture, [(1.5, 0.5, 0.0), (0.5, 0.5, -45.0)])
    assert not same_picture(picture, [(1.5, 0.5, 0.0), (0.5, 0.5, 10.0)])
    assert not same_picture(picture, [(1.5, 0.5, 0.0), (0.5, 0.50001, 45.0)])
    assert not same_picture(picture, picture[:1])
    mirrored = placements([[(x, 1 - y) for x, y in _cells([(0, 0)], tilt=10.0)[0]]])
    assert not same_picture(placements(_cells([(0, 0)], tilt=10.0)), mirrored)


# --------------------------------------------------------------------------- real pictures


def test_a_rendering_is_read_y_up_in_units_of_a_square() -> None:
    """An L of three unit squares drawn at 100 pixels a unit, its frame offset, read back
    as the packing: y up from the frame's lower-left corner."""

    def svg_point(x: int, y: int) -> str:
        return f"{10 + 100 * x},{20 + 100 * (2 - y)}"

    polygons = "".join(
        '<polygon data-feature="square-fill" data-square="s" points="'
        f'{" ".join(svg_point(left + dx, bottom + dy) for dx, dy in UNIT)}" fill="#000000"/>'
        for left, bottom in ((0, 0), (1, 0), (0, 1))
    )
    squares, side = rendering_squares(
        '<svg><rect data-feature="container-outline" x="10" y="20" width="200" '
        f'height="200"/>{polygons}</svg>'
    )
    assert side == 2.0
    assert squares == _cells([(0, 0), (1, 0), (0, 1)])
    with pytest.raises(ValueError, match="no container outline"):
        rendering_squares(polygons)


def test_n_11_keeps_its_published_pose() -> None:
    eleven = _picture(11)
    assert eleven.rendering == "packing/atlas/known-best/rendering/n-011.svg"
    assert eleven.side == pytest.approx(3.877084, abs=1e-6)
    decision = decide(eleven.squares, eleven.side)
    assert decision.pose == IDENTITY
    assert decision.decided_by == "quadrants"


@pytest.mark.parametrize("n", [4, 5, 9])
def test_a_symmetric_packing_keeps_its_published_pose(n: int) -> None:
    drawn = _picture(n)
    decision = decide(drawn.squares, drawn.side)
    assert decision.pose == IDENTITY
    assert decision.decided_by == "quadrants"


def test_the_decisions_the_rule_was_measured_by() -> None:
    def decided(n: int) -> Decision:
        drawn = _picture(n)
        return decide(drawn.squares, drawn.side)

    ten = decided(10)
    assert ten.pose == IDENTITY
    assert ten.quadrants == pytest.approx((0.8607, 0.5946, 0.8607, 0.5946), abs=5e-5)
    assert decided(17).pose == Pose(rotate=90, flip=True)
    assert _picture(18).drawn == "view"
    assert decided(18).pose == Pose(rotate=90, flip=False)
    # 62 and 254 are grids short of a square number, drawn with their empty cells at the
    # top row's right end, and kept; a finer grid decides them.
    assert (decided(62).pose, decided(62).decided_by) == (IDENTITY, "grid-8")
    assert (decided(254).pose, decided(254).decided_by) == (IDENTITY, "grid-16")


@pytest.mark.parametrize("n", [10, 17, 18, 37, 62, 254])
def test_every_pose_of_a_picture_draws_the_same_picture(n: int) -> None:
    drawn = _picture(n)
    squares, side = drawn.squares, drawn.side
    pictures, stages = [], set()
    for pose in POSES:
        image = [orient_polygon(pose, corners, side) for corners in squares]
        decision = decide(image, side)
        stages.add(decision.decided_by)
        pictures.append(placements(orient_polygon(decision.pose, c, side) for c in image))
    assert len(stages) == 1
    assert all(same_picture(pictures[0], other) for other in pictures[1:])
    assert invariant(squares, side)
    # The canonical pose of a picture already in it is the identity.
    canonical = [orient_polygon(decide(squares, side).pose, c, side) for c in squares]
    assert decide(canonical, side).pose == IDENTITY


def test_the_command_decides_drawn_pictures() -> None:
    rows = decide_counts([10, 17], invariance=True)
    assert [(row["n"], row["rotate"], row["flip"], row["invariant"]) for row in rows] == [
        (10, 0, False, True),
        (17, 90, True, True),
    ]
    summary = totals(rows)
    assert (summary["identity"], summary["turned"]) == (1, 1)
    assert summary["decided_by"]["quadrants"] == 2
    assert summary["not_invariant"] == []


# --------------------------------------------------------------------------- the record


def test_the_check_names_a_perturbed_row(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Every other row is current, so the perturbed one is the only count named."""
    record = json.loads(RECORD.read_text(encoding="utf-8"))
    eleven = next(row for row in record["entries"] if row["n"] == 11)
    eleven["rotate"] = 90
    stale = tmp_path / "flip-regularization.json"
    stale.write_text(text(record), encoding="utf-8")
    assert check(stale) == 1
    named = [line for line in capsys.readouterr().out.splitlines() if "n=" in line]
    assert len(named) == 1
    assert named[0].startswith("flip regularization: n=11: the record has ")
    assert check(tmp_path / "missing.json") == 1


def test_differences_name_missing_extra_and_doubled_rows() -> None:
    record = json.loads(RECORD.read_text(encoding="utf-8"))
    assert differences(record, record) == []
    changed = json.loads(json.dumps(record))
    entries = changed["entries"]
    entries.remove(next(row for row in entries if row["n"] == 3))
    entries.append({**entries[0]})
    entries.append({**entries[1], "n": 400})
    changed["totals"]["identity"] += 1
    changed["extra"] = True
    assert differences(changed, record) == [
        "n=1: the record has two rows",
        "n=3: the record has no row",
        "n=400: the record has a row for no count",
        "the record's totals is not the rule's",
        "the record has a field 'extra'",
    ]


def test_poses_reads_every_count_and_draws_a_missing_one_unturned(tmp_path: Path) -> None:
    record = json.loads(RECORD.read_text(encoding="utf-8"))
    recorded = poses()
    assert sorted(recorded) == list(range(1, 325))
    assert recorded == {row["n"]: Pose.from_record(row) for row in record["entries"]}
    assert poses(tmp_path / "missing.json") == dict.fromkeys(range(1, 325), IDENTITY)
    turned = next(row for row in record["entries"] if not Pose.from_record(row).identity)
    record["entries"].remove(turned)
    partial = tmp_path / "partial.json"
    partial.write_text(text(record), encoding="utf-8")
    assert poses(partial) == {**recorded, turned["n"]: IDENTITY}
