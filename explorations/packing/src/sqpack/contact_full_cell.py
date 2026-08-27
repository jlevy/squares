"""Target-free structural labels and work prices for one fixed-angle cell.

Version 1 deliberately supports only the exact axis-aligned frame. It owns no centres,
container side, numerical row matrix, solver outcome, or target-corpus lookup. Its job is
to make every discrete choice explicit before a later stage is allowed to solve it.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from itertools import combinations, islice, permutations
from typing import Literal

from sqpack.contact_assembly import (
    D4_TRANSFORMS,
    VECTOR_WALLS,
    WALL_ORDER,
    WALL_VECTORS,
    Axis,
    D4Transform,
    OrbitWitness,
    Wall,
)

ANGLE_FRAME = "axis-aligned/v1"
ANGLE_VALUE = "0"
EVIDENCE_ROLE = (
    "target-free structural full-cell label and work price; no geometry, container fit, "
    "packing feasibility, or optimality claim"
)
MAX_FULL_CELL_SIZE = 5


def _is_square_id(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


class FullCellError(ValueError):
    """A typed malformed-input or unsupported-slice refusal."""

    def __init__(self, kind: str, detail: str):
        super().__init__(detail)
        self.kind = kind


@dataclass(frozen=True, order=True)
class AssemblyPart:
    """One caller-declared structural part in a complete square partition."""

    kind: str
    members: tuple[int, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.kind, str) or not self.kind:
            raise FullCellError("full-cell-partition", "part kinds must be nonempty")
        if (
            not self.members
            or any(not _is_square_id(member) for member in self.members)
            or len(set(self.members)) != len(self.members)
        ):
            raise FullCellError("full-cell-partition", "parts must contain distinct square ids")
        object.__setattr__(self, "members", tuple(sorted(self.members)))


@dataclass(frozen=True, order=True)
class WallDecision:
    """The total Boolean state of one square against one container wall."""

    square: int
    wall: Wall
    seated: bool

    def __post_init__(self) -> None:
        if (
            not _is_square_id(self.square)
            or self.wall not in WALL_ORDER
            or not isinstance(self.seated, bool)
        ):
            raise FullCellError(
                "full-cell-wall-inventory", "wall decisions require a known wall and bool"
            )


@dataclass(frozen=True, order=True)
class OrientedPairAxis:
    """One endpoint-owned local axis and its positive endpoint on an unordered pair.

    In the v1 equal-angle frame both endpoints own the same two physical axis lines.
    The lower endpoint is therefore the declared structural owner tie-break. The
    positive endpoint retains the pair order, leaving four distinct physical branches
    after the eight raw endpoint-owner, local-axis, and order proposals are normalized.
    """

    left: int
    right: int
    owner: int
    axis: Axis
    positive: int

    def __post_init__(self) -> None:
        if any(
            not _is_square_id(value)
            for value in (self.left, self.right, self.owner, self.positive)
        ):
            raise FullCellError(
                "full-cell-nonedge-axis-inventory",
                "oriented pair axes require exact non-Boolean integer square ids",
            )
        if self.left >= self.right:
            raise FullCellError(
                "full-cell-nonedge-axis-inventory",
                "oriented pair axes require left < right",
            )
        pair = {self.left, self.right}
        if self.owner not in pair or self.positive not in pair or self.axis not in {"u", "v"}:
            raise FullCellError(
                "full-cell-nonedge-axis-inventory",
                "axis owner and positive endpoint must belong to the pair and use u/v",
            )
        object.__setattr__(self, "owner", self.left)

    @property
    def pair(self) -> tuple[int, int]:
        return self.left, self.right


@dataclass(frozen=True)
class FullFixedAngleCell:
    """One complete axis-aligned structural cell, before any numerical solve."""

    angle_frame: str
    angles: tuple[str, ...]
    parts: tuple[AssemblyPart, ...]
    walls: tuple[WallDecision, ...]
    contacts: tuple[OrientedPairAxis, ...]
    nonedges: tuple[OrientedPairAxis, ...]

    def __post_init__(self) -> None:
        size = len(self.angles)
        if not 1 <= size <= MAX_FULL_CELL_SIZE:
            raise FullCellError(
                "full-cell-square-inventory",
                f"full-cell labels require 1..{MAX_FULL_CELL_SIZE} squares",
            )
        if self.angle_frame != ANGLE_FRAME or any(
            angle != ANGLE_VALUE for angle in self.angles
        ):
            raise FullCellError(
                "full-cell-unsupported-angle",
                "FullFixedAngleCellLabel/v1 supports only literal axis-aligned angles",
            )

        parts = tuple(sorted(self.parts))
        members = [member for part in parts for member in part.members]
        if sorted(members) != list(range(size)):
            raise FullCellError(
                "full-cell-partition",
                "assembly parts must partition the complete square inventory exactly once",
            )

        walls = tuple(sorted(self.walls, key=lambda row: (row.square, WALL_ORDER[row.wall])))
        wall_keys = [(row.square, row.wall) for row in walls]
        required_walls = [
            (square, wall)
            for square in range(size)
            for wall in sorted(WALL_ORDER, key=WALL_ORDER.__getitem__)
        ]
        if wall_keys != required_walls:
            raise FullCellError(
                "full-cell-wall-inventory",
                "the full-cell wall decision inventory must contain every "
                "square-wall pair once",
            )

        contacts = tuple(sorted(self.contacts))
        nonedges = tuple(sorted(self.nonedges))
        all_rows = contacts + nonedges
        if any(
            row.left < 0 or row.right >= size or row.owner >= size or row.positive >= size
            for row in all_rows
        ):
            raise FullCellError(
                "full-cell-nonedge-axis-inventory", "pair-axis square id is out of range"
            )
        contact_pairs = [row.pair for row in contacts]
        nonedge_pairs = [row.pair for row in nonedges]
        required_pairs = list(combinations(range(size), 2))
        if (
            len(set(contact_pairs)) != len(contact_pairs)
            or len(set(nonedge_pairs)) != len(nonedge_pairs)
            or set(contact_pairs) & set(nonedge_pairs)
            or sorted(contact_pairs + nonedge_pairs) != required_pairs
        ):
            raise FullCellError(
                "full-cell-pair-inventory",
                "the contact and non-edge pair partition must be exact and disjoint",
            )

        object.__setattr__(self, "parts", parts)
        object.__setattr__(self, "walls", walls)
        object.__setattr__(self, "contacts", contacts)
        object.__setattr__(self, "nonedges", nonedges)


@dataclass(frozen=True)
class FullCellLimits:
    maximum_orbit_images: int = 960

    def __post_init__(self) -> None:
        if (
            isinstance(self.maximum_orbit_images, bool)
            or not isinstance(self.maximum_orbit_images, int)
            or self.maximum_orbit_images < 1
        ):
            raise FullCellError(
                "full-cell-malformed-cap", "maximum_orbit_images must be a positive integer"
            )


@dataclass(frozen=True)
class CanonicalFullCell:
    status: Literal["canonical"]
    canonical_label: str
    cell: FullFixedAngleCell
    witness: OrbitWitness
    raw_image_count: int
    unique_image_count: int


@dataclass(frozen=True)
class FullCellCanonicalizationLimit:
    status: Literal["limit"]
    kind: Literal["orbit-image-cap"]
    limit: int
    required_images: int
    examined_images: int
    partial_best_label: str


type FullCellCanonicalization = CanonicalFullCell | FullCellCanonicalizationLimit


@dataclass(frozen=True)
class FullCellPrice:
    evidence_role: str
    inventory: dict[str, int]
    candidate_domains: dict[str, int]
    executed_work: dict[str, int]


def _vector(transform: D4Transform, x: int, y: int) -> tuple[int, int]:
    return transform.xx * x + transform.xy * y, transform.yx * x + transform.yy * y


def _transform_axis(
    row: OrientedPairAxis,
    *,
    symmetry: D4Transform,
    old_to_new: tuple[int, ...],
) -> OrientedPairAxis:
    source = (1, 0) if row.axis == "u" else (0, 1)
    x, y = _vector(symmetry, *source)
    if x:
        axis: Axis = "u"
        polarity = x
    else:
        axis = "v"
        polarity = y
    mapped_left = old_to_new[row.left]
    mapped_right = old_to_new[row.right]
    left, right = sorted((mapped_left, mapped_right))
    mapped_positive = old_to_new[row.positive]
    positive = mapped_positive if polarity > 0 else ({left, right} - {mapped_positive}).pop()
    return OrientedPairAxis(
        left,
        right,
        old_to_new[row.owner],
        axis,
        positive,
    )


def transform_full_cell(
    cell: FullFixedAngleCell,
    *,
    symmetry: D4Transform,
    old_to_new: tuple[int, ...],
) -> FullFixedAngleCell:
    """Apply one declared D4 action and square relabeling to the entire label."""
    size = len(cell.angles)
    if tuple(sorted(old_to_new)) != tuple(range(size)):
        raise FullCellError(
            "full-cell-malformed-permutation", "old_to_new must be a square permutation"
        )
    angles = [ANGLE_VALUE] * size
    for old, new in enumerate(old_to_new):
        angles[new] = cell.angles[old]
    parts = tuple(
        AssemblyPart(part.kind, tuple(old_to_new[member] for member in part.members))
        for part in cell.parts
    )
    walls = tuple(
        WallDecision(
            old_to_new[row.square],
            VECTOR_WALLS[_vector(symmetry, *WALL_VECTORS[row.wall])],
            row.seated,
        )
        for row in cell.walls
    )
    contacts = tuple(
        _transform_axis(row, symmetry=symmetry, old_to_new=old_to_new) for row in cell.contacts
    )
    nonedges = tuple(
        _transform_axis(row, symmetry=symmetry, old_to_new=old_to_new) for row in cell.nonedges
    )
    return FullFixedAngleCell(
        ANGLE_FRAME,
        tuple(angles),
        parts,
        walls,
        contacts,
        nonedges,
    )


def full_cell_label(cell: FullFixedAngleCell) -> str:
    """Serialize one normalized full structural cell to deterministic bytes."""
    document = {
        "contract": "packing.squares:FullFixedAngleCellLabel/v1",
        "angle_frame": cell.angle_frame,
        "angles": list(cell.angles),
        "parts": [{"kind": part.kind, "members": list(part.members)} for part in cell.parts],
        "walls": [[row.square, row.wall, row.seated] for row in cell.walls],
        "contacts": [
            [row.left, row.right, row.owner, row.axis, row.positive] for row in cell.contacts
        ],
        "nonedges": [
            [row.left, row.right, row.owner, row.axis, row.positive] for row in cell.nonedges
        ],
    }
    return json.dumps(document, sort_keys=True, separators=(",", ":"))


def canonicalize_full_cell(
    cell: FullFixedAngleCell,
    *,
    limits: FullCellLimits | None = None,
) -> FullCellCanonicalization:
    """Minimize the complete label over D4 by square relabeling, or type the cap."""
    if limits is None:
        limits = FullCellLimits()
    size = len(cell.angles)
    required = len(D4_TRANSFORMS) * math.factorial(size)
    images = (
        (symmetry_index, OrbitWitness(symmetry.name, old_to_new), image)
        for symmetry_index, symmetry in enumerate(D4_TRANSFORMS)
        for old_to_new in permutations(range(size))
        for image in (transform_full_cell(cell, symmetry=symmetry, old_to_new=old_to_new),)
    )
    best: tuple[str, int, tuple[int, ...], OrbitWitness, FullFixedAngleCell] | None = None
    unique: set[str] = set()
    examined = 0
    for symmetry_index, witness, image in islice(images, limits.maximum_orbit_images):
        examined += 1
        label = full_cell_label(image)
        unique.add(label)
        candidate = (label, symmetry_index, witness.old_to_new, witness, image)
        if best is None or candidate[:3] < best[:3]:
            best = candidate
    if best is None:
        raise AssertionError("a full cell has an empty symmetry orbit")
    if examined < required:
        return FullCellCanonicalizationLimit(
            "limit",
            "orbit-image-cap",
            limits.maximum_orbit_images,
            required,
            examined,
            best[0],
        )
    return CanonicalFullCell(
        "canonical",
        best[0],
        best[4],
        best[3],
        required,
        len(unique),
    )


def replay_full_cell_witness(
    cell: FullFixedAngleCell, witness: OrbitWitness
) -> FullFixedAngleCell:
    """Replay a retained full-label orbit witness."""
    by_name = {transform.name: transform for transform in D4_TRANSFORMS}
    try:
        symmetry = by_name[witness.symmetry]
    except KeyError as error:
        raise FullCellError(
            "full-cell-unknown-symmetry", f"unknown D4 symmetry {witness.symmetry!r}"
        ) from error
    return transform_full_cell(
        cell,
        symmetry=symmetry,
        old_to_new=witness.old_to_new,
    )


def price_full_cell(
    cell: FullFixedAngleCell, canonical: FullCellCanonicalization
) -> FullCellPrice:
    """Derive candidate-domain and executed-work counts; accept no caller price."""
    if canonical.status != "canonical":
        raise FullCellError(
            "full-cell-price-prerequisite",
            "pricing requires a completed canonical cell, not a partial orbit",
        )
    required_images = len(D4_TRANSFORMS) * math.factorial(len(cell.angles))
    verified = canonicalize_full_cell(
        cell, limits=FullCellLimits(maximum_orbit_images=required_images)
    )
    if verified.status != "canonical" or verified != canonical:
        raise FullCellError(
            "full-cell-price-prerequisite",
            "the canonical receipt does not replay exactly against the priced full cell",
        )
    nonedge_branches = 8 ** len(cell.nonedges)
    return FullCellPrice(
        EVIDENCE_ROLE,
        {
            "squares": len(cell.angles),
            "angle_values": len(cell.angles),
            "wall_decisions": len(cell.walls),
            "seated_walls": sum(row.seated for row in cell.walls),
            "contact_pairs": len(cell.contacts),
            "nonedge_pairs": len(cell.nonedges),
        },
        {
            "partitions": 1,
            "angle_assignments": 1,
            "wall_seatings": 1,
            "nonedge_axis_assignments": nonedge_branches,
            "raw_cells": nonedge_branches,
        },
        {
            "raw_cells_built": 1,
            "axis_order_branches_examined": 1,
            "orbit_images_examined": canonical.raw_image_count,
            "unique_orbit_images": canonical.unique_image_count,
            "duplicate_orbit_images": canonical.raw_image_count - canonical.unique_image_count,
            "canonical_cells_emitted": 1,
            "lp_solves": 0,
        },
    )
