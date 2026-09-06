"""Bounded BC-230 adaptive JSON input and pure folded-cover validators.

Loading validates the closed schema and the pre-coverage premises. It does not
check Condition 5, trust the declared minimum, or produce a retention verdict.
The scalar loader and retained source bytes are outside this module's scope.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from fractions import Fraction
from itertools import pairwise
from pathlib import Path
from typing import Never, cast

from sqpack.fractional.adaptive import AdaptiveCertificate, AngleCell
from sqpack.fractional.model import Atom

MAX_CERTIFICATE_BYTES = 8_388_608
MAX_ATOMS = 4_096
MAX_ANGLE_CELLS = 10_001
MAX_RATIONAL_TEXT = 512
RATIONAL = re.compile(r"-?(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?")
TOP_FIELDS = frozenset(
    {
        "id",
        "variant",
        "n",
        "claim",
        "outer_side",
        "symmetry",
        "containment_rule",
        "seam_owner",
        "angle_cells",
        "total_mass",
        "least_cell_mass",
        "atoms",
    }
)
CELL_FIELDS = frozenset(
    {
        "index",
        "half_tangent",
        "lower_boundary_tangent",
        "upper_boundary_tangent",
        "max_mismatch_tangent",
        "square_side",
    }
)
type ClosedCover = tuple[tuple[Fraction, Fraction], ...]


class AdaptiveFormatError(ValueError):
    """An adaptive input fails the closed contract before coverage is attempted."""


@dataclass(frozen=True, slots=True)
class AdaptiveInput:
    """Parsed control input; the declared minimum has not been verified.

    Atom coordinates are container coordinates (x, y). Angle-cell boundaries
    are folded-angle tangents, not center-space event-cell coordinates.
    """

    certificate: AdaptiveCertificate
    identifier: str
    claim: str
    declared_total_mass: Fraction
    declared_least_cell_mass: Fraction | None


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise AdaptiveFormatError(f"duplicate JSON object key {key!r}")
        result[key] = value
    return result


def _reject_number(value: str) -> Never:
    raise AdaptiveFormatError(f"inexact JSON number {value!r}; use an exact rational string")


def _object(value: object, fields: frozenset[str], location: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise AdaptiveFormatError(f"{location} must be an object")
    record = cast(dict[str, object], value)
    missing = fields - record.keys()
    if missing:
        raise AdaptiveFormatError(f"{location} missing required field {min(missing)!r}")
    unknown = record.keys() - fields
    if unknown:
        raise AdaptiveFormatError(f"{location} has unknown field {min(unknown)!r}")
    return record


def _array(value: object, location: str) -> list[object]:
    if not isinstance(value, list):
        raise AdaptiveFormatError(f"{location} must be an array")
    return cast(list[object], value)


def _integer(value: object, location: str) -> int:
    if type(value) is not int:
        raise AdaptiveFormatError(f"{location} must be a JSON integer")
    return cast(int, value)


def _string(value: object, location: str) -> str:
    if not isinstance(value, str):
        raise AdaptiveFormatError(f"{location} must be a string")
    return value


def _rational(value: object, location: str) -> Fraction:
    if not isinstance(value, str):
        raise AdaptiveFormatError(f"{location} must be an exact rational string")
    if len(value) > MAX_RATIONAL_TEXT:
        raise AdaptiveFormatError(f"{location} exceeds the {MAX_RATIONAL_TEXT}-character limit")
    if RATIONAL.fullmatch(value) is None:
        raise AdaptiveFormatError(f"{location} must be a canonical rational string")
    result = Fraction(value)
    if str(result) != value:
        raise AdaptiveFormatError(f"{location} must be a canonical rational string")
    return result


def validate_endpoints(closures: ClosedCover) -> None:
    """Check the axis and fold endpoints without JSON or declaration validation."""
    if not closures:
        raise AdaptiveFormatError("the closed cover needs at least one interval")
    if any(not isinstance(endpoint, Fraction) for pair in closures for endpoint in pair):
        raise AdaptiveFormatError("closed-cover endpoints must be exact Fractions")
    if closures[0][0] != 0:
        raise AdaptiveFormatError("closed-cover axis endpoint must be zero")
    if closures[-1][1] != 1:
        raise AdaptiveFormatError("closed-cover fold endpoint must be one")


def validate_closed_cover(closures: ClosedCover) -> None:
    """Check exact positive-width closures that meet only at neighboring seams.

    This deliberately accepts closures directly: the F4 gap/overlap controls must
    reach this branch without first failing a serialized declaration comparison.
    """
    validate_endpoints(closures)
    for index, (lower, upper) in enumerate(closures):
        if lower >= upper:
            raise AdaptiveFormatError(f"closed-cover interval {index} needs positive width")
    for index, (left, right) in enumerate(pairwise(closures)):
        if left[1] < right[0]:
            raise AdaptiveFormatError(f"closed-cover gap after angle cell {index}")
        if left[1] > right[0]:
            raise AdaptiveFormatError(f"closed-cover overlap after angle cell {index}")


def validate_angle_declarations(cells: tuple[AngleCell, ...]) -> None:
    """Compare derived fields before testing the complete folded cover.

    Unlike the in-memory constructor, this input check separates declaration
    equality from final-seam validity. F5 must reach the latter with all dependent
    declarations recomputed, while a stale field must still take the F3 branch.
    This is a parser check, not the independent interval or standalone route.
    """
    if len(cells) < 2:
        raise AdaptiveFormatError("angle_cells needs at least two angle cells")
    if any(type(cell.index) is not int or cell.index != i for i, cell in enumerate(cells)):
        raise AdaptiveFormatError("angle-cell indices must be contiguous from zero")
    tangents = tuple(cell.half_tangent for cell in cells)
    if tangents[0] != 0 or any(t < 0 or t >= 1 for t in tangents):
        raise AdaptiveFormatError("half-tangents must start at zero and lie in [0, 1)")
    if any(left >= right for left, right in pairwise(tangents)):
        raise AdaptiveFormatError("half-tangents must be strictly increasing")
    previous, final = tangents[-2:]
    if previous * previous + 2 * previous - 1 >= 0 or final * final + 2 * final - 1 < 0:
        raise AdaptiveFormatError("final directions must bracket the folded endpoint")
    seams = (
        Fraction(0),
        *((left + right) / (1 - left * right) for left, right in pairwise(tangents)),
        Fraction(1),
    )
    for index, cell in enumerate(cells):
        lower, upper = seams[index : index + 2]
        if (cell.lower_boundary_tangent, cell.upper_boundary_tangent) != (lower, upper):
            raise AdaptiveFormatError(f"angle cell {index} differs from its derived boundary")
        tangent = cell.half_tangent
        direction_tangent = 2 * tangent / (1 - tangent * tangent)
        mismatch = max(
            abs(direction_tangent - q) / (1 + direction_tangent * q) for q in (lower, upper)
        )
        if cell.max_mismatch_tangent != mismatch:
            raise AdaptiveFormatError(f"angle cell {index} differs from its derived mismatch")
    if seams[-2] >= 1:
        raise AdaptiveFormatError("final seam q_K >= 1 lies at or beyond the folded endpoint")
    validate_closed_cover(tuple(pairwise(seams)))


def _structures(
    record: dict[str, object],
) -> tuple[list[dict[str, object]], list[list[object]]]:
    raw_cells = _array(record["angle_cells"], "angle_cells")
    raw_atoms = _array(record["atoms"], "atoms")
    if len(raw_cells) > MAX_ANGLE_CELLS:
        raise AdaptiveFormatError(f"angle_cells exceeds the {MAX_ANGLE_CELLS}-cell limit")
    if len(raw_atoms) > MAX_ATOMS:
        raise AdaptiveFormatError(f"atoms exceeds the {MAX_ATOMS}-atom limit")
    if len(raw_cells) < 2:
        raise AdaptiveFormatError("angle_cells needs at least two angle cells")
    cells = [
        _object(cell, CELL_FIELDS, f"angle_cells[{i}]") for i, cell in enumerate(raw_cells)
    ]
    atoms = [_array(atom, f"atoms[{i}]") for i, atom in enumerate(raw_atoms)]
    for index, atom in enumerate(atoms):
        if len(atom) != 3:
            raise AdaptiveFormatError(f"atoms[{index}] must contain exactly three entries")
    return cells, atoms


def _angle_cell(record: dict[str, object], index: int) -> AngleCell:
    location = f"angle_cells[{index}]"
    return AngleCell(
        _integer(record["index"], f"{location}.index"),
        _rational(record["half_tangent"], f"{location}.half_tangent"),
        _rational(record["lower_boundary_tangent"], f"{location}.lower_boundary_tangent"),
        _rational(record["upper_boundary_tangent"], f"{location}.upper_boundary_tangent"),
        _rational(record["max_mismatch_tangent"], f"{location}.max_mismatch_tangent"),
        _rational(record["square_side"], f"{location}.square_side"),
    )


def load_bytes(data: bytes) -> AdaptiveInput:
    """Load one bounded byte string, without coverage, rereads, or acceptance."""
    if len(data) > MAX_CERTIFICATE_BYTES:
        raise AdaptiveFormatError(f"input exceeds the {MAX_CERTIFICATE_BYTES}-byte limit")
    try:
        decoded = cast(
            object,
            json.loads(
                data,
                object_pairs_hook=_unique_object,
                parse_float=_reject_number,
                parse_constant=_reject_number,
            ),
        )
    except AdaptiveFormatError:
        raise
    except (UnicodeError, ValueError, RecursionError) as error:
        raise AdaptiveFormatError(f"invalid JSON: {error}") from None
    record = _object(decoded, TOP_FIELDS, "top-level JSON")
    raw_cells, raw_atoms = _structures(record)
    identifier = _string(record["id"], "id")
    claim = _string(record["claim"], "claim")
    for field, expected in (
        ("variant", "adaptive-unconditional"),
        ("symmetry", "D4"),
        ("containment_rule", "legacy-linear-v1"),
        ("seam_owner", "lower-index"),
    ):
        if _string(record[field], field) != expected:
            raise AdaptiveFormatError(f"{field} must equal {expected!r}")
    n = _integer(record["n"], "n")
    outer = _rational(record["outer_side"], "outer_side")
    if n <= 0 or outer <= 0:
        raise AdaptiveFormatError("n and outer_side must be positive")
    total = _rational(record["total_mass"], "total_mass")
    minimum = (
        None
        if record["least_cell_mass"] is None
        else _rational(record["least_cell_mass"], "least_cell_mass")
    )
    cells = tuple(_angle_cell(cell, index) for index, cell in enumerate(raw_cells))
    atoms = tuple(
        Atom(
            str(index),
            _rational(row[0], f"atoms[{index}].x"),
            _rational(row[1], f"atoms[{index}].y"),
            _rational(row[2], f"atoms[{index}].weight"),
        )
        for index, row in enumerate(raw_atoms)
    )
    validate_angle_declarations(cells)
    try:
        certificate = AdaptiveCertificate(n, outer, atoms, cells)
    except ValueError as error:
        raise AdaptiveFormatError(str(error)) from None
    if total != certificate.total_mass:
        raise AdaptiveFormatError("declared total_mass differs from the exact atom sum")
    if claim != f"s({n}) >= {outer}":
        raise AdaptiveFormatError(
            "claim differs from the theorem conclusion for n and outer_side"
        )
    return AdaptiveInput(certificate, identifier, claim, total, minimum)


def load(path: Path) -> AdaptiveInput:
    """Read at most the byte limit plus one; this is not a frozen-byte retention API."""
    with path.open("rb") as stream:
        data = stream.read(MAX_CERTIFICATE_BYTES + 1)
    return load_bytes(data)
