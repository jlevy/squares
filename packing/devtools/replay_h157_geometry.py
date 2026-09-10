"""Replay the corrected H157 geometry readings from retained repository sources.

The replay covers the four neutral eight-bin parent patches, their eight sixteen-bin
children, the two isolated whole-core poses, and one positive-area subpatch of core 59.
It validates a published result; it does not create a search target or change a packing
bound. Exact polygon distance decides intersection before vertex-to-edge distance.
"""

from __future__ import annotations

import argparse
import importlib.machinery
import importlib.util
import json
import re
import subprocess
import sys
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, replace
from fractions import Fraction
from pathlib import Path
from types import ModuleType
from typing import Protocol, cast

from devtools.owner_footprints import (
    convex_hull,
    convex_polygon_contains_polygon,
    convex_polygon_intersection,
    endpoint_footprint,
    owner_branch_manifest,
    point_in_closed_convex_polygon,
    polygon_area_twice,
)
from devtools.screen_corner_dual_salvage import strict_separation
from devtools.transport_ceiling_family import transport
from sqpack.cover import write_text_atomic
from sqpack.fractional.ceiling import CeilingCertificate
from sqpack.fractional.model import Direction

type Point = tuple[Fraction, Fraction]
type Polygon = tuple[Point, ...]

RETAINED_ROOT = Path(
    "packing/campaign/series/series-000-smoke-and-calibration/results/agenda-034"
)
RETAINED_FAMILY_PATH = RETAINED_ROOT / "ceiling-family-191-50.json"
RETAINED_BIN16_PATH = RETAINED_ROOT / "lane-x4-nbins.py.txt"
PUBLISHED_CHILDREN_PATH = RETAINED_ROOT / "lane-x4-survivors-16.json"

SOURCE_BLOBS: tuple[tuple[str, Path, str], ...] = (
    (
        "retained ceiling family",
        RETAINED_FAMILY_PATH,
        "2afc8fa9099f0d17c1f184400f7ebd2eb6483857",
    ),
    (
        "retained sixteen-bin helper",
        RETAINED_BIN16_PATH,
        "1ff2aac4902c89a205d0f97c8b276a7617ebe2b5",
    ),
    (
        "published sixteen-bin survivor rows",
        PUBLISHED_CHILDREN_PATH,
        "fadc62ad7493f040a430340934e7fcb67ae4ccae",
    ),
    (
        "exact owner geometry",
        Path("packing/devtools/owner_footprints.py"),
        "65501ad186a463eb5e7e16978daf03e603149fbd",
    ),
    (
        "exact separating-axis screen",
        Path("packing/devtools/screen_corner_dual_salvage.py"),
        "f8a993a9a2c24a0c844d5e43e10d33d95b332565",
    ),
    (
        "exact family transport",
        Path("packing/devtools/transport_ceiling_family.py"),
        "abb8ebe3f0b5b168133659bcef93971ae5c4c1b6",
    ),
    (
        "ceiling-family reader",
        Path("packing/src/sqpack/fractional/ceiling.py"),
        "f026bd04186787096fb57128517e319e7ee1ae00",
    ),
    (
        "exact direction model",
        Path("packing/src/sqpack/fractional/model.py"),
        "a5df6094eadfe441dba66fee8fe37a4e5530b6f6",
    ),
)

CASE_GROUPS = (
    ("m1", 3, (6, 7), 55),
    ("m1", 4, (8, 9), 55),
    ("m2", 3, (6, 7), 50),
    ("m2", 4, (8, 9), 50),
)
INTERSECTING_FIXED_TARGETS = frozenset({("m1", 16, 9), ("m2", 16, 6)})
EXPECTED_DISJOINT_DISTANCE = Fraction(75308842465387162009, 335694834731568400000000)
EXPECTED_NEAREST_AFTER_INTERSECTION = Fraction(
    154520421972020636842286626510179978387793755009897266163721,
    8274126656975111962857032162670705972822328494029059600000000,
)
EXPECTED_INTERSECTION_AREA = Fraction(
    9222372181955609687025480276566995509626950895711929,
    209023728552687322733150309907630740784000000000000000,
)
EXPECTED_WALL_MARGIN = Fraction(785411, 88696100)
EXPECTED_PATCH_AREA = Fraction(99540529, 10000000000000000)


