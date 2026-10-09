"""Target-free closed child coverage and accepted-premise custody controls."""

from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

import pytest

from devtools import check_n17_two_center_children as tool

Q = tool.Q


def deadline() -> float:
    return time.monotonic() + 30


def work() -> dict[str, int]:
    return {"generated_clip_vertices": 0, "intersection_vertex_pairs": 0}


def rectangle(lo: Q, hi: Q) -> list[tool.Point]:
    return [(lo, lo), (hi, lo), (hi, hi), (lo, hi)]


def context() -> dict[str, Any]:
    rows = {}
    for owner in tool.OWNERS[1:]:
        count = 32 if owner == 12 else 64
        rows[str(owner)] = [
            {
                "reference": {"kind": "wall_seed", "owner": owner, "row": i},
                "interval": [str(Q(i, count)), str(Q(i + 1, count))],
                "domain": [["3", "3"]] if i == 0 else [],
            }
            for i in range(count)
        ]
    groups = {str(o): [] if o in tool.CANDIDATES else [["1", "1"]] for o in tool.OWNERS}
    groups["0"] = tool.finite.serial(rectangle(Q(9, 10), Q(11, 10)))
    return {
        "guard": {
            "half_width": "0",
            "angle_interval": ["53/128", "53/128"],
            "centre_box": [["1", "1"], ["1", "1"]],
        },
        "all_original_rows_checked": 1056,
        "all_foreign_rows_conditioned": 992,
        "owned_groups": groups,
        "conditional_rows": rows,
    }


def fixture(tmp_path: Path) -> dict[str, Any]:
    ctx = context()
    guard_descriptor = {"schema": tool.guard.DESCRIPTOR_SCHEMA}
    accepted = {
        "schema": tool.guard.SCHEMA,
        "status": "criterion_missed",
        "accepted_inputs": guard_descriptor,
        "contexts": [ctx],
        "regional_context_started": False,
        "closure": None,
        "point_closure": None,
        "constants": tool.guard.constants(),
        "container": tool.guard.standing.CenteredContainer(tool.cases.U, tool.cases.V).record(),
        "criterion_met": False,
        "point_guard_exclusion_proved": False,
        "matched_owned_point_witness": {"tau": "53/128", "centre": ["1", "1"]},
        "original_endpoint_control": {
            "all17_retained": True,
            "family_disjoint": True,
            "witnesses": [{"label": i, "owner": o} for i, o in enumerate(tool.OWNERS, 1)],
        },
        "parent_custody": {
            "steps": 16,
            "typed_reference_context": {
                "node_id": "synthetic",
                "step_owners": [o for o in tool.OWNERS if o != 12],
            },
        },
    }
    doc = {"schema": tool.DESCRIPTOR_SCHEMA}
    for role, value in zip(
        tool.ROLES,
        (guard_descriptor, accepted, accepted | {"verification_passed": True}),
        strict=True,
    ):
        raw = json.dumps(value, sort_keys=True).encode()
        path = tmp_path / f"{role}.json"
        path.write_bytes(raw)
        doc[role] = path.name
        doc[role + "_sha256"] = hashlib.sha256(raw).hexdigest()
    return doc


@pytest.mark.parametrize("side", [-1, 1])
def test_closed_cut_keeps_point_segment_and_seam(side: int) -> None:
    midpoint = Q(1)
    pts = [(Q(0), Q(2)), (Q(2), Q(2))]
    clipped = tool.closed_clip(pts, 0, midpoint, side, work(), deadline())
    assert (midpoint, Q(2)) in clipped
    assert tool.closed_clip([(midpoint, Q(2))], 0, midpoint, side, work(), deadline()) == [
        (midpoint, Q(2))
    ]


def test_selector_ties_owner_then_x_before_y() -> None:
    rows, groups = tool.context_geometry(
        context(), {"node_id": "synthetic", "step_owners": []}, deadline()
    )
    selected = tool.select(rows, groups, work(), deadline())
    assert selected["owner"] == 5
    assert selected["axis"] == 0
    assert selected["midpoint"] == "3"
    assert selected["candidate_count"] == 20


def test_selector_minimizes_worst_child_diagonal() -> None:
    rows, groups = tool.context_geometry(
        context(), {"node_id": "synthetic", "step_owners": []}, deadline()
    )
    for owner in tool.CANDIDATES:
        for row in rows[owner]:
            row["domain"] = [(Q(1), Q(1)), (Q(4), Q(1)), (Q(4), Q(2)), (Q(1), Q(2))]
    result = tool.select(rows, groups, work(), deadline())
    assert result["axis"] == 0
    assert Q(result["worst_child_squared_diagonal"]) == Q(13, 4)


