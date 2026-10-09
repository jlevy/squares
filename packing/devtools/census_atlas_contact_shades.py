#!/usr/bin/env python3
"""Census why axis-aligned squares in the atlas render lighter than dark green.

A square's hue in the atlas is its angle family, and its shade is how many of its four
sides it shares whole with a wall or a same-angle square: four is the darkest shade. This
tool replicates the shading rule exactly, for every square of every known-best packing
n = 1..324, and for each axis-aligned square that is shaded lighter than four contacts it
asks why, face by face: how far the square could slide in that direction before it meets
something (an exact polygon sweep), and what it meets.

Two renderers draw the atlas, with two different rules, and both are censused:

- `atlas-house` -- the homepage atlas's Grid and Triangle views. Each tile is drawn by
  `devtools.render_frontier_page.packing_svg` from the committed house rendering
  `atlas/known-best/rendering/n-NNN.svg`, copying its fills. Those fills come from
  `sqpack.render.color`: a side counts when one of the square's edges matches a wall or a
  same-orientation square's edge at both endpoints within `2e-6`, orientations agreeing
  within `1e-6` radians, on the full-precision witness. The census reads the shade and hue
  the SVG actually carries and checks its own float replica of that rule against it.
- `workbench-stage` -- the workbench page's catalogue stage (`packages/workbench`), which
  recomputes contacts live in `core/geometry.ts` `contactFacts` with `gap: 0.01` and a
  0.5 degree angle tolerance, on the corpus frames `build_candidate.compact_frame` writes
  (centres rounded to 1e-6, angles to 1e-4 degrees modulo 90). `workbench-studio` is the
  same rule at the animation studio's `gap: 0.004`, kept to show the sensitivity.

Each face with no contact is given the first cause that applies, from its sweep
clearance `c`, the obstacle's `tilt` against the square, and the obstacle's centre offset
`across` the face. The structural causes come first, then the slides, and only a face that
every rule-scale test passes reaches the bands where a tolerance or precision explanation
could apply:

- `hole-or-open` -- `c > 0.5`: an empty region, so the square is short of any neighbour.
- `tilted-neighbour` -- `tilt` exceeds ten times the rule's angle tolerance: a full shared
  side is impossible by the rule's own definition.
- `offset` -- an aligned neighbour with `across > 0.1`: a partial face, a staggered row.
- `slack` -- an aligned full face or a wall at `c` beyond ten times the gap: the square
  could slide that far into contact.
- `misaligned` -- touching or nearly, but `across` is beyond ten times the gap (and at
  most 0.1): the neighbour is there, shifted along the face.
- `angle-near-miss` -- `tilt` within (tolerance, 10 x tolerance].
- `near-miss` -- the rule's own miss, `max(|c|, across)`, within (gap, 10 x gap].
- `rule-boundary` -- that miss is within the gap, yet the rule found no contact (the page's
  centre metric and the polygon disagree at the edge, or the pair's frame is the other
  square's).

A light square is `structural` if any face is one of the first three, `slack` if otherwise
any face needs a slide beyond ten times the rule's tolerance, and `within-band` if every
non-contact face lies within ten times the tolerance. Under the house rule's `2e-6` only a
`within-band` square could plausibly be blamed on inexact arithmetic; under the stage's
`0.01` the band is itself a centimetre of a unit side, far above any arithmetic.

Usage, from `packing/`, each after `uv run --frozen --all-extras --group dev`:
    python -m devtools.census_atlas_contact_shades --update
    python -m devtools.census_atlas_contact_shades --check
    python -m devtools.census_atlas_contact_shades --report
    python -m devtools.census_atlas_contact_shades --witness PATH...
"""

from __future__ import annotations

import argparse
import gzip
import itertools
import json
import math
import re
from collections import Counter, defaultdict
from collections.abc import Iterable, Iterator, Sequence
from dataclasses import dataclass, field
from fractions import Fraction
from functools import cache
from pathlib import Path
from typing import Any, Literal

import mpmath as mp
from strif import atomic_output_file

from sqpack import retained_json
from sqpack.yamlio import load_yaml

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "atlas/known-best/manifest.json"
OUTPUT = ROOT / "campaign/explorations/X049-families-data/contact-shade-census.json"
GENERATOR = "python -m devtools.census_atlas_contact_shades"
CONTRACT = "packing.squares:AtlasContactShadeCensus/v1"

QUARTER = math.pi / 2

HOLE_CLEARANCE = 0.5
"""A face that can slide farther than half a side is short of any neighbour."""
BAND_FACTOR = 10.0
"""The near-miss bands run from a rule's tolerance to this multiple of it."""
SWEEP_OVERLAP_FLOOR = 1e-6
"""An obstacle blocks a face only if it overlaps the face's swept band by more than this
across, so a diagonal neighbour meeting the square corner to corner is not an obstacle."""
STATIC_AXIS = 1e-12
"""A separating axis this close to perpendicular to the motion is treated as static."""
TIE = 1e-9
"""Obstacles reached within this of one another are simultaneous; the widest one wins."""
NAMED_CASES = (102, 103, 106, 206, 268, 269)
DETAILED_RULES = ("atlas-house", "workbench-stage")
"""The rules whose named cases are published square by square; the studio's gap is a
sensitivity check and is published as counts only."""
PRECISION_SCALE = 1e-4
"""A rule whose gap is at most this lists its band faces one by one: only there can the
near-miss band be an arithmetic or precision question. Coarser rules tally them per n."""
SIGNIFICANT = 4
"""Floats are published to this many significant digits, so a last-ulp difference in a
platform's `cos` cannot move a byte of the retained document."""

FACES = ("+x", "-x", "+y", "-y")
EDGE_FACES = ("-y", "+x", "+y", "-x")
"""The face each edge of `Square.corners` lies on, edge `i` running corner `i` to `i + 1`."""
WALL_NAMES = {"-x": "wall-left", "+x": "wall-right", "-y": "wall-bottom", "+y": "wall-top"}
STRUCTURAL = frozenset({"hole-or-open", "tilted-neighbour", "offset"})
SLIDES = frozenset({"slack", "misaligned"})
BANDS = frozenset({"angle-near-miss", "near-miss", "rule-boundary"})
AXIS_EXACT = 1e-6
"""Radians: within this of the axes a square is one the house renderer calls a right angle."""
NEAR_AXIS = 0.5 * math.pi / 180
"""Radians: a square tilted past `AXIS_EXACT` but within this is near-axis, a right angle to
the workbench's half-degree colour tolerance and another angle family to the house."""
STAGGER_ACROSS = 0.1
"""An aligned neighbour offset by more than this across the face is a staggered row."""
DECADES = (2e-6, 2e-5, 1e-4, 1e-3, 1e-2, 1e-1, 0.5)
SPECTRUM = (0.0, *(10.0**-power for power in range(15, 0, -1)), 0.5)
"""The miss spectrum's edges: exactly zero, then every decade from 1e-15 to 0.1, then 0.5."""
ACROSS_EDGES = (2e-5, 1e-4, 1e-3, 1e-2, 0.04, 0.1, 0.25, 0.5, 0.75)
TILT_EDGES = (1e-5, 1e-4, 1e-3, 0.5 * math.pi / 180, 0.1, 0.4, math.pi / 4)
"""Tilt edges in radians; the fourth is the workbench's half degree, so a tilted neighbour
below it is one the stage would call aligned."""

