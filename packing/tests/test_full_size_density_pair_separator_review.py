"""Independent toy/input controls; no target construction or binding roundtrip."""

from __future__ import annotations

import copy
import json
import signal
from pathlib import Path
from typing import Any

import pytest

from devtools import check_full_size_density_pair_separator as checker
from devtools import run_full_size_density_pair_separator as runner
from sqpack.full_size_density.support_ceiling import SupportError


def hand_built_toy_witness() -> dict[str, Any]:
    family = checker.control_family("toy-overlap-v1")
    return {
        "version": 1,
        "source": "toy-overlap-v1",
        "family": checker.family_signature(family),
        "eligible": 1,
        "separations": [],
        "witness": {
            "pair": [0, 1],
            "point": [["5/4"], ["1"]],
            "radius": "1/16",
            "excess": "1/2",
        },
    }


def test_hand_built_witness_requires_strict_margins_and_positive_area() -> None:
    # The overlap is [1, 3/2] x [1/2, 3/2]; the selected center has minimum margin 1/4.
    packet = hand_built_toy_witness()
    assert checker.replay_packet(packet) == "candidate-refuted"
    for change in (
        {"radius": "1/8"},
        {"radius": "0"},
        {"point": [["1"], ["1"]]},
        {"excess": "0"},
    ):
        altered = copy.deepcopy(packet)
        altered["witness"].update(change)
        with pytest.raises(SupportError):
            checker.replay_packet(altered)
    omitted = copy.deepcopy(packet)
    omitted["witness"] = None
    with pytest.raises(SupportError, match="omits an eligible pair"):
        checker.replay_packet(omitted)


def test_worker_alarms_cover_input_and_restore_handlers(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    previous = object()
    handlers: list[Any] = []
    alarms: list[int] = []
    for tool in (runner, checker):
        handlers.clear()
        alarms.clear()
        with monkeypatch.context() as patch:

            def install(signum: int, handler: Any) -> Any:
                assert signum == signal.SIGALRM
                handlers.append(handler)
                return previous

            def arm(seconds: int) -> int:
                alarms.append(seconds)
                return 0

            def interrupted(*_args: Any, **_kwargs: Any) -> None:
                assert alarms == [30]
                handlers[0](signal.SIGALRM, None)
                raise AssertionError("the installed alarm handler did not interrupt")

            patch.setattr(tool.signal, "signal", install)
            patch.setattr(tool.signal, "alarm", arm)
            if tool is runner:
                patch.setattr(runner, "worker", interrupted)
                arguments = ["--control", "toy-edge-v1", "--worker"]
            else:
                patch.setattr(checker, "load_packet", interrupted)
                arguments = ["unopened-toy.json", "--worker"]
            assert tool.main(arguments) == 1
            captured = capsys.readouterr()
            assert captured.out == ""
            assert "unresolved" in captured.err
            assert alarms == [30, 0]
            assert len(handlers) == 2
            assert handlers[-1] is previous


def test_public_reader_accepts_toy_file_and_refuses_link_and_duplicate_keys(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "toy.json"
    path.write_text(json.dumps(hand_built_toy_witness()))
    assert checker.main([str(path), "--worker"]) == 0
    captured = capsys.readouterr()
    assert json.loads(captured.out) == {
        "verdict": "candidate-refuted",
        "scope": "fixed candidate only; H099 unresolved; no-hit is not feasibility",
    }
    assert "cpu_seconds" in json.loads(captured.err)

    link = tmp_path / "linked-toy.json"
    link.symlink_to(path)
    for refused in (link, tmp_path):
        assert checker.main([str(refused), "--worker"]) == 2
        captured = capsys.readouterr()
        assert captured.out == ""
        assert "regular file" in captured.err

    path.write_text('{"version":1,"version":1}')
    assert checker.main([str(path), "--worker"]) == 2
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "duplicate JSON" in captured.err