class Bin16Helper(Protocol):
    def endpoint_footprint(
        self,
        mark: Point,
        sector: int,
        directions: tuple[Direction, ...],
        bins: int,
    ) -> Polygon: ...


@dataclass(frozen=True, slots=True)
class PolygonDistance:
    """An exact closed-polygon distance with its intersection decision."""

    intersects: bool
    squared: Fraction
    intersection: Polygon


def _git(repo: Path, *args: str) -> str:
    try:
        return subprocess.run(
            ["git", *args], cwd=repo, check=True, capture_output=True, text=True
        ).stdout.strip()
    except subprocess.CalledProcessError as error:
        detail = error.stderr.strip() or error.stdout.strip() or "git command failed"
        raise ValueError(detail) from error


def git_blob_binding(repo: Path, source: Path, expected_blob: str) -> dict[str, object]:
    """Bind clean worktree bytes and HEAD to one declared Git blob."""

    if re.fullmatch(r"[0-9a-f]{40}", expected_blob) is None:
        raise ValueError("expected Git blob must be 40 lowercase hexadecimal characters")
    root = repo.resolve()
    resolved = source.resolve()
    if not resolved.is_relative_to(root):
        raise ValueError("source must be inside the repository")
    relative = resolved.relative_to(root).as_posix()
    if _git(root, "ls-files", "--error-unmatch", "--", relative) != relative:
        raise ValueError(f"source is not tracked: {relative}")
    if _git(root, "status", "--porcelain", "--", relative):
        raise ValueError(f"source is dirty: {relative}")
    worktree_blob = _git(root, "hash-object", "--", relative)
    head_blob = _git(root, "rev-parse", f"HEAD:{relative}")
    if worktree_blob != expected_blob or head_blob != expected_blob:
        raise ValueError(f"source does not match the expected Git blob: {relative}")
    return {
        "path": relative,
        "git_blob": expected_blob,
        "clean_worktree_and_head_match": True,
    }


def build_source_manifest(repo: Path) -> dict[str, object]:
    """Validate and record every retained input and exact maintained dependency."""

    root = repo.resolve()
    if not (root / "packing/pyproject.toml").is_file():
        raise ValueError("repository does not contain packing/pyproject.toml")
    sources = []
    for purpose, relative, expected_blob in SOURCE_BLOBS:
        binding = git_blob_binding(root, root / relative, expected_blob)
        binding["purpose"] = purpose
        sources.append(binding)
    return {
        "schema": "h157-geometry-source-manifest-v1",
        "repository_head": _git(root, "rev-parse", "HEAD"),
        "sources": sources,
        "case_contract": {
            "eight_bin_parents": ["m1:j3", "m1:j4", "m2:j3", "m2:j4"],
            "sixteen_bin_children": [
                f"{mark}:J{sector}" for mark in ("m1", "m2") for sector in (6, 7, 8, 9)
            ],
            "fixed_targets": {"m1": 55, "m2": 50},
            "intersection_before_distance": ["m1:J9", "m2:J6"],
            "pose_cores": [59, 60],
            "subpatch_counterexample": "core 59 scaled by 1/10000 about corner 2",
        },
    }


def _validated_ccw(polygon: Polygon) -> Polygon:
    if len(polygon) < 3:
        raise ValueError("a convex polygon must have at least three vertices")
    if any(
        first == second
        for first, second in zip(polygon, polygon[1:] + polygon[:1], strict=True)
    ):
        raise ValueError("a convex polygon cannot have a zero-length edge")
    area = polygon_area_twice(polygon)
    if area == 0:
        raise ValueError("a convex polygon must have nonzero area")
    ccw = tuple(reversed(polygon)) if area < 0 else polygon
    start = ccw.index(min(ccw))
    ordered = ccw[start:] + ccw[:start]
    if ordered != convex_hull(ordered):
        raise ValueError("polygon must be convex with boundary vertices in order")
    return ccw


