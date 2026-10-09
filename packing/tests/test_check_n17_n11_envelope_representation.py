"""Synthetic isolated-cell representation controls; no actual95 geometry."""

from __future__ import annotations

import copy
import hashlib
import json
import os
import subprocess
import sys
import time
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import pytest

from devtools import check_n17_n11_envelope_representation as tool

NAMES = [f"synthetic-{i}" for i in range(24)]
MASK = (1 << 17) - 1


def child_environment() -> dict[str, str]:
    """Import the selected checkout in a fresh process, preserving caller settings."""
    project = Path(__file__).resolve().parents[1]
    return os.environ | {"PYTHONPATH": os.pathsep.join((str(project / "src"), str(project)))}


def deadline() -> float:
    return time.monotonic() + 60


def boxes(kind: str = "kill") -> list[tool.Box]:
    edge = tool.U - Q(1, 2)
    corners = [(Q(1, 2), Q(1, 2)), (edge, Q(1, 2)), (Q(1, 2), edge), (edge, edge)]
    if kind == "kill":
        points = [c for c in corners for _ in range(6)]
    elif kind == "positive":
        points = [(Q(2), Q(2))] * 11 + [corners[i % 4] for i in range(13)]
    else:
        points = [(Q(1) if i % 2 == 0 else Q(31, 8), Q(2)) for i in range(24)]
    return [(x, x, y, y) for x, y in points]


def synthetic_roster() -> list[dict[str, Any]]:
    # Repeated masks are only this injected synthetic premise, never actual intake.
    return [{"mask": MASK, "cells": NAMES[:17], "orbit_size": 1} for _ in range(95)]


def endpoint(kind: str) -> int:
    return sum(1 << i for i in range(7, 24)) if kind == "positive" else MASK


@pytest.mark.parametrize(
    ("kind", "status"),
    [
        ("kill", "independent_aabb_architecture_killed"),
        ("positive", "ordinary_assignment_obstructions"),
        ("mixed", "criterion_missed"),
    ],
)
def test_complete109440_and_distinct_primary_scopes(kind: str, status: str) -> None:
    result = tool.construct(
        boxes(kind), NAMES, synthetic_roster(), endpoint(kind), deadline=deadline()
    )
    assert result["status"] == status
    assert result["state_window_counts_accounted"] == 109440
    assert len(result["states"]) == 95
    assert len(result["upper_window_roster"]) == len(result["lower_window_roster"]) == 576
    assert result["ordinary_assignment_exclusion_proved"] is (kind == "positive")
    assert result["independent_whole_cell_aabb_architecture_killed"] is (kind == "kill")
    assert result["criterion_met"] is (kind != "mixed")
    assert result["endpoint_upper_window_counts_accounted"] == 576
    assert result["endpoint_upper_calibration"]["maximum_full_envelope_count"] <= 10
    assert result["global_bound_proved"] is False
    assert result["census_admission_proved"] is False
    assert result["lower_envelope_physical_packing_proved"] is False
    for row in result["states"]:
        assert row["lower"]["ordinary_assignment_exclusion_proved"] is False
        assert (
            row["lower"]["maximum_full_envelope_count"]
            >= row["upper"]["maximum_full_envelope_count"]
        )


def test_exact_sandwich_and_wall_coupling_sharpens_old_box() -> None:
    upper, lower = tool.representations(boxes(), deadline())
    old = tool.old.envelopes(boxes(), deadline())
    assert upper[0] == lower[0] == (Q(0), Q(1), Q(0), Q(1))
    assert old[0][1] > upper[0][1]
    for u, lower_box, e in zip(upper, lower, old, strict=True):
        assert all(e[i] <= u[i] <= lower_box[i] for i in (0, 2))
        assert all(lower_box[i] <= u[i] <= e[i] for i in (1, 3))


def test_lower_is_optimistic_not_an_all_angle_enclosure() -> None:
    source = [(Q(2), Q(2), Q(2), Q(2))] * 24
    upper, lower = tool.representations(source, deadline())
    assert lower[0][1] == Q(5, 2)
    c, s = tool.finite.trig(Q(53, 128))
    extent = (c + s) / 2
    assert Q(2) + extent > lower[0][1]
    assert Q(2) + extent <= upper[0][1]


@pytest.mark.parametrize("axis", [0, 1])
def test_full_wall_coupled_enclosure_of_feasible_rational_rotations(axis: int) -> None:
    source = [(Q(3, 4), Q(1), Q(2), Q(9, 4))] * 24
    upper, _ = tool.representations(source, deadline())
    for t in (Q(0), Q(1, 5), Q(53, 128), Q(1)):
        c, s = tool.finite.trig(t)
        radius = (c + s) / 2
        for x in (Q(3, 4), Q(1)):
            for y in (Q(2), Q(9, 4)):
                if radius <= min(x, tool.U - x, y, tool.U - y):
                    centre = (x, y)[axis]
                    assert upper[0][2 * axis] <= centre - radius
                    assert centre + radius <= upper[0][2 * axis + 1]


