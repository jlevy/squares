"""Synthetic whole-envelope controls, without evaluating the actual95 states."""

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

from devtools import check_n17_n11_envelope_windows as tool


def deadline() -> float:
    return time.monotonic() + 60


def boxes(*, positive: bool = True) -> list[tool.Box]:
    if positive:
        return [(Q(2), Q(2), Q(2), Q(2))] * 24
    return [(Q(0), tool.U, Q(0), tool.U)] * 24


NAMES = [f"cell-{i}" for i in range(24)]
MASK = (1 << 17) - 1


def test_radius_bounds_every_rotated_square_and_strict_n11_gap() -> None:
    assert 2 * tool.R**2 >= 1
    assert Q(31, 7999999992) == tool.B11 - tool.H
    for tau in (Q(0), Q(1, 3), Q(53, 128), Q(1)):
        c, s = (1 - tau * tau) / (1 + tau * tau), 2 * tau / (1 + tau * tau)
        assert (c + s) / 2 <= tool.R


@pytest.mark.parametrize("positive", [True, False])
def test_full576_counts_and_first_witness(positive: bool) -> None:  # noqa: FBT001
    rectangles = tool.envelopes(boxes(positive=positive), deadline())
    windows = tool.window_roster(rectangles, NAMES, deadline())
    result = tool.scan_state(MASK, windows, NAMES, deadline())
    assert result["windows_accounted"] == len(result["window_counts"]) == 576
    assert result["ordinary_assignment_obstruction"] is positive
    assert result["maximum_full_envelope_count"] == (17 if positive else 0)
    assert result["first_argmax_anchor_indices"] == [0, 0]
    if positive:
        assert result["witness"]["cell_indices"] == list(range(11))
        tool.verify_witness(MASK, rectangles, NAMES, result["witness"])


def test_centre_only_false_positive_rejected() -> None:
    assert tool.contained((Q(2), Q(2), Q(2), Q(2)), Q(0), Q(0))
    assert not tool.contained((Q(0), tool.U, Q(0), tool.U), Q(0), Q(0))


def test_closed_equality_and_window_outside_outer_container() -> None:
    start = Q(1, 4)
    rectangle = (start, start + tool.H, start, start + tool.H)
    assert tool.contained(rectangle, start, start)
    assert not tool.contained(rectangle, start + Q(1, 1000), start)
    assert not tool.contained(rectangle, start, start - Q(1, 1000))
    assert Q(1) + tool.H > tool.U
    assert tool.contained((Q(1), tool.U, Q(1), tool.U), Q(1), Q(1))


def test_anchor_completeness_and_duplicate_aliases() -> None:
    rectangles = [(Q(1), Q(2), Q(1), Q(2))] * 24
    rectangles[1] = (Q(3, 2), Q(3), Q(1, 2), Q(2))
    windows = tool.window_roster(rectangles, NAMES, deadline())
    assert windows[1]["anchor_indices"] == [0, 1]
    assert windows[1]["contained_cell_mask"] == (1 << 24) - 1
    assert len(windows) == 576
    assert windows[0]["window"] == windows[48]["window"]
    assert windows[0]["anchor_indices"] != windows[48]["anchor_indices"]


@pytest.mark.parametrize("kind", ["duplicate", "unoccupied", "window", "name"])
def test_bad_eleven_cell_witness_refuses(kind: str) -> None:
    rectangles = tool.envelopes(boxes(), deadline())
    witness = tool.scan_state(
        MASK, tool.window_roster(rectangles, NAMES, deadline()), NAMES, deadline()
    )["witness"]
    if kind == "duplicate":
        witness["cell_indices"][1] = witness["cell_indices"][0]
    elif kind == "unoccupied":
        witness["cell_indices"][-1] = 23
    elif kind == "window":
        witness["window"][1] = "0"
    else:
        witness["cells"][0] = "wrong"
    with pytest.raises(ValueError, match=r"distinct|containment"):
        tool.verify_witness(MASK, rectangles, NAMES, witness)


def theorem_fixture() -> tuple[dict[str, Any], dict[str, Any]]:
    return {
        "results": [
            {
                "id": "T-061",
                "kind": "lower-bound",
                "scope": {"n_values": [11]},
                "verification": "V3",
                "confirmation": "C3",
                "claim": "s(11) > 3875000000/999999999, inherited accepted theorem",
                "evidence": [
                    "E-n011-wang-li-source-replay",
                    "E-n011-wang-li-native-parent-core",
                ],
            }
        ]
    }, {
        "status": "PASS_FRESH_TWO_IMPLEMENTATION_FULL_REPLAY",
        "certificate_sha256": (
            "31e10ceb8368cc858e61f45ce7cfee783e8d0c7910893559164810f45439cc34"
        ),
        "rows": 12028,
        "histogram": {"1000047559": 12028},
        "surplus_units": 428125,
    }