def _segment_distance_squared(point: Point, start: Point, end: Point) -> Fraction:
    dx, dy = end[0] - start[0], end[1] - start[1]
    denominator = dx * dx + dy * dy
    if denominator == 0:
        raise ValueError("polygon edge has zero length")
    parameter = ((point[0] - start[0]) * dx + (point[1] - start[1]) * dy) / denominator
    parameter = max(Fraction(0), min(Fraction(1), parameter))
    offset_x = point[0] - start[0] - parameter * dx
    offset_y = point[1] - start[1] - parameter * dy
    return offset_x * offset_x + offset_y * offset_y


def polygon_distance_squared(first: Polygon, second: Polygon) -> PolygonDistance:
    """Return exact convex-polygon distance, deciding closed intersection first."""

    left, right = _validated_ccw(first), _validated_ccw(second)
    intersection = convex_polygon_intersection(left, right)
    if intersection:
        return PolygonDistance(intersects=True, squared=Fraction(0), intersection=intersection)
    squared = min(
        _segment_distance_squared(point, start, end)
        for points, edges in ((left, right), (right, left))
        for point in points
        for start, end in zip(edges, edges[1:] + edges[:1], strict=True)
    )
    return PolygonDistance(intersects=False, squared=squared, intersection=())


def patch_claim_status(
    owner_core: Polygon,
    patch: Polygon,
    marks: Mapping[str, Point],
    survivor_weight: Fraction,
) -> dict[str, object]:
    """Separate the subset lower bound from equality's common-mark premise."""

    owner, candidate = _validated_ccw(owner_core), _validated_ccw(patch)
    if not convex_polygon_contains_polygon(owner, candidate):
        raise ValueError("patch is not contained in the owner core")
    common_marks = sorted(
        name for name, mark in marks.items() if point_in_closed_convex_polygon(mark, candidate)
    )
    return {
        "inside_owner_core": True,
        "patch_area": str(polygon_area_twice(candidate) / 2),
        "common_mark_ids": common_marks,
        "survivor_weight": str(survivor_weight),
        "subset_lower_bound_holds": survivor_weight >= 10,
        "equality_premise_holds": bool(common_marks),
        "survivor_weight_equals_ten": survivor_weight == 10,
    }


def parse_published_children(record: object) -> dict[str, dict[str, object]]:
    """Validate the eight retained child criteria used as the replay oracle."""

    if not isinstance(record, dict):
        raise TypeError("published child criteria must be a JSON object")
    expected_ids = {
        f"bottom-left:{mark}:J{sector}/16" for mark in ("m1", "m2") for sector in (6, 7, 8, 9)
    }
    if set(record) != expected_ids:
        raise ValueError("published child criteria do not name the expected eight classes")
    checked: dict[str, dict[str, object]] = {}
    for class_id in sorted(expected_ids):
        row = record[class_id]
        if not isinstance(row, dict):
            raise TypeError(f"published child row is not an object: {class_id}")
        mark = class_id.split(":")[1]
        sector = int(class_id.split("J")[1].split("/")[0])
        parent = sector // 2
        special = (mark, 16, sector) in INTERSECTING_FIXED_TARGETS
        expected_weight = "19/2" if special else "10"
        expected_count = 76 if special else 80
        if row.get("bins") != 16 or row.get("mark") != mark or row.get("sector") != sector:
            raise ValueError(f"published child identity is malformed: {class_id}")
        if row.get("parent_class") != f"bottom-left:{mark}:j{parent}":
            raise ValueError(f"published child has the wrong parent: {class_id}")
        if row.get("parent_survivor_weight") != "10":
            raise ValueError(f"published parent survivor weight is stale: {class_id}")
        if row.get("survivor_weight") != expected_weight:
            raise ValueError(f"published child survivor weight is stale: {class_id}")
        if row.get("survivor_count") != expected_count:
            raise ValueError(f"published child survivor count is stale: {class_id}")
        survivors = row.get("survivors")
        if not isinstance(survivors, list) or len(survivors) != expected_count:
            raise ValueError(f"published child survivor list is malformed: {class_id}")
        checked[class_id] = cast(dict[str, object], row)
    return checked


def _load_bin16_helper(source: Path) -> Bin16Helper:
    module_name = "_sqpack_retained_h157_nbins"
    loader = importlib.machinery.SourceFileLoader(module_name, str(source))
    spec = importlib.util.spec_from_loader(module_name, loader)
    if spec is None:
        raise ValueError("could not construct the retained sixteen-bin module")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    loader.exec_module(module)
    return cast(Bin16Helper, cast(ModuleType, module))


