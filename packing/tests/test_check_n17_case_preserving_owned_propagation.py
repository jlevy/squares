"""Synthetic complete case rosters and fresh finite implications; no target inputs."""

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

from devtools import check_n17_case_preserving_owned_propagation as tool

Q = tool.Q


def child_environment() -> dict[str, str]:
    """Import the selected checkout in a fresh process, preserving caller settings."""
    project = Path(__file__).resolve().parents[1]
    return os.environ | {"PYTHONPATH": os.pathsep.join((str(project / "src"), str(project)))}


def deadline() -> float:
    return time.monotonic() + 60


def geometry() -> tuple[Any, Any]:
    rows = {
        o: [
            {
                "reference": {"synthetic": [o, i]},
                "interval": [
                    str(Q(i, 32 if o == 12 else 64)),
                    str(Q(i + 1, 32 if o == 12 else 64)),
                ],
                "domain": [(Q(4), Q(4))] if o != 18 else [(tool.prior.MIDPOINT, Q(2))],
            }
            for i in range(32 if o == 12 else 64)
        ]
        for o in tool.OWNERS[1:]
    }
    groups = {o: [] for o in tool.OWNERS}
    groups[0] = [
        (Q(1, 10), Q(1, 10)),
        (Q(2, 10), Q(1, 10)),
        (Q(2, 10), Q(2, 10)),
        (Q(1, 10), Q(2, 10)),
    ]
    return rows, groups


def coverage(rows: Any, excluded: set[tuple[int, int]] | None = None) -> dict[str, Any]:
    excluded = excluded or set()
    effective = copy.deepcopy(rows)
    entries = []
    for owner in tool.OWNERS[1:]:
        decisions = []
        for i, r in enumerate(rows[owner]):
            covered = not r["domain"] or (owner, i) in excluded
            decisions.append(
                {
                    "row_index": i,
                    "reference": copy.deepcopy(r["reference"]),
                    "interval": list(r["interval"]),
                    "covered": covered,
                    "inherited_domain_nonempty": bool(r["domain"]),
                    "domain_retained_unchanged": bool(r["domain"]) and not covered,
                }
            )
            if covered:
                effective[owner][i]["domain"] = []
        before, after = (
            tool.prior.interval_union(rows[owner]),
            tool.prior.interval_union(effective[owner]),
        )

        def length(u):
            return tool.collective.length([tuple(map(Q, p)) for p in u])

        entries.append(
            {
                "owner": owner,
                "rows": decisions,
                "old_closed_interval_union": before,
                "new_closed_interval_union": after,
                "lost_length": str(length(before) - length(after)),
            }
        )
    return {
        "all_foreign_rows_accounted": 992,
        "owners": entries,
        "complete_empty_owners": [
            o for o in tool.OWNERS[1:] if not any(r["domain"] for r in effective[o])
        ],
        "work": tool.collective.new_work(),
        "case_groups_frozen_during_collective_pass": True,
        "point_guard_necessary_domain_restriction_proved": False,
        "point_contradiction_proved": False,
        "original_owned_sets_unchanged": True,
        "simultaneous_original_groups_only": True,
    }