FILL_RE = re.compile(r'<polygon data-feature="square-fill" ([^>]*?)/>')
ATTR_RE = re.compile(r'([\w-]+)="([^"]*)"')


# --------------------------------------------------------------------------- geometry


@dataclass(frozen=True)
class Square:
    """One unit square: its recorded angle, and its frame folded nearest the axes."""

    ident: str
    x: float
    y: float
    angle: float
    """Radians, as recorded (the workbench rule takes `cos` and `sin` of this)."""
    tilt: float
    """The angle folded into [-pi/4, pi/4): the square's frame nearest the axes."""
    ux: float
    uy: float
    corners: tuple[tuple[float, float], ...]

    def axis(self, face: str) -> tuple[float, float]:
        """The outward unit normal of `face` in this square's folded frame."""
        return {
            "+x": (self.ux, self.uy),
            "-x": (-self.ux, -self.uy),
            "+y": (-self.uy, self.ux),
            "-y": (self.uy, -self.ux),
        }[face]

    def face_towards(self, dx: float, dy: float) -> str:
        """The face whose normal is nearest the direction `(dx, dy)`."""
        along = dx * self.ux + dy * self.uy
        across = -dx * self.uy + dy * self.ux
        if abs(along) >= abs(across):
            return "+x" if along > 0 else "-x"
        return "+y" if across > 0 else "-y"


@cache
def project_sin_cos(angle: float) -> tuple[float, float]:
    """Deterministic binary64 projections at the unchanged census thresholds.

    Platform libm differs by an ulp in some rotations. Cancellation near contact
    magnifies it into different sub-picometre diagnostic spectrum bins. Evaluate the
    exact binary64 argument at a fixed precision before its sole float rounding.
    """
    with mp.workdps(80):
        value = mp.mpf(angle)
        return float(mp.cos(value)), float(mp.sin(value))


def _atan2(y: float, x: float) -> float:
    """The same fixed-precision boundary for exact-corner orientation displays."""
    with mp.workdps(80):
        return float(mp.atan2(mp.mpf(y), mp.mpf(x)))


def make_square(ident: str, x: float, y: float, angle: float) -> Square:
    tilt = math.fmod(angle, QUARTER)
    if tilt < 0:
        tilt += QUARTER
    if tilt >= QUARTER / 2:
        tilt -= QUARTER
    cosine, sine = project_sin_cos(tilt)
    corners = tuple(
        (x + cosine * a - sine * b, y + sine * a + cosine * b)
        for a, b in ((-0.5, -0.5), (0.5, -0.5), (0.5, 0.5), (-0.5, 0.5))
    )
    return Square(ident, x, y, angle, tilt, cosine, sine, corners)


def tilt_between(left: Square, right: Square) -> float:
    """The orientation distance of two squares modulo a quarter turn, in radians."""
    difference = abs(left.tilt - right.tilt) % QUARTER
    return min(difference, QUARTER - difference)


@dataclass(frozen=True)
class Packing:
    side: float
    squares: tuple[Square, ...]


class Grid:
    """Square indices bucketed by centre in unit cells."""

    def __init__(self, squares: Sequence[Square]) -> None:
        self.cells: dict[tuple[int, int], list[int]] = defaultdict(list)
        for index, square in enumerate(squares):
            self.cells[math.floor(square.x), math.floor(square.y)].append(index)

    def near(self, x: float, y: float, radius: float) -> list[int]:
        found: list[int] = []
        for cell_x in range(math.floor(x - radius), math.floor(x + radius) + 1):
            for cell_y in range(math.floor(y - radius), math.floor(y + radius) + 1):
                found.extend(self.cells.get((cell_x, cell_y), ()))
        return sorted(found)


PAIR_REACH = 1.6
"""Both rules look no farther than this between centres: the stage's `sqrt(2.5)` is under
it by more than the frame's rounding, and the house's edge match needs a distance of 1."""


def near_pairs(packing: Packing) -> list[tuple[int, int]]:
    """Every index pair `i < j` whose centres lie within `PAIR_REACH`, in index order."""
    grid = Grid(packing.squares)
    pairs: list[tuple[int, int]] = []
    for left, first in enumerate(packing.squares):
        for right in grid.near(first.x, first.y, PAIR_REACH):
            if right > left:
                second = packing.squares[right]
                if math.hypot(second.x - first.x, second.y - first.y) <= PAIR_REACH:
                    pairs.append((left, right))
    return pairs


@dataclass(frozen=True)
class Sweep:
    """How far one face can slide, and what it meets."""

    clearance: float
    obstacle: Literal["wall", "square"]
    obstacle_id: str
    across: float
    """The obstacle's centre offset across the face (zero for a wall)."""
    tilt: float
    """The obstacle's orientation against the square (the square's own tilt for a wall)."""
    obstacle_tilt: float
    """The obstacle's own tilt from the axes, in radians (zero for a wall)."""


def _project(
    points: Iterable[tuple[float, float]], ax: float, ay: float
) -> tuple[float, float]:
    values = [px * ax + py * ay for px, py in points]
    return min(values), max(values)


def sweep_into(mover: Square, face: str, target: Square) -> tuple[float, float] | None:
    """The interval of travel along `face`'s normal over which `mover` overlaps `target`.

    Separating axes for moving convex polygons: on each of the four edge normals the two
    shadows overlap over an interval of travel, and the squares overlap exactly where all
    four intervals do. An axis perpendicular to the motion is static, and there the shadows
    must overlap by more than `SWEEP_OVERLAP_FLOOR` or the target is never reached.
    """
    dx, dy = mover.axis(face)
    entry, exit_ = -math.inf, math.inf
    axes = (
        (mover.ux, mover.uy),
        (-mover.uy, mover.ux),
        (target.ux, target.uy),
        (-target.uy, target.ux),
    )
    for ax, ay in axes:
        p0, p1 = _project(mover.corners, ax, ay)
        q0, q1 = _project(target.corners, ax, ay)
        rate = dx * ax + dy * ay
        if abs(rate) < STATIC_AXIS:
            if min(p1, q1) - max(p0, q0) <= SWEEP_OVERLAP_FLOOR:
                return None
            continue
        start, stop = (q0 - p1) / rate, (q1 - p0) / rate
        if start > stop:
            start, stop = stop, start
        entry, exit_ = max(entry, start), min(exit_, stop)
    if entry > exit_:
        return None
    return entry, exit_