def _load_family(repo: Path) -> CeilingCertificate:
    raw = json.loads((repo / RETAINED_FAMILY_PATH).read_text())
    if not isinstance(raw, dict):
        raise TypeError("retained ceiling family must be a JSON object")
    source = CeilingCertificate.from_record(raw)
    receipt = raw.get("provenance", {}).get("verify_ceiling", {})
    if (
        source.n != 11
        or source.outer_side != Fraction(191, 50)
        or source.square_side != Fraction(9977, 10000)
        or source.total_weight != 11
        or len(source.placements) != 88
        or receipt.get("proved") is not True
        or receipt.get("failures") != []
        or receipt.get("max_depth") != "1"
        or receipt.get("regime") != "net"
        or receipt.get("symmetric_only") is not True
    ):
        raise ValueError("retained ceiling family does not satisfy the H157 source contract")
    moved = transport(raw, Fraction(1), side=Fraction(96, 25))
    return CeilingCertificate.from_record(moved)


def _survivors(patch: Polygon, family: CeilingCertificate) -> tuple[tuple[int, ...], Fraction]:
    candidate = _validated_ccw(patch)
    sat = tuple(
        index
        for index, placement in enumerate(family.placements)
        if strict_separation(candidate, placement.corners()) is not None
    )
    clipping = tuple(
        index
        for index, placement in enumerate(family.placements)
        if not convex_polygon_intersection(candidate, _validated_ccw(placement.corners()))
    )
    if sat != clipping:
        raise ValueError("separating-axis and clipping survivor sets disagree")
    weight = sum((family.placements[index].weight for index in sat), Fraction(0))
    return sat, weight


def _case_row(
    *,
    mark_id: str,
    bins: int,
    sector: int,
    parent_sector: int,
    target_index: int,
    patch: Polygon,
    family: CeilingCertificate,
    published: dict[str, dict[str, object]],
) -> dict[str, object]:
    survivor_indices, survivor_weight = _survivors(patch, family)
    target = family.placements[target_index].corners()
    fixed_distance = polygon_distance_squared(patch, target)
    survivor_distances = {
        index: polygon_distance_squared(patch, family.placements[index].corners()).squared
        for index in survivor_indices
    }
    nearest_distance = min(survivor_distances.values())
    nearest_indices = sorted(
        index for index, squared in survivor_distances.items() if squared == nearest_distance
    )
    intersection_area = (
        abs(polygon_area_twice(fixed_distance.intersection)) / 2
        if fixed_distance.intersection
        else Fraction(0)
    )
    class_id = (
        f"bottom-left:{mark_id}:j{sector}"
        if bins == 8
        else f"bottom-left:{mark_id}:J{sector}/16"
    )
    row: dict[str, object] = {
        "class_id": class_id,
        "class_kind": "parent" if bins == 8 else "child",
        "mark": mark_id,
        "bins": bins,
        "sector": sector,
        "parent_sector": parent_sector,
        "fixed_target": target_index,
        "fixed_target_intersects": fixed_distance.intersects,
        "intersection_polygon": [[str(x), str(y)] for x, y in fixed_distance.intersection],
        "intersection_area": str(intersection_area),
        "fixed_target_distance_squared": str(fixed_distance.squared),
        "nearest_actual_survivor_indices": nearest_indices,
        "nearest_actual_survivor_distance_squared": str(nearest_distance),
        "survivor_count": len(survivor_indices),
        "survivor_weight": str(survivor_weight),
        "sat_clipping_survivor_sets_identical": True,
    }
    if bins == 16:
        oracle = published[class_id]
        oracle_survivors = cast(list[dict[str, object]], oracle["survivors"])
        oracle_indices = tuple(cast(int, entry["source_index"]) for entry in oracle_survivors)
        mask = sum(1 << index for index in survivor_indices)
        parent_id = f"bottom-left:{mark_id}:j{parent_sector}"
        identical = (
            oracle_indices == survivor_indices
            and oracle["survivor_count"] == len(survivor_indices)
            and oracle["survivor_weight"] == str(survivor_weight)
            and oracle["survivor_mask_hex"] == hex(mask)
            and oracle["parent_class"] == parent_id
        )
        if not identical:
            raise ValueError(f"replay disagrees with the published survivor record: {class_id}")
        row["published_survivor_record_identical"] = True
    return row


