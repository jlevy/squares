#!/usr/bin/env python3
"""Regularize the axis-aligned components of a witness into an exact derived view.

Usage, from `packing/`, each after
`uv run --frozen --all-extras --group dev python -m devtools.regularize_axis_components`:

    witnesses/known-best/n-102.yaml --output-dir /some/scratch/dir [--json]
    --update-atlas [--n N ...] [--workers K]
    --check-atlas
    --verify-atlas [--n N ...] [--workers K]

Each mode also takes `--smallest-dilation`, the prototype described under "Dilation"
below. `--workers` defaults to `sqpack.workers.worker_count`: the `PACK_JOBS` cap the gate
exports, and the whole machine from a shell.

Two renderers shade a square by how many of its four sides it shares whole with a wall
or a same-angle neighbour (X-049, "Why Grid Squares Render Light"). The *house* rule
draws the homepage atlas: `sqpack.render.color` counts an edge matching a wall or a
neighbour's edge at both ends within `2e-6`, angles within `1e-6` radians. The *stage*
rule is the workbench's `core/geometry.ts` `contactFacts`: centres a side apart within
`0.01`, angles within half a degree. This tool counts the house rule with the census's
replica, `devtools.census_atlas_contact_shades.edge_rule_contacts`, and the stage rule
with its own float copy of `contactFacts` at the census's constants.

Many grid squares render lighter than their component suggests because the retained pose
carries slack: a row sits 0.03 from the wall it visibly belongs to, or a square is a
hundredth off the row below it. This tool builds a *regularized view* of one witness and
checks it exactly:

1. **The exact frame.** A decimal witness is promoted to its 36-digit rational pose at
   centre dilation 1 -- the first candidate `promote_rational` tries, and the one every
   retained Couzo certificate is -- and refused when that pose is not exactly a packing
   within `1e-9` of the printed side. A rational witness is its own frame. Every square
   tilted beyond the angle snap tolerance keeps its exact pose.
2. **Straightening.** Every square within the angle snap tolerance of axis alignment is
   replaced by the exactly axis-aligned unit square at the same rational centre, when
   that is exactly feasible. An exact lattice position needs an exactly axis-aligned
   square: a square tilted by `theta` sticks out past a wall-seated lattice slot by
   `theta / 2`.
3. **Compaction.** Each exactly axis-aligned square slides, one axis at a time, toward the
   nearest lattice position (`1/2 + i` from one wall or `side - 1/2 - j` from the other)
   and stops at the first exact contact. A slide is kept when it lowers neither of the
   square's own counts, house or stage, and either is a snap (below the snap tolerance),
   ends on a wall or an exactly axis-aligned square, or raises a count. Passes repeat
   until no square moves.
4. **Neighbour non-regression.** A slide judged by its own square's counts can still cost
   a neighbour a contact. After the passes every square's house and stage counts are
   compared with the source's. A count that fell lost a contact the source had, and a
   contact is lost only when one of its two squares changed: the changed one, the
   neighbour by preference, is held -- its slides first, then its straightening -- and
   the whole regularization runs again from the exact frame. Holding is how a move is
   undone, since a slide reversed in place could run into a square that has since moved
   into the room it left. Rounds repeat until no count falls or nothing changed is left
   to hold, and what remains is reported.
5. **Verification.** The result is verified over `Q` twice: by the repository's exact
   separating-axis verifier and by the independent rational checker that shares no code
   with it.

The view never replaces the source witness, never changes the certified side, never
promotes an evidence tier, and is written by `--output-dir` only outside `witnesses/` and
`atlas/`. A drawing made from it must say it is regularized.

**The atlas layer.** `--update-atlas` regularizes every record of
`atlas/known-best/manifest.json` and keeps, under `atlas/known-best/regularized/`, each
view that changes a square, as deterministic gzip, beside `index.json`: per n the source
witness and its digest, the view and its digest, house and stage light counts before and
after (the census's `witness_shades` on both files), the residual regressions, the exact
verification and the side difference. A record whose view would change no square is
`unchanged` and keeps no file; a record the tool cannot regularize is `refused`, with its
reason. `--check-atlas` is cheap: it compares the index with the manifest, the witnesses
and the retained views by digest and re-verifies nothing. `--verify-atlas` re-derives every
record and requires the index and the views to come out identical.

The index's SHA-256 values are cache keys, not integrity claims (development.md, "Hashes
and Repository-Owned Artifacts"). The source's says whether a view was derived from the
witness the atlas now holds, so a changed witness reads as a stale view rather than
passing. The view's binds the verification verdict recorded beside it to the bytes it was
computed on, so a view regenerated or edited without its verdict being re-derived fails
the cheap check instead of inheriting a verdict it never earned.

**Dilation.** `promote_rational` scales every rounded centre about the container's centre
by `1 + 10^-p`, for `p` from `digits - 5` down to 3 in steps of two, and keeps the first
factor whose pose is exactly a packing within `1e-9` of the printed side. The factor
spreads the whole packing apart: every contact the decimal witness rounded into a sliver
of overlap opens into a gap, and the container grows by about `(side - 1) * 10^-p`. The
atlas layer uses factor 1 only. `--smallest-dilation` is the measured alternative, kept
as a prototype behind a flag: it walks the same ladder and frames the view at the first
factor that verifies. It is not the layer's policy, for the reason the atlas README's
"The regularized views" records: on the records it would open, an exactly verified view
would certify a side the register does not, which is a tier promotion under a drawing's
name.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import math
import tempfile
import time
from collections.abc import Collection, Sequence
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass, field
from fractions import Fraction
from pathlib import Path
from typing import Any

from strif import atomic_output_file

from devtools import census_atlas_contact_shades as shades
from devtools import check_rational_witness_independent as independent
from devtools.atlas_orientation import (
    geometry_transform,
    orient_regularized_view,
    source_orientation,
)
from devtools.upper_bound_packets import MAX_SIDE_INCREASE, RATIONAL_DIGITS
from sqpack import retained_json
from sqpack.verify import separated, verify_packing
from sqpack.witness import (
    WitnessError,
    # `promote_rational` tries centre dilation 1 first and then up to fifteen wider ones,
    # each a full exact verification. The atlas layer refuses any dilation but 1, so this
    # builds each candidate itself and verifies it the same way, rather than paying for
    # verdicts it would discard; `--smallest-dilation` walks the same ladder.
    _promoted_candidate,  # pyright: ignore[reportPrivateUsage]
    exact_verify,
    load_witness,
    materialize_exact_witness,
    witness_document,
)
from sqpack.workers import worker_count
from sqpack.yamlio import load_yaml

ROOT = Path(__file__).resolve().parent.parent
REPO = ROOT.parent
WITNESSES = ROOT / "witnesses"
WITNESS_SCHEMA = WITNESSES / "witness.schema.yaml"
FORBIDDEN_OUTPUT_ROOTS = (WITNESSES, ROOT / "atlas")
MANIFEST = ROOT / "atlas/known-best/manifest.json"
ATLAS_DIR = ROOT / "atlas/known-best/regularized"

ATLAS_CONTRACT = "packing.squares:RegularizedAtlasIndex/v1"
ATLAS_GENERATOR = "python -m devtools.regularize_axis_components --update-atlas"
ALGORITHM = "regularize_axis_components/2"
"""Changed by hand whenever a change to this module changes a view or a count. The cheap
check sees the index, not the code, so this is how it learns the views are out of date."""
VIEW_SUFFIX = "-regularized.yaml.gz"
DRAWING_LABEL = "regularized"
RENDERINGS = "rendering"
"""The subdirectory `devtools.render_regularized_atlas` draws the views into. Its own
`--check` holds those files to the index; this tool's check leaves the directory to it."""


def _rule(name: str) -> shades.Rule:
    return next(rule for rule in shades.RULES if rule.name == name)


HOUSE_RULE = _rule("atlas-house")
"""The homepage atlas's rule: `sqpack.render.color`, as the census replicates it."""
STAGE_RULE = _rule("workbench-stage")
"""The workbench catalogue stage's rule: `core/geometry.ts` `contactFacts`."""
STAGE_GAP = STAGE_RULE.gap
STAGE_ANGLE_TOLERANCE_RADIANS = STAGE_RULE.angle_tolerance
STAGE_ANGLE_TOLERANCE_DEGREES = round(math.degrees(STAGE_ANGLE_TOLERANCE_RADIANS), 12)
ANGLE_SNAP_TOLERANCE_RADIANS = 1e-4
"""Squares tilted less than this are straightened exactly; more is a real rotation."""
SNAP_TOLERANCE = Fraction("1e-9")
"""A move of at most this is a snap, accepted without a contact-count argument."""
PASS_CAP_MARGIN = 2
"""Passes beyond the square count before the fixpoint loop gives up."""
BOX_MARGIN = 1e-6
"""Float bounding boxes only prefilter exact tests. Coordinates stay below twenty, where
binary64 is good to about 4e-15, so a pair whose boxes are this far apart is apart."""
HOLD_SLIDES = "slides"
"""A held square keeps its straightened pose and takes no slide."""
HOLD_POSE = "pose"
"""A held square keeps its certified pose: no straightening, no slide."""

HALF = Fraction(1, 2)
QUARTER_TURN = math.pi / 2

Point = tuple[Fraction, Fraction]
Corners = list[Point]
Direction = tuple[int, int]
Box = tuple[float, float, float, float]
"""`min_x, max_x, min_y, max_y` in binary64, for prefilters only."""

AXES: tuple[tuple[str, int], ...] = (("x", 0), ("y", 1))
FACES: tuple[tuple[str, Direction], ...] = (
    ("left", (-1, 0)),
    ("right", (1, 0)),
    ("bottom", (0, -1)),
    ("top", (0, 1)),
)
STAGE_WALLS: tuple[tuple[str, int, bool], ...] = (
    ("-x", 0, False),
    ("+x", 0, True),
    ("-y", 1, False),
    ("+y", 1, True),
)
"""The census's face name, the axis, and whether the wall is the far one."""