def wall_clearance(square: Square, face: str, side: float) -> float:
    """Travel along `face`'s normal until the square's farthest corner meets the faced wall."""
    dx, dy = square.axis(face)
    if abs(dx) >= abs(dy):
        if dx > 0:
            return (side - max(x for x, _ in square.corners)) / dx
        return min(x for x, _ in square.corners) / -dx
    if dy > 0:
        return (side - max(y for _, y in square.corners)) / dy
    return min(y for _, y in square.corners) / -dy


def sweep_face(packing: Packing, grid: Grid, index: int, face: str) -> Sweep:
    """The first obstacle a square meets sliding out through `face`, wall or square."""
    square = packing.squares[index]
    dx, dy = square.axis(face)
    wx, wy = -dy, dx
    reach = 2.5
    best: tuple[float, float, int] | None = None
    candidates = grid.near(square.x, square.y, reach)
    for attempt in range(2):
        for other in candidates:
            if other == index:
                continue
            target = packing.squares[other]
            rx, ry = target.x - square.x, target.y - square.y
            if rx * dx + ry * dy < -0.75 or abs(rx * wx + ry * wy) > 1.2072:
                continue
            interval = sweep_into(square, face, target)
            if interval is None or interval[1] <= STATIC_AXIS:
                continue
            p0, p1 = _project(square.corners, wx, wy)
            q0, q1 = _project(target.corners, wx, wy)
            overlap = min(p1, q1) - max(p0, q0)
            key = (interval[0], -overlap, other)
            if (
                best is None
                or key[0] < best[0] - TIE
                or (abs(key[0] - best[0]) <= TIE and key[1:] < best[1:])
            ):
                best = key
        # A face whose nearest obstacle may lie past the bucketed reach scans everything.
        if attempt == 0 and (best is None or best[0] > reach - 1.5):
            candidates = list(range(len(packing.squares)))
            continue
        break
    wall = wall_clearance(square, face, packing.side)
    if best is None or wall < best[0] - TIE:
        return Sweep(wall, "wall", WALL_NAMES[face], 0.0, abs(square.tilt), 0.0)
    target = packing.squares[best[2]]
    rx, ry = target.x - square.x, target.y - square.y
    return Sweep(
        best[0],
        "square",
        target.ident,
        abs(rx * wx + ry * wy),
        tilt_between(square, target),
        abs(target.tilt),
    )


# --------------------------------------------------------------------------- the two rules


@dataclass(frozen=True)
class Rule:
    name: str
    metric: Literal["edge", "centre"]
    gap: float
    angle_tolerance: float
    """Radians."""
    poses: Literal["witness", "frame"]
    governs: str


RULES = (
    Rule(
        "atlas-house",
        "edge",
        2e-6,
        1e-6,
        "witness",
        "the homepage atlas Grid and Triangle views: devtools/overview_sections.py "
        "atlas_grid -> render_frontier_page.packing_svg copies the fills of "
        "atlas/known-best/rendering/n-NNN.svg, shaded by sqpack.render.color "
        "(full_side_contact_tolerance 2e-6, angle_tolerance_radians 1e-6)",
    ),
    Rule(
        "workbench-stage",
        "centre",
        0.01,
        0.5 * math.pi / 180,
        "frame",
        "the workbench catalogue stage: packages/workbench/src/application.js "
        "CONTACT = { gap: 0.01 } into core/geometry.ts contactFacts, angle tolerance "
        "COLOUR_ANGLE_TOLERANCE_DEGREES = 0.5 from build_candidate.py",
    ),
    Rule(
        "workbench-studio",
        "centre",
        0.004,
        0.5 * math.pi / 180,
        "frame",
        "sensitivity only: the animation studio's gap (view/animation-scene.ts "
        "gap: 0.004), applied to the same corpus frames",
    ),
)


@dataclass(frozen=True)
class Contact:
    face: str
    other: str
    residual: float


def edge_rule_contacts(
    packing: Packing, rule: Rule, pairs: Sequence[tuple[int, int]] | None = None
) -> list[list[Contact]]:
    """`sqpack.render.color._full_side_contacts`, in floats: per edge, its best match.

    An axis-aligned square's edge meets a wall when both its endpoints lie within the
    gap of that wall's line; two squares of one orientation share a side when an edge of
    each coincides at both endpoints within the gap, coordinate by coordinate. Each edge
    keeps only its least-residual match, so a square has at most four.
    """
    squares = packing.squares
    side = packing.side
    candidates: list[list[list[Contact]]] = [[[] for _ in range(4)] for _ in squares]
    for index, square in enumerate(squares):
        if abs(square.tilt) > rule.angle_tolerance:
            continue
        for edge in range(4):
            a, b = square.corners[edge], square.corners[(edge + 1) % 4]
            for face, axis, boundary in (
                ("-x", 0, 0.0),
                ("+x", 0, side),
                ("-y", 1, 0.0),
                ("+y", 1, side),
            ):
                residual = max(abs(a[axis] - boundary), abs(b[axis] - boundary))
                if residual <= rule.gap:
                    candidates[index][edge].append(
                        Contact(EDGE_FACES[edge], WALL_NAMES[face], residual)
                    )
    for left, right in near_pairs(packing) if pairs is None else pairs:
        first, second = squares[left], squares[right]
        distance = math.hypot(second.x - first.x, second.y - first.y)
        # Edges matching at both ends within the gap put the centres one side apart.
        if abs(distance - 1) > 1e-4 or tilt_between(first, second) > rule.angle_tolerance:
            continue
        for left_edge in range(4):
            a0, a1 = first.corners[left_edge], first.corners[(left_edge + 1) % 4]
            for right_edge in range(4):
                b0, b1 = second.corners[right_edge], second.corners[(right_edge + 1) % 4]
                direct = max(
                    abs(a0[0] - b0[0]),
                    abs(a0[1] - b0[1]),
                    abs(a1[0] - b1[0]),
                    abs(a1[1] - b1[1]),
                )
                reverse = max(
                    abs(a0[0] - b1[0]),
                    abs(a0[1] - b1[1]),
                    abs(a1[0] - b0[0]),
                    abs(a1[1] - b0[1]),
                )
                residual = min(direct, reverse)
                if residual > rule.gap:
                    continue
                candidates[left][left_edge].append(
                    Contact(EDGE_FACES[left_edge], second.ident, residual)
                )
                candidates[right][right_edge].append(
                    Contact(EDGE_FACES[right_edge], first.ident, residual)
                )
    return [
        [
            min(edge, key=lambda contact: (contact.residual, contact.other))
            for edge in edges
            if edge
        ]
        for edges in candidates
    ]


def _js_fold(angle: float) -> float:
    """`foldAngle` in `core/geometry.ts`: JavaScript's `%` is C's `fmod`."""
    return math.fmod(math.fmod(angle, QUARTER) + QUARTER, QUARTER)


