"""Current guards and historical peak reporting remain distinct in a reused process."""

# pyright: reportPrivateUsage=false
# ruff: noqa: SLF001 -- Native ABI and failure-path controls inspect the platform adapter.

from __future__ import annotations

import ctypes
import errno
import json
import os
import subprocess
import sys
from textwrap import dedent
from types import SimpleNamespace
from typing import Any

import pytest

from devtools import process_memory as memory
from devtools.process_memory import current_memory_bytes, peak_memory_bytes

CURRENT_RSS_HOSTS = {"linux", "win32", "darwin"}
requires_current_rss = pytest.mark.skipif(
    sys.platform not in CURRENT_RSS_HOSTS,
    reason="current RSS is measured on Linux, Windows and macOS",
)


def test_ungated_platform_refuses_current_memory(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(sys, "platform", "unsupported")
    with pytest.raises(OSError, match="unavailable on unsupported"):
        current_memory_bytes()


@pytest.mark.parametrize("received", [0, 95, 96])
def test_darwin_native_bytes_and_failed_or_short_reads(
    monkeypatch: pytest.MonkeyPatch, received: int
) -> None:
    def pidinfo(pid: int, flavor: int, arg: int, buffer: Any, size: int) -> int:
        assert pid > 0
        assert flavor == 4
        assert arg == 0
        assert size == 96
        value = ctypes.cast(buffer, ctypes.POINTER(memory._DarwinTaskInfo)).contents
        value.resident_size = 123456789
        ctypes.set_errno(errno.EPERM)
        return received

    monkeypatch.setattr(sys, "platform", "darwin")
    monkeypatch.setattr(
        memory, "_darwin_libproc", lambda: SimpleNamespace(proc_pidinfo=pidinfo)
    )
    if received == 96:
        assert current_memory_bytes() == 123456789
    else:
        with pytest.raises(OSError, match=f"returned {received}/96 bytes") as failure:
            current_memory_bytes()
        assert failure.value.errno == errno.EPERM


def test_darwin_native_load_failure_is_explicit(monkeypatch: pytest.MonkeyPatch) -> None:
    def unavailable() -> ctypes.CDLL:
        raise OSError("native library unavailable")

    monkeypatch.setattr(sys, "platform", "darwin")
    monkeypatch.setattr(memory, "_darwin_libproc", unavailable)
    with pytest.raises(OSError, match="native library unavailable"):
        current_memory_bytes()


@requires_current_rss
def test_live_memory_sample_is_positive() -> None:
    assert current_memory_bytes() > 0
    assert peak_memory_bytes() > 0


@requires_current_rss
def test_released_allocation_does_not_leave_current_memory_above_guard() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            dedent("""
            import gc
            import json
            import mmap
            import sys
            from devtools.process_memory import current_memory_bytes, peak_memory_bytes
            baseline = current_memory_bytes()
            threshold = baseline + 48 * 1024**2
            # macOS malloc may retain a freed bytearray's pages; munmap really releases them.
            allocation = (mmap.mmap(-1, 96 * 1024**2) if sys.platform == "darwin"
                          else bytearray(96 * 1024**2))
            for i in range(0, len(allocation), 4096):
                allocation[i] = 1
            live = current_memory_bytes()
            if isinstance(allocation, mmap.mmap):
                allocation.close()
            del allocation
            gc.collect()
            print(json.dumps(dict(threshold=threshold, live=live,
                                  current=current_memory_bytes(), peak=peak_memory_bytes())))
        """),
        ],
        text=True,
        capture_output=True,
        check=True,
        timeout=15,
    )
    sample = json.loads(result.stdout)
    assert sample["live"] > sample["threshold"]
    assert sample["peak"] > sample["threshold"]
    assert sample["current"] < sample["threshold"]


@pytest.mark.skipif(sys.platform != "darwin", reason="independent macOS ps RSS control")
def test_darwin_current_memory_agrees_with_external_ps() -> None:
    before = current_memory_bytes()
    result = subprocess.run(
        ["/bin/ps", "-o", "rss=", "-p", str(os.getpid())],
        text=True,
        capture_output=True,
        check=True,
        timeout=5,
    )
    external = int(result.stdout.strip()) * 1024
    after = current_memory_bytes()
    # ps rounds to KiB and the parent may allocate while launching the subprocess.
    assert min(before, after) - 8 * 1024**2 <= external <= max(before, after) + 8 * 1024**2