class RegularizeError(ValueError):
    """A typed refusal: the witness cannot be regularized exactly, and this says why."""

    def __init__(self, kind: str, detail: str):
        super().__init__(detail)
        self.kind = kind


# --------------------------------------------------------------------------------------
# Rational geometry
# --------------------------------------------------------------------------------------


def rational_sign(value: Fraction) -> int:
    return (value > 0) - (value < 0)


def literal(value: Fraction) -> str:
    return (
        str(value.numerator)
        if value.denominator == 1
        else f"{value.numerator}/{value.denominator}"
    )


def centre(corners: Corners) -> Point:
    return (
        sum((x for x, _ in corners), Fraction(0)) / 4,
        sum((y for _, y in corners), Fraction(0)) / 4,
    )


def bounding_box(corners: Corners) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    xs = [x for x, _ in corners]
    ys = [y for _, y in corners]
    return min(xs), max(xs), min(ys), max(ys)


def float_box(corners: Corners) -> Box:
    xs = [float(x) for x, _ in corners]
    ys = [float(y) for _, y in corners]
    return min(xs), max(xs), min(ys), max(ys)


def boxes_apart(first: Box, second: Box) -> bool:
    """Whether two float boxes are separated by more than `BOX_MARGIN` on some axis."""
    return (
        first[1] + BOX_MARGIN < second[0]
        or second[1] + BOX_MARGIN < first[0]
        or first[3] + BOX_MARGIN < second[2]
        or second[3] + BOX_MARGIN < first[2]
    )


def axis_square(center: Point) -> Corners:
    """The exactly axis-aligned unit square at `center`, counter-clockwise from lower-left."""
    cx, cy = center
    return [
        (cx - HALF, cy - HALF),
        (cx + HALF, cy - HALF),
        (cx + HALF, cy + HALF),
        (cx - HALF, cy + HALF),
    ]


def translate(corners: Corners, direction: Direction, distance: Fraction) -> Corners:
    dx, dy = direction
    return [(x + dx * distance, y + dy * distance) for x, y in corners]


def is_exact_axis(corners: Corners) -> bool:
    (ax, ay), (bx, by) = corners[0], corners[1]
    return (ax == bx) or (ay == by)


def _edge_normals(corners: Corners) -> list[Point]:
    normals: list[Point] = []
    for k in (0, 1):
        (px, py), (qx, qy) = corners[k], corners[k + 1]
        normals.append((-(qy - py), qx - px))
    return normals


def _projection(corners: Corners, axis: Point) -> tuple[Fraction, Fraction]:
    values = [axis[0] * x + axis[1] * y for x, y in corners]
    return min(values), max(values)


def interior_overlap_interval(
    moving: Corners, direction: Direction, fixed: Corners
) -> tuple[Fraction, Fraction] | None:
    """The open interval of slide distances at which the two interiors overlap.

    `moving + t * direction` and `fixed` have overlapping interiors exactly when every
    edge-normal axis of either square sees their projections overlap as open intervals.
    Each axis contributes one open interval of `t` (or everything, or nothing); the
    answer is their intersection, `None` when it is empty.  Exact over the rationals,
    which is what lets a slide stop at a zero gap without calling it an overlap.
    """
    low: Fraction | None = None
    high: Fraction | None = None
    for axis in _edge_normals(moving) + _edge_normals(fixed):
        a_lo, a_hi = _projection(moving, axis)
        b_lo, b_hi = _projection(fixed, axis)
        speed = direction[0] * axis[0] + direction[1] * axis[1]
        if speed == 0:
            if a_lo < b_hi and b_lo < a_hi:
                continue
            return None
        enter, leave = (b_lo - a_hi) / speed, (b_hi - a_lo) / speed
        if speed < 0:
            enter, leave = leave, enter
        low = enter if low is None else max(low, enter)
        high = leave if high is None else min(high, leave)
    if low is None or high is None or low >= high:
        return None
    return low, high


@dataclass(frozen=True)
class Blocker:
    kind: str
    """`wall`, `square`, or `target`."""
    name: str


def slide_limit(
    moving: Corners,
    direction: Direction,
    distance: Fraction,
    others: Sequence[tuple[str, Corners]],
    side: Fraction,
    *,
    boxes: Sequence[Box] | None = None,
) -> tuple[Fraction, list[Blocker]]:
    """How far `moving` may slide along `direction`, and what it then touches.

    Returns the exact distance, at most `distance`, and every blocker in contact at
    that distance: the wall or squares that stop the slide, or `target` alone when
    nothing does.  A square already overlapping is reported as a zero slide.  `boxes`,
    one float box per entry of `others`, lets a caller that keeps them skip the exact
    bounding boxes; a box only decides which pairs reach the exact test.
    """
    limit = distance
    blockers: list[Blocker] = [Blocker("target", "")]
    min_x, max_x, min_y, max_y = bounding_box(moving)
    dx, dy = direction
    wall_room = {
        (-1, 0): min_x,
        (1, 0): side - max_x,
        (0, -1): min_y,
        (0, 1): side - max_y,
    }[direction]
    wall_name = {(-1, 0): "x=0", (1, 0): "x=s", (0, -1): "y=0", (0, 1): "y=s"}[direction]
    if wall_room < limit:
        limit, blockers = wall_room, [Blocker("wall", wall_name)]
    elif wall_room == limit:
        blockers.append(Blocker("wall", wall_name))
    swept = (
        min(min_x, min_x + dx * distance),
        max(max_x, max_x + dx * distance),
        min(min_y, min_y + dy * distance),
        max(max_y, max_y + dy * distance),
    )
    swept_box: Box = (float(swept[0]), float(swept[1]), float(swept[2]), float(swept[3]))
    for position, (name, fixed) in enumerate(others):
        if boxes is not None:
            if boxes_apart(boxes[position], swept_box):
                continue
        else:
            o_min_x, o_max_x, o_min_y, o_max_y = bounding_box(fixed)
            # Boxes that only touch the swept box are kept: a slide that ends in exact
            # contact must report what it touches, which is how a move is judged.
            if (
                o_max_x < swept[0]
                or o_min_x > swept[1]
                or o_max_y < swept[2]
                or o_min_y > swept[3]
            ):
                continue
        window = interior_overlap_interval(moving, direction, fixed)
        if window is None:
            continue
        enter, leave = window
        if leave <= 0:
            continue
        room = max(enter, Fraction(0))
        if room < limit:
            limit, blockers = room, [Blocker("square", name)]
        elif room == limit:
            blockers.append(Blocker("square", name))
    if limit == distance and blockers and blockers[0].kind != "target":
        blockers.insert(0, Blocker("target", ""))
    return limit, blockers


def lattice_target(coordinate: Fraction, side: Fraction) -> Fraction:
    """The nearest lattice centre, seated from either wall; ties go to the origin side."""
    slots = math.floor(side - 1)
    if slots < 0:
        return coordinate
    low_index = min(max(round(coordinate - HALF), 0), slots)
    high_index = min(max(round(side - HALF - coordinate), 0), slots)
    low = HALF + low_index
    high = side - HALF - high_index
    return low if abs(coordinate - low) <= abs(coordinate - high) else high


# --------------------------------------------------------------------------------------
# The two shading rules, in binary64 as the renderers hold the poses
# --------------------------------------------------------------------------------------

Pose = tuple[float, float, float]
"""A square's centre and angle in radians, in binary64, as the workbench holds them."""


def angle_gap(angle: float) -> float:
    """Distance of an angle from the nearest quarter-turn multiple, as the stage folds it."""
    distance = math.fmod(abs(angle), QUARTER_TURN)
    return min(distance, QUARTER_TURN - distance)


def _shares_side(first: Pose, second: Pose, gap: float) -> bool:
    dx, dy = second[0] - first[0], second[1] - first[1]
    cosine, sine = math.cos(first[2]), math.sin(first[2])
    along = dx * cosine + dy * sine
    across = -dx * sine + dy * cosine
    return (abs(abs(along) - 1) <= gap and abs(across) <= gap) or (
        abs(abs(across) - 1) <= gap and abs(along) <= gap
    )


def _stage_pair(first: Pose, second: Pose) -> bool:
    """Whether a pair shares a side under the stage rule, read in `first`'s frame, which
    `contactFacts` takes to be the lower-indexed square's."""
    dx, dy = second[0] - first[0], second[1] - first[1]
    if dx * dx + dy * dy > 2.5:
        return False
    if angle_gap(first[2] - second[2]) > STAGE_ANGLE_TOLERANCE_RADIANS:
        return False
    return _shares_side(first, second, STAGE_GAP)


def _stage_walls(pose: Pose, side: float) -> list[str]:
    x, y, angle = pose
    if angle_gap(angle) > STAGE_ANGLE_TOLERANCE_RADIANS:
        return []
    return [
        shades.WALL_NAMES[face]
        for face, axis, far in STAGE_WALLS
        if abs((x, y)[axis] - (side - 0.5 if far else 0.5)) <= STAGE_GAP
    ]


def stage_partners(poses: Sequence[Pose], side: float, ids: Sequence[str]) -> list[list[str]]:
    """Every full-side contact each square has under the stage rule, uncapped: the walls by
    the census's names and the neighbours by square id. The stage shades by
    `min(4, len(...))`. Walls count only for a square within the angle tolerance of the
    axes; a pair counts when both fold to one angle class and, in the lower-indexed
    square's frame, one centre offset is a side and the other nothing, each within the
    gap."""
    found = [_stage_walls(pose, side) for pose in poses]
    for left in range(len(poses)):
        for right in range(left + 1, len(poses)):
            if _stage_pair(poses[left], poses[right]):
                found[left].append(ids[right])
                found[right].append(ids[left])
    return found


def stage_contacts(poses: Sequence[Pose], side: float) -> list[int]:
    """Each square's stage count, capped at four as the stage shades."""
    ids = [str(index) for index in range(len(poses))]
    return [min(4, len(found)) for found in stage_partners(poses, side, ids)]


def stage_count_of(index: int, poses: Sequence[Pose], side: float) -> int:
    """One square's stage count, equal to its entry in `stage_contacts`."""
    count = len(_stage_walls(poses[index], side))
    for other, pose in enumerate(poses):
        if other == index:
            continue
        first, second = (poses[index], pose) if index < other else (pose, poses[index])
        if _stage_pair(first, second):
            count += 1
    return min(4, count)


