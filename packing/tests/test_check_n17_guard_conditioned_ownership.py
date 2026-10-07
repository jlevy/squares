"""Synthetic strict ownership and closed conditional-complement controls."""

from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

import pytest
from test_check_n17_partner_pose_coupling import rows, synthetic_state, write_fixture

from devtools import check_n17_guard_conditioned_ownership as tool

Q = tool.Q


def deadline() -> float:
    return time.monotonic() + 30


def rectangle(lo: Q, hi: Q) -> list[tool.Point]:
    return [(lo, lo), (hi, lo), (hi, hi), (lo, hi)]


def square_planes() -> list[tool.Plane]:
    return [(Q(1), Q(0), Q(1)), (Q(-1), Q(0), Q(1)), (Q(0), Q(1), Q(1)), (Q(0), Q(-1), Q(1))]


def test_guard_owned_positive_area_and_all_corner_arc_control() -> None:
    centre = (Q(1), Q(1))
    work = tool.new_work()
    owned = tool.guard_owned(centre, work, deadline())
    assert tool.parent.area2(owned) > 0
    for corner in tool.centre_box(centre):
        shifted = [tool.cases.subtract(p, corner) for p in owned]
        assert tool.standing.core_strict(
            shifted, tool.TAU - tool.HALF_WIDTH, tool.TAU + tool.HALF_WIDTH
        )
    assert work["strict_quadratic_checks"] > 0
    assert not (tool.TAU - tool.HALF_WIDTH <= 0 <= tool.TAU + tool.HALF_WIDTH)
    assert not (tool.TAU - tool.HALF_WIDTH <= 1 <= tool.TAU + tool.HALF_WIDTH)


def test_empty_owner0_guard_core_refuses() -> None:
    with pytest.raises(ValueError, match="positive area"):
        tool.guard_owned((Q(100), Q(100)), tool.new_work(), deadline())


def test_ownership_plane_uses_minimum_not_maximum() -> None:
    centres = [(Q(1), Q(1)), (Q(3), Q(1))]
    planes = tool.ownership_planes(centres, Q(0), Q(0), tool.new_work(), deadline())
    for a, b, rhs in planes:
        assert rhs == Q(1, 2) - tool.MARGIN + min(tool.finite.dot(p, (a, b)) for p in centres)
    assert any(
        rhs != Q(1, 2) - tool.MARGIN + max(tool.finite.dot(p, (a, b)) for p in centres)
        for a, b, rhs in planes
    )


@pytest.mark.parametrize("point", [(Q(1, 2), Q(0)), (Q(0), Q(1, 2)), (Q(2, 5), Q(2, 5))])
def test_strict_body_boundary_and_interior_angle_violation(point: tool.Point) -> None:
    assert not tool.strictly_owned(
        [point], [(Q(0), Q(0))], Q(0), Q(1), tool.new_work(), deadline()
    )


@pytest.mark.parametrize(
    "piece",
    [[], [(Q(0), Q(0))], [(Q(-1, 2), Q(0)), (Q(1, 2), Q(0))], rectangle(Q(-1, 2), Q(1, 2))],
)
def test_inside_forbidden_piece_empty_under_closed_complement(piece: list[tool.Point]) -> None:
    result = tool.subtract_piece(piece, square_planes(), tool.new_work(), deadline())
    assert result["empty"]
    assert result["pieces"] == []
    assert all(branch["empty"] for branch in result["branches"])


@pytest.mark.parametrize("piece", [[(Q(1), Q(0))], [(Q(1), Q(-1, 2)), (Q(1), Q(1, 2))]])
def test_forbidden_boundary_points_and_segments_retained(piece: list[tool.Point]) -> None:
    result = tool.subtract_piece(piece, square_planes(), tool.new_work(), deadline())
    assert not result["empty"]
    assert any(all(tool.cases.contains(p, x) for x in piece) for p in result["pieces"])
    assert result["boundary_retained"]


