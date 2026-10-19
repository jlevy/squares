"""Target-free numeric-cap input custody, wall, resource and CLI controls."""

from __future__ import annotations

import copy
import gzip
import json
import subprocess
import sys
import time
from dataclasses import replace
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools import check_n17_capture_checkpoint as control
from devtools import check_n17_endpoint_prefix as prefix
from devtools import pilot_n17_capture as pilot
from sqpack.hull_kernel.frame import Frame, SymmetryAction
from sqpack.hull_kernel.induction import common_core_planes
from sqpack.hull_kernel.rational import Q


def context(*, world: int = 17) -> dict[str, Any]:
    names = tuple("side-S2" if i == 5 else f"synthetic-{i + 1}" for i in range(world))
    centres = tuple((Q(1) + Q(i, 50), Q(1)) for i in range(world))
    cells = tuple(
        tuple(
            (x + a, y + b)
            for a, b in (
                (Q(-1, 100), Q(-1, 100)),
                (Q(1, 100), Q(-1, 100)),
                (Q(1, 100), Q(1, 100)),
                (Q(-1, 100), Q(1, 100)),
            )
        )
        for x, y in centres
    )
    base = Frame(
        "synthetic",
        control.OUTER,
        control.OUTER,
        cells,
        names,
        17,
        (SymmetryAction("r0", (1, 0, 0, 1), tuple(range(world))),),
    )
    numeric = replace(base, name="synthetic-capture", capture_cap=control.CAP)
    root = {
        "root_inclusion_box_used": [["1/3", "1/3"], ["1/4", "1/4"]],
        "root_verification_passed": True,
    }
    targets = tuple(
        pilot.Target(
            i + 1,
            i,
            names[i],
            (pilot.Box.point(Fraction(str(x))), pilot.Box.point(Fraction(str(y)))),
            ((Q(0), Q(0)),),
            0.0,
        )
        for i, (x, y) in enumerate(centres[:17])
    )
    endpoint = pilot.Endpoint(
        targets,
        pilot.Box.point(Fraction(str(control.CAP)) - Fraction(1, 2 * 10**12)),
        control.CAP,
        (1.0, 0.0),
        (0.0, 1.0),
        {"t_box": ["1/3", "1/3"], "b_box": ["1/4", "1/4"]},
        slides={},
    )
    poses = tuple(prefix.EndpointPose(t.label, t.owner, t.centre, t.charts) for t in targets)
    return {
        "root": root,
        "root_box": {"midpoint": ["1/3", "1/4"], "inclusion_bounds": ["1/100", "1/100"]},
        "cap_check": {"verification_passed": True, "cap_certified": True},
        "base": base,
        "numeric": numeric,
        "endpoint": endpoint,
        "poses": poses,
        "endpoint_inputs": {"root": copy.deepcopy(root)},
        "source_bytes": {"root": "synthetic", "geometry": "synthetic"},
    }


def packet(value: dict[str, Any]) -> dict[str, Any]:
    return control.input_packet(value, deadline=time.monotonic() + 10)


