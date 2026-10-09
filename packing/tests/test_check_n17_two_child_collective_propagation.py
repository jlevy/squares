"""Synthetic closed-case finite implications; inherited premises are not real packings."""

from __future__ import annotations

import copy
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

import pytest
from test_check_n17_one_round_owned_domain_propagation import direct_fixture

from devtools import check_n17_two_child_collective_propagation as tool

Q = tool.Q


def child_environment() -> dict[str, str]:
    """Import the selected checkout in a fresh process, preserving caller settings."""
    project = Path(__file__).resolve().parents[1]
    return os.environ | {"PYTHONPATH": os.pathsep.join((str(project / "src"), str(project)))}


def deadline() -> float:
    return time.monotonic() + 60


def square(x: Q, y: Q, radius: Q) -> list[tool.Point]:
    return [
        (x - radius, y - radius),
        (x + radius, y - radius),
        (x + radius, y + radius),
        (x - radius, y + radius),
    ]


def geometry() -> tuple[Any, Any]:
    rows = {
        o: [
            {
                "reference": {"synthetic": [o, i]},
                "interval": [
                    str(Q(i, 32 if o == 12 else 64)),
                    str(Q(i + 1, 32 if o == 12 else 64)),
                ],
                "domain": [(Q(4), Q(4))] if o != 18 else [(Q(2), Q(2))] if i == 0 else [],
            }
            for i in range(32 if o == 12 else 64)
        ]
        for o in tool.OWNERS[1:]
    }
    groups = {o: [] for o in tool.OWNERS}
    groups[0] = square(Q(1, 4), Q(1, 4), Q(1, 10))
    return rows, groups


def flags(
    rows: Any, *, side: int, excluded: set[tuple[int, int]], closed: bool = False
) -> dict[str, Any]:
    return {
        "side": side,
        "closed": closed,
        "surviving_rows": {
            str(o): [
                {
                    "row_index": i,
                    "reference": copy.deepcopy(r["reference"]),
                    "interval": list(r["interval"]),
                    "live": bool(r["domain"]) and not closed and (o, i) not in excluded,
                }
                for i, r in enumerate(entries)
            ]
            for o, entries in rows.items()
        },
    }


@pytest.mark.parametrize(
    "polygon",
    [[(Q(471, 250), Q(2))], [(Q(1), Q(2)), (Q(3), Q(2))], square(Q(471, 250), Q(2), Q(1, 10))],
)
def test_closed_clips_retain_shared_seam_and_original_rows(polygon: list[tool.Point]) -> None:
    rows = [{"reference": {"closed": True}, "interval": ["0", "1"], "domain": polygon}]
    work = {"generated_clip_vertices": 0}
    lower, upper = (tool.clip_rows(rows, side, work, deadline()) for side in (-1, 1))
    assert tool.cases.contains(lower[0]["domain"], (tool.MIDPOINT, Q(2)))
    assert tool.cases.contains(upper[0]["domain"], (tool.MIDPOINT, Q(2)))
    assert lower[0]["reference"] == upper[0]["reference"] == rows[0]["reference"]
    assert rows[0]["domain"] == polygon


def test_one_closed_case_is_not_whole_guard_exclusion() -> None:
    rows, groups = geometry()
    result = tool.construct(rows, groups, deadline=deadline())
    assert result["closed_case_count"] == 1
    assert result["children"][0]["closure"]["kind"] == "selected_owner_cover_empty"
    assert result["children"][1]["collective_rows_accounted"] == 992
    assert result["criterion_met"] is False
    assert result["declared_guard_exclusion_proved"] is False
    assert result["children"][1]["other_owned_groups_unchanged"]


def test_both_cases_strict_common_owned_intersection_closes_region() -> None:
    rows, groups = geometry()
    for row in rows[18]:
        if row["domain"]:
            row["domain"] = [(tool.MIDPOINT, Q(2))]
    groups[1] = [(tool.MIDPOINT, Q(2))]
    result = tool.construct(rows, groups, deadline=deadline())
    assert result["both_children_closed"]
    assert result["declared_guard_exclusion_proved"]
    assert result["point_guard_exclusion_proved"] is False
    assert all(c["closure"]["owners"] == [18, 1] for c in result["children"])
    assert all(c["collective"] is None for c in result["children"])