def _js_angle_gap(left: float, right: float) -> float:
    distance = math.fmod(abs(left - right), QUARTER)
    return min(distance, QUARTER - distance)


def centre_rule_contacts(
    packing: Packing, rule: Rule, pairs: Sequence[tuple[int, int]] | None = None
) -> list[list[Contact]]:
    """`contactFacts` in `core/geometry.ts`, line for line, keeping every contact found.

    The count the page shades by is `min(4, len(contacts))`. Walls count only for a
    square within the angle tolerance of the axes, by its centre's distance from half a
    side in from the wall; a pair counts when both fold to one angle within tolerance,
    the centres are within `sqrt(2.5)`, and in the lower-indexed square's recorded frame
    `| |along| - 1 |` and `|across|` (or the two swapped) are both within the gap.
    `nearbyPairs` buckets the same pairs differently, but it visits each once, lower index
    first, and the cap at four commutes with the order the increments arrive in.
    """
    squares = packing.squares
    side = packing.side
    found: list[list[Contact]] = [[] for _ in squares]
    for index, square in enumerate(squares):
        if _js_angle_gap(_js_fold(square.angle), 0) > rule.angle_tolerance:
            continue
        for face, offset in (
            ("-x", square.x - 0.5),
            ("+x", square.x - (side - 0.5)),
            ("-y", square.y - 0.5),
            ("+y", square.y - (side - 0.5)),
        ):
            if abs(offset) <= rule.gap:
                found[index].append(Contact(face, WALL_NAMES[face], abs(offset)))
    for left, right in near_pairs(packing) if pairs is None else pairs:
        first, second = squares[left], squares[right]
        dx, dy = second.x - first.x, second.y - first.y
        if dx * dx + dy * dy > 2.5:
            continue
        if _js_angle_gap(_js_fold(first.angle), _js_fold(second.angle)) > rule.angle_tolerance:
            continue
        cosine, sine = project_sin_cos(first.angle)
        along = dx * cosine + dy * sine
        across = -dx * sine + dy * cosine
        if abs(abs(along) - 1) <= rule.gap and abs(across) <= rule.gap:
            residual = max(abs(abs(along) - 1), abs(across))
        elif abs(abs(across) - 1) <= rule.gap and abs(along) <= rule.gap:
            residual = max(abs(abs(across) - 1), abs(along))
        else:
            continue
        found[left].append(Contact(first.face_towards(dx, dy), second.ident, residual))
        found[right].append(Contact(second.face_towards(-dx, -dy), first.ident, residual))
    return found


def atlas_slots(angles_degrees: Sequence[float], tolerance_degrees: float) -> list[int]:
    """`buildAtlasMap(...).slotOf` in `view/colour.ts`: 0 is the right-angle (green) family.

    Only the two pinned slots are told apart; every free family reads as 2.
    """

    def fold(angle: float) -> float:
        return math.fmod(math.fmod(angle, 90.0) + 90.0, 90.0)

    def gap(left: float, right: float) -> float:
        distance = abs(fold(left) - fold(right))
        return min(distance, 90.0 - distance)

    def pinned(angle: float) -> int:
        if gap(angle, 0) <= tolerance_degrees:
            return 0
        if gap(angle, 45) <= tolerance_degrees:
            return 1
        return 2

    representatives: list[float] = []
    sums: list[float] = []
    counts: list[int] = []
    for raw in angles_degrees:
        angle = fold(raw)
        match = next(
            (
                i
                for i, rep in enumerate(representatives)
                if gap(angle, rep) <= tolerance_degrees
            ),
            -1,
        )
        if match < 0:
            representatives.append(angle)
            sums.append(0.0)
            counts.append(1)
            continue
        difference = angle - representatives[match]
        if difference > 45:
            difference -= 90
        elif difference < -45:
            difference += 90
        sums[match] += difference
        counts[match] += 1
    centres = [
        fold(rep + total / count)
        for rep, total, count in zip(representatives, sums, counts, strict=True)
    ]
    slots = [pinned(centre) for centre in centres]
    result: list[int] = []
    for raw in angles_degrees:
        angle = fold(raw)
        match = next(
            (i for i, c in enumerate(centres) if gap(angle, c) <= tolerance_degrees), -1
        )
        result.append(slots[match] if match >= 0 else pinned(angle))
    return result


# --------------------------------------------------------------------------- inputs


@dataclass(frozen=True)
class Case:
    n: int
    entry: dict[str, Any]
    witness: Packing
    frame: Packing
    frame_degrees: tuple[float, ...]
    rendering: tuple[dict[str, str], ...]


def _number(value: str) -> float:
    """A witness scalar as the nearest float: a decimal directly (`float` rounds a decimal
    string correctly, exactly as `float(Fraction(value))` does), a ratio through `Fraction`."""
    try:
        return float(value)
    except ValueError:
        return float(Fraction(value))


def _radians(value: str, unit: str) -> float:
    angle = _number(value)
    if unit == "radians":
        return angle
    if unit == "degrees":
        return math.radians(angle)
    raise ValueError(f"center-angle witness declares angle_unit {unit!r}")


def _frame_degrees(value: str, unit: str) -> float:
    """`build_candidate._angle_degrees`, which the corpus frame is written from."""
    angle = _number(value)
    if unit == "degrees":
        return angle
    if unit == "radians":
        return math.degrees(angle)
    raise ValueError(f"center-angle witness declares angle_unit {unit!r}")


def packings_from_witness(
    witness: dict[str, Any],
) -> tuple[Packing, Packing, tuple[float, ...]]:
    """A Witness/v2 body at full precision, the page's rounded frame of it, and the frame's
    angles in degrees.

    The frame is `build_candidate.load_witness` then `compact_frame`: centres rounded to
    six decimals, the angle in degrees modulo 90 rounded to four, the side to nine.
    """
    representation = witness["representation"]
    unit = witness["coordinates"]["angle_unit"]
    side = _number(witness["side"])
    exact: list[Square] = []
    framed: list[Square] = []
    degrees: list[float] = []
    for row in witness["squares"]:
        ident = str(row["id"])
        if representation == "center-angle":
            x, y = (_number(value) for value in row["center"])
            angle = _radians(row["angle"], unit)
            frame_angle = _frame_degrees(row["angle"], unit) % 90.0
        else:
            corners = [(Fraction(cx), Fraction(cy)) for cx, cy in row["corners"]]
            x = float(sum(cx for cx, _ in corners) / 4)
            y = float(sum(cy for _, cy in corners) / 4)
            (x0, y0), (x1, y1) = corners[0], corners[1]
            angle = _atan2(float(y1 - y0), float(x1 - x0))
            frame_angle = math.degrees(angle) % 90.0
        exact.append(make_square(ident, x, y, angle))
        rounded = round(frame_angle, 4)
        degrees.append(rounded)
        framed.append(make_square(ident, round(x, 6), round(y, 6), rounded * math.pi / 180))
    return (
        Packing(side, tuple(exact)),
        Packing(round(side, 9), tuple(framed)),
        tuple(degrees),
    )


