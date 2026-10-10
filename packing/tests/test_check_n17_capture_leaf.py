"""Target-free closed-domain, frame and terminal-predicate controls."""

from __future__ import annotations

import copy
import gzip
import json
import subprocess
import time
from dataclasses import replace
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, cast

import pytest

from devtools import audit_n17_endpoint_receipt as exact
from devtools import check_n17_capture_leaf as consumer
from sqpack.hull_kernel.frame import (
    D4_ACTIONS,
    Frame,
    SymmetryAction,
    d4_matrix,
    induced_permutation,
)
from sqpack.hull_kernel.rational import Q as KernelQ


def fixture(action: str = "r0", scale: Q = Q(1)) -> consumer.Leaf:
    offsets = {(0, 0)}
    for x, y in ((1, 0), (1, 1), (1, 2)):
        for name in D4_ACTIONS:
            a, b, c, d = d4_matrix(name)
            offsets.add((a * x + b * y, c * x + d * y))
    points = [(KernelQ(x + 5), KernelQ(y + 5)) for x, y in sorted(offsets)]
    assert len(points) == 17
    cells = tuple((point,) for point in points)
    actions = tuple(
        SymmetryAction(
            name, d4_matrix(name), induced_permutation(cells, d4_matrix(name), KernelQ(5))
        )
        for name in D4_ACTIONS
    )
    frame = Frame(
        "synthetic-exact-frame",
        KernelQ(10),
        KernelQ(scale * 10),
        cells,
        tuple("side-S2" if i == 5 else f"cell{i}" for i in range(17)),
        17,
        actions,
    )
    permutation = next(value.permutation for value in actions if value.name == action)
    roles = {label: permutation.index(label - 1) for label in consumer.LABELS}
    rows = {}
    for owner, point in enumerate(points):
        polygon = [[str(scale * Q(str(value))) for value in point]]
        rows[owner] = [
            {
                "interval": ["0", "1/1000000"],
                "reference": {"owner": owner, "row": 0},
                "residual_polygons": [polygon],
            },
            {
                "interval": ["1/1000000", "1"],
                "reference": {"owner": owner, "row": 1},
                "residual_polygons": [],
            },
        ]
    axes = {name: (exact.point(1), exact.point(0)) for name in ("ex", "u", "p")}
    axes.update({name: (exact.point(0), exact.point(1)) for name in ("ey", "v", "q")})
    layout = exact.Layout(
        {
            label: (
                exact.point(Q(str(points[label - 1][0])) - 1),
                exact.point(Q(str(points[label - 1][1])) - 1),
            )
            for label in consumer.LABELS
        },
        axes,
        {},
        {},
        exact.point(8),
    )
    return consumer.Leaf(
        frame,
        layout,
        rows,
        roles,
        {label: label - 1 for label in consumer.LABELS},
        action,
        {"fresh_replay": True, "original_container_premise": "centred-C(S*)"},
    )


@pytest.mark.parametrize("action", D4_ACTIONS)
def test_exact_rotation_reflection_and_label_transport(action: str) -> None:
    leaf = fixture(action)
    report = consumer.predicates(consumer.bounds(leaf))
    assert report["status"] == "local_terminal"
    assert report["square6_S2"]
    assert len(report["angle_pieces"]) == 16
    assert report["capture_tree_proved"] is False
    for name in consumer.apex.position_names():
        assert report["intervals"][name] == ["0", "0"]


def test_field_scale_is_used_and_root_shift_is_not_midpoint_only() -> None:
    leaf = fixture(scale=Q(3, 2))
    assert consumer.predicates(consumer.bounds(leaf))["status"] == "local_terminal"
    changed = replace(leaf.layout, side=(Q(8), Q(801, 100)))
    report = consumer.predicates(consumer.bounds(replace(leaf, layout=changed)))
    assert report["status"] == "unresolved"
    assert exact.read_interval(report["intervals"]["eta1"])[1] == Q(1, 200)