def test_subtraction_is_union_not_intersection_and_preserves_gap_pieces() -> None:
    piece = rectangle(Q(-2), Q(2))
    result = tool.subtract_piece(piece, square_planes(), tool.new_work(), deadline())
    assert any(tool.cases.contains(p, (Q(2), Q(0))) for p in result["pieces"])
    assert any(tool.cases.contains(p, (Q(0), Q(2))) for p in result["pieces"])
    assert not any(tool.cases.contains(p, (Q(0), Q(0))) for p in result["pieces"])
    assert len(result["pieces"]) == 4


def test_forbidden_difference_is_q0_minus_partner_core() -> None:
    q0 = [(Q(2) + x, Q(3) + y) for x, y in rectangle(Q(-1, 4), Q(1, 4))]
    partner = rectangle(Q(-1, 8), Q(1, 8))
    planes = tool.forbidden_planes(q0, partner, deadline())
    for q in q0:
        for d in partner:
            point = tool.cases.subtract(q, d)
            assert all(tool.finite.dot(point, (a, b)) <= rhs for a, b, rhs in planes)
    assert any(tool.finite.dot((Q(-2), Q(-3)), (a, b)) > rhs for a, b, rhs in planes)


def row(centre: tool.Point) -> dict[str, Any]:
    return {"domain": [centre], "interval": ["0", "1"]}


def test_common_owned_intersects_all_rows_and_empty_k_is_not_empty_cover() -> None:
    work = tool.new_work()
    first = tool.common_owned([row((Q(1), Q(1)))], work, deadline())
    assert first
    combined = tool.common_owned([row((Q(1), Q(1))), row((Q(3), Q(1)))], work, deadline())
    assert combined == []
    assert tool.strictly_owned(first, [(Q(1), Q(1))], Q(0), Q(1), tool.new_work(), deadline())
    with pytest.raises(ValueError, match="distinct conditional closure"):
        tool.common_owned([{"domain": [], "interval": ["0", "1"]}], work, deadline())


@pytest.mark.parametrize(
    "groups",
    [
        {0: [(Q(1), Q(1))], 1: [(Q(1), Q(1))]},
        {0: [(Q(0), Q(0)), (Q(2), Q(0))], 1: [(Q(1), Q(-1)), (Q(1), Q(1))]},
        {0: rectangle(Q(0), Q(1)), 1: rectangle(Q(1), Q(2))},
    ],
)
def test_exact_owned_intersection_point_segment_and_touch(
    groups: dict[int, list[tool.Point]],
) -> None:
    closure = tool.shared_owned(groups, tool.new_work(), deadline())
    assert closure is not None
    assert closure["owners"] == [0, 1]
    assert closure["conditional_only"]


def test_empty_and_disjoint_owned_groups_supply_no_closure() -> None:
    assert (
        tool.shared_owned({0: [], 1: rectangle(Q(1), Q(2))}, tool.new_work(), deadline())
        is None
    )
    assert (
        tool.shared_owned({0: [(Q(0), Q(0))], 1: [(Q(1), Q(1))]}, tool.new_work(), deadline())
        is None
    )


