"""Target-free closed-domain, frame and terminal-predicate controls."""

from __future__ import annotations

import copy
import json
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