def _validate_distance_cases(rows: Sequence[Mapping[str, object]]) -> None:
    if len(rows) != 12:
        raise ValueError("H157 replay must contain twelve parent and child cases")
    for row in rows:
        key = (cast(str, row["mark"]), cast(int, row["bins"]), cast(int, row["sector"]))
        intersects = key in INTERSECTING_FIXED_TARGETS
        expected_distance = Fraction(0) if intersects else EXPECTED_DISJOINT_DISTANCE
        expected_nearest = (
            EXPECTED_NEAREST_AFTER_INTERSECTION if intersects else EXPECTED_DISJOINT_DISTANCE
        )
        expected_weight = "19/2" if intersects else "10"
        expected_count = 76 if intersects else 80
        if row["fixed_target_intersects"] is not intersects:
            raise ValueError(f"fixed-target intersection criterion changed: {key}")
        if Fraction(cast(str, row["fixed_target_distance_squared"])) != expected_distance:
            raise ValueError(f"fixed-target distance criterion changed: {key}")
        if (
            Fraction(cast(str, row["nearest_actual_survivor_distance_squared"]))
            != expected_nearest
        ):
            raise ValueError(f"nearest-survivor distance criterion changed: {key}")
        area = Fraction(cast(str, row["intersection_area"]))
        if area != (EXPECTED_INTERSECTION_AREA if intersects else 0):
            raise ValueError(f"fixed-target intersection area criterion changed: {key}")
        if row["survivor_weight"] != expected_weight or row["survivor_count"] != expected_count:
            raise ValueError(f"survivor criterion changed: {key}")


def _pose_row(
    index: int, family: CeilingCertificate, marks: Mapping[str, Point]
) -> dict[str, object]:
    placement = family.placements[index]
    core = placement.corners()
    survivor_indices, survivor_weight = _survivors(core, family)
    parent = replace(placement, side=Fraction(1))
    margin = min(
        min(x, y, family.outer_side - x, family.outer_side - y) for x, y in parent.corners()
    )
    return {
        "index": index,
        "centre": [str(placement.centre_x), str(placement.centre_y)],
        "core_side": str(placement.side),
        "half_tangent": str(placement.half_tangent),
        "contains_marks": {
            name: point_in_closed_convex_polygon(mark, _validated_ccw(core))
            for name, mark in marks.items()
        },
        "same_centre_same_angle_unit_parent_contained": margin >= 0,
        "same_centre_same_angle_unit_parent_wall_margin": str(margin),
        "survivor_count": len(survivor_indices),
        "survivor_weight": str(survivor_weight),
        "sat_clipping_survivor_sets_identical": True,
    }


def _scaled_about(polygon: Polygon, anchor: Point, denominator: int) -> Polygon:
    return tuple(
        (
            anchor[0] + (point[0] - anchor[0]) / denominator,
            anchor[1] + (point[1] - anchor[1]) / denominator,
        )
        for point in polygon
    )