def house_partners(poses: Sequence[Pose], side: float, ids: Sequence[str]) -> list[list[str]]:
    """Every full-side contact each square has under the house rule: at most one per edge,
    the walls by name and the neighbours by square id, from the census's replica of
    `sqpack.render.color`."""
    packing = shades.Packing(
        side,
        tuple(shades.make_square(ident, *pose) for ident, pose in zip(ids, poses, strict=True)),
    )
    return [
        [contact.other for contact in found]
        for found in shades.edge_rule_contacts(packing, HOUSE_RULE)
    ]


def house_count_of(index: int, poses: Sequence[Pose], side: float, ids: Sequence[str]) -> int:
    """One square's house count, equal to its entry in `house_partners`.

    Only squares within the census's pair reach can share an edge with it, so the
    replica is run on those alone, with only the pairs that include this square.
    """
    x, y, _angle = poses[index]
    reach = shades.PAIR_REACH
    order = [
        index,
        *(
            other
            for other, (ox, oy, _other_angle) in enumerate(poses)
            if other != index and abs(ox - x) <= reach and abs(oy - y) <= reach
        ),
    ]
    packing = shades.Packing(
        side, tuple(shades.make_square(ids[member], *poses[member]) for member in order)
    )
    pairs = [(0, position) for position in range(1, len(order))]
    return len(shades.edge_rule_contacts(packing, HOUSE_RULE, pairs)[0])


def house_green(pose: Pose) -> bool:
    """Whether the house renderer gives this square the right-angle hue."""
    return abs(shades.make_square("", *pose).tilt) <= HOUSE_RULE.angle_tolerance


def stage_green(pose: Pose) -> bool:
    """Whether the stage puts this square in the right-angle class."""
    return angle_gap(pose[2]) <= STAGE_ANGLE_TOLERANCE_RADIANS


def pose_of(corners: Corners) -> Pose:
    cx, cy = centre(corners)
    (ax, ay), (bx, by) = corners[0], corners[1]
    angle = 0.0 if is_exact_axis(corners) else math.atan2(float(by - ay), float(bx - ax))
    return float(cx), float(cy), angle


# --------------------------------------------------------------------------------------
# Loading: the exact frame a witness can be regularized in
# --------------------------------------------------------------------------------------


@dataclass
class Piece:
    square_id: str
    corners: Corners
    source_angle: float
    """The retained angle in radians, folded to its distance from axis alignment."""
    status: str = "tilted"
    """`tilted`, `near-axis-untouched`, `exact-axis`, `rotation-blocked`, or `held`."""
    moves: list[dict[str, Any]] = field(default_factory=list)
    pose: Pose = field(init=False)
    box: Box = field(init=False)

    def __post_init__(self) -> None:
        self.place(self.corners)

    def place(self, corners: Corners) -> None:
        """Move the square, keeping its binary64 pose and box in step with its corners."""
        self.corners = corners
        self.pose = pose_of(corners)
        self.box = float_box(corners)

    @property
    def stage_axis(self) -> bool:
        return self.source_angle <= STAGE_ANGLE_TOLERANCE_RADIANS

    @property
    def exact_axis(self) -> bool:
        return self.status == "exact-axis"


@dataclass
class ExactFrame:
    pieces: list[Piece]
    side: Fraction
    reported_side: Fraction
    before: list[Pose]
    """The retained witness as the renderers draw it: binary64 centres and angles."""
    provenance: dict[str, Any]


def _witness_poses(witness: dict[str, Any]) -> list[Pose]:
    """The retained pose in the workbench's arithmetic, shifted to a lower-left origin."""
    side = float(Fraction(str(witness["side"])))
    shift = side / 2 if witness["coordinates"]["origin"] == "container-center" else 0.0
    unit = witness["coordinates"]["angle_unit"]
    poses: list[Pose] = []
    for square in witness["squares"]:
        if witness["representation"] == "corners":
            corners = [(Fraction(str(x)), Fraction(str(y))) for x, y in square["corners"]]
            x, y, angle = pose_of(corners)
            poses.append((x + shift, y + shift, angle))
            continue
        x, y = (float(Fraction(str(value))) for value in square["center"])
        if witness["representation"] == "center-angle":
            angle = float(Fraction(str(square["angle"])))
            angle = math.radians(angle) if unit == "degrees" else angle
        else:
            angle = math.atan2(
                float(Fraction(str(square["basis"][1]))),
                float(Fraction(str(square["basis"][0]))),
            )
        poses.append((x + shift, y + shift, angle))
    return poses


def promotion_dilations(rational_digits: int) -> list[Fraction]:
    """`promote_rational`'s ladder of centre dilations, smallest first: 1, then
    `1 + 10^-p` for `p` from `rational_digits - 5` down to 3 in steps of two."""
    exponents = range(max(2, rational_digits - 5), 1, -2)
    return [Fraction(1), *(Fraction(1) + Fraction(1, 10**power) for power in exponents)]


def _decimal_frame(
    witness: dict[str, Any], *, smallest_dilation: bool = False
) -> tuple[list[Corners], Fraction, Fraction]:
    """The 36-digit rational pose and the centre dilation it was built at.

    Dilation 1 alone unless `smallest_dilation`, which tries `promote_rational`'s ladder in
    its order and takes the first pose that is exactly a packing within `1e-9` of the
    printed side; refused when none is.
    """
    reported_side = Fraction(str(witness["side"]))
    allowed = reported_side + Fraction(MAX_SIDE_INCREASE)
    ladder = promotion_dilations(RATIONAL_DIGITS) if smallest_dilation else [Fraction(1)]
    refusal = RegularizeError("promotion-overlap", "no candidate attempted")
    for dilation in ladder:
        at = f"the {RATIONAL_DIGITS}-digit rational pose at dilation {literal(dilation)}"
        try:
            squares, side = _promoted_candidate(
                witness, rational_digits=RATIONAL_DIGITS, dilation=dilation
            )
        except WitnessError as error:
            raise RegularizeError(
                "promotion-unsupported",
                f"no {RATIONAL_DIGITS}-digit rational pose can be built from this witness: "
                f"{error}",
            ) from error
        if side > allowed:
            refusal = RegularizeError(
                "promotion-side",
                f"{at} needs side {float(side):.17g}, more than {MAX_SIDE_INCREASE} above "
                f"the printed {witness['side']}",
            )
            continue
        report = verify_packing(squares, side, sign=rational_sign, bucket=True)
        if report.valid:
            return [list(square) for square in squares], side, dilation
        refusal = RegularizeError(
            "promotion-overlap",
            f"{at} is not a packing ({len(report.failures)} failures, first "
            f"{report.failures[:2]}); "
            + (
                "no dilation on promote_rational's ladder within the side allowance is"
                if smallest_dilation
                else "only a dilated pose would be, and that is not the author's packing"
            ),
        )
    raise refusal


def exact_frame(witness: dict[str, Any], *, smallest_dilation: bool = False) -> ExactFrame:
    """The exact rational pose this witness is regularized from, and where it came from."""
    kind = witness["scalar"]["kind"]
    if kind not in {"rational", "decimal"}:
        raise RegularizeError(
            "unsupported-scalar-kind",
            f"{kind!r} geometry has no exact rational frame here: an enclosure proves no "
            "equality and an algebraic field needs field arithmetic this tool lacks",
        )
    reported_side = Fraction(str(witness["side"]))
    before = _witness_poses(witness)
    if kind == "rational":
        expanded, side = materialize_exact_witness(witness)
        if not isinstance(side, Fraction):
            raise TypeError("rational regularization requires a rational side")
        corners: list[Corners] = []
        for square in expanded:
            parsed: Corners = []
            for x, y in square:
                if not isinstance(x, Fraction) or not isinstance(y, Fraction):
                    raise TypeError("rational regularization requires rational corners")
                parsed.append((x, y))
            corners.append(parsed)
        pieces = [
            Piece(str(square["id"]), expanded_corners, angle_gap(pose[2]))
            for square, expanded_corners, pose in zip(
                witness["squares"], corners, before, strict=True
            )
        ]
        provenance = {
            "kind": "rational",
            "derivation": (
                "the witness's own rational corners"
                if witness["representation"] == "corners"
                else "the witness's exact rational pose expansion"
            ),
            "certified_side": literal(reported_side),
            "center_dilation": "1",
        }
        return ExactFrame(pieces, side, reported_side, before, provenance)
    corners, side, dilation = _decimal_frame(witness, smallest_dilation=smallest_dilation)
    pieces = [
        Piece(str(square["id"]), square_corners, angle_gap(pose[2]))
        for square, square_corners, pose in zip(
            witness["squares"], corners, before, strict=True
        )
    ]
    derivation = (
        f"the {RATIONAL_DIGITS}-digit rational pose at centre dilation 1, the first "
        "candidate promote_rational tries and the procedure upper_bound_packets "
        "certify uses, verified exactly in process"
        if dilation == 1
        else f"the {RATIONAL_DIGITS}-digit rational pose at centre dilation "
        f"{literal(dilation)}, the first on promote_rational's ladder that is exactly a "
        "packing, verified exactly in process (the --smallest-dilation prototype)"
    )
    provenance = {
        "kind": "rational",
        "derivation": derivation,
        "rational_digits": RATIONAL_DIGITS,
        "max_side_increase": MAX_SIDE_INCREASE,
        "center_dilation": literal(dilation),
        "certified_side": literal(side),
        "certified_side_decimal": f"{float(side):.17g}",
    }
    return ExactFrame(pieces, side, reported_side, before, provenance)


# --------------------------------------------------------------------------------------
# Regularization
# --------------------------------------------------------------------------------------


def _feasible(index: int, corners: Corners, pieces: Sequence[Piece], side: Fraction) -> bool:
    """Whether `corners` in place of piece `index` is exactly inside and interior-disjoint."""
    min_x, max_x, min_y, max_y = bounding_box(corners)
    if min_x < 0 or min_y < 0 or max_x > side or max_y > side:
        return False
    box: Box = (float(min_x), float(max_x), float(min_y), float(max_y))
    for other, piece in enumerate(pieces):
        if other == index or boxes_apart(box, piece.box):
            continue
        if separated(corners, piece.corners, rational_sign) is None:
            return False
    return True


