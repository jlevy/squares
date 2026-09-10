"""Self-contained exact polygon-union audit for the frozen five-dot proposal.

The implementation deliberately imports no project geometry.  It reads the rational
proposal, reconstructs the direction manifest, builds collision polygons in physical
coordinates, and measures their union by exact inclusion-exclusion.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import subprocess
import tempfile
import time
from dataclasses import dataclass
from fractions import Fraction
from functools import cmp_to_key
from itertools import pairwise
from pathlib import Path
from typing import cast

type Point = tuple[Fraction, Fraction]
type Polygon = tuple[Point, ...]

EXPECTED_SCHEMA = "owner-footprint-cover/v1"
EXPECTED_CLASS = "bottom-left:m1:j0"
EXPECTED_OUTER_SIDE = Fraction(96, 25)
EXPECTED_CORE_SIDE = Fraction(9977, 10000)
EXPECTED_DIRECTION_COUNT = 361


class AuditError(ValueError):
    """A source, geometry, or execution guard refused the audit."""


class DeadlineError(AuditError):
    """The exact union computation exceeded its declared deadline."""


@dataclass(frozen=True, slots=True)
class Direction:
    """One exact counterclockwise rotation in physical coordinates."""

    label: str
    cosine: Fraction
    sine: Fraction

    def __post_init__(self) -> None:
        if self.cosine * self.cosine + self.sine * self.sine != 1:
            raise AuditError("direction is not exactly unit length")


@dataclass(frozen=True, slots=True)
class DirectionSource:
    """One folded-net source of a canonical square axis."""

    folded_index: int
    reflected: bool


@dataclass(frozen=True, slots=True)
class ManifestEntry:
    """One canonical direction and its folded-net provenance."""

    index: int
    direction: Direction
    sources: tuple[DirectionSource, ...]


@dataclass(frozen=True, slots=True)
class FrozenInput:
    """The independently parsed rational input premise."""

    source_path: str
    git_commit: str
    git_blob: str
    outer_side: Fraction
    core_side: Fraction
    angle_limit: Fraction
    direction_steps: int
    footprints: tuple[Polygon, ...]
    dots: tuple[Point, ...]
    common_weight: Fraction
    total_mass: Fraction
    directions: tuple[Direction, ...]


@dataclass(frozen=True, slots=True)
class UnionMeasure:
    """Exact area of a finite convex-polygon union inside a container."""

    covered_area: Fraction
    container_area: Fraction
    nonempty_subsets: int

    @property
    def uncovered_area(self) -> Fraction:
        return self.container_area - self.covered_area


def _git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ("git", *args), cwd=root, check=False, capture_output=True, text=True
    )
    if result.returncode != 0:
        raise AuditError(result.stderr.strip() or f"git {' '.join(args)} failed")
    return result.stdout.strip()


def bind_clean_tracked_source(path: Path, expected_blob: str) -> tuple[Path, str, str, str]:
    """Bind working bytes to one clean tracked Git blob."""

    if len(expected_blob) != 40 or any(
        char not in "0123456789abcdef" for char in expected_blob
    ):
        raise AuditError("expected source blob must be a lowercase 40-digit Git object id")
    resolved = path.resolve()
    root_text = _git(Path.cwd(), "rev-parse", "--show-toplevel")
    root = Path(root_text).resolve()
    try:
        relative = resolved.relative_to(root).as_posix()
    except ValueError as error:
        raise AuditError("source receipt is outside the Git repository") from error
    _git(root, "ls-files", "--error-unmatch", "--", relative)
    if _git(root, "status", "--porcelain", "--", relative):
        raise AuditError("source receipt has modified or staged bytes")
    blob = _git(root, "hash-object", "--", relative)
    if blob != expected_blob:
        raise AuditError(f"source blob {blob} does not match expected {expected_blob}")
    return root, relative, _git(root, "rev-parse", "HEAD"), blob


def _mapping(value: object, label: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise AuditError(f"{label} must be an object")
    return cast(dict[str, object], value)


def _sequence(value: object, label: str) -> list[object]:
    if not isinstance(value, list):
        raise AuditError(f"{label} must be an array")
    return cast(list[object], value)


def _fraction(value: object, label: str) -> Fraction:
    if not isinstance(value, (str, int)) or isinstance(value, bool):
        raise AuditError(f"{label} must be an exact rational string")
    try:
        return Fraction(value)
    except (ValueError, ZeroDivisionError) as error:
        raise AuditError(f"{label} is not an exact rational") from error


def _integer(value: object, label: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise AuditError(f"{label} must be an integer")
    return value


def _point(value: object, label: str) -> Point:
    raw = _sequence(value, label)
    if len(raw) != 2:
        raise AuditError(f"{label} must have two coordinates")
    return _fraction(raw[0], f"{label}.x"), _fraction(raw[1], f"{label}.y")


def _subtract(left: Point, right: Point) -> Point:
    return left[0] - right[0], left[1] - right[1]


def _cross(left: Point, right: Point) -> Fraction:
    return left[0] * right[1] - left[1] * right[0]


def polygon_area_twice(polygon: Polygon) -> Fraction:
    """Return the signed doubled area of a polygon."""

    return sum(
        (
            first[0] * second[1] - first[1] * second[0]
            for first, second in pairwise(polygon + polygon[:1])
        ),
        start=Fraction(0),
    )


def polygon_area(polygon: Polygon) -> Fraction:
    """Return exact unsigned polygon area."""

    return abs(polygon_area_twice(polygon)) / 2


def convex_hull(points: tuple[Point, ...]) -> Polygon:
    """Return a counterclockwise exact hull without collinear vertices."""

    ordered = sorted(set(points))
    if len(ordered) <= 1:
        return tuple(ordered)

    def half(sequence: list[Point]) -> list[Point]:
        result: list[Point] = []
        for point in sequence:
            while (
                len(result) >= 2
                and _cross(_subtract(result[-1], result[-2]), _subtract(point, result[-1])) <= 0
            ):
                result.pop()
            result.append(point)
        return result

    return tuple(half(ordered)[:-1] + half(list(reversed(ordered)))[:-1])


def _clip_half_plane(polygon: Polygon, start: Point, end: Point) -> Polygon:
    if not polygon:
        return ()
    edge = _subtract(end, start)

    def signed(point: Point) -> Fraction:
        return _cross(edge, _subtract(point, start))

    output: list[Point] = []
    previous = polygon[-1]
    previous_value = signed(previous)
    for current in polygon:
        current_value = signed(current)
        if (current_value >= 0) != (previous_value >= 0):
            factor = previous_value / (previous_value - current_value)
            output.append(
                (
                    previous[0] + factor * (current[0] - previous[0]),
                    previous[1] + factor * (current[1] - previous[1]),
                )
            )
        if current_value >= 0:
            output.append(current)
        previous, previous_value = current, current_value
    return convex_hull(tuple(output))


def convex_intersection(first: Polygon, second: Polygon) -> Polygon:
    """Intersect two counterclockwise convex polygons exactly."""

    if not first or not second:
        return ()
    if len(second) < 3 or polygon_area_twice(second) <= 0:
        raise AuditError("clipping polygon must be nondegenerate and counterclockwise")
    result = first
    for start, end in pairwise(second + second[:1]):
        result = _clip_half_plane(result, start, end)
        if len(result) < 3 or polygon_area_twice(result) == 0:
            return ()
    return result


def point_in_closed_convex_polygon(point: Point, polygon: Polygon) -> bool:
    """Test exact closed membership in a nondegenerate counterclockwise polygon."""

    return len(polygon) >= 3 and all(
        _cross(_subtract(end, start), _subtract(point, start)) >= 0
        for start, end in pairwise(polygon + polygon[:1])
    )


def _rotation_from_half_tangent(label: str, tangent: Fraction) -> Direction:
    denominator = 1 + tangent * tangent
    return Direction(label, (1 - tangent * tangent) / denominator, 2 * tangent / denominator)


def _canonical_axis(cosine: Fraction, sine: Fraction) -> Point:
    candidates = ((cosine, sine), (-sine, cosine), (-cosine, -sine), (sine, -cosine))
    matches = tuple(point for point in candidates if point[0] > 0 and point[1] >= 0)
    if len(matches) != 1:
        raise AuditError("could not canonicalize a square orientation")
    return matches[0]


def full_direction_manifest(angle_limit: Fraction, steps: int) -> tuple[ManifestEntry, ...]:
    """Independently reconstruct the canonical rational direction net."""

    if angle_limit <= 0 or steps < 1:
        raise AuditError("direction net parameters must be positive")
    sources: dict[Point, list[DirectionSource]] = {}
    for folded_index in range(steps + 1):
        tangent = angle_limit * folded_index / steps
        base = _rotation_from_half_tangent(str(folded_index), tangent)
        for cosine, sine, reflected in (
            (base.cosine, base.sine, False),
            (base.sine, base.cosine, True),
        ):
            axis = _canonical_axis(cosine, sine)
            sources.setdefault(axis, []).append(DirectionSource(folded_index, reflected))

    def compare(left: Point, right: Point) -> int:
        cross = _cross(left, right)
        if cross > 0:
            return -1
        if cross < 0:
            return 1
        return (left > right) - (left < right)

    axes = sorted(sources, key=cmp_to_key(compare))
    return tuple(
        ManifestEntry(
            index,
            Direction(f"owner-{index:03d}", cosine, sine),
            tuple(sources[(cosine, sine)]),
        )
        for index, (cosine, sine) in enumerate(axes)
    )


def _manifest_record(entry: ManifestEntry) -> dict[str, object]:
    return {
        "label": entry.direction.label,
        "ux": str(entry.direction.cosine),
        "uy": str(entry.direction.sine),
        "sources": [
            {"folded_index": source.folded_index, "reflected": source.reflected}
            for source in entry.sources
        ],
    }


def _parse_frozen_receipt(
    document: object, source_path: str, git_commit: str, git_blob: str
) -> FrozenInput:
    receipt = _mapping(document, "receipt")
    if receipt.get("schema") != EXPECTED_SCHEMA or receipt.get("status") != "complete":
        raise AuditError("source receipt must be a complete owner-footprint-cover/v1 record")
    settings = _mapping(receipt.get("settings"), "settings")
    outer_side = _fraction(settings.get("outer_side"), "settings.outer_side")
    core_side = _fraction(settings.get("square_side"), "settings.square_side")
    if (outer_side, core_side) != (EXPECTED_OUTER_SIDE, EXPECTED_CORE_SIDE):
        raise AuditError("source changes the frozen outer or core side")
    if settings.get("owner_count") != 4 or settings.get("residual_square_count") != 7:
        raise AuditError("source is not the frozen four-owner branch")
    if settings.get("owner_footprints_derived_from_full_manifest") is not True:
        raise AuditError("source footprints are not declared from the full manifest")
    selected = tuple(
        _integer(value, "folded index")
        for value in _sequence(settings.get("folded_source_indices"), "folded indices")
    )
    if not selected or selected != tuple(sorted(set(selected))) or selected[0] != 0:
        raise AuditError("folded source indices must be sorted, unique, and start at zero")
    steps = selected[-1]
    provenance = _sequence(receipt.get("direction_provenance"), "direction provenance")
    endpoint: dict[str, object] | None = None
    for raw in provenance:
        record = _mapping(raw, "direction record")
        for raw_source in _sequence(record.get("sources"), "direction sources"):
            source = _mapping(raw_source, "direction source")
            if source.get("folded_index") == steps and source.get("reflected") is False:
                endpoint = record
    if endpoint is None:
        raise AuditError("direction provenance does not expose the final base direction")
    endpoint_cosine = _fraction(endpoint.get("ux"), "endpoint.ux")
    endpoint_sine = _fraction(endpoint.get("uy"), "endpoint.uy")
    angle_limit = endpoint_sine / (1 + endpoint_cosine)
    manifest = full_direction_manifest(angle_limit, steps)
    if len(manifest) != EXPECTED_DIRECTION_COUNT:
        raise AuditError("independent direction reconstruction did not produce 361 axes")
    expected_provenance = [
        _manifest_record(entry)
        for entry in manifest
        if any(source.folded_index in selected for source in entry.sources)
    ]
    if provenance != expected_provenance:
        raise AuditError(
            "serialized direction provenance disagrees with independent reconstruction"
        )
    if settings.get("full_owner_orientation_count") != len(manifest):
        raise AuditError("serialized full direction count disagrees with reconstruction")
    if settings.get("selected_canonical_directions") != len(provenance):
        raise AuditError("serialized selected direction count disagrees with provenance")

    class_record = _mapping(receipt.get("class"), "class")
    if class_record.get("id") != EXPECTED_CLASS or class_record.get("owner_count") != 4:
        raise AuditError("source changes the frozen owner class")
    if (
        class_record.get("mark_id") not in (None, "m1")
        or class_record.get("sector") not in (None, 0)
        or class_record.get("reflected_class_id") not in (None, "bottom-left:m2:j7")
    ):
        raise AuditError("source changes the frozen owner class metadata")
    if class_record.get("four_owner_map") != "(x,y),(q-x,y),(x,q-y),(q-x,q-y)":
        raise AuditError("source changes the four-owner reflection map")
    mark = _point(class_record.get("mark"), "class.mark")

    endpoint_arm = _mapping(_mapping(receipt.get("arms"), "arms").get("endpoint"), "endpoint")
    if endpoint_arm.get("footprint") is not None:
        raise AuditError("four-owner endpoint arm must use only footprint_union")
    raw_footprints = _sequence(endpoint_arm.get("footprint_union"), "endpoint footprints")
    if len(raw_footprints) != 4:
        raise AuditError("source must contain exactly four endpoint footprints")
    footprints: list[Polygon] = []
    for index, raw_polygon in enumerate(raw_footprints):
        polygon = tuple(
            _point(value, f"footprint {index} point")
            for value in _sequence(raw_polygon, f"footprint {index}")
        )
        hull = convex_hull(polygon)
        if polygon != hull or len(hull) < 3 or polygon_area_twice(hull) <= 0:
            raise AuditError(f"footprint {index} is not a normalized convex polygon")
        if any(not (0 <= x <= outer_side and 0 <= y <= outer_side) for x, y in hull):
            raise AuditError(f"footprint {index} leaves the container")
        footprints.append(hull)
    base = footprints[0]
    reflected = (
        base,
        convex_hull(tuple((outer_side - x, y) for x, y in base)),
        convex_hull(tuple((x, outer_side - y) for x, y in base)),
        convex_hull(tuple((outer_side - x, outer_side - y) for x, y in base)),
    )
    if tuple(footprints) != reflected or mark not in base:
        raise AuditError("serialized footprint union disagrees with the declared reflections")

    proposal = _mapping(endpoint_arm.get("proposal"), "endpoint proposal")
    if proposal.get("converged") is not True:
        raise AuditError("endpoint proposal is not complete")
    raw_atoms = _sequence(proposal.get("rationalised_atoms"), "endpoint atoms")
    if len(raw_atoms) != 5:
        raise AuditError("source must contain exactly five endpoint atoms")
    dots: list[Point] = []
    weights: list[Fraction] = []
    for index, raw_atom in enumerate(raw_atoms):
        atom = _sequence(raw_atom, f"atom {index}")
        if len(atom) != 3:
            raise AuditError(f"atom {index} must contain x, y, and weight")
        dots.append((_fraction(atom[0], "atom.x"), _fraction(atom[1], "atom.y")))
        weights.append(_fraction(atom[2], "atom.weight"))
    if len(set(dots)) != 5:
        raise AuditError("five-dot proposal contains duplicate positions")
    if len(set(weights)) != 1 or weights[0] <= 0:
        raise AuditError("five-dot proposal must have one positive common weight")
    total = sum(weights, start=Fraction(0))
    if total != _fraction(proposal.get("rationalised_total_mass"), "total mass"):
        raise AuditError("serialized total mass disagrees with the five weights")
    if any(not (0 <= x <= outer_side and 0 <= y <= outer_side) for x, y in dots):
        raise AuditError("a dot leaves the container")
    if any(point_in_closed_convex_polygon(dot, patch) for dot in dots for patch in footprints):
        raise AuditError("a dot lies in the closed owner-footprint union")
    return FrozenInput(
        source_path,
        git_commit,
        git_blob,
        outer_side,
        core_side,
        angle_limit,
        steps,
        tuple(footprints),
        tuple(dots),
        weights[0],
        total,
        tuple(entry.direction for entry in manifest),
    )


def load_frozen_input(path: Path, expected_blob: str) -> FrozenInput:
    """Load and independently validate the clean frozen receipt."""

    _, relative, commit, blob = bind_clean_tracked_source(path, expected_blob)
    try:
        document = cast(object, json.loads(path.read_text(encoding="utf-8")))
    except (OSError, json.JSONDecodeError) as error:
        raise AuditError(f"could not read source receipt: {error}") from error
    return _parse_frozen_receipt(document, relative, commit, blob)


def container_rectangle(
    outer_side: Fraction, core_side: Fraction, direction: Direction
) -> Polygon:
    """Build the physical rectangle of contained core centres."""

    extent = core_side * (abs(direction.cosine) + abs(direction.sine)) / 2
    low, high = extent, outer_side - extent
    if low >= high:
        raise AuditError("core has no full-dimensional contained-centre rectangle")
    return ((low, low), (high, low), (high, high), (low, high))


def core_offsets(core_side: Fraction, direction: Direction) -> Polygon:
    """Build the four physical vertices of a centred oriented core."""

    half = core_side / 2
    u = (half * direction.cosine, half * direction.sine)
    v = (-half * direction.sine, half * direction.cosine)
    return convex_hull(
        tuple(
            (sx * u[0] + sy * v[0], sx * u[1] + sy * v[1]) for sx in (-1, 1) for sy in (-1, 1)
        )
    )


def collision_polygon(footprint: Polygon, offsets: Polygon) -> Polygon:
    """Build centres whose closed oriented core meets a closed footprint."""

    return convex_hull(tuple((x + dx, y + dy) for x, y in footprint for dx, dy in offsets))


def exact_union_area(
    container: Polygon,
    polygons: tuple[Polygon, ...],
    *,
    max_subsets: int,
    deadline: float | None = None,
) -> UnionMeasure:
    """Measure a convex-polygon union by exact inclusion-exclusion."""

    subset_count = (1 << len(polygons)) - 1
    if not polygons or subset_count > max_subsets:
        raise AuditError("polygon subset count exceeds the declared guard")
    if len(container) < 3 or polygon_area_twice(container) <= 0:
        raise AuditError("union container must be nondegenerate and counterclockwise")
    intersections: list[Polygon] = [()] * (subset_count + 1)
    covered = Fraction(0)
    nonempty = 0
    for mask in range(1, subset_count + 1):
        if deadline is not None and time.perf_counter() >= deadline:
            raise DeadlineError("exact union deadline reached")
        bit = mask & -mask
        polygon_index = bit.bit_length() - 1
        parent = mask ^ bit
        intersection = convex_intersection(
            container if parent == 0 else intersections[parent], polygons[polygon_index]
        )
        intersections[mask] = intersection
        if not intersection:
            continue
        area = polygon_area(intersection)
        if area == 0:
            intersections[mask] = ()
            continue
        nonempty += 1
        covered += area if mask.bit_count() % 2 else -area
    container_area = polygon_area(container)
    if not 0 <= covered <= container_area:
        raise AuditError("inclusion-exclusion produced an impossible union area")
    return UnionMeasure(covered, container_area, nonempty)


def measure_direction(
    source: FrozenInput, direction: Direction, *, max_subsets: int, deadline: float | None
) -> UnionMeasure:
    """Measure the nine collision polygons for one exact direction."""

    container = container_rectangle(source.outer_side, source.core_side, direction)
    offsets = core_offsets(source.core_side, direction)
    obstacles = tuple(collision_polygon(patch, offsets) for patch in source.footprints) + tuple(
        collision_polygon((dot,), offsets) for dot in source.dots
    )
    return exact_union_area(container, obstacles, max_subsets=max_subsets, deadline=deadline)


def _square_axis_key(direction: Direction) -> Point:
    """Canonicalize a square direction modulo quarter turns."""

    cosine, sine = direction.cosine, direction.sine
    return min(
        (
            (cosine, sine),
            (-sine, cosine),
            (-cosine, -sine),
            (sine, -cosine),
        )
    )


def atomic_write_json(path: Path, document: dict[str, object]) -> None:
    """Replace one JSON checkpoint atomically."""

    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            json.dump(document, stream, indent=1)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        Path(temporary).replace(path)
    except BaseException:
        Path(temporary).unlink(missing_ok=True)
        raise


def validate_output_path(output: Path, source: Path, repository: Path) -> Path:
    """Refuse any output that could overwrite an input or project source."""

    resolved = output.resolve()
    protected_directory = Path(__file__).resolve().parent
    tests_directory = repository / "packing" / "tests"
    if resolved == source.resolve() or resolved.is_relative_to(protected_directory):
        raise AuditError("output may not overwrite the input or checker source")
    if resolved.is_relative_to(tests_directory) or resolved.suffix != ".json":
        raise AuditError("output must be a JSON record outside project code and tests")
    if resolved.exists():
        raise AuditError("output path must be fresh; this audit does not resume or overwrite")
    return resolved


def run_full_net(
    source: FrozenInput, *, max_subsets: int, deadline_seconds: float, output: Path
) -> dict[str, object]:
    """Check all directions, stopping on a positive-area gap or deadline."""

    if len(source.directions) != EXPECTED_DIRECTION_COUNT or len(
        {_square_axis_key(item) for item in source.directions}
    ) != len(source.directions):
        raise AuditError("full-net driver requires 361 unique directions modulo quarter turns")
    if len(source.footprints) != 4 or len(source.dots) != 5 or max_subsets < 511:
        raise AuditError("full-net driver requires four patches, five dots, and 511 subsets")
    started = time.perf_counter()
    deadline = started + deadline_seconds
    result: dict[str, object] = {
        "schema": "independent-five-dot-union/v1",
        "status": "running",
        "outcome": "unresolved",
        "source": {
            "path": source.source_path,
            "git_commit": source.git_commit,
            "git_blob": source.git_blob,
        },
        "method": "self-contained exact convex clipping and inclusion-exclusion",
        "claim_limit": "finite-net five-dot coverage only; no LP minimum or optimum claim",
        "settings": {
            "outer_side": str(source.outer_side),
            "core_side": str(source.core_side),
            "angle_limit": str(source.angle_limit),
            "direction_steps": source.direction_steps,
            "direction_count": len(source.directions),
            "owner_footprints": len(source.footprints),
            "dots": len(source.dots),
            "common_weight": str(source.common_weight),
            "total_mass": str(source.total_mass),
            "max_subsets_per_direction": max_subsets,
            "deadline_seconds": deadline_seconds,
        },
        "directions": [],
        "summary": None,
    }
    atomic_write_json(output, result)
    records = cast(list[object], result["directions"])
    maximum_nonempty = 0
    try:
        for index, direction in enumerate(source.directions):
            if time.perf_counter() >= deadline:
                raise DeadlineError("full-net deadline reached")
            direction_started = time.perf_counter()
            measure = measure_direction(
                source, direction, max_subsets=max_subsets, deadline=deadline
            )
            maximum_nonempty = max(maximum_nonempty, measure.nonempty_subsets)
            records.append(
                {
                    "index": index,
                    "label": direction.label,
                    "container_area": str(measure.container_area),
                    "covered_area": str(measure.covered_area),
                    "uncovered_area": str(measure.uncovered_area),
                    "nonempty_subsets": measure.nonempty_subsets,
                    "wall_seconds": time.perf_counter() - direction_started,
                }
            )
            if measure.uncovered_area > 0:
                result["status"] = "complete"
                result["outcome"] = "uncovered"
                break
            atomic_write_json(output, result)
        else:
            result["status"] = "complete"
            result["outcome"] = "covered"
    except AuditError as error:
        result["status"] = "partial"
        result["outcome"] = "unresolved"
        result["error"] = str(error)
    result["summary"] = {
        "checked_directions": len(records),
        "expected_directions": len(source.directions),
        "all_covered": result["outcome"] == "covered",
        "maximum_nonempty_subsets": maximum_nonempty,
    }
    result["wall_seconds"] = time.perf_counter() - started
    atomic_write_json(output, result)
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("receipt", type=Path)
    parser.add_argument("--expect-receipt-blob", required=True)
    parser.add_argument("--expect-directions", type=int, default=EXPECTED_DIRECTION_COUNT)
    parser.add_argument("--max-subsets-per-direction", type=int, default=511)
    parser.add_argument("--deadline-seconds", type=float, default=240)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    started = time.perf_counter()
    output: Path | None = None
    try:
        repository_text = _git(Path.cwd(), "rev-parse", "--show-toplevel")
        repository = Path(repository_text).resolve()
        output = validate_output_path(args.output, args.receipt, repository)
        if args.expect_directions != EXPECTED_DIRECTION_COUNT:
            raise AuditError("this frozen audit requires exactly 361 directions")  # noqa: TRY301
        if (
            args.max_subsets_per_direction < 511
            or not math.isfinite(args.deadline_seconds)
            or args.deadline_seconds <= 0
        ):
            raise AuditError(  # noqa: TRY301
                "execution guards are below the frozen audit requirements"
            )
        source = load_frozen_input(args.receipt, args.expect_receipt_blob)
        if len(source.directions) != args.expect_directions:
            raise AuditError(  # noqa: TRY301
                "loaded direction count disagrees with the command guard"
            )
        result = run_full_net(
            source,
            max_subsets=args.max_subsets_per_direction,
            deadline_seconds=args.deadline_seconds,
            output=output,
        )
    except (AuditError, OSError, json.JSONDecodeError) as error:
        result = {
            "schema": "independent-five-dot-union/v1",
            "status": "partial",
            "outcome": "unresolved",
            "error": str(error),
            "wall_seconds": time.perf_counter() - started,
        }
        if output is not None:
            atomic_write_json(output, result)
    print(json.dumps(result, indent=1), flush=True)
    return 0 if result.get("status") == "complete" else 2


if __name__ == "__main__":
    raise SystemExit(main())
