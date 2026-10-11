"""Synthetic wall-first owned-point witnesses, without scientific inputs."""

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
from test_probe_n17_pooled_relaxation_witness import fixture, selected

from devtools import probe_n17_pooled_feasible_center as tool

Q = tool.Q


def deadline() -> float:
    return time.monotonic() + 30


def synthetic() -> tuple[dict[str, Any], dict[str, Any]]:
    source, certificate = fixture()
    pool = certificate["custody"]["proof_pool"]
    pool["pools"]["0"] = [["3/4", "1"]]
    five = tool.finite.serial([(x - Q(1, 4), y) for x, y in selected()])
    pool["selected_five"] = five
    certificate["custody"]["guard_source"]["point_origins"]["selected"] = five
    lo, hi = tool.cases.INTERVAL
    reach = min(sum(tool.finite.trig(lo)), sum(tool.finite.trig(hi))) / 2
    left = tool.cases.OFFSET + reach
    certificate["rows"][1]["pieces"][0]["domain"] = tool.finite.serial(
        [
            (left, Q(99, 100)),
            (left + Q(1, 100), Q(99, 100)),
            (left + Q(1, 100), Q(101, 100)),
            (left, Q(101, 100)),
        ]
    )
    covered, probe = tool.witness.sweep(
        [(Q(x), Q(y)) for x, y in certificate["rows"][1]["pieces"][0]["domain"]], [], deadline()
    )
    assert covered is False
    certificate["rows"][1]["pieces"][0]["pooled"]["uncovered_probe"] = str(probe)
    return source, certificate


