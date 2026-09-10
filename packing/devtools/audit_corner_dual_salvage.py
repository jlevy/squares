#!/usr/bin/env python3
"""Independently audit an exact corner dual-salvage receipt.

The reader reconstructs the immutable source transport, owner polygons, exact
separating-axis decisions, survivor masses, and four-corner intersections.  It does
not invoke the screen producer, replay the source arrangement, or solve an LP.
"""

from __future__ import annotations

import argparse
import gzip
import json
import os
import subprocess
import sys
import tempfile
import time
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
    point_footprint,
    triangle_footprint,
)
from sqpack.fractional.ceiling import CeilingCertificate, Placement

type Point = tuple[Fraction, Fraction]
type Polygon = tuple[Point, ...]

REPO = Path(__file__).resolve().parents[2]
TARGET_SIDE = Fraction(96, 25)
TARGET_SQUARE_SIDE = Fraction(9977, 10000)
TRANSLATION = Fraction(1, 100)
KINDS = ("point", "triangle", "endpoint")
CORNERS = ("bottom-left", "bottom-right", "top-left", "top-right")
ONE_CORNER_THRESHOLD = Fraction(10)
FOUR_CORNER_THRESHOLD = Fraction(7)
DEPTH_FAILURE = "K3 total weight at least n"


@dataclass(frozen=True, slots=True)
class Separation:
    axis: Point
    gap: Fraction


@dataclass(frozen=True, slots=True)
class AuditedScreen:
    class_id: str
    mask: int
    count: int
    weight: Fraction