def test_candidate_set_cannot_silently_change() -> None:
    rows, groups = tool.context_geometry(
        context(), {"node_id": "synthetic", "step_owners": []}, deadline()
    )
    groups[5] = [(Q(1), Q(1))]
    with pytest.raises(ValueError, match="ten empty"):
        tool.select(rows, groups, work(), deadline())


def test_one_child_closure_is_not_complete() -> None:
    rows = {
        5: [{"reference": {}, "interval": ["0", "0"], "domain": [(Q(3), Q(3)), (Q(4), Q(3))]}]
    }
    groups = {0: [(Q(13, 4), Q(3))], 5: []}
    result = tool.children(
        rows,
        groups,
        {"owner": 5, "axis": 0, "midpoint": "7/2"},
        work(),
        tool.guard.new_work(),
        deadline(),
    )
    assert result["children"][0]["closed"]
    assert not result["children"][1]["closed"]
    assert not result["both_children_closed"]


def test_both_children_exact_strict_touch_closes() -> None:
    rows = {5: [{"reference": {}, "interval": ["0", "0"], "domain": [(Q(3), Q(3))]}]}
    groups = {0: [(Q(3), Q(3))], 5: []}
    result = tool.children(
        rows,
        groups,
        {"owner": 5, "axis": 0, "midpoint": "3"},
        work(),
        tool.guard.new_work(),
        deadline(),
    )
    assert result["both_children_closed"]
    assert all(r["closure"]["owners"] == [5, 0] for r in result["children"])


def test_empty_child_is_distinct_from_empty_owned_information() -> None:
    rows = {
        5: [{"reference": {}, "interval": ["0", "1"], "domain": [(Q(2), Q(2)), (Q(4), Q(4))]}]
    }
    result = tool.children(
        rows,
        {0: [], 5: []},
        {"owner": 5, "axis": 0, "midpoint": "1"},
        work(),
        tool.guard.new_work(),
        deadline(),
    )
    assert result["children"][0]["closure"]["kind"] == "complete_child_owner_empty"
    assert result["children"][1]["owned"] == []
    assert not result["children"][1]["closed"]


@pytest.mark.parametrize("kind", ["row", "seam", "reference", "owner", "big"])
def test_full_closed_geometry_and_resource_refusals(kind: str) -> None:
    raw = context()
    if kind == "row":
        raw["conditional_rows"]["5"].pop()
    if kind == "seam":
        raw["conditional_rows"]["5"][1]["interval"][0] = "1/65"
    if kind == "reference":
        raw["conditional_rows"]["5"][0]["reference"]["owner"] = 7
    if kind == "owner":
        raw["owned_groups"].pop("21")
    if kind == "big":
        raw["conditional_rows"]["5"][0]["domain"] = [[str(2**4100), "3"]]
    with pytest.raises((ValueError, tool.IncompleteError)):
        tool.context_geometry(raw, {"node_id": "synthetic", "step_owners": []}, deadline())


