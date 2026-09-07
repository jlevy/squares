"""Toy adapters and malformed receipts only; target/source-scale dispatch is mocked."""

from __future__ import annotations

import copy
import json
import signal
import subprocess
import sys
from pathlib import Path

import pytest

import devtools.check_full_size_density_faces as reader
import devtools.run_full_size_density_faces as producer
from devtools.check_full_size_density_faces import replay_packet
from devtools.check_full_size_density_pair_separator import (
    CANDIDATE_WEIGHTS,
    bind_parent,
)
from devtools.check_full_size_density_support_ceiling import load_packet
from devtools.run_full_size_density_faces import produce
from sqpack.full_size_density.support_ceiling import SupportError


def test_contact_receipt_requires_a_complete_independent_slab_replay() -> None:
    packet = produce(control="toy-edge-v1")
    assert packet["result"] == {"kind": "complete-ae-maximum", "maximum": "1"}
    decision = replay_packet(packet, control="toy-edge-v1")
    assert decision["decision"] == "ae-feasible"
    assert decision["maximum"] == "1"


@pytest.mark.parametrize("control", ["toy-corner-v1", "toy-gap-v1", "toy-equal-v1"])
def test_complete_positive_toys(control: str) -> None:
    assert replay_packet(produce(control=control), control=control)["decision"] == "ae-feasible"


@pytest.mark.parametrize(
    "control", ["toy-triple-v1", "toy-narrow-overlap-v1", "toy-algebraic-v1"]
)
def test_strict_negative_uses_independent_box_not_full_replay(
    control: str, monkeypatch
) -> None:
    packet = produce(control=control)

    def forbidden(*_args, **_kwargs):
        pytest.fail("negative witness must not require a complete positive replay")

    monkeypatch.setattr(reader, "verify_density_slabs", forbidden)
    assert packet["result"]["kind"] == "strict-excess-box"
    decision = replay_packet(packet, control=control)
    assert decision["decision"] == "fixed-weights-refuted"
    assert decision["maximum"] is None


def test_forged_positive_requires_actual_complete_maximum() -> None:
    packet = produce(control="toy-triple-v1")
    packet["result"] = {"kind": "complete-ae-maximum", "maximum": "1"}
    with pytest.raises(SupportError, match="independent complete"):
        replay_packet(packet, control="toy-triple-v1")


def test_receipt_header_and_rational_refusals() -> None:
    original = produce(control="toy-edge-v1")
    for key, value in (
        ("version", True),
        ("source", "exp-113-candidate-v1"),
        ("semantics", "closed-pointwise-depth"),
        ("mass", "3/2e0"),
        ("mass", "6/4"),
        ("mass", 1.5),
        ("mass", True),
        ("mass", "9"),
        ("result", {"kind": "complete-ae-maximum", "maximum": "1", "partial": True}),
        ("result", {"kind": "complete-ae-maximum", "maximum": "3/2"}),
        ("result", {"kind": "complete-ae-maximum", "maximum": False}),
        ("result", {"kind": "unchecked"}),
    ):
        packet = copy.deepcopy(original)
        packet[key] = value
        with pytest.raises(SupportError):
            replay_packet(packet, control="toy-edge-v1")
    for key in original:
        packet = copy.deepcopy(original)
        del packet[key]
        with pytest.raises(SupportError):
            replay_packet(packet, control="toy-edge-v1")


def test_side_weight_and_duplicate_geometry_refusals() -> None:
    original = produce(control="toy-edge-v1")
    for part in ("side", "weight", "duplicate"):
        packet = copy.deepcopy(original)
        if part == "side":
            packet["family"]["side"] = ["4"]
        elif part == "weight":
            packet["family"]["placements"][0]["weight"] = "0"
        else:
            packet["family"]["placements"].append(packet["family"]["placements"][0])
        with pytest.raises(SupportError, match="canonical support"):
            replay_packet(packet, control="toy-edge-v1")


def test_negative_box_mutations_are_refused() -> None:
    original = produce(control="toy-triple-v1")
    for key, value in (
        ("radius", "0"),
        ("radius", "2"),
        ("radius", "2/4"),
        ("excess", "1"),
        ("members", [0, 0, 1, 2]),
        ("members", [True, 1, 2]),
        ("members", [0, 1, 99]),
        ("members", [2, 1, 0]),
        ("members", []),
        ("point", [["1", "0"], ["1"]]),
        ("point", [["0"], ["0"]]),
    ):
        packet = copy.deepcopy(original)
        packet["result"][key] = value
        with pytest.raises(SupportError):
            replay_packet(packet, control="toy-triple-v1")


def test_mode_refusals_precede_any_source_construction(monkeypatch) -> None:
    packet = produce(control="toy-edge-v1")

    def forbidden(*_args, **_kwargs):
        pytest.fail("malformed mode reached source construction")

    monkeypatch.setattr(reader, "candidate_family", forbidden)
    monkeypatch.setattr(reader, "control_family", forbidden)
    monkeypatch.setattr(producer, "source_family", forbidden)
    for arguments in ({}, {"control": "unknown"}, {"control": "toy-edge-v1", "parent": {}}):
        with pytest.raises(SupportError):
            replay_packet(packet, **arguments)
        with pytest.raises(SupportError):
            produce(**arguments)
    with pytest.raises(SupportError, match="explicit mode"):
        replay_packet(packet, parent={})