def straighten(
    pieces: list[Piece], side: Fraction, *, angle_snap: float, keep: Collection[int] = ()
) -> None:
    """Replace every nearly axis-aligned square by the exact one at its centre, when feasible.

    All candidates are straightened together first, because two squares in exact contact
    in the certificate may each block the other's straightening alone and not together.
    If the joint replacement fails, each candidate is tried on its own in id order and
    the ones that fail are kept as the certificate has them. Squares in `keep` are held
    at their certified pose and are not candidates.
    """
    candidates = [
        index
        for index, piece in enumerate(pieces)
        if piece.source_angle <= angle_snap and index not in keep
    ]
    proposed = {index: axis_square(centre(pieces[index].corners)) for index in candidates}
    trial = [
        Piece(p.square_id, proposed.get(i, p.corners), p.source_angle)
        for i, p in enumerate(pieces)
    ]
    if all(_feasible(index, trial[index].corners, trial, side) for index in candidates):
        for index in candidates:
            pieces[index].place(proposed[index])
            pieces[index].status = "exact-axis"
    else:
        for index in candidates:
            if _feasible(index, proposed[index], pieces, side):
                pieces[index].place(proposed[index])
                pieces[index].status = "exact-axis"
            else:
                pieces[index].status = "rotation-blocked"
    for index in keep:
        pieces[index].status = "held"
    for piece in pieces:
        if piece.status == "tilted" and piece.stage_axis:
            piece.status = "near-axis-untouched"


def _attempt_slide(
    index: int,
    axis: int,
    pieces: list[Piece],
    side: Fraction,
    *,
    ids: Sequence[str],
    by_id: dict[str, Piece],
    snap_tolerance: Fraction,
) -> dict[str, Any] | None:
    """Slide one square along one axis toward its lattice target; return the move or None."""
    piece = pieces[index]
    position = centre(piece.corners)[axis]
    target = lattice_target(position, side)
    if target == position:
        return None
    sign = 1 if target > position else -1
    direction: Direction = (sign, 0) if axis == 0 else (0, sign)
    distance = abs(target - position)
    others = [(p.square_id, p.corners) for i, p in enumerate(pieces) if i != index]
    boxes = [p.box for i, p in enumerate(pieces) if i != index]
    limit, blockers = slide_limit(piece.corners, direction, distance, others, side, boxes=boxes)
    if limit == 0:
        return None
    moved = translate(piece.corners, direction, limit)
    walls = float(side)
    poses = [p.pose for p in pieces]
    stage_before = stage_count_of(index, poses, walls)
    house_before = house_count_of(index, poses, walls, ids)
    poses[index] = pose_of(moved)
    stage_after = stage_count_of(index, poses, walls)
    house_after = house_count_of(index, poses, walls, ids)
    ends_on_face = any(
        b.kind == "wall" or (b.kind == "square" and by_id[b.name].exact_axis) for b in blockers
    )
    kind = "snap" if limit <= snap_tolerance else "compaction"
    lowers = stage_after < stage_before or house_after < house_before
    raises = stage_after > stage_before or house_after > house_before
    accepted = not lowers and (kind == "snap" or raises or ends_on_face)
    move = {
        "axis": "xy"[axis],
        "direction": sign,
        "distance": str(limit),
        "distance_decimal": f"{float(limit):.3e}",
        "reached_target": limit == distance,
        "blockers": [f"{b.kind}:{b.name}" if b.name else b.kind for b in blockers],
        "kind": kind,
        "stage_contacts": [stage_before, stage_after],
        "house_contacts": [house_before, house_after],
        "accepted": accepted,
    }
    if accepted:
        piece.place(moved)
    return move


def compact(
    pieces: list[Piece],
    side: Fraction,
    *,
    snap_tolerance: Fraction,
    max_passes: int,
    frozen: Collection[int] = (),
) -> dict[str, Any]:
    """Slide exact axis-aligned squares toward lattice positions until nothing moves.

    Squares in `frozen` are held where they are: others may slide into contact with them.
    """
    order = sorted(
        (i for i, p in enumerate(pieces) if p.exact_axis and i not in frozen),
        key=lambda i: (_wall_distance(pieces[i].corners, side), pieces[i].square_id),
    )
    ids = [p.square_id for p in pieces]
    by_id = {p.square_id: p for p in pieces}
    passes = 0
    converged = False
    accepted = rejected = snaps = compactions = 0
    largest = Fraction(0)
    while passes < max_passes:
        passes += 1
        moved_any = False
        for index in order:
            for _name, axis in AXES:
                move = _attempt_slide(
                    index,
                    axis,
                    pieces,
                    side,
                    ids=ids,
                    by_id=by_id,
                    snap_tolerance=snap_tolerance,
                )
                if move is None:
                    continue
                if move["accepted"] or move not in pieces[index].moves:
                    pieces[index].moves.append(move)
                if move["accepted"]:
                    moved_any = True
                    accepted += 1
                    if move["kind"] == "snap":
                        snaps += 1
                    else:
                        compactions += 1
                    largest = max(largest, Fraction(move["distance"]))
                else:
                    rejected += 1
        if not moved_any:
            converged = True
            break
    return {
        "passes": passes,
        "converged": converged,
        "accepted": accepted,
        "snaps": snaps,
        "compactions": compactions,
        "rejected": rejected,
        "largest_move": str(largest),
        "largest_move_decimal": f"{float(largest):.3e}",
    }


def _wall_distance(corners: Corners, side: Fraction) -> Fraction:
    min_x, max_x, min_y, max_y = bounding_box(corners)
    return min(min_x, min_y, side - max_x, side - max_y)


def histogram(counts: Sequence[int]) -> list[int]:
    """How many squares carry each contact count from zero to four."""
    return [sum(1 for count in counts if count == k) for k in range(5)]


# --------------------------------------------------------------------------------------
# Neighbour non-regression
# --------------------------------------------------------------------------------------

RULE_NAMES = ("house", "stage")


@dataclass(frozen=True)
class Regression:
    """A square whose count under one rule fell below the source's."""

    index: int
    rule: str
    before: int
    after: int
    lost: tuple[str, ...]
    """The contacts the source had and the view does not: square ids and wall names."""


def contact_partners(poses: Sequence[Pose], side: float, ids: Sequence[str]) -> dict[str, Any]:
    return {
        "house": house_partners(poses, side, ids),
        "stage": stage_partners(poses, side, ids),
    }


def regressions_between(
    baseline: dict[str, list[list[str]]], now: dict[str, list[list[str]]]
) -> list[Regression]:
    found: list[Regression] = []
    for rule in RULE_NAMES:
        for index, (was, is_now) in enumerate(zip(baseline[rule], now[rule], strict=True)):
            before, after = min(4, len(was)), min(4, len(is_now))
            if after < before:
                lost = tuple(sorted(set(was) - set(is_now)))
                found.append(Regression(index, rule, before, after, lost))
    return found


def escalations_for(
    regressions: Sequence[Regression],
    pieces: Sequence[Piece],
    certified: Sequence[Corners],
    held: dict[int, str],
    index_of: dict[str, int],
) -> dict[int, str]:
    """Which squares to hold next round, and how far, to give back each lost contact.

    A lost contact had two squares, or a square and a wall, and is lost only if one of
    them changed. The neighbour is held when it changed -- the move being undone is the
    one that cost another square its contact -- and otherwise the square itself. A square
    that slid is first held to its straightened pose; one that changed only by being
    straightened, or is already held there, goes back to its certified pose. A square is
    escalated at most once a round, and an unchanged one never.
    """
    chosen: dict[int, str] = {}

    def escalate(index: int) -> bool:
        if index in chosen:
            return True
        if pieces[index].corners == certified[index]:
            return False
        slid = held.get(index) is None and any(m["accepted"] for m in pieces[index].moves)
        chosen[index] = HOLD_SLIDES if slid else HOLD_POSE
        return True

    for regression in regressions:
        for label in regression.lost:
            neighbour = index_of.get(label)
            if neighbour is not None and escalate(neighbour):
                continue
            escalate(regression.index)
    return chosen


# --------------------------------------------------------------------------------------
# Classifying what stays light
# --------------------------------------------------------------------------------------


def _face_contact(index: int, face: Direction, poses: Sequence[Pose], side: float) -> bool:
    x, y, _angle = poses[index]
    fx, fy = face
    if fx and abs(x - (0.5 if fx < 0 else side - 0.5)) <= STAGE_GAP:
        return True
    if fy and abs(y - (0.5 if fy < 0 else side - 0.5)) <= STAGE_GAP:
        return True
    for other, pose in enumerate(poses):
        if other == index or angle_gap(pose[2]) > STAGE_ANGLE_TOLERANCE_RADIANS:
            continue
        dx, dy = pose[0] - x, pose[1] - y
        along, across = (dx, dy) if fx else (dy, dx)
        if abs(along - (fx or fy)) <= STAGE_GAP and abs(across) <= STAGE_GAP:
            return True
    return False


def at_lattice(piece: Piece, side: Fraction, axis: int) -> bool:
    """Whether the square's centre sits exactly on its nearest lattice position on `axis`."""
    position = centre(piece.corners)[axis]
    return lattice_target(position, side) == position


