"""Target-free finite algebra, accepted-premise custody and clean CLI controls.

The synthetic H290 receipt is a loader fixture, not a geometric certificate or
a feasible seventeen-square packing.
"""

from __future__ import annotations

import copy
import gzip
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

import pytest

from devtools import probe_n17_conditional_owned_hull as control

Q = control.Q


def rows(count: int = 64, *, centre: str = "1") -> list[dict[str, Any]]:
    return [
        {
            "interval": [str(Q(i, count)), str(Q(i + 1, count))],
            "reference": {"kind": "synthetic", "row": i},
            "outer_domain": [[centre, centre]],
            "residual_polygons": [[[centre, centre]]],
        }
        for i in range(count)
    ]


def fixture(tmp_path: Path) -> tuple[dict[str, Any], Path]:
    mask = list(range(17))
    names = [
        "corner-SW" if i == 0 else "side-S2" if i == 5 else f"synthetic-{i}" for i in range(24)
    ]
    frame = {
        "U": str(control.U),
        "L": str(control.U),
        "B": "1",
        "capture_cap": str(control.V),
        "occupancy": 17,
        "cell_names": names,
        "cells": [[["0", "0"], ["2", "0"], ["2", "2"], ["0", "2"]] for _ in names],
        "actions": [
            {"name": a, "matrix": [1, 0, 0, 1], "permutation": list(range(24))}
            for a in ("r0", "r1", "r2", "r3", "f0", "f1", "f2", "f3")
        ],
    }
    seed = {"U": str(control.U), "B": "1", "mask": mask, "bins": 32, "world": frame["cells"]}
    seed_id = control.identity(seed)
    order = [o for o in mask if o != 5]
    final = {
        "U": str(control.U),
        "B": "1",
        "mask": mask,
        "mask_index": None,
        "source": {"sha256": seed_id},
        "world": frame["cells"],
        "constraints": [],
        "guard": {},
        "guard_source": None,
        "groups": {str(o): [] for o in mask},
        "cells": {str(o): rows(32 if o == 5 else 64) for o in mask},
    }
    # Keep one live row for the finite reconstruction success fixture. The full
    # row inventory remains closed and complete; empty rows impose no planes.
    for owner_rows in final["cells"].values():
        for row in owner_rows[1:]:
            row["outer_domain"] = []
            row["residual_polygons"] = []
    node = {
        "U": str(control.U),
        "B": "1",
        "mask": mask,
        "mask_index": None,
        "source": {"sha256": seed_id},
        "parent": None,
        "guard_source": None,
        "constraints": [],
        "steps": [{"owner": o} for o in order],
        "final_state": final,
        "closed": False,
        "terminal": False,
        "contradiction": None,
    }
    directory = tmp_path / "objects"
    directory.mkdir()
    digests = {}
    for kind, value in (("seed", seed), ("node", node)):
        path = directory / f"{kind}-synthetic.json.gz"
        path.write_bytes(gzip.compress(control.canonical(value), mtime=0))
        digests[str(path.relative_to(tmp_path))] = hashlib.sha256(path.read_bytes()).hexdigest()
    owners = [
        {"label": i, "owner": i - 1, "witness": {"synthetic": True}} for i in range(1, 18)
    ]
    receipt = {
        "schema": "n17-numeric-cap-checkpoint/v1",
        "readiness_passed": True,
        "verification_passed": True,
        "saved_checkpoint_replayed": True,
        "root": {"synthetic_accepted_premise": True},
        "intervals": {f"synthetic{i}": ["0", "0"] for i in range(49)},
        "custody": {
            "parent_replay": {
                "frame": frame,
                "mask": mask,
                "status": "PASS_SAVED_STALL",
                "closure": None,
                "steps_checked": 16,
                "step_owners": order,
                "seed_sha256": seed_id,
                "node_sha256": control.identity(node),
                "compressed_object_sha256": digests,
            },
            "endpoint_retention": {"held": True, "lost_labels": [], "owners": owners},
            "input_control": {
                "endpoint_roster": [
                    {
                        "label": i,
                        "owner": i - 1,
                        "centre": [["1", "1"], ["1", "1"]],
                        "charts": [["0", "0"], ["1", "1"]],
                    }
                    for i in range(1, 18)
                ]
            },
        },
    }
    receipt_path = tmp_path / "h290.json"
    receipt["custody"]["fresh_replay"] = {
        "exit_code": 0,
        "receipt": {
            **copy.deepcopy(receipt["custody"]["parent_replay"]),
            "producer_imported": False,
        },
    }
    receipt_path.write_text(json.dumps(receipt))
    document = {
        "schema": control.SCHEMA,
        "h290_receipt": "h290.json",
        "h290_receipt_sha256": hashlib.sha256(receipt_path.read_bytes()).hexdigest(),
        "label_to_owner": {str(i): i - 1 for i in range(1, 18)},
        "frame": frame,
        "saved_objects": "objects",
        "compressed_sha256": digests,
        "seed_sha256": seed_id,
        "node_sha256": control.identity(node),
    }
    path = tmp_path / "descriptor.json"
    path.write_text(json.dumps(document))
    return document, path