def write_inputs(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> dict[str, Any]:
    source, certificate = synthetic()
    document: dict[str, Any] = {"schema": tool.DESCRIPTOR_SCHEMA}
    previous: dict[str, Any] = {"schema": tool.witness.DESCRIPTOR_SCHEMA}
    for role, value in zip(
        tool.witness.INPUTS,
        (source, certificate, certificate | {"verification_passed": True}),
        strict=True,
    ):
        raw = json.dumps(value).encode()
        path = tmp_path / (role + ".json")
        path.write_bytes(raw)
        for target in (previous, document):
            target[role], target[role + "_sha256"] = path.name, hashlib.sha256(raw).hexdigest()
    monkeypatch.setattr(tool.finite, "REPO", tmp_path)
    old = tool.witness.generate(previous, deadline=deadline())
    assert old["container_passed"] is False
    assert old["all_owner0_strict"] is True
    assert old["all_foreign_open_avoidance"] is True
    for role, value in zip(
        tool.INPUTS[3:], (previous, old, old | {"verification_passed": True}), strict=True
    ):
        raw = json.dumps(value).encode()
        path = tmp_path / (role + ".json")
        path.write_bytes(raw)
        document[role], document[role + "_sha256"] = path.name, hashlib.sha256(raw).hexdigest()
    return document


def test_wall_clip_before_first_gap_creates_valid_candidate() -> None:
    _, certificate = synthetic()
    old = tool.witness.construct(certificate, deadline=deadline())
    assert old["container_passed"] is False
    fresh = tool.construct(certificate, deadline=deadline())
    assert fresh["criterion_met"] is True
    assert fresh["pose"]["container_passed"] is True
    assert fresh["chosen"]["selection"]["center"] != old["selection"]["center"]


def test_both_axis_signs_fixed_owned_margin_and_empty_target() -> None:
    own = [(Q(1), Q(1))]
    domain = [(Q(1, 4), Q(1, 4)), (Q(7, 4), Q(1, 4)), (Q(7, 4), Q(7, 4)), (Q(1, 4), Q(7, 4))]
    clipped = tool.target(domain, own, deadline())
    assert clipped
    for p in clipped:
        x, y = tool.witness.body(own[0], p)
        assert abs(x) <= Q(1, 2) - tool.MARGIN
        assert abs(y) <= Q(1, 2) - tool.MARGIN
    assert tool.target([(Q(0), Q(0))], own, deadline()) == []
    c, s = tool.finite.trig(tool.TAU)
    isolated_own = [(Q(3, 2), Q(3, 2))]
    allowed = (Q(3, 2) - c * (Q(1, 2) - tool.MARGIN), Q(3, 2) - s * (Q(1, 2) - tool.MARGIN))
    assert tool.target([allowed], isolated_own, deadline()) == [allowed]
    boundary = (Q(3, 2) - c / 2, Q(3, 2) - s / 2)
    assert tool.target([boundary], isolated_own, deadline()) == []


@pytest.mark.parametrize("kind", ["point", "segment", "empty"])
def test_degenerate_targets(kind: str) -> None:
    _, certificate = fixture()
    domain = (
        [["1", "1"]]
        if kind == "point"
        else [["1", "1"], ["11/10", "1"]]
        if kind == "segment"
        else [["0", "0"]]
    )
    certificate["rows"][1]["pieces"][0]["domain"] = domain
    result = tool.construct(certificate, deadline=deadline())
    assert result["criterion_met"] is (kind != "empty")
    assert result["status"] == (
        "criterion_missed" if kind == "empty" else "owned_point_relaxation_witness"
    )


def test_full_square_minkowski_sign_and_closed_boundary_blocks_search() -> None:
    pools = {0: [], 1: [(Q(3), Q(3))]}
    regions, count = tool.foreign_regions(pools, deadline())
    shape = tool.witness.square((Q(0), Q(0)), deadline())
    assert count == 4
    assert set(regions[1]) == {(3 - x, 3 - y) for x, y in shape}
    point = min(regions[1])
    assert tool.standing.degenerate_covered([point], list(regions.values())) is True
    assert (
        tool.standing.degenerate_covered(
            [(point[0] - Q(1, 100000), point[1])], list(regions.values())
        )
        is False
    )


def test_covered_early_pieces_then_first_later_candidate() -> None:
    _, certificate = fixture()
    first = copy.deepcopy(certificate["rows"][1]["pieces"][0])
    certificate["custody"]["proof_pool"]["pools"]["1"] = [["3/2", "1"]]
    first["domain"] = [["11/10", "1"]]
    second = copy.deepcopy(first) | {"piece_index": 1, "domain": [["3/4", "1"]]}
    third = copy.deepcopy(second) | {"piece_index": 2}
    certificate["rows"][1]["pieces"] = [first, second, third]
    result = tool.construct(certificate, deadline=deadline())
    assert result["chosen"]["piece_index"] == 1
    assert result["pieces"][0]["covered"] is True
    assert result["unstarted_piece_indices"] == [2]


def test_no_alternate_after_pose_calibration_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    _, certificate = fixture()
    calls = []

    def bad(*args: Any) -> dict[str, Any]:
        calls.append(args)
        return {"criterion_met": False}

    monkeypatch.setattr(tool.witness, "pose", bad)
    with pytest.raises(ValueError, match="calibration"):
        tool.construct(certificate, deadline=deadline())
    assert len(calls) == 1


@pytest.mark.parametrize(
    "field",
    [
        "container_passed",
        "all_owner0_strict",
        "all_foreign_open_avoidance",
        "parent",
        "accepted_union_inputs",
        "verification_passed",
    ],
)
def test_previous_history_custody_tamper(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, field: str
) -> None:
    document = write_inputs(tmp_path, monkeypatch)
    role = "witness_replay" if field == "verification_passed" else "witness_certificate"
    path = tmp_path / document[role]
    value = json.loads(path.read_text())
    value[field] = (
        True
        if field == "container_passed"
        else False
        if field in {"all_owner0_strict", "all_foreign_open_avoidance", "verification_passed"}
        else {}
    )
    raw = json.dumps(value).encode()
    path.write_bytes(raw)
    document[role + "_sha256"] = hashlib.sha256(raw).hexdigest()
    if field != "verification_passed":
        fresh_path = tmp_path / document["witness_replay"]
        fresh_raw = json.dumps(value | {"verification_passed": True}).encode()
        fresh_path.write_bytes(fresh_raw)
        document["witness_replay_sha256"] = hashlib.sha256(fresh_raw).hexdigest()
    with pytest.raises(ValueError, match=r"payload|miss|join"):
        tool.generate(document, deadline=deadline())


def test_own_fresh_replay_and_immutable_input_bytes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    document = write_inputs(tmp_path, monkeypatch)
    generated = tool.generate(document, deadline=deadline())
    assert generated["criterion_met"] is True
    assert tool.check(document, generated, deadline=deadline())["verification_passed"] is True
    assert generated["seventeen_square_packing_proved"] is False
    changed = copy.deepcopy(generated)
    changed["chosen"]["piece_index"] = 9
    with pytest.raises(ValueError, match="reconstruction differs"):
        tool.check(document, changed, deadline=deadline())
    path = tmp_path / document["union_replay"]
    path.write_bytes(path.read_bytes() + b" ")
    with pytest.raises(ValueError, match="identity"):
        tool.generate(document, deadline=deadline())


def test_resource_caps_and_unused_opaque_metadata(monkeypatch: pytest.MonkeyPatch) -> None:
    _, certificate = fixture()
    certificate["opaque"] = "1" + "0" * 5000
    assert tool.construct(certificate, deadline=deadline())["criterion_met"] is True
    certificate["rows"][1]["pieces"][0]["domain"][0][0] = "1" + "0" * 5000
    with pytest.raises(tool.IncompleteError):
        tool.construct(certificate, deadline=deadline())
    monkeypatch.setattr(tool, "PAIR_LIMIT", 3)
    with pytest.raises(tool.IncompleteError, match="pair ceiling"):
        tool.foreign_regions({0: [], 1: [(Q(1), Q(1))]}, deadline())
    with pytest.raises(tool.IncompleteError):
        tool.target([(Q(1), Q(1))], [], time.monotonic() - 1)


def test_two_clean_cli_processes(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    document = write_inputs(tmp_path, monkeypatch)
    descriptor = tmp_path / "descriptor.json"
    descriptor.write_text(json.dumps(document))
    script = (
        "import sys;from pathlib import Path;"
        "from devtools import probe_n17_pooled_feasible_center as t;"
        "t.finite.REPO=Path(sys.argv[1]);raise SystemExit(t.main(sys.argv[2:]))"
    )
    outputs = [tmp_path / "generation.json", tmp_path / "fresh.json"]
    for output in outputs:
        extra = [] if output == outputs[0] else ["--certificate", str(outputs[0])]
        done = subprocess.run(
            [
                sys.executable,
                "-c",
                script,
                str(tmp_path),
                "--descriptor",
                str(descriptor),
                *extra,
                "--output",
                str(output),
            ],
            capture_output=True,
            text=True,
            timeout=20,
            check=False,
        )
        assert done.returncode == 0, done.stderr + (
            output.read_text() if output.exists() else ""
        )
    generated, fresh = (json.loads(p.read_text()) for p in outputs)
    assert tool.witness.payload(generated) == tool.witness.payload(fresh)
    assert fresh["verification_passed"] is True
    assert generated["criterion_met"] is True
    assert generated["parent_geometry_replayed"] is False


def test_output_ceiling_retains_incomplete(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    document = write_inputs(tmp_path, monkeypatch)
    descriptor, output = tmp_path / "descriptor.json", tmp_path / "out.json"
    descriptor.write_text(json.dumps(document))
    monkeypatch.setattr(tool, "OUTPUT_LIMIT", 10)
    assert tool.main(["--descriptor", str(descriptor), "--output", str(output)]) == 1
    result = json.loads(output.read_text())
    assert result["status"] == "incomplete"
    assert result["conditional_I_exclusion_proved"] is False


def test_complete_covered_recipe_miss_is_not_infeasibility() -> None:
    _, certificate = fixture()
    certificate["custody"]["proof_pool"]["pools"]["1"] = [["1", "1"]]
    result = tool.construct(certificate, deadline=deadline())
    assert result["status"] == "criterion_missed"
    assert result["chosen"] is None
    assert result["pieces"][0]["covered"] is True
    assert result["miss_proves_fixed_angle_infeasibility"] is False


def test_six_input_byte_ceiling(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    document = write_inputs(tmp_path, monkeypatch)
    monkeypatch.setattr(tool, "JSON_LIMIT", 10)
    with pytest.raises(tool.IncompleteError, match="byte ceiling"):
        tool.generate(document, deadline=deadline())


def test_piece_cap_and_source_scope_tamper(monkeypatch: pytest.MonkeyPatch) -> None:
    _, certificate = fixture()
    monkeypatch.setattr(tool, "PIECE_LIMIT", 0)
    with pytest.raises(tool.IncompleteError, match="piece ceiling"):
        tool.construct(certificate, deadline=deadline())


def test_input_bytes_rechecked_after_construction(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    document = write_inputs(tmp_path, monkeypatch)
    original = tool.construct
    path = tmp_path / document["witness_replay"]

    def mutate(certificate: dict[str, Any], *, deadline: float) -> dict[str, Any]:
        result = original(certificate, deadline=deadline)
        path.write_bytes(path.read_bytes() + b" ")
        return result

    monkeypatch.setattr(tool, "construct", mutate)
    with pytest.raises(ValueError, match="inputs changed"):
        tool.generate(document, deadline=deadline())
