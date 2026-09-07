"""Unrelated source-free binding controls; never construct a scientific family."""

from __future__ import annotations

import copy
import json
import subprocess
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools import run_full_size_density_graph as runner
from devtools.check_full_size_density_pair_separator import control_family
from sqpack.full_size_density.pair_separator import make_family
from sqpack.full_size_density.support_ceiling import SupportError


@pytest.mark.parametrize(
    ("source", "proved"), [("toy-edge-v1", True), ("toy-overlap-v1", False)]
)
def test_toy_binding_and_full_independent_replay(source: str, *, proved: bool) -> None:
    family = control_family(source)
    packet = runner.produce_bound(family, source, node_limit=10)
    checked = runner.replay_bound(packet, family, source)
    assert checked["bound_proved"] is proved
    assert checked["status"] == ("verified_density_bound" if proved else "unresolved")
    assert checked["mass"] == "3/2"


def test_all_cyclic_representations_bind_identically_and_zero_is_retained() -> None:
    family = control_family("toy-edge-v1")
    altered = make_family(
        tuple(
            tuple(reversed(entry.square[1:] + entry.square[:1])) for entry in family.placements
        ),
        family.side,
        tuple(entry.weight for entry in family.placements),
    )
    assert runner.family_source(altered) == runner.family_source(family)
    zeros = make_family(
        tuple(entry.square for entry in family.placements),
        family.side,
        (Fraction(0), Fraction(1)),
    )
    raw = runner.family_source(zeros)
    assert len(raw["squares"]) == 2
    assert raw["squares"][0]["weight"] == "0"
    packet = runner.produce_bound(zeros, "toy", node_limit=10)
    assert runner.replay_bound(packet, zeros, "toy")["bound_proved"] is True


@pytest.mark.parametrize(
    ("key", "value"),
    [("version", True), ("source", "wrong"), ("side", ["0"])],
)
def test_wrapper_binding_tampering_is_refused(key: str, value: Any) -> None:
    family = control_family("toy-edge-v1")
    packet = runner.produce_bound(family, "toy-edge-v1", node_limit=10)
    packet[key] = value
    with pytest.raises(SupportError):
        runner.replay_bound(packet, family, "toy-edge-v1")


def test_zero_weight_source_geometry_cannot_be_substituted() -> None:
    family = control_family("toy-edge-v1")
    packet = runner.produce_bound(family, "toy-edge-v1", node_limit=10)
    altered = copy.deepcopy(packet)
    altered["certificate"]["source"]["squares"][0]["weight"] = "0"
    with pytest.raises(ValueError, match="source"):
        runner.replay_bound(altered, family, "toy-edge-v1")


def test_invalid_admission_never_loads_any_source(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden(*_args: Any, **_kwargs: Any) -> Any:
        raise AssertionError("source loading was reached")

    monkeypatch.setattr(runner, "control_family", forbidden)
    monkeypatch.setattr(runner, "load_packet", forbidden)
    for control, candidate, nodes in [
        (None, None, 1),
        ("bad", None, 1),
        ("toy-edge-v1", None, 0),
    ]:
        with pytest.raises(SupportError):
            runner.worker(control=control, candidate=candidate, packet=None, node_limit=nodes)


def test_candidate_routes_use_separate_constructors_without_real_input(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    family = control_family("toy-edge-v1")
    calls: list[str] = []
    monkeypatch.setattr(runner, "load_packet", lambda _path: {})

    def constructor(name: str):
        def build(_parent: Any):
            calls.append(name)
            return family

        return build

    monkeypatch.setattr(runner, "frozen_candidate", constructor("producer"))
    monkeypatch.setattr(runner, "candidate_family", constructor("reader"))
    monkeypatch.setattr(runner, "produce_bound", lambda *_args, **_kwargs: {})
    monkeypatch.setattr(runner, "replay_bound", lambda *_args, **_kwargs: {})
    runner.worker(control=None, candidate=Path("unused"), packet=None, node_limit=1)
    runner.worker(control=None, candidate=Path("unused"), packet=Path("unused2"), node_limit=1)
    assert calls == ["producer", "reader"]


def test_parent_timeout_never_emits_a_partial_success(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    def timeout(command: list[str], **kwargs: Any) -> Any:
        assert kwargs["timeout"] == 1
        raise subprocess.TimeoutExpired(command, 1)

    monkeypatch.setattr(runner.subprocess, "run", timeout)
    assert (
        runner.main(["--control", "toy-edge-v1", "--node-limit", "1", "--timeout-seconds", "1"])
        == 1
    )
    captured = capsys.readouterr()
    assert not captured.out
    assert "unresolved" in captured.err


@pytest.mark.parametrize(
    ("nodes", "seconds"), [("0", "1"), ("1", "0"), ("10001", "1"), ("1", "61")]
)
def test_cli_limits_are_validated_before_launch(nodes: str, seconds: str) -> None:
    with pytest.raises(SystemExit) as exc:
        runner.main(
            ["--control", "toy-edge-v1", "--node-limit", nodes, "--timeout-seconds", seconds]
        )
    assert exc.value.code == 2


def test_explicit_toy_cli_producer_and_reader_roundtrip(tmp_path: Path) -> None:
    command = [
        sys.executable,
        "-m",
        "devtools.run_full_size_density_graph",
        "--control",
        "toy-edge-v1",
        "--node-limit",
        "10",
        "--timeout-seconds",
        "5",
    ]
    produced = subprocess.run(command, capture_output=True, text=True, timeout=8, check=False)
    assert produced.returncode == 0, produced.stderr
    packet = tmp_path / "toy.json"
    packet.write_text(produced.stdout, encoding="utf-8")
    replayed = subprocess.run(
        [*command, "--input", str(packet)],
        capture_output=True,
        text=True,
        timeout=8,
        check=False,
    )
    assert replayed.returncode == 0, replayed.stderr
    checked = json.loads(replayed.stdout)
    assert checked["status"] == "verified_density_bound"
    assert checked["bound_proved"] is True
    assert checked["mass"] == "3/2"


@pytest.mark.parametrize("limit_name", ["PRODUCER_MAX_FIELD_DEGREE", "READER_MAX_FIELD_DEGREE"])
def test_declared_degree_preflight_precedes_scientific_loaders(
    limit_name: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def forbidden(*_args: Any, **_kwargs: Any) -> Any:
        raise AssertionError("scientific loader was reached")

    monkeypatch.setattr(runner, limit_name, 4)
    monkeypatch.setattr(runner, "control_family", forbidden)
    monkeypatch.setattr(runner, "load_packet", forbidden)
    for control, candidate in [("trump-original-control-v1", None), (None, Path("unused"))]:
        with pytest.raises(SupportError, match="declared source degree"):
            runner.worker(control=control, candidate=candidate, packet=None, node_limit=1)


def test_serialized_output_limit_includes_the_final_newline(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    raw = {"payload": "small unrelated toy"}
    expected = json.dumps(raw, sort_keys=True)
    monkeypatch.setattr(runner, "PACKET_BYTES", len(expected.encode("utf-8")) + 1)
    assert runner.serialize_packet(raw) == expected
    monkeypatch.setattr(runner, "PACKET_BYTES", len(expected.encode("utf-8")))
    with pytest.raises(SupportError, match=r"serialized.*byte cap"):
        runner.serialize_packet(raw)