def test_closed_guard_keeps_both_adjacent_singleton_rows() -> None:
    value = control.reconstruct(rows(), control.GUARDS["target"], time.monotonic() + 10)
    joins = value["row_intersections"]
    assert [r["row"] for r in joins] == [25, 26, 27]
    assert joins[0]["intersection"] == ["13/32", "13/32"]
    assert joins[-1]["intersection"] == ["27/64", "27/64"]


def test_guard_points_satisfy_every_rectangle_corner_halfplane() -> None:
    value = control.reconstruct(rows(), control.GUARDS["target"], time.monotonic() + 10)
    points = control.polygon(value["selected"])
    assert points
    for joined in value["row_intersections"]:
        lo, hi = map(Q, joined["intersection"])
        c0, s0 = control.trig(lo)
        c1, s1 = control.trig(hi)
        for centre in control.polygon(joined["centre_hull"]):
            for c in (c1, c0):
                for s in (s0, s1):
                    for sign in (-1, 1):
                        for p in points:
                            delta = (p[0] - centre[0], p[1] - centre[1])
                            assert (
                                control.dot(delta, (sign * c, sign * s))
                                <= Q(1, 2) - control.MARGIN
                            )
                            assert (
                                control.dot(delta, (-sign * s, sign * c))
                                <= Q(1, 2) - control.MARGIN
                            )


def test_numeric_wall_clip_applies_to_all_angle_control() -> None:
    value = control.reconstruct(
        rows(1, centre="0"), control.GUARDS["all"], time.monotonic() + 10
    )
    assert value["row_intersections"][0]["centre_hull"] == []
    assert value["planes"] == 0
    assert len(value["kernel"]) == 4


def test_support_ties_are_lexicographic_and_deduplicated() -> None:
    value = control.reconstruct(rows(1), (Q(0), Q(0)), time.monotonic() + 10)
    selected = control.polygon(value["selected"])
    expected = Q(3, 2) - control.MARGIN
    assert value["selected"][0] == [str(expected), str(Q(1, 2) + control.MARGIN)]
    assert len(selected) == 4


def test_gain_exact_support_threshold_and_empty_baseline_area() -> None:
    baseline = [(Q(0), Q(0))]
    assert control.gain([(control.GAIN, Q(0))], baseline)["passed"] is True
    assert control.gain([(control.GAIN / 2, Q(0))], baseline)["passed"] is False
    box = [(Q(0), Q(0)), (Q(1, 1024), Q(0)), (Q(1, 1024), Q(1, 1024)), (Q(0), Q(1, 1024))]
    assert control.gain(box, [])["passed"] is True
    assert control.gain(box[:2], [])["passed"] is False
    assert control.gain([], baseline)["passed"] is False