@pytest.mark.parametrize(
    "bad",
    [
        (Q(0), Q(1), Q(1), Q(1)),
        (Q(1), tool.U, Q(1), Q(1)),
        (Q(2), Q(1), Q(1), Q(1)),
        (Q(1), Q(1), Q(0), Q(1)),
    ],
)
def test_necessary_wall_bounds_refuse(bad: tool.Box) -> None:
    with pytest.raises(ValueError, match="wall bounds"):
        tool.representations([bad] * 24, deadline())


def test_endpoint_upper_positive_refuses() -> None:
    with pytest.raises(ValueError, match="endpoint"):
        tool.construct(boxes("positive"), NAMES, synthetic_roster(), MASK, deadline=deadline())


def test_lower_equality_and_catalogue_aliases() -> None:
    _, lower = tool.representations(boxes("mixed"), deadline())
    windows = tool.old.window_roster(lower, NAMES, deadline())
    result = tool.lower_scan(MASK, windows, NAMES, deadline())
    assert result["maximum_full_envelope_count"] == 17
    assert result["nonproof_window_witness"]["anchor_indices"] == [0, 0]
    assert result["nonproof_window_witness"]["cell_indices"] == list(range(11))
    assert windows[0]["window"] == windows[1]["window"]
    assert windows[0]["anchor_indices"] != windows[1]["anchor_indices"]