def test_quarter_turn_equivalence_principal_seam_and_label16() -> None:
    ex = exact.point(1), exact.point(0)
    assert consumer.principal_half_angle(ex, exact.point(0), "r0", 0) == exact.point(0)
    assert consumer.principal_half_angle(ex, exact.point(1), "r0", 3) == exact.point(0)
    assert consumer.principal_half_angle(ex, exact.point(0), "r0", 2) is None
    beta = Q(1, 3)
    p = exact.point((1 - beta**2) / (1 + beta**2)), exact.point(-2 * beta / (1 + beta**2))
    tau = (1 - beta) / (1 + beta)
    assert consumer.principal_half_angle(p, exact.point(tau), "r0", 3) == exact.point(0)


@pytest.mark.parametrize("mutation", ["label", "custody", "premise", "action"])
def test_malformed_source_identity_or_transform_refused(mutation: str) -> None:
    leaf = fixture()
    if mutation == "label":
        roles = dict(leaf.roles)
        roles[1] = roles[2]
        leaf = replace(leaf, roles=roles)
    elif mutation == "custody":
        leaf = replace(leaf, custody={})
    elif mutation == "premise":
        leaf = replace(leaf, custody={"fresh_replay": True})
    else:
        leaf = replace(leaf, action="bad")
    with pytest.raises(exact.AuditError):
        consumer.bounds(leaf)


def test_other_valid_assignment_is_unresolved_never_excluded() -> None:
    leaf = fixture()
    roles = dict(leaf.roles)
    roles[1], roles[2] = roles[2], roles[1]
    assert consumer.bounds(replace(leaf, roles=roles))["reason"] == "unsupported_assignment"


@pytest.mark.parametrize("mutation", ["missing", "open", "overlap"])
def test_closed_orientation_cover_cannot_drop_pieces(mutation: str) -> None:
    leaf = fixture()
    rows = {
        owner: [dict(item) for item in copy.deepcopy(items)]
        for owner, items in leaf.rows.items()
    }
    if mutation == "missing":
        rows[0].pop()
    elif mutation == "open":
        rows[0][1]["interval"][0] = "1/1000"
    else:
        rows[0][1]["interval"][0] = "0"
    with pytest.raises(consumer.OpenCoverage):
        consumer.bounds(replace(leaf, rows=rows))


def bounded_report(position: Q, angle: Q, b: tuple[Q, Q] = (Q(0), Q(0))) -> dict[str, Any]:
    intervals = {
        name: [str(-position), str(position)] for name in consumer.apex.position_names()
    }
    intervals.update({f"q{i}": [str(-angle), str(angle)] for i in consumer.ACTIVE})
    intervals.update({"a": ["0", "1/4"], "b": [str(v) for v in b], "z": ["-1/8", "1/16"]})
    return {"status": "bounded", "intervals": intervals, "square6_S2": True}


def test_local_closed_boundary_and_wide_only_is_never_terminal() -> None:
    local = consumer.predicates(bounded_report(Q(1, 5000), Q(1, 10000)))
    assert local["status"] == "local_terminal"
    wide = consumer.predicates(bounded_report(Q(1, 100), Q(1, 200)))
    assert wide["status"] == "wide_domain_only"
    assert not wide["predicates"]["local_terminal"]
    assert not wide["predicates"]["apex_terminal"]
    assert not wide["predicates"]["patch_exclusion"]


def test_wide_b_floor_cannot_be_inherited_from_small_radius_theorem() -> None:
    report = bounded_report(Q(1, 100), Q(1, 100000), (Q(-1, 2000), Q(0)))
    result = consumer.predicates(report, apex_q0=Q(1, 10000))
    assert result["status"] == "unresolved"
    assert not result["predicates"]["wide_domain"]