@pytest.mark.parametrize(
    ("excluded_right", "expected"), [(set(), "0"), ({(1, 10)}, "1/64"), ({(1, 11)}, "0")]
)
def test_survivors_union_precedes_additional_length(
    excluded_right: set[tuple[int, int]], expected: str
) -> None:
    rows, _groups = geometry()
    children = [
        flags(rows, side=-1, excluded={(1, 10)}),
        flags(rows, side=1, excluded=excluded_right),
    ]
    result = tool.combine(rows, children, deadline())
    entry = next(r for r in result if r["owner"] == 1)
    assert entry["additional_lost_length"] == expected
    if expected == "1/64":
        assert entry["combined_surviving_closed_interval_union"] == [
            ["0", "5/32"],
            ["11/64", "1"],
        ]


def test_closed_case_with_surviving_child_no_false_combined_gain() -> None:
    rows, _groups = geometry()
    result = tool.combine(
        rows,
        [
            flags(rows, side=-1, excluded=set(), closed=True),
            flags(rows, side=1, excluded=set()),
        ],
        deadline(),
    )
    assert all(r["additional_lost_length"] == "0" for r in result)


def test_selected_intersection_singleton_least_other_and_precharge(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    groups = {o: [] for o in tool.OWNERS}
    groups[18] = groups[1] = groups[2] = [(Q(1), Q(1))]
    work = {"intersection_vertex_pairs": 0}
    intersection = tool.selected_intersection(groups, work, deadline())
    assert intersection is not None
    assert intersection["owners"] == [18, 1]
    monkeypatch.setattr(tool, "INTERSECTION_PRODUCTS", 0)
    monkeypatch.setattr(
        tool.cases.conditional,
        "intersection",
        lambda *_a: pytest.fail("unprecharged primitive"),
    )
    with pytest.raises(tool.IncompleteError, match="intersection product"):
        tool.selected_intersection(groups, {"intersection_vertex_pairs": 0}, deadline())


def test_cumulative_clip_ceiling_and_second_case_partial_is_not_proof(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    rows, groups = geometry()
    monkeypatch.setattr(tool, "CLIP_VERTICES", 0)
    with pytest.raises(tool.guard.ContextIncompleteError) as found:
        tool.construct(rows, groups, deadline=deadline())
    refusal = tool.failure(found.value)
    assert refusal["status"] == "incomplete"
    assert refusal["criterion_met"] is False
    assert len(refusal["candidate_observations"]["finished_children_candidates"]) == 1
    assert all(refusal[k] is False for k in tool.scope())


def test_recovery_support_ceiling_never_creates_accepted_branch(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    rows, groups = geometry()
    monkeypatch.setattr(tool.guard, "RECOVERY_SUPPORT_LIMIT", 0)
    with pytest.raises(tool.IncompleteError, match="support"):
        tool.construct(rows, groups, deadline=deadline())


def test_exact_union_hole_is_not_covered_just_because_vertices_are() -> None:
    p = square(Q(0), Q(0), Q(1))
    regions = [(1, 0, square(Q(-1), Q(0), Q(1))), (2, 1, square(Q(1), Q(0), Q(1)))]
    # Move the facing edges apart while retaining all four target vertices.
    regions[0] = (1, 0, [(Q(-2), Q(-1)), (Q(-1, 2), Q(-1)), (Q(-1, 2), Q(1)), (Q(-2), Q(1))])
    regions[1] = (2, 1, [(Q(1, 2), Q(-1)), (Q(2), Q(-1)), (Q(2), Q(1)), (Q(1, 2), Q(1))])
    result = tool.collective.cover_row(p, regions, tool.collective.new_work(), deadline())
    assert result["covered"] is False
    assert result["primitive"] == "covered_by_sweep"


def fixture(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> dict[str, Any]:
    """Synthetic accepted base proof, not a seventeen-square packing certificate."""
    original_doc = direct_fixture(tmp_path, monkeypatch)
    with monkeypatch.context() as context:
        # Empty inherited groups are legitimate no-information premises.
        context.setattr(tool.guard, "common_owned", lambda *_a: [])
        accepted = tool.previous.generate(original_doc, deadline=deadline())
    assert accepted["status"] == "criterion_missed"
    selection = {
        "schema": tool.selection_tool.SCHEMA,
        "status": "criterion_missed",
        "criterion_met": False,
        "selection": {"owner": 18, "axis": 0, "midpoint": "471/250"},
        "parent_custody": copy.deepcopy(accepted["parent_custody"]),
    }

    def retain(name: str, value: Any) -> tuple[str, str]:
        raw = json.dumps(value, sort_keys=True).encode()
        path = tmp_path / (name + ".json")
        path.write_bytes(raw)
        return path.name, hashlib.sha256(raw).hexdigest()

    doc = {"schema": tool.DESCRIPTOR_SCHEMA}
    for role, value in zip(
        tool.ROLES,
        (
            original_doc,
            accepted,
            accepted | {"verification_passed": True},
            selection,
            selection | {"verification_passed": True},
        ),
        strict=True,
    ):
        doc[role], doc[role + "_sha256"] = retain("two-case-" + role, value)
    return doc


def test_generate_inherits_base_proof_and_freshly_reconstructs_new_geometry(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    doc = fixture(tmp_path, monkeypatch)
    monkeypatch.setattr(
        tool.previous, "generate", lambda *_a, **_k: pytest.fail("base replay forbidden")
    )
    monkeypatch.setattr(
        tool.previous.regional,
        "regional_decision",
        lambda *_a, **_k: pytest.fail("prior collective replay forbidden"),
    )
    result = tool.generate(doc, deadline=deadline())
    fresh = tool.check(doc, result, deadline=deadline())
    assert fresh["verification_passed"]
    assert result["base_proof_inherited"]
    assert result["base_collective_arithmetic_replayed"] is False
    assert result["base_foreign_rows_accounted"] == 992
    assert result["selection_point_geometry_used"] is False


@pytest.mark.parametrize(
    "tamper", ["mode", "baseline", "row", "guard", "selection", "fresh", "native"]
)
def test_accepted_custody_and_typed_rows_refuse_tamper(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, tamper: str
) -> None:
    doc = fixture(tmp_path, monkeypatch)
    role = "selection_certificate" if tamper == "selection" else "propagation_certificate"
    path = tmp_path / doc[role]
    accepted = json.loads(path.read_text())
    if tamper == "mode":
        accepted["mode"] = "fixed_core_regional"
    elif tamper == "baseline":
        accepted["prior_component_parameter_loss"] = "25/64"
    elif tamper == "row":
        accepted["new_collective"]["owners"][0]["rows"][0]["reference"] = {"invented": True}
    elif tamper == "guard":
        accepted["guard"]["half_width"] = "1/8388608"
    elif tamper == "selection":
        accepted["selection"]["midpoint"] = "2"
    elif tamper == "fresh":
        role = "propagation_replay"
        path = tmp_path / doc[role]
        accepted = json.loads(path.read_text())
        accepted["verification_passed"] = False
    else:
        (tmp_path / "node-synthetic.json.gz").write_bytes(b"tampered opaque native")
    if tamper != "native":
        path.write_text(json.dumps(accepted, sort_keys=True))
        doc[role + "_sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
        if tamper != "fresh":
            replay_role = role.replace("certificate", "replay")
            replay_path = tmp_path / doc[replay_role]
            replay_path.write_text(
                json.dumps(accepted | {"verification_passed": True}, sort_keys=True)
            )
            doc[replay_role + "_sha256"] = hashlib.sha256(replay_path.read_bytes()).hexdigest()
    with pytest.raises(ValueError, match=r"differs|identity|roster|required|bytes"):
        tool.generate(doc, deadline=deadline())


def test_two_clean_processes_match_new_finite_payload(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    doc = fixture(tmp_path, monkeypatch)
    descriptor = tmp_path / "descriptor.json"
    descriptor.write_text(json.dumps(doc))
    runner = tmp_path / "runner.py"
    runner.write_text(
        "import sys\nfrom pathlib import Path\n"
        "from devtools import check_n17_two_child_collective_propagation as t\n"
        "t.finite.REPO=Path(sys.argv[1])\n"
        "raise SystemExit(t.main(sys.argv[2:]))\n"
    )
    generated, fresh = tmp_path / "generated.json", tmp_path / "fresh.json"
    args = [
        sys.executable,
        str(runner),
        str(tmp_path),
        "--descriptor",
        str(descriptor),
        "--max-seconds",
        "60",
    ]
    for tail in (
        ["--output", str(generated)],
        ["--certificate", str(generated), "--output", str(fresh)],
    ):
        process = subprocess.run(
            [*args, *tail],
            env=child_environment(),
            capture_output=True,
            text=True,
            timeout=90,
            check=False,
        )
        assert process.returncode == 0, process.stdout + process.stderr
    left, right = json.loads(generated.read_text()), json.loads(fresh.read_text())
    assert tool.payload(left) == tool.payload(right)
    assert right["verification_passed"]
    assert right["point_guard_exclusion_proved"] is False
