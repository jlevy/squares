"""Target-free real process-group controls for bounded POSIX launches."""

from __future__ import annotations

import json
import os
import select
import signal
import subprocess
import sys
import time
from collections.abc import Callable
from pathlib import Path
from types import SimpleNamespace
from typing import Any
from unittest.mock import Mock

import pytest

from devtools import supervise_posix as tool

pytestmark = pytest.mark.skipif(os.name != "posix", reason="POSIX-only instrument")


def run(tmp_path: Path, code: str, **kwargs: float) -> dict[str, Any]:
    return tool.supervise(
        [sys.executable, "-c", code],
        stdout=tmp_path / "stdout",
        stderr=tmp_path / "stderr",
        max_seconds=kwargs.get("max_seconds", 3),
        max_memory_mib=kwargs.get("max_memory_mib", 4096),
        sample_seconds=0.02,
        cleanup_seconds=0.2,
    )


def test_short_sleep_normal_exit_preserves_partial_logs(tmp_path: Path) -> None:
    receipt = run(
        tmp_path,
        "import time,sys; print('saved',flush=True); "
        "print('err',file=sys.stderr,flush=True); time.sleep(.05)",
    )
    assert receipt["status"] == "COMPLETED"
    assert receipt["returncode"] == 0
    assert receipt["cleanup_complete"]
    assert (tmp_path / "stdout").read_text() == "saved\n"
    assert (tmp_path / "stderr").read_text() == "err\n"


@pytest.mark.parametrize("stop_reason", ["wall_limit", "supervisor_signal"])
def test_exit_observed_after_blocking_sample_keeps_stop_reason(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, stop_reason: str
) -> None:
    """A sampling delay cannot turn a timer- or signal-stopped child into success."""
    now = 0.0
    child = Mock(pid=12345, returncode=None)
    child.poll.side_effect = lambda: child.returncode
    callbacks: list[Callable[[], None]] = []

    def timer(_delay: float, callback: Callable[[], None]) -> Mock:
        callbacks.append(callback)
        return Mock()

    def sample(pgid: int) -> dict[int, int]:
        nonlocal now
        if pgid == os.getpgrp():
            return {os.getpid(): 1}
        if child.returncode is None:
            if stop_reason == "wall_limit":
                now = 1.0
                callbacks[0]()
            else:
                handler = signal.getsignal(signal.SIGTERM)
                assert callable(handler)
                handler(signal.SIGTERM, None)
            child.returncode = -signal.SIGTERM
        return {}

    launch = Mock(return_value=child)
    monkeypatch.setattr(tool.subprocess, "Popen", launch)
    monkeypatch.setattr(tool.threading, "Timer", timer)
    monkeypatch.setattr(tool, "time", SimpleNamespace(monotonic=lambda: now, sleep=Mock()))
    monkeypatch.setattr(tool, "_signal_group", Mock())
    receipt = tool.supervise(
        ["owned-command"],
        max_seconds=1,
        max_memory_mib=1,
        sample_seconds=0.1,
        cleanup_seconds=0.2,
        stdout=tmp_path / "stdout",
        stderr=tmp_path / "stderr",
        sampler=sample,
    )
    assert launch.call_args.kwargs["start_new_session"] is True
    assert receipt["owned_pgid"] == child.pid
    assert receipt["status"] == "INCOMPLETE"
    assert receipt["reason"] == stop_reason
    assert receipt["returncode"] == -signal.SIGTERM
    assert receipt["cleanup_complete"]
    child.wait.assert_called_once_with(timeout=2)


