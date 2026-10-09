"""Current guards and historical peak reporting remain distinct in a reused process."""

# These SDK and refusal controls intentionally inspect the private FFI boundary.
# ruff: noqa: SLF001
# pyright: reportPrivateUsage=false

from __future__ import annotations

import ctypes
import json
import os
import subprocess
import sys
from pathlib import Path
from textwrap import dedent
from types import SimpleNamespace
from typing import Any

import pytest

from devtools import process_memory as memory
from devtools.process_memory import current_memory_bytes, peak_memory_bytes
from sqpack.yamlio import safe_load

CURRENT_RSS_HOSTS = {"linux", "win32", "darwin"}
requires_current_rss = pytest.mark.skipif(
    sys.platform not in CURRENT_RSS_HOSTS,
    reason="current RSS supports Linux, Windows and Darwin; other hosts refuse",
)


def test_ungated_platform_refuses_current_memory(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(sys, "platform", "unsupported-test-host")
    with pytest.raises(OSError, match="unavailable on unsupported-test-host"):
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
            import mmap
            import json
            from devtools.process_memory import current_memory_bytes, peak_memory_bytes
            baseline = current_memory_bytes()
            threshold = baseline + 48 * 1024**2
            allocation = mmap.mmap(-1, 96 * 1024**2)
            for i in range(0, len(allocation), 4096):
                allocation[i] = 1
            live = current_memory_bytes()
            allocation.close()
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


def test_mach_packed_layout_is_explicit() -> None:
    assert memory._MachTimeValue._layout_ == "ms"
    assert memory._MachTaskBasicInfo._layout_ == "ms"
    assert ctypes.sizeof(memory._MachTimeValue) == 8
    assert ctypes.alignment(memory._MachTimeValue) == 4
    assert ctypes.sizeof(memory._MachTaskBasicInfo) == 48
    assert ctypes.alignment(memory._MachTaskBasicInfo) == 4


@pytest.mark.parametrize(
    ("result", "count", "resident"), [(5, 12, 100), (0, 11, 100), (0, 12, 0)]
)
def test_mach_failed_query_never_substitutes_peak(
    monkeypatch: pytest.MonkeyPatch, result: int, count: int, resident: int
) -> None:
    def query(_port: int, _flavor: int, value: Any, returned: Any) -> int:
        ctypes.cast(
            value, ctypes.POINTER(memory._MachTaskBasicInfo)
        ).contents.resident_size = resident
        ctypes.cast(returned, ctypes.POINTER(ctypes.c_uint32)).contents.value = count
        return result

    monkeypatch.setattr(
        memory, "_darwin_api", lambda: (SimpleNamespace(task_info=query), ctypes.c_uint32(10))
    )
    with pytest.raises(OSError, match="query failed"):
        memory._darwin_memory()


def test_mach_reads_live_port_and_current_field(monkeypatch: pytest.MonkeyPatch) -> None:
    ports = []
    port = ctypes.c_uint32(10)

    def query(task: int, flavor: int, value: Any, _count: Any) -> int:
        assert flavor == 20
        ports.append(task)
        info = ctypes.cast(value, ctypes.POINTER(memory._MachTaskBasicInfo)).contents
        info.resident_size = 100
        info.resident_size_max = 1000
        return 0

    monkeypatch.setattr(memory, "_darwin_api", lambda: (SimpleNamespace(task_info=query), port))
    assert memory._darwin_memory() == 100
    port.value = 20
    assert memory._darwin_memory() == 100
    assert ports == [10, 20]
    port.value = 0
    with pytest.raises(OSError, match="task port"):
        memory._darwin_memory()


def test_missing_mach_library_refuses(monkeypatch: pytest.MonkeyPatch) -> None:
    def unavailable(_name: str) -> None:
        raise OSError("no library")

    memory._darwin_api.cache_clear()
    monkeypatch.setattr(ctypes, "CDLL", unavailable)
    with pytest.raises(OSError, match="API is unavailable"):
        memory._darwin_api()
    memory._darwin_api.cache_clear()


def _field_offset(structure: type[ctypes.Structure], name: str) -> int:
    return int(getattr(structure, name).offset)


@pytest.mark.skipif(
    sys.platform != "darwin", reason="requires a real Darwin host and system SDK"
)
def test_darwin_sdk_layout_and_independent_rss(tmp_path: Path) -> None:
    """The SDK, not another Python declaration, supplies the native ABI oracle."""
    source = tmp_path / "layout.c"
    executable = tmp_path / "layout"
    source.write_text(
        dedent("""
        #include <mach/mach.h>
        #include <stddef.h>
        #include <stdio.h>
        int main(void) {
            printf("%zu %zu %u %u %zu %zu %zu %zu %zu %zu %zu %zu %zu %zu %zu\\n",
                sizeof(mach_task_basic_info_data_t), _Alignof(mach_task_basic_info_data_t),
                (unsigned)MACH_TASK_BASIC_INFO, (unsigned)MACH_TASK_BASIC_INFO_COUNT,
                offsetof(mach_task_basic_info_data_t, virtual_size),
                offsetof(mach_task_basic_info_data_t, resident_size),
                offsetof(mach_task_basic_info_data_t, resident_size_max),
                offsetof(mach_task_basic_info_data_t, user_time),
                offsetof(mach_task_basic_info_data_t, system_time),
                offsetof(mach_task_basic_info_data_t, policy),
                offsetof(mach_task_basic_info_data_t, suspend_count),
                sizeof(time_value_t), _Alignof(time_value_t), offsetof(time_value_t, seconds),
                offsetof(time_value_t, microseconds));
            return 0;
        }
    """),
        encoding="utf-8",
    )
    subprocess.run(
        ["/usr/bin/xcrun", "clang", "-std=c11", str(source), "-o", str(executable)],
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
        "resident_size_max",
        "user_time",
        "system_time",
        "policy",
        "suspend_count",
    )
    offsets = [_field_offset(memory._MachTaskBasicInfo, name) for name in fields]
    assert abi == [
        ctypes.sizeof(memory._MachTaskBasicInfo),
        ctypes.alignment(memory._MachTaskBasicInfo),
        20,
        12,
        *offsets,
        ctypes.sizeof(memory._MachTimeValue),
        ctypes.alignment(memory._MachTimeValue),
        _field_offset(memory._MachTimeValue, "seconds"),
        _field_offset(memory._MachTimeValue, "microseconds"),
    ]
    before = current_memory_bytes()
    value = subprocess.run(
        ["/bin/ps", "-o", "rss=", "-p", str(os.getpid())],
        capture_output=True,
        text=True,
        check=True,
        timeout=15,
    )
    after = current_memory_bytes()
    independent = int(value.stdout.strip()) * 1024
    margin = 8 * 1024**2  # Frozen allowance for small interpreter activity/page rounding.
    assert independent > 0
    assert min(before, after) - margin <= independent <= max(before, after) + margin
    print(
        json.dumps(
            {"ABI": abi, "before": before, "ps": independent, "after": after, "margin": margin}
        )
    )


def test_macos_native_memory_step_is_bounded_and_requires_three_real_cases() -> None:
    path = Path(__file__).resolve().parents[2] / ".github/workflows/packing-validation.yml"
    job = safe_load(path.read_text(encoding="utf-8"))["jobs"]["macos-portability"]
    assert job["timeout-minutes"] == 5
    assert job["if"] == "github.event_name != 'pull_request' || github.base_ref == 'main'"
    step = next(
        item
        for item in job["steps"]
        if item["name"] == "Native Darwin current memory and system SDK layout"
    )
    assert step["timeout-minutes"] == 1
    for name in (
        "test_live_memory_sample_is_positive",
        "test_released_allocation_does_not_leave_current_memory_above_guard",
        "test_darwin_sdk_layout_and_independent_rss",
    ):
        assert f"tests/test_process_memory.py::{name}" in step["run"]
    assert '"skipped"' in step["run"]
    assert "==3" in step["run"]
