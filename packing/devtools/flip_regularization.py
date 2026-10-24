#!/usr/bin/env python3
"""Flip regularization: each default picture turned by one of the container's eight symmetries.

Usage, from `packing/`, after
`uv run --frozen --all-extras --group dev python -m devtools.flip_regularization`:

    [--update | --check | --invariance] [--n N ...] [--json]

Packings arrive in whatever pose their source published, so neighbouring atlas tiles
are turned and mirrored against one another. Flip regularization, the last stage of the
regularization process and separate from the others, picks for each count's default
picture the symmetry that draws it in its canonical pose, decided in binary64 from where
its squares lie (regularization policy, section 13). It is display only: the renderers
apply the pose as they draw, and no witness, view or certificate changes. The plan is
`docs/project/specs/active/plan-2026-10-23-flip-regularization.md`.

**Poses.** A `Pose` is the owner's two steps: `rotate` 0, 90, 180 or 270 degrees
counter-clockwise about the container's centre, then, if `flip`, mirror across the
diagonal from the upper-left to the lower-right corner. That mirror fixes the upper-left
and lower-right quadrants and swaps the other two, so the rotation decides which quadrant
is lower right and the flip which of its neighbours is lower left. Each of the eight
symmetries is exactly one pair, and with y up and side `s` the composites are:

    pose        point map         reads as
    (0, F)      (x, y)            unchanged
    (90, F)     (s - y, x)        quarter turn counter-clockwise
    (180, F)    (s - x, s - y)    half turn
    (270, F)    (y, s - x)        quarter turn clockwise
    (0, T)      (s - y, s - x)    mirror across the falling diagonal
    (90, T)     (s - x, y)        mirror left-right
    (180, T)    (y, x)            mirror across the rising diagonal y = x
    (270, T)    (x, s - y)        mirror top-bottom

`POSES` lists them in that order, rotations without a flip first.

**The picture.** A count's default picture is read from its retained rendering: its
regularized view's (`VIEW_RENDERINGS`) where `default_drawings.regularized_defaults`
makes the view the default, as `render_frontier_page.default_root` chooses, else its
house rendering (`RENDERINGS`). The container outline and the squares' fill polygons are
read as `render_frontier_page.packing_svg` reads them, but at full precision, as
binary64, y up from the outline's lower-left corner and scaled to a unit square's side
(`rendering_squares`). No frame is built: `--check` decides all 324 counts in about
1.4 seconds of wall, serially, a quarter of it importing `default_drawings`.

**The rule** (`decide`). The owner, 23 October 2026: rotate the heaviest quadrant by
filled area to the lower right, then flip if the upper right outweighs the lower left,
ties broken by some further deterministic rule. The upper left is then forced, and the
upper right takes what is left, so empty space gathers upper right, as the catalogues
draw the integer grids.

1. *Weights.* On an m x m grid over the container, a cell's weight is the area of the
   squares inside it over the cell's area, each square clipped to the cell as a convex
   polygon in binary64. Cells are read in quadtree order (`quadtree_cells`): lower
   right, lower left, upper left, upper right, and within each quadrant its own four in
   that order, recursively. At m = 2 that is the four quadrants.
2. *Filter.* Of the candidate poses, keep at each position in turn those whose image's
   weight there is within `TOLERANCE` of the greatest (`strongest`). At m = 2 this is
   the owner's two steps.
3. *Levels.* The filter runs at m = 2, then 4, 8 and 16 (`LEVELS`) on the survivors.
4. *Final key.* Each survivor's image as its squares, each `(cy, -cx, tilt)` rounded to
   nine places and sorted (the lowest square first, then the rightmost), the least kept.
   The tilt is the square's angle modulo 90 degrees in (-45, 45]; it is in the key
   because two mirror images can share every centre and differ only in its sign. The
   range's two ends are one angle, so a tilt within `TOLERANCE` of either keys as 45.
5. *Same picture.* After each stage the survivors are matched square for square; once
   they all draw the same picture, the packing having that symmetry, the stage that got
   there is `decided_by` and the first survivor in `POSES` order is the pose, so a
   symmetric packing keeps its published pose where it can. Distinct pictures surviving
   the final key raise, rather than a symmetry being assumed.

The command decides every count and prints how many each stage decided and each pose
took; `--n` and `--json` print the decisions. `--update` writes the record, `RECORD`:
for each count the picture drawn, its rendering, the pose, the stage that decided it and
the oriented quadrant weights. `--check`, a records-tier step, decides every count again
and fails, naming each count, where the record differs. `--invariance` also decides each
picture from all eight of its poses and fails unless all eight draw the same
(`invariant`). The renderers read the record through `poses`.
"""

