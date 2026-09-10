#!/usr/bin/env python3
"""Screen a retained depth-one square family against exact owner footprints.

This deletion-only instrument translates an immutable source family, checks literal
membership in the full canonical owner direction family, and retains only placements
with a positive exact separating-axis gap from a selected footprint.  It does not solve
an LP or re-establish depth: deleting nonnegative source members inherits the source's
all-point depth-one bound.
"""

from __future__ import annotations

import argparse
import gzip
import json
import subprocess
import sys
import tempfile
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from fractions import Fraction
from itertools import product
from math import lcm
from pathlib import Path
from typing import Any

from devtools.owner_footprints import (
    ENDPOINT_FOOTPRINT_STATUS,
    SOURCE_CONTRACTS,
    OwnerClass,
    endpoint_footprint,
    owner_branch_manifest,
    triangle_footprint,
)
from devtools.transport_ceiling_family import transport
from sqpack.cover import write_text_atomic
from sqpack.fractional.ceiling import CeilingCertificate, Placement

type Point = tuple[Fraction, Fraction]
type Polygon = tuple[Point, ...]

REPO = Path(__file__).resolve().parents[2]
DEPTH_FAILURE = "K3 total weight at least n"
CORNER_NAMES = ("bottom-left", "bottom-right", "top-left", "top-right")
ONE_CORNER_THRESHOLD = Fraction(10)
FOUR_CORNER_THRESHOLD = Fraction(7)


@dataclass(frozen=True, slots=True)
class Separation:
    """One exact positive SAT gap; axis scaling is retained in the receipt."""

    axis: Point
    gap: Fraction


@dataclass(frozen=True, slots=True)
class Survivor:
    source_index: int
    weight: Fraction
    separation: Separation


@dataclass(frozen=True, slots=True)
class Screen:
    class_id: str
    corner: str
    kind: str
    polygon: Polygon
    mask: int
    survivors: tuple[Survivor, ...]

    @property
    def total_weight(self) -> Fraction:
        return sum((entry.weight for entry in self.survivors), Fraction(0))


def strict_separation(first: Polygon, second: Polygon) -> Separation | None:
    """Return a positive exact SAT gap, or ``None`` for contact or overlap."""

    if not first or not second:
        raise ValueError("strict-separation operands must be nonempty")
    best: Separation | None = None
    for polygon in (first, second):
        for start, end in zip(polygon, polygon[1:] + polygon[:1], strict=True):
            dx, dy = end[0] - start[0], end[1] - start[1]
            if dx == 0 and dy == 0:
                continue
            axis = (-dy, dx)
            left = tuple(axis[0] * x + axis[1] * y for x, y in first)
            right = tuple(axis[0] * x + axis[1] * y for x, y in second)
            gap = max(min(right) - max(left), min(left) - max(right))
            if gap > 0 and (best is None or gap > best.gap):
                best = Separation(axis, gap)
    return best


def _contained(placement: Placement, side: Fraction) -> bool:
    return all(0 <= x <= side and 0 <= y <= side for x, y in placement.corners())


def _orientation_axis(placement: Placement) -> Point:
    direction = placement.direction
    candidates = (
        (direction.ux, direction.uy),
        (direction.vx, direction.vy),
        (-direction.ux, -direction.uy),
        (-direction.vx, -direction.vy),
    )
    canonical = tuple((x, y) for x, y in candidates if x > 0 and y >= 0)
    if len(canonical) != 1:
        raise ValueError("source pose has no canonical orientation modulo quarter turns")
    return canonical[0]