@pytest.mark.parametrize(
    "kind", ["registry", "confirmation", "evidence", "rows", "surplus", "digest", "claim"]
)
def test_theorem_premise_tamper_refuses(kind: str) -> None:
    registry, replay = theorem_fixture()
    if kind == "registry":
        registry["results"][0]["scope"] = {"n_values": [17]}
    elif kind == "confirmation":
        registry["results"][0]["confirmation"] = "C1"
    elif kind == "evidence":
        registry["results"][0]["evidence"] = []
    elif kind == "rows":
        replay["rows"] -= 1
    elif kind == "surplus":
        replay["surplus_units"] = 0
    elif kind == "digest":
        replay["certificate_sha256"] = "0" * 64
    else:
        registry["results"][0]["claim"] = "s(11) > 3"
    with pytest.raises(ValueError, match=r"premise|evidence"):
        tool.theorem(registry, replay)


def test_accepted_theorem_is_only_inherited() -> None:
    tool.theorem(*theorem_fixture())
    assert tool.scope()["n11_theorem_reproved"] is False


@pytest.mark.parametrize("kind", ["distance", "names", "orbit"])
def test_unselected_partition_row_metadata_must_be_recomputed(kind: str) -> None:
    permutations = {f"identity-{i}": list(range(24)) for i in range(8)}
    other = MASK ^ (1 << 0) ^ (1 << 17) ^ (1 << 1) ^ (1 << 18)
    row = {
        "mask": other,
        "orbit_size": 1,
        "distance": 4,
        "cells": [NAMES[i] for i in range(24) if other & (1 << i)],
    }
    tool.named_row(row, NAMES, permutations, {MASK})
    row[{"distance": "distance", "names": "cells", "orbit": "orbit_size"}[kind]] = 0
    with pytest.raises(ValueError, match="named orbit"):
        tool.named_row(row, NAMES, permutations, {MASK})


@pytest.mark.parametrize("positive", [True, False])
def test_all95_generate_and_fresh_payload(
    monkeypatch: pytest.MonkeyPatch,
    positive: bool,  # noqa: FBT001
) -> None:
    # The synthetic inherited premise has95 records; it is not a physical packing.
    roster = [{"mask": MASK, "cells": NAMES[:17], "orbit_size": 1}] * 95
    monkeypatch.setattr(
        tool, "intake", lambda *_: (boxes(positive=positive), NAMES, roster, {})
    )
    result = tool.generate({}, deadline=deadline())
    fresh = tool.check({}, result, deadline=deadline())
    assert fresh["verification_passed"] is True
    assert result["states_accounted"] == 95
    assert result["state_window_counts_accounted"] == 54720
    assert result["criterion_met"] is positive
    assert result["ordinary_assignment_exclusion_proved"] is positive
    assert result["global_optimality_proved"] is False
    assert result["census_admission_proved"] is False
    assert result["assurance"]["t061_proof_replayed"] is False
    wrong = copy.deepcopy(result)
    wrong["states"][0]["window_counts"][0] += 1
    with pytest.raises(ValueError, match="payload"):
        tool.check({}, wrong, deadline=deadline())


def test_deadline_and_wrong_aabb_never_prove_exclusion() -> None:
    with pytest.raises(tool.finite.IncompleteError):
        tool.envelopes(boxes(), time.monotonic() - 1)
    bad = boxes()
    bad[0] = (tool.U + 1, tool.U + 2, Q(0), Q(1))
    with pytest.raises(ValueError, match="outside original frame"):
        tool.envelopes(bad, deadline())
    assert tool.failure(ValueError("bad"))["ordinary_assignment_exclusion_proved"] is False


def test_used_geometry_bit_ceiling() -> None:
    tiny = Q(1, 1 << 4096)
    bad = boxes()
    bad[0] = (tiny, tiny, tiny, tiny)
    with pytest.raises(tool.finite.IncompleteError):
        tool.envelopes(bad, deadline())