from __future__ import annotations

import argparse
import json
import math
import re
from bisect import bisect_left, bisect_right
from collections import Counter
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from functools import cache
from pathlib import Path
from typing import Any, Protocol, Self

from strif import atomic_output_file

from sqpack import retained_json

ROOT = Path(__file__).resolve().parent.parent
REPO = ROOT.parent
RECORD = ROOT / "atlas/known-best/flip-regularization.json"
RECORD_PATH = RECORD.relative_to(REPO).as_posix()
CONTRACT = "packing.squares:FlipRegularization/v1"
SCHEMA = "flip-regularization.schema.yaml"
GENERATOR = "python -m devtools.flip_regularization"
POLICY_DOCUMENT = "docs/project/policies/regularization-policy.md"
RULE = f"{POLICY_DOCUMENT}#13-flip-regularization"
#: The house renderings and the regularized views' renderings, repository-relative:
#: `render_frontier_page.RENDERINGS` and `REGULARIZED_RENDERINGS`, which this module
#: cannot import, since that one imports it.
RENDERINGS = "packing/atlas/known-best/rendering"
VIEW_RENDERINGS = "packing/atlas/known-best/regularized/rendering"
#: What a count's default picture is: its regularized view, or its house drawing.
VIEW, HOUSE = "view", "house"
COUNTS = range(1, 325)

ROTATIONS = (0, 90, 180, 270)
TOLERANCE = 1e-9
"""Two weights this close are equal, and so are a tilt this close to -45 or 45 degrees
and 45 in the final key."""
LEVELS = (2, 4, 8, 16)
STAGES = ("quadrants", "grid-4", "grid-8", "grid-16", "squares")
"""What decided a pose: the grid at each of `LEVELS`, then the final key."""
KEY_PLACES = 9
"""The final key's rounding, in decimal places."""
MATCH_TOLERANCE = 1e-6
"""Two pictures are the same when their squares pair off within this, centres in the
container's units and tilts in degrees."""
QUADRANTS = ((1, 0), (0, 0), (0, 1), (1, 1))
"""The quadrants in the rule's order, lower right, lower left, upper left, upper right,
each as `(column, row)` of a 2 x 2 grid from the lower left."""


class Coordinate(Protocol):
    """What `Pose.point` needs of a coordinate: subtraction from the side."""

    def __sub__(self, other: Self, /) -> Self: ...