def fixture(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> dict[str, Any]:
    rows, groups = geometry()
    original = {
        "guard": {"half_width": "1/512"},
        "container": {"synthetic": True},
        "parent_custody": {"synthetic": True},
        "original_endpoint_control": {"synthetic": True},
    }
    monkeypatch.setattr(tool.finite, "REPO", tmp_path)
    monkeypatch.setattr(
        tool.prior,
        "intake",
        lambda *_a: (copy.deepcopy(rows), copy.deepcopy(groups), copy.deepcopy(original), {}),
    )
    children = []
    for side in (-1, 1):
        child = copy.deepcopy(rows)
        child[18] = tool.prior.clip_rows(
            child[18], side, {"generated_clip_vertices": 0}, deadline()
        )
        cov = coverage(child, {(6, 10)})
        effective = tool.apply_case_decisions(child, cov, deadline())
        children.append(
            {
                **tool.flags(effective, side, closed=False),
                "closure": None,
                "other_owned_groups_unchanged": True,
                "collective_rows_accounted": 992,
                "collective": cov,
                "selected_owned_group": [],
                "selected_owner_clipped_rows": [
                    {
                        "row_index": i,
                        "reference": r["reference"],
                        "interval": r["interval"],
                        "domain": tool.finite.serial(r["domain"]),
                    }
                    for i, r in enumerate(child[18])
                ],
                "halfplane": {
                    "axis": 0,
                    "relation": "<=" if side == -1 else ">=",
                    "midpoint": str(tool.prior.MIDPOINT),
                },
            }
        )
    descriptor = {"synthetic": True}
    accepted = {
        "schema": tool.prior.SCHEMA,
        "accepted_inputs": descriptor,
        "status": "additional_angle_union_restricted",
        "criterion_met": True,
        **tool.scope(progress=True),
        **original,
        "closed_case_count": 0,
        "both_children_closed": False,
        "survivors_unioned_across_cases": True,
        "no_sequential_feedback": True,
        "base_foreign_rows_accounted": 992,
        "original_rows_inherited": 1056,
        "fixed_selection": {"owner": 18, "axis": 0, "midpoint": str(tool.prior.MIDPOINT)},
        "children": children,
        "combined_restrictions": tool.prior.combine(rows, children, deadline()),
    }
    doc = {"schema": tool.DESCRIPTOR_SCHEMA}
    for role, value in zip(
        tool.ROLES,
        (descriptor, accepted, accepted | {"verification_passed": True}),
        strict=True,
    ):
        path = tmp_path / (role + ".json")
        path.write_text(json.dumps(value, sort_keys=True))
        doc[role] = path.name
        doc[role + "_sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
    return doc


def mocks(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(tool, "common_owned", lambda *_a: [])
    monkeypatch.setattr(
        tool.collective, "construct", lambda rows, _groups, **_k: coverage(rows)
    )


def test_generate_fresh_full992_each_and_baseline_not_recounted(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    doc = fixture(tmp_path, monkeypatch)
    mocks(monkeypatch)
    result = tool.generate(doc, deadline=deadline())
    fresh = tool.check(doc, result, deadline=deadline())
    assert fresh["verification_passed"]
    assert result["status"] == "criterion_missed"
    assert result["changed_owners"] == []
    assert result["accepted_cases_arithmetic_replayed"] is False
    assert all(
        c["collective_rows_accounted"] == 992 and c["all16_recoveries_completed"]
        for c in result["children"]
    )
    assert (
        next(r for r in result["combined_restrictions"] if r["owner"] == 6)[
            "additional_lost_length"
        ]
        == "0"
    )
    assert result["declared_guard_exclusion_proved"] is False


@pytest.mark.parametrize(
    "tamper",
    ["row", "side", "domain", "flag", "baseline", "context", "fresh", "roster", "sha", "scope"],
)
def test_complete_case_custody_refuses_tamper(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, tamper: str
) -> None:
    doc = fixture(tmp_path, monkeypatch)
    path = tmp_path / doc["cases_certificate"]
    a = json.loads(path.read_text())
    if tamper == "row":
        a["children"][0]["collective"]["owners"][0]["rows"][0]["reference"] = {}
    elif tamper == "side":
        a["children"][0]["side"] = 1
    elif tamper == "domain":
        a["children"][0]["selected_owner_clipped_rows"][0]["domain"] = []
    elif tamper == "flag":
        a["children"][0]["surviving_rows"]["6"][10]["live"] = True
    elif tamper == "baseline":
        a["combined_restrictions"][0]["combined_surviving_closed_interval_union"] = []
    elif tamper == "context":
        a["guard"]["half_width"] = "0"
    elif tamper == "roster":
        a["children"][0]["collective"]["owners"][0]["rows"].pop()
    elif tamper == "scope":
        a["global_optimality_proved"] = True
    elif tamper == "sha":
        path.write_text("{}")
    if tamper != "sha":
        path.write_text(json.dumps(a))
        doc["cases_certificate_sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
        replay = tmp_path / doc["cases_replay"]
        replay.write_text(json.dumps(a | {"verification_passed": tamper != "fresh"}))
        doc["cases_replay_sha256"] = hashlib.sha256(replay.read_bytes()).hexdigest()
    with pytest.raises((ValueError, KeyError), match=r"differ|required|bytes|premise"):
        tool.intake(doc, deadline())


@pytest.mark.parametrize(
    ("right", "expected"), [(set(), "0"), ({(1, 11)}, "0"), ({(1, 10)}, "1/64")]
)
def test_case_correlation_and_or_before_length(
    right: set[tuple[int, int]], expected: str
) -> None:
    base, _ = geometry()
    old = [tool.flags(base, s, closed=False) for s in (-1, 1)]
    baseline = tool.prior.combine(base, old, deadline())
    children = []
    for side, excluded in zip((-1, 1), ({(1, 10)}, right), strict=True):
        effective = tool.apply_case_decisions(base, coverage(base, excluded), deadline())
        children.append(tool.flags(effective, side, closed=False))
    result = tool.compare_combined(base, baseline, children, deadline())
    assert result[0]["additional_lost_length"] == expected


def test_one_closed_case_no_gain_both_closed_exclusion(monkeypatch: pytest.MonkeyPatch) -> None:
    base, groups = geometry()
    baseline = tool.prior.combine(
        base, [tool.flags(base, s, closed=False) for s in (-1, 1)], deadline()
    )
    monkeypatch.setattr(
        tool,
        "case_result",
        lambda rows, _g, side, _w, _d: {
            **tool.flags(rows, side, closed=side == -1),
            "collective": None,
        },
    )
    result = tool.construct(base, [base, base], groups, baseline, deadline=deadline())
    assert not result["criterion_met"]
    assert result["closed_case_count"] == 1
    monkeypatch.setattr(
        tool,
        "case_result",
        lambda rows, _g, side, _w, _d: {
            **tool.flags(rows, side, closed=True),
            "collective": None,
        },
    )
    result = tool.construct(base, [base, base], groups, baseline, deadline=deadline())
    assert result["both_children_closed"]
    assert result["declared_guard_exclusion_proved"]
    assert result["global_optimality_proved"] is False


def test_shared_seam_clip_and_empty_group_not_empty_cover(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    rows, groups = geometry()
    mocks(monkeypatch)
    for side in (-1, 1):
        clipped = tool.prior.clip_rows(
            rows[18], side, {"generated_clip_vertices": 0}, deadline()
        )
        assert all(r["domain"] == rows[18][i]["domain"] for i, r in enumerate(clipped))
    r = tool.case_result(rows, groups, -1, tool.guard.new_work(), deadline())
    assert r["closed"] is False
    rows[1] = [{**r, "domain": []} for r in rows[1]]
    r = tool.case_result(rows, groups, -1, tool.guard.new_work(), deadline())
    assert r["closure"]["kind"] == "accepted_case_owner_cover_empty"


def test_local_recovery_matches_reference_both_axes_and_closed_arc() -> None:
    rows = [{"domain": [(Q(1), Q(1))], "interval": ["13/32", "27/64"]}]
    left, right = tool.guard.new_work(), tool.guard.new_work()
    assert tool.common_owned(rows, left, deadline()) == tool.guard.common_owned(
        rows, right, deadline()
    )
    assert left == right
    boundary = [(Q(3, 2), Q(1))]
    assert (
        tool.strictly_owned(
            boundary, [(Q(1), Q(1))], Q(0), Q(0), tool.guard.new_work(), deadline()
        )
        is False
    )


@pytest.mark.parametrize(
    ("key", "capname", "call"),
    [
        ("minimum_support_products", "RECOVERY_SUPPORT_LIMIT", "planes"),
        ("strict_vertex_pairs", "STRICT_PAIR_LIMIT", "strict"),
        ("strict_quadratic_checks", "STRICT_CHECK_LIMIT", "strict"),
    ],
)
def test_shared_recovery_precharge_and_exact_boundary(
    monkeypatch: pytest.MonkeyPatch, key: str, capname: str, call: str
) -> None:
    monkeypatch.setattr(tool, capname, 1)
    work = tool.guard.new_work()
    work[key] = 1
    operation = (
        (lambda: tool.ownership_planes([(Q(1), Q(1))], Q(0), Q(0), work, deadline()))
        if call == "planes"
        else (
            lambda: tool.strictly_owned(
                [(Q(1), Q(1))], [(Q(1), Q(1))], Q(0), Q(0), work, deadline()
            )
        )
    )
    with pytest.raises(tool.IncompleteError, match="ceiling"):
        operation()
    assert work[key] == 2


def test_singleton_intersection_lex_and_precharge(monkeypatch: pytest.MonkeyPatch) -> None:
    groups = {o: [] for o in tool.OWNERS}
    groups[1] = groups[2] = [(Q(1), Q(1))]
    result = tool.shared_intersection(groups, tool.guard.new_work(), deadline())
    assert result is not None
    assert result["owners"] == [1, 2]
    monkeypatch.setattr(tool, "INTERSECTION_PRODUCTS", 0)
    monkeypatch.setattr(
        tool.cases.conditional, "intersection", lambda *_a: pytest.fail("before charge")
    )
    with pytest.raises(tool.IncompleteError, match="product"):
        tool.shared_intersection(groups, tool.guard.new_work(), deadline())


def test_all16_recovered_before_collective_and_no_feedback(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    rows, groups = geometry()
    snapshot = copy.deepcopy(rows)
    order = []

    def recovery(_rows: Any, _work: Any, _deadline: float) -> list[Any]:
        order.append("recover")
        return []

    def collective(r: Any, g: Any, **_k: Any) -> Any:
        assert len(order) == 16
        assert set(g) == set(tool.OWNERS)
        order.append("collective")
        return coverage(r)

    monkeypatch.setattr(tool, "common_owned", recovery)
    monkeypatch.setattr(tool.collective, "construct", collective)
    result = tool.case_result(rows, groups, -1, tool.guard.new_work(), deadline())
    assert rows == snapshot
    assert result["closed"] is False
    assert order[-1] == "collective"


def test_second_case_incomplete_retains_candidate_no_primary(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    rows, groups = geometry()
    baseline = tool.prior.combine(
        rows, [tool.flags(rows, s, closed=False) for s in (-1, 1)], deadline()
    )

    def child(r: Any, _g: Any, side: int, _w: Any, _d: Any) -> Any:
        if side == 1:
            raise tool.IncompleteError("second case")
        return {**tool.flags(r, side, closed=True), "collective": None}

    monkeypatch.setattr(tool, "case_result", child)
    with pytest.raises(tool.guard.ContextIncompleteError) as found:
        tool.construct(rows, [rows, rows], groups, baseline, deadline=deadline())
    failure = tool.failure(found.value)
    assert failure["criterion_met"] is False
    assert failure["status"] == "incomplete"
    assert len(failure["candidate_observations"]["finished_children_candidates"]) == 1
    assert all(failure[k] is False for k in tool.scope())


def test_descriptor_extra_and_nonfinite_cli_refuse(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    doc = fixture(tmp_path, monkeypatch)
    doc["extra"] = True
    with pytest.raises(ValueError, match="descriptor"):
        tool.intake(doc, deadline())
    with pytest.raises(SystemExit):
        tool.main(
            [
                "--descriptor",
                "unused",
                "--output",
                str(tmp_path / "out"),
                "--max-seconds",
                "nan",
            ]
        )


def test_post_computation_byte_mutation_refuses(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    doc = fixture(tmp_path, monkeypatch)
    mocks(monkeypatch)
    original = tool.construct

    def mutate(*args: Any, **kwargs: Any) -> Any:
        result = original(*args, **kwargs)
        (tmp_path / doc["cases_certificate"]).write_text("{}")
        return result

    monkeypatch.setattr(tool, "construct", mutate)
    with pytest.raises(ValueError, match="premise changed"):
        tool.generate(doc, deadline=deadline())


def test_conflicting_transitive_alias_refuses(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    doc = fixture(tmp_path, monkeypatch)
    rows, groups = geometry()
    accepted = json.loads((tmp_path / doc["cases_certificate"]).read_text())
    monkeypatch.setattr(
        tool.prior,
        "intake",
        lambda *_a: (
            rows,
            groups,
            accepted,
            {tmp_path / doc["cases_certificate"]: ("0" * 64, tool.OUTPUT_LIMIT)},
        ),
    )
    with pytest.raises(ValueError, match="aliases"):
        tool.intake(doc, deadline())


def test_clean_two_process_reconstruction_with_explicit_synthetic_premises(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    doc = fixture(tmp_path, monkeypatch)
    descriptor = tmp_path / "descriptor.json"
    descriptor.write_text(json.dumps(doc))
    runner = tmp_path / "runner.py"
    runner.write_text(
        "import sys,json,copy\nfrom pathlib import Path\n"
        "from devtools import check_n17_case_preserving_owned_propagation as t\n"
        f"sys.path.insert(0,{str(Path(__file__).parent)!r})\n"
        "from test_check_n17_case_preserving_owned_propagation import geometry,coverage\n"
        "t.finite.REPO=Path(sys.argv[1])\n"
        "d=json.loads(Path(sys.argv[2]).read_text())\n"
        'a=json.loads((t.finite.REPO/d["cases_certificate"]).read_text())\n'
        "r,g=geometry()\n"
        "t.prior.intake=lambda *_a:(copy.deepcopy(r),copy.deepcopy(g),a,{})\n"
        "t.common_owned=lambda *_a:[]\n"
        "t.collective.construct=lambda rows,_g,**_k:coverage(rows)\n"
        "raise SystemExit(t.main(sys.argv[3:]))\n"
    )
    generated, fresh = tmp_path / "generated.json", tmp_path / "fresh.json"
    for tail in (
        ["--output", str(generated)],
        ["--certificate", str(generated), "--output", str(fresh)],
    ):
        run = subprocess.run(
            [
                sys.executable,
                str(runner),
                str(tmp_path),
                str(descriptor),
                "--descriptor",
                str(descriptor),
                "--max-seconds",
                "60",
                *tail,
            ],
            env=child_environment(),
            capture_output=True,
            text=True,
            timeout=70,
            check=False,
        )
        assert run.returncode == 0, run.stdout + run.stderr
    left, right = json.loads(generated.read_text()), json.loads(fresh.read_text())
    assert tool.payload(left) == tool.payload(right)
    assert right["verification_passed"] is True
    assert left["accepted_cases_arithmetic_replayed"] is False
    assert all(c["collective_rows_accounted"] == 992 for c in left["children"])


@pytest.mark.parametrize(
    ("left", "right"),
    [
        ([(Q(0), Q(0))], [(Q(0), Q(0))]),
        ([(Q(0), Q(0)), (Q(1), Q(0))], [(Q(1), Q(0)), (Q(2), Q(0))]),
    ],
)
def test_closed_point_segment_intersections_not_self_owner(left: Any, right: Any) -> None:
    groups = {o: [] for o in tool.OWNERS}
    groups[1], groups[2] = left, right
    result = tool.shared_intersection(groups, tool.guard.new_work(), deadline())
    assert result is not None
    assert result["owners"] == [1, 2]
    groups[2] = []
    assert tool.shared_intersection(groups, tool.guard.new_work(), deadline()) is None
