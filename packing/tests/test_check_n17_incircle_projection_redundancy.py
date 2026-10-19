"""Synthetic projections are not scientific seventeen-square witnesses."""

from __future__ import annotations

import copy
import itertools
import time
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import pytest

from devtools import check_n17_incircle_projection_redundancy as tool


def fixture(*, small: bool = False) -> tuple[Any, ...]:
    # Every catalogue cell overlaps; only the finite relaxation is under test.
    lo, hi = (Q(1), Q(11, 10)) if small else (Q(1, 2), tool.U - Q(1, 2))
    polygon = [(lo, lo), (hi, lo), (hi, hi), (lo, hi)]
    polygons = [polygon[:] for _ in range(24)]
    names = [f"synthetic-{i}" for i in range(24)]
    masks = [
        sum(1 << i for i in cells)
        for cells in itertools.islice(itertools.combinations(range(24), 17), 95)
    ]
    return polygons, names, [{"mask": m} for m in masks]


def run(data: tuple[Any, ...]) -> dict[str, Any]:
    return tool.construct(*data, deadline=time.monotonic() + 60)


@pytest.mark.parametrize(
    ("point", "inside"),
    [
        ((Q(0), Q(0)), True),
        ((Q(1), Q(0)), False),
        ((Q(-1), Q(0)), False),
        ((Q(0), Q(-1)), False),
        ((Q(0), Q(1)), False),
        ((Q(7, 10), Q(7, 10)), False),
        ((Q(-7, 10), Q(7, 10)), False),
        ((Q(7, 10), Q(-7, 10)), False),
        ((Q(-7, 10), Q(-7, 10)), False),
        ((Q(1) - Q(1, 2**100), Q(0)), True),
        ((Q(1) + Q(1, 2**100), Q(0)), False),
    ],
)
def test_octagon_strict_boundary_and_narrow_gap(point: tool.Point, *, inside: bool) -> None:
    work = {"face_checks": 0}
    result = tool.vertex_cover([point], work, time.monotonic() + 10)
    assert (result[0] is None) == inside
    assert work["face_checks"] == 8


def test_nonvertex_inside_does_not_imply_strict_projection_cut() -> None:
    points = [(Q(-1), Q(0)), (Q(1), Q(0))]
    assert all(
        x is not None
        for x in tool.vertex_cover(points, {"face_checks": 0}, time.monotonic() + 10)
    )
    assert tool.vertex_cover([(Q(0), Q(0))], {"face_checks": 0}, time.monotonic() + 10) == [
        None
    ]
    with pytest.raises(ValueError, match="canonical"):
        _ = tool.vertex_cover(
            [points[0], (Q(0), Q(0)), points[1]], {"face_checks": 0}, time.monotonic() + 10
        )


def test_exact_wall_projection_preserves_point_segment_and_closed_seam() -> None:
    deadline = time.monotonic() + 10
    point = (Q(1, 2), Q(1, 2))
    assert tool.centre_projection([point], deadline) == [point]
    assert tool.centre_projection([(Q(0), Q(1)), (Q(1), Q(1))], deadline) == [
        (Q(1, 2), Q(1)),
        (Q(1), Q(1)),
    ]
    with pytest.raises(ValueError, match="empty unconditioned"):
        _ = tool.centre_projection([(Q(0), Q(0))], deadline)


def test_difference_sign_and_degenerate_hull() -> None:
    work = {"vertex_differences": 0}
    result = tool.difference_hull([(Q(0), Q(0))], [(Q(2), Q(3))], work, time.monotonic() + 10)
    assert result == [(Q(2), Q(3))]
    assert work["vertex_differences"] == 1


def test_complete_redundancy_and_joint_relaxation_not_physical_packing() -> None:
    result = run(fixture())
    assert result["complete_classification"] is True
    assert result["criterion_met"] is False
    assert result["all95_shared_convexified_relaxations_redundant"] is True
    assert result["work"]["state_pairs_accounted"] == 12920
    assert len(result["states"]) == 95
    assert all(
        s["pairs_accounted"] == 136 and s["shared_convexified_relaxation_witness_checked"]
        for s in result["states"]
    )
    assert all(result[k] is False for k in tool.scope())
    assert (
        result["states"][0]["uncoupled_centre_vertices"][0]
        == result["states"][0]["uncoupled_centre_vertices"][1]
    )


def test_inside_extreme_selects_only_potential_lp_cut() -> None:
    result = run(fixture(small=True))
    assert result["criterion_met"] is True
    assert result["potential_cut_pairs"]
    assert result["shared_center_LP_solved"] is False
    assert result["ordinary_assignment_exclusion_proved"] is False
    assert all(not s["shared_convexified_relaxation_witness_checked"] for s in result["states"])