def fixture(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> dict[str, Any]:
    prior = {
        "schema": tool.old.SCHEMA,
        "status": "criterion_missed",
        "criterion_met": False,
        "states_accounted": 95,
        "windows_per_state": 576,
        "state_window_counts_accounted": 54720,
        "obstructed_masks": [],
        "states": [
            {
                "mask": MASK,
                "ordinary_assignment_obstruction": False,
                "windows_accounted": 576,
                "window_counts": [0] * 576,
                "maximum_full_envelope_count": 0,
                "witness": None,
            }
            for _ in range(95)
        ],
        **tool.old.scope(),
    }
    partition = {
        "orbits": [{"mask": MASK, "cells": NAMES[:17], "orbit_size": 1, "distance": 0}]
    }
    part_path = tmp_path / "partition.json"
    part_path.write_text(json.dumps(partition))
    descriptor = {"partition": str(part_path), "d4": {"identity": list(range(24))}}
    prior["accepted_inputs"] = descriptor
    values = {
        "prior_descriptor": descriptor,
        "prior_certificate": prior,
        "prior_replay": prior | {"verification_passed": True},
    }
    doc: dict[str, Any] = {"schema": tool.CONTEXT_SCHEMA}
    for role, value in values.items():
        path = tmp_path / (role + ".json")
        raw = json.dumps(value).encode()
        path.write_bytes(raw)
        doc[role] = str(path)
        doc[role + "_sha256"] = hashlib.sha256(raw).hexdigest()
    monkeypatch.setattr(
        tool.old,
        "intake",
        lambda *_a: (boxes(), NAMES, synthetic_roster(), {part_path: part_path.read_bytes()}),
    )
    return doc


def test_generate_complete_fresh_payload_and_inherited_scope(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    doc = fixture(tmp_path, monkeypatch)
    generated = tool.generate(doc, deadline=deadline())
    fresh = tool.check(doc, generated, deadline=deadline())
    assert fresh["verification_passed"] is True
    assert tool.payload(fresh) == tool.payload(generated)
    assert generated["assurance"]["accepted304_proof_inherited"] is True
    assert generated["assurance"]["old_windows_replayed"] is False
    assert generated["assurance"]["n11_T061_proof_replayed"] is False
    forged = copy.deepcopy(generated)
    forged["states"][0]["lower"]["window_counts"][0] += 1
    with pytest.raises(ValueError, match="reconstruction"):
        tool.check(doc, forged, deadline=deadline())


@pytest.mark.parametrize(
    "kind", ["status", "verified", "roster", "scope", "counts", "identity"]
)
def test_prior_custody_or_accepted_negative_tamper_refuses(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, kind: str
) -> None:
    doc = fixture(tmp_path, monkeypatch)
    role = "prior_replay" if kind == "verified" else "prior_certificate"
    path = Path(doc[role])
    value = json.loads(path.read_text())
    if kind == "status":
        value["status"] = "ordinary_assignment_obstructions"
    elif kind == "verified":
        value["verification_passed"] = False
    elif kind == "roster":
        value["states"].pop()
    elif kind == "scope":
        value["global_bound_proved"] = True
    elif kind == "counts":
        value["states"][0]["window_counts"][0] = 11
    else:
        value["accepted_inputs"]["partition"] = "different.json"
    raw = json.dumps(value).encode()
    path.write_bytes(raw)
    doc[role + "_sha256"] = hashlib.sha256(raw).hexdigest()
    with pytest.raises(ValueError, match=r"premise|roster"):
        tool.intake(doc, deadline())


def test_descriptor_extra_and_byte_mismatch_refuse(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    doc = fixture(tmp_path, monkeypatch)
    with pytest.raises(ValueError, match="descriptor"):
        tool.intake(doc | {"extra": 1}, deadline())
    doc["prior_certificate_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="bytes"):
        tool.intake(doc, deadline())


def test_afterhash_mutation_refuses(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    doc = fixture(tmp_path, monkeypatch)
    original = tool.construct

    def changed(*args: Any, **kwargs: Any) -> dict[str, Any]:
        result = original(*args, **kwargs)
        Path(doc["prior_replay"]).write_text("{}")
        return result

    monkeypatch.setattr(tool, "construct", changed)
    with pytest.raises(ValueError, match="bytes changed"):
        tool.generate(doc, deadline=deadline())


@pytest.mark.parametrize("kind", ["typed_row", "bad_count"])
def test_both_accepted_payloads_tampered_still_refuse(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, kind: str
) -> None:
    doc = fixture(tmp_path, monkeypatch)
    for role in ("prior_certificate", "prior_replay"):
        path = Path(doc[role])
        value = json.loads(path.read_text())
        if kind == "typed_row":
            value["states"][0] = []
        else:
            value["states"][0]["window_counts"][0] = 11
            value["states"][0]["maximum_full_envelope_count"] = 11
        raw = json.dumps(value).encode()
        path.write_bytes(raw)
        doc[role + "_sha256"] = hashlib.sha256(raw).hexdigest()
    with pytest.raises(ValueError, match="roster"):
        tool.intake(doc, deadline())


def test_role_list_typed_refusal(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    doc = fixture(tmp_path, monkeypatch)
    path = Path(doc["prior_replay"])
    raw = b"[]"
    path.write_bytes(raw)
    doc["prior_replay_sha256"] = hashlib.sha256(raw).hexdigest()
    with pytest.raises(ValueError, match=r"typed|object"):
        tool.intake(doc, deadline())


def test_monotonic_count_assertion_refuses_faulty_lower_scan(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    original = tool.lower_scan

    def inconsistent(*args: Any) -> dict[str, Any]:
        value = original(*args)
        value["maximum_full_envelope_count"] = -1
        return value

    monkeypatch.setattr(tool, "lower_scan", inconsistent)
    with pytest.raises(ValueError, match="lower count"):
        tool.construct(boxes(), NAMES, synthetic_roster(), MASK, deadline=deadline())


def test_limits_deadline_and_all_failure_flags_false() -> None:
    with pytest.raises(tool.finite.IncompleteError, match="wall"):
        tool.representations(boxes(), time.monotonic() - 1)
    value = Q(1 << 4097)
    with pytest.raises(tool.finite.IncompleteError, match="bit"):
        tool.representations([(value, value, Q(1), Q(1))] * 24, deadline())
    for exc in (ValueError("malformed"), tool.finite.IncompleteError("wall")):
        failed = tool.failure(exc)
        assert all(failed[k] is False for k in tool.scope())
        assert failed["criterion_met"] is False


def test_clean_two_processes_explicit_synthetic_inherited_premise(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    doc = fixture(tmp_path, monkeypatch)
    descriptor = tmp_path / "descriptor.json"
    descriptor.write_text(json.dumps(doc))
    runner = tmp_path / "runner.py"
    runner.write_text(
        "import sys\nfrom pathlib import Path\n"
        "from devtools import check_n17_n11_envelope_representation as t\n"
        f"sys.path.insert(0,{str(Path(__file__).parent)!r})\n"
        "from test_check_n17_n11_envelope_representation import boxes,NAMES,synthetic_roster\n"
        "p=Path(sys.argv[1])\n"
        "t.old.intake=lambda *_a:(boxes(),NAMES,synthetic_roster(),{p:p.read_bytes()})\n"
        "raise SystemExit(t.main(sys.argv[2:]))\n"
    )
    generated, replay = tmp_path / "generated.json", tmp_path / "replay.json"
    for tail in (
        ["--output", str(generated)],
        ["--certificate", str(generated), "--output", str(replay)],
    ):
        run = subprocess.run(
            [
                sys.executable,
                str(runner),
                str(tmp_path / "partition.json"),
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
    cert, fresh = json.loads(generated.read_text()), json.loads(replay.read_text())
    assert fresh["verification_passed"] is True
    assert tool.payload(cert) == tool.payload(fresh)