def screen_footprint(
    family: CeilingCertificate,
    polygon: Polygon,
    *,
    class_id: str,
    corner: str,
    kind: str,
    source_placements: tuple[Placement, ...],
    direction_axes: frozenset[Point],
) -> Screen:
    """Filter one footprint with literal orientations and positive exact gaps."""

    if len(family.placements) != len(source_placements):
        raise ValueError("transport changed the source family cardinality")
    mask = 0
    survivors: list[Survivor] = []
    for index, (placement, source) in enumerate(
        zip(family.placements, source_placements, strict=True)
    ):
        if placement.side != family.square_side:
            raise ValueError(f"source placement {index} has the wrong square side")
        if _orientation_axis(placement) not in direction_axes:
            continue
        if not _contained(placement, family.outer_side):
            raise ValueError(f"translated source placement {index} leaves the container")
        if placement.weight != source.weight or placement.side != source.side:
            raise ValueError(f"transport altered source placement {index}")
        separation = strict_separation(placement.corners(), polygon)
        if separation is None:
            continue
        mask |= 1 << index
        survivors.append(Survivor(index, placement.weight, separation))
    return Screen(class_id, corner, kind, polygon, mask, tuple(survivors))


def verify_survivors(
    entries: Sequence[Mapping[str, object]], source: tuple[Placement, ...]
) -> tuple[int, Fraction]:
    """Replay source indices and weights; refuse duplicates and altered weights."""

    seen: set[int] = set()
    mask = 0
    total = Fraction(0)
    for offset, entry in enumerate(entries):
        index = entry.get("source_index")
        if type(index) is not int or not 0 <= index < len(source):
            raise ValueError(f"survivor {offset} has an invalid source index")
        if index in seen:
            raise ValueError(f"survivor {offset} repeats source index {index}")
        seen.add(index)
        weight = Fraction(str(entry.get("weight")))
        if weight != source[index].weight:
            raise ValueError(f"survivor {offset} altered source weight {index}")
        mask |= 1 << index
        total += weight
    return mask, total


def _corner_polygon(polygon: Polygon, corner: str, side: Fraction) -> Polygon:
    if corner == "bottom-left":
        return polygon
    if corner == "bottom-right":
        return tuple((side - x, y) for x, y in polygon)
    if corner == "top-left":
        return tuple((x, side - y) for x, y in polygon)
    if corner == "top-right":
        return tuple((side - x, side - y) for x, y in polygon)
    raise ValueError(f"unknown corner {corner}")


def _base_polygon(owner: OwnerClass, kind: str, directions: tuple[Any, ...]) -> Polygon:
    if kind == "point":
        return (owner.mark,)
    if kind == "triangle":
        return triangle_footprint(owner.mark, owner.sector)
    if kind == "endpoint":
        return endpoint_footprint(owner.mark, owner.sector, directions)
    raise ValueError(f"unknown footprint kind {kind}")


def _screen_record(screen: Screen, threshold: Fraction) -> dict[str, object]:
    survivors = [
        {
            "source_index": entry.source_index,
            "weight": str(entry.weight),
            "separating_axis": [str(value) for value in entry.separation.axis],
            "positive_projection_gap": str(entry.separation.gap),
        }
        for entry in screen.survivors
    ]
    return {
        "class_id": screen.class_id,
        "corner": screen.corner,
        "footprint_kind": screen.kind,
        "footprint": [[str(x), str(y)] for x, y in screen.polygon],
        "survivor_mask_hex": hex(screen.mask),
        "survivor_count": len(screen.survivors),
        "survivor_weight": str(screen.total_weight),
        "threshold": str(threshold),
        "obstructs": screen.total_weight >= threshold,
        "survivors": survivors,
    }


def summarize_records(
    records: list[dict[str, object]], *, class_field: str
) -> dict[str, object]:
    """Produce exact guarded extrema and verdict counts from emitted class rows."""

    if not records:
        raise ValueError("cannot summarize an empty class grid")
    weighted = [(Fraction(str(record["survivor_weight"])), record) for record in records]
    minimum = min(weight for weight, _ in weighted)
    maximum = max(weight for weight, _ in weighted)
    return {
        "class_count": len(records),
        "obstructed_count": sum(record["obstructs"] is True for record in records),
        "minimum_survivor_weight": str(minimum),
        "minimum_attaining_classes": [
            record[class_field] for weight, record in weighted if weight == minimum
        ],
        "maximum_survivor_weight": str(maximum),
        "maximum_attaining_classes": [
            record[class_field] for weight, record in weighted if weight == maximum
        ],
    }