@dataclass(frozen=True)
class Pose:
    """One of the container's eight symmetries, as the owner's two steps."""

    rotate: int
    """0, 90, 180 or 270: degrees counter-clockwise about the container's centre."""
    flip: bool
    """Then mirror across the diagonal from the upper-left to the lower-right corner."""

    def __post_init__(self) -> None:
        if not isinstance(self.rotate, int) or isinstance(self.rotate, bool):
            raise TypeError(f"rotate must be an integer, not {self.rotate!r}")
        if self.rotate not in ROTATIONS:
            raise ValueError(f"rotate must be one of {ROTATIONS}, not {self.rotate!r}")
        if not isinstance(self.flip, bool):
            raise TypeError(f"flip must be a boolean, not {self.flip!r}")

    def point[T: Coordinate](self, x: T, y: T, side: T) -> tuple[T, T]:
        """Where `(x, y)` lands, y up with the origin lower left.

        Only `side - v` and swapping, so it maps ints, floats, `Fraction`s, `Decimal`s
        and number-field elements alike, each in its own arithmetic."""
        match self.rotate:
            case 90:
                x, y = side - y, x
            case 180:
                x, y = side - x, side - y
            case 270:
                x, y = y, side - x
            case _:
                pass
        if self.flip:
            x, y = side - y, side - x
        return x, y

    def inverse(self) -> Pose:
        """The pose that undoes this one: a flipped pose is a reflection, its own
        inverse, and a rotation's is the opposite turn."""
        return self if self.flip else Pose(rotate=(360 - self.rotate) % 360, flip=False)

    def record(self) -> dict[str, Any]:
        return {"rotate": self.rotate, "flip": self.flip}

    @classmethod
    def from_record(cls, record: Mapping[str, Any]) -> Pose:
        """The pose a record states, its fields checked as a new pose's are; other fields,
        such as a `Decision`'s, are ignored."""
        missing = sorted({"rotate", "flip"} - record.keys())
        if missing:
            raise ValueError(f"a pose record needs {', '.join(missing)}")
        return cls(rotate=record["rotate"], flip=record["flip"])

    @property
    def identity(self) -> bool:
        return self.rotate == 0 and not self.flip


POSES = tuple(Pose(rotate=rotate, flip=flip) for flip in (False, True) for rotate in ROTATIONS)
IDENTITY = POSES[0]
DESCRIPTIONS = dict(
    zip(
        POSES,
        (
            "unchanged",
            "quarter turn counter-clockwise",
            "half turn",
            "quarter turn clockwise",
            "mirror across the falling diagonal",
            "mirror left-right",
            "mirror across the rising diagonal",
            "mirror top-bottom",
        ),
        strict=True,
    )
)


@cache
def poses(record: Path = RECORD) -> dict[int, Pose]:
    """Every count's flip regularization (policy section 13): the pose its default
    picture is drawn in, from the record, for each of `COUNTS`. A count the record has no
    row for, or a record that is missing, draws in `IDENTITY`, its source's pose. Nothing
    is decided here, and the record's contract is not held: `--check` holds the record to
    the data."""
    found = dict.fromkeys(COUNTS, IDENTITY)
    if not record.is_file():
        return found
    for row in json.loads(record.read_text(encoding="utf-8")).get("entries") or []:
        n = int(row["n"])
        if n in found:
            found[n] = Pose.from_record(row)
    return found


def orient_polygon[T: Coordinate](
    pose: Pose, corners: Iterable[tuple[T, T]], side: T
) -> list[tuple[T, T]]:
    """Map each corner; when the pose flips, reverse the corner order so the winding is
    kept."""
    mapped = [pose.point(x, y, side) for x, y in corners]
    return mapped[::-1] if pose.flip else mapped


# --------------------------------------------------------------------------- the rule

type Corners = Sequence[tuple[float, float]]
type Placement = tuple[float, float, float]
"""A square as its centre and its tilt: `(cx, cy, degrees in (-45, 45])`."""


def _half_plane(
    polygon: list[tuple[float, float]], axis: int, bound: float, *, below: bool
) -> list[tuple[float, float]]:
    """One Sutherland-Hodgman pass: the part of a convex polygon on one side of an axis
    line, `axis` 0 for x and 1 for y, on or below `bound` when `below`, else on or above.
    """
    kept: list[tuple[float, float]] = []
    if not polygon:
        return kept
    previous = polygon[-1]
    previous_in = previous[axis] <= bound if below else previous[axis] >= bound
    for current in polygon:
        current_in = current[axis] <= bound if below else current[axis] >= bound
        if current_in != previous_in:
            share = (bound - previous[axis]) / (current[axis] - previous[axis])
            other = previous[1 - axis] + share * (current[1 - axis] - previous[1 - axis])
            kept.append((bound, other) if axis == 0 else (other, bound))
        if current_in:
            kept.append(current)
        previous, previous_in = current, current_in
    return kept


