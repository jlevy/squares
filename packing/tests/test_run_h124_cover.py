"""Bounded caller controls use unrelated toy sources, never H124 construction."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace
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


@pytest.mark.parametrize("frame", ["axis", "diagonal"])
def test_scientific_routes_select_independent_constructors_without_calling_them(
    frame: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[tuple[str, bool]] = []

    def source(frame: str, *, reader: bool):
        calls.append((frame, reader))
        return runner.toy_source("covered")

    monkeypatch.setattr(runner, "scientific_source", source)
    raw = runner.worker(frame=frame, control=None, raw=None, limit=100)
    runner.worker(frame=frame, control=None, raw=raw, limit=100)
    assert calls == [(frame, False), (frame, True)]


@pytest.mark.parametrize("control", ["covered", "gap"])
def test_collision_routes_use_independent_mock_modules(
    control: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    calls: list[tuple[str, tuple[Any, ...]]] = []

    def load(module: str) -> SimpleNamespace:
        def source(*args: Any):
            calls.append((module, args))
            return runner.toy_source(control)

        return SimpleNamespace(cover_source=source)

    monkeypatch.setattr(runner, "import_module", load)
    raw = runner.worker(frame=None, control=None, collision=True, raw=None, limit=100)
    checked = runner.worker(frame=None, control=None, collision=True, raw=raw, limit=100)
    assert calls == [
        ("devtools.h124_collision_source", ()),
        ("devtools.check_h124_collision_source", ()),
    ]
    assert raw["kind"] == runner.KIND
    assert raw["source"] == checked["source"] == "h124:axis-collision-v1"
    assert checked["cover_proved"] is (control == "covered")
    assert checked["status"] == (
        "verified_source_cover" if control == "covered" else "unresolved"
    )


def test_collision_refuses_old_axis_envelope_before_source_load(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    raw = runner.worker(frame=None, control="covered", raw=None, limit=100)
    raw["source"] = "h124:axis"

    def forbidden(*_args: Any, **_kwargs: Any):
        raise AssertionError("source loader reached")

    monkeypatch.setattr(runner, "import_module", forbidden)
    with pytest.raises(ValueError, match="envelope"):
        runner.worker(frame=None, control=None, collision=True, raw=raw, limit=100)


@pytest.mark.parametrize(
    ("frame", "control", "collision"),
    [
        (None, None, 1),
        (None, None, 0),
        (None, None, "true"),
        (None, None, None),
        ("axis", None, True),
        (None, "covered", True),
    ],
)
def test_collision_admission_rejects_non_boolean_and_multiple_modes(
    frame: str | None,
    control: str | None,
    collision: Any,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def forbidden(*_args: Any, **_kwargs: Any):
        raise AssertionError("source loader reached")

    monkeypatch.setattr(runner, "import_module", forbidden)
    with pytest.raises(ValueError, match=r"boolean|required"):
        runner.worker(frame=frame, control=control, collision=collision, raw=None, limit=100)


def test_parent_forwards_explicit_collision_mode(monkeypatch: pytest.MonkeyPatch) -> None:
    def run(command: list[str], **kwargs: Any):
        assert command[3:] == [
            "--worker",
            "--limit",
            "100",
            "--timeout-seconds",
            "2",
            "--axis-collision",
            "--input",
            "unused",
        ]
        assert kwargs["timeout"] == 2
        return subprocess.CompletedProcess(command, 0, stdout="", stderr="")

    monkeypatch.setattr(runner.subprocess, "run", run)
    assert (
        runner.main(
            [
                "--axis-collision",
                "--limit",
                "100",
                "--timeout-seconds",
                "2",
                "--input",
                "unused",
            ]
        )
        == 0
    )


@pytest.mark.parametrize("other", [["--frame", "axis"], ["--toy-control", "covered"]])
def test_collision_cli_modes_are_mutually_exclusive(other: list[str]) -> None:
    with pytest.raises(SystemExit) as error:
        runner.main(
            [
                "--axis-collision",
                *other,
                "--limit",
                "100",
                "--timeout-seconds",
                "1",
            ]
        )
    assert error.value.code == 2


@pytest.mark.parametrize(
    "arguments",
    [
        ["--limit", "100", "--timeout-seconds", "1"],
        ["--axis-collision", "--limit", "0", "--timeout-seconds", "1"],
        ["--axis-collision", "--limit", "5001", "--timeout-seconds", "1"],
        ["--axis-collision", "--limit", "1", "--timeout-seconds", "0"],
        ["--axis-collision", "--limit", "1", "--timeout-seconds", "121"],
    ],
)
def test_collision_is_not_default_and_keeps_parser_caps(arguments: list[str]) -> None:
    with pytest.raises(SystemExit) as error:
        runner.main(arguments)
    assert error.value.code == 2


def test_collision_worker_cli_roundtrip_with_mocked_sources(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    modules: list[str] = []

    def load(module: str) -> SimpleNamespace:
        modules.append(module)
        return SimpleNamespace(cover_source=lambda: runner.toy_source("covered"))

    monkeypatch.setattr(runner, "import_module", load)
    command = ["--worker", "--axis-collision", "--limit", "100", "--timeout-seconds", "2"]
    assert runner.main(command) == 0
    raw = json.loads(capsys.readouterr().out)
    monkeypatch.setattr(runner, "load_packet", lambda _path: raw)
    assert runner.main([*command, "--input", "unused"]) == 0
    checked = json.loads(capsys.readouterr().out)
    assert modules == ["devtools.h124_collision_source", "devtools.check_h124_collision_source"]
    assert checked["source"] == "h124:axis-collision-v1"
    assert checked["status"] == "verified_source_cover"
    assert checked["cover_proved"] is True


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


@pytest.mark.parametrize("mode", [["--frame", "axis"], ["--axis-collision"]])
def test_null_input_cannot_switch_replay_to_production(
    mode: list[str],
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
                *mode,
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