@pytest.mark.pool_heavy
@pytest.mark.parametrize("startup_seconds", [0.0, 0.3])
def test_timeout_kills_term_ignoring_group(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, startup_seconds: float
) -> None:
    command = [
        sys.executable,
        "-c",
        (
            "import signal,sys,time; time.sleep(float(sys.argv[1])); "
            "signal.signal(signal.SIGTERM,signal.SIG_IGN); "
            "print('ready',flush=True); time.sleep(30)"
        ),
        str(startup_seconds),
    ]
    child = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, start_new_session=True
    )
    try:
        assert child.stdout is not None
        ready, _, _ = select.select([child.stdout], [], [], 5)
        assert ready == [child.stdout]
        assert child.stdout.readline() == b"ready\n"
        # Interpreter startup can exceed the wall limit; give it an initialized group.
        monkeypatch.setattr(
            tool,
            "subprocess",
            SimpleNamespace(
                Popen=Mock(return_value=child),
                run=subprocess.run,
                SubprocessError=subprocess.SubprocessError,
            ),
        )
        receipt = tool.supervise(
            command,
            stdout=tmp_path / "stdout",
            stderr=tmp_path / "stderr",
            max_seconds=0.2,
            max_memory_mib=4096,
            sample_seconds=0.02,
            cleanup_seconds=0.2,
        )
    finally:
        if child.poll() is None:
            os.killpg(child.pid, signal.SIGKILL)
        child.wait(timeout=2)
        if child.stdout is not None:
            child.stdout.close()
    assert receipt["status"] == "INCOMPLETE"
    assert receipt["reason"] == "wall_limit"
    assert receipt["kill_elapsed_seconds"] is not None
    assert receipt["returncode"] == -signal.SIGKILL
    assert receipt["wall_seconds"] < 2
    assert receipt["cleanup_complete"]


def test_current_rss_guard_and_unavailable_guard(tmp_path: Path) -> None:
    receipt = run(
        tmp_path, "import time; a=bytearray(20*1024*1024); time.sleep(30)", max_memory_mib=1
    )
    assert receipt["reason"] == "memory_limit"
    assert receipt["cleanup_complete"]
    assert receipt["maximum_sampled_current_rss_bytes_by_pid"]
    with pytest.raises(OSError, match="cannot observe"):
        tool.supervise(
            [sys.executable, "-c", "raise AssertionError"],
            max_seconds=1,
            max_memory_mib=1,
            sample_seconds=0.1,
            stdout=tmp_path / "x",
            stderr=tmp_path / "y",
            sampler=lambda _: {},
        )
    assert not (tmp_path / "x").exists()


def test_sampling_cadence_is_bounded_in_live_run(tmp_path: Path) -> None:
    receipt = tool.supervise(
        [sys.executable, "-c", "import time; time.sleep(1)"],
        max_seconds=3,
        max_memory_mib=4096,
        sample_seconds=0.1,
        stdout=tmp_path / "cadence.stdout",
        stderr=tmp_path / "cadence.stderr",
        cleanup_seconds=0.2,
    )
    assert receipt["status"] == "COMPLETED"
    assert 5 <= receipt["samples"] <= 15


def test_cli_signal_cleans_owned_descendants_not_unrelated(tmp_path: Path) -> None:
    unrelated = subprocess.Popen(
        [sys.executable, "-c", "import time; time.sleep(30)"], start_new_session=True
    )
    receipt = tmp_path / "receipt.json"
    launched = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "devtools.supervise_posix",
            "--max-seconds",
            "20",
            "--sample-seconds",
            ".02",
            "--output",
            str(receipt),
            "--",
            sys.executable,
            "-c",
            (
                "import subprocess,sys,time; "
                "p=subprocess.Popen([sys.executable,'-c','import time;time.sleep(30)']); "
                "print(p.pid,flush=True);time.sleep(30)"
            ),
        ]
    )
    try:
        log = receipt.with_suffix(".stdout.log")
        deadline = time.monotonic() + 5
        while (not log.exists() or not log.read_text().strip()) and time.monotonic() < deadline:
            time.sleep(0.02)
        assert log.exists()
        assert log.read_text().strip()
        descendant = int(log.read_text().strip())
        launched.send_signal(signal.SIGTERM)
        assert launched.wait(timeout=4) == 1
        result = json.loads(receipt.read_text())
        assert result["reason"] == "supervisor_signal"
        assert result["cleanup_complete"]
        assert result["signal_received"] == signal.SIGTERM
        assert descendant not in tool.process_group_rss(result["owned_pgid"])
        assert unrelated.poll() is None
    finally:
        if launched.poll() is None:
            launched.kill()
            launched.wait(timeout=2)
        unrelated.terminate()
        unrelated.wait(timeout=2)