def _area(polygon: Sequence[tuple[float, float]]) -> float:
    if len(polygon) < 3:
        return 0.0
    total = 0.0
    previous = polygon[-1]
    for current in polygon:
        total += previous[0] * current[1] - current[0] * previous[1]
        previous = current
    return abs(total) / 2


def _span(edges: Sequence[float], low: float, high: float) -> range:
    """The cells along one axis that `[low, high]` can reach."""
    last = len(edges) - 2
    first = min(last, max(0, bisect_right(edges, low) - 1))
    return range(first, min(last, max(0, bisect_left(edges, high) - 1)) + 1)


@cache
def quadtree_cells(cells: int) -> tuple[tuple[int, int], ...]:
    """The cells of a `cells` x `cells` grid, `cells` a power of two, as `(column, row)`
    from the lower left, in the rule's order: the quadrants in `QUADRANTS` order, and
    within each its own cells in this order. A cell's key is its quadrant at each level,
    coarse to fine, so at m = 4 the lower-right quadrant's four cells come first, its
    lower right first."""
    if cells < 1 or cells & (cells - 1):
        raise ValueError(f"a grid's side must be a power of two, not {cells}")
    if cells == 1:
        return ((0, 0),)
    half = cells // 2
    return tuple(
        (column * half + inner_column, row * half + inner_row)
        for column, row in QUADRANTS
        for inner_column, inner_row in quadtree_cells(half)
    )


def grid_weights(squares: Iterable[Corners], side: float, cells: int) -> tuple[float, ...]:
    """Each cell's filled fraction on a `cells` x `cells` grid, in `quadtree_cells`
    order. A square inside one cell adds its whole area there; any other is clipped only
    against the cells its bounding box reaches, which keeps a 16 x 16 grid cheap."""
    edges = [side * index / cells for index in range(cells + 1)]
    areas = [[0.0] * cells for _column in range(cells)]
    for corners in squares:
        polygon = list(corners)
        xs = [x for x, _y in polygon]
        ys = [y for _x, y in polygon]
        columns, rows = _span(edges, min(xs), max(xs)), _span(edges, min(ys), max(ys))
        if len(columns) == 1 and len(rows) == 1:
            areas[columns[0]][rows[0]] += _area(polygon)
            continue
        for column in columns:
            strip = _half_plane(polygon, 0, edges[column], below=False)
            strip = _half_plane(strip, 0, edges[column + 1], below=True)
            if len(strip) < 3:
                continue
            for row in rows:
                piece = _half_plane(strip, 1, edges[row], below=False)
                piece = _half_plane(piece, 1, edges[row + 1], below=True)
                areas[column][row] += _area(piece)
    cell = side / cells
    return tuple(areas[column][row] / (cell * cell) for column, row in quadtree_cells(cells))


