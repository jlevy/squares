"""Exact mass of a literal closed-parent union in the frozen BC303 measure.

The source checks and arithmetic are independent of the T1 core reader. The measure is
identified by its proposal revision and repository-relative path, and the reader by
the checkout HEAD it runs from; both are recorded, with whether either file differs
from HEAD, and neither is compared with a Git blob (OR-16). What the reader checks is
the measure's content: its constants, its 377 distinct in-container atoms, their total
mass and their weight scale.
"""

from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from fractions import Fraction
from math import lcm
from pathlib import Path
from typing import cast

SOURCE_REVISION = "39714308ce2081abbd76624387d134fee4be6deb"
SOURCE_PATH = (
    "packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/"
    "bc-293-measure-free-96-25.json"
)
READER_PATH = "packing/devtools/read_bc303_parent_union.py"
OUTER_SIDE = Fraction(96, 25)
CORE_SIDE = Fraction(9977, 10000)
ANGLE_LIMIT = Fraction(207107, 500000)
TOTAL_MASS = Fraction(22524199, 2000000)
WEIGHT_SCALE = 4_000_000
Q0 = (Fraction(0), Fraction(0), Fraction(1), Fraction(1))

type Point = tuple[Fraction, Fraction]
type Parent = tuple[Fraction, Fraction, Fraction, Fraction]
type Atom = tuple[Point, Fraction]


class ParentUnionError(ValueError):
    """A source, geometry, or checkout check failed."""


@dataclass(frozen=True, slots=True)
class BoundMeasure:
    """The parsed measure and the revisions that name it; the drift flag is recorded."""

    atoms: tuple[Atom, ...]
    source_revision: str
    implementation_revision: str
    implementation_dirty: bool


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ParentUnionError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _reject_constant(value: str) -> object:
    raise ParentUnionError(f"non-finite JSON constant: {value}")


def _fraction(value: object) -> Fraction:
    if not isinstance(value, str):
        raise ParentUnionError("measure coordinate or weight is not a rational string")
    try:
        return Fraction(value)
    except (ValueError, ZeroDivisionError) as error:
        raise ParentUnionError("invalid rational") from error


def parse_measure(data: bytes) -> tuple[Atom, ...]:
    """Check and parse all source rows by content, without measuring any parent."""

    try:
        document = json.loads(
            data, object_pairs_hook=_unique_object, parse_constant=_reject_constant
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ParentUnionError("invalid measure JSON") from error
    if not isinstance(document, dict) or set(document) != {
        "id",
        "n",
        "outer_side",
        "square_side",
        "angle_limit",
        "direction_steps",
        "total_mass",
        "least_cell_mass",
        "symmetry",
        "note",
        "atoms",
    }:
        raise ParentUnionError("measure schema changed")
    source = cast(dict[str, object], document)
    if (
        source["id"] != "bc-293-D-free-final"
        or source["n"] != 11
        or _fraction(source["outer_side"]) != OUTER_SIDE
        or _fraction(source["square_side"]) != CORE_SIDE
        or _fraction(source["angle_limit"]) != ANGLE_LIMIT
        or source["direction_steps"] != 180
        or _fraction(source["total_mass"]) != TOTAL_MASS
        or _fraction(source["least_cell_mass"]) != Fraction(800003, 800000)
        or source["symmetry"] != "D4"
        or not isinstance(source["note"], str)
    ):
        raise ParentUnionError("measure constants changed")
    rows = source["atoms"]
    if not isinstance(rows, list) or len(rows) != 377:
        raise ParentUnionError("measure must have 377 atoms")
    atoms: list[Atom] = []
    seen: set[Point] = set()
    for index, row in enumerate(rows):
        if not isinstance(row, list) or len(row) != 3:
            raise ParentUnionError(f"atom {index} is malformed")
        point = (_fraction(row[0]), _fraction(row[1]))
        weight = _fraction(row[2])
        if (
            point in seen
            or weight <= 0
            or not (0 <= point[0] <= OUTER_SIDE and 0 <= point[1] <= OUTER_SIDE)
        ):
            raise ParentUnionError(f"atom {index} is duplicated or out of range")
        seen.add(point)
        atoms.append((point, weight))
    if sum((weight for _, weight in atoms), Fraction()) != TOTAL_MASS:
        raise ParentUnionError("atom mass does not equal source total")
    if lcm(*(weight.denominator for _, weight in atoms)) != WEIGHT_SCALE:
        raise ParentUnionError("atom weight scale changed")
    return tuple(atoms)


def _git(repository: Path, *arguments: str) -> bytes:
    result = subprocess.run(
        ("git", "-C", str(repository), *arguments), check=False, capture_output=True
    )
    if result.returncode:
        raise ParentUnionError("git revision or source object unavailable")
    return result.stdout


def load_bound_measure(repository: Path) -> BoundMeasure:
    """Read the measure in this checkout and record the revisions that identify it.

    `implementation_dirty` says whether the source or this reader differs from HEAD.
    It is information beside the result, never a refusal.
    """

    root = repository.resolve()
    if Path(_git(root, "rev-parse", "--show-toplevel").decode().strip()).resolve() != root:
        raise ParentUnionError("repository must be its worktree root")
    head = _git(root, "rev-parse", "HEAD").decode().strip()
    source_path = root / SOURCE_PATH
    reader_path = root / READER_PATH
    if source_path.is_symlink() or not source_path.is_file():
        raise ParentUnionError("source path is not a regular file")
    if (
        reader_path.is_symlink()
        or not reader_path.is_file()
        or Path(__file__).resolve() != reader_path
    ):
        raise ParentUnionError("executing reader path differs from checkout")
    atoms = parse_measure(source_path.read_bytes())
    dirty = bool(_git(root, "status", "--porcelain", "--", SOURCE_PATH, READER_PATH).strip())
    return BoundMeasure(atoms, SOURCE_REVISION, head, dirty)


def parent_union_mass(atoms: tuple[Atom, ...], parents: tuple[Parent, ...]) -> Fraction:
    """Sum each source atom once when any closed parent contains it."""

    if not parents:
        raise ParentUnionError("parent union is empty")
    for left, bottom, right, top in parents:
        if not (left < right and bottom < top):
            raise ParentUnionError("parent has nonpositive area")
        if not (0 <= left <= right <= OUTER_SIDE and 0 <= bottom <= top <= OUTER_SIDE):
            raise ParentUnionError("parent is outside container")
        if right - left != 1 or top - bottom != 1:
            raise ParentUnionError("parent is not a unit square")
    return sum(
        (
            weight
            for (x, y), weight in atoms
            if any(
                left <= x <= right and bottom <= y <= top
                for left, bottom, right, top in parents
            )
        ),
        Fraction(),
    )


def literal_q0_mass(repository: Path) -> tuple[int, BoundMeasure]:
    """Return the exact integer W*mu(Q0), with the source and reader revisions."""

    measure = load_bound_measure(repository)
    scaled = WEIGHT_SCALE * parent_union_mass(measure.atoms, (Q0,))
    if scaled.denominator != 1:
        raise ParentUnionError("literal parent mass is not integral at source scale")
    return scaled.numerator, measure