def saved_fixture(tmp_path: Path) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    """Unchanged empty-hull restrictions, not a feasible17-square packing."""
    value = context(world=24)
    frame = value["numeric"]
    groups = {str(i): [] for i in range(17)}
    cells = {}
    for owner in range(17):
        polygon = [[str(x), str(y)] for x, y in frame.world(owner)]
        cells[str(owner)] = [
            {
                "interval": [str(Q(i, 32)), str(Q(i + 1, 32))],
                "reference": {"kind": "wall_seed", "owner": owner, "row": i},
                "outer_domain": copy.deepcopy(polygon),
                "outer_bounds": [],
                "residual_polygons": [copy.deepcopy(polygon)],
            }
            for i in range(32)
        ]
    seed = {
        "schema": "generic_wall_seed_v1",
        "mask_index": None,
        "mask": list(range(17)),
        "U": str(frame.cap),
        "B": "1",
        "bins": 32,
        "groups": copy.deepcopy(groups),
        "cells": copy.deepcopy(cells),
        "world": [[[str(x), str(y)] for x, y in frame.world(owner)] for owner in range(24)],
    }
    core = [
        (Q(-1, 10), Q(-1, 10)),
        (Q(1, 10), Q(-1, 10)),
        (Q(1, 10), Q(1, 10)),
        (Q(-1, 10), Q(1, 10)),
    ]
    steps, owners = [], [i for i in range(17) if i != 5]
    for index, owner in enumerate(owners):
        vertices = frame.world(owner)
        planes = common_core_planes(core, vertices)
        rows = []
        for row_index, prior in enumerate(cells[str(owner)]):
            row = {
                **copy.deepcopy(prior),
                "prior_reference": prior["reference"],
                "reference": {
                    "kind": "phase3",
                    "node": "synthetic-noop",
                    "step": index,
                    "row": row_index,
                },
                "input_domain": copy.deepcopy(prior["outer_domain"]),
                "core_vertices": [[str(x), str(y)] for x, y in core],
                "collision_regions": [],
                "self_hull_cuts": [],
                "common_core_halfplanes": [
                    {"normal": [str(a), str(b)], "upper": str(c)} for a, b, c in planes
                ],
            }
            rows.append(row)
        steps.append(
            {
                "index": index,
                "owner": owner,
                "complete": True,
                "allowed_half_angle": ["0", "1"],
                "prior_owned_hulls": copy.deepcopy(groups),
                "prior_partner_pose_covers": {},
                "rows": rows,
                "common_owned_kernel": [],
            }
        )
        cells[str(owner)] = [
            {
                k: copy.deepcopy(r[k])
                for k in ("interval", "reference", "outer_domain", "residual_polygons")
            }
            for r in rows
        ]
    saved = control.import_module("devtools.check_n17_subpattern")
    node = {
        "schema": "exact_generic_owned_hull_v1",
        "node_id": "synthetic-noop",
        "U": str(frame.cap),
        "B": "1",
        "mask_index": None,
        "mask": list(range(17)),
        "parent": None,
        "guard_source": None,
        "constraints": [],
        "source": {"sha256": saved.content_sha256(seed)},
        "initial": {
            "groups": copy.deepcopy(groups),
            "cell_references": {
                str(i): [row["reference"] for row in seed["cells"][str(i)]] for i in range(17)
            },
        },
        "steps": steps,
        "final_state": {
            "groups": groups,
            "cells": cells,
            "mask_index": None,
            "mask": list(range(17)),
            "U": str(frame.cap),
            "B": "1",
            "constraints": [],
            "guard": {},
            "guard_source": None,
            "source": {"sha256": saved.content_sha256(seed)},
            "world": copy.deepcopy(seed["world"]),
        },
        "contradiction": None,
        "closed": False,
        "terminal": False,
        "mask_exclusion_proved": False,
        "global_optimality_proved": False,
    }
    directory = tmp_path / "objects"
    directory.mkdir()
    for kind, obj in (("seed", seed), ("node", node)):
        (directory / f"{kind}-synthetic.json.gz").write_bytes(
            gzip.compress(saved.canonical_bytes(obj), mtime=0)
        )
    document = {
        "schema": control.CHECKPOINT_SCHEMA,
        "action": "r0",
        "saved_objects": "objects",
        "frame": control.frame_record(frame),
        "state": list(range(17)),
        "label_to_owner": {str(i + 1): i for i in range(17)},
        "step_owners": owners,
        "seed_sha256": saved.content_sha256(seed),
        "node_sha256": saved.content_sha256(node),
    }
    return document, seed, node