def test_only_a_floor_can_use_original_containment_premise() -> None:
    report = bounded_report(Q(1, 100), Q(1, 100000))
    report["intervals"]["a"] = ["-1/100", "1/4"]
    assert consumer.predicates(report)["status"] == "unresolved"
    report["a_floor_from_containment"] = True
    result = consumer.predicates(report)
    assert result["status"] == "wide_domain_only"
    assert result["effective_a_interval"] == ["0", "1/4"]
    assert result["intervals"]["a"] == ["-1/100", "1/4"]
    report["intervals"]["a"] = ["-1/100", "-1/1000"]
    assert consumer.predicates(report)["status"] == "unresolved"


def test_apex_and_entire_closed_patch_require_separate_accepted_inputs() -> None:
    report = bounded_report(Q(1, 100), Q(1, 100000))
    assert consumer.predicates(report)["status"] == "wide_domain_only"
    assert consumer.predicates(report, apex_q0=Q(1, 100000))["status"] == "apex_terminal"
    box = tuple((Q(-1, 100000), Q(1, 100000)) for _ in consumer.ACTIVE)
    assert consumer.predicates(report, patch_box=box)["status"] == "patch_exclusion"
    changed = (*box[:-1], (Q(0), Q(1, 100000)))
    assert consumer.predicates(report, patch_box=changed)["status"] == "wide_domain_only"


def test_reference_escape_and_wrong_frame_cap_refused(monkeypatch: pytest.MonkeyPatch) -> None:
    for path in ("/tmp/x", "../../x"):
        with pytest.raises(exact.AuditError):
            consumer.retained_path(path)
    monkeypatch.setattr(
        consumer.forcing, "load_root", lambda: ({}, fixture().layout, fixture().layout)
    )
    cells = consumer.cover.build_cover(consumer.cover.UNIQUE_24)
    document = {
        "schema": consumer.SCHEMA,
        "state_encoding": "sorted-cell-indices/v1",
        "cover_design": consumer.cover.UNIQUE_24.name,
        "cells": [consumer.cover.cell_record(cell) for cell in cells],
        "U": "10",
        "L": "10",
        "B": "1",
        "capture_cap": "10",
    }
    with pytest.raises(exact.AuditError, match="cap"):
        consumer.load_leaf(document, deadline=1, max_nodes=10)