def replay_geometry(repo: Path) -> dict[str, object]:
    """Run the fixed H157 replay and return its guarded exact receipt."""

    if sys.version_info[:2] != (3, 14):
        raise ValueError("H157 geometry replay requires project Python 3.14")
    root = repo.resolve()
    manifest = build_source_manifest(root)
    family = _load_family(root)
    retained_helper = _load_bin16_helper(root / RETAINED_BIN16_PATH)
    owner_manifest = owner_branch_manifest()
    directions = owner_manifest.directions.directions
    marks = {owner.mark_id: owner.mark for owner in owner_manifest.classes}
    published = parse_published_children(
        json.loads((root / PUBLISHED_CHILDREN_PATH).read_text())
    )

    rows: list[dict[str, object]] = []
    for mark_id, parent_sector, children, target in CASE_GROUPS:
        rows.append(
            _case_row(
                mark_id=mark_id,
                bins=8,
                sector=parent_sector,
                parent_sector=parent_sector,
                target_index=target,
                patch=endpoint_footprint(marks[mark_id], parent_sector, directions),
                family=family,
                published=published,
            )
        )
        rows.extend(
            _case_row(
                mark_id=mark_id,
                bins=16,
                sector=child,
                parent_sector=parent_sector,
                target_index=target,
                patch=retained_helper.endpoint_footprint(marks[mark_id], child, directions, 16),
                family=family,
                published=published,
            )
            for child in children
        )
    _validate_distance_cases(rows)

    poses = [_pose_row(index, family, marks) for index in (59, 60)]
    if any(
        row["survivor_weight"] != "10"
        or row["same_centre_same_angle_unit_parent_contained"] is not True
        or Fraction(cast(str, row["same_centre_same_angle_unit_parent_wall_margin"]))
        != EXPECTED_WALL_MARGIN
        for row in poses
    ):
        raise ValueError("whole-core pose criterion changed")

    owner_core = family.placements[59].corners()
    owner_survivors, owner_weight = _survivors(owner_core, family)
    mark_control = patch_claim_status(owner_core, owner_core, marks, owner_weight)
    mark_control["owner_core"] = 59
    mark_control["survivor_count"] = len(owner_survivors)

    corner_index = 2
    small_patch = _scaled_about(owner_core, owner_core[corner_index], 10_000)
    patch_survivors, patch_weight = _survivors(small_patch, family)
    counterexample = patch_claim_status(owner_core, small_patch, marks, patch_weight)
    counterexample.update(
        {
            "owner_core": 59,
            "corner_index": corner_index,
            "construction": "core 59 scaled by 1/10000 about corner 2",
            "patch": [[str(x), str(y)] for x, y in small_patch],
            "survivor_count": len(patch_survivors),
            "sat_clipping_survivor_sets_identical": True,
        }
    )
    if (
        counterexample["patch_area"] != str(EXPECTED_PATCH_AREA)
        or counterexample["survivor_weight"] != "43/4"
        or counterexample["common_mark_ids"] != []
        or counterexample["subset_lower_bound_holds"] is not True
        or counterexample["equality_premise_holds"] is not False
        or mark_control["survivor_weight_equals_ten"] is not True
        or mark_control["equality_premise_holds"] is not True
    ):
        raise ValueError("core-59 patch criterion changed")

    child_weights = [
        Fraction(cast(str, row["survivor_weight"])) for row in rows if row["bins"] == 16
    ]
    return {
        "schema": "h157-geometry-receipt-v1",
        "source_manifest": manifest,
        "scope": {
            "operation": "replay of the retained H157 geometry result",
            "new_research_target": False,
            "changes_global_packing_bounds": False,
            "physical_completion_claim": False,
        },
        "distance_cases": rows,
        "refined_survivor_summary": {
            "class_count": len(child_weights),
            "maximum_survivor_weight": str(max(child_weights)),
            "maximum_attaining_class_count": sum(
                weight == max(child_weights) for weight in child_weights
            ),
            "minimum_survivor_weight": str(min(child_weights)),
        },
        "pose_rows": poses,
        "mark_containing_patch_control": mark_control,
        "arbitrary_subpatch_counterexample": counterexample,
    }


def _write_output(output: Path, receipt: dict[str, object]) -> None:
    if output.exists():
        raise FileExistsError(f"refusing to overwrite {output}")
    if not output.parent.is_dir():
        raise ValueError("output parent directory does not exist")
    output.mkdir()
    manifest = cast(dict[str, object], receipt["source_manifest"])
    write_text_atomic(
        output / "source-manifest.json",
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
    )
    write_text_atomic(
        output / "geometry-receipt.json",
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
    )


def _find_repo() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "packing/pyproject.toml").is_file():
            return parent
    raise ValueError("could not locate the repository; pass --repo")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--repo", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    if args.out.exists():
        raise FileExistsError(f"refusing to overwrite {args.out}")
    repo = args.repo.resolve() if args.repo is not None else _find_repo()
    if args.out.resolve() == repo or args.out.resolve().is_relative_to(repo):
        raise ValueError("receipt output must be outside the repository")
    receipt = replay_geometry(repo)
    _write_output(args.out, receipt)
    print(
        json.dumps(
            {
                "output": str(args.out),
                "case_count": len(cast(list[object], receipt["distance_cases"])),
                "status": "confirmed retained H157 geometry replay",
            }
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
