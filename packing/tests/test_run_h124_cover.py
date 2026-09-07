"""Bounded caller controls use unrelated toy sources, never H124 construction."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest

from devtools import run_h124_cover as runner


@pytest.mark.parametrize("control", ["covered", "gap"])
def test_toy_production_and_independent_replay(control: str) -> None:
    raw = runner.worker(frame=None, control=control, raw=None, limit=100)
    checked = runner.worker(frame=None, control=control, raw=raw, limit=100)
    assert checked["cover_proved"] is (control == "covered")
    assert checked["status"] == (
        "verified_source_cover" if control == "covered" else "unresolved"
    )
    assert checked["source"] == f"toy:{control}"


def test_source_binding_and_envelope_mutations_refuse() -> None:
    raw = runner.worker(frame=None, control="covered", raw=None, limit=100)
    for key, value in [("kind", "other"), ("source", "h124:axis"), ("extra", 0)]:
        with pytest.raises(ValueError, match="envelope"):
            runner.worker(frame=None, control="covered", raw={**raw, key: value}, limit=100)


def test_scientific_routes_select_independent_constructors_without_calling_them(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[tuple[str, bool]] = []

    def source(frame: str, *, reader: bool):
        calls.append((frame, reader))
        return runner.toy_source("covered")

    monkeypatch.setattr(runner, "scientific_source", source)
    raw = runner.worker(frame="axis", control=None, raw=None, limit=100)
    runner.worker(frame="axis", control=None, raw=raw, limit=100)
    assert calls == [("axis", False), ("axis", True)]


@pytest.mark.parametrize(
    ("frame", "control", "limit"),
    [(None, None, 1), ("axis", "gap", 1), ("bad", None, 1), ("axis", None, 0)],
)
def test_bad_admission_does_not_load_sources(
    frame: str | None,
    control: str | None,
    limit: int,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def forbidden(*_args: Any, **_kwargs: Any):
        raise AssertionError("source loader reached")

    monkeypatch.setattr(runner, "scientific_source", forbidden)
    with pytest.raises(ValueError, match=r"required|band|cap"):
        runner.worker(frame=frame, control=control, raw=None, limit=limit)


def test_output_cap_includes_newline_and_rejects_nan(monkeypatch: pytest.MonkeyPatch) -> None:
    raw = {"toy": "small"}
    encoded = json.dumps(raw, sort_keys=True)
    monkeypatch.setattr(runner, "PACKET_BYTES", len(encoded.encode()) + 1)
    assert runner.serialize_packet(raw) == encoded
    monkeypatch.setattr(runner, "PACKET_BYTES", len(encoded.encode()))
    with pytest.raises(ValueError, match="byte cap"):
        runner.serialize_packet(raw)
    with pytest.raises(ValueError, match="JSON compliant"):
        runner.serialize_packet({"bad": float("nan")})


def test_parent_timeout_discards_partial_stdout(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    def timeout(command: list[str], **kwargs: Any):
        assert kwargs["timeout"] == 1
        raise subprocess.TimeoutExpired(command, 1, output="partial")

    monkeypatch.setattr(runner.subprocess, "run", timeout)
    assert (
        runner.main(["--toy-control", "covered", "--limit", "100", "--timeout-seconds", "1"])
        == 1
    )
    assert not capsys.readouterr().out


def test_null_input_cannot_switch_replay_to_production(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    def forbidden(**_kwargs: Any):
        raise AssertionError("source or producer reached")

    monkeypatch.setattr(runner, "load_packet", lambda _path: None)
    monkeypatch.setattr(runner, "worker", forbidden)
    assert (
        runner.main(
            [
                "--worker",
                "--frame",
                "axis",
                "--limit",
                "1",
                "--timeout-seconds",
                "1",
                "--input",
                "unused",
            ]
        )
        == 2
    )
    captured = capsys.readouterr()
    assert not captured.out
    assert "input certificate must be an object" in captured.err


@pytest.mark.parametrize("control", ["covered", "gap"])
def test_real_toy_cli_roundtrip(control: str, tmp_path: Path) -> None:
    command = [
        sys.executable,
        "-m",
        "devtools.run_h124_cover",
        "--toy-control",
        control,
        "--limit",
        "100",
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
    assert json.loads(replayed.stdout)["cover_proved"] is (control == "covered")