def _source_receipt(record: dict[str, Any], family: CeilingCertificate) -> dict[str, object]:
    provenance = record.get("provenance")
    if not isinstance(provenance, dict):
        raise TypeError("source family lacks provenance")
    receipt = provenance.get("verify_ceiling")
    if not isinstance(receipt, dict):
        raise TypeError("source family lacks its exact depth receipt")
    if receipt.get("max_depth") != "1":
        raise ValueError("source receipt does not report exact maximum depth one")
    if receipt.get("failures") != [DEPTH_FAILURE]:
        raise ValueError("source receipt has failures beyond the source mass threshold")
    if receipt.get("regime") != "net" or receipt.get("symmetric_only") is not True:
        raise ValueError("source receipt does not identify the retained net family")
    if record.get("total_weight") != str(family.total_weight):
        raise ValueError("source total weight disagrees with its placements")
    return {
        "max_depth": "1",
        "vertices": receipt.get("vertices"),
        "decided_exactly": receipt.get("decided_exactly"),
        "regime": "net",
        "symmetric_only": True,
        "derived_depth_bound": "at most 1 by deletion of nonnegative source members",
    }


def source_binding(path: Path, expected_blob: str) -> dict[str, object]:
    """Require the clean tracked bytes to equal the preregistered Git blob."""

    resolved = path.resolve()
    if not resolved.is_relative_to(REPO):
        raise ValueError("source family must be inside the repository")
    relative = resolved.relative_to(REPO).as_posix()

    def git(*args: str) -> str:
        return subprocess.run(
            ["git", *args], cwd=REPO, check=True, capture_output=True, text=True
        ).stdout.strip()

    if git("ls-files", "--error-unmatch", "--", relative) != relative:
        raise ValueError("source family is not tracked")
    if git("status", "--porcelain", "--", relative):
        raise ValueError("source family is dirty")
    observed_blob = git("hash-object", "--", relative)
    commit_blob = git("rev-parse", f"HEAD:{relative}")
    if observed_blob != expected_blob or commit_blob != expected_blob:
        raise ValueError("source family does not match the expected Git blob")
    return {
        "path": relative,
        "git_commit": git("rev-parse", "HEAD"),
        "git_blob": observed_blob,
        "clean_tracked_blob_match": True,
    }


def _mass_lookup(family: CeilingCertificate) -> tuple[int, tuple[int, ...]]:
    denominator = lcm(*(placement.weight.denominator for placement in family.placements))
    scaled = tuple(int(placement.weight * denominator) for placement in family.placements)
    return denominator, scaled


def _mask_mass(mask: int, scaled: tuple[int, ...]) -> tuple[int, int]:
    count = 0
    total = 0
    while mask:
        bit = mask & -mask
        index = bit.bit_length() - 1
        total += scaled[index]
        count += 1
        mask ^= bit
    return count, total


def _joint_records(
    screens: dict[str, tuple[Screen, ...]], family: CeilingCertificate
) -> tuple[list[dict[str, object]], int]:
    denominator, scaled = _mass_lookup(family)
    cache: dict[int, tuple[int, int]] = {}
    rows: list[dict[str, object]] = []
    for choices in product(*(screens[corner] for corner in CORNER_NAMES)):
        mask = choices[0].mask & choices[1].mask & choices[2].mask & choices[3].mask
        measured = cache.get(mask)
        if measured is None:
            measured = _mask_mass(mask, scaled)
            cache[mask] = measured
        count, numerator = measured
        total = Fraction(numerator, denominator)
        rows.append(
            {
                "class_ids": [screen.class_id for screen in choices],
                "survivor_mask_hex": hex(mask),
                "survivor_count": count,
                "survivor_weight": str(total),
                "threshold": str(FOUR_CORNER_THRESHOLD),
                "obstructs": total >= FOUR_CORNER_THRESHOLD,
            }
        )
    return rows, len(cache)


