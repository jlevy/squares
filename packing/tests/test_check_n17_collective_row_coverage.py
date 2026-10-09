"""Target-free collective closed-row union coverage controls."""

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

from devtools import check_n17_collective_row_coverage as tool

prior = tool.prior
Q = tool.Q


def deadline() -> float:
    return time.monotonic() + 30


def rectangle(lo: Q, hi: Q) -> list[prior.Point]:
    return [(lo, lo), (hi, lo), (hi, hi), (lo, hi)]


def context() -> dict[str, Any]:
    rows = {}
    for owner in prior.OWNERS[1:]:
        count = 32 if owner == 12 else 64
        rows[str(owner)] = [
            {
                "reference": {"kind": "wall_seed", "owner": owner, "row": i},
                "interval": [str(Q(i, count)), str(Q(i + 1, count))],
                "domain": [["3", "3"]] if i == 0 else [],
            }
            for i in range(count)
        ]
    groups = {str(o): [] if o in prior.CANDIDATES else [["1", "1"]] for o in prior.OWNERS}
    groups["0"] = prior.finite.serial(rectangle(Q(9, 10), Q(11, 10)))
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


def parent_fixture(tmp_path: Path) -> dict[str, Any]:
    ctx = context()
    guard_descriptor = {"schema": prior.guard.DESCRIPTOR_SCHEMA}
    accepted = {
        "schema": prior.guard.SCHEMA,
        "status": "criterion_missed",
        "accepted_inputs": guard_descriptor,
        "contexts": [ctx],
        "regional_context_started": False,
        "closure": None,
        "point_closure": None,
        "constants": prior.guard.constants(),
        "container": prior.guard.standing.CenteredContainer(
            prior.cases.U, prior.cases.V
        ).record(),
        "criterion_met": False,
        "point_guard_exclusion_proved": False,
        "matched_owned_point_witness": {"tau": "53/128", "centre": ["1", "1"]},
        "original_endpoint_control": {
            "all17_retained": True,
            "family_disjoint": True,
            "witnesses": [{"label": i, "owner": o} for i, o in enumerate(prior.OWNERS, 1)],
        },
        "parent_custody": {
            "steps": 16,
            "typed_reference_context": {
                "node_id": "synthetic",
                "step_owners": [o for o in prior.OWNERS if o != 12],
            },
        },
    }
    doc = {"schema": prior.DESCRIPTOR_SCHEMA}
    for role, value in zip(
        prior.ROLES,
        (guard_descriptor, accepted, accepted | {"verification_passed": True}),
        strict=True,
    ):
        raw = json.dumps(value, sort_keys=True).encode()
        path = tmp_path / f"{role}.json"
        path.write_bytes(raw)
        doc[role] = path.name
        doc[role + "_sha256"] = hashlib.sha256(raw).hexdigest()
    return doc


def fixture(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, *, positive: bool = False
) -> dict[str, Any]:
    monkeypatch.setattr(tool.finite, "REPO", tmp_path)
    base = parent_fixture(tmp_path)
    if positive:
        # Synthetic inherited-premise plumbing; no physical17-packing claim.
        value = json.loads((tmp_path / base["guard_certificate"]).read_text())
        value["contexts"][0]["conditional_rows"]["5"][0]["domain"] = [["1", "1"]]
        value["contexts"][0]["conditional_rows"]["5"][1]["domain"] = [["3", "3"]]
        for role in ("guard_certificate", "guard_replay"):
            saved = (
                value if role == "guard_certificate" else value | {"verification_passed": True}
            )
            raw = json.dumps(saved, sort_keys=True).encode()
            (tmp_path / base[role]).write_bytes(raw)
            base[role + "_sha256"] = hashlib.sha256(raw).hexdigest()
    route = prior.generate(base, deadline=deadline())
    fresh = prior.check(base, route, deadline=deadline())
    doc = {"schema": tool.DESCRIPTOR_SCHEMA, **{k: v for k, v in base.items() if k != "schema"}}
    for role, value in zip(tool.ROLES[-2:], (route, fresh), strict=True):
        raw = json.dumps(value, sort_keys=True).encode()
        path = tmp_path / (role + ".json")
        path.write_bytes(raw)
        doc[role] = path.name
        doc[role + "_sha256"] = hashlib.sha256(raw).hexdigest()
    return doc


def box(x0: Q, y0: Q, x1: Q, y1: Q) -> list[tool.Point]:
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def reg(*polygons: list[tool.Point]) -> list[tuple[int, int, list[tool.Point]]]:
    return [(i + 1, i, p) for i, p in enumerate(polygons)]