def parse_rendering(text: str, n: int) -> tuple[dict[str, str], ...]:
    """Each square's fill attributes from a house rendering, in witness order."""
    rows = {
        attrs["data-square"]: attrs
        for attrs in (dict(ATTR_RE.findall(match.group(1))) for match in FILL_RE.finditer(text))
    }
    if len(rows) != n:
        raise ValueError(f"n={n}: the rendering draws {len(rows)} squares")
    return tuple(rows[f"square-{index + 1:03d}"] for index in range(n))


def load_case(entry: dict[str, Any]) -> Case:
    """One manifest entry's witness, frame and committed rendering."""
    n = entry["n"]
    data = load_yaml((ROOT / entry["witness"]["path"]).read_text(encoding="utf-8"))
    witness, frame, degrees = packings_from_witness(data["witness"])
    if len(witness.squares) != n:
        raise ValueError(f"n={n}: the witness carries {len(witness.squares)} squares")
    text = (ROOT / entry["rendering"]["path"]).read_text(encoding="utf-8")
    return Case(n, entry, witness, frame, degrees, parse_rendering(text, n))


# --------------------------------------------------------------------------- the census


def sig(value: float) -> float:
    """`value` to `SIGNIFICANT` significant digits, for a byte-stable document."""
    if value == 0 or not math.isfinite(value):
        return 0.0 if value == 0 else value
    return float(f"{value:.{SIGNIFICANT - 1}e}")


def classify(sweep: Sweep, rule: Rule) -> str:
    """The first cause in the module's order that explains a face without a contact."""
    tests = (
        ("hole-or-open", sweep.clearance > HOLE_CLEARANCE),
        ("tilted-neighbour", sweep.tilt > BAND_FACTOR * rule.angle_tolerance),
        ("offset", sweep.across > STAGGER_ACROSS),
        ("slack", abs(sweep.clearance) > BAND_FACTOR * rule.gap),
        ("misaligned", sweep.across > BAND_FACTOR * rule.gap),
        ("angle-near-miss", sweep.tilt > rule.angle_tolerance),
        ("near-miss", slide(sweep) > rule.gap),
    )
    return next((cause for cause, holds in tests if holds), "rule-boundary")


def square_kind(causes: Iterable[str]) -> str:
    present = set(causes)
    if present & STRUCTURAL:
        return "structural"
    if present & SLIDES:
        return "slack"
    return "within-band"


@dataclass
class RuleResult:
    """One rule over one packing: who renders green, who renders light, and why."""

    contacts: list[list[Contact]]
    counts: list[int]
    green: list[bool]
    shades: list[int]
    faces: dict[int, dict[str, tuple[str, Sweep]]] = field(default_factory=dict)


@dataclass
class Scratch:
    """What the rules over one case share: its buckets, its near pairs, and the sweeps
    already run, since a face's sweep is geometry and only its classification is a rule's."""

    grid: Grid
    pairs: list[tuple[int, int]]
    sweeps: dict[tuple[int, str], Sweep] = field(default_factory=dict)

    @classmethod
    def of(cls, case: Case) -> Scratch:
        return cls(Grid(case.witness.squares), near_pairs(case.witness))


def apply_rule(case: Case, rule: Rule, scratch: Scratch) -> RuleResult:
    pairs = scratch.pairs
    if rule.metric == "edge":
        contacts = edge_rule_contacts(case.witness, rule, pairs)
        green = [row["data-hue-index"] == "0" for row in case.rendering]
        shades = [int(row["data-shade-index"]) for row in case.rendering]
    else:
        contacts = centre_rule_contacts(case.frame, rule, pairs)
        tolerance_degrees = rule.angle_tolerance * 180 / math.pi
        green = [slot == 0 for slot in atlas_slots(case.frame_degrees, tolerance_degrees)]
        shades = [4 - min(4, len(found)) for found in contacts]
    counts = [min(4, len(found)) for found in contacts]
    result = RuleResult(contacts, counts, green, shades)
    for index, square_contacts in enumerate(contacts):
        if not green[index] or shades[index] == 0:
            continue
        touched = {contact.face for contact in square_contacts}
        diagnosed: dict[str, tuple[str, Sweep]] = {}
        for face in FACES:
            if face in touched:
                continue
            key = (index, face)
            if key not in scratch.sweeps:
                scratch.sweeps[key] = sweep_face(case.witness, scratch.grid, index, face)
            diagnosed[face] = (classify(scratch.sweeps[key], rule), scratch.sweeps[key])
        result.faces[index] = diagnosed
    return result


def distribution(values: Sequence[float]) -> dict[str, Any]:
    ordered = sorted(values)
    count = len(ordered)

    def rank(q: float) -> float | None:
        return sig(ordered[max(0, math.ceil(q * count) - 1)]) if count else None

    return {
        "count": count,
        "max": rank(1.0),
        "p99": rank(0.99),
        "p50": rank(0.5),
        "above_1e-12": sum(value > 1e-12 for value in ordered),
        "above_1e-9": sum(value > 1e-9 for value in ordered),
        "above_1e-6": sum(value > 1e-6 for value in ordered),
        "above_1e-3": sum(value > 1e-3 for value in ordered),
    }


def decades(values: Iterable[float], edges: Sequence[float] = DECADES) -> list[list[Any]]:
    """How many values fall in each band `(previous edge, edge]` of `edges`, as ordered
    `[label, count]` rows (a list, so sorted keys cannot reorder the bands)."""
    bins: Counter[str] = Counter()
    for value in values:
        label = next((f"<={edge:g}" for edge in edges if value <= edge), f">{edges[-1]:g}")
        bins[label] += 1
    order = [f"<={edge:g}" for edge in edges] + [f">{edges[-1]:g}"]
    return [[label, bins[label]] for label in order if bins[label]]


def face_record(cause: str, sweep: Sweep) -> dict[str, Any]:
    return {
        "cause": cause,
        "clearance": sig(sweep.clearance),
        "obstacle": sweep.obstacle,
        "obstacle_id": sweep.obstacle_id,
        "across": sig(sweep.across),
        "tilt_radians": sig(sweep.tilt),
    }


def square_record(case: Case, result: RuleResult, index: int) -> dict[str, Any]:
    square = case.witness.squares[index]
    faces = result.faces[index]
    return {
        "id": square.ident,
        "centre": [sig(square.x), sig(square.y)],
        "contacts": result.counts[index],
        "contact_faces": sorted(contact.face for contact in result.contacts[index]),
        "shade": result.shades[index],
        "kind": square_kind(cause for cause, _ in faces.values()),
        "faces": {face: face_record(*faces[face]) for face in sorted(faces)},
    }