def build_screen(
    source_record: dict[str, Any],
    *,
    source_identity: dict[str, object],
    kinds: tuple[str, ...],
    corner_counts: tuple[int, ...],
    target_side: Fraction = Fraction(96, 25),
) -> dict[str, object]:
    """Build one exact deletion receipt without replaying source arrangement depth."""

    source = CeilingCertificate.from_record(source_record)
    source_receipt = _source_receipt(source_record, source)
    manifest = owner_branch_manifest()
    full_half_tangents = tuple(
        direction.uy / (1 + direction.ux) for direction in manifest.directions.directions
    )
    transported_record = transport(
        source_record, Fraction(1), side=target_side, half_tangents=full_half_tangents
    )
    family = CeilingCertificate.from_record(transported_record)
    if family.square_side != Fraction(9977, 10000):
        raise ValueError("translated family does not use target B = 9977/10000")
    if transported_record["transport"]["translation"] != ["1/100", "1/100"]:
        raise ValueError("source family did not receive the required central translation")
    translation = Fraction(1, 100)
    for index, (placement, original) in enumerate(
        zip(family.placements, source.placements, strict=True)
    ):
        expected = (
            original.half_tangent,
            original.centre_x + translation,
            original.centre_y + translation,
            original.weight,
            original.side,
        )
        observed = (
            placement.half_tangent,
            placement.centre_x,
            placement.centre_y,
            placement.weight,
            placement.side,
        )
        if observed != expected:
            raise ValueError(f"transport altered source pose {index}")
    direction_axes = frozenset(
        (direction.ux, direction.uy) for direction in manifest.directions.directions
    )
    eligible = tuple(
        index
        for index, placement in enumerate(family.placements)
        if _orientation_axis(placement) in direction_axes
        and _contained(placement, family.outer_side)
    )
    eligible_mass = sum((family.placements[index].weight for index in eligible), Fraction(0))
    one_corner: list[dict[str, object]] = []
    by_kind_corner: dict[str, dict[str, tuple[Screen, ...]]] = {}
    for kind in kinds:
        by_corner: dict[str, tuple[Screen, ...]] = {}
        for corner in CORNER_NAMES:
            screens = tuple(
                screen_footprint(
                    family,
                    _corner_polygon(
                        _base_polygon(owner, kind, manifest.directions.directions),
                        corner,
                        target_side,
                    ),
                    class_id=f"{corner}:{owner.mark_id}:j{owner.sector}",
                    corner=corner,
                    kind=kind,
                    source_placements=source.placements,
                    direction_axes=direction_axes,
                )
                for owner in manifest.classes
            )
            by_corner[corner] = screens
            if 1 in corner_counts and corner == "bottom-left":
                one_corner.extend(
                    _screen_record(screen, ONE_CORNER_THRESHOLD) for screen in screens
                )
        by_kind_corner[kind] = by_corner
    joint: dict[str, object] = {}
    if 4 in corner_counts:
        for kind, screens in by_kind_corner.items():
            rows, unique_masks = _joint_records(screens, family)
            joint[kind] = {
                "class_count": len(rows),
                "unique_survivor_masks": unique_masks,
                "summary": summarize_records(rows, class_field="class_ids"),
                "component_screens": {
                    corner: [
                        _screen_record(screen, ONE_CORNER_THRESHOLD)
                        for screen in screens[corner]
                    ]
                    for corner in CORNER_NAMES
                },
                "classes": rows,
            }
    return {
        "schema": "corner-dual-salvage-screen/v1",
        "evidence_tier": "exact deletion consequence of retained depth-one source",
        "scope": (
            "fractional residual-cover method only; no packing bound and no owner "
            "compatibility claim"
        ),
        "source": {
            **source_identity,
            "placements": len(source.placements),
            "total_weight": str(source.total_weight),
            "depth_receipt": source_receipt,
        },
        "transport": transported_record["transport"],
        "directions": {
            "membership": "literal full canonical orientation modulo quarter turns",
            "folded_sources": manifest.directions.folded_count,
            "full_canonical_count": manifest.directions.full_count,
            "orientations": [
                {
                    "index": orientation.index,
                    "half_tangent": str(half_tangent),
                    "sources": [
                        {
                            "folded_index": source.folded_index,
                            "reflected": source.reflected,
                        }
                        for source in orientation.sources
                    ],
                }
                for orientation, half_tangent in zip(
                    manifest.directions.orientations, full_half_tangents, strict=True
                )
            ],
            "orientation_and_containment_filter": {
                "source_count": len(family.placements),
                "retained_count": len(eligible),
                "retained_weight": str(eligible_mass),
                "deleted_missing_orientation_or_containment": len(family.placements)
                - len(eligible),
            },
        },
        "owner_manifest": {
            "raw_classes_per_corner": len(manifest.classes),
            "source_contracts": list(SOURCE_CONTRACTS),
            "endpoint_footprint_status": ENDPOINT_FOOTPRINT_STATUS,
        },
        "one_corner": one_corner,
        "one_corner_summaries": {
            kind: summarize_records(
                [row for row in one_corner if row["footprint_kind"] == kind],
                class_field="class_id",
            )
            for kind in kinds
            if 1 in corner_counts
        },
        "four_corner": joint,
        "thresholds": {"one_corner": "10", "four_corner": "7"},
    }