def test_collective_union_without_single_cover() -> None:
    domain = box(Q(0), Q(0), Q(2), Q(2))
    left = box(Q(0), Q(0), Q(1), Q(2))
    right = box(Q(1), Q(0), Q(2), Q(2))
    assert not tool.cover_row(domain, reg(left), tool.new_work(), deadline())["covered"]
    assert not tool.cover_row(domain, reg(right), tool.new_work(), deadline())["covered"]
    result = tool.cover_row(domain, reg(left, right), tool.new_work(), deadline())
    assert result["covered"]
    assert result["primitive"] == "covered_by_sweep"


def test_covered_vertices_do_not_hide_interior_hole() -> None:
    domain = box(Q(0), Q(0), Q(4), Q(4))
    low = box(Q(0), Q(0), Q(4), Q(1))
    high = box(Q(0), Q(3), Q(4), Q(4))
    result = tool.cover_row(domain, reg(low, high), tool.new_work(), deadline())
    assert result["primitive"] == "covered_by_sweep"
    assert not result["covered"]
    assert result["sweep_probe"] is not None


@pytest.mark.parametrize("domain", [[(Q(1), Q(0))], [(Q(0), Q(0)), (Q(2), Q(0))]])
def test_degenerate_and_boundary_coverage(domain: list[tool.Point]) -> None:
    left = box(Q(0), Q(-1), Q(1), Q(0))
    right = box(Q(1), Q(-1), Q(2), Q(0))
    assert tool.cover_row(domain, reg(left, right), tool.new_work(), deadline())["covered"]


def test_vertex_outside_shortcut_is_exact(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        tool.guard.standing, "covered_by_sweep", lambda *_: pytest.fail("sweep called")
    )
    result = tool.cover_row(
        box(Q(0), Q(0), Q(2), Q(2)),
        reg(box(Q(0), Q(0), Q(1), Q(1))),
        tool.new_work(),
        deadline(),
    )
    assert not result["covered"]
    assert result["negative_vertex"] == ["0", "2"]


def test_closed_interval_union_retains_seams_and_avoids_double_count() -> None:
    intervals = [(Q(0), Q(1, 2)), (Q(1, 2), Q(1)), (Q(1, 2), Q(1, 2))]
    assert tool.union_intervals(intervals) == [(Q(0), Q(1))]
    assert tool.length(intervals) == 1
    assert tool.union_intervals([(Q(1, 2), Q(1, 2))]) == [(Q(1, 2), Q(1, 2))]
    assert tool.length([(Q(1, 2), Q(1, 2))]) == 0


@pytest.mark.parametrize("shape", [[(Q(2), Q(3))], [(Q(2), Q(3)), (Q(3), Q(3))]])
def test_minkowski_sign_degenerate_owned_set_and_cache(shape: list[tool.Point]) -> None:
    groups = {0: shape, 1: shape}
    cache, cores, saved, work = {}, {}, [], tool.new_work()
    regions = tool.regions_for(1, Q(0), Q(1, 64), groups, cache, cores, saved, work, deadline())
    assert [o for o, _i, _p in regions] == [0]
    assert all(tool.cases.contains(regions[0][2], p) for p in shape)
    assert not tool.cases.contains(regions[0][2], (-Q(2), -Q(3)))
    tool.regions_for(1, Q(0), Q(1, 64), groups, cache, cores, saved, work, deadline())
    assert work["region_cache_misses"] == 1
    assert work["region_cache_hits"] == 1


