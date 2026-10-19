"""Target-free uniform-core composition and fresh finite-reconstruction controls."""

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
from test_check_n17_collective_row_coverage import parent_fixture

from devtools import check_n17_strict_core_regional_transfer as tool

Q = tool.Q


def deadline() -> float:
    return time.monotonic() + 30


def rectangle() -> list[tool.Point]:
    x, y, radius = Q(1), Q(1), Q(1, 10)
    return [
        (x - radius, y - radius),
        (x + radius, y - radius),
        (x + radius, y + radius),
        (x - radius, y + radius),
    ]


def fixture(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> dict[str, Any]:
    """Synthetic inherited premise, not a seventeen-square geometric certificate."""
    monkeypatch.setattr(tool.finite, "REPO", tmp_path)
    base = parent_fixture(tmp_path)
    accepted = json.loads((tmp_path / base["guard_certificate"]).read_text())
    context = accepted["contexts"][0]
    context["owner0_owned"] = copy.deepcopy(context["owned_groups"]["0"])
    for index, row in enumerate(context["conditional_rows"]["18"]):
        row["domain"] = [["1", "1"]] if index in tool.TARGET_INDICES else [["3", "3"]]
    endpoint = accepted["original_endpoint_control"]["witnesses"]
    for left, right in ((5, 11), (10, 14)):
        endpoint[left]["owner"], endpoint[right]["owner"] = (
            endpoint[right]["owner"],
            endpoint[left]["owner"],
        )

    def retain(name: str, value: dict[str, Any]) -> tuple[str, str]:
        raw = json.dumps(value, sort_keys=True).encode()
        path = tmp_path / (name + ".json")
        path.write_bytes(raw)
        return path.name, hashlib.sha256(raw).hexdigest()

    for role, value in (
        ("guard_certificate", accepted),
        ("guard_replay", accepted | {"verification_passed": True}),
    ):
        base[role], base[role + "_sha256"] = retain(role, value)
    route = tool.collective.prior.generate(base, deadline=deadline())
    route_replay = tool.collective.prior.check(base, route, deadline=deadline())
    old_doc = {**base, "schema": tool.collective.DESCRIPTOR_SCHEMA}
    for role, value in (("two_child_certificate", route), ("two_child_replay", route_replay)):
        old_doc[role], old_doc[role + "_sha256"] = retain(role, value)
    certificate = tool.collective.generate(old_doc, deadline=deadline())
    replay = tool.collective.check(old_doc, certificate, deadline=deadline())
    assert certificate["changed_owners"] == [18]
    assert certificate["criterion_met"]
    doc = {"schema": tool.DESCRIPTOR_SCHEMA}
    for role, value in zip(tool.ROLES, (old_doc, certificate, replay), strict=True):
        doc[role], doc[role + "_sha256"] = retain(role, value)
    return doc


def test_four_corners_both_signed_axes_and_full_reserve() -> None:
    result = tool.uniform_owned(rectangle(), (Q(1), Q(1)), deadline=deadline())
    assert result["quadratic_checks"] == 64
    assert {row[2] for row in result["quadratic_minima"]} == {"u", "v"}
    assert {row[3] for row in result["quadratic_minima"]} == {-1, 1}
    assert {row[1] for row in result["quadratic_minima"]} == {0, 1, 2, 3}
    assert all(Q(row[4]) >= 0 for row in result["quadratic_minima"])


def test_maximum_32_vertex_core_exactly_512_quadratics() -> None:
    xs = [Q(-1, 20) + Q(i, 150) for i in range(16)]
    core = [(Q(1) + x, Q(1) - Q(1, 10) + x * x) for x in xs]
    core += [(Q(1) + x, Q(1) + Q(1, 10) - x * x) for x in reversed(xs)]
    parsed = tool.parse_core(tool.finite.serial(core), deadline())
    result = tool.uniform_owned(parsed, (Q(1), Q(1)), deadline=deadline())
    assert result["core_vertices"] == 32
    assert result["quadratic_checks"] == 512


def test_exact_interior_stationary_and_endpoint_ties() -> None:
    lo, hi = tool.TAU - tool.HALF_WIDTH, tool.TAU + tool.HALF_WIDTH
    polynomial = (tool.TAU**2, -2 * tool.TAU, Q(1))
    assert tool.sat.minimum(polynomial, lo, hi) == (Q(0), tool.TAU)
    assert tool.sat.minimum((Q(0), Q(0), Q(0)), lo, hi) == (Q(0), lo)


def test_point_boundary_with_zero_reserve_refuses() -> None:
    c, s = tool.finite.trig(tool.TAU)
    point = (Q(1) + c / 2, Q(1) + s / 2)
    core = [
        point,
        (point[0] - Q(1, 100), point[1] + Q(1, 100)),
        (point[0] - Q(1, 100), point[1]),
    ]
    with pytest.raises(ValueError, match="point strict-margin"):
        tool.uniform_owned(core, (Q(1), Q(1)), deadline=deadline())


def test_exact_point_reserve_boundary_remains_uniformly_owned() -> None:
    c, s = tool.finite.trig(tool.TAU)
    a = Q(1, 2) - tool.MARGIN
    body = [(Q(-1, 10), Q(-1, 10)), (a, Q(-1, 10)), (a, Q(1, 10)), (Q(-1, 10), Q(1, 10))]
    core = [(Q(1) + c * x - s * y, Q(1) + s * x + c * y) for x, y in body]
    result = tool.uniform_owned(core, (Q(1), Q(1)), deadline=deadline())
    assert result["point_axis_absolute_maxima"][0] == str(a)
    assert result["uniform_strict_ownership_checked"]


def test_regional_threshold_equality_is_still_strict(monkeypatch: pytest.MonkeyPatch) -> None:
    original = tool.sat.minimum
    monkeypatch.setattr(tool.sat, "minimum", lambda _p, lo, _hi: (Q(0), lo))
    result = tool.uniform_owned(rectangle(), (Q(1), Q(1)), deadline=deadline())
    assert result["equality_at_regional_threshold_allowed"]
    assert Q(result["regional_threshold"]) < Q(1, 2)
    monkeypatch.setattr(tool.sat, "minimum", original)


@pytest.mark.parametrize(
    "kind", ["empty", "segment", "clockwise", "nonconvex", "oversized", "bigscalar"]
)
def test_core_representation_refuses_or_stops(kind: str) -> None:
    raw = tool.finite.serial(rectangle())
    if kind == "empty":
        raw = []
    elif kind == "segment":
        raw = raw[:2]
    elif kind == "clockwise":
        raw.reverse()
    elif kind == "nonconvex":
        raw = [["0", "0"], ["2", "0"], ["1", "1"], ["2", "2"], ["0", "2"]]
    elif kind == "oversized":
        raw *= 9
    else:
        raw[0][0] = str(2**4100)
    error = tool.IncompleteError if kind in ("oversized", "bigscalar") else ValueError
    with pytest.raises(error, match=r"core|convex|rational"):
        tool.parse_core(raw, deadline())


def test_guard_width_and_quadratic_work_are_frozen(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(tool, "HALF_WIDTH", Q(1, 2**22))
    with pytest.raises(ValueError, match="radius differs"):
        tool.uniform_owned(rectangle(), (Q(1), Q(1)), deadline=deadline())
    monkeypatch.setattr(tool, "HALF_WIDTH", Q(1, 2**23))
    monkeypatch.setattr(tool, "QUADRATIC_LIMIT", 1)
    with pytest.raises(tool.IncompleteError, match="quadratic ceiling"):
        tool.uniform_owned(rectangle(), (Q(1), Q(1)), deadline=deadline())


def test_full_transfer_rechecks_collective_once_and_does_not_transport_point_footprint(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    doc = fixture(tmp_path, monkeypatch)
    calls = []
    original = tool.collective.check

    def counted(*args: Any, **kwargs: Any) -> dict[str, Any]:
        calls.append(True)
        return original(*args, **kwargs)

    monkeypatch.setattr(tool.collective, "check", counted)
    result = tool.generate(doc, deadline=deadline())
    assert calls == [True]
    assert result["collective_rows_rechecked"] == 992
    assert result["regional_necessary_domain_restriction_proved"]
    assert not result["foreign_regional_domains_reconstructed"]
    assert not result["old_owner0_target_rows_transferred"]
    assert not result["declared_guard_exclusion_proved"]
    assert result["endpoint_family_disjoint_checked_now"]
    assert len(result["requested_rows"]) == 25
    # A nearby centre is outside an old zero-width owner0 diagnostic footprint,
    # while every retained core vertex is uniformly owned at that centre.
    assert result["guard"]["centre_box"][0][0] != "1"
    assert result["new_uniform_ownership"]["uniform_strict_ownership_checked"]
    assert tool.check(doc, result, deadline=deadline())["verification_passed"]


@pytest.mark.parametrize(
    "mutation", ["payload", "missing_row", "core_equality", "frame", "endpoint"]
)
def test_changed_premise_refuses(
    mutation: str, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    doc = fixture(tmp_path, monkeypatch)
    old_doc = json.loads((tmp_path / doc["collective_descriptor"]).read_text())
    if mutation in ("payload", "missing_row"):
        path = tmp_path / doc["collective_certificate"]
        value = json.loads(path.read_text())
        if mutation == "payload":
            value["owners"][0]["lost_length"] = "1"
        else:
            value["owners"][0]["rows"].pop()
        raw = json.dumps(value).encode()
        path.write_bytes(raw)
        doc["collective_certificate_sha256"] = hashlib.sha256(raw).hexdigest()
    else:
        path = tmp_path / old_doc["guard_certificate"]
        value = json.loads(path.read_text())
        if mutation == "core_equality":
            value["contexts"][0]["owner0_owned"][0][0] = "0"
        elif mutation == "frame":
            value["container"]["outer_U"] = "5"
        else:
            value["original_endpoint_control"]["all17_retained"] = False
        path.write_text(json.dumps(value))
    with pytest.raises(ValueError, match=r"differs|required|custody"):
        tool.generate(doc, deadline=deadline())


def test_serialized_candidate_tamper_refuses(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    doc = fixture(tmp_path, monkeypatch)
    result = tool.generate(doc, deadline=deadline())
    result["new_uniform_ownership"]["quadratic_minima"][0][4] = "100"
    with pytest.raises(ValueError, match="reconstruction differs"):
        tool.check(doc, result, deadline=deadline())


def test_expired_clock_and_failures_clear_flags() -> None:
    with pytest.raises(tool.IncompleteError):
        tool.uniform_owned(rectangle(), (Q(1), Q(1)), deadline=time.monotonic() - 1)
    for exc in (tool.IncompleteError("wall"), ValueError("custody")):
        result = tool.failure(exc)
        assert not result["criterion_met"]
        assert not any(v for k, v in result.items() if k.endswith("_proved"))


def test_two_clean_processes_match_compact_payload(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    doc = fixture(tmp_path, monkeypatch)
    descriptor = tmp_path / "descriptor.json"
    descriptor.write_text(json.dumps(doc))
    outputs = [tmp_path / "candidate.json", tmp_path / "fresh.json"]
    bootstrap = (
        "import sys; from pathlib import Path; "
        "from devtools import check_n17_strict_core_regional_transfer as m; "
        "m.finite.REPO=Path(sys.argv.pop(1)); raise SystemExit(m.main(sys.argv[1:]))"
    )
    for index, output in enumerate(outputs):
        argv = [
            sys.executable,
            "-c",
            bootstrap,
            str(tmp_path),
            "--descriptor",
            str(descriptor),
            "--max-seconds",
            "30",
            "--output",
            str(output),
        ]
        if index:
            argv += ["--certificate", str(outputs[0])]
        run = subprocess.run(argv, capture_output=True, text=True, timeout=35, check=False)
        assert run.returncode == 0, run.stderr + output.read_text()
        assert output.stat().st_size <= tool.OUTPUT_LIMIT
    first, fresh = [json.loads(p.read_text()) for p in outputs]
    assert tool.payload(first) == tool.payload(fresh)
    assert fresh["verification_passed"]