def test_byte_custody_changes_refuse(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    path = tmp_path / "premise.json"
    path.write_text("{}")
    monkeypatch.setattr(
        tool, "intake", lambda *_: (boxes(), NAMES, [{"mask": MASK}] * 95, {path: b"changed"})
    )
    with pytest.raises(ValueError, match="bytes changed"):
        tool.generate({}, deadline=deadline())


def test_two_clean_cli_processes_reconstruct_synthetic_premise(tmp_path: Path) -> None:
    descriptor = tmp_path / "descriptor.json"
    descriptor.write_text("{}")
    # The private driver injects only a labelled synthetic inherited input.
    driver = tmp_path / "driver.py"
    driver.write_text(
        "from fractions import Fraction as Q\n"
        "from devtools import check_n17_n11_envelope_windows as t\n"
        "names=[f'cell-{i}' for i in range(24)]\n"
        "t.intake=lambda *_: ([(Q(2),Q(2),Q(2),Q(2))]*24,names,[{'mask':(1<<17)-1}]*95,{})\n"
        "raise SystemExit(t.main())\n"
    )
    paths = [tmp_path / "certificate.json", tmp_path / "replay.json"]
    env = os.environ.copy()
    for i, output in enumerate(paths):
        argv = [
            sys.executable,
            str(driver),
            "--descriptor",
            str(descriptor),
            "--output",
            str(output),
        ]
        if i:
            argv += ["--certificate", str(paths[0])]
        run = subprocess.run(
            argv, check=False, capture_output=True, text=True, env=env, timeout=30
        )
        assert run.returncode == 0, run.stderr
    a, b = [json.loads(p.read_text()) for p in paths]
    assert b["verification_passed"] is True
    assert tool.payload(a) == tool.payload(b)


@pytest.mark.parametrize("kind", ["path", "revision"])
def test_registry_uses_named_git_source_without_checksum_lock(kind: str) -> None:
    document = {
        "theorem_registry": "packing/frontier/results.yaml",
        "theorem_registry_git_commit": "0" * 40,
    }
    document["theorem_registry" if kind == "path" else "theorem_registry_git_commit"] = "bad"
    with pytest.raises(ValueError, match="Git identity"):
        tool.read_registry(document, deadline())


def test_registry_git_read_is_bounded_and_projection_based(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from types import SimpleNamespace  # noqa: PLC0415

    import yaml  # noqa: PLC0415

    raw = yaml.safe_dump(theorem_fixture()[0]).encode()
    calls = []

    def run(argv: list[str], **_kwargs: Any) -> Any:
        calls.append(argv)
        value = (
            b"commit\n"
            if argv[2] == "-t"
            else str(len(raw)).encode()
            if argv[1] == "cat-file"
            else raw
        )
        return SimpleNamespace(stdout=value)

    monkeypatch.setattr(tool.subprocess, "run", run)
    for revision in ("0" * 40, "1" * 40):
        record = tool.read_registry(
            {
                "theorem_registry": "packing/frontier/results.yaml",
                "theorem_registry_git_commit": revision,
            },
            deadline(),
        )
        tool.theorem(record, theorem_fixture()[1])
    assert len(calls) == 6


def test_registry_oversized_git_object_stops_before_read(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from types import SimpleNamespace  # noqa: PLC0415

    calls = []

    def run(argv: list[str], **_kwargs: Any) -> Any:
        calls.append(argv)
        return SimpleNamespace(
            stdout=b"commit\n" if argv[2] == "-t" else str(tool.INPUT_LIMIT + 1).encode()
        )

    monkeypatch.setattr(tool.subprocess, "run", run)
    with pytest.raises(tool.finite.IncompleteError, match="byte ceiling"):
        tool.read_registry(
            {
                "theorem_registry": "packing/frontier/results.yaml",
                "theorem_registry_git_commit": "0" * 40,
            },
            deadline(),
        )
    assert len(calls) == 2


def descriptor_fixture(tmp_path: Path) -> dict[str, Any]:
    path = tmp_path / "metadata.json"
    raw = b"{}"
    path.write_bytes(raw)
    result: dict[str, Any] = {
        "schema": tool.CONTEXT_SCHEMA,
        "outer_U": str(tool.U),
        "radius": str(tool.R),
        "window_side": str(tool.H),
        "n11_lower_bound": str(tool.B11),
        "n11_premise": "T-061",
        "required_squares": 11,
        "states": [],
        "d4": {},
        "theorem_registry": "packing/frontier/results.yaml",
        "theorem_registry_git_commit": "0" * 40,
    }
    for role in ("partition", "cover", "theorem_replay"):
        result[role] = str(path)
        result[role + "_sha256"] = hashlib.sha256(raw).hexdigest()
    return result


@pytest.mark.parametrize(
    "key", ["window_side", "n11_lower_bound", "required_squares", "radius"]
)
def test_changed_frozen_scalar_refuses_before_any_input_read(tmp_path: Path, key: str) -> None:
    document = descriptor_fixture(tmp_path)
    document[key] = "0"
    with pytest.raises(ValueError, match=r"context|arity"):
        tool.intake(document, deadline())


def test_generated_artifact_digest_tamper_refuses_before_geometry(tmp_path: Path) -> None:
    document = descriptor_fixture(tmp_path)
    document["partition_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="bytes differ"):
        tool.intake(document, deadline())