def classify_face(
    index: int, face: Direction, pieces: Sequence[Piece], poses: Sequence[Pose], side: Fraction
) -> str:
    """Why a face of an exact axis-aligned square has no counted stage contact.

    The face is pushed outward by up to one side with the same exact slide the
    compaction uses, and what stops it decides the label.  `hole`: nothing within a side,
    or a wall or an aligned axis-aligned square further than the gap while every square
    involved already sits on its lattice, so the gap is the mismatch between the two
    wall-seated lattices and no slide closes it.  `tilted-neighbour`: the first thing in
    front is a square outside the stage angle tolerance.  `offset`: an axis-aligned
    square is in front but shifted across by more than the gap.  `slack`: an aligned
    axis-aligned square is in front, further than the gap, and one of the two is off its
    lattice, so a compaction was blocked or refused.  `wall-slack`: the same for a wall.
    `untouched-neighbour`: the square in front is one the stage calls axis-aligned but
    that was not straightened (tilted beyond the snap tolerance, or held), so it is as
    certified.  A gap wider than half a side is a hole whatever is behind it: no lattice
    slot fits in it.
    """
    piece = pieces[index]
    others = [(p.square_id, p.corners) for i, p in enumerate(pieces) if i != index]
    boxes = [p.box for i, p in enumerate(pieces) if i != index]
    limit, blockers = slide_limit(piece.corners, face, Fraction(1), others, side, boxes=boxes)
    stops = [b for b in blockers if b.kind != "target"]
    if limit >= 1 or not stops:
        return "hole"
    axis = 0 if face[0] else 1
    seated = at_lattice(piece, side, axis)
    if any(b.kind == "wall" for b in stops):
        return "hole" if seated or limit > HALF else "wall-slack"
    by_id = {p.square_id: (i, p) for i, p in enumerate(pieces)}
    other, neighbour = by_id[stops[0].name]
    if not neighbour.stage_axis:
        return "tilted-neighbour"
    if not neighbour.exact_axis:
        return "untouched-neighbour"
    across = abs(poses[other][1 - axis] - poses[index][1 - axis])
    if across > STAGE_GAP:
        return "offset"
    both_seated = seated and at_lattice(neighbour, side, axis)
    return "hole" if both_seated or limit > HALF else "slack"


# --------------------------------------------------------------------------------------
# The whole operation
# --------------------------------------------------------------------------------------


def regularized_witness(
    witness: dict[str, Any], frame: ExactFrame, *, summary: dict[str, Any], source_path: str
) -> dict[str, Any]:
    """The regularized view as a Witness/v2 record: rational corners, verified, derived."""
    retained = witness.get("source") or {}
    source = {"path": str(retained.get("path") or "unrecorded")}
    for key in ("key", "url", "retrieved"):
        value = retained.get(key)
        if isinstance(value, str) and value:
            source[key] = value
    return {
        "id": f"{witness['id']}-regularized",
        "n": witness["n"],
        "side": literal(frame.side),
        "square_size": "1",
        "representation": "corners",
        "scalar": {"kind": "rational"},
        "coordinates": {
            "origin": "lower-left",
            "axes": "x-right-y-up",
            "angle_unit": "not-applicable",
        },
        "squares": [
            {
                "id": witness["squares"][i]["id"],
                "corners": [[literal(x), literal(y)] for x, y in p.corners],
            }
            for i, p in enumerate(frame.pieces)
        ],
        "claim": {
            "coordinate_provenance": "verified",
            "method": "exact-algebraic",
            "limitations": (
                "A regularized derived view for drawing, not the source witness: tilted "
                "squares keep their certified exact pose, nearly axis-aligned squares are "
                "straightened and slid into exact lattice or face contact unless that "
                "would cost any square a house or stage contact the source has, and the "
                "container side is the exact certificate's. It changes no frontier value, "
                "promotes no evidence tier, and any drawing made from it must say it is "
                "regularized."
            ),
        },
        "source": source,
        "certificate": {
            "kind": "regularized-view",
            "label": DRAWING_LABEL,
            "derived_from": witness["id"],
            "derived_from_path": source_path,
            "exact_frame": frame.provenance,
            "regularization": summary,
            "replay": "uv run --frozen packing-witness verify <this file, decompressed>",
        },
    }


def contact_tally(
    before: Sequence[int],
    after: Sequence[int],
    green_before: Sequence[bool],
    green_after: Sequence[bool],
) -> dict[str, Any]:
    """One rule's counts before and after: the light right-angle squares, the squares that
    turned dark or lighter, and the histograms."""
    return {
        "green_before": sum(green_before),
        "green_after": sum(green_after),
        "light_before": sum(g and c < 4 for g, c in zip(green_before, before, strict=True)),
        "light_after": sum(g and c < 4 for g, c in zip(green_after, after, strict=True)),
        "became_dark": sum(
            g and b < 4 and a == 4 for g, b, a in zip(green_after, before, after, strict=True)
        ),
        "became_lighter": sum(a < b for b, a in zip(before, after, strict=True)),
        "histogram_before": histogram(before),
        "histogram_after": histogram(after),
        "total_before": sum(before),
        "total_after": sum(after),
    }


@dataclass
class Outcome:
    """What the rounds of regularization settle on."""

    pieces: list[Piece]
    moves: dict[str, Any]
    held: dict[int, str]
    rounds: list[dict[str, Any]]
    baseline: dict[str, list[list[str]]]
    final: dict[str, list[list[str]]]
    residual: list[Regression]


def settle(
    frame: ExactFrame, *, angle_snap: float, snap_tolerance: Fraction, max_passes: int
) -> Outcome:
    """Straighten and compact, then hold what cost a neighbour a contact, until stable."""
    ids = [p.square_id for p in frame.pieces]
    index_of = {ident: index for index, ident in enumerate(ids)}
    certified = [p.corners for p in frame.pieces]
    baseline = contact_partners(frame.before, float(frame.reported_side), ids)
    walls = float(frame.side)
    held: dict[int, str] = {}
    rounds: list[dict[str, Any]] = []
    # Each round either stops or raises at least one square's hold, and a square has two
    # holds to give, so this many rounds can never run out first.
    for _round in range(2 * len(ids) + 1):
        pieces = [Piece(p.square_id, p.corners, p.source_angle) for p in frame.pieces]
        straighten(
            pieces,
            frame.side,
            angle_snap=angle_snap,
            keep={i for i, level in held.items() if level == HOLD_POSE},
        )
        moves = compact(
            pieces,
            frame.side,
            snap_tolerance=snap_tolerance,
            max_passes=max_passes,
            frozen=set(held),
        )
        final = contact_partners([p.pose for p in pieces], walls, ids)
        regressions = regressions_between(baseline, final)
        escalations = escalations_for(regressions, pieces, certified, held, index_of)
        rounds.append(
            {
                "regressions": {
                    rule: sum(regression.rule == rule for regression in regressions)
                    for rule in RULE_NAMES
                },
                "newly_held": {ids[i]: level for i, level in sorted(escalations.items())},
            }
        )
        if not regressions or not escalations:
            return Outcome(pieces, moves, held, rounds, baseline, final, regressions)
        held.update(escalations)
    message = "the non-regression rounds did not settle"
    raise RuntimeError(message)


def regularize_frame(
    witness: dict[str, Any],
    frame: ExactFrame,
    *,
    source_path: str,
    angle_snap: float = ANGLE_SNAP_TOLERANCE_RADIANS,
    snap_tolerance: Fraction = SNAP_TOLERANCE,
    max_passes: int | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Regularize a witness from its exact frame; return the report and the view."""
    side = frame.side
    passes = max_passes if max_passes is not None else len(frame.pieces) + PASS_CAP_MARGIN
    outcome = settle(
        frame, angle_snap=angle_snap, snap_tolerance=snap_tolerance, max_passes=passes
    )
    pieces = outcome.pieces
    ids = [p.square_id for p in pieces]
    after_poses = [p.pose for p in pieces]
    counts = {
        rule: (
            [min(4, len(found)) for found in outcome.baseline[rule]],
            [min(4, len(found)) for found in outcome.final[rule]],
        )
        for rule in RULE_NAMES
    }
    greens = {
        "house": (
            [house_green(p) for p in frame.before],
            [house_green(p) for p in after_poses],
        ),
        "stage": (
            [stage_green(p) for p in frame.before],
            [stage_green(p) for p in after_poses],
        ),
    }
    report = verify_packing([p.corners for p in pieces], side, sign=rational_sign, bucket=True)
    certified = [p.corners for p in frame.pieces]
    changed = sum(p.corners != corners for p, corners in zip(pieces, certified, strict=True))

    per_square: list[dict[str, Any]] = []
    structural: dict[str, int] = {}
    stage_before, stage_after = counts["stage"]
    for index, piece in enumerate(pieces):
        entry: dict[str, Any] = {
            "id": piece.square_id,
            "status": piece.status,
            "held": outcome.held.get(index),
            "source_angle_from_axis": f"{piece.source_angle:.3e}",
            "house": [counts["house"][0][index], counts["house"][1][index]],
            "stage": [stage_before[index], stage_after[index]],
            "moves": [m for m in piece.moves if m["accepted"]],
            "rejected_moves": [m for m in piece.moves if not m["accepted"]],
        }
        if piece.exact_axis and stage_after[index] < 4:
            faces = {
                name: classify_face(index, face, pieces, after_poses, side)
                for name, face in FACES
                if not _face_contact(index, face, after_poses, float(side))
            }
            entry["light_faces"] = faces
            for reason in faces.values():
                structural[reason] = structural.get(reason, 0) + 1
        per_square.append(entry)

    statuses: dict[str, int] = {}
    for piece in pieces:
        statuses[piece.status] = statuses.get(piece.status, 0) + 1
    summary = {
        "angle_snap_tolerance_radians": angle_snap,
        "snap_tolerance": str(snap_tolerance),
        "statuses": statuses,
        "moves": outcome.moves,
        "non_regression": {
            "rules": list(RULE_NAMES),
            "rounds": len(outcome.rounds),
            "held": {ids[i]: level for i, level in sorted(outcome.held.items())},
            "residual_regressions": len(outcome.residual),
        },
        "changed_squares": changed,
        "exact_contacts_after": report.touching_pairs,
    }
    result = {
        "operation": "regularize",
        "source": {
            "id": witness["id"],
            "path": source_path,
            "n": witness["n"],
            "reported_side": str(frame.reported_side),
            "scalar_kind": witness["scalar"]["kind"],
            "representation": witness["representation"],
            "coordinate_provenance": witness["claim"]["coordinate_provenance"],
            "method": witness["claim"]["method"],
        },
        "exact_frame": {
            **frame.provenance,
            "side_minus_reported": str(side - frame.reported_side),
            "side_minus_reported_decimal": f"{float(side - frame.reported_side):.3e}",
            "fits_reported_side": side <= frame.reported_side,
        },
        "rules": {
            "house": {
                "gap": HOUSE_RULE.gap,
                "angle_tolerance_radians": HOUSE_RULE.angle_tolerance,
                "governs": HOUSE_RULE.governs,
            },
            "stage": {
                "gap": STAGE_GAP,
                "angle_tolerance_degrees": STAGE_ANGLE_TOLERANCE_DEGREES,
                "walls": "axis-aligned squares only",
                "cap": 4,
                "governs": STAGE_RULE.governs,
            },
        },
        "regularization": {**summary, "rounds": outcome.rounds},
        "contacts": {rule: contact_tally(*counts[rule], *greens[rule]) for rule in RULE_NAMES},
        "residual_regressions": [
            {
                "id": ids[r.index],
                "rule": r.rule,
                "before": r.before,
                "after": r.after,
                "lost": list(r.lost),
            }
            for r in outcome.residual
        ],
        "structural_light_faces": dict(sorted(structural.items())),
        "exact_verification": {
            "arithmetic": "rational (fractions.Fraction), exact separating-axis predicates",
            "repository_verifier": {
                "valid": report.valid,
                "pairs_tested": report.pairs_tested,
                "touching_pairs": report.touching_pairs,
                "container_contacts": report.container_contacts,
                "failures": report.failures[:10],
            },
        },
        "squares": per_square,
        "claim_boundary": (
            "Derived view only. Same n, the certificate's exact side (never larger than "
            "the verified upper bound), tilted squares unchanged from the certificate. Not "
            "the source witness, not a frontier change, not an evidence-tier promotion; a "
            "drawing of it must say it is regularized."
        ),
    }
    view_frame = ExactFrame(pieces, side, frame.reported_side, frame.before, frame.provenance)
    view = regularized_witness(witness, view_frame, summary=summary, source_path=source_path)
    return result, view


def regularize(
    witness: dict[str, Any],
    *,
    source_path: str,
    angle_snap: float = ANGLE_SNAP_TOLERANCE_RADIANS,
    snap_tolerance: Fraction = SNAP_TOLERANCE,
    max_passes: int | None = None,
    smallest_dilation: bool = False,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Regularize one witness; return the report and the regularized Witness/v2 record."""
    return regularize_frame(
        witness,
        exact_frame(witness, smallest_dilation=smallest_dilation),
        source_path=source_path,
        angle_snap=angle_snap,
        snap_tolerance=snap_tolerance,
        max_passes=max_passes,
    )


# --------------------------------------------------------------------------------------
# One witness to a directory
# --------------------------------------------------------------------------------------


def _guard_output_dir(output_dir: Path) -> Path:
    resolved = output_dir.resolve()
    for forbidden in FORBIDDEN_OUTPUT_ROOTS:
        if resolved == forbidden.resolve() or forbidden.resolve() in resolved.parents:
            raise RegularizeError(
                "forbidden-output",
                "a regularized view is a derived artifact and may not be written under "
                f"{forbidden}",
            )
    return resolved


def _repository_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO).as_posix()
    except ValueError:
        return path.as_posix()