def test_exact_synthetic16_step_saved_replay(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(control.exact, "REPO", tmp_path)
    document, _seed, _node = saved_fixture(tmp_path)
    trace, receipt = control.saved_replay(
        document, control.read_frame(document["frame"]), deadline=time.monotonic() + 20
    )
    assert len(trace.steps) == 16
    assert receipt["actual_seed_rows_checked"] == 544
    assert receipt["closure"] is None
    assert receipt["root_cap_independently_checked"] is False
    assert control.exact.exact_structure(receipt["frame"], document["frame"])


def test_actual_clean_child_cli_does_not_import_producer(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(control.exact, "REPO", tmp_path)
    document, _seed, _node = saved_fixture(tmp_path)
    descriptor, output = tmp_path / "descriptor.json", tmp_path / "child.json"
    descriptor.write_text(json.dumps(document))
    script = """
import sys
from pathlib import Path
from devtools import check_n17_capture_checkpoint as control
assert 'sqpack.hull_kernel.producer' not in sys.modules
control.exact.REPO = Path(sys.argv[1])
raise SystemExit(control.main(sys.argv[2:]))
"""
    process = subprocess.run(
        [
            sys.executable,
            "-c",
            script,
            str(tmp_path),
            "--fresh-saved",
            str(descriptor),
            "--max-seconds",
            "20",
            "--output",
            str(output),
        ],
        capture_output=True,
        text=True,
        timeout=25,
        check=False,
    )
    assert process.returncode == 0, process.stderr
    receipt = json.loads(output.read_text())
    assert receipt["producer_imported"] is False
    assert receipt["steps_checked"] == 16
    assert receipt["frame"] == document["frame"]
    assert receipt["global_admission_proved"] is False


def phase_fixture(tmp_path: Path, document: dict[str, Any]) -> dict[str, Any]:
    value = context(world=24)
    checked = packet(value)
    settings = {
        "box": None,
        "max_rounds": 1,
        "bins": 32,
        "max_live": 64,
        "min_width": "1/4194304",
        "hull_limit": 48,
        "core": "octagon",
        "seed_grid": 0,
        "replay_share": 0,
    }
    production = {
        "status": "PASS_PILOT_MEASURED",
        "system": "n17",
        "cap": "capture",
        "inner_cap": str(control.CAP),
        "U": str(control.OUTER),
        "frame": value["numeric"].name,
        "seed_sha256": document["seed_sha256"],
        "node_sha256": document["node_sha256"],
        "endpoint_control": {"held": True, "checked_after": 17},
        "closure": None,
        "refusal": None,
        "settings": settings,
        "resumed": None,
        "endpoint": value["endpoint"].provenance,
        "owners": [
            {"label": t.label, "owner": t.owner, "cell": t.cell, "coarse": t.label == 6}
            for t in value["endpoint"].targets
        ],
        "rounds": [{"round": 1, "complete": True}],
        "updates": [
            {"round": 1, "step": i, "label": o + 1}
            for i, o in enumerate(document["step_owners"])
        ],
    }
    fresh = copy.deepcopy(production)
    fresh["resumed"] = {"round": 1, "changed_since": []}
    fresh["settings"]["replay_share"] = 0.5
    fresh["replay"] = {"status": "PASS_REPLAYED", "steps": 16, "final_state_agrees": True}
    for name, obj in (("production", production), ("fresh", fresh), ("input", checked)):
        (tmp_path / f"{name}.json").write_text(json.dumps(obj))
    document.update(
        root_path="root.json",
        cap_certificate="cap.json",
        geometry="geometry.json",
        root=copy.deepcopy(value["root"]),
        input_control="input.json",
        production_receipt="production.json",
        fresh_replay_receipt="fresh.json",
        original_container_premise="centred-C(S*)",
        composition_premise="docs/project/reviews/review-2026-10-02-n17-local-half-composition.md",
    )
    return value


@pytest.mark.parametrize(
    "mutation",
    ["step_order", "seed_id", "frame_name", "resumed_production", "endpoint", "input"],
)
def test_h289_phase_receipt_mutations_refuse(
    mutation: str,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(control.exact, "REPO", tmp_path)
    document, _seed, _node = saved_fixture(tmp_path)
    value = phase_fixture(tmp_path, document)
    name = "input" if mutation == "input" else "production"
    path = tmp_path / f"{name}.json"
    receipt = json.loads(path.read_text())
    if mutation == "step_order":
        receipt["updates"].reverse()
    elif mutation == "seed_id":
        receipt["seed_sha256"] = "stale"
    elif mutation == "frame_name":
        receipt["frame"] = "old-none-frame"
    elif mutation == "resumed_production":
        receipt["resumed"] = {"round": 0}
    elif mutation == "endpoint":
        receipt["owners"][0]["owner"] = 1
    else:
        receipt["root"]["root_verification_passed"] = False
    path.write_text(json.dumps(receipt))
    with pytest.raises(ValueError, match=r"receipt differs|custody differs|replay differs"):
        control.phase_receipts(document, packet(value))


@pytest.mark.parametrize("mutation", ["seed", "node", "order", "coarse", "guard"])
def test_saved_identity_order_or_guard_mutation_refuses(
    mutation: str,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(control.exact, "REPO", tmp_path)
    document, _seed, node = saved_fixture(tmp_path)
    if mutation in {"seed", "node"}:
        document[f"{mutation}_sha256"] = "stale"
    elif mutation == "order":
        document["step_owners"].reverse()
    elif mutation == "coarse":
        document["step_owners"][-1] = 5
    else:
        node["guard_source"] = "unsupported"
        saved = control.import_module("devtools.check_n17_subpattern")
        (tmp_path / "objects/node-synthetic.json.gz").write_bytes(
            gzip.compress(saved.canonical_bytes(node))
        )
    with pytest.raises(ValueError, match=r"identity differs|order|roster differs|guard"):
        control.saved_replay(
            document, control.read_frame(document["frame"]), deadline=time.monotonic() + 20
        )


def test_gzip_decoded_cap_and_truncation(tmp_path: Path) -> None:
    path = tmp_path / "object.gz"
    path.write_bytes(gzip.compress(b"x" * 100))
    with pytest.raises(control.IncompleteError, match="byte ceiling"):
        control.bounded_gzip(path, 99, deadline=time.monotonic() + 5)
    path.write_bytes(path.read_bytes()[:-4])
    with pytest.raises(EOFError):
        control.bounded_gzip(path, 100, deadline=time.monotonic() + 5)


@pytest.mark.parametrize(
    "outcome", ["ready", "zero_interval", "child_identity", "expired", "lost_endpoint"]
)
def test_consumer_wires_complete_replay_and_all49_conditional_bounds(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    outcome: str,
) -> None:
    # Mock only scientific context/child launch; actual kernel replay and leaf geometry
    # run on a synthetic24-cell restriction. This is not a geometric n17 control.
    monkeypatch.setattr(control.exact, "REPO", tmp_path)
    document, _seed, _node = saved_fixture(tmp_path)
    value = phase_fixture(tmp_path, document)
    descriptor = tmp_path / "descriptor.json"
    descriptor.write_text(json.dumps(document))
    monkeypatch.setattr(control, "load_context", lambda *_: value)
    cap, _prefix, _pilot = control.scientific_modules()
    side = Fraction(str(control.CAP)) - Fraction(1, 2 * 10**12)
    sigma = (Fraction(str(control.OUTER)) - side) / 2
    centres = {
        t.label: (
            control.exact.point(Fraction(str(t.centre[0].lo)) - sigma),
            control.exact.point(Fraction(str(t.centre[1].lo)) - sigma),
        )
        for t in value["endpoint"].targets
    }
    ex, ey = (
        (control.exact.point(1), control.exact.point(0)),
        (control.exact.point(0), control.exact.point(1)),
    )
    layout = control.exact.Layout(
        centres,
        {"u": ex, "v": ey, "p": ex, "q": ey, "ex": ex, "ey": ey},
        {},
        {},
        control.exact.point(side),
    )
    monkeypatch.setattr(
        cap.root_loader, "load_root", lambda *_: (value["root"], layout, layout)
    )
    child_leases = []

    def child(_path: Path, *, seconds: float, limits: dict[str, int]) -> dict[str, Any]:
        child_leases.append(seconds)
        _trace, receipt = control.saved_replay(
            document, value["numeric"], deadline=time.monotonic() + 20, limits=limits
        )
        receipt["producer_imported"] = False
        if outcome == "child_identity":
            receipt["frame"]["U"] = "5"
        return {"receipt": receipt}

    monkeypatch.setattr(control, "fresh_child", child)
    if outcome == "zero_interval":
        consumer = control.import_module("devtools.check_n17_capture_leaf")
        original_bounds = consumer.bounds

        def exclude_zero(*args: Any, **kwargs: Any) -> dict[str, Any]:
            result = original_bounds(*args, **kwargs)
            result["intervals"][next(iter(result["intervals"]))] = ["1", "2"]
            return result

        monkeypatch.setattr(consumer, "bounds", exclude_zero)
    elif outcome == "lost_endpoint":
        monkeypatch.setattr(_prefix, "endpoint_check", lambda *_: {"held": False})
    deadline = time.monotonic() + 20
    if outcome == "expired":
        replay = control.saved_replay

        def expire(*args: Any, **kwargs: Any) -> Any:
            result = replay(*args, **kwargs)
            monkeypatch.setattr(control.time, "monotonic", lambda: deadline + 1)
            return result

        monkeypatch.setattr(control, "saved_replay", expire)
        with pytest.raises(control.IncompleteError, match="before fresh"):
            control.consume_checkpoint(
                descriptor, deadline=deadline, child_seconds=300, limits=dict(control.LIMITS)
            )
        assert child_leases == []
        return
    if outcome != "ready":
        with pytest.raises(
            ValueError, match=r"full-frame replay|zero-containing|endpoint lost"
        ):
            control.consume_checkpoint(
                descriptor, deadline=deadline, child_seconds=300, limits=dict(control.LIMITS)
            )
        return
    result = control.consume_checkpoint(
        descriptor,
        deadline=deadline,
        child_seconds=300,
        limits=dict(control.LIMITS),
    )
    assert result["readiness_passed"] is True
    assert result["status"] == "unresolved"
    assert len(result["intervals"]) == 49
    assert result["custody"]["endpoint_retention"]["held"] is True
    assert 0 < child_leases[0] < 20
    assert result["global_admission_proved"] is False
    assert result["census_admission_proved"] is False
    output = tmp_path / "parent.json"
    assert (
        control.main(
            ["--checkpoint", str(descriptor), "--max-seconds", "20", "--output", str(output)]
        )
        == 0
    )
    assert control.exact.decode(output.read_bytes())["readiness_passed"] is True


@pytest.mark.parametrize("name", ["seed_bytes", "node_bytes", "decoded_node_bytes"])
def test_saved_byte_caps_are_incomplete(
    name: str,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(control.exact, "REPO", tmp_path)
    document, _seed, _node = saved_fixture(tmp_path)
    limits = {**control.LIMITS, name: 1}
    with pytest.raises(control.IncompleteError, match="byte ceiling"):
        control.saved_replay(
            document,
            control.read_frame(document["frame"]),
            deadline=time.monotonic() + 20,
            limits=limits,
        )


def test_node_stream_itself_enforces_decoded_ceiling(tmp_path: Path) -> None:
    document, _seed, _node = saved_fixture(tmp_path)
    saved = control.import_module("devtools.check_n17_subpattern")
    path = tmp_path / document["saved_objects"] / "node-synthetic.json.gz"
    size = len(
        control.bounded_gzip(
            path, control.NODE_DECODED_LIMIT, deadline=time.monotonic() + 5, retain=True
        )
    )
    with pytest.raises(control.IncompleteError, match="streaming decoded"):
        control.bounded_node(saved, path, size - 1, deadline=time.monotonic() + 5)


@pytest.mark.parametrize("failure", ["timeout", "incomplete"])
def test_fresh_child_resource_failure_stays_incomplete(
    failure: str,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def stopped(command: list[str], **_: Any) -> Any:
        if failure == "timeout":
            raise subprocess.TimeoutExpired(command, 1)
        Path(command[command.index("--output") + 1]).write_text('{"status":"incomplete"}')
        return subprocess.CompletedProcess(command, 1)

    monkeypatch.setattr(control.subprocess, "run", stopped)
    with pytest.raises(control.IncompleteError, match="fresh numeric replay"):
        control.fresh_child(
            tmp_path / "descriptor.json", seconds=1, limits=dict(control.LIMITS)
        )


@pytest.mark.parametrize("setting", ["--max-seconds", "--max-seed-bytes"])
def test_invalid_checkpoint_limit_cannot_load_inputs(
    setting: str,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        control, "consume_checkpoint", lambda *_a, **_k: pytest.fail("read input")
    )
    output = tmp_path / "refused.json"
    assert control.main(["--checkpoint", "unused", setting, "0", "--output", str(output)]) == 1
    assert control.exact.decode(output.read_bytes())["status"] == "refused"


def test_output_limit_preserves_incomplete_without_promotion(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        control,
        "consume_checkpoint",
        lambda *_a, **_k: {
            "readiness_passed": True,
            "status": "unresolved",
            "intervals": {"x": ["0", "1"]},
        },
    )
    output = tmp_path / "incomplete.json"
    assert (
        control.main(
            ["--checkpoint", "unused", "--max-output-bytes", "1", "--output", str(output)]
        )
        == 1
    )
    result = control.exact.decode(output.read_bytes())
    assert result["status"] == "incomplete"
    assert result["readiness_passed"] is False
    assert result["census_admission_proved"] is False


def mock_loader(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> tuple[Path, Path, Path, list[str]]:
    value = context()
    cap, _, pilot_module = control.scientific_modules()
    paths = tuple(tmp_path / name for name in ("root.json", "cap.json", "geometry.json"))
    root_path, cap_path, geometry_path = paths
    root_path.write_text(json.dumps({"box": {"midpoint": value["root_box"]["midpoint"]}}))
    cap_path.write_text(json.dumps({"inputs": value["root"]}))
    geometry_path.write_text(
        json.dumps({"criterion_passed": True, "geometry": {"box": value["root_box"]}})
    )
    (tmp_path / "polynomial.json").write_text("{}")
    monkeypatch.setattr(control.exact, "REPO", tmp_path)
    monkeypatch.setattr(cap.root_loader.root, "SOURCE_PATH", Path("polynomial.json"))
    monkeypatch.setattr(cap, "check", lambda *_: value["cap_check"])
    monkeypatch.setattr(
        cap.root_loader.root,
        "check",
        lambda *_: {
            "verification_passed": True,
            "inclusion_bounds": value["root_box"]["inclusion_bounds"],
        },
    )
    monkeypatch.setattr(pilot_module.cover, "CERTIFICATE", geometry_path)
    monkeypatch.setattr(
        pilot_module,
        "capture_frame",
        lambda inner: value["base"] if inner is None else value["numeric"],
    )
    loaded: list[str] = []

    def endpoint(_frame: Frame) -> pilot.Endpoint:
        loaded.append("pilot")
        return value["endpoint"]

    monkeypatch.setattr(pilot_module, "load_endpoint", endpoint)
    monkeypatch.setattr(
        prefix,
        "load_endpoint",
        lambda: (value["base"], value["poses"], value["endpoint_inputs"]),
    )
    return root_path, cap_path, geometry_path, loaded


def test_loader_joins_exact_geometry_box_before_pilot(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root_path, cap_path, geometry_path, loaded = mock_loader(tmp_path, monkeypatch)
    result = control.load_context(root_path, cap_path, geometry_path, time.monotonic() + 10)
    assert packet(result)["input_join_passed"] is True
    assert loaded == ["pilot"]
    document = json.loads(geometry_path.read_text())
    document["geometry"]["box"]["inclusion_bounds"][0] = "1/101"
    geometry_path.write_text(json.dumps(document))
    loaded.clear()
    with pytest.raises(ValueError, match="exact box binding"):
        control.load_context(root_path, cap_path, geometry_path, time.monotonic() + 10)
    assert loaded == []


def test_refused_cap_prevents_root_and_pilot_loading(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root_path, cap_path, geometry_path, loaded = mock_loader(tmp_path, monkeypatch)
    cap, _, _ = control.scientific_modules()
    monkeypatch.setattr(
        cap, "check", lambda *_: {"verification_passed": True, "cap_certified": False}
    )
    monkeypatch.setattr(
        cap.root_loader.root, "check", lambda *_: pytest.fail("refused cap read root")
    )
    with pytest.raises(ValueError, match="cap prerequisite"):
        control.load_context(root_path, cap_path, geometry_path, time.monotonic() + 10)
    assert loaded == []


def test_loader_refuses_changed_geometry_bytes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root_path, cap_path, geometry_path, _ = mock_loader(tmp_path, monkeypatch)
    _, _, pilot_module = control.scientific_modules()
    original = pilot_module.load_endpoint

    def changed(frame: Frame) -> pilot.Endpoint:
        value = original(frame)
        geometry_path.write_text(geometry_path.read_text() + " ")
        return value

    monkeypatch.setattr(pilot_module, "load_endpoint", changed)
    with pytest.raises(ValueError, match="changed across loading"):
        control.load_context(root_path, cap_path, geometry_path, time.monotonic() + 10)


def test_synthetic_full_roster_and_numeric_wall_coefficients() -> None:
    result = packet(context())
    assert result["input_join_passed"] is True
    assert len(result["endpoint_roster"]) == 17
    assert len(result["frame"]["row_prototypes"]) == 32
    assert all(result[name] is False for name in control.FALSE_FLAGS)
    assert result["frame"]["seed_generated"] is False


@pytest.mark.parametrize("field", ["capture_cap", "name", "cells", "actions", "length"])
def test_numeric_frame_mutation_refuses(field: str) -> None:
    value = context()
    changed = {
        "capture_cap": None,
        "name": "synthetic",
        "cells": value["base"].cells[:-1],
        "actions": (),
        "length": Q(5),
    }
    value["numeric"] = replace(value["numeric"], **{field: changed[field]})
    with pytest.raises(ValueError, match="numeric frame"):
        packet(value)


@pytest.mark.parametrize("field", ["capture_cap", "coarse", "system", "scale"])
def test_endpoint_frozen_scope_mutation_refuses(field: str) -> None:
    value = context()
    changed = {"capture_cap": control.OUTER, "coarse": None, "system": "n11", "scale": Q(2)}
    value["endpoint"] = replace(value["endpoint"], **{field: changed[field]})
    with pytest.raises(ValueError, match=r"cap differs|scope differs"):
        packet(value)


def test_root_custody_and_narrow_pilot_box_refuse() -> None:
    value = context()
    value["endpoint_inputs"]["root"]["root_verification_passed"] = False
    with pytest.raises(ValueError, match="root endpoint custody"):
        packet(value)
    value = context()
    value["endpoint"].provenance["t_box"] = ["1/2", "1/2"]
    with pytest.raises(ValueError, match="too narrow"):
        packet(value)


def test_side_lower_bound_and_full_root_pose_containment_refuse() -> None:
    value = context()
    value["endpoint"] = replace(
        value["endpoint"],
        side=pilot.Box(
            Fraction(str(control.CAP)) - Fraction(2, 10**12),
            Fraction(str(control.CAP)) - Fraction(1, 2 * 10**12),
        ),
    )
    with pytest.raises(ValueError, match="all-root excess"):
        packet(value)
    value = context()
    pose = value["poses"][0]
    value["poses"] = (
        replace(pose, centre=(pilot.Box.point(2), pose.centre[1])),
        *value["poses"][1:],
    )
    with pytest.raises(ValueError, match="full accepted-root pose"):
        packet(value)


@pytest.mark.parametrize("mutation", ["missing", "duplicate", "owner", "chart"])
def test_full17_endpoint_mapping_mutation_refuses(mutation: str) -> None:
    value = context()
    targets = value["endpoint"].targets
    if mutation == "missing":
        targets = targets[:-1]
    elif mutation == "duplicate":
        targets = (*targets[:-1], replace(targets[-1], label=1))
    elif mutation == "owner":
        targets = (replace(targets[0], owner=1), *targets[1:])
    else:
        targets = (replace(targets[0], charts=((Q(1), Q(1)),)), *targets[1:])
    value["endpoint"] = replace(value["endpoint"], targets=targets)
    with pytest.raises(ValueError, match=r"roster differs|full accepted-root pose"):
        packet(value)


def test_expired_control_stays_incomplete() -> None:
    with pytest.raises(control.IncompleteError):
        control.input_packet(context(), deadline=0)


def test_cli_roundtrip_and_incomplete_status(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(control, "load_context", lambda *_: context())
    output = tmp_path / "control.json"
    argv = ["--cap-certificate", str(tmp_path / "synthetic-cap.json"), "--output", str(output)]
    assert control.main(argv) == 0
    result = control.exact.decode(output.read_bytes())
    assert result["input_join_passed"] is True
    assert len(result["endpoint_roster"]) == 17
    monkeypatch.setattr(control.time, "monotonic", lambda: 0)

    def expired(*_: Any) -> dict[str, Any]:
        monkeypatch.setattr(control.time, "monotonic", lambda: 100)
        return context()

    monkeypatch.setattr(control, "load_context", expired)
    assert control.main(argv) == 1
    result = json.loads(output.read_text())
    assert result["status"] == "incomplete"
    assert result["input_join_passed"] is False


@pytest.mark.parametrize("limit", ["nan", "inf", "0", "-1"])
def test_cli_invalid_ceiling_reads_no_input(
    limit: str, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        control, "load_context", lambda *_: pytest.fail("invalid limit read input")
    )
    output = tmp_path / "refused.json"
    assert (
        control.main(
            ["--cap-certificate", "unused", "--max-seconds", limit, "--output", str(output)]
        )
        == 1
    )
    assert json.loads(output.read_text())["status"] == "refused"