def test_generated_clip_and_intersection_counters_are_bounded(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(tool, "GENERATED_LIMIT", 0)
    with pytest.raises(tool.IncompleteError, match="clip vertex"):
        tool.closed_clip([(Q(1), Q(1))], 0, Q(1), 1, work(), deadline())


def test_point_miss_skips_regional_and_fresh_roundtrip(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(tool.finite, "REPO", tmp_path)
    doc = fixture(tmp_path)

    def forbidden(*_args: Any, **_kwargs: Any) -> Any:
        raise AssertionError("regional branch must not run")

    monkeypatch.setattr(tool, "regional", forbidden)
    result = tool.generate(doc, deadline=deadline())
    assert result["status"] == "criterion_missed"
    assert not result["regional_context_started"]
    assert tool.check(doc, json.loads(json.dumps(result)), deadline=deadline())[
        "verification_passed"
    ]
    changed = copy.deepcopy(result)
    changed["selection"]["midpoint"] = "4"
    with pytest.raises(ValueError, match="reconstruction"):
        tool.check(doc, changed, deadline=deadline())


@pytest.mark.parametrize("role", tool.ROLES)
def test_accepted_input_byte_tampering_refuses(
    role: str, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(tool.finite, "REPO", tmp_path)
    doc = fixture(tmp_path)
    (tmp_path / doc[role]).write_text("{}")
    with pytest.raises(ValueError, match="custody"):
        tool.generate(doc, deadline=deadline())


def test_two_fresh_clean_cli_processes(tmp_path: Path) -> None:
    doc = fixture(tmp_path)
    descriptor = tmp_path / "context.json"
    descriptor.write_text(json.dumps(doc))
    outputs = [tmp_path / "first.json", tmp_path / "fresh.json"]
    for index, path in enumerate(outputs):
        argv = [
            sys.executable,
            "-c",
            (
                "import sys; from pathlib import Path; "
                "from devtools import check_n17_two_center_children as t; "
                "t.finite.REPO=Path(sys.argv[1]); raise SystemExit(t.main(sys.argv[2:]))"
            ),
            str(tmp_path),
            "--descriptor",
            str(descriptor),
            "--max-seconds",
            "30",
            "--output",
            str(path),
        ]
        if index:
            argv += ["--certificate", str(outputs[0])]
        completed = subprocess.run(
            argv, capture_output=True, text=True, timeout=35, check=False
        )
        assert completed.returncode == 0, completed.stderr + path.read_text()
    first, fresh = [json.loads(p.read_text()) for p in outputs]
    assert tool.payload(first) == tool.payload(fresh)
    assert fresh["verification_passed"]


def test_expired_deadline_never_accepts(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(tool.finite, "REPO", tmp_path)
    with pytest.raises(tool.IncompleteError):
        tool.generate(fixture(tmp_path), deadline=0)


@pytest.mark.parametrize("field", ["angle", "centre", "tau", "container", "constants"])
def test_fixed_witness_and_container_join_refuses(
    field: str, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(tool.finite, "REPO", tmp_path)
    doc = fixture(tmp_path)
    certificate = json.loads((tmp_path / doc["guard_certificate"]).read_text())
    if field == "angle":
        certificate["contexts"][0]["guard"]["angle_interval"] = ["0", "0"]
    elif field == "centre":
        certificate["contexts"][0]["guard"]["centre_box"][0] = ["2", "2"]
    elif field == "tau":
        certificate["matched_owned_point_witness"]["tau"] = "0"
    elif field == "container":
        certificate["container"]["inner_V"] = "4"
    else:
        certificate["constants"]["margin"] = "0"
    for role, value in (
        ("guard_certificate", certificate),
        ("guard_replay", certificate | {"verification_passed": True}),
    ):
        raw = json.dumps(value).encode()
        (tmp_path / doc[role]).write_bytes(raw)
        doc[role + "_sha256"] = hashlib.sha256(raw).hexdigest()
    with pytest.raises(ValueError, match="differs"):
        tool.generate(doc, deadline=deadline())


@pytest.mark.parametrize("regional_closes", [False, True])
def test_point_secondary_and_same_cut_regional_primary(
    regional_closes: bool,  # noqa: FBT001
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(tool.finite, "REPO", tmp_path)
    doc = fixture(tmp_path)
    called = []

    def child(
        _rows: Any,
        _groups: Any,
        selection: dict[str, Any],
        _work: Any,
        _recovery: Any,
        _deadline: Any,
    ) -> dict[str, Any]:
        called.append(copy.deepcopy(selection))
        return {
            "both_children_closed": True if len(called) == 1 else regional_closes,
            "children": [{"closed": True}, {"closed": True}],
        }

    monkeypatch.setattr(tool, "children", child)

    def region(_document: Any, _accepted: Any, _held: Any, _deadline: Any) -> dict[str, Any]:
        return context() | {"work": {}}

    monkeypatch.setattr(tool, "regional", region)
    result = tool.generate(doc, deadline=deadline())
    assert result["point_guard_exclusion_proved"]
    assert result["criterion_met"] is regional_closes
    assert result["declared_guard_exclusion_proved"] is regional_closes
    assert called[0] == called[1]


def test_regional_timeout_retains_only_point_candidates(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(tool.finite, "REPO", tmp_path)
    doc = fixture(tmp_path)
    monkeypatch.setattr(
        tool, "children", lambda *_a: {"both_children_closed": True, "children": []}
    )

    def stop(*_args: Any) -> Any:
        raise tool.IncompleteError("regional wall ceiling")

    monkeypatch.setattr(tool, "regional", stop)
    with pytest.raises(tool.guard.ContextIncompleteError) as caught:
        tool.generate(doc, deadline=deadline())
    observations = caught.value.observations
    assert observations["point_guard_exclusion_candidate"]
    assert not observations["verification_passed"]
    assert observations["completed_contexts_are_candidates_only"]


def test_closed_clip_nesting_for_fixed_cut() -> None:
    small = rectangle(Q(1), Q(2))
    large = rectangle(Q(0), Q(3))
    for side in (-1, 1):
        a = tool.closed_clip(small, 0, Q(3, 2), side, work(), deadline())
        b = tool.closed_clip(large, 0, Q(3, 2), side, work(), deadline())
        assert all(tool.cases.contains(b, p) for p in a)