def slide(sweep: Sweep) -> float:
    """How far a face is from a full shared side: its gap or its offset, whichever is more."""
    return max(abs(sweep.clearance), sweep.across)


def witness_class(entry: dict[str, Any]) -> str:
    witness = entry["witness"]
    tolerance = witness.get("tolerance") or "exact"
    return f"{witness['method']}/{witness['coordinate_provenance']}/{tolerance}"


def is_near_axis(tilt: float) -> bool:
    return AXIS_EXACT < abs(tilt) <= NEAR_AXIS


def near_axis_face(sweep: Sweep, square: Square) -> bool:
    """A face of a near-axis square, or one whose obstacle is a near-axis square."""
    return is_near_axis(square.tilt) or (
        sweep.obstacle == "square" and is_near_axis(sweep.obstacle_tilt)
    )


def tilt_explains(sweep: Sweep, square: Square, rule: Rule) -> bool:
    """Whether a near-axis tilt is all that keeps a face from being a contact: the face
    touches within the gap and its obstacle is aligned across it within the gap, so only
    the turn is left (for the stage, only its centre metric or the tilted square's frame)."""
    return near_axis_face(sweep, square) and slide(sweep) <= rule.gap


def near_axis_tally(case: Case, result: RuleResult, rule: Rule) -> dict[str, int]:
    """Near-axis squares in one record, and how far their tilt explains its light shades."""
    squares = case.witness.squares
    tally = {
        "squares": sum(is_near_axis(square.tilt) for square in squares),
        "green": sum(
            is_near_axis(square.tilt) and green
            for square, green in zip(squares, result.green, strict=True)
        ),
        "light": 0,
        "light_facing": 0,
        "light_only_facing": 0,
        "light_tilt_alone": 0,
        "faces_facing": 0,
        "faces_tilt_alone": 0,
    }
    for index, faces in result.faces.items():
        square = squares[index]
        facing = [near_axis_face(sweep, square) for _, sweep in faces.values()]
        explained = [tilt_explains(sweep, square, rule) for _, sweep in faces.values()]
        tally["light"] += is_near_axis(square.tilt)
        tally["light_facing"] += any(facing)
        tally["light_only_facing"] += all(facing)
        tally["light_tilt_alone"] += all(explained)
        tally["faces_facing"] += sum(facing)
        tally["faces_tilt_alone"] += sum(explained)
    return tally


def entry_row(case: Case, result: RuleResult, rule: Rule) -> dict[str, Any]:
    causes: Counter[str] = Counter()
    kinds: Counter[str] = Counter()
    slides: list[float] = []
    for faces in result.faces.values():
        causes.update(cause for cause, _ in faces.values())
        kind = square_kind(cause for cause, _ in faces.values())
        kinds[kind] += 1
        if kind != "structural":
            slides.append(max(slide(sweep) for _, sweep in faces.values()))
    return {
        "n": case.n,
        "source_kind": case.entry["source"]["kind"],
        "witness_class": witness_class(case.entry),
        "green": sum(result.green),
        "light": len(result.faces),
        "faces": dict(sorted(causes.items())),
        "squares": dict(sorted(kinds.items())),
        "max_regularizable_slide": sig(max(slides)) if slides else None,
        "near_axis": near_axis_tally(case, result, rule),
    }


def totals(rows: Sequence[dict[str, Any]]) -> dict[str, Any]:
    """A group of entry rows summed: the summary is rebuilt from the rows alone."""
    faces: Counter[str] = Counter()
    kinds: Counter[str] = Counter()
    near: Counter[str] = Counter()
    for row in rows:
        faces.update(row["faces"])
        kinds.update(row["squares"])
        near.update(row["near_axis"])
    return {
        "records": len(rows),
        "records_with_light": sum(row["light"] > 0 for row in rows),
        "green": sum(row["green"] for row in rows),
        "light": sum(row["light"] for row in rows),
        "faces": dict(sorted(faces.items())),
        "squares": dict(sorted(kinds.items())),
        "near_axis": dict(sorted(near.items())),
        "records_with_near_axis_squares": sum(row["near_axis"]["squares"] > 0 for row in rows),
    }


def vacancy_family(case: Case, results: dict[str, RuleResult]) -> dict[str, Any] | None:
    """n = k^2 - 1 or k^2 - 2 on the k x k grid: are the vacancy's neighbours light?"""
    k = math.isqrt(case.n) + 1
    if case.n not in {k * k - 1, k * k - 2} or abs(case.witness.side - k) > 1e-12:
        return None
    cells: dict[tuple[int, int], int] = {}
    for index, square in enumerate(case.witness.squares):
        cell = (round(square.x - 0.5), round(square.y - 0.5))
        if (
            square.tilt != 0
            or abs(square.x - 0.5 - cell[0]) > 1e-12
            or abs(square.y - 0.5 - cell[1]) > 1e-12
        ):
            return None
        cells[cell] = index
    vacancies = sorted({(i, j) for i in range(k) for j in range(k)} - set(cells))
    neighbours = sorted(
        {
            cells[(i + di, j + dj)]
            for i, j in vacancies
            for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1))
            if (i + di, j + dj) in cells
        }
    )
    row: dict[str, Any] = {
        "n": case.n,
        "k": k,
        "vacancies": [list(cell) for cell in vacancies],
        "vacancy_neighbours": len(neighbours),
    }
    for name, result in results.items():
        light = [
            index for index in range(case.n) if result.green[index] and result.shades[index] > 0
        ]
        row[name] = {
            "light": len(light),
            "light_neighbours": sum(index in neighbours for index in light),
            "light_elsewhere": sum(index not in neighbours for index in light),
            "neighbour_contacts": dict(
                sorted(Counter(str(result.counts[i]) for i in neighbours).items())
            ),
            "neighbour_faces": dict(
                sorted(
                    Counter(
                        cause
                        for i in neighbours
                        for cause, _ in result.faces.get(i, {}).values()
                    ).items()
                )
            ),
        }
    return row


@dataclass
class Collector:
    """What the census accumulates across the corpus, rule by rule."""

    rows: dict[str, list[dict[str, Any]]] = field(default_factory=lambda: defaultdict(list))
    contact_residuals: dict[str, list[float]] = field(default_factory=lambda: defaultdict(list))
    green_residuals: dict[str, list[float]] = field(default_factory=lambda: defaultdict(list))
    class_residuals: dict[str, dict[str, list[float]]] = field(
        default_factory=lambda: defaultdict(lambda: defaultdict(list))
    )
    class_misses: dict[str, dict[str, list[float]]] = field(
        default_factory=lambda: defaultdict(lambda: defaultdict(list))
    )
    clearances: dict[str, dict[str, list[float]]] = field(
        default_factory=lambda: defaultdict(lambda: defaultdict(list))
    )
    obstacles: dict[str, Counter[str]] = field(default_factory=lambda: defaultdict(Counter))
    across: dict[str, dict[str, list[float]]] = field(
        default_factory=lambda: defaultdict(lambda: defaultdict(list))
    )
    tilts: dict[str, dict[str, list[float]]] = field(
        default_factory=lambda: defaultdict(lambda: defaultdict(list))
    )
    band_faces: dict[str, list[dict[str, Any]]] = field(
        default_factory=lambda: defaultdict(list)
    )
    regularizable: dict[str, list[dict[str, Any]]] = field(
        default_factory=lambda: defaultdict(list)
    )
    named: dict[str, dict[str, Any]] = field(default_factory=dict)
    vacancy: list[dict[str, Any]] = field(default_factory=list)
    replica: Counter[str] = field(default_factory=Counter)
    replica_mismatches: list[dict[str, Any]] = field(default_factory=list)