def test_primitive_resource_stops_are_not_closures(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(tool, "STRICT_CHECK_LIMIT", 1)
    with pytest.raises(tool.IncompleteError, match="quadratic"):
        tool.strictly_owned(
            [(Q(0), Q(0))], [(Q(0), Q(0))], Q(0), Q(1), tool.new_work(), deadline()
        )
    with pytest.raises(tool.IncompleteError, match="wall"):
        tool.subtract_piece(
            rectangle(Q(0), Q(1)), square_planes(), tool.new_work(), time.monotonic() - 1
        )


@pytest.mark.parametrize("kind", ["shared", "owner_empty", "miss"])
def test_complete_conditional_cover_and_dispositions(kind: str) -> None:
    cells, roles, roster, centre = synthetic_state(positive=kind == "owner_empty")
    if kind == "miss":
        broad = tool.finite.serial(rectangle(Q(3, 4), Q(4)))
        for owner, rows in cells.items():
            if owner != "0":
                rows[0]["residual_polygons"] = [broad]
    result = tool.construct(cells, roles, roster, centre, deadline=deadline())
    assert result["all_original_rows_checked"] == 1056
    assert result["all_foreign_rows_conditioned"] == 992
    assert result["original_endpoint_control"]["all17_retained"]
    assert not result["original_endpoint_control"]["conditional_endpoint_retention_required"]
    if kind == "miss":
        assert result["status"] == "criterion_missed"
        assert any(group == [] for group in result["owned_groups"].values())
        assert result["closure"] is None
    else:
        assert result["status"] == "closed_guard_exclusion"
        expected = (
            "conditional_owner_cover_empty"
            if kind == "owner_empty"
            else "shared_strictly_owned_point"
        )
        assert result["closure"]["kind"] == expected
    for rows in result["conditional_rows"].values():
        for row in rows:
            assert "pieces" not in row
            assert not row["conditional_polygon_coordinates_serialized"]
            assert len(row["source_pieces"]) == row["original_piece_count"]
    assert not result["conditional_geometry_assurance"][
        "geometry_hash_used_instead_of_arithmetic"
    ]


def test_closed_guard_seams_and_actual_fixed_piece_retained() -> None:
    cells, roles, roster, centre = synthetic_state()
    lo, hi = tool.TAU - tool.HALF_WIDTH, tool.TAU + tool.HALF_WIDTH
    cells["0"][25]["interval"][1] = str(lo)
    cells["0"][26]["interval"] = [str(lo), str(hi)]
    cells["0"][27]["interval"][0] = str(hi)
    result = tool.construct(cells, roles, roster, centre, deadline=deadline())
    targets = result["owner0_target_rows"]
    assert [row["row_index"] for row in targets] == [25, 26, 27]
    assert targets[0]["interval"] == [str(lo), str(lo)]
    assert targets[-1]["interval"] == [str(hi), str(hi)]
    cells["0"][26]["residual_polygons"] = []
    with pytest.raises(ValueError, match="actual guard target piece"):
        tool.construct(cells, roles, roster, centre, deadline=deadline())


@pytest.mark.parametrize("kind", ["missing_row", "empty_original", "endpoint"])
def test_original_cover_or_endpoint_failure_refuses_before_conditioning(kind: str) -> None:
    cells, roles, roster, centre = synthetic_state()
    if kind == "missing_row":
        cells["1"].pop()
    elif kind == "empty_original":
        cells["1"][0]["residual_polygons"] = []
    else:
        roster[1]["centre"] = [["100", "100"], ["100", "100"]]
    with pytest.raises(ValueError, match=r"row|endpoint"):
        tool.construct(cells, roles, roster, centre, deadline=deadline())


def descriptor(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> dict[str, Any]:
    return write_fixture(tmp_path, monkeypatch) | {"schema": tool.DESCRIPTOR_SCHEMA}


def test_full_intake_roundtrip_and_compact_alias_tamper(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    doc = descriptor(tmp_path, monkeypatch)
    certificate = tool.generate(doc, deadline=deadline())
    decoded = tool.finite.decode(tool.retained_json.dumps(certificate).encode())
    assert tool.check(doc, decoded, deadline=deadline())["verification_passed"]
    assert all(certificate[key] is False for key in tool.scope())
    assert certificate["parent_custody"]["steps"] == 16
    decoded["conditional_rows"]["1"][0]["source_pieces"][0][0] = 99
    with pytest.raises(ValueError, match="reconstruction differs"):
        tool.check(doc, decoded, deadline=deadline())


def test_post_construction_custody_change_refuses(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    doc = descriptor(tmp_path, monkeypatch)
    original = tool.construct

    def mutate(*args: Any, **kwargs: Any) -> dict[str, Any]:
        result = original(*args, **kwargs)
        path = tmp_path / doc["centered_receipt"]
        path.write_bytes(path.read_bytes() + b"changed")
        return result

    monkeypatch.setattr(tool, "construct", mutate)
    with pytest.raises(ValueError, match="inputs changed"):
        tool.generate(doc, deadline=deadline())


def test_two_fresh_producer_root_free_cli_reconstructions(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    doc = descriptor(tmp_path, monkeypatch)
    path = tmp_path / "guard.json"
    path.write_text(json.dumps(doc))
    outputs = [tmp_path / "generated.json", tmp_path / "fresh.json"]
    code = (
        "from pathlib import Path; import sys; "
        "from devtools import check_n17_guard_conditioned_ownership as t; "
        "t.finite.REPO=Path(sys.argv[1]); raise SystemExit(t.main(sys.argv[2:]))"
    )
    for index, output in enumerate(outputs):
        args = [
            sys.executable,
            "-c",
            code,
            str(tmp_path),
            "--descriptor",
            str(path),
            "--max-seconds",
            "30",
            "--output",
            str(output),
        ]
        if index:
            args.extend(["--certificate", str(outputs[0])])
        completed = subprocess.run(
            args, capture_output=True, text=True, timeout=40, check=False
        )
        assert completed.returncode == 0, completed.stderr + completed.stdout
    first, fresh = [json.loads(p.read_bytes()) for p in outputs]
    assert tool.parent.feasible.witness.payload(first) == tool.parent.feasible.witness.payload(
        fresh
    )
    assert fresh["verification_passed"]
    assert first["invocation"] != fresh["invocation"]


@pytest.mark.parametrize("kind", ["output", "expired", "custody"])
def test_cli_limits_and_refusal_never_promote_exclusion(
    kind: str, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    doc = descriptor(tmp_path, monkeypatch)
    if kind == "custody":
        doc["centered_receipt_sha256"] = "f" * 64
    if kind == "output":
        monkeypatch.setattr(tool, "OUTPUT_LIMIT", 1)
    path, out = tmp_path / "guard.json", tmp_path / "out.json"
    path.write_text(json.dumps(doc))
    seconds = "0.000001" if kind == "expired" else "30"
    assert (
        tool.main(["--descriptor", str(path), "--output", str(out), "--max-seconds", seconds])
        == 1
    )
    result = json.loads(out.read_bytes())
    assert result["status"] == ("refused" if kind == "custody" else "incomplete")
    assert not result["criterion_met"]
    assert all(result[key] is False for key in tool.scope())


def test_compact_source_aliases_preserve_every_duplicate_original_piece() -> None:
    raw = rows(1)[0]
    raw["residual_polygons"] = [[["3", "3"]] for _ in range(70)]
    domain = tool.parent.row_domain(raw, [0], deadline())
    q0 = tool.guard_owned((Q(1), Q(1)), tool.new_work(), deadline())
    result = tool.condition_row(domain, q0, {}, tool.new_work(), deadline())
    assert result["original_piece_count"] == 70
    assert result["conditional_piece_count"] == 1
    assert [source[0] for source in result["source_pieces"]] == list(range(70))
    assert all(source[2] == [0] for source in result["source_pieces"])
    assert all(source[1] is not None and source[3] == [] for source in result["source_pieces"])


@pytest.mark.parametrize(
    "kind",
    [
        "fast_support",
        "recovery_support",
        "generated_vertices",
        "row_pieces",
        "global_pieces",
        "strict_pairs",
    ],
)
def test_each_new_work_ceiling_remains_incomplete(
    kind: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    def operation() -> None:
        if kind == "fast_support":
            monkeypatch.setattr(tool, "FAST_SUPPORT_LIMIT", 0)
            tool.subtract_piece(
                rectangle(Q(-2), Q(2)), square_planes(), tool.new_work(), deadline()
            )
        elif kind == "recovery_support":
            monkeypatch.setattr(tool, "RECOVERY_SUPPORT_LIMIT", 0)
            tool.ownership_planes([(Q(1), Q(1))], Q(0), Q(1), tool.new_work(), deadline())
        elif kind == "generated_vertices":
            monkeypatch.setattr(tool, "GENERATED_VERTEX_LIMIT", 0)
            tool.subtract_piece(
                rectangle(Q(-2), Q(2)), square_planes(), tool.new_work(), deadline()
            )
        elif kind == "strict_pairs":
            monkeypatch.setattr(tool, "STRICT_PAIR_LIMIT", 0)
            tool.strictly_owned(
                [(Q(1), Q(1))], [(Q(1), Q(1))], Q(0), Q(1), tool.new_work(), deadline()
            )
        else:
            monkeypatch.setattr(
                tool,
                "CONDITIONAL_ROW_LIMIT" if kind == "row_pieces" else "CONDITIONAL_PIECE_LIMIT",
                0,
            )
            cells, roles, roster, centre = synthetic_state()
            tool.construct(cells, roles, roster, centre, deadline=deadline())

    with pytest.raises(tool.IncompleteError, match="ceiling"):
        operation()


def test_fixed_witness_inside_aggregate_hull_but_no_actual_piece_refuses() -> None:
    cells, roles, roster, centre = synthetic_state()
    delta = tool.HALF_WIDTH / 2
    points = [(centre[0] - delta, centre[1]), (centre[0] + delta, centre[1])]
    cells["0"][26]["residual_polygons"] = [tool.finite.serial([p]) for p in points]
    assert tool.cases.contains(tool.cases.bounded_hull(points, 256, deadline()), centre)
    with pytest.raises(ValueError, match="actual guard target piece"):
        tool.construct(cells, roles, roster, centre, deadline=deadline())


def test_restricted_angle_wall_clip_output_counter_exact_boundary(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    point = [(Q(1), Q(1))]
    lo, hi = tool.TAU - tool.HALF_WIDTH, tool.TAU + tool.HALF_WIDTH
    monkeypatch.setattr(tool, "GENERATED_VERTEX_LIMIT", 4)
    work = tool.new_work()
    assert tool.guard_wall_clip(point, lo, hi, work, deadline()) == tool.parent.wall_clip(
        point, lo, hi, deadline()
    )
    assert work["generated_clip_output_vertices"] == 4
    monkeypatch.setattr(tool, "GENERATED_VERTEX_LIMIT", 3)
    with pytest.raises(tool.IncompleteError, match="clip-output vertex ceiling"):
        tool.guard_wall_clip(point, lo, hi, tool.new_work(), deadline())


def test_point_guard_core_contains_nonzero_guard_core_and_width_is_frozen() -> None:
    centre = (Q(1), Q(1))
    point = tool.guard_owned(centre, tool.new_work(), deadline(), half_width=Q(0))
    region = tool.guard_owned(centre, tool.new_work(), deadline(), half_width=tool.HALF_WIDTH)
    assert all(tool.cases.contains(point, p) for p in region)
    assert tool.parent.area2(point) >= tool.parent.area2(region) > 0
    with pytest.raises(ValueError, match="half-width differs"):
        tool.centre_box(centre, Q(1, 1024))


def test_point_miss_skips_region_and_original_reconstruction_shared(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    cells, roles, roster, centre = synthetic_state()
    broad = tool.finite.serial(rectangle(Q(3, 4), Q(4)))
    for owner, raw in cells.items():
        if owner != "0":
            raw[0]["residual_polygons"] = [broad]
    original = tool.parent.row_domain
    calls = []

    def count(*args: Any, **kwargs: Any) -> dict[str, Any]:
        calls.append(1)
        return original(*args, **kwargs)

    monkeypatch.setattr(tool.parent, "row_domain", count)
    result = tool.construct(cells, roles, roster, centre, deadline=deadline())
    assert len(calls) == 1056
    assert result["status"] == "criterion_missed"
    assert not result["point_guard_excluded"]
    assert not result["regional_context_started"]
    assert result["regional_skip_reason"] == "complete_point_miss_monotonic_inclusion"
    assert [c["guard"]["half_width"] for c in result["contexts"]] == ["0"]


def test_two_context_piece_storage_cap_is_per_context_work_is_cumulative(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    cells, roles, roster, centre = synthetic_state()
    monkeypatch.setattr(tool, "CONDITIONAL_PIECE_LIMIT", 17)
    original = tool.parent.row_domain
    calls = []

    def count(*args: Any, **kwargs: Any) -> dict[str, Any]:
        calls.append(1)
        return original(*args, **kwargs)

    monkeypatch.setattr(tool.parent, "row_domain", count)
    result = tool.construct(cells, roles, roster, centre, deadline=deadline())
    assert len(calls) == 1056
    assert result["criterion_met"]
    assert result["point_guard_excluded"]
    assert [c["context_retained_pieces"] for c in result["contexts"]] == [17, 17]
    assert result["work"]["retained_conditional_pieces"] == 34
    first, last = [c["work"] for c in result["contexts"]]
    assert all(last[key] >= value for key, value in first.items())
    assert result["contexts"][0]["point_guard_exclusion_proved"]
    assert not result["contexts"][0]["declared_guard_exclusion_proved"]
    assert result["contexts"][1]["declared_guard_exclusion_proved"]


def test_second_context_shared_clip_cap_retains_point_only_candidate(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    cells, roles, roster, centre = synthetic_state()
    monkeypatch.setattr(tool, "GENERATED_VERTEX_LIMIT", 8)
    with pytest.raises(tool.ContextIncompleteError, match="clip-output") as caught:
        tool.construct(cells, roles, roster, centre, deadline=deadline())
    partial = caught.value.observations
    assert partial["point_guard_exclusion_candidate"]
    assert partial["unfinished_context_half_width"] == str(tool.HALF_WIDTH)
    assert len(partial["completed_contexts"]) == 1
    assert partial["work"]["generated_clip_output_vertices"] == 9
    assert not partial["partial_custody_recheck_complete"]


def test_complete_secondary_point_only_is_not_primary_regional_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    cells, roles, roster, centre = synthetic_state()
    original = tool.condition_context

    def region_miss(*args: Any, **kwargs: Any) -> dict[str, Any]:
        result = original(*args, **kwargs)
        if kwargs["half_width"]:
            result.update(
                closure=None,
                status="criterion_missed",
                criterion_met=False,
                declared_guard_exclusion_proved=False,
            )
        return result

    monkeypatch.setattr(tool, "condition_context", region_miss)
    result = tool.construct(cells, roles, roster, centre, deadline=deadline())
    assert result["status"] == "fixed_witness_only"
    assert result["point_guard_excluded"]
    assert result["regional_context_started"]
    assert result["closure"] is None
    assert not result["criterion_met"]
    assert not result["declared_guard_exclusion_proved"]


def test_cli_second_context_stop_retains_candidate_without_primary_claim(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    doc = descriptor(tmp_path, monkeypatch)
    monkeypatch.setattr(tool, "GENERATED_VERTEX_LIMIT", 14)
    path, output = tmp_path / "paired.json", tmp_path / "partial.json"
    path.write_text(json.dumps(doc))
    assert (
        tool.main(["--descriptor", str(path), "--output", str(output), "--max-seconds", "30"])
        == 1
    )
    result = json.loads(output.read_bytes())
    assert result["status"] == "incomplete"
    assert result["point_guard_exclusion_candidate"]
    assert not result["criterion_met"]
    assert not result["declared_guard_exclusion_proved"]
    assert all(result[key] is False for key in tool.scope())