def test_incomplete_cli_receipt_is_explicit(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    source = tmp_path / "leaf.json"
    source.write_text("{}")

    def incomplete(_document: dict[str, Any], **_kwargs: Any) -> consumer.Leaf:
        raise consumer.OpenCoverage("synthetic open piece")

    monkeypatch.setattr(consumer, "load_leaf", incomplete)
    assert (
        consumer.main(["--leaf", str(source), "--output", str(tmp_path / "receipt.json")]) == 1
    )
    receipt = exact.decode((tmp_path / "receipt.json").read_bytes())
    assert receipt["status"] == "incomplete"
    assert receipt["verification_passed"] is False


@pytest.mark.parametrize("unsupported", [False, True])
def test_successful_and_unsupported_cli_json_roundtrip(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    unsupported: bool,  # noqa: FBT001
) -> None:
    leaf = fixture("f1")
    if unsupported:
        roles = dict(leaf.roles)
        roles[1], roles[2] = roles[2], roles[1]
        leaf = replace(leaf, roles=roles)
    monkeypatch.setattr(consumer, "load_leaf", lambda _document, **_kwargs: leaf)
    source, output = tmp_path / "leaf.json", tmp_path / "receipt.json"
    source.write_text("{}")
    assert consumer.main(["--leaf", str(source), "--output", str(output)]) == 0
    receipt = exact.decode(output.read_bytes())
    assert receipt["verification_passed"] is True
    assert receipt["status"] == ("unresolved" if unsupported else "local_terminal")
    assert receipt["global_admission_proved"] is False
    assert receipt["capture_tree_proved"] is False
    assert receipt["terminal_inputs"] == {"features": None, "apex": None, "patch": None}


def test_optional_terminal_certificate_inputs_are_retained_in_cli_receipt(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setattr(consumer, "load_leaf", lambda _document, **_kwargs: fixture())
    angle_box = [["-1/200", "1/200"] for _ in consumer.ACTIVE]
    packet = {"q0": "1/100000", "attempts": [{"angle_box": angle_box}]}
    monkeypatch.setattr(consumer.exact, "read_bytes", lambda _path: json.dumps(packet).encode())
    monkeypatch.setattr(
        consumer.apex,
        "check",
        lambda _packet, _path: {"verification_passed": True, "q0": "1/100000"},
    )
    monkeypatch.setattr(
        consumer.patch,
        "check",
        lambda _packet, _features, _apex: {"positive_patch_certified": True},
    )
    output = tmp_path / "receipt.json"
    assert (
        consumer.main(
            [
                "--leaf",
                "synthetic/leaf.json",
                "--features",
                "synthetic/features.json",
                "--apex",
                "synthetic/apex.json",
                "--patch",
                "synthetic/patch.json",
                "--output",
                str(output),
            ]
        )
        == 0
    )
    receipt = exact.decode(output.read_bytes())
    joins = receipt["terminal_inputs"]
    assert joins["features"].endswith("synthetic/features.json")
    assert joins["apex"]["path"].endswith("synthetic/apex.json")
    assert joins["apex"]["q0"] == "1/100000"
    assert joins["patch"]["path"].endswith("synthetic/patch.json")
    assert joins["patch"]["angle_box"] == angle_box


def test_empty_owner_requires_separate_exclusion_consumer() -> None:
    leaf = fixture()
    rows = {
        owner: [dict(item) for item in copy.deepcopy(items)]
        for owner, items in leaf.rows.items()
    }
    for item in rows[0]:
        item["residual_polygons"] = []
    report = consumer.predicates(consumer.bounds(replace(leaf, rows=rows)))
    assert report["status"] == "unresolved"
    assert report["reason"] == "empty_owner_requires_exclusion_consumer"


@pytest.mark.parametrize("mutation", ["accepted", "receipt", "fresh_replay"])
def test_validated_loader_binds_sources_and_requires_fresh_replay(
    monkeypatch: pytest.MonkeyPatch, mutation: str
) -> None:
    cells = consumer.cover.build_cover(consumer.cover.UNIQUE_24)
    expected = {label: label - 1 for label in consumer.LABELS}
    sixth = next(i for i, cell in enumerate(cells) if cell.name == "side-S2")
    other_label = sixth + 1
    expected[6], expected[other_label] = sixth, 5
    root_layout = replace(fixture().layout, side=exact.point(4))
    monkeypatch.setattr(
        consumer.forcing,
        "load_root",
        lambda: (
            {"root_inclusion_box_used": [["0", "0"], ["0", "0"]]},
            root_layout,
            root_layout,
        ),
    )
    monkeypatch.setattr(consumer.cover, "endpoint", lambda *_args: None)
    monkeypatch.setattr(
        consumer.cover,
        "family_state",
        lambda *_args: {
            "one_state": True,
            "squares": [
                {"label": label, "cell": cells[owner].name} for label, owner in expected.items()
            ],
        },
    )
    seed_packet, node_packet = {"bins": 2}, {"node_id": "synthetic"}
    receipt = {
        "replay": {"status": "PASS_REPLAYED", "final_state_agrees": True},
        "node_sha256": consumer.producer.content_sha256(node_packet),
        "seed_sha256": consumer.producer.content_sha256(seed_packet),
    }
    if mutation == "receipt":
        receipt["node_sha256"] = "wrong-source"
    packets = {"seed.json": seed_packet, "node.json": node_packet, "receipt.json": receipt}
    monkeypatch.setattr(
        consumer.exact, "read_bytes", lambda path: json.dumps(packets[path.name]).encode()
    )
    calls = []

    def seed_check(_frame: Frame, source: dict[str, Any], **kwargs: Any) -> consumer.node.Seed:
        calls.append("seed")
        assert source == seed_packet
        assert kwargs["mask"] == list(range(17))
        return consumer.node.Seed({}, {})

    def node_check(
        _frame: Frame, source: dict[str, Any], _seed: consumer.node.Seed, **kwargs: Any
    ) -> consumer.sequential.SequentialTrace:
        calls.append("node")
        assert source == node_packet
        assert kwargs["seed_sha256"] == receipt["seed_sha256"]
        if mutation == "fresh_replay":
            raise ValueError("synthetic fresh replay refusal")
        return consumer.sequential.SequentialTrace(rows=cast(Any, dict(fixture().rows)))

    monkeypatch.setattr(consumer.node, "admit_seed", seed_check)
    monkeypatch.setattr(consumer.sequential, "replay_sequential", node_check)
    document = {
        "schema": consumer.SCHEMA,
        "state_encoding": "sorted-cell-indices/v1",
        "cover_design": consumer.cover.UNIQUE_24.name,
        "cells": [consumer.cover.cell_record(cell) for cell in cells],
        "U": str(consumer.cover.U),
        "L": str(consumer.cover.U),
        "B": "1",
        "capture_cap": str(consumer.cover.U),
        "state": list(range(17)),
        "label_to_owner": {str(label): owner for label, owner in expected.items()},
        "seed": "synthetic/seed.json",
        "node": "synthetic/node.json",
        "producer_receipt": "synthetic/receipt.json",
        "action": "r0",
        "original_container_premise": "centred-C(S*)",
        "composition_premise": consumer.COMPOSITION,
    }
    if mutation == "accepted":
        leaf = consumer.load_leaf(document, deadline=1, max_nodes=10)
        assert leaf.custody["fresh_replay"]
        assert leaf.expected_roles == expected
        assert calls == ["seed", "node"]
    else:
        with pytest.raises(ValueError, match=r"custody|fresh replay"):
            consumer.load_leaf(document, deadline=1, max_nodes=10)
        assert calls == ([] if mutation == "receipt" else ["seed", "node"])


@pytest.mark.parametrize("scale", [Q(1), Q(3, 2)])
def test_none_and_numeric_u_have_identical_affine_and_seed_walls(scale: Q) -> None:
    frame = fixture(scale=scale).frame
    seed = {"cells": {"0": [{"interval": ["0", "1/3"]}, {"interval": ["1/3", "1"]}]}}
    checked = consumer.wall_normalization(frame, seed)
    assert checked["original_capture_cap"] is None
    assert checked["normalized_inner_cap"] == "10"
    assert checked["seed_wall_rows_checked"] == 2
    assert checked["affine_formula"] == "offset=0; field bounds=(B*h, B*(U-h))"
    with pytest.raises(exact.AuditError, match="original cap None"):
        consumer.wall_normalization(replace(frame, capture_cap=KernelQ(9)), seed)


def test_direct_v9_keeps_thin_polygon_correlation() -> None:
    leaf = fixture()
    rows = cast(dict[int, list[dict[str, Any]]], copy.deepcopy(dict(leaf.rows)))
    # Along u=(4/5,3/5), v=(-3/5,4/5) the direct projection is exactly zero.
    centre = [Q(value) for value in rows[8][0]["residual_polygons"][0][0]]
    rows[8][0]["residual_polygons"] = [
        [
            [str(centre[0] + sign * Q(2, 25)), str(centre[1] + sign * Q(3, 50))]
            for sign in (-1, 1)
        ]
    ]
    axes = dict(leaf.layout.axes)
    axes["u"] = exact.point(Q(4, 5)), exact.point(Q(3, 5))
    axes["v"] = exact.point(Q(-3, 5)), exact.point(Q(4, 5))
    report = consumer.bounds(replace(leaf, rows=rows, layout=replace(leaf.layout, axes=axes)))
    assert report["intervals"]["v9"] == ["0", "0"]
    loose = exact.dot(
        axes["v"],
        (
            exact.read_interval(report["intervals"]["xi9"]),
            exact.read_interval(report["intervals"]["eta9"]),
        ),
    )
    assert loose == (Q(-12, 125), Q(12, 125))
    assert "v9" not in consumer.apex.position_names()


@pytest.mark.parametrize("failure", ["truncated", "oversize", "deadline"])
def test_saved_gzip_input_is_bounded_and_resource_status_is_explicit(
    tmp_path: Path,
    failure: str,
) -> None:
    path = tmp_path / "input.json.gz"
    raw = gzip.compress(b"0123456789")
    path.write_bytes(raw[:-6] if failure == "truncated" else raw)
    if failure == "deadline":
        with pytest.raises(consumer.IncompleteError, match="wall ceiling"):
            consumer.bounded_gzip(path, 10, deadline=0)
    elif failure == "oversize":
        with pytest.raises(exact.AuditError, match="decoded byte ceiling"):
            consumer.bounded_gzip(path, 9, deadline=time.monotonic() + 10)
    else:
        with pytest.raises(EOFError):
            consumer.bounded_gzip(path, 10, deadline=time.monotonic() + 10)


@pytest.mark.parametrize(
    "mutation",
    [
        "accepted",
        "seed_id",
        "node_id",
        "guard",
        "sampled",
        "incomplete",
        "closed",
        "frame",
        "mask",
        "step_count",
        "stale_receipt",
        "changed_file",
        "trailing_data",
        "root",
        "remaining_time",
        "expired_before_launch",
    ],
)
def test_saved_prefix_binds_eof_fresh_receipt_and_frozen_objects(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    mutation: str,
) -> None:
    frame = fixture().frame
    seed = {"bins": 2, "cells": {"0": [{"interval": ["0", "1"]}]}}
    packet = {
        "parent": None,
        "guard_source": None,
        "constraints": [],
        "steps": [{"index": 0, "owner": 0, "complete": True}],
        "terminal": False,
    }
    if mutation == "guard":
        packet["guard_source"] = "unsupported"
    seed_id = consumer.producer.content_sha256(seed)
    node_id = consumer.producer.content_sha256(packet)
    directory = tmp_path / "objects"
    directory.mkdir()
    seed_path, node_path = (
        directory / "seed-any-name.json.gz",
        directory / "node-any-name.json.gz",
    )
    seed_path.write_bytes(gzip.compress(json.dumps(seed).encode()))
    raw = json.dumps(packet, sort_keys=True).encode()
    node_path.write_bytes(gzip.compress(raw + (b"{}" if mutation == "trailing_data" else b"")))
    source = {
        "status": "PASS_ENDPOINT_PREFIX",
        "control_passed": True,
        "inputs": {"root": {"synthetic": True}},
        "seed_sha256": seed_id,
        "node_sha256": node_id,
        "complete_owner_updates": 1,
        "closure": None,
    }
    source_path = tmp_path / "producer.json"
    source_path.write_text(json.dumps(source))
    monkeypatch.setattr(
        consumer,
        "retained_path",
        lambda value: directory if value == "objects" else source_path,
    )
    monkeypatch.setattr(
        consumer.node, "admit_seed", lambda *_args, **_kwargs: consumer.node.Seed({}, {})
    )

    def replay(_frame: Frame, value: dict[str, Any], _seed: Any, **kwargs: Any) -> Any:
        steps = list(value["steps"])
        if mutation in {"remaining_time", "expired_before_launch"}:
            deadline = kwargs["budget"].deadline
            remaining = 0.25 if mutation == "remaining_time" else 0
            monkeypatch.setattr(consumer.time, "monotonic", lambda: deadline - remaining)
        return consumer.sequential.SequentialTrace(rows=cast(Any, fixture().rows), steps=steps)

    monkeypatch.setattr(consumer.sequential, "replay_sequential", replay)
    fresh = {
        "status": "PASS_SAVED_STALL",
        "closure": None,
        "producer_imported": False,
        "steps_checked": 1,
        "seed_sha256": seed_id,
        "node_sha256": node_id,
        "frame": frame.name,
        "mask": list(range(17)),
        "cells": list(frame.cell_names),
        "bins": 2,
        "cover_backend": "indexed",
    }
    if mutation in {"sampled", "incomplete", "closed"}:
        fresh["status"] = {
            "sampled": "PASS_SAMPLE",
            "incomplete": "INCOMPLETE",
            "closed": "PASS_SAVED_CLOSED",
        }[mutation]
    elif mutation == "frame":
        fresh["frame"] = "different"
    elif mutation == "mask":
        fresh["mask"] = [0]
    elif mutation == "step_count":
        fresh["steps_checked"] = 2
    elif mutation == "stale_receipt":
        fresh["node_sha256"] = "stale"

    def fresh_replay(_directory: Path, _seconds: float) -> dict[str, Any]:
        if mutation == "expired_before_launch":
            pytest.fail("expired parent must not launch fresh replay")
        if mutation == "remaining_time":
            assert _seconds == 0.25
        if mutation == "changed_file":
            node_path.write_bytes(gzip.compress(raw, mtime=42))
        return {"command": ["synthetic-clean-interpreter"], "exit_code": 0, "receipt": fresh}

    monkeypatch.setattr(consumer, "fresh_saved_replay", fresh_replay)
    document = {
        "action": "r0",
        "expected_steps": 1,
        "root": {"synthetic": True},
        "state": list(range(17)),
        "saved_objects": "objects",
        "producer_receipt": "producer",
        "seed_sha256": "wrong" if mutation == "seed_id" else seed_id,
        "node_sha256": "wrong" if mutation == "node_id" else node_id,
    }
    if mutation == "root":
        document["root"] = {"synthetic": False}
    if mutation in {"accepted", "remaining_time"}:
        rows, custody = consumer.load_saved_prefix(
            document, frame, deadline=time.monotonic() + 10, max_nodes=100, replay_seconds=1
        )
        assert set(rows) == set(range(17))
        assert custody["node_sha256"] == node_id
        assert custody["fresh_full_replay"]["receipt"]["producer_imported"] is False
    elif mutation == "expired_before_launch":
        with pytest.raises(consumer.IncompleteError, match="parent leaf ceiling"):
            consumer.load_saved_prefix(
                document, frame, deadline=time.monotonic() + 10, max_nodes=100, replay_seconds=1
            )
    else:
        with pytest.raises(ValueError, match=r"saved|fresh|data follows"):
            consumer.load_saved_prefix(
                document, frame, deadline=time.monotonic() + 10, max_nodes=100, replay_seconds=1
            )


@pytest.mark.parametrize("timeout", [False, True])
def test_fresh_replay_uses_clean_interpreter_and_no_producer_updates(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    timeout: bool,  # noqa: FBT001
) -> None:
    def execute(command: list[str], **kwargs: Any) -> subprocess.CompletedProcess[bytes]:
        assert command[:3] == [consumer.sys.executable, "-m", "devtools.check_n17_subpattern"]
        assert "--check-saved" in command
        assert "--cover" in command
        assert kwargs["timeout"] == 1
        if timeout:
            raise subprocess.TimeoutExpired(command, 1)
        kwargs["stdout"].write(b'{"status":"PASS_SAVED_STALL"}')
        return subprocess.CompletedProcess(command, 0)

    monkeypatch.setattr(consumer.subprocess, "run", execute)
    if timeout:
        with pytest.raises(consumer.IncompleteError, match="fresh saved replay wall"):
            consumer.fresh_saved_replay(tmp_path, 1)
    else:
        assert (
            consumer.fresh_saved_replay(tmp_path, 1)["receipt"]["status"] == "PASS_SAVED_STALL"
        )


@pytest.mark.parametrize("mutation", ["accepted", "label", "pose", "root"])
def test_saved_endpoint_join_uses_all17_boxes_not_midpoints(
    monkeypatch: pytest.MonkeyPatch,
    mutation: str,
) -> None:
    leaf = fixture()
    rows = cast(dict[int, list[dict[str, Any]]], copy.deepcopy(dict(leaf.rows)))
    poses = []
    for label, owner in leaf.roles.items():
        x, y = map(Q, rows[owner][0]["residual_polygons"][0][0])
        epsilon = Q(1, 10000)
        rows[owner][0]["residual_polygons"] = [
            [
                [str(xx), str(yy)]
                for xx, yy in (
                    (x - epsilon, y - epsilon),
                    (x + epsilon, y - epsilon),
                    (x + epsilon, y + epsilon),
                    (x - epsilon, y + epsilon),
                )
            ]
        ]
        poses.append(
            consumer.prefix.EndpointPose(
                label,
                owner,
                (
                    consumer.Box(x - epsilon, x + epsilon),
                    consumer.Box(y - epsilon, y + epsilon),
                ),
                ((KernelQ(0), KernelQ(0)),),
            )
        )
    if mutation == "pose":
        midpoint = (poses[-1].centre[0].lo + poses[-1].centre[0].hi) / 2
        poses[-1] = replace(
            poses[-1],
            centre=(
                consumer.Box(midpoint - Q(1, 100), midpoint + Q(1, 100)),
                poses[-1].centre[1],
            ),
        )
    roles = dict(leaf.roles)
    if mutation == "label":
        roles[1], roles[2] = roles[2], roles[1]
    monkeypatch.setattr(
        consumer.prefix,
        "load_endpoint",
        lambda: (
            leaf.frame,
            tuple(poses),
            {"root": {"synthetic": True}},
        ),
    )
    root = {"synthetic": mutation != "root"}
    if mutation == "accepted":
        checked = consumer.saved_endpoint_retention(
            leaf.frame, roles, leaf.expected_roles, root, rows
        )
        assert checked["held"] is True
        assert len(checked["owners"]) == 17
    else:
        with pytest.raises(ValueError, match="endpoint"):
            consumer.saved_endpoint_retention(
                leaf.frame, roles, leaf.expected_roles, root, rows
            )


@pytest.mark.parametrize("contains_zero", [False, True])
def test_saved_cli_retains_readiness_and_zero_interval_join_without_global_claim(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    contains_zero: bool,  # noqa: FBT001
) -> None:
    leaf = fixture()
    custody = {**leaf.custody, "saved_objects": "synthetic/objects"}
    if not contains_zero:
        centres = dict(leaf.layout.centres)
        centres[1] = exact.add(centres[1][0], exact.point(Q(1, 100))), centres[1][1]
        leaf = replace(leaf, layout=replace(leaf.layout, centres=centres))
    leaf = replace(leaf, custody=custody)
    monkeypatch.setattr(consumer, "load_leaf", lambda _document, **_kwargs: leaf)
    descriptor, output = tmp_path / "leaf.json", tmp_path / "receipt.json"
    descriptor.write_text("{}")
    assert consumer.main(["--leaf", str(descriptor), "--output", str(output)]) == (
        0 if contains_zero else 1
    )
    report = exact.decode(output.read_bytes())
    assert report["global_admission_proved"] is False
    assert report["capture_tree_proved"] is False
    if contains_zero:
        assert report["intervals"]["v9"] == ["0", "0"]
        assert report["status"] == "local_terminal"
    else:
        assert report["status"] == "refused"
