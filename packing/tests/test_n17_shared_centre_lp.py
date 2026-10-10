"""Synthetic readiness controls; no real endpoint or first-eight target is evaluated."""

from __future__ import annotations

import copy
import hashlib
import json
import os
import subprocess
import sys
import time
from dataclasses import replace
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Self, cast

import pytest

from devtools import n17_shared_centre_lp as tool


def budget(operations: int = 2_000_000) -> tool.Budget:
    return tool.Budget(time.monotonic() + 30, operations)


def synthetic_descriptor() -> dict[str, Any]:
    return {
        "schema": tool.CONTEXT_SCHEMA,
        **{
            key: "unused"
            for role in tool.projection.prior.ROLES
            for key in (role, role + "_sha256")
        },
    }


def synthetic_polygons() -> list[list[tool.Point]]:
    polygon = [(Q(1, 2), Q(1, 2)), (Q(4), Q(1, 2)), (Q(4), Q(4)), (Q(1, 2), Q(4))]
    return [polygon[:] for _ in range(24)]


@pytest.fixture(scope="module")
def model() -> tool.Model:
    # Coincident synthetic cells deliberately lack the physical capacity-one premise.
    return tool.build_model(synthetic_polygons(), tuple(range(17)), budget())


def packet(model: tool.Model) -> dict[str, Any]:
    return {"model": tool.model_payload(model, budget()), "point": ["2"] * 34}


def test_all_pair_rows_and_shared_primal_are_checked(model: tool.Model) -> None:
    assert len(model.pairs) == 136
    assert len(model.rows) == 17 * 4 + 136 * 4
    assert tool.check_packet(model, packet(model), budget()) == (Q(2),) * 34
    violated = packet(model)
    violated["point"][0] = "0"
    with pytest.raises(ValueError, match="exact primal violates cell:0"):
        tool.check_packet(model, violated, budget())


def test_closed_touching_and_tiny_exact_violation(model: tool.Model) -> None:
    touching = packet(model)
    touching["point"] = ["1/2"] * 34
    assert tool.check_packet(model, touching, budget()) == (Q(1, 2),) * 34
    touching["point"][0] = str(Q(1, 2) - Q(1, 2**100))
    with pytest.raises(ValueError, match="exact primal violates"):
        tool.check_packet(model, touching, budget())


@pytest.mark.parametrize(
    "alteration",
    ["missing-pair", "duplicate-pair", "missing-row", "duplicate-row", "row-sign", "row-order"],
)
def test_payload_inventory_cannot_omit_or_change_constraints(
    model: tool.Model, alteration: str
) -> None:
    changed = packet(model)
    payload = changed["model"]
    if alteration == "missing-pair":
        payload["pairs"].pop()
    elif alteration == "duplicate-pair":
        payload["pairs"][-1] = payload["pairs"][0]
    elif alteration == "missing-row":
        payload["rows"].pop()
    elif alteration == "duplicate-row":
        payload["rows"][-1] = payload["rows"][0]
    elif alteration == "row-sign":
        payload["rows"][0]["rhs"] = "-99"
    else:
        payload["rows"].reverse()
    with pytest.raises(ValueError, match="original row/pair payload differs"):
        tool.check_packet(model, changed, budget())


def test_reader_refuses_broken_model_inventory(model: tool.Model) -> None:
    with pytest.raises(ValueError, match="missing/reordered"):
        tool.check_primal(replace(model, rows=model.rows[:-1]), ["2"] * 34, budget())
    with pytest.raises(ValueError, match="duplicate row"):
        tool.check_primal(
            replace(model, rows=(*model.rows[:-1], model.rows[0])), ["2"] * 34, budget()
        )
    with pytest.raises(ValueError, match="pair roster"):
        tool.check_primal(replace(model, pairs=model.pairs[:-1]), ["2"] * 34, budget())


