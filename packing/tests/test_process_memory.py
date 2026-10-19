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
from pathlib import Path
from textwrap import dedent
from types import SimpleNamespace
from typing import Any
from unittest.mock import Mock

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


@pytest.mark.parametrize("received", [-1, 0, 95, 96, 97])
def test_darwin_native_bytes_and_failed_or_short_reads(
    monkeypatch: pytest.MonkeyPatch, received: int
) -> None:
    def pidinfo(pid: int, flavor: int, arg: int, buffer: Any, size: int) -> int:
        assert pid > 0
        assert flavor == 4
        assert arg == 0
        assert size == 96
        value = ctypes.cast(buffer, ctypes.POINTER(memory._DarwinTaskInfo)).contents
        value.resident_size = 2**40 + 37
        ctypes.set_errno(errno.EPERM)
        return received

    monkeypatch.setattr(sys, "platform", "darwin")
    monkeypatch.setattr(
        memory, "_darwin_libproc", lambda: SimpleNamespace(proc_pidinfo=pidinfo)
    )
    if received == 96:
        assert current_memory_bytes() == 2**40 + 37
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


@pytest.mark.parametrize("missing_symbol", [False, True])
def test_darwin_loader_failures_are_oserrors(
    monkeypatch: pytest.MonkeyPatch, *, missing_symbol: bool
) -> None:
    error = OSError(errno.ENOENT, "native library unavailable")
    loader = Mock(return_value=SimpleNamespace()) if missing_symbol else Mock(side_effect=error)
    monkeypatch.setattr(ctypes, "CDLL", loader)
    memory._darwin_libproc.cache_clear()
    try:
        with pytest.raises(
            OSError, match=r"proc_pidinfo|native library unavailable"
        ) as failure:
            memory._darwin_libproc()
        if not missing_symbol:
            assert failure.value is error
    finally:
        memory._darwin_libproc.cache_clear()