def census_case(case: Case, collector: Collector) -> None:
    scratch = Scratch.of(case)
    results = {rule.name: apply_rule(case, rule, scratch) for rule in RULES}
    house = results["atlas-house"]
    for index, row in enumerate(case.rendering):
        drawn = int(row["data-contact-sides"])
        if drawn == house.counts[index]:
            collector.replica["agree"] += 1
        else:
            collector.replica["disagree"] += 1
            collector.replica_mismatches.append(
                {
                    "n": case.n,
                    "id": case.witness.squares[index].ident,
                    "replica": house.counts[index],
                    "rendering": drawn,
                }
            )
    for rule in RULES:
        result = results[rule.name]
        collector.rows[rule.name].append(entry_row(case, result, rule))
        for index, found in enumerate(result.contacts):
            residuals = [contact.residual for contact in found]
            collector.contact_residuals[rule.name].extend(residuals)
            collector.class_residuals[rule.name][witness_class(case.entry)].extend(residuals)
            if result.green[index]:
                collector.green_residuals[rule.name].extend(residuals)
        regular: list[list[Any]] = []
        for index, faces in result.faces.items():
            for face, (cause, sweep) in faces.items():
                collector.clearances[rule.name][cause].append(sweep.clearance)
                collector.obstacles[rule.name][f"{cause} / {sweep.obstacle}"] += 1
                if cause not in STRUCTURAL:
                    collector.class_misses[rule.name][witness_class(case.entry)].append(
                        slide(sweep)
                    )
                if cause in {"offset", "misaligned"}:
                    collector.across[rule.name][cause].append(sweep.across)
                if cause in {"tilted-neighbour", "angle-near-miss"}:
                    collector.tilts[rule.name][cause].append(sweep.tilt)
                if cause in BANDS:
                    collector.band_faces[rule.name].append(
                        {"n": case.n, "id": case.witness.squares[index].ident, "face": face}
                        | face_record(cause, sweep)
                    )
            kind = square_kind(cause for cause, _ in faces.values())
            if kind != "structural":
                regular.append(
                    [
                        case.witness.squares[index].ident,
                        kind,
                        sig(max(abs(sweep.clearance) for _, sweep in faces.values())),
                        sig(max(sweep.across for _, sweep in faces.values())),
                    ]
                )
        if regular:
            collector.regularizable[rule.name].append(
                {
                    "n": case.n,
                    "squares": regular,
                    "max_slide": max(max(row[2], row[3]) for row in regular),
                    "within_band_only": all(row[1] == "within-band" for row in regular),
                }
            )
    if case.n in NAMED_CASES:
        collector.named[str(case.n)] = {
            "source_kind": case.entry["source"]["kind"],
            "witness_class": witness_class(case.entry),
        } | {
            name: [
                square_record(case, results[name], index)
                for index in sorted(results[name].faces)
            ]
            for name in DETAILED_RULES
        }
    family = vacancy_family(case, results)
    if family is not None:
        collector.vacancy.append(family)


def manifest_entries() -> list[dict[str, Any]]:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))["atlas"]["entries"]


def rule_summary(rule: Rule, collector: Collector) -> dict[str, Any]:
    rows = collector.rows[rule.name]
    by_source: dict[str, list[dict[str, Any]]] = defaultdict(list)
    by_class: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_source[row["source_kind"]].append(row)
        by_class[row["witness_class"]].append(row)
    regular = collector.regularizable[rule.name]
    return {
        "rule": {
            "metric": rule.metric,
            "gap": rule.gap,
            "angle_tolerance_radians": sig(rule.angle_tolerance),
            "poses": rule.poses,
            "governs": rule.governs,
        },
        "totals": totals(rows),
        "by_source_kind": {kind: totals(group) for kind, group in sorted(by_source.items())},
        "by_witness_class": {kind: totals(group) for kind, group in sorted(by_class.items())},
        "contact_residuals": distribution(collector.contact_residuals[rule.name]),
        "contact_residuals_by_witness_class": {
            kind: distribution(values)
            for kind, values in sorted(collector.class_residuals[rule.name].items())
        },
        "miss_spectrum_by_witness_class": {
            kind: {
                "contact_residuals": decades(values, SPECTRUM),
                "light_face_slides": decades(collector.class_misses[rule.name][kind], SPECTRUM),
            }
            for kind, values in sorted(collector.class_residuals[rule.name].items())
        },
        "green_contact_residuals": distribution(collector.green_residuals[rule.name]),
        "light_face_clearance_decades": {
            cause: decades(values)
            for cause, values in sorted(collector.clearances[rule.name].items())
        },
        "light_face_minimum_clearance": {
            cause: sig(min(values))
            for cause, values in sorted(collector.clearances[rule.name].items())
        },
        "across_decades": {
            cause: decades(values, ACROSS_EDGES)
            for cause, values in sorted(collector.across[rule.name].items())
        },
        "tilt_decades_radians": {
            cause: decades(values, TILT_EDGES)
            for cause, values in sorted(collector.tilts[rule.name].items())
        },
        "faces_by_obstacle": dict(sorted(collector.obstacles[rule.name].items())),
        "band_faces": (
            collector.band_faces[rule.name]
            if rule.gap <= PRECISION_SCALE
            else {
                str(n): count
                for n, count in sorted(
                    Counter(face["n"] for face in collector.band_faces[rule.name]).items()
                )
            }
        ),
        "regularizable_records": [row["n"] for row in regular],
        "regularizable_squares": sum(len(row["squares"]) for row in regular),
        "within_band_squares": sum(
            item[1] == "within-band" for row in regular for item in row["squares"]
        ),
        "within_band_records": sorted(
            {row["n"] for row in regular for item in row["squares"] if item[1] == "within-band"}
        ),
    }