def test_degenerate_planes_retain_closed_equalities() -> None:
    point = [(Q(1), Q(2))]
    segment = [(Q(1), Q(2)), (Q(3), Q(4))]
    assert tool.planes(point, budget()) == (
        (Q(1), Q(0), Q(1)),
        (Q(-1), Q(0), Q(-1)),
        (Q(0), Q(1), Q(2)),
        (Q(0), Q(-1), Q(-2)),
    )
    assert len(tool.planes(segment, budget())) == 4
    # A point on the segment, including its closed endpoint, survives the complete rows.
    for p in [*segment, (Q(2), Q(3))]:
        assert all(a * p[0] + b * p[1] <= c for a, b, c in tool.planes(segment, budget()))
    assert any(a * Q(2) + b * Q(4) > c for a, b, c in tool.planes(segment, budget()))
    assert tool.clip(segment, (Q(1), Q(0), Q(1)), 73, budget()) == [segment[0]]
    assert tool.centre_domain([(Q(1, 2), Q(1, 2))], budget()) == [(Q(1, 2), Q(1, 2))]


def test_pair_domain_difference_sign_and_touching() -> None:
    assert tool.pair_domain([(Q(1), Q(1))], [(Q(2), Q(1))], budget()) == [(Q(1), Q(0))]
    assert tool.pair_domain([(Q(2), Q(1))], [(Q(1), Q(1))], budget()) == [(Q(-1), Q(0))]
    with pytest.raises(ValueError, match="empty pair domain"):
        tool.pair_domain([(Q(1), Q(1))], [(Q(1), Q(1))], budget())
    with pytest.raises(ValueError, match="empty centre domain"):
        tool.centre_domain([(Q(0), Q(0))], budget())


def test_guards_reject_intermediate_growth_even_when_final_answer_cancels() -> None:
    active = budget()
    large = tool.Guarded(Q(2**3000), active)
    with pytest.raises(tool.IncompleteError, match="bit ceiling"):
        _ = large * large - large * large
    with pytest.raises(tool.IncompleteError, match="bit ceiling"):
        _ = tool.Guarded(Q(1, 2**3000), budget()) * Q(1, 2**3000)
    assert (tool.Guarded(Q(7), active) / Q(7)).value == 1
    with pytest.raises(ValueError, match="mixed arithmetic budgets"):
        _ = large + tool.Guarded(Q(0), budget())


def test_reflected_unary_and_comparison_operations_keep_the_guard() -> None:
    active = budget()
    value = tool.Guarded(Q(2, 3), active)
    assert (Q(3) - value).value == Q(7, 3)
    assert (Q(3) / value).value == Q(9, 2)
    assert (Q(3) * value).value == 2
    assert (Q(3) + value).value == Q(11, 3)
    assert (-value).value == Q(-2, 3)
    assert Q(1) > value
    assert Q(1) >= value
    assert Q(0) < value
    assert Q(0) <= value
    assert value == Q(2, 3)
    assert value != Q(1)
    assert bool(value)
    assert not tool.Guarded(Q(0), active)
    assert active.operations > 0
    # A foreign constructor must refuse rather than silently strip this guard.
    with pytest.raises(TypeError, match=r"argument|Rational|Fraction"):
        _ = Q(cast(Any, value))