def test_darwin_loader_caches_library_but_not_pid_buffer_or_measurement(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    buffers: list[Any] = []
    pids: list[int] = []

    def pidinfo(pid: int, flavor: int, arg: int, buffer: Any, size: int) -> int:
        pids.append(pid)
        buffers.append(buffer)  # Keep both native allocations alive for the ownership check.
        assert (flavor, arg, size) == (4, 0, ctypes.sizeof(memory._DarwinTaskInfo))
        value = ctypes.cast(buffer, ctypes.POINTER(memory._DarwinTaskInfo)).contents
        assert value.resident_size == 0
        value.virtual_size = 2**44
        value.resident_size = 2**40 + pid
        return size

    query = Mock(side_effect=pidinfo)
    library = SimpleNamespace(proc_pidinfo=query)
    loader = Mock(return_value=library)
    monkeypatch.setattr(ctypes, "CDLL", loader)
    process_ids = iter((1234, 5678))
    monkeypatch.setattr(os, "getpid", lambda: next(process_ids))
    memory._darwin_libproc.cache_clear()
    try:
        assert memory._darwin_current_memory() == 2**40 + 1234
        assert memory._darwin_current_memory() == 2**40 + 5678
        loader.assert_called_once_with("/usr/lib/libproc.dylib", use_errno=True)
        assert query.argtypes == [
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_uint64,
            ctypes.c_void_p,
            ctypes.c_int,
        ]
        assert query.restype is ctypes.c_int
        assert pids == [1234, 5678]
        assert (
            ctypes.cast(buffers[0], ctypes.c_void_p).value
            != ctypes.cast(buffers[1], ctypes.c_void_p).value
        )
    finally:
        memory._darwin_libproc.cache_clear()


def test_darwin_failed_read_clears_stale_errno(monkeypatch: pytest.MonkeyPatch) -> None:
    def pidinfo(_pid: int, _flavor: int, _arg: int, _buffer: Any, _size: int) -> int:
        assert ctypes.get_errno() == 0
        return 0

    monkeypatch.setattr(
        memory, "_darwin_libproc", lambda: SimpleNamespace(proc_pidinfo=pidinfo)
    )
    ctypes.set_errno(errno.EPERM)
    with pytest.raises(OSError, match="no native error reported") as failure:
        memory._darwin_current_memory()
    assert failure.value.errno == 0


def test_darwin_zero_resident_memory_refuses(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        memory,
        "_darwin_libproc",
        lambda: SimpleNamespace(
            proc_pidinfo=lambda *_args: ctypes.sizeof(memory._DarwinTaskInfo)
        ),
    )
    with pytest.raises(OSError, match="no current resident memory"):
        memory._darwin_current_memory()


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
    print(json.dumps(sample))


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
    print(json.dumps({"before": before, "ps": external, "after": after}))


@pytest.mark.skipif(sys.platform != "darwin", reason="requires installed Darwin system SDK")
def test_darwin_sdk_layout_and_signature(tmp_path: Path) -> None:
    """Adapted from Guzhou0806's PR407 SDK oracle; the installed headers own the ABI."""
    source = tmp_path / "layout.c"
    executable = tmp_path / "layout"
    source.write_text(
        dedent("""
        #include <libproc.h>
        #include <sys/proc_info.h>
        #include <stddef.h>
        #include <stdint.h>
        #include <stdio.h>
        _Static_assert(_Generic(&proc_pidinfo,
            int (*)(int, int, uint64_t, void *, int): 1, default: 0),
            "proc_pidinfo signature disagrees with ctypes binding");
        #define FIELD(name) printf("%zu %zu ", offsetof(struct proc_taskinfo, pti_##name), \
            sizeof(((struct proc_taskinfo *)0)->pti_##name))
        int main(void) {
            printf("%zu %zu %d %zu ", sizeof(struct proc_taskinfo),
                _Alignof(struct proc_taskinfo), PROC_PIDTASKINFO,
                (size_t)PROC_PIDTASKINFO_SIZE);
            FIELD(virtual_size); FIELD(resident_size);
            FIELD(total_user); FIELD(total_system);
            FIELD(threads_user); FIELD(threads_system);
            FIELD(policy); FIELD(faults); FIELD(pageins); FIELD(cow_faults);
            FIELD(messages_sent); FIELD(messages_received);
            FIELD(syscalls_mach); FIELD(syscalls_unix); FIELD(csw);
            FIELD(threadnum); FIELD(numrunning); FIELD(priority);
            return 0;
        }
        """),
        encoding="utf-8",
    )
    subprocess.run(
        [
            "/usr/bin/xcrun",
            "clang",
            "-std=c11",
            "-Wall",
            "-Wextra",
            "-Werror",
            str(source),
            "-o",
            str(executable),
        ],
        capture_output=True,
        text=True,
        check=True,
        timeout=15,
    )
    result = subprocess.run(
        [str(executable)], capture_output=True, text=True, check=True, timeout=15
    )
    abi = [int(value) for value in result.stdout.split()]
    fields = (
        "virtual_size",
        "resident_size",
        "total_user",
        "total_system",
        "threads_user",
        "threads_system",
        "policy",
        "faults",
        "pageins",
        "cow_faults",
        "messages_sent",
        "messages_received",
        "syscalls_mach",
        "syscalls_unix",
        "csw",
        "threadnum",
        "numrunning",
        "priority",
    )
    expected = [
        ctypes.sizeof(memory._DarwinTaskInfo),
        ctypes.alignment(memory._DarwinTaskInfo),
        4,
        ctypes.sizeof(memory._DarwinTaskInfo),
    ]
    for name in fields:
        field = getattr(memory._DarwinTaskInfo, name)
        expected.extend((int(field.offset), int(field.size)))
    assert abi == expected
    print(json.dumps({"proc_taskinfo_abi": abi}))