def test_canonical_stream_and_finite_roundtrip(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    document, _path = fixture(tmp_path)
    monkeypatch.setattr(control, "REPO", tmp_path)
    certificate = control.generate(document, deadline=time.monotonic() + 10)
    assert certificate["status"] == "unconditional_refresh_candidate"
    assert certificate["custody"]["parent_geometry_replayed"] is False
    assert certificate["custody"]["root_checked_now"] is False
    assert certificate["endpoint_control"]["strictly_inside"] is True
    decoded = json.loads(control.retained_json.dumps(certificate))
    assert control.check(document, decoded, deadline=time.monotonic() + 10)[
        "finite_reconstruction_verified"
    ]
    decoded["variants"]["target"]["selected"][0][0] = "0"
    with pytest.raises(ValueError, match="certificate differs"):
        control.check(document, decoded, deadline=time.monotonic() + 10)


@pytest.mark.parametrize(
    "mutation", ["receipt", "node", "seed", "frame", "labels", "endpoint", "bounds"]
)
def test_changed_accepted_premises_refuse(
    mutation: str,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    document, _path = fixture(tmp_path)
    monkeypatch.setattr(control, "REPO", tmp_path)
    if mutation == "receipt":
        (tmp_path / "h290.json").write_text("{}")
    elif mutation in {"node", "seed"}:
        document[f"{mutation}_sha256"] = "0" * 64
    elif mutation == "frame":
        document["frame"]["B"] = "2"
    elif mutation == "labels":
        document["label_to_owner"]["1"] = 1
    else:
        path = tmp_path / "h290.json"
        receipt = json.loads(path.read_text())
        if mutation == "endpoint":
            receipt["custody"]["endpoint_retention"]["held"] = False
        else:
            receipt["intervals"]["synthetic0"] = ["1", "2"]
        path.write_text(json.dumps(receipt))
        document["h290_receipt_sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
    with pytest.raises(ValueError, match=r"differ|premise"):
        control.generate(document, deadline=time.monotonic() + 10)


@pytest.mark.parametrize("limit", ["bits", "vertices", "seed", "node", "slice", "wall"])
def test_resource_stops_never_report_gain(
    limit: str,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    document, _path = fixture(tmp_path)
    monkeypatch.setattr(control, "REPO", tmp_path)
    if limit == "bits":
        monkeypatch.setattr(control, "BIT_LIMIT", 1)
    elif limit == "vertices":
        monkeypatch.setattr(control, "VERTEX_LIMIT", 0)
    elif limit == "seed":
        monkeypatch.setattr(control, "SEED_LIMIT", 1)
    elif limit == "node":
        monkeypatch.setattr(control, "DECODED_LIMIT", 1)
    elif limit == "slice":
        monkeypatch.setattr(control, "SLICE_LIMIT", 1)
    with pytest.raises(control.IncompleteError):
        control.generate(document, deadline=time.monotonic() + (-1 if limit == "wall" else 10))


@pytest.mark.parametrize("mutation", ["truncated", "trailing", "final_headers", "row_count"])
def test_node_eof_and_final_state_are_required(
    mutation: str,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    document, _path = fixture(tmp_path)
    monkeypatch.setattr(control, "REPO", tmp_path)
    node_path = tmp_path / "objects/node-synthetic.json.gz"
    raw = gzip.decompress(node_path.read_bytes())
    if mutation == "truncated":
        node_path.write_bytes(node_path.read_bytes()[:-8])
    elif mutation == "trailing":
        node_path.write_bytes(gzip.compress(raw + b"{}", mtime=0))
    else:
        node = json.loads(raw)
        if mutation == "final_headers":
            node["final_state"]["guard_source"] = "unsupported"
        else:
            node["final_state"]["cells"]["0"].pop()
        raw = control.canonical(node)
        node_path.write_bytes(gzip.compress(raw, mtime=0))
        document["node_sha256"] = control.identity(node)
    document["compressed_sha256"][str(node_path.relative_to(tmp_path))] = hashlib.sha256(
        node_path.read_bytes()
    ).hexdigest()
    receipt_path = tmp_path / "h290.json"
    receipt = json.loads(receipt_path.read_text())
    receipt["custody"]["parent_replay"]["compressed_object_sha256"] = document[
        "compressed_sha256"
    ]
    receipt["custody"]["parent_replay"]["node_sha256"] = document["node_sha256"]
    receipt["custody"]["fresh_replay"]["receipt"]["node_sha256"] = document["node_sha256"]
    receipt_path.write_text(json.dumps(receipt))
    document["h290_receipt_sha256"] = hashlib.sha256(receipt_path.read_bytes()).hexdigest()
    with pytest.raises((ValueError, EOFError, control.standing.VerificationError)):
        control.generate(document, deadline=time.monotonic() + 10)


def test_clean_fresh_cli_reconstructs_without_scientific_modules(tmp_path: Path) -> None:
    _document, path = fixture(tmp_path)
    certificate, replay = tmp_path / "certificate.json", tmp_path / "replay.json"
    bootstrap = (
        "import sys; from pathlib import Path; "
        "from devtools import probe_n17_conditional_owned_hull as m; "
        "m.REPO=Path(sys.argv.pop(1)); raise SystemExit(m.main(sys.argv[1:]))"
    )
    first = [
        sys.executable,
        "-c",
        bootstrap,
        str(tmp_path),
        "--descriptor",
        str(path),
        "--output",
        str(certificate),
    ]
    second = [
        sys.executable,
        "-c",
        bootstrap,
        str(tmp_path),
        "--descriptor",
        str(path),
        "--check",
        str(certificate),
        "--output",
        str(replay),
    ]
    for command in (first, second):
        execution = subprocess.run(
            command,
            capture_output=True,
            timeout=20,
            check=False,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )
        assert execution.returncode == 0, execution.stderr.decode()
    checked = json.loads(replay.read_text())
    assert checked["finite_reconstruction_verified"] is True
    assert checked["producer_run"] is False
    assert checked["parent_geometry_replayed"] is False


@pytest.mark.parametrize(
    "kind", ["conditional", "no_gain", "endpoint_failure", "endpoint_empty"]
)
def test_gain_decision_order_and_endpoint_controls(
    kind: str,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    document, _path = fixture(tmp_path)
    monkeypatch.setattr(control, "REPO", tmp_path)
    final, custody = control.extract(document, time.monotonic() + 10)
    if kind == "conditional":
        complete = rows()
        for index in (25, 26, 27):
            final["cells"]["0"][index] = complete[index]
        all_points = control.reconstruct(
            final["cells"]["0"], control.GUARDS["all"], time.monotonic() + 10
        )["selected_hull"]
        final["groups"]["0"] = all_points
    elif kind == "no_gain":
        final["groups"]["0"] = [
            ["0", "0"],
            [str(control.U), "0"],
            [str(control.U), str(control.U)],
            ["0", str(control.U)],
        ]
    elif kind == "endpoint_failure":
        custody["label1_geometry"]["centre"] = [["10", "10"], ["10", "10"]]
    else:
        final["cells"]["0"][1]["residual_polygons"] = [[["3", "1"]]]
    monkeypatch.setattr(control, "extract", lambda *_: (final, custody))
    result = control.generate(document, deadline=time.monotonic() + 10)
    expected = {
        "conditional": "conditional_gain_candidate",
        "no_gain": "no_gain_under_frozen_recipe",
        "endpoint_failure": "refused_endpoint_control",
        "endpoint_empty": "inconclusive_control_empty",
    }
    assert result["status"] == expected[kind]
    assert result["producer_run"] is False
    assert result["conditional_owned_exclusion"] is False
    if kind == "conditional":
        assert all(
            row["centre_hull"] for row in result["variants"]["target"]["row_intersections"]
        )
        assert result["variants"]["target"]["planes"] > 0


def test_extended_native_source_record_is_carried_not_restricted(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    document, _path = fixture(tmp_path)
    monkeypatch.setattr(control, "REPO", tmp_path)
    path = tmp_path / "objects/node-synthetic.json.gz"
    node = json.loads(gzip.decompress(path.read_bytes()))
    node["source"]["kind"] = "generic_wall_seed"
    node["source"]["path"] = "synthetic retained seed reference"
    node["final_state"]["source"] = copy.deepcopy(node["source"])
    path.write_bytes(gzip.compress(control.canonical(node), mtime=0))
    document["node_sha256"] = control.identity(node)
    document["compressed_sha256"][str(path.relative_to(tmp_path))] = hashlib.sha256(
        path.read_bytes()
    ).hexdigest()
    receipt_path = tmp_path / "h290.json"
    receipt = json.loads(receipt_path.read_text())
    for key in ("parent_replay",):
        receipt["custody"][key]["node_sha256"] = document["node_sha256"]
        receipt["custody"][key]["compressed_object_sha256"] = document["compressed_sha256"]
    receipt["custody"]["fresh_replay"]["receipt"]["node_sha256"] = document["node_sha256"]
    receipt_path.write_text(json.dumps(receipt))
    document["h290_receipt_sha256"] = hashlib.sha256(receipt_path.read_bytes()).hexdigest()
    assert (
        control.generate(document, deadline=time.monotonic() + 10)["status"]
        == "unconditional_refresh_candidate"
    )


def test_saved_bytes_changed_during_finite_construction_refuse(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    document, _path = fixture(tmp_path)
    monkeypatch.setattr(control, "REPO", tmp_path)
    original = control.reconstruct

    def mutate(*args: Any) -> dict[str, Any]:
        result = original(*args)
        (tmp_path / "objects/seed-synthetic.json.gz").write_bytes(b"changed")
        return result

    monkeypatch.setattr(control, "reconstruct", mutate)
    with pytest.raises(ValueError, match="changed during finite construction"):
        control.generate(document, deadline=time.monotonic() + 10)


@pytest.mark.parametrize("centre", [[["1", "1"]], [["1", "0"], ["1", "1"]]])
def test_endpoint_centre_missing_axis_or_reversed_interval_refuses(
    centre: list[list[str]],
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    document, _path = fixture(tmp_path)
    monkeypatch.setattr(control, "REPO", tmp_path)
    path = tmp_path / "h290.json"
    receipt = json.loads(path.read_text())
    receipt["custody"]["input_control"]["endpoint_roster"][0]["centre"] = centre
    path.write_text(json.dumps(receipt))
    document["h290_receipt_sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
    with pytest.raises(ValueError, match=r"two-axis.*(ordered|shape)"):
        control.generate(document, deadline=time.monotonic() + 10)


def test_retained_metadata_rational_bit_ceiling() -> None:
    with pytest.raises(control.IncompleteError, match="bit ceiling"):
        control.rational_tree({"accepted_numeric_metadata": str(2**4097)})


@pytest.mark.parametrize("value", ["1e999999999", "0.125", "01/2", "1/-2", "1/0"])
def test_noncanonical_rational_grammar_refuses_before_fraction_allocation(
    value: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        control, "Q", lambda *_: pytest.fail("Fraction allocation before grammar")
    )
    with pytest.raises(ValueError, match="grammar required"):
        control.rational(value)


def rebind_synthetic_parent(
    document: dict[str, Any],
    tmp_path: Path,
    receipt: dict[str, Any],
    node: dict[str, Any] | None = None,
) -> None:
    """Simulate a newly admitted fixture, without asserting geometric acceptance."""
    if node is not None:
        path = tmp_path / "objects/node-synthetic.json.gz"
        path.write_bytes(gzip.compress(control.canonical(node), mtime=0))
        document["node_sha256"] = control.identity(node)
        document["compressed_sha256"][str(path.relative_to(tmp_path))] = hashlib.sha256(
            path.read_bytes()
        ).hexdigest()
        receipt["custody"]["parent_replay"]["node_sha256"] = document["node_sha256"]
        receipt["custody"]["parent_replay"]["compressed_object_sha256"] = document[
            "compressed_sha256"
        ]
        receipt["custody"]["fresh_replay"]["receipt"]["node_sha256"] = document["node_sha256"]
    path = tmp_path / "h290.json"
    path.write_text(json.dumps(receipt))
    document["h290_receipt_sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()


@pytest.mark.parametrize("used", ["unused", "label1", "owner0"])
def test_large_opaque_parent_coordinates_vs_used_arithmetic_ceiling(
    used: str,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    document, _path = fixture(tmp_path)
    monkeypatch.setattr(control, "REPO", tmp_path)
    giant = "9" * 1381 + "/" + "8" * 1380
    receipt = json.loads((tmp_path / "h290.json").read_text())
    node = json.loads(
        gzip.decompress((tmp_path / "objects/node-synthetic.json.gz").read_bytes())
    )
    pose = 0 if used == "label1" else 15
    receipt["custody"]["input_control"]["endpoint_roster"][pose]["centre"][1] = [giant, giant]
    owner = "0" if used == "owner0" else "1"
    node["final_state"]["cells"][owner][0]["residual_polygons"] = [[[giant, "1"]]]
    node["final_state"]["groups"][owner] = [[giant, "1"]]
    rebind_synthetic_parent(document, tmp_path, receipt, node)
    if used != "unused":
        with pytest.raises(control.IncompleteError, match="rational string ceiling"):
            control.generate(document, deadline=time.monotonic() + 10)
    else:
        original = control.rational

        def guard(value: Any) -> Q:
            assert value != giant, "opaque parent rational entered arithmetic"
            return original(value)

        monkeypatch.setattr(control, "rational", guard)
        certificate = control.generate(document, deadline=time.monotonic() + 10)
        assert certificate["status"] == "unconditional_refresh_candidate"
        assert giant not in control.retained_json.dumps(certificate)
        assert len(certificate["custody"]["endpoint_retention"]["owners"]) == 17
        reference = certificate["custody"]["accepted_parent_premises"][
            "other_owner_final_geometry"
        ]
        assert reference["node_sha256"] == document["node_sha256"]
        assert reference["saved_node"] == "objects/node-synthetic.json.gz"
        assert control.check(document, certificate, deadline=time.monotonic() + 10)[
            "finite_reconstruction_verified"
        ]


@pytest.mark.parametrize(
    "change", ["witness_roster", "steps", "owner_keys", "row_count", "row_reference"]
)
def test_opaque_geometry_still_requires_full_structural_custody(
    change: str,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    document, _path = fixture(tmp_path)
    monkeypatch.setattr(control, "REPO", tmp_path)
    receipt = json.loads((tmp_path / "h290.json").read_text())
    node = json.loads(
        gzip.decompress((tmp_path / "objects/node-synthetic.json.gz").read_bytes())
    )
    if change == "witness_roster":
        receipt["custody"]["endpoint_retention"]["owners"].pop()
    elif change == "steps":
        receipt["custody"]["parent_replay"]["steps_checked"] = 15
    elif change == "owner_keys":
        node["final_state"]["cells"].pop("1")
    elif change == "row_count":
        node["final_state"]["cells"]["1"].pop()
    else:
        node["final_state"]["cells"]["1"][0]["reference"] = "untyped"
    rebind_synthetic_parent(document, tmp_path, receipt, node)
    with pytest.raises(ValueError, match=r"differ|premise"):
        control.generate(document, deadline=time.monotonic() + 10)


@pytest.mark.parametrize("where", ["unused_centre", "unused_polygon"])
def test_opaque_parent_scalar_grammar_refuses_exponent_without_arithmetic(
    where: str,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    document, _path = fixture(tmp_path)
    monkeypatch.setattr(control, "REPO", tmp_path)
    receipt = json.loads((tmp_path / "h290.json").read_text())
    node = json.loads(
        gzip.decompress((tmp_path / "objects/node-synthetic.json.gz").read_bytes())
    )
    if where == "unused_centre":
        receipt["custody"]["input_control"]["endpoint_roster"][15]["centre"][1][0] = (
            "1e999999999"
        )
    else:
        node["final_state"]["cells"]["1"][0]["residual_polygons"] = [[["1e999999999", "1"]]]
    rebind_synthetic_parent(document, tmp_path, receipt, node)
    with pytest.raises(ValueError, match="grammar required"):
        control.generate(document, deadline=time.monotonic() + 10)