def test_deadline_crossing_during_final_comparison_is_incomplete(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    active = budget()
    value = tool.Guarded(Q(1), active)
    clock = [0.0]
    monkeypatch.setattr(tool.time, "monotonic", lambda: clock[0])
    active.deadline = 1.0

    def slow_comparison(left: Q, right: Q) -> bool:
        clock[0] = 2.0
        return left <= right

    with pytest.raises(tool.IncompleteError, match="wall ceiling"):
        value.comparison(Q(1), slow_comparison)


def test_tiny_operation_and_expired_deadline_stop_inside_geometry(model: tool.Model) -> None:
    with pytest.raises(tool.IncompleteError, match="operation ceiling"):
        tool.hull(synthetic_polygons()[0], 32, budget(2))
    with pytest.raises(tool.IncompleteError, match="wall ceiling"):
        tool.check_packet(model, packet(model), tool.Budget(time.monotonic() - 1, 100))
    with pytest.raises(ValueError, match="finite deadline"):
        tool.Budget(float("inf"), 100)


@pytest.mark.parametrize("coordinate", ["nan", "1.0", "01", "1/2/3", "-0"])
def test_noncanonical_primal_is_refused(model: tool.Model, coordinate: str) -> None:
    changed = packet(model)
    changed["point"][0] = coordinate
    with pytest.raises(ValueError, match="canonical"):
        tool.check_packet(model, changed, budget())


def test_output_and_held_input_limits(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    held = tmp_path / "generated.json"
    held.write_bytes(b"accepted")
    tool.check_held({held: b"accepted"}, budget())
    held.write_bytes(b"changed")
    with pytest.raises(ValueError, match="held input bytes changed"):
        tool.check_held({held: b"accepted"}, budget())
    monkeypatch.setattr(tool, "PACKET_LIMIT", 16)
    with pytest.raises(tool.IncompleteError, match="packet byte ceiling"):
        tool.packet_bytes({"payload": "x" * 30}, budget())


def synthetic_endpoint() -> tuple[
    dict[str, Any],
    list[str],
    list[dict[str, Any]],
    dict[str, list[int]],
    list[list[tool.Point]],
]:
    cells = [i for i in range(24) if tool.ENDPOINT_MASK & (1 << i)]
    names = [f"synthetic-{i}" for i in range(24)]
    assignment = [
        {"label": label, "cell": names[cell]}
        for label, cell in zip(range(1, 18), cells, strict=True)
    ]
    witness = {
        "n": 17,
        "side": str(tool.SIDE),
        "representation": "corners",
        "coordinates": {
            "origin": "lower-left",
            "axes": "x-right-y-up",
            "angle_unit": "not-applicable",
        },
        "scalar": {"kind": "rational"},
        "squares": [
            {"id": i + 1, "corners": [[str(Q(2) + Q(i, 100)), str(Q(2) + Q(i, 200))]] * 4}
            for i in range(17)
        ],
    }
    return witness, names, assignment, {"r3": list(range(24))}, synthetic_polygons()


def retained_assignment_metadata() -> tuple[
    list[str], list[dict[str, Any]], dict[str, list[int]]
]:
    # Integer-only exp247 catalogue metadata, accepted through exp308. No witness
    # or physical cell geometry is used by this fixture.
    cells = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 18, 20, 21]
    names = [f"catalogue-{i}" for i in range(24)]
    assignment = [
        {"label": label, "cell": names[cell]}
        for label, cell in zip(range(1, 18), cells, strict=True)
    ]
    d4 = {
        "r3": [
            2,
            0,
            3,
            1,
            14,
            15,
            5,
            4,
            10,
            11,
            9,
            8,
            6,
            7,
            13,
            12,
            17,
            23,
            20,
            18,
            21,
            19,
            16,
            22,
        ],
        "f1": [
            3,
            1,
            2,
            0,
            15,
            14,
            13,
            12,
            11,
            10,
            9,
            8,
            7,
            6,
            5,
            4,
            23,
            17,
            20,
            21,
            18,
            19,
            22,
            16,
        ],
    }
    return names, assignment, d4


def test_selected_nonidentity_catalogue_action_keeps_legacy_r3_refusal() -> None:
    names, assignment, d4 = retained_assignment_metadata()
    cells = [names.index(row["cell"]) for row in assignment]
    assert sum(1 << cell for cell in cells) == 3439615
    assert sum(1 << d4["r3"][cell] for cell in cells) == 3730943
    assert sum(1 << d4["f1"][cell] for cell in cells) == 1900015
    with pytest.raises(ValueError, match="wrong canonical endpoint orbit"):
        tool.frame_assignment(names, assignment, d4, budget())
    assigned, permutation = tool.frame_assignment(names, assignment, d4, budget(), "f1")
    assert [assigned[label] for label in range(1, 18)] == cells
    assert permutation == tuple(d4["f1"])


@pytest.mark.parametrize("damage", ["missing", "duplicate", "boolean"])
def test_selected_catalogue_permutation_must_be_complete(damage: str) -> None:
    names, assignment, d4 = retained_assignment_metadata()
    if damage == "missing":
        del d4["f1"]
    elif damage == "duplicate":
        d4["f1"][0] = d4["f1"][1]
    else:
        d4["f1"][0] = True
    with pytest.raises(ValueError, match="complete f1 cell permutation"):
        tool.frame_assignment(names, assignment, d4, budget(), "f1")


def test_selected_point_action_distinguishes_asymmetric_r3_and_f1() -> None:
    point = (Q(3, 4), Q(9, 8))
    assert tool.frame_point(point, budget()) == (Q(9, 8), tool.U - Q(3, 4))
    assert tool.frame_point(point, budget(), "f1") == (tool.U - Q(9, 8), tool.U - Q(3, 4))
    with pytest.raises(ValueError, match="unsupported endpoint frame action"):
        tool.frame_point(point, budget(), cast(Any, "r0"))


def test_selected_f1_uses_same_nonidentity_action_for_cells_and_synthetic_centres() -> None:
    witness = synthetic_endpoint()[0]
    names, assignment, d4 = retained_assignment_metadata()
    cells, point = tool.endpoint_coordinates(
        witness, names, assignment, d4, synthetic_polygons(), budget=budget(), frame_action="f1"
    )
    labels = (1, 5, 2, 6, 3, 7, 4, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17)
    delta = (tool.U - tool.SIDE) / 2
    expected = {}
    for row, label in enumerate(labels):
        original = names.index(assignment[label - 1]["cell"])
        expected[d4["f1"][original]] = (
            tool.U - Q(2) - Q(row, 200) - delta,
            tool.U - Q(2) - Q(row, 100) - delta,
        )
    assert cells == tuple(sorted(expected))
    assert point == tuple(q for cell in sorted(expected) for q in expected[cell])


def test_wrong_catalogue_action_is_refused_before_witness_io(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    names, assignment, d4 = retained_assignment_metadata()
    partition, cover = tmp_path / "partition.json", tmp_path / "cover.json"
    held = {
        partition: json.dumps({"orbits": [{"distance": 0, "mask": 1900015}]}).encode(),
        cover: json.dumps(
            {
                "endpoint": {
                    "family": {
                        "h256-centroid": {
                            "one_state": True,
                            "squares": assignment,
                        }
                    }
                }
            }
        ).encode(),
    }
    accepted = {"accepted_inputs": {"partition": str(partition), "cover": str(cover), "d4": d4}}
    monkeypatch.setattr(
        tool.projection.prior, "intake", lambda *_args: ([], names, [], accepted, held)
    )
    with pytest.raises(ValueError, match="wrong canonical endpoint orbit"):
        tool.endpoint_packet(
            synthetic_descriptor(),
            tmp_path / "absent-witness.yaml",
            "unused",
            budget(),
        )


def test_cli_frozen_frame_choice_is_retained_and_checked_independently(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    descriptor = tmp_path / "descriptor.json"
    descriptor.write_text("{}", encoding="utf-8")
    actions: list[str] = []

    def synthetic_construction(*_args: Any, frame_action: tool.FrameAction) -> dict[str, Any]:
        actions.append(frame_action)
        return {"model": {}, "point": []}

    monkeypatch.setattr(tool, "endpoint_packet", synthetic_construction)
    monkeypatch.setattr(tool, "provenance", lambda *_args: {})
    common = [
        "--descriptor",
        str(descriptor),
        "--witness",
        "unused",
        "--witness-sha256",
        "unused",
    ]
    constructed = tmp_path / "constructed.json"
    assert tool.main([*common, "--frame-action", "f1", "--output", str(constructed)]) == 0
    envelope = json.loads(constructed.read_text())
    assert envelope["frame_action"] == "f1"
    verified = tmp_path / "verified.json"
    assert (
        tool.main(
            [
                *common,
                "--frame-action",
                "f1",
                "--check",
                str(constructed),
                "--output",
                str(verified),
            ]
        )
        == 0
    )
    assert json.loads(verified.read_text())["frame_action"] == "f1"
    assert actions == ["f1", "f1"]
    mismatch = tmp_path / "mismatch.json"
    assert tool.main([*common, "--check", str(constructed), "--output", str(mismatch)]) == 1
    refused = json.loads(mismatch.read_text())
    assert refused["frame_action"] == "r3"
    assert "differs from frozen checker choice" in refused["reason"]
    assert actions == ["f1", "f1"]  # Refusal precedes reconstruction; no packet adoption.
    del envelope["frame_action"]
    missing = tmp_path / "missing-action.json"
    missing.write_text(json.dumps(envelope))
    output = tmp_path / "missing-refused.json"
    assert (
        tool.main(
            [*common, "--frame-action", "f1", "--check", str(missing), "--output", str(output)]
        )
        == 1
    )
    assert "differs from frozen checker choice" in json.loads(output.read_text())["reason"]
    assert actions == ["f1", "f1"]
    legacy = tmp_path / "legacy.json"
    assert tool.main([*common, "--output", str(legacy)]) == 0
    assert json.loads(legacy.read_text())["frame_action"] == "r3"
    assert actions == ["f1", "f1", "r3"]


def test_synthetic_endpoint_mapping_uses_exact_mean_shift_and_rotation() -> None:
    arguments = synthetic_endpoint()
    cells, point = tool.endpoint_coordinates(*arguments, budget=budget())
    delta = (tool.U - tool.SIDE) / 2
    assert sum(1 << i for i in cells) == tool.ENDPOINT_MASK
    labels = (1, 5, 2, 6, 3, 7, 4, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17)
    expected = []
    for label in range(1, 18):
        row = labels.index(label)
        expected.extend((Q(2) + Q(row, 200) + delta, tool.U - Q(2) - Q(row, 100) - delta))
    assert point == tuple(expected)
    changed = copy.deepcopy(arguments)
    changed[0]["squares"][0]["corners"] = [["0", "0"]] * 4
    with pytest.raises(ValueError, match="outside candidate"):
        tool.endpoint_coordinates(*changed, budget=budget())
    changed = copy.deepcopy(arguments)
    changed[2][0]["cell"] = changed[1][next(i for i in range(24) if i not in cells)]
    with pytest.raises(ValueError, match="wrong canonical endpoint"):
        tool.endpoint_coordinates(*changed, budget=budget())


def test_source_row_ids_and_duplicate_assignment_are_refused() -> None:
    arguments = synthetic_endpoint()
    arguments[0]["squares"][0]["id"] = 17
    with pytest.raises(ValueError, match="source row IDs"):
        tool.endpoint_coordinates(*arguments, budget=budget())
    arguments = synthetic_endpoint()
    arguments[2][0]["cell"] = arguments[2][1]["cell"]
    with pytest.raises(ValueError, match="duplicate transformed"):
        tool.endpoint_coordinates(*arguments, budget=budget())


def synthetic_intake(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> tuple[Path, str]:
    witness, names, assignment, d4, polygons = synthetic_endpoint()
    alias = tmp_path / "alias"
    alias.mkdir()
    partition, cover = tmp_path / "partition.json", tmp_path / "cover.json"
    partition.write_text(
        json.dumps({"orbits": [{"distance": 0, "mask": tool.ENDPOINT_MASK}]}),
        encoding="utf-8",
    )
    cover.write_text(
        json.dumps(
            {
                "endpoint": {
                    "family": {"h256-centroid": {"one_state": True, "squares": assignment}}
                }
            }
        ),
        encoding="utf-8",
    )
    accepted = {
        "accepted_inputs": {
            "partition": str(alias / ".." / partition.name),
            "cover": str(alias / ".." / cover.name),
            "d4": d4,
        }
    }
    held = {path.resolve(): path.read_bytes() for path in (partition, cover)}
    monkeypatch.setattr(
        tool.projection.prior,
        "intake",
        lambda *_args: (polygons, names, [], accepted, held),
    )
    witness_path = tmp_path / "witness.yaml"
    raw = json.dumps({"witness": witness}).encode("utf-8")
    witness_path.write_bytes(raw)
    return witness_path, hashlib.sha256(raw).hexdigest()


def test_witness_byte_ceiling_is_incomplete_before_digest_check(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    witness_path, _digest = synthetic_intake(tmp_path, monkeypatch)
    monkeypatch.setattr(tool, "WITNESS_LIMIT", 8)
    with pytest.raises(tool.IncompleteError, match="witness byte ceiling"):
        tool.endpoint_packet(synthetic_descriptor(), witness_path, "wrong", budget())


def test_held_lookup_aliases_match_resolved_intake_keys(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    witness_path, digest = synthetic_intake(tmp_path, monkeypatch)
    result = tool.endpoint_packet(synthetic_descriptor(), witness_path, digest, budget())
    assert len(result["model"]["pairs"]) == 136
    assert len(result["point"]) == 34


def test_clean_process_reconstructs_every_synthetic_pair() -> None:
    script = """
from fractions import Fraction as Q
import time
from devtools import n17_shared_centre_lp as t
p=[(Q(1,2),Q(1,2)),(Q(4),Q(1,2)),(Q(4),Q(4)),(Q(1,2),Q(4))]
b=t.Budget(time.monotonic()+20,2000000)
m=t.build_model([p[:] for _ in range(24)],tuple(range(17)),b)
assert len(m.pairs)==136
assert t.check_packet(m,{'model':t.model_payload(m,b),'point':['2']*34},b)==(Q(2),)*34
"""
    result = subprocess.run(
        [sys.executable, "-B", "-c", script],
        check=False,
        capture_output=True,
        text=True,
        timeout=25,
        env=os.environ.copy(),
    )
    assert result.returncode == 0, result.stderr


def test_cli_refuses_changed_descriptor_after_proof_work(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, model: tool.Model
) -> None:
    descriptor, output = tmp_path / "descriptor.json", tmp_path / "output.json"
    descriptor.write_text("{}", encoding="utf-8")

    def synthetic_construction(*_args: Any, **_kwargs: Any) -> dict[str, Any]:
        descriptor.write_text('{"changed":true}', encoding="utf-8")
        return packet(model)

    monkeypatch.setattr(tool, "endpoint_packet", synthetic_construction)
    assert (
        tool.main(
            [
                "--descriptor",
                str(descriptor),
                "--witness",
                "unused",
                "--witness-sha256",
                "unused",
                "--output",
                str(output),
            ]
        )
        == 1
    )
    result = json.loads(output.read_text(encoding="utf-8"))
    assert result["status"] == "refused"
    assert result["verification_passed"] is False
    assert "held input bytes changed" in result["reason"]


def test_fresh_checker_refuses_changed_synthetic_coordinates(
    monkeypatch: pytest.MonkeyPatch, model: tool.Model
) -> None:
    original = packet(model)
    monkeypatch.setattr(tool, "endpoint_packet", lambda *_args, **_kwargs: original)
    result = tool.check_endpoint_packet({}, Path("unused"), "unused", original, budget())
    assert result["verification_passed"] is True
    assert result["census_admission_proved"] is False
    changed = copy.deepcopy(original)
    changed["point"][0] = "1"
    with pytest.raises(ValueError, match="fresh endpoint mathematical payload differs"):
        tool.check_endpoint_packet({}, Path("unused"), "unused", changed, budget())


def test_publish_new_exposes_only_complete_bytes_and_refuses_collision(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    output = tmp_path / "receipt.json"
    contents = b'{"status":"verified"}'
    link = tool.os.link

    def inspect_commit(source: Path, destination: Path) -> None:
        assert not destination.exists()
        assert source.parent == destination.parent
        assert source.read_bytes() == contents
        link(source, destination)

    monkeypatch.setattr(tool.os, "link", inspect_commit)
    tool.publish_new(output, contents, budget())
    assert output.read_bytes() == contents
    assert list(tmp_path.iterdir()) == [output]
    monkeypatch.setattr(tool.os, "link", link)
    with pytest.raises(FileExistsError):
        tool.publish_new(output, b"replacement", budget())
    assert output.read_bytes() == contents
    assert list(tmp_path.iterdir()) == [output]


def test_publish_new_cleans_private_partial_write_without_publishing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    output = tmp_path / "receipt.json"
    fdopen = tool.os.fdopen

    class FailingWriter:
        def __init__(self, descriptor: int, mode: str):
            self.stream = fdopen(descriptor, mode)

        def __enter__(self) -> Self:
            return self

        def write(self, contents: bytes) -> int:
            self.stream.write(contents[:5])
            raise OSError("injected private write failure")

        def __exit__(self, *_args: object) -> None:
            self.stream.close()

    monkeypatch.setattr(tool.os, "fdopen", FailingWriter)
    with pytest.raises(OSError, match="injected private write failure"):
        tool.publish_new(output, b'{"status":"verified"}', budget())
    assert not output.exists()
    assert list(tmp_path.iterdir()) == []


@pytest.mark.parametrize("arguments", [["--max-seconds", "nan"], ["--max-operations", "0"]])
def test_cli_invalid_resource_arguments_publish_refusal(
    tmp_path: Path, arguments: list[str]
) -> None:
    output = tmp_path / "refused.json"
    assert (
        tool.main(
            [
                "--descriptor",
                "unused",
                "--witness",
                "unused",
                "--witness-sha256",
                "unused",
                "--output",
                str(output),
                *arguments,
            ]
        )
        == 1
    )
    result = json.loads(output.read_bytes())
    assert result["status"] == "refused"
    assert result["verification_passed"] is False
    assert result["reason"] in ("frozen phase wall ceiling", "operation cap")


def test_cli_malformed_synthetic_yaml_publishes_refusal(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    witness, _digest = synthetic_intake(tmp_path, monkeypatch)
    raw = b"["
    witness.write_bytes(raw)
    descriptor = tmp_path / "descriptor.json"
    descriptor.write_text(json.dumps(synthetic_descriptor()), encoding="utf-8")
    output = tmp_path / "refused.json"
    assert (
        tool.main(
            [
                "--descriptor",
                str(descriptor),
                "--witness",
                str(witness),
                "--witness-sha256",
                hashlib.sha256(raw).hexdigest(),
                "--output",
                str(output),
            ]
        )
        == 1
    )
    result = json.loads(output.read_bytes())
    assert result["status"] == "refused"
    assert result["verification_passed"] is False
    assert "while parsing" in result["reason"]


def test_model_conversion_stops_before_complete_oversized_payload(
    monkeypatch: pytest.MonkeyPatch, model: tool.Model
) -> None:
    visited = []
    checked = tool.Budget.checked

    def count_conversion(self: tool.Budget, value: Q) -> Q:
        visited.append(value)
        return checked(self, value)

    base = {"cells": list(model.cells), "pairs": [list(p) for p in model.pairs], "rows": []}
    allowance = len(tool.packet_bytes(base, budget())) + 64 + 6 * len(model.rows[0].label) + 22
    monkeypatch.setattr(tool, "PACKET_LIMIT", allowance)
    monkeypatch.setattr(tool.Budget, "checked", count_conversion)
    with pytest.raises(tool.IncompleteError, match="model payload byte ceiling"):
        tool.model_payload(model, budget())
    assert 0 < len(visited) < 34
    with pytest.raises(tool.IncompleteError, match="wall ceiling"):
        tool.model_payload(model, tool.Budget(time.monotonic() - 1, 100))


def test_cli_publication_collision_reports_failure_without_overwrite(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    output = tmp_path / "existing.json"
    original = b"existing evidence"
    output.write_bytes(original)
    assert (
        tool.main(
            [
                "--descriptor",
                "unused",
                "--witness",
                "unused",
                "--witness-sha256",
                "unused",
                "--output",
                str(output),
                "--max-operations",
                "0",
            ]
        )
        == 1
    )
    assert output.read_bytes() == original
    assert list(tmp_path.iterdir()) == [output]
    assert "endpoint receipt publication failed" in capsys.readouterr().err


@pytest.mark.parametrize("key", ["unexpected", "corner_descriptor"])
def test_cli_nested_descriptor_publishes_refusal_before_intake(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, key: str
) -> None:
    descriptor, output = tmp_path / "descriptor.json", tmp_path / "refused.json"
    document = synthetic_descriptor()
    document.pop(key, None)
    flat = json.dumps(document)[:-1]
    descriptor.write_text(
        flat + ', "' + key + '":' + "[" * 1200 + "0" + "]" * 1200 + "}",
        encoding="utf-8",
    )

    def no_intake(*_args: Any) -> None:
        pytest.fail("malformed descriptor reached accepted-input intake")

    monkeypatch.setattr(tool.projection.prior, "intake", no_intake)
    assert (
        tool.main(
            [
                "--descriptor",
                str(descriptor),
                "--witness",
                "unused",
                "--witness-sha256",
                "unused",
                "--output",
                str(output),
            ]
        )
        == 1
    )
    result = json.loads(output.read_bytes())
    assert result["status"] == "refused"
    assert result["verification_passed"] is False
    assert "endpoint descriptor" in result["reason"]


def test_cli_nested_submitted_payload_publishes_refusal(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    descriptor, submitted = tmp_path / "descriptor.json", tmp_path / "constructed.json"
    descriptor.write_text("{}", encoding="utf-8")
    # In-process search tools can raise the worker's encoder recursion ceiling.
    depth = sys.getrecursionlimit() + 1
    submitted.write_text(
        '{"schema":"n17-shared-centre-endpoint/v1","status":"constructed",'
        '"frame_action":"r3","mathematical":{"point":' + "[" * depth + "0" + "]" * depth + "}}",
        encoding="utf-8",
    )
    monkeypatch.setattr(tool, "endpoint_packet", lambda *_args, **_kwargs: {"point": []})
    output = tmp_path / "refused.json"
    assert (
        tool.main(
            [
                "--descriptor",
                str(descriptor),
                "--witness",
                "unused",
                "--witness-sha256",
                "unused",
                "--check",
                str(submitted),
                "--output",
                str(output),
            ]
        )
        == 1
    )
    result = json.loads(output.read_bytes())
    assert result["status"] == "refused"
    assert result["verification_passed"] is False
    assert "packet nesting exceeds encoder depth" in result["reason"]


@pytest.mark.parametrize("boundary", ["descriptor", "construction"])
def test_cli_json_decoder_depth_failure_publishes_refusal(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, boundary: str
) -> None:
    descriptor, submitted = tmp_path / "descriptor.json", tmp_path / "constructed.json"
    descriptor.write_text("{}", encoding="utf-8")
    output = tmp_path / "refused.json"
    read_json = tool.projection.finite.read_json

    def excessive_depth(path: Path, ceiling: int) -> tuple[bytes, dict[str, Any]]:
        if path == (descriptor if boundary == "descriptor" else submitted):
            raise RecursionError("injected decoder depth failure")
        return read_json(path, ceiling)

    monkeypatch.setattr(tool.projection.finite, "read_json", excessive_depth)
    arguments = ["--check", str(submitted)] if boundary == "construction" else []
    assert (
        tool.main(
            [
                "--descriptor",
                str(descriptor),
                "--witness",
                "unused",
                "--witness-sha256",
                "unused",
                "--output",
                str(output),
                *arguments,
            ]
        )
        == 1
    )
    result = json.loads(output.read_bytes())
    assert result["status"] == "refused"
    assert result["verification_passed"] is False
    assert boundary + " JSON nesting exceeds decoder depth" in result["reason"]


def test_cli_unrelated_recursion_error_remains_a_programming_failure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    descriptor, output = tmp_path / "descriptor.json", tmp_path / "receipt.json"
    descriptor.write_text("{}", encoding="utf-8")

    def broken_construction(*_args: Any, **_kwargs: Any) -> dict[str, Any]:
        raise RecursionError("synthetic programming error")

    monkeypatch.setattr(tool, "endpoint_packet", broken_construction)
    with pytest.raises(RecursionError, match="synthetic programming error"):
        tool.main(
            [
                "--descriptor",
                str(descriptor),
                "--witness",
                "unused",
                "--witness-sha256",
                "unused",
                "--output",
                str(output),
            ]
        )
    assert not output.exists()
