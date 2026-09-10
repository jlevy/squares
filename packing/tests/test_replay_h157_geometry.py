"""Independent controls for the bounded H157 geometry replay."""

from __future__ import annotations

import importlib.util
import json
import sys
from copy import deepcopy
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest


def _find_repo() -> Path:
    candidates = (*Path(__file__).resolve().parents, Path.cwd(), *Path.cwd().resolve().parents)
    for candidate in candidates:
        if (candidate / "packing/pyproject.toml").is_file():
            return candidate
    raise RuntimeError("could not locate the squares repository")


REPO = _find_repo()
MODULE_PATH = Path(__file__).parents[1] / "devtools/replay_h157_geometry.py"
SPEC = importlib.util.spec_from_file_location("replay_h157_geometry_candidate", MODULE_PATH)
assert SPEC is not None
assert SPEC.loader is not None
replay = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = replay
SPEC.loader.exec_module(replay)

type Point = tuple[Fraction, Fraction]
type Polygon = tuple[Point, ...]


def _rectangle(left: int, bottom: int, right: int, top: int) -> Polygon:
    return (
        (Fraction(left), Fraction(bottom)),
        (Fraction(right), Fraction(bottom)),
        (Fraction(right), Fraction(top)),
        (Fraction(left), Fraction(top)),
    )


def test_distance_decides_crossing_and_tangency_before_vertex_edge_distance() -> None:
    horizontal = _rectangle(-2, -1, 2, 1)
    vertical = _rectangle(-1, -2, 1, 2)
    # These polygons cross, although neither has a vertex inside the other.
    crossing = replay.polygon_distance_squared(horizontal, vertical)
    assert crossing.intersects is True
    assert crossing.squared == 0

    square = _rectangle(0, 0, 1, 1)
    tangent = replay.polygon_distance_squared(square, _rectangle(1, 0, 2, 1))
    assert tangent.intersects is True
    assert tangent.squared == 0

    disjoint = replay.polygon_distance_squared(square, _rectangle(2, 0, 3, 1))
    assert disjoint.intersects is False
    assert disjoint.squared == 1

    bow_tie = (
        (Fraction(0), Fraction(0)),
        (Fraction(1), Fraction(1)),
        (Fraction(0), Fraction(1)),
        (Fraction(1), Fraction(0)),
    )
    with pytest.raises(ValueError, match="convex"):
        replay.polygon_distance_squared(bow_tie, square)


def test_patch_equality_status_requires_a_mark_inside_the_patch() -> None:
    owner = _rectangle(0, 0, 4, 4)
    marks = {"inside": (Fraction(2), Fraction(2))}
    mark_patch = _rectangle(1, 1, 3, 3)
    mark_status = replay.patch_claim_status(owner, mark_patch, marks, Fraction(10))
    assert mark_status["inside_owner_core"] is True
    assert mark_status["common_mark_ids"] == ["inside"]
    assert mark_status["equality_premise_holds"] is True
    assert mark_status["survivor_weight_equals_ten"] is True

    arbitrary_patch = _rectangle(0, 0, 1, 1)
    arbitrary_status = replay.patch_claim_status(owner, arbitrary_patch, marks, Fraction(43, 4))
    assert arbitrary_status["inside_owner_core"] is True
    assert arbitrary_status["common_mark_ids"] == []
    assert arbitrary_status["subset_lower_bound_holds"] is True
    assert arbitrary_status["equality_premise_holds"] is False
    assert arbitrary_status["survivor_weight_equals_ten"] is False

    with pytest.raises(ValueError, match="owner core"):
        replay.patch_claim_status(owner, _rectangle(3, 3, 5, 5), marks, Fraction(10))


def test_retained_replay_covers_all_cases_and_preserves_published_counts() -> None:
    result = replay.replay_geometry(REPO)
    rows = {(row["mark"], row["bins"], row["sector"]): row for row in result["distance_cases"]}
    assert len(rows) == 12

    for key, target in ((("m1", 16, 9), 55), (("m2", 16, 6), 50)):
        row = rows[key]
        assert row["fixed_target"] == target
        assert row["fixed_target_intersects"] is True
        assert Fraction(row["fixed_target_distance_squared"]) == 0
        assert Fraction(row["intersection_area"]) > 0
        assert Fraction(row["nearest_actual_survivor_distance_squared"]) > 0
        assert row["survivor_count"] == 76
        assert row["survivor_weight"] == "19/2"

    for key, row in rows.items():
        if key not in {("m1", 16, 9), ("m2", 16, 6)}:
            assert row["fixed_target_intersects"] is False
            assert Fraction(row["fixed_target_distance_squared"]) > 0
            assert row["survivor_count"] == 80
            assert row["survivor_weight"] == "10"
        assert row["sat_clipping_survivor_sets_identical"] is True
        if row["bins"] == 16:
            assert row["published_survivor_record_identical"] is True

    poses = {row["index"]: row for row in result["pose_rows"]}
    assert set(poses) == {59, 60}
    assert all(row["same_centre_same_angle_unit_parent_contained"] for row in poses.values())
    assert all(row["survivor_weight"] == "10" for row in poses.values())

    counterexample = result["arbitrary_subpatch_counterexample"]
    assert counterexample["owner_core"] == 59
    assert counterexample["corner_index"] == 2
    assert counterexample["patch_area"] == "99540529/10000000000000000"
    assert counterexample["common_mark_ids"] == []
    assert counterexample["survivor_weight"] == "43/4"
    assert counterexample["equality_premise_holds"] is False
    assert result["mark_containing_patch_control"]["survivor_weight_equals_ten"] is True


def test_source_and_published_criteria_mutations_are_rejected() -> None:
    family = REPO / replay.RETAINED_FAMILY_PATH
    with pytest.raises(ValueError, match="40 lowercase hexadecimal"):
        replay.git_blob_binding(REPO, family, "not-a-blob")

    criteria = json.loads((REPO / replay.PUBLISHED_CHILDREN_PATH).read_text())
    changed: dict[str, Any] = deepcopy(criteria)
    changed["bottom-left:m1:J9/16"]["survivor_weight"] = "10"
    with pytest.raises(ValueError, match="survivor weight"):
        replay.parse_published_children(changed)


def test_cli_writes_an_immutable_manifest_and_receipt(tmp_path: Path) -> None:
    output = tmp_path / "receipt"
    assert replay.main(["--repo", str(REPO), "--out", str(output)]) == 0
    manifest = json.loads((output / "source-manifest.json").read_text())
    receipt = json.loads((output / "geometry-receipt.json").read_text())
    assert manifest["schema"] == "h157-geometry-source-manifest-v1"
    assert receipt["schema"] == "h157-geometry-receipt-v1"
    assert receipt["source_manifest"] == manifest
    with pytest.raises(FileExistsError, match="refusing to overwrite"):
        replay.main(["--repo", str(REPO), "--out", str(output)])
