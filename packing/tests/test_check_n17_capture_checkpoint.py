"""Target-free numeric-cap input custody, wall, resource and CLI controls."""

from __future__ import annotations

import copy
import json
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
from sqpack.hull_kernel.rational import Q


def context() -> dict[str, Any]:
    names = tuple("side-S2" if i == 5 else f"synthetic-{i + 1}" for i in range(17))
    centres = tuple((Q(1) + Q(i, 50), Q(1)) for i in range(17))
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
        (SymmetryAction("r0", (1, 0, 0, 1), tuple(range(17))),),
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
        for i, (x, y) in enumerate(centres)
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