def _csv_strings(value: str) -> tuple[str, ...]:
    return tuple(item.strip() for item in value.split(",") if item.strip())


def _csv_ints(value: str) -> tuple[int, ...]:
    return tuple(int(item) for item in _csv_strings(value))


def write_record_atomic(path: Path, record: dict[str, object]) -> None:
    """Write JSON or deterministic JSON gzip without exposing a partial receipt."""

    if path.exists():
        raise FileExistsError(f"refusing to overwrite {path}")
    text = json.dumps(record, indent=1) + "\n"
    if path.name.endswith(".json"):
        write_text_atomic(path, text)
        return
    if not path.name.endswith(".json.gz"):
        raise ValueError("output must end in .json or .json.gz")
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb", dir=path.parent, prefix=f".{path.name}.", delete=False
        ) as temporary:
            temporary.write(gzip.compress(text.encode(), mtime=0))
            temporary.flush()
            temporary_name = temporary.name
        Path(temporary_name).replace(path)
    finally:
        if temporary_name is not None:
            temporary = Path(temporary_name)
            if temporary.exists():
                temporary.unlink()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("source", type=Path)
    parser.add_argument("--footprint-kinds", default="point,triangle,endpoint")
    parser.add_argument("--corner-counts", default="1,4")
    parser.add_argument("--target-side", type=Fraction, default=Fraction(96, 25))
    parser.add_argument("--expect-source-blob", required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    kinds = _csv_strings(args.footprint_kinds)
    if not kinds or any(kind not in {"point", "triangle", "endpoint"} for kind in kinds):
        parser.error("footprint kinds must come from point,triangle,endpoint")
    corner_counts = _csv_ints(args.corner_counts)
    if not corner_counts or any(count not in {1, 4} for count in corner_counts):
        parser.error("corner counts must come from 1,4")
    record = json.loads(args.source.read_text())
    if not isinstance(record, dict):
        parser.error("source family must be a JSON object")
    result = build_screen(
        record,
        source_identity=source_binding(args.source, args.expect_source_blob),
        kinds=kinds,
        corner_counts=corner_counts,
        target_side=args.target_side,
    )
    write_record_atomic(args.out, result)
    print(json.dumps({"output": str(args.out), "schema": result["schema"]}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