def run_one(
    path: Path,
    output_dir: Path,
    *,
    angle_snap: float,
    snap_tolerance: Fraction,
    max_passes: int | None,
    smallest_dilation: bool = False,
) -> dict[str, Any]:
    witness = load_witness(path, fallback_schema=WITNESS_SCHEMA)
    report, view = regularize(
        witness,
        source_path=_repository_path(path),
        angle_snap=angle_snap,
        snap_tolerance=snap_tolerance,
        max_passes=max_passes,
        smallest_dilation=smallest_dilation,
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    stem = f"{path.stem}-regularized"
    witness_path = output_dir / f"{stem}.yaml"
    schema = WITNESS_SCHEMA.relative_to(output_dir.resolve(), walk_up=True).as_posix()
    with atomic_output_file(witness_path) as temporary:
        temporary.write_text(witness_document(view, schema=schema), encoding="utf-8")
    independent_verdict = independent.check(witness_path)
    report["exact_verification"]["independent_checker"] = independent_verdict
    report["exact_verification"]["passed"] = bool(
        report["exact_verification"]["repository_verifier"]["valid"]
        and independent_verdict["verification_passed"]
    )
    report_path = output_dir / f"{stem}.json"
    report["outputs"] = {"witness": str(witness_path), "report": str(report_path)}
    with atomic_output_file(report_path) as temporary:
        temporary.write_text(json.dumps(report, indent=2, sort_keys=True, default=str) + "\n")
    return report


def summarize(report: dict[str, Any]) -> str:
    house = report["contacts"]["house"]
    stage = report["contacts"]["stage"]
    moves = report["regularization"]["moves"]
    guard = report["regularization"]["non_regression"]
    exact = report["exact_verification"]
    dilation = report["exact_frame"]["center_dilation"]
    return (
        f"n={report['source']['n']}"
        f"{'' if dilation == '1' else f' (centre dilation {dilation})'}: "
        f"house light {house['light_before']} of "
        f"{house['green_before']} -> {house['light_after']} of {house['green_after']}; "
        f"stage light {stage['light_before']} of {stage['green_before']} -> "
        f"{stage['light_after']} of {stage['green_after']}; lighter after: house "
        f"{house['became_lighter']}, stage {stage['became_lighter']} (rounds "
        f"{guard['rounds']}, held {len(guard['held'])}); "
        f"moves {moves['accepted']} accepted ({moves['snaps']} snaps, "
        f"{moves['compactions']} compactions), {moves['rejected']} refused, "
        f"largest {moves['largest_move_decimal']}, passes {moves['passes']}"
        f"{'' if moves['converged'] else ' (NOT converged)'}; "
        f"structural {report['structural_light_faces']}; "
        f"exact {'passed' if exact.get('passed') else 'FAILED'} "
        f"(side - reported = {report['exact_frame']['side_minus_reported_decimal']})"
    )


# --------------------------------------------------------------------------------------
# The atlas layer
# --------------------------------------------------------------------------------------


@dataclass(frozen=True)
class AtlasLayout:
    """Where the atlas layer reads and writes; the tests point it at a scratch tree."""

    packing: Path
    """Where the manifest's witness paths resolve."""
    repo: Path
    """What every path the index records is relative to."""
    manifest: Path
    directory: Path
    certificates: Path
    """Searched for `*/n-NNN-rational.yaml.gz`, the retained rational certificates."""

    @property
    def index(self) -> Path:
        return self.directory / "index.json"

    def view(self, n: int) -> Path:
        return self.directory / f"n-{n:03d}{VIEW_SUFFIX}"

    def relative(self, path: Path) -> str:
        return path.resolve().relative_to(self.repo.resolve()).as_posix()

    def schema_reference(self) -> str:
        """The schema path a view records, relative to the directory it is kept in."""
        return WITNESS_SCHEMA.relative_to(self.directory.resolve(), walk_up=True).as_posix()


ATLAS = AtlasLayout(ROOT, REPO, MANIFEST, ATLAS_DIR, WITNESSES)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


SMALLEST_DILATION = "smallest on promote_rational's ladder that is exactly a packing"
"""What the index's parameters say when a layer is built with `--smallest-dilation`."""


def atlas_parameters(*, smallest_dilation: bool = False) -> dict[str, Any]:
    return {
        "angle_snap_tolerance_radians": ANGLE_SNAP_TOLERANCE_RADIANS,
        "snap_tolerance": str(SNAP_TOLERANCE),
        "rational_digits": RATIONAL_DIGITS,
        "max_side_increase": MAX_SIDE_INCREASE,
        "center_dilation": SMALLEST_DILATION if smallest_dilation else "1",
        "house_rule": {
            "gap": HOUSE_RULE.gap,
            "angle_tolerance_radians": HOUSE_RULE.angle_tolerance,
        },
        "stage_rule": {
            "gap": STAGE_GAP,
            "angle_tolerance_degrees": STAGE_ANGLE_TOLERANCE_DEGREES,
        },
        "shades_measured_by": "devtools.census_atlas_contact_shades.witness_shades",
    }


def _shade_record(before: dict[str, int], after: dict[str, int]) -> dict[str, Any]:
    return {
        rule: {
            "green_before": before[f"{rule}_green"],
            "light_before": before[f"{rule}_light"],
            "green_after": after[f"{rule}_green"],
            "light_after": after[f"{rule}_light"],
        }
        for rule in RULE_NAMES
    }


def _certificate_matches(frame: ExactFrame, path: Path) -> bool:
    """Whether a retained rational certificate is exactly this frame, side and corners."""
    document = load_yaml(gzip.decompress(path.read_bytes()).decode("utf-8"))["witness"]
    if Fraction(str(document["side"])) != frame.side:
        return False
    return all(
        [(Fraction(str(x)), Fraction(str(y))) for x, y in square["corners"]] == piece.corners
        for square, piece in zip(document["squares"], frame.pieces, strict=True)
    )


def atlas_record(
    entry: dict[str, Any], layout: AtlasLayout, *, smallest_dilation: bool = False
) -> tuple[dict[str, Any], str | None, float]:
    """One manifest entry's index record, its view's text when it keeps one, and the
    seconds it took. Runs in a worker process under `--workers`."""
    started = time.perf_counter()
    n = entry["n"]
    source = layout.packing / entry["witness"]["path"]
    witness = load_witness(source, fallback_schema=WITNESS_SCHEMA)
    record: dict[str, Any] = {
        "n": n,
        "status": "",
        "source": {
            "witness": layout.relative(source),
            "id": witness["id"],
            "scalar_kind": witness["scalar"]["kind"],
            "sha256": digest(source.read_bytes()),
        },
    }
    before = shades.witness_shades(source)
    # Compaction chooses lattice targets and breaks ties in the published orientation.
    # Derive there, then apply the selected isometry to the exact result.
    ancestor = source_orientation(witness)
    transform = geometry_transform(witness)
    try:
        frame = exact_frame(ancestor, smallest_dilation=smallest_dilation)
    except RegularizeError as error:
        record["status"] = "refused"
        record["refusal"] = {"kind": error.kind, "reason": str(error)}
        record["shades"] = _shade_record(before, before)
        return record, None, time.perf_counter() - started
    # A count certified again from a later packet has a certificate in each packet's
    # directory, and the frame is exactly the one of the packing the atlas now draws; the
    # first in order is named only when none matches.
    candidates = sorted(layout.certificates.glob(f"*/n-{n:03d}-rational.yaml.gz"))
    matching = next((path for path in candidates if _certificate_matches(frame, path)), None)
    certificate = matching or next(iter(candidates), None)
    record["exact_frame"] = {
        "derivation": frame.provenance["derivation"],
        "retained_certificate": layout.relative(certificate) if certificate else None,
        "matches_retained_certificate": (matching is not None) if certificate else None,
    }
    # Only a dilated frame names its factor, so a layer built at dilation 1 reads the same
    # whether or not the prototype exists.
    if frame.provenance["center_dilation"] != "1":
        record["exact_frame"]["center_dilation"] = frame.provenance["center_dilation"]
    if transform is not None:
        record["exact_frame"]["ancestor_matches_retained_certificate"] = (
            (matching is not None) if certificate else None
        )
        record["exact_frame"]["matches_retained_certificate"] = False
        record["exact_frame"]["geometry_transform"] = transform
        record["exact_frame"]["derivation"] = (
            f"{frame.provenance['derivation']}; isometry-derived atlas orientation"
        )
    report, view = regularize_frame(ancestor, frame, source_path=layout.relative(source))
    view = orient_regularized_view(
        view, witness, parent_certificate=layout.relative(certificate) if certificate else None
    )
    # The ancestor's verdict is not a receipt for the reflected rational coordinates.
    # Both independent implementations verify the actual retained view below.
    _, transformed_report = exact_verify(view) if transform is not None else (None, None)
    regularization = report["regularization"]
    record["moves"] = {
        key: regularization["moves"][key]
        for key in ("accepted", "snaps", "compactions", "rejected", "largest_move_decimal")
    }
    record["statuses"] = dict(sorted(regularization["statuses"].items()))
    record["non_regression"] = {
        "rounds": regularization["non_regression"]["rounds"],
        "held_slides": sum(
            level == HOLD_SLIDES for level in regularization["non_regression"]["held"].values()
        ),
        "held_pose": sum(
            level == HOLD_POSE for level in regularization["non_regression"]["held"].values()
        ),
        "residual_regressions": {
            rule: report["contacts"][rule]["became_lighter"] for rule in RULE_NAMES
        },
    }
    record["side"] = {
        "reported": str(witness["side"]),
        "view_minus_reported": report["exact_frame"]["side_minus_reported_decimal"],
        "fits_reported_side": report["exact_frame"]["fits_reported_side"],
    }
    if regularization["changed_squares"] == 0:
        record["status"] = "unchanged"
        record["shades"] = _shade_record(before, before)
        return record, None, time.perf_counter() - started
    text = witness_document(view, schema=layout.schema_reference())
    with tempfile.TemporaryDirectory() as scratch:
        plain = Path(scratch) / "view.yaml"
        plain.write_text(text, encoding="utf-8")
        verdict = independent.check(plain)
        after = shades.witness_shades(plain)
    repository = report["exact_verification"]["repository_verifier"]
    repository_valid = (
        transformed_report.valid if transformed_report is not None else repository["valid"]
    )
    passed = bool(repository_valid and verdict["verification_passed"])
    record["status"] = "regularized" if passed else "failed-verification"
    record["changed_squares"] = regularization["changed_squares"]
    record["view"] = {"path": layout.relative(layout.view(n)), "sha256": digest(text.encode())}
    record["shades"] = _shade_record(before, after)
    record["exact_verification"] = {
        "repository_verifier": bool(repository_valid),
        "independent_checker": bool(verdict["verification_passed"]),
        "pairs_tested_independently": verdict["pairs_tested"],
        "passed": passed,
    }
    return record, text if passed else None, time.perf_counter() - started


def atlas_totals(records: Sequence[dict[str, Any]]) -> dict[str, Any]:
    statuses: dict[str, int] = {}
    refusals: dict[str, int] = {}
    for record in records:
        statuses[record["status"]] = statuses.get(record["status"], 0) + 1
        if record["status"] == "refused":
            kind = record["refusal"]["kind"]
            refusals[kind] = refusals.get(kind, 0) + 1
    shade_totals = {
        rule: {
            key: sum(record["shades"][rule][key] for record in records)
            for key in ("green_before", "light_before", "green_after", "light_after")
        }
        for rule in RULE_NAMES
    }
    regularized = [record for record in records if record["status"] == "regularized"]
    return {
        "records": len(records),
        "statuses": dict(sorted(statuses.items())),
        "refusals": dict(sorted(refusals.items())),
        "shades": shade_totals,
        "shades_of_regularized_records": {
            rule: {
                key: sum(record["shades"][rule][key] for record in regularized)
                for key in ("green_before", "light_before", "green_after", "light_after")
            }
            for rule in RULE_NAMES
        },
        "residual_regressions": {
            rule: sum(
                record.get("non_regression", {}).get("residual_regressions", {}).get(rule, 0)
                for record in records
            )
            for rule in RULE_NAMES
        },
        "held_squares": sum(
            record.get("non_regression", {}).get("held_slides", 0)
            + record.get("non_regression", {}).get("held_pose", 0)
            for record in records
        ),
    }


def atlas_index(
    records: Sequence[dict[str, Any]], *, smallest_dilation: bool = False
) -> dict[str, Any]:
    return {
        "contract": ATLAS_CONTRACT,
        "generated_by": ATLAS_GENERATOR,
        "algorithm": ALGORITHM,
        "label": DRAWING_LABEL,
        "policy": (
            "A derived drawing layer, never a witness: each view is the record's exact frame "
            "with its near-axis squares straightened and slid into exact contact, verified "
            "twice over Q at the certificate's side. It changes no side, frontier value or "
            "evidence tier, and every drawing made from it must be labelled 'regularized'."
        ),
        "digests": (
            "Cache keys, not integrity claims: source.sha256 says the view was derived from "
            "the witness the atlas now holds; view.sha256, of the decompressed YAML, binds "
            "the verification verdict recorded beside it to those bytes."
        ),
        "parameters": atlas_parameters(smallest_dilation=smallest_dilation),
        "totals": atlas_totals(records),
        "entries": list(records),
    }


def _index_text(index: dict[str, Any]) -> str:
    return retained_json.dumps(index, ensure_ascii=False)


def _normalized(record: dict[str, Any]) -> dict[str, Any]:
    """A record as it reads back from the index's JSON."""
    return json.loads(json.dumps(record))


def manifest_entries(layout: AtlasLayout) -> list[dict[str, Any]]:
    return json.loads(layout.manifest.read_text(encoding="utf-8"))["atlas"]["entries"]


def _select(
    entries: Sequence[dict[str, Any]], only: Collection[int] | None
) -> list[dict[str, Any]]:
    if not only:
        return list(entries)
    known = {entry["n"] for entry in entries}
    missing = sorted(set(only) - known)
    if missing:
        message = f"not in the manifest: {missing}"
        raise SystemExit(message)
    return [entry for entry in entries if entry["n"] in only]


def run_records(
    entries: Sequence[dict[str, Any]],
    layout: AtlasLayout,
    *,
    workers: int,
    smallest_dilation: bool = False,
) -> dict[int, tuple[dict[str, Any], str | None, float]]:
    """Every entry's record, the largest n first so the workers finish together."""
    ordered = sorted(entries, key=lambda entry: -entry["n"])
    results: dict[int, tuple[dict[str, Any], str | None, float]] = {}

    def note(n: int, outcome: tuple[dict[str, Any], str | None, float]) -> None:
        results[n] = outcome
        record, _text, seconds = outcome
        print(
            f"[{len(results)}/{len(ordered)}] n={n}: {record['status']} ({seconds:.1f}s)",
            flush=True,
        )

    if workers <= 1:
        for entry in ordered:
            note(entry["n"], atlas_record(entry, layout, smallest_dilation=smallest_dilation))
        return results
    with ProcessPoolExecutor(max_workers=workers) as pool:
        futures = {
            pool.submit(
                atlas_record, entry, layout, smallest_dilation=smallest_dilation
            ): entry["n"]
            for entry in ordered
        }
        for future in as_completed(futures):
            note(futures[future], future.result())
    return results


def _committed_index(layout: AtlasLayout) -> dict[str, Any] | None:
    if not layout.index.is_file():
        return None
    return json.loads(layout.index.read_text(encoding="utf-8"))


def _gzip(text: str) -> bytes:
    """Deterministic gzip: no name, no timestamp, the same text gives the same bytes."""
    return gzip.compress(text.encode("utf-8"), compresslevel=9, mtime=0)


def update_atlas(
    layout: AtlasLayout,
    *,
    only: Collection[int] | None,
    workers: int | None,
    smallest_dilation: bool = False,
) -> int:
    started = time.perf_counter()
    entries = manifest_entries(layout)
    selected = _select(entries, only)
    workers = worker_count(len(selected)) if workers is None else workers
    results = run_records(
        selected, layout, workers=workers, smallest_dilation=smallest_dilation
    )
    committed = _committed_index(layout)
    previous = {record["n"]: record for record in (committed or {}).get("entries", [])}
    records: list[dict[str, Any]] = []
    for entry in entries:
        n = entry["n"]
        if n in results:
            records.append(_normalized(results[n][0]))
        elif n in previous:
            records.append(previous[n])
        else:
            message = f"n={n} has no record; run --update-atlas without --n first"
            raise SystemExit(message)
    layout.directory.mkdir(parents=True, exist_ok=True)
    for n, (_record, text, _seconds) in sorted(results.items()):
        target = layout.view(n)
        if text is None:
            target.unlink(missing_ok=True)
            continue
        with atomic_output_file(target) as temporary:
            temporary.write_bytes(_gzip(text))
    kept = {layout.view(record["n"]).name for record in records if "view" in record}
    for stray in layout.directory.glob(f"*{VIEW_SUFFIX}"):
        if stray.name not in kept:
            stray.unlink()
    index = atlas_index(records, smallest_dilation=smallest_dilation)
    with atomic_output_file(layout.index) as temporary:
        temporary.write_text(_index_text(index), encoding="utf-8")
    elapsed = time.perf_counter() - started
    serial = sum(seconds for _record, _text, seconds in results.values())
    print(_totals_line(index["totals"]))
    print(
        f"{len(results)} records in {elapsed:.0f}s wall on {workers} worker(s), "
        f"{serial:.0f}s summed over records"
    )
    failed = [record["n"] for record in records if record["status"] == "failed-verification"]
    if failed:
        print(f"FAILED exact verification: {failed}")
        return 1
    return 0


def _totals_line(totals: dict[str, Any]) -> str:
    house = totals["shades"]["house"]
    stage = totals["shades"]["stage"]
    return (
        f"{totals['records']} records {totals['statuses']}, refusals {totals['refusals']}; "
        f"house light {house['light_before']} -> {house['light_after']} "
        f"(green {house['green_before']} -> {house['green_after']}); stage light "
        f"{stage['light_before']} -> {stage['light_after']}; residual regressions "
        f"{totals['residual_regressions']}; held squares {totals['held_squares']}"
    )


def check_atlas(layout: AtlasLayout, *, smallest_dilation: bool = False) -> list[str]:
    """The cheap check: the index against the manifest, the witnesses and the retained
    views, by digest. It re-derives and re-verifies nothing."""
    index = _committed_index(layout)
    if index is None:
        return [f"{layout.relative(layout.index)} is missing; run --update-atlas"]
    problems: list[str] = []
    for key, expected in (
        ("contract", ATLAS_CONTRACT),
        ("algorithm", ALGORITHM),
        ("label", DRAWING_LABEL),
        ("parameters", _normalized(atlas_parameters(smallest_dilation=smallest_dilation))),
    ):
        if index.get(key) != expected:
            problems.append(f"index {key} is {index.get(key)!r}, the tool's is {expected!r}")
    records = index.get("entries", [])
    if index.get("totals") != _normalized(atlas_totals(records)):
        problems.append("index totals do not sum its entries")
    by_n = {record["n"]: record for record in records}
    entries = manifest_entries(layout)
    if sorted(by_n) != sorted(entry["n"] for entry in entries) or len(by_n) != len(records):
        problems.append("index entries are not exactly the manifest's n, once each")
    kept: set[str] = set()
    for entry in entries:
        record = by_n.get(entry["n"])
        if record is None:
            continue
        problems.extend(_check_record(layout, entry, record, kept))
    problems.extend(
        f"unexpected file {layout.relative(path)}"
        for path in sorted(layout.directory.iterdir())
        if path.name not in {layout.index.name, *kept}
        and not (path.name == RENDERINGS and path.is_dir())
    )
    return problems


def _check_record(
    layout: AtlasLayout, entry: dict[str, Any], record: dict[str, Any], kept: set[str]
) -> list[str]:
    n = entry["n"]
    source = layout.packing / entry["witness"]["path"]
    problems: list[str] = []
    if record["source"]["witness"] != layout.relative(source):
        problems.append(f"n={n}: index names {record['source']['witness']}, manifest {source}")
    elif digest(source.read_bytes()) != record["source"]["sha256"]:
        problems.append(f"n={n}: the witness changed since its view was derived (stale)")
    status = record["status"]
    view = layout.view(n)
    if status == "regularized":
        kept.add(view.name)
        if record["view"]["path"] != layout.relative(view):
            problems.append(f"n={n}: index view path {record['view']['path']}")
        if not view.is_file():
            problems.append(f"n={n}: {layout.relative(view)} is missing")
            return problems
        data = view.read_bytes()
        if data[:8] != b"\x1f\x8b\x08\x00\x00\x00\x00\x00":
            problems.append(f"n={n}: the view is not a deterministic gzip")
        if digest(gzip.decompress(data)) != record["view"]["sha256"]:
            problems.append(
                f"n={n}: the view differs from the one its verdict was recorded for"
            )
        if not record["exact_verification"]["passed"]:
            problems.append(f"n={n}: recorded exact verification did not pass")
    elif status in {"unchanged", "refused"}:
        if view.exists():
            problems.append(f"n={n}: {status}, yet {layout.relative(view)} exists")
    else:
        problems.append(f"n={n}: status {status!r}")
    return problems


def verify_atlas(
    layout: AtlasLayout,
    *,
    only: Collection[int] | None,
    workers: int | None,
    smallest_dilation: bool = False,
) -> list[str]:
    """Re-derive every selected record and require it, and its view, to be identical."""
    index = _committed_index(layout)
    if index is None:
        return [f"{layout.relative(layout.index)} is missing; run --update-atlas"]
    expected = _normalized(atlas_parameters(smallest_dilation=smallest_dilation))
    if index.get("parameters") != expected:
        return [f"index parameters are {index.get('parameters')!r}, the tool's {expected!r}"]
    committed = {record["n"]: record for record in index.get("entries", [])}
    selected = _select(manifest_entries(layout), only)
    workers = worker_count(len(selected)) if workers is None else workers
    results = run_records(
        selected, layout, workers=workers, smallest_dilation=smallest_dilation
    )
    problems: list[str] = []
    for n, (record, text, _seconds) in sorted(results.items()):
        if _normalized(record) != committed.get(n):
            problems.append(f"n={n}: the re-derived record differs from the index")
        view = layout.view(n)
        retained = (
            gzip.decompress(view.read_bytes()).decode("utf-8") if view.is_file() else None
        )
        if text != retained:
            problems.append(f"n={n}: the re-derived view differs from the retained one")
    return problems


# --------------------------------------------------------------------------------------
# Command line
# --------------------------------------------------------------------------------------


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    command.add_argument(
        "witnesses", nargs="*", type=Path, help="Witness/v2 YAML files to regularize"
    )
    command.add_argument(
        "--output-dir",
        type=Path,
        help="where the regularized witness and report go (never under witnesses/ or atlas/)",
    )
    mode = command.add_mutually_exclusive_group()
    mode.add_argument(
        "--update-atlas",
        action="store_true",
        help="regularize the atlas's records into atlas/known-best/regularized/",
    )
    mode.add_argument(
        "--check-atlas",
        action="store_true",
        help="compare the retained layer's index with the manifest, witnesses and views",
    )
    mode.add_argument(
        "--verify-atlas",
        action="store_true",
        help="re-derive the retained layer and require it to come out identical",
    )
    command.add_argument(
        "--n", type=int, nargs="+", default=None, help="only these n (update and verify)"
    )
    command.add_argument(
        "--workers",
        type=int,
        default=None,
        help="worker processes (update and verify); default: the PACK_JOBS cap, or every cpu",
    )
    command.add_argument(
        "--smallest-dilation",
        action="store_true",
        help=(
            "prototype: frame a decimal witness at the smallest centre dilation on "
            "promote_rational's ladder that is exactly a packing, not at dilation 1 only"
        ),
    )
    command.add_argument(
        "--angle-snap",
        type=float,
        default=ANGLE_SNAP_TOLERANCE_RADIANS,
        help="radians from axis alignment within which a square is straightened exactly",
    )
    command.add_argument(
        "--snap-tolerance",
        type=Fraction,
        default=SNAP_TOLERANCE,
        help="moves up to this are snaps and need no contact-count argument",
    )
    command.add_argument(
        "--max-passes", type=int, default=None, help="cap on compaction passes"
    )
    command.add_argument("--json", action="store_true", help="print each report as JSON")
    return command


def _atlas_main(args: argparse.Namespace, layout: AtlasLayout) -> int:
    if args.witnesses or args.output_dir is not None:
        print("the atlas modes take no witness files and no --output-dir")
        return 2
    dilate = bool(args.smallest_dilation)
    if args.check_atlas:
        started = time.perf_counter()
        problems = check_atlas(layout, smallest_dilation=dilate)
        for problem in problems:
            print(problem)
        elapsed = time.perf_counter() - started
        if problems:
            print(f"regularized atlas check FAILED: {len(problems)} problem(s)")
            return 1
        index = _committed_index(layout) or {}
        print(_totals_line(index["totals"]))
        print(f"regularized atlas check passed in {elapsed:.2f}s")
        return 0
    only = set(args.n) if args.n else None
    if args.update_atlas:
        return update_atlas(layout, only=only, workers=args.workers, smallest_dilation=dilate)
    started = time.perf_counter()
    problems = verify_atlas(layout, only=only, workers=args.workers, smallest_dilation=dilate)
    for problem in problems:
        print(problem)
    elapsed = time.perf_counter() - started
    print(
        f"regularized atlas verification {'FAILED' if problems else 'passed'} in {elapsed:.0f}s"
    )
    return 1 if problems else 0


def main(argv: Sequence[str] | None = None, *, layout: AtlasLayout = ATLAS) -> int:
    args = parser().parse_args(argv)
    if args.update_atlas or args.check_atlas or args.verify_atlas:
        return _atlas_main(args, layout)
    if not args.witnesses or args.output_dir is None:
        print("give witness files and --output-dir, or one of the atlas modes")
        return 2
    try:
        output_dir = _guard_output_dir(args.output_dir)
    except RegularizeError as error:
        print(f"refused [{error.kind}]: {error}")
        return 2
    status = 0
    for path in args.witnesses:
        try:
            report = run_one(
                path,
                output_dir,
                angle_snap=args.angle_snap,
                snap_tolerance=args.snap_tolerance,
                max_passes=args.max_passes,
                smallest_dilation=args.smallest_dilation,
            )
        except (RegularizeError, WitnessError) as error:
            print(f"{path}: refused [{error.kind}]: {error}")
            status = 1
            continue
        print(
            json.dumps(report, indent=2, sort_keys=True, default=str)
            if args.json
            else summarize(report)
        )
        if not report["exact_verification"]["passed"]:
            status = 1
    return status


if __name__ == "__main__":
    raise SystemExit(main())