@pytest.mark.parametrize("change", ["missing", "duplicate", "bool"])
def test_bad95_mask_roster_refuses(change: str) -> None:
    data = fixture()
    if change == "missing":
        data[2].pop()
    elif change == "duplicate":
        data[2][-1] = data[2][0]
    else:
        data[2][0]["mask"] = True
    with pytest.raises(ValueError, match=r"roster|typed"):
        _ = run(data)


def test_work_budget_precharges_and_used_big_coordinate(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(tool, "DIFFERENCE_LIMIT", 0)
    work = {"vertex_differences": 0}
    with pytest.raises(tool.finite.IncompleteError, match="difference"):
        _ = tool.difference_hull([(Q(0), Q(0))], [(Q(1), Q(1))], work, time.monotonic() + 10)
    assert work["vertex_differences"] == 1
    monkeypatch.setattr(tool, "FACE_LIMIT", 0)
    with pytest.raises(tool.finite.IncompleteError, match="face"):
        _ = tool.vertex_cover([(Q(0), Q(0))], {"face_checks": 0}, time.monotonic() + 10)
    with pytest.raises(tool.finite.IncompleteError, match="bit"):
        _ = tool.centre_projection([(Q(1 << 4096), Q(0))], time.monotonic() + 10)
    with pytest.raises(tool.finite.IncompleteError, match="wall"):
        _ = tool.centre_projection([(Q(1), Q(1))], time.monotonic() - 1)


def test_fresh_intake_once_no_saved_pose_or_corner_run(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    data = fixture(small=True)
    p = tmp_path / "premise.json"
    raw = b"{}"
    _ = p.write_bytes(raw)
    calls = []

    def intake(document: Any, _deadline: float) -> tuple[Any, ...]:
        assert document["schema"] == tool.prior.CONTEXT_SCHEMA
        calls.append("intake")
        return (*data, {"unused_saved_pose": ["1e999999999"]}, {p: raw})

    monkeypatch.setattr(tool.prior, "intake", intake)

    def forbidden(*_args: Any, **_kwargs: Any) -> Any:
        raise AssertionError("saved pose/classification/DP must not run")

    monkeypatch.setattr(tool.prior, "construct", forbidden)
    for name in ("construct", "classify", "capacity_dp", "generate", "check"):
        monkeypatch.setattr(tool.prior.corner, name, forbidden)
    document = {"schema": tool.CONTEXT_SCHEMA}
    result = tool.generate(document, deadline=time.monotonic() + 60)
    fresh = tool.check(document, result, deadline=time.monotonic() + 60)
    assert tool.payload(result) == tool.payload(fresh)
    assert fresh["verification_passed"] is True
    assert calls == ["intake", "intake"]
    changed = copy.deepcopy(result)
    changed["pairs"][0]["strict_inside_extreme_indices"] = []
    with pytest.raises(ValueError, match="fresh"):
        _ = tool.check(document, changed, deadline=time.monotonic() + 60)
    _ = p.write_bytes(b"changed")
    with pytest.raises(ValueError, match="premise bytes"):
        _ = tool.generate(document, deadline=time.monotonic() + 60)


def test_failure_scope_and_descriptor_refusal() -> None:
    for error, status in [
        (ValueError("malformed"), "refused"),
        (tool.finite.IncompleteError("wall"), "incomplete"),
    ]:
        result = tool.failure(error)
        assert result["status"] == status
        assert result["criterion_met"] is False
        assert result["complete_classification"] is False
        assert all(result[k] is False for k in tool.scope())
    with pytest.raises(ValueError, match="schema"):
        _ = tool.generate([], deadline=time.monotonic() + 10)


def test_minkowski_nonextreme_zero_is_removed_before_octagon_decision() -> None:
    segment = [(Q(0), Q(0)), (Q(2), Q(0))]
    d = tool.difference_hull(segment, segment, {"vertex_differences": 0}, time.monotonic() + 10)
    assert d == [(Q(-2), Q(0)), (Q(2), Q(0))]
    assert all(
        face is not None
        for face in tool.vertex_cover(d, {"face_checks": 0}, time.monotonic() + 10)
    )


def test_fixed_octagon_vertex_enclosure_and_all_signed_faces() -> None:
    assert len(set(tool.FACES)) == 8
    vertices = [(Q(-1), Q(0)), (Q(1), Q(0)), (Q(0), Q(-1)), (Q(0), Q(1))]
    vertices += [(Q(7 * s, 10), Q(7 * t, 10)) for s, t in itertools.product((-1, 1), repeat=2)]
    for x, y in vertices:
        assert x * x + y * y <= 1
        assert all(a * x + b * y <= 7 for a, b in tool.FACES)