def expected_document(entries: Sequence[dict[str, Any]] | None = None) -> dict[str, Any]:
    collector = Collector()
    for entry in manifest_entries() if entries is None else entries:
        census_case(load_case(entry), collector)
    return {
        "contract": CONTRACT,
        "generated_by": GENERATOR,
        "corpus": "atlas/known-best/manifest.json; every entry",
        "claim_status": "descriptive-measurement",
        "parameters": {
            "hole_clearance": HOLE_CLEARANCE,
            "band_factor": BAND_FACTOR,
            "sweep_overlap_floor": SWEEP_OVERLAP_FLOOR,
            "significant_digits": SIGNIFICANT,
            "faces": "+x, -x, +y, -y in the square's own frame folded nearest the axes",
            "sweep": (
                "exact separating-axis sweep of the square's polygon along the face normal "
                "against every square and the faced wall, on the full-precision witness"
            ),
            "green": (
                "atlas-house: the rendering's data-hue-index 0; workbench rules: "
                "buildAtlasMap slot 0 over the frame's angles in witness order"
            ),
            "light": "green and shaded lighter than four contacts",
            "stagger_across": STAGGER_ACROSS,
            "kinds": (
                "structural: some face is hole-or-open, tilted-neighbour or offset; "
                "slack: otherwise some face is slack or misaligned; within-band: every "
                "non-contact face is angle-near-miss, near-miss or rule-boundary"
            ),
            "regularizable": (
                "the slack and within-band squares: each non-contact face could meet an "
                "aligned neighbour or wall by a slide (or, for angle-near-miss, a turn) of the "
                "recorded size; face by face, not a claim that all can close at once. Rows are "
                "[id, kind, max |clearance|, max across]"
            ),
        },
        "house_replica": {
            "squares_agreeing_with_rendering": collector.replica["agree"],
            "squares_disagreeing_with_rendering": collector.replica["disagree"],
            "mismatches": collector.replica_mismatches,
        },
        "rules": {rule.name: rule_summary(rule, collector) for rule in RULES},
        "named_cases": collector.named,
        "vacancy_families": collector.vacancy,
        "regularizable": {rule.name: collector.regularizable[rule.name] for rule in RULES},
        "entries": {rule.name: collector.rows[rule.name] for rule in RULES},
    }


def _text(document: dict[str, Any]) -> str:
    return retained_json.dumps(document, sort_keys=True)


def _records(document: dict[str, Any]) -> int:
    return len(document["entries"][RULES[0].name])


def update() -> None:
    document = expected_document()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with atomic_output_file(OUTPUT) as temporary:
        temporary.write_text(_text(document), encoding="utf-8")
    print(f"contact-shade census updated: {_records(document)} records")


def json_differences(retained: Any, expected: Any, path: str = "$") -> Iterator[str]:
    """Each JSON path where the retained document and a fresh one disagree, with both values.

    A byte comparison says only that the census moved; this says where, so a failure on a
    runner nobody can reproduce on is diagnosed from its own log.
    """
    if isinstance(retained, dict) and isinstance(expected, dict):
        for key in sorted(set(retained) | set(expected)):
            if key not in retained or key not in expected:
                side = "retained" if key in retained else "fresh"
                yield f"{path}.{key}: present only in {side}"
            else:
                yield from json_differences(retained[key], expected[key], f"{path}.{key}")
    elif isinstance(retained, list) and isinstance(expected, list):
        if len(retained) != len(expected):
            yield f"{path}: retained {len(retained)} items, fresh {len(expected)}"
        for index, (left, right) in enumerate(zip(retained, expected, strict=False)):
            yield from json_differences(left, right, f"{path}[{index}]")
    elif retained != expected:
        yield f"{path}: retained {retained!r}, fresh {expected!r}"


def check() -> None:
    document = expected_document()
    if not OUTPUT.is_file():
        raise ValueError(f"{OUTPUT.relative_to(ROOT)} is missing")
    retained = OUTPUT.read_text(encoding="utf-8")
    if retained != _text(document):
        differences = list(
            itertools.islice(
                json_differences(json.loads(retained), json.loads(_text(document))), 20
            )
        )
        raise ValueError(
            f"{OUTPUT.relative_to(ROOT)} is stale; first differences:\n  "
            + "\n  ".join(differences or ["the bytes differ but the parsed documents agree"])
        )
    print(f"contact-shade census check passed: {_records(document)} records")


def report() -> None:
    document = expected_document()
    for name, summary in document["rules"].items():
        overall = summary["totals"]
        print(
            f"{name}: {overall['light']} of {overall['green']} green squares light in "
            f"{overall['records_with_light']} records; faces {overall['faces']}; "
            f"squares {overall['squares']}"
        )
        print(f"  contact residuals {summary['contact_residuals']}")
        print(f"  band faces {len(summary['band_faces'])}")


def witness_shades(path: Path) -> dict[str, int]:
    """Light and dark axis-aligned squares of any Witness/v2 file under the house and stage
    rules, with no rendering to read.

    This is how a pose outside the atlas -- a regularized view, say -- is shaded the way
    the atlas would shade it. Without a rendering, the house rule's green is a square
    within its angle tolerance of the axes, which is the class `sqpack.render.color` pins
    to hue 0; the stage's green is the atlas slot the page computes. A `.gz` file is read
    decompressed.
    """
    raw = path.read_bytes()
    text = (gzip.decompress(raw) if path.suffix == ".gz" else raw).decode("utf-8")
    witness, frame, degrees = packings_from_witness(load_yaml(text)["witness"])
    house, stage = RULES[0], RULES[1]
    house_counts = [min(4, len(found)) for found in edge_rule_contacts(witness, house)]
    house_green = [abs(square.tilt) <= house.angle_tolerance for square in witness.squares]
    stage_counts = [min(4, len(found)) for found in centre_rule_contacts(frame, stage)]
    tolerance_degrees = stage.angle_tolerance * 180 / math.pi
    stage_green = [slot == 0 for slot in atlas_slots(degrees, tolerance_degrees)]
    return {
        "house_green": sum(house_green),
        "house_light": sum(g and c < 4 for g, c in zip(house_green, house_counts, strict=True)),
        "stage_green": sum(stage_green),
        "stage_light": sum(g and c < 4 for g, c in zip(stage_green, stage_counts, strict=True)),
    }


def witness_report(paths: Sequence[Path]) -> None:
    for path in paths:
        shades = witness_shades(path)
        print(
            f"{path}: house {shades['house_light']} light of {shades['house_green']} green; "
            f"stage {shades['stage_light']} light of {shades['stage_green']} green"
        )


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    mode = command.add_mutually_exclusive_group(required=True)
    mode.add_argument("--update", action="store_true", help="rewrite the retained census")
    mode.add_argument(
        "--check", action="store_true", help="require the retained census to match"
    )
    mode.add_argument("--report", action="store_true", help="print the census summary")
    mode.add_argument(
        "--witness",
        nargs="+",
        type=Path,
        help="shade any Witness/v2 files (.yaml or .yaml.gz) under the house and stage rules",
    )
    return command


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    if args.update:
        update()
    elif args.check:
        check()
    elif args.witness:
        witness_report(args.witness)
    else:
        report()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