@cache
def _targets(pose: Pose, cells: int) -> tuple[int, ...]:
    """Where each cell, in `quadtree_cells` order, lands under `pose`: its centre mapped
    in whole half-cells, so the permutation is exact."""
    order = quadtree_cells(cells)
    position = {cell: index for index, cell in enumerate(order)}
    targets: list[int] = []
    for column, row in order:
        x, y = pose.point(2 * column + 1, 2 * row + 1, 2 * cells)
        targets.append(position[(x - 1) // 2, (y - 1) // 2])
    return tuple(targets)


def image_weights(weights: Sequence[float], pose: Pose, cells: int) -> tuple[float, ...]:
    """The weights of the picture `pose` draws, from the source picture's own."""
    image = [0.0] * len(weights)
    for weight, target in zip(weights, _targets(pose, cells), strict=True):
        image[target] = weight
    return tuple(image)


def strongest(candidates: list[Pose], weights: Mapping[Pose, Sequence[float]]) -> list[Pose]:
    """The candidates whose weights are lexicographically greatest, within `TOLERANCE`
    position by position: weights that close count as equal."""
    for position in range(len(weights[candidates[0]])):
        if len(candidates) == 1:
            break
        best = max(weights[pose][position] for pose in candidates)
        candidates = [
            pose for pose in candidates if weights[pose][position] >= best - TOLERANCE
        ]
    return candidates


def _tilt(degrees: float) -> float:
    """An angle modulo a quarter turn, in `(-45, 45]`."""
    reduced = degrees % 90.0
    return reduced - 90.0 if reduced > 45.0 else reduced


def placements(squares: Iterable[Corners]) -> list[Placement]:
    """Each square's centre and tilt, the tilt from its first edge."""
    found: list[Placement] = []
    for corners in squares:
        (x0, y0), (x1, y1) = corners[0], corners[1]
        found.append(
            (
                sum(x for x, _y in corners) / len(corners),
                sum(y for _x, y in corners) / len(corners),
                _tilt(math.degrees(math.atan2(y1 - y0, x1 - x0))),
            )
        )
    return found


def oriented_placements(
    source: Iterable[Placement], pose: Pose, side: float
) -> list[Placement]:
    """The placements of the picture `pose` draws. A turn by quarter turns keeps a tilt
    and a mirror negates it, modulo a quarter turn."""
    return [
        (*pose.point(x, y, side), _tilt(-tilt) if pose.flip else tilt) for x, y, tilt in source
    ]


def same_picture(first: Sequence[Placement], second: Sequence[Placement]) -> bool:
    """Whether two pictures pair off square for square, each pair's centres within
    `MATCH_TOLERANCE` and its tilts within it in degrees, modulo 90.

    Paired by position rather than by sorting both lists: a sort by rounded key can order
    two squares of one row differently in two images of one picture, when a centre sits
    within float noise of a rounding boundary. Unit squares that do not overlap have
    centres at least 1 apart, so a pairing within the tolerance is unique."""
    if len(first) != len(second):
        return False
    buckets: dict[tuple[int, int], list[int]] = {}
    for index, (x, y, _angle) in enumerate(second):
        buckets.setdefault((round(x), round(y)), []).append(index)
    paired: set[int] = set()
    for x, y, tilt in first:
        column, row = round(x), round(y)
        match = next(
            (
                index
                for dx in (-1, 0, 1)
                for dy in (-1, 0, 1)
                for index in buckets.get((column + dx, row + dy), ())
                if index not in paired and _paired((x, y, tilt), second[index])
            ),
            None,
        )
        if match is None:
            return False
        paired.add(match)
    return True


def _paired(left: Placement, right: Placement) -> bool:
    turn = abs(left[2] - right[2]) % 90.0
    return (
        math.dist(left[:2], right[:2]) <= MATCH_TOLERANCE
        and min(turn, 90.0 - turn) <= MATCH_TOLERANCE
    )


def _key(image: Iterable[Placement]) -> list[tuple[float, float, float]]:
    return sorted(
        (round(y, KEY_PLACES), round(-x, KEY_PLACES), round(_key_tilt(tilt), KEY_PLACES))
        for x, y, tilt in image
    )


def _key_tilt(tilt: float) -> float:
    """A tilt as the final key reads it: `(-45, 45]` meets itself at its ends, so a tilt
    within `TOLERANCE` of either is 45, wherever float noise put it."""
    return 45.0 if abs(abs(tilt) - 45.0) <= TOLERANCE else tilt


@dataclass(frozen=True)
class Decision:
    """The pose that draws a picture in its canonical pose, and what decided it."""

    pose: Pose
    decided_by: str
    """The first of `STAGES` after which every surviving pose drew the same picture."""
    quadrants: tuple[float, float, float, float]
    """The oriented picture's quadrant weights: lower right, lower left, upper left,
    upper right."""

    def record(self) -> dict[str, Any]:
        """The record's fields for this picture's pose."""
        return {
            **self.pose.record(),
            "decided_by": self.decided_by,
            "quadrants": [round(weight, 6) for weight in self.quadrants],
        }


def decide(squares: Sequence[Sequence[tuple[float, float]]], side: float) -> Decision:
    """The canonical pose of a picture given as each square's corners, in binary64. A
    grid finer than the quadrants is weighed only where poses still tie."""
    source = placements(squares)
    images: dict[Pose, list[Placement]] = {}

    def image(pose: Pose) -> list[Placement]:
        if pose not in images:
            images[pose] = oriented_placements(source, pose, side)
        return images[pose]

    def one_picture(candidates: Sequence[Pose]) -> bool:
        first = image(candidates[0])
        return all(same_picture(first, image(pose)) for pose in candidates[1:])

    candidates = list(POSES)
    quadrants: dict[Pose, tuple[float, ...]] = {}
    for cells, stage in zip(LEVELS, STAGES, strict=False):
        weights = grid_weights(squares, side, cells)
        oriented = {pose: image_weights(weights, pose, cells) for pose in candidates}
        if cells == LEVELS[0]:
            quadrants = oriented
        candidates = strongest(candidates, oriented)
        if one_picture(candidates):
            return _decision(candidates[0], stage, quadrants)
    keys = {pose: _key(image(pose)) for pose in candidates}
    least = min(keys.values())
    candidates = [pose for pose in candidates if keys[pose] == least]
    if one_picture(candidates):
        return _decision(candidates[0], STAGES[-1], quadrants)
    names = ", ".join(f"({pose.rotate}, {pose.flip})" for pose in candidates)
    raise ValueError(f"distinct pictures survive the {STAGES[-1]!r} stage: poses {names}")


def _decision(pose: Pose, stage: str, quadrants: Mapping[Pose, Sequence[float]]) -> Decision:
    lower_right, lower_left, upper_left, upper_right = quadrants[pose]
    return Decision(pose, stage, (lower_right, lower_left, upper_left, upper_right))


def invariant(squares: Sequence[Sequence[tuple[float, float]]], side: float) -> bool:
    """Whether a picture is drawn the same from each of its eight poses, which is what
    makes the pose canonical: each pose's image, decided and oriented, is one picture."""
    drawn: list[list[Placement]] = []
    for pose in POSES:
        image = [orient_polygon(pose, corners, side) for corners in squares]
        chosen = decide(image, side).pose
        drawn.append(placements(orient_polygon(chosen, corners, side) for corners in image))
    return all(same_picture(drawn[0], other) for other in drawn[1:])


# --------------------------------------------------------------------------- the pictures

OUTLINE = re.compile(
    r'<rect data-feature="container-outline" x="([\d.]+)" y="([\d.]+)" '
    r'width="([\d.]+)" height="([\d.]+)"'
)
SQUARE = re.compile(r'<polygon data-feature="square-fill"[^>]*? points="([^"]+)"')


def rendering_squares(text: str) -> tuple[list[list[tuple[float, float]]], float]:
    """A rendering's squares as their corners, and the container's side: binary64, y up
    from the container outline's lower-left corner, in units of a square's side. The
    renderer draws the packing y down, scaled so a unit square's side is its first
    square's first edge."""
    outline = OUTLINE.search(text)
    if outline is None:
        raise ValueError("the rendering has no container outline")
    left, top, width, height = (float(value) for value in outline.groups())
    drawn = [
        [(float(x), float(y)) for x, y in (pair.split(",") for pair in points.split())]
        for points in SQUARE.findall(text)
    ]
    if not drawn:
        raise ValueError("the rendering draws no squares")
    (x0, y0), (x1, y1) = drawn[0][0], drawn[0][1]
    unit = math.hypot(x1 - x0, y1 - y0)
    bottom = top + height
    squares = [
        [((x - left) / unit, (bottom - y) / unit) for x, y in corners] for corners in drawn
    ]
    return squares, width / unit


@dataclass(frozen=True)
class Picture:
    """A count's default picture, as `decide` reads it."""

    n: int
    drawn: str
    """`VIEW` where the count's regularized view is its default picture, else `HOUSE`."""
    rendering: str
    """The retained rendering it is read from, repository-relative."""
    squares: list[list[tuple[float, float]]]
    side: float


def drawn_views() -> frozenset[int]:
    """The counts whose default picture is their regularized view (policy section 12),
    as `render_frontier_page.default_root` reads them."""
    # Imported here: `poses` is what the renderers import this module for, and the
    # drawings record's module brings the measuring code with it.
    from devtools.default_drawings import regularized_defaults  # noqa: PLC0415

    return frozenset(regularized_defaults())


def picture(n: int, views: frozenset[int]) -> Picture:
    """Count `n`'s default picture: its view's rendering where `n` is in `views`, else
    its house rendering."""
    drawn = VIEW if n in views else HOUSE
    rendering = f"{VIEW_RENDERINGS if drawn == VIEW else RENDERINGS}/n-{n:03d}.svg"
    squares, side = rendering_squares((REPO / rendering).read_text(encoding="utf-8"))
    if len(squares) != n:
        raise ValueError(f"{rendering} draws {len(squares)} squares, not {n}")
    return Picture(n, drawn, rendering, squares, side)


def decide_counts(counts: Iterable[int], *, invariance: bool = False) -> list[dict[str, Any]]:
    """One row a count: its default picture, that picture's decision and, when asked,
    whether the picture is `invariant`."""
    views = drawn_views()
    rows: list[dict[str, Any]] = []
    for n in counts:
        drawn = picture(n, views)
        row = {
            "n": n,
            "drawn": drawn.drawn,
            "rendering": drawn.rendering,
            **decide(drawn.squares, drawn.side).record(),
        }
        if invariance:
            row["invariant"] = invariant(drawn.squares, drawn.side)
        rows.append(row)
    return rows


def totals(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    stages = Counter(row["decided_by"] for row in rows)
    taken = Counter(Pose.from_record(row) for row in rows)
    summary: dict[str, Any] = {
        "counts": len(rows),
        "identity": taken[IDENTITY],
        "turned": len(rows) - taken[IDENTITY],
        "decided_by": {stage: stages[stage] for stage in STAGES},
        "poses": [
            {**pose.record(), "reads_as": DESCRIPTIONS[pose], "counts": taken[pose]}
            for pose in POSES
        ],
    }
    if any("invariant" in row for row in rows):
        summary["not_invariant"] = [row["n"] for row in rows if not row["invariant"]]
    return summary


# --------------------------------------------------------------------------- the record


def document(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    """The record of every count's decision."""
    return {
        "softschema": {"contract": CONTRACT, "schema": SCHEMA, "status": "enforced"},
        "contract": CONTRACT,
        "generated_by": f"{GENERATOR} --update",
        "policy_document": POLICY_DOCUMENT,
        "rule": RULE,
        "totals": totals(rows),
        "entries": list(rows),
    }


def text(record: Mapping[str, Any]) -> str:
    return retained_json.dumps(record, ensure_ascii=False) + "\n"


def differences(found: Mapping[str, Any], expected: Mapping[str, Any]) -> list[str]:
    """Where a record differs from the one the rule gives: each count whose row differs,
    is missing or is extra, then each other field that differs."""
    rows: dict[Any, Any] = {}
    problems: list[str] = []
    for row in found.get("entries") or []:
        n = row.get("n") if isinstance(row, Mapping) else None
        if n in rows:
            problems.append(f"n={n}: the record has two rows")
        rows[n] = row
    for row in expected["entries"]:
        held = rows.pop(row["n"], None)
        if held is None:
            problems.append(f"n={row['n']}: the record has no row")
        elif held != row:
            problems.append(
                f"n={row['n']}: the record has {json.dumps(held, separators=(',', ':'))}, "
                f"the rule gives {json.dumps(row, separators=(',', ':'))}"
            )
    problems.extend(f"n={n}: the record has a row for no count" for n in rows)
    problems.extend(
        f"the record's {key} is not the rule's"
        for key in expected
        if key != "entries" and found.get(key) != expected[key]
    )
    problems.extend(f"the record has a field {key!r}" for key in found if key not in expected)
    return problems


def update() -> int:
    expected = document(decide_counts(COUNTS))
    content = text(expected)
    if not RECORD.is_file() or RECORD.read_text(encoding="utf-8") != content:
        with atomic_output_file(RECORD) as temporary:
            temporary.write_text(content, encoding="utf-8")
    poses.cache_clear()
    print(f"flip regularization updated: {_summary(expected['totals'])}")
    return 0


def check(record: Path = RECORD) -> int:
    """Decide every count again and compare the record."""
    if not record.is_file():
        print(f"{RECORD_PATH} is missing; run `{GENERATOR} --update`")
        return 1
    expected = document(decide_counts(COUNTS))
    content = record.read_text(encoding="utf-8")
    problems = differences(json.loads(content), expected)
    if not problems and content != text(expected):
        problems.append(f"the record is not laid out as `{GENERATOR} --update` writes it")
    for problem in problems:
        print(f"flip regularization: {problem}")
    if problems:
        print(f"{RECORD_PATH} is stale; run `{GENERATOR} --update`")
        return 1
    print(f"flip regularization check passed: {_summary(expected['totals'])}")
    return 0


def _summary(summary: Mapping[str, Any]) -> str:
    stages = ", ".join(f"{stage} {count}" for stage, count in summary["decided_by"].items())
    return (
        f"{summary['counts']} counts, {summary['identity']} in their published pose and "
        f"{summary['turned']} turned; decided by {stages}"
    )


# --------------------------------------------------------------------------- command line


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    mode = command.add_mutually_exclusive_group()
    mode.add_argument("--update", action="store_true", help=f"write {RECORD_PATH}")
    mode.add_argument(
        "--check",
        action="store_true",
        help="decide every count again; exit 1, naming each count, where the record differs",
    )
    mode.add_argument(
        "--invariance",
        action="store_true",
        help="also decide each picture from all eight poses; exit 1 unless all draw the same",
    )
    command.add_argument("--n", type=int, nargs="+", help="counts to print (default 1..324)")
    command.add_argument("--json", action="store_true", help="print the decisions as JSON")
    return command


def main(argv: Sequence[str] | None = None) -> int:
    command = parser()
    args = command.parse_args(argv)
    if (args.update or args.check) and (args.n or args.json):
        command.error("--n and --json print decisions; --update and --check take neither")
    if args.update:
        return update()
    if args.check:
        return check()
    unknown = sorted(set(args.n or ()) - set(COUNTS))
    if unknown:
        command.error(f"no default picture for n = {', '.join(map(str, unknown))}")
    rows = decide_counts(args.n or COUNTS, invariance=args.invariance)
    summary = totals(rows)
    failed = 1 if summary.get("not_invariant") else 0
    if args.json:
        decisions = {"generated_by": GENERATOR, "totals": summary, "entries": rows}
        print(json.dumps(decisions, indent=1))
        return failed
    if args.n:
        print(f"{'n':>4} {'drawn':<5} {'rotate':>6} {'flip':>5}  {'decided by':<10}  quadrants")
        for row in rows:
            weights = " ".join(f"{weight:.4f}" for weight in row["quadrants"])
            print(
                f"{row['n']:>4} {row['drawn']:<5} {row['rotate']:>6} "
                f"{'yes' if row['flip'] else 'no':>5}  {row['decided_by']:<10}  {weights}"
            )
        print("  quadrants: lower right, lower left, upper left, upper right\n")
    print(_summary(summary))
    for pose in summary["poses"]:
        flip = "flip" if pose["flip"] else "no flip"
        print(f"  rotate {pose['rotate']:>3}, {flip:<7} ({pose['reads_as']}): {pose['counts']}")
    if "not_invariant" in summary:
        broken = ", ".join(str(n) for n in summary["not_invariant"]) or "none"
        print(f"drawn differently from some pose: {broken}")
    return failed


if __name__ == "__main__":
    raise SystemExit(main())