def _mapping(value: object, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise TypeError(f"{label} must be a JSON object")
    return value


def _sequence(value: object, label: str) -> list[Any]:
    if not isinstance(value, list):
        raise TypeError(f"{label} must be a JSON array")
    return value


def git_blob_binding(path: Path, expected_blob: str, *, label: str) -> dict[str, object]:
    """Bind a clean tracked input to its preregistered Git blob and current HEAD."""

    resolved = path.resolve()
    if not resolved.is_relative_to(REPO):
        raise ValueError(f"{label} must be inside the repository")
    relative = resolved.relative_to(REPO).as_posix()

    def git(*args: str) -> str:
        return subprocess.run(
            ["git", *args], cwd=REPO, check=True, capture_output=True, text=True
        ).stdout.strip()

    if git("ls-files", "--error-unmatch", "--", relative) != relative:
        raise ValueError(f"{label} is not tracked")
    if git("status", "--porcelain", "--", relative):
        raise ValueError(f"{label} is dirty")
    worktree_blob = git("hash-object", "--", relative)
    head_blob = git("rev-parse", f"HEAD:{relative}")
    if worktree_blob != expected_blob or head_blob != expected_blob:
        raise ValueError(f"{label} does not match the expected Git blob")
    return {
        "path": relative,
        "git_commit": git("rev-parse", "HEAD"),
        "git_blob": worktree_blob,
        "clean_tracked_blob_match": True,
    }


def load_receipt(
    path: Path, *, max_compressed_bytes: int, max_uncompressed_bytes: int
) -> dict[str, Any]:
    """Load one gzip JSON receipt under compressed and expanded byte guards."""

    compressed = path.stat().st_size
    if compressed > max_compressed_bytes:
        raise ValueError(
            f"receipt has {compressed} compressed bytes above guard {max_compressed_bytes}"
        )
    with gzip.open(path, "rb") as source:
        raw = source.read(max_uncompressed_bytes + 1)
    if len(raw) > max_uncompressed_bytes:
        raise ValueError(
            f"receipt exceeds the {max_uncompressed_bytes}-byte uncompressed guard"
        )
    return _mapping(json.loads(raw), "receipt")


def exact_separation(first: Polygon, second: Polygon) -> Separation | None:
    """Recompute the producer's strict convex SAT decision in exact arithmetic."""

    if not first or not second:
        raise ValueError("separation operands must be nonempty")
    best: Separation | None = None
    for polygon in (first, second):
        for start, end in zip(polygon, polygon[1:] + polygon[:1], strict=True):
            dx, dy = end[0] - start[0], end[1] - start[1]
            if dx == 0 and dy == 0:
                continue
            axis = (-dy, dx)
            first_projection = tuple(axis[0] * x + axis[1] * y for x, y in first)
            second_projection = tuple(axis[0] * x + axis[1] * y for x, y in second)
            gap = max(
                min(second_projection) - max(first_projection),
                min(first_projection) - max(second_projection),
            )
            if gap > 0 and (best is None or gap > best.gap):
                best = Separation(axis, gap)
    return best


def _canonical_axis(placement: Placement) -> Point:
    direction = placement.direction
    candidates = (
        (direction.ux, direction.uy),
        (direction.vx, direction.vy),
        (-direction.ux, -direction.uy),
        (-direction.vx, -direction.vy),
    )
    matches = tuple(point for point in candidates if point[0] > 0 and point[1] >= 0)
    if len(matches) != 1:
        raise ValueError("source pose has no canonical orientation modulo quarter turns")
    return matches[0]


def _contained(placement: Placement) -> bool:
    return all(0 <= x <= TARGET_SIDE and 0 <= y <= TARGET_SIDE for x, y in placement.corners())


def _transport_source(
    source: CeilingCertificate, destination_half_tangents: tuple[Fraction, ...]
) -> CeilingCertificate:
    if source.outer_side != Fraction(191, 50):
        raise ValueError("source family has the wrong outer side")
    if source.square_side != TARGET_SQUARE_SIDE:
        raise ValueError("source family has the wrong square side")
    if any(tangent not in destination_half_tangents for tangent in source.half_tangents):
        raise ValueError("canonical owner directions omit a source orientation")
    return CeilingCertificate(
        source.n,
        TARGET_SIDE,
        source.square_side,
        destination_half_tangents,
        tuple(
            Placement(
                placement.half_tangent,
                placement.centre_x + TRANSLATION,
                placement.centre_y + TRANSLATION,
                placement.weight,
                placement.side,
            )
            for placement in source.placements
        ),
    )


def _fraction_polygon(value: object, label: str) -> Polygon:
    rows = _sequence(value, label)
    result: list[Point] = []
    for index, row in enumerate(rows):
        coordinates = _sequence(row, f"{label}[{index}]")
        if len(coordinates) != 2:
            raise ValueError(f"{label}[{index}] must contain two coordinates")
        result.append((Fraction(str(coordinates[0])), Fraction(str(coordinates[1]))))
    if not result:
        raise ValueError(f"{label} must be nonempty")
    return tuple(result)


def _base_polygon(owner: OwnerClass, kind: str, directions: tuple[Any, ...]) -> Polygon:
    if kind == "point":
        return point_footprint(owner.mark)
    if kind == "triangle":
        return triangle_footprint(owner.mark, owner.sector)
    if kind == "endpoint":
        return endpoint_footprint(owner.mark, owner.sector, directions)
    raise ValueError(f"unknown footprint kind {kind}")


def _corner_polygon(polygon: Polygon, corner: str) -> Polygon:
    if corner == "bottom-left":
        return polygon
    if corner == "bottom-right":
        return tuple((TARGET_SIDE - x, y) for x, y in polygon)
    if corner == "top-left":
        return tuple((x, TARGET_SIDE - y) for x, y in polygon)
    if corner == "top-right":
        return tuple((TARGET_SIDE - x, TARGET_SIDE - y) for x, y in polygon)
    raise ValueError(f"unknown corner {corner}")


def _owner_class_id(owner: OwnerClass, corner: str) -> str:
    return f"{corner}:{owner.mark_id}:j{owner.sector}"


def _expected_transport(
    source: CeilingCertificate, destination_half_tangents: tuple[Fraction, ...]
) -> dict[str, object]:
    return {
        "factor": "1",
        "source_outer_side": str(source.outer_side),
        "scaled_outer_side": str(source.outer_side),
        "translation": [str(TRANSLATION), str(TRANSLATION)],
        "source_half_tangents": [str(value) for value in source.half_tangents],
        "destination_half_tangents": [str(value) for value in destination_half_tangents],
        "depth_check": "not run; exact affine transport preserves the source depth",
    }


def _expected_direction_receipt(manifest: Any) -> dict[str, object]:
    half_tangents = tuple(
        direction.uy / (1 + direction.ux) for direction in manifest.directions.directions
    )
    return {
        "membership": "literal full canonical orientation modulo quarter turns",
        "folded_sources": manifest.directions.folded_count,
        "full_canonical_count": manifest.directions.full_count,
        "orientations": [
            {
                "index": orientation.index,
                "half_tangent": str(tangent),
                "sources": [
                    {
                        "folded_index": source.folded_index,
                        "reflected": source.reflected,
                    }
                    for source in orientation.sources
                ],
            }
            for orientation, tangent in zip(
                manifest.directions.orientations, half_tangents, strict=True
            )
        ],
    }


def audit_component_screen(
    record: Mapping[str, object],
    *,
    expected_polygon: Polygon,
    expected_class_id: str,
    expected_corner: str,
    expected_kind: str,
    source: tuple[Placement, ...],
    transported: tuple[Placement, ...],
    direction_axes: frozenset[Point],
) -> AuditedScreen:
    """Recompute one complete screen, including every inclusion and exclusion."""

    if len(source) != len(transported):
        raise ValueError("source and transported family cardinalities disagree")
    fixed_fields: dict[str, object] = {
        "class_id": expected_class_id,
        "corner": expected_corner,
        "footprint_kind": expected_kind,
        "threshold": str(ONE_CORNER_THRESHOLD),
    }
    for field, expected in fixed_fields.items():
        if record.get(field) != expected:
            raise ValueError(f"screen {expected_class_id} has wrong {field}")
    if _fraction_polygon(record.get("footprint"), "screen footprint") != expected_polygon:
        raise ValueError(f"screen {expected_class_id} has altered footprint geometry")

    expected_survivors: list[tuple[int, Placement, Separation]] = []
    expected_mask = 0
    for index, (original, placement) in enumerate(zip(source, transported, strict=True)):
        if placement.weight != original.weight or placement.side != original.side:
            raise ValueError(f"transport altered source placement {index}")
        if _canonical_axis(placement) not in direction_axes:
            continue
        if not _contained(placement):
            raise ValueError(f"transported placement {index} leaves the container")
        separation = exact_separation(placement.corners(), expected_polygon)
        if separation is not None:
            expected_mask |= 1 << index
            expected_survivors.append((index, placement, separation))

    rows = _sequence(record.get("survivors"), f"screen {expected_class_id} survivors")
    if len(rows) != len(expected_survivors):
        raise ValueError(f"screen {expected_class_id} has an incomplete survivor list")
    total = Fraction(0)
    for ordinal, (raw, expected) in enumerate(zip(rows, expected_survivors, strict=True)):
        row = _mapping(raw, f"screen {expected_class_id} survivor {ordinal}")
        index, placement, separation = expected
        if row.get("source_index") != index:
            raise ValueError(f"screen {expected_class_id} has a wrong survivor index")
        if Fraction(str(row.get("weight"))) != placement.weight:
            raise ValueError(f"screen {expected_class_id} altered survivor weight {index}")
        axis = _sequence(row.get("separating_axis"), "separating axis")
        observed_axis = (Fraction(str(axis[0])), Fraction(str(axis[1])))
        observed_gap = Fraction(str(row.get("positive_projection_gap")))
        if observed_gap <= 0:
            raise ValueError(f"screen {expected_class_id} records a nonpositive SAT gap")
        if (observed_axis, observed_gap) != (separation.axis, separation.gap):
            raise ValueError(f"screen {expected_class_id} has an altered exact SAT witness")
        total += placement.weight

    count = len(expected_survivors)
    if int(str(record.get("survivor_mask_hex")), 16) != expected_mask:
        raise ValueError(f"screen {expected_class_id} has a wrong survivor mask")
    if record.get("survivor_count") != count:
        raise ValueError(f"screen {expected_class_id} has a wrong survivor count")
    if Fraction(str(record.get("survivor_weight"))) != total:
        raise ValueError(f"screen {expected_class_id} has a wrong survivor mass")
    if record.get("obstructs") is not (total >= ONE_CORNER_THRESHOLD):
        raise ValueError(f"screen {expected_class_id} has a wrong obstruction verdict")
    return AuditedScreen(expected_class_id, expected_mask, count, total)


def summarize_rows(
    rows: Sequence[Mapping[str, object]], *, class_field: str
) -> dict[str, object]:
    if not rows:
        raise ValueError("cannot summarize an empty class grid")
    weighted = [(Fraction(str(row["survivor_weight"])), row) for row in rows]
    minimum = min(weight for weight, _ in weighted)
    maximum = max(weight for weight, _ in weighted)
    return {
        "class_count": len(rows),
        "obstructed_count": sum(row.get("obstructs") is True for row in rows),
        "minimum_survivor_weight": str(minimum),
        "minimum_attaining_classes": [
            row[class_field] for weight, row in weighted if weight == minimum
        ],
        "maximum_survivor_weight": str(maximum),
        "maximum_attaining_classes": [
            row[class_field] for weight, row in weighted if weight == maximum
        ],
    }


def audit_joint_rows(
    rows: Sequence[Mapping[str, object]],
    screens: Mapping[str, Sequence[AuditedScreen]],
    placements: tuple[Placement, ...],
) -> tuple[int, dict[str, object]]:
    """Check product order, mask intersections, exact cardinalities, mass, and summary."""

    expected_count = 1
    for corner in CORNERS:
        expected_count *= len(screens[corner])
    if len(rows) != expected_count:
        raise ValueError("four-corner class grid has the wrong cardinality")
    denominator = lcm(*(placement.weight.denominator for placement in placements))
    scaled = tuple(int(placement.weight * denominator) for placement in placements)
    cache: dict[int, tuple[int, Fraction]] = {}
    for ordinal, (raw, choices) in enumerate(
        zip(rows, product(*(screens[corner] for corner in CORNERS)), strict=True)
    ):
        row = _mapping(raw, f"joint row {ordinal}")
        class_ids = [choice.class_id for choice in choices]
        if row.get("class_ids") != class_ids:
            raise ValueError(f"joint row {ordinal} has wrong class product order")
        mask = choices[0].mask & choices[1].mask & choices[2].mask & choices[3].mask
        measured = cache.get(mask)
        if measured is None:
            remainder = mask
            count = 0
            numerator = 0
            while remainder:
                bit = remainder & -remainder
                index = bit.bit_length() - 1
                if index >= len(scaled):
                    raise ValueError(f"joint row {ordinal} has an out-of-range mask bit")
                numerator += scaled[index]
                count += 1
                remainder ^= bit
            measured = count, Fraction(numerator, denominator)
            cache[mask] = measured
        count, weight = measured
        expected_fields: dict[str, object] = {
            "survivor_mask_hex": hex(mask),
            "survivor_count": count,
            "survivor_weight": str(weight),
            "threshold": str(FOUR_CORNER_THRESHOLD),
            "obstructs": weight >= FOUR_CORNER_THRESHOLD,
        }
        for field, expected in expected_fields.items():
            if row.get(field) != expected:
                raise ValueError(f"joint row {ordinal} has wrong {field}")
    return len(cache), summarize_rows(rows, class_field="class_ids")


def _validate_source_receipt(
    receipt: Mapping[str, object],
    source_record: Mapping[str, object],
    source: CeilingCertificate,
    source_binding: Mapping[str, object],
) -> None:
    expected_identity = {
        "path": source_binding["path"],
        "git_blob": source_binding["git_blob"],
        "clean_tracked_blob_match": True,
        "placements": len(source.placements),
        "total_weight": str(source.total_weight),
    }
    for field, expected in expected_identity.items():
        if receipt.get(field) != expected:
            raise ValueError(f"receipt has wrong source {field}")
    producer_commit = receipt.get("git_commit")
    if not isinstance(producer_commit, str):
        raise TypeError("receipt lacks its producer Git commit")
    historical_blob = subprocess.run(
        ["git", "rev-parse", f"{producer_commit}:{source_binding['path']}"],
        cwd=REPO,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    if historical_blob != source_binding["git_blob"]:
        raise ValueError("producer commit does not bind the declared source blob")
    if source_record.get("total_weight") != str(source.total_weight):
        raise ValueError("source family has an inconsistent total weight")
    provenance = _mapping(source_record.get("provenance"), "source provenance")
    depth = _mapping(provenance.get("verify_ceiling"), "source depth receipt")
    if (
        depth.get("max_depth") != "1"
        or depth.get("failures") != [DEPTH_FAILURE]
        or depth.get("regime") != "net"
        or depth.get("symmetric_only") is not True
    ):
        raise ValueError("source family lacks the retained exact depth-one receipt")
    expected_depth = {
        "max_depth": "1",
        "vertices": depth.get("vertices"),
        "decided_exactly": depth.get("decided_exactly"),
        "regime": "net",
        "symmetric_only": True,
        "derived_depth_bound": "at most 1 by deletion of nonnegative source members",
    }
    if receipt.get("depth_receipt") != expected_depth:
        raise ValueError("receipt does not preserve the source exact depth receipt")


def audit_receipt(
    receipt: dict[str, Any],
    source_record: dict[str, Any],
    *,
    receipt_binding: dict[str, object],
    source_binding: dict[str, object],
    max_source_placements: int,
    max_component_screens: int,
    max_joint_classes: int,
) -> dict[str, object]:
    """Audit an exp137-style receipt with bounded exact independent recomputation."""

    started = time.perf_counter()
    if receipt.get("schema") != "corner-dual-salvage-screen/v1":
        raise ValueError("input has the wrong corner screen schema")
    expected_top = {
        "schema",
        "evidence_tier",
        "scope",
        "source",
        "transport",
        "directions",
        "owner_manifest",
        "one_corner",
        "one_corner_summaries",
        "four_corner",
        "thresholds",
    }
    if set(receipt) != expected_top:
        raise ValueError("receipt has missing or unexpected top-level fields")
    if receipt.get("evidence_tier") != (
        "exact deletion consequence of retained depth-one source"
    ):
        raise ValueError("receipt has altered evidence tier")
    if receipt.get("scope") != (
        "fractional residual-cover method only; no packing bound and no owner "
        "compatibility claim"
    ):
        raise ValueError("receipt has altered claim scope")
    if receipt.get("thresholds") != {"one_corner": "10", "four_corner": "7"}:
        raise ValueError("receipt has altered screen thresholds")
    source = CeilingCertificate.from_record(source_record)
    if len(source.placements) > max_source_placements:
        raise ValueError("source placement count exceeds the audit guard")
    _validate_source_receipt(
        _mapping(receipt.get("source"), "receipt source"),
        source_record,
        source,
        source_binding,
    )

    manifest = owner_branch_manifest()
    if len(manifest.classes) != 16:
        raise ValueError("owner manifest no longer has sixteen raw classes")
    direction_receipt = _expected_direction_receipt(manifest)
    destination_half_tangents = tuple(
        Fraction(str(row["half_tangent"]))
        for row in direction_receipt["orientations"]  # type: ignore[union-attr]
    )
    directions = _mapping(receipt.get("directions"), "directions")
    for field, expected in direction_receipt.items():
        if directions.get(field) != expected:
            raise ValueError(f"receipt has altered canonical directions field {field}")
    transported = _transport_source(source, destination_half_tangents)
    if receipt.get("transport") != _expected_transport(source, destination_half_tangents):
        raise ValueError("receipt has altered exact +1/100 transport")
    direction_axes = frozenset(
        (direction.ux, direction.uy) for direction in manifest.directions.directions
    )
    eligible = tuple(
        index
        for index, placement in enumerate(transported.placements)
        if _canonical_axis(placement) in direction_axes and _contained(placement)
    )
    eligible_weight = sum(
        (transported.placements[index].weight for index in eligible), Fraction(0)
    )
    expected_filter = {
        "source_count": len(source.placements),
        "retained_count": len(eligible),
        "retained_weight": str(eligible_weight),
        "deleted_missing_orientation_or_containment": len(source.placements) - len(eligible),
    }
    if directions.get("orientation_and_containment_filter") != expected_filter:
        raise ValueError("receipt has altered orientation/containment filter totals")
    expected_owner = {
        "raw_classes_per_corner": 16,
        "source_contracts": list(SOURCE_CONTRACTS),
        "endpoint_footprint_status": ENDPOINT_FOOTPRINT_STATUS,
    }
    if receipt.get("owner_manifest") != expected_owner:
        raise ValueError("receipt has altered owner manifest metadata")

    four_corner = _mapping(receipt.get("four_corner"), "four_corner")
    if set(four_corner) != set(KINDS):
        raise ValueError("receipt must contain all three footprint kinds")
    total_screens = len(KINDS) * len(CORNERS) * len(manifest.classes)
    if total_screens > max_component_screens:
        raise ValueError("component screen count exceeds the audit guard")
    if len(manifest.classes) ** 4 > max_joint_classes:
        raise ValueError("joint class count exceeds the audit guard")

    one_corner = _sequence(receipt.get("one_corner"), "one_corner")
    one_summaries = _mapping(receipt.get("one_corner_summaries"), "one summaries")
    if set(one_summaries) != set(KINDS):
        raise ValueError("receipt must contain all three one-corner summaries")
    expected_one_rows: list[Mapping[str, object]] = []
    kind_results: dict[str, object] = {}
    sat_checks = 0
    for kind in KINDS:
        kind_record = _mapping(four_corner[kind], f"four_corner {kind}")
        component_receipt = _mapping(kind_record.get("component_screens"), "component screens")
        if list(component_receipt) != list(CORNERS):
            raise ValueError(f"{kind} component screens have wrong corner order")
        audited_by_corner: dict[str, tuple[AuditedScreen, ...]] = {}
        for corner in CORNERS:
            rows = _sequence(component_receipt[corner], f"{kind} {corner} screens")
            if len(rows) != len(manifest.classes):
                raise ValueError(f"{kind} {corner} has the wrong screen count")
            audited: list[AuditedScreen] = []
            for raw, owner in zip(rows, manifest.classes, strict=True):
                base = _base_polygon(owner, kind, manifest.directions.directions)
                audited.append(
                    audit_component_screen(
                        _mapping(raw, f"{kind} {corner} screen"),
                        expected_polygon=_corner_polygon(base, corner),
                        expected_class_id=_owner_class_id(owner, corner),
                        expected_corner=corner,
                        expected_kind=kind,
                        source=source.placements,
                        transported=transported.placements,
                        direction_axes=direction_axes,
                    )
                )
                sat_checks += len(source.placements)
            audited_by_corner[corner] = tuple(audited)
            if corner == "bottom-left":
                expected_one_rows.extend(_mapping(row, "one-corner source row") for row in rows)

        joint_rows = [
            _mapping(row, f"{kind} joint row")
            for row in _sequence(kind_record.get("classes"), f"{kind} joint classes")
        ]
        unique_masks, summary = audit_joint_rows(
            joint_rows, audited_by_corner, transported.placements
        )
        if kind_record.get("class_count") != len(joint_rows):
            raise ValueError(f"{kind} records a wrong joint class count")
        if kind_record.get("unique_survivor_masks") != unique_masks:
            raise ValueError(f"{kind} records a wrong unique-mask count")
        if kind_record.get("summary") != summary:
            raise ValueError(f"{kind} records a wrong four-corner summary")
        kind_results[kind] = {
            "component_screens": len(CORNERS) * len(manifest.classes),
            "exact_sat_checks": len(CORNERS) * len(manifest.classes) * len(source.placements),
            "joint_classes": len(joint_rows),
            "unique_survivor_masks": unique_masks,
            "summary_verified": True,
            "obstructed_count": summary["obstructed_count"],
            "minimum_survivor_weight": summary["minimum_survivor_weight"],
            "maximum_survivor_weight": summary["maximum_survivor_weight"],
        }
        print(json.dumps({"progress": "kind-complete", "kind": kind}), flush=True)

    observed_one = [_mapping(row, "one-corner row") for row in one_corner]
    if observed_one != expected_one_rows:
        raise ValueError("one-corner rows do not match bottom-left component screens")
    for kind in KINDS:
        rows = [row for row in observed_one if row.get("footprint_kind") == kind]
        expected_summary = summarize_rows(rows, class_field="class_id")
        if one_summaries.get(kind) != expected_summary:
            raise ValueError(f"{kind} records a wrong one-corner summary")

    return {
        "schema": "corner-dual-salvage-audit/v1",
        "status": "complete",
        "evidence_tier": "independent exact receipt audit; no arrangement replay or LP",
        "claim_limit": "Audits the recorded deletion screen only; no packing bound.",
        "receipt": receipt_binding,
        "source": source_binding,
        "settings": {
            "source_placements_guard": max_source_placements,
            "component_screens_guard": max_component_screens,
            "joint_classes_per_kind_guard": max_joint_classes,
            "transport": "+1/100 in each coordinate, exact",
        },
        "verified": {
            "source_placements": len(source.placements),
            "folded_direction_sources": manifest.directions.folded_count,
            "canonical_directions": len(manifest.directions.directions),
            "owner_classes_per_corner": len(manifest.classes),
            "endpoint_footprint_status": ENDPOINT_FOOTPRINT_STATUS,
            "component_screens": total_screens,
            "exact_sat_checks": sat_checks,
            "kinds": kind_results,
        },
        "seconds": time.perf_counter() - started,
    }


def write_exclusive_atomic(path: Path, record: dict[str, object]) -> None:
    """Write a compact audit receipt atomically and refuse overwrite."""

    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=path.parent, prefix=f".{path.name}.", delete=False
        ) as temporary:
            json.dump(record, temporary, indent=1)
            temporary.write("\n")
            temporary.flush()
            temporary_name = temporary.name
        os.link(temporary_name, path)
    finally:
        if temporary_name is not None:
            temporary = Path(temporary_name)
            if temporary.exists():
                temporary.unlink()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("receipt", type=Path)
    parser.add_argument("source", type=Path)
    parser.add_argument("--expect-receipt-blob", required=True)
    parser.add_argument("--expect-source-blob", required=True)
    parser.add_argument("--max-compressed-bytes", type=int, default=20_000_000)
    parser.add_argument("--max-uncompressed-bytes", type=int, default=200_000_000)
    parser.add_argument("--max-source-placements", type=int, default=1_000)
    parser.add_argument("--max-component-screens", type=int, default=1_000)
    parser.add_argument("--max-joint-classes", type=int, default=100_000)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    guards = (
        args.max_compressed_bytes,
        args.max_uncompressed_bytes,
        args.max_source_placements,
        args.max_component_screens,
        args.max_joint_classes,
    )
    if min(guards) < 1:
        parser.error("all audit guards must be positive")
    if args.out.exists():
        parser.error(f"refusing to overwrite {args.out}")
    receipt_binding = git_blob_binding(
        args.receipt, args.expect_receipt_blob, label="screen receipt"
    )
    source_binding = git_blob_binding(
        args.source, args.expect_source_blob, label="source family"
    )
    receipt = load_receipt(
        args.receipt,
        max_compressed_bytes=args.max_compressed_bytes,
        max_uncompressed_bytes=args.max_uncompressed_bytes,
    )
    source = _mapping(json.loads(args.source.read_text()), "source family")
    result = audit_receipt(
        receipt,
        source,
        receipt_binding=receipt_binding,
        source_binding=source_binding,
        max_source_placements=args.max_source_placements,
        max_component_screens=args.max_component_screens,
        max_joint_classes=args.max_joint_classes,
    )
    write_exclusive_atomic(args.out, result)
    print(json.dumps({"output": str(args.out), "status": "complete"}), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