@pytest.mark.parametrize("cap", ["MINK_LIMIT", "POINT_PRODUCTS", "EDGE_PAIRS"])
def test_work_caps_are_incomplete(cap: str, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(tool, cap, 0)
    if cap == "MINK_LIMIT":
        with pytest.raises(tool.IncompleteError):
            tool.regions_for(
                1, Q(0), Q(1, 64), {0: [(Q(0), Q(0))]}, {}, {}, [], tool.new_work(), deadline()
            )
    else:
        with pytest.raises(tool.IncompleteError):
            tool.cover_row(
                box(Q(0), Q(0), Q(1), Q(1)),
                reg(box(Q(-1), Q(-1), Q(2), Q(2))),
                tool.new_work(),
                deadline(),
            )


def test_generate_fresh_negative_all992_and_owned_sets_unchanged(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    doc = fixture(tmp_path, monkeypatch)
    before = copy.deepcopy(doc)
    result = tool.generate(doc, deadline=deadline())
    assert result["status"] == "criterion_missed"
    assert result["all_foreign_rows_accounted"] == 992
    assert result["original_owned_sets_unchanged"]
    assert result["simultaneous_original_groups_only"]
    assert doc == before
    assert tool.check(doc, result, deadline=deadline())["verification_passed"]
    result["criterion_met"] = True
    with pytest.raises(ValueError, match="fresh collective"):
        tool.check(doc, result, deadline=deadline())


@pytest.mark.parametrize("role", tool.ROLES)
def test_changed_premise_bytes_refused(
    role: str, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    doc = fixture(tmp_path, monkeypatch)
    (tmp_path / doc[role]).write_text("{}")
    with pytest.raises(ValueError, match="custody"):
        tool.generate(doc, deadline=deadline())


def test_missing_row_refused(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    doc = fixture(tmp_path, monkeypatch)
    path = tmp_path / doc["guard_certificate"]
    value = json.loads(path.read_text())
    value["contexts"][0]["conditional_rows"]["18"].pop()
    json.dumps(value, sort_keys=True).encode()
    for role in ("guard_certificate", "guard_replay"):
        saved = value if role == "guard_certificate" else value | {"verification_passed": True}
        data = json.dumps(saved, sort_keys=True).encode()
        (tmp_path / doc[role]).write_bytes(data)
        doc[role + "_sha256"] = hashlib.sha256(data).hexdigest()
    with pytest.raises(ValueError, match="row"):
        tool.generate(doc, deadline=deadline())


def test_two_fresh_cli_processes(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    doc = fixture(tmp_path, monkeypatch)
    descriptor = tmp_path / "context.json"
    descriptor.write_text(json.dumps(doc))
    outputs = [tmp_path / "first.json", tmp_path / "fresh.json"]
    for i, path in enumerate(outputs):
        argv = [
            sys.executable,
            "-c",
            (
                "import sys; from pathlib import Path; "
                "from devtools import check_n17_collective_row_coverage as t; "
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
        if i:
            argv += ["--certificate", str(outputs[0])]
        completed = subprocess.run(
            argv, capture_output=True, text=True, timeout=35, check=False
        )
        assert completed.returncode == 0, completed.stderr + path.read_text()
    first, fresh = [json.loads(p.read_text()) for p in outputs]
    assert tool.payload(first) == tool.payload(fresh)
    assert fresh["verification_passed"]


def test_expired_deadline_has_no_result(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    doc = fixture(tmp_path, monkeypatch)
    with pytest.raises(tool.IncompleteError):
        tool.generate(doc, deadline=time.monotonic() - 1)


def test_complete_positive_angle_loss_fresh_and_adjacent_closed_seam(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    doc = fixture(tmp_path, monkeypatch, positive=True)
    result = tool.generate(doc, deadline=deadline())
    owner = next(x for x in result["owners"] if x["owner"] == 5)
    assert owner["lost_length"] == "1/64"
    assert owner["old_closed_interval_union"] == [["0", "1/32"]]
    assert owner["new_closed_interval_union"] == [["1/64", "1/32"]]
    assert owner["rows"][0]["covered"]
    assert owner["rows"][1]["domain_retained_unchanged"]
    assert result["criterion_met"]
    assert result["point_guard_necessary_domain_restriction_proved"]
    assert not result["declared_guard_exclusion_proved"]
    assert not result["conditional_I_exclusion_proved"]
    assert not result["point_guard_exclusion_proved"]
    assert tool.check(doc, result, deadline=deadline())["verification_passed"]


def test_original_owned_groups_not_modified_in_simultaneous_pass() -> None:
    rows, groups = tool.context_geometry(
        context(), {"node_id": "synthetic", "step_owners": []}, deadline()
    )
    before = copy.deepcopy(groups)
    result = tool.construct(rows, groups, deadline=deadline())
    assert groups == before
    assert result["simultaneous_original_groups_only"]


def test_complete_owner_empty_is_point_secondary_only() -> None:
    rows, groups = tool.context_geometry(
        context(), {"node_id": "synthetic", "step_owners": []}, deadline()
    )
    rows[5][0]["domain"] = [(Q(1), Q(1))]
    result = tool.construct(rows, groups, deadline=deadline())
    assert 5 in result["complete_empty_owners"]
    assert result["point_contradiction_proved"]
    assert result["criterion_met"]