def test_parent_binding_rejects_changed_source_side_and_weights_without_geometry() -> None:
    metadata = {"side": ["declared-source-side"], "orbits": ["declared-source-orbits"]}
    parent = {
        "version": 1,
        "source": "trump11-v1",
        "support": metadata,
        "rows": [],
        "dispositions": [],
        "primal": [str(weight) for weight in CANDIDATE_WEIGHTS],
        "multipliers": [],
        "bound": "56/5",
        "solve_pivots": 0,
    }
    # This seam binds previously accepted metadata; it does not replay the LP.
    bind_parent(parent, metadata)
    for key, value in (
        ("version", True),
        ("source", "another-source"),
        ("support", {"side": ["changed-side"], "orbits": metadata["orbits"]}),
        ("primal", ["0"] * 8),
        ("bound", "11"),
    ):
        changed = copy.deepcopy(parent)
        changed[key] = value
        with pytest.raises(SupportError):
            bind_parent(changed, metadata)


@pytest.mark.parametrize("text", ['{"a":1,"a":2}', '{"a":1.5}', '{"a":NaN}', '{"a":'])
def test_bounded_file_parser_refuses_ambiguous_or_partial_json(
    tmp_path: Path, text: str
) -> None:
    path = tmp_path / "packet.json"
    path.write_text(text)
    with pytest.raises(SupportError):
        load_packet(path)


def test_bounded_file_parser_refuses_symlink_and_size(tmp_path: Path) -> None:
    path = tmp_path / "packet.json"
    path.write_text("{}")
    link = tmp_path / "link.json"
    link.symlink_to(path)
    with pytest.raises(SupportError):
        load_packet(link)
    path.write_text(" " * (reader.MAX_RECEIPT_BYTES + 1))
    with pytest.raises(SupportError):
        load_packet(path)


@pytest.mark.parametrize("module", [producer, reader])
def test_cli_requires_explicit_bounded_cap(module) -> None:
    prefix = ["unused.json"] if module is reader else []
    for suffix in ([], ["--timeout-seconds", "0"], ["--timeout-seconds", "121"]):
        with pytest.raises(SystemExit) as caught:
            module.main([*prefix, "--control", "toy-edge-v1", *suffix])
        assert caught.value.code == 2


def test_nonzero_or_truncated_child_never_publishes_partial_receipt(
    monkeypatch, capsys
) -> None:
    monkeypatch.setattr(
        reader.subprocess,
        "run",
        lambda *_args, **_kwargs: subprocess.CompletedProcess([], 1, '{"partial":', "stopped"),
    )
    assert producer.main(["--control", "toy-edge-v1", "--timeout-seconds", "1"]) == 1
    assert capsys.readouterr().out == ""
    monkeypatch.setattr(
        reader.subprocess,
        "run",
        lambda *_args, **_kwargs: subprocess.CompletedProcess([], 0, '{"partial":', ""),
    )
    assert producer.main(["--control", "toy-edge-v1", "--timeout-seconds", "1"]) == 2
    assert capsys.readouterr().out == ""


def test_timeout_discards_output_and_child_alarm_covers_loading(monkeypatch, capsys) -> None:
    def expired_process(*_args, **kwargs):
        assert kwargs["timeout"] == 7
        raise subprocess.TimeoutExpired("toy", 7, output='{"partial":')

    monkeypatch.setattr(reader.subprocess, "run", expired_process)
    assert producer.main(["--control", "toy-edge-v1", "--timeout-seconds", "7"]) == 1
    assert capsys.readouterr().out == ""
    alarms = []
    previous = signal.getsignal(signal.SIGALRM)
    monkeypatch.setattr(reader.signal, "alarm", alarms.append)

    def expired_load(_path):
        assert alarms == [7]
        raise TimeoutError("loading exceeded the cap")

    monkeypatch.setattr(reader, "load_packet", expired_load)
    assert (
        reader.main(
            ["unused.json", "--control", "toy-edge-v1", "--timeout-seconds", "7", "--worker"]
        )
        == 1
    )
    assert alarms == [7, 0]
    assert signal.getsignal(signal.SIGALRM) == previous


def test_real_toy_file_roundtrip_in_bounded_processes(tmp_path: Path) -> None:
    produced = subprocess.run(
        [
            sys.executable,
            "-m",
            "devtools.run_full_size_density_faces",
            "--control",
            "toy-edge-v1",
            "--timeout-seconds",
            "5",
        ],
        text=True,
        capture_output=True,
        timeout=7,
        check=True,
    )
    path = tmp_path / "receipt.json"
    path.write_text(produced.stdout)
    checked = subprocess.run(
        [
            sys.executable,
            "-m",
            "devtools.check_full_size_density_faces",
            str(path),
            "--control",
            "toy-edge-v1",
            "--timeout-seconds",
            "5",
        ],
        text=True,
        capture_output=True,
        timeout=7,
        check=True,
    )
    assert json.loads(checked.stdout)["decision"] == "ae-feasible"
