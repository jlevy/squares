"""Process memory measurements shared by bounded diagnostic tools."""

from __future__ import annotations

import ctypes
import importlib
import os
import sys
from ctypes import wintypes
from functools import lru_cache
from pathlib import Path


class _MachTimeValue(ctypes.Structure):
    # Apple's task_info.h uses pack(4). Explicit ms layout implements that packing
    # in Python 3.14; this selects memory layout, not a Windows API.
    _layout_ = "ms"
    _pack_ = 4
    _fields_ = [("seconds", ctypes.c_int32), ("microseconds", ctypes.c_int32)]


class _MachTaskBasicInfo(ctypes.Structure):
    _layout_ = "ms"
    _pack_ = 4
    _fields_ = [
        ("virtual_size", ctypes.c_uint64),
        ("resident_size", ctypes.c_uint64),
        ("resident_size_max", ctypes.c_uint64),
        ("user_time", _MachTimeValue),
        ("system_time", _MachTimeValue),
        ("policy", ctypes.c_int32),
        ("suspend_count", ctypes.c_int32),
    ]
    resident_size: int
    resident_size_max: int


@lru_cache(maxsize=1)
def _darwin_api() -> tuple[ctypes.CDLL, ctypes.c_uint32]:
    """Keep the library alive, but retain the live port symbol rather than its value."""
    if ctypes.sizeof(_MachTaskBasicInfo) != 48 or ctypes.alignment(_MachTaskBasicInfo) != 4:
        raise OSError("Darwin task_info layout is unavailable")
    try:
        library = ctypes.CDLL("/usr/lib/libSystem.B.dylib")
        library.task_info.argtypes = [
            ctypes.c_uint32,
            ctypes.c_uint32,
            ctypes.POINTER(_MachTaskBasicInfo),
            ctypes.POINTER(ctypes.c_uint32),
        ]
        library.task_info.restype = ctypes.c_int32
        port = ctypes.c_uint32.in_dll(library, "mach_task_self_")
    except (OSError, AttributeError, ValueError) as error:
        raise OSError("Darwin task_info API is unavailable") from error
    return library, port


def _darwin_memory() -> int:
    library, port = _darwin_api()
    if not port.value:
        raise OSError("Darwin current task port is unavailable")
    value = _MachTaskBasicInfo()
    count = ctypes.c_uint32(ctypes.sizeof(value) // ctypes.sizeof(ctypes.c_uint32))
    result = library.task_info(port.value, 20, ctypes.byref(value), ctypes.byref(count))
    if result != 0 or count.value != 12 or value.resident_size <= 0:
        raise OSError(f"Darwin current RSS query failed: kernel={result}, count={count.value}")
    return int(value.resident_size)


def peak_memory_bytes() -> int:
    """Lifetime peak working set on Windows, or lifetime peak RSS on Unix."""
    if sys.platform != "win32":
        resource = importlib.import_module("resource")
        peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        return int(peak if sys.platform == "darwin" else peak * 1024)

    return _windows_memory()[0]


def _windows_memory() -> tuple[int, int]:
    class Counters(ctypes.Structure):
        _fields_ = [("cb", wintypes.DWORD), ("faults", wintypes.DWORD)] + [
            (name, ctypes.c_size_t)
            for name in ("peak", "working", "pp", "p", "pnp", "np", "page", "peakpage")
        ]

    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    psapi = ctypes.WinDLL("psapi", use_last_error=True)
    kernel.GetCurrentProcess.restype = wintypes.HANDLE
    psapi.GetProcessMemoryInfo.argtypes = [wintypes.HANDLE, ctypes.c_void_p, wintypes.DWORD]
    psapi.GetProcessMemoryInfo.restype = wintypes.BOOL
    value = Counters()
    value.cb = ctypes.sizeof(value)
    if not psapi.GetProcessMemoryInfo(
        kernel.GetCurrentProcess(), ctypes.byref(value), value.cb
    ):
        raise ctypes.WinError(ctypes.get_last_error())
    return int(value.peak), int(value.working)


def current_memory_bytes() -> int:
    """Current resident bytes on Windows/Linux/macOS; unsupported hosts refuse.

    Lifetime peaks are separate reporting evidence, never this guard's input. Darwin
    uses self-only Mach task_info, validated against the system SDK in native CI.
    """
    if sys.platform == "win32":
        return _windows_memory()[1]
    if sys.platform.startswith("linux"):
        resident_pages = int(Path("/proc/self/statm").read_text(encoding="ascii").split()[1])
        return resident_pages * os.sysconf("SC_PAGE_SIZE")
    if sys.platform == "darwin":
        return _darwin_memory()
    raise OSError(f"Current resident memory is unavailable on {sys.platform}")
