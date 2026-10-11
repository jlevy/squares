"""Target-free real process-group controls for bounded POSIX launches."""

from __future__ import annotations

import json
import os
import signal
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

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


def test_timeout_kills_term_ignoring_group(tmp_path: Path) -> None:
    receipt = run(
        tmp_path,
        "import signal,time; signal.signal(signal.SIGTERM,signal.SIG_IGN); "
        "print('ready',flush=True); time.sleep(30)",
        max_seconds=0.2,
    )
    assert receipt["status"] == "INCOMPLETE"
    assert receipt["reason"] == "wall_limit"
    assert receipt["kill_elapsed_seconds"] is not None
    assert receipt["returncode"] == -signal.SIGKILL
    assert receipt["wall_seconds"] < 2
    assert receipt["cleanup_complete"]
    assert "ready" in (tmp_path / "stdout").read_text()


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
