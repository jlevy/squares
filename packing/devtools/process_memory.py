"""Process memory measurements shared by bounded diagnostic tools."""

from __future__ import annotations

import ctypes
import importlib
import os
import sys
from ctypes import wintypes
from functools import cache
from pathlib import Path


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


class _DarwinTaskInfo(ctypes.Structure):
    """Native proc_taskinfo ABI from Apple's <sys/proc_info.h>."""

    _fields_ = [
        (name, ctypes.c_uint64)
        for name in (
            "virtual_size",
            "resident_size",
            "total_user",
            "total_system",
            "threads_user",
            "threads_system",
        )
    ] + [
        (name, ctypes.c_int32)
        for name in (
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
    ]


@cache
def _darwin_libproc() -> ctypes.CDLL:
    library = ctypes.CDLL("/usr/lib/libproc.dylib", use_errno=True)
    library.proc_pidinfo.argtypes = [
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_uint64,
        ctypes.c_void_p,
        ctypes.c_int,
    ]
    library.proc_pidinfo.restype = ctypes.c_int
    return library


def _darwin_current_memory() -> int:
    value = _DarwinTaskInfo()
    size = ctypes.sizeof(value)
    ctypes.set_errno(0)
    # PROC_PIDTASKINFO = 4 in Apple's <sys/proc_info.h>.
    received = _darwin_libproc().proc_pidinfo(os.getpid(), 4, 0, ctypes.byref(value), size)
    if received != size:
        error = ctypes.get_errno()
        detail = os.strerror(error) if error else "no native error reported"
        raise OSError(error, f"proc_pidinfo returned {received}/{size} bytes: {detail}")
    resident = int(value.resident_size)
    if resident <= 0:
        raise OSError("proc_pidinfo returned no current resident memory")
    return resident


def current_memory_bytes() -> int:
    """Current resident bytes on Windows/Linux/macOS; other hosts fail explicitly.

    Lifetime peaks are separate reporting evidence, never this guard's input. macOS
    uses libproc's resident-size field in bytes, not physical footprint or peak RSS.
    """
    if sys.platform == "win32":
        return _windows_memory()[1]
    if sys.platform.startswith("linux"):
        resident_pages = int(Path("/proc/self/statm").read_text(encoding="ascii").split()[1])
        return resident_pages * os.sysconf("SC_PAGE_SIZE")
    if sys.platform == "darwin":
        return _darwin_current_memory()
    raise OSError(f"Current resident memory is unavailable on {sys.platform}")
