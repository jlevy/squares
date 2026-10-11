"""Run one owned POSIX process group with sampled current-RSS and wall ceilings.

Children must remain in the launched group. Sampling is not an allocation-time guard;
processes deliberately escaping the session are outside this instrument's contract.
"""

from __future__ import annotations

import argparse
import math
import os
import signal
import subprocess
import sys
import threading
import time
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import Any

from sqpack import retained_json


def process_group_rss(pgid: int) -> dict[int, int]:
    """Current ps RSS (KiB converted to bytes), excluding terminated zombies."""
    table = subprocess.run(
        ["/bin/ps", "-axo", "pid=,pgid=,rss=,stat="],
        capture_output=True,
        text=True,
        check=True,
        timeout=1,
    ).stdout
    found: dict[int, int] = {}
    for line in table.splitlines():
        fields = line.split()
        if len(fields) != 4:
            raise OSError("ps returned malformed process/RSS data")
        pid, group, kib = map(int, fields[:3])
        if kib < 0:
            raise OSError("ps returned negative current RSS")
        if group == pgid and not fields[3].startswith("Z"):
            found[pid] = kib * 1024
    return found


def _signal_group(pgid: int, sig: signal.Signals) -> None:
    try:
        os.killpg(pgid, sig)
    except ProcessLookupError:
        pass
    except PermissionError:
        # Darwin can report EPERM for a just-killed group containing only zombies.
        # A live group remains a genuine failure; never suppress a denied signal to it.
        if process_group_rss(pgid):
            raise


def supervise(
    argv: Sequence[str],
    *,
    max_seconds: float,
    max_memory_mib: float,
    sample_seconds: float,
    stdout: Path,
    stderr: Path,
    cleanup_seconds: float = 10,
    sampler: Callable[[int], dict[int, int]] = process_group_rss,
) -> dict[str, Any]:
    """Own exactly one group, terminate/reap it, and retain small custody evidence."""
    if os.name != "posix":
        raise ValueError("POSIX process groups are required")
    if not argv or any(
        not math.isfinite(value) or value <= 0
        for value in (max_seconds, max_memory_mib, sample_seconds, cleanup_seconds)
    ):
        raise ValueError("argv and finite positive ceilings are required")
    # Refuse unavailable/invalid guards before launching anything.
    if os.getpid() not in sampler(os.getpgrp()):
        raise OSError("current-RSS guard cannot observe the supervisor")
    stdout.parent.mkdir(parents=True, exist_ok=True)
    stderr.parent.mkdir(parents=True, exist_ok=True)
    interrupted: list[int] = []

    def receive(sig: int, _frame: Any) -> None:
        interrupted.append(sig)

    prior = {sig: signal.getsignal(sig) for sig in (signal.SIGTERM, signal.SIGINT)}
    for sig in prior:
        signal.signal(sig, receive)
    started = time.monotonic()
    child: subprocess.Popen[bytes] | None = None
    reason = "normal_exit"
    failure: str | None = None
    maxima: dict[int, int] = {}
    samples = 0
    term_at: float | None = None
    kill_at: float | None = None
    cleanup_complete = False
    timers: list[threading.Timer] = []
    try:
        with stdout.open("wb") as out, stderr.open("wb") as err:
            child = subprocess.Popen(list(argv), stdout=out, stderr=err, start_new_session=True)
            pgid = child.pid

            def wall_term() -> None:
                nonlocal term_at
                term_at = time.monotonic() - started
                _signal_group(pgid, signal.SIGTERM)

            def wall_kill() -> None:
                nonlocal kill_at
                kill_at = time.monotonic() - started
                _signal_group(pgid, signal.SIGKILL)

            # A stalled ps sample cannot postpone the scientific TERM/KILL clock.
            for deadline, callback in (
                (max_seconds, wall_term),
                (max_seconds + cleanup_seconds, wall_kill),
            ):
                timer = threading.Timer(
                    max(0, deadline - (time.monotonic() - started)), callback
                )
                timers.append(timer)
                timer.start()
            while True:
                now = time.monotonic()
                if interrupted:
                    reason = "supervisor_signal"
                    break
                if now - started >= max_seconds:
                    reason = "wall_limit"
                    break
                try:
                    members = sampler(pgid)
                except (OSError, ValueError, subprocess.SubprocessError) as error:
                    reason, failure = "guard_unavailable", str(error)
                    break
                samples += 1
                for pid, rss in members.items():
                    maxima[pid] = max(maxima.get(pid, 0), rss)
                if any(rss > max_memory_mib * 1024**2 for rss in members.values()):
                    reason = "memory_limit"
                    break
                if child.poll() is not None:
                    break
                time.sleep(
                    min(sample_seconds, max(0, started + max_seconds - time.monotonic()))
                )
            # Even a normally exiting leader may leave live children in its group.
            if term_at is None:
                term_at = time.monotonic() - started
            _signal_group(pgid, signal.SIGTERM)
            cleanup_deadline = started + term_at + cleanup_seconds
            while time.monotonic() < cleanup_deadline:
                child.poll()
                try:
                    if not sampler(pgid):
                        cleanup_complete = True
                        break
                except (OSError, ValueError, subprocess.SubprocessError) as error:
                    failure = str(error)
                    break
                time.sleep(min(0.05, max(0, cleanup_deadline - time.monotonic())))
            if not cleanup_complete:
                kill_at = time.monotonic() - started
                _signal_group(pgid, signal.SIGKILL)
            child.wait(timeout=2)
            try:
                cleanup_complete = not sampler(pgid)
            except (OSError, ValueError, subprocess.SubprocessError) as error:
                failure = str(error)
    finally:
        for timer in timers:
            timer.cancel()
        for timer in timers:
            timer.join()
        if child is not None and child.poll() is None:
            _signal_group(child.pid, signal.SIGKILL)
            child.wait(timeout=2)
        for sig, handler in prior.items():
            signal.signal(sig, handler)
    assert child is not None
    return {
        "schema": "posix-bounded-command-supervision/v1",
        "status": "COMPLETED"
        if reason == "normal_exit" and cleanup_complete and failure is None
        else "INCOMPLETE",
        "reason": reason,
        "failure": failure,
        "argv": list(argv),
        "pid": child.pid,
        "owned_pgid": child.pid,
        "returncode": child.returncode,
        "signal_received": interrupted[0] if interrupted else None,
        "wall_seconds": time.monotonic() - started,
        "max_seconds": max_seconds,
        "cleanup_seconds": cleanup_seconds,
        "max_memory_mib_per_process": max_memory_mib,
        "sample_seconds": sample_seconds,
        "samples": samples,
        "maximum_sampled_current_rss_bytes_by_pid": maxima,
        "rss_source": "/bin/ps RSS KiB; current resident bytes, not lifetime peak",
        "rss_enforcement": (
            "sampled per live process in owned group; not allocation-time hardcap"
        ),
        "term_elapsed_seconds": term_at,
        "kill_elapsed_seconds": kill_at,
        "cleanup_complete": cleanup_complete,
        "stdout": str(stdout.resolve()),
        "stderr": str(stderr.resolve()),
        "scope": "one owned process group; children must not escape it",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-seconds", type=float, required=True)
    parser.add_argument("--max-memory-mib", type=float, default=4096)
    parser.add_argument("--sample-seconds", type=float, default=1)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--stdout", type=Path)
    parser.add_argument("--stderr", type=Path)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args(argv)
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    try:
        result = supervise(
            command,
            max_seconds=args.max_seconds,
            max_memory_mib=args.max_memory_mib,
            sample_seconds=args.sample_seconds,
            stdout=args.stdout or args.output.with_suffix(".stdout.log"),
            stderr=args.stderr or args.output.with_suffix(".stderr.log"),
        )
    except (ValueError, OSError, subprocess.SubprocessError) as error:
        result = {
            "schema": "posix-bounded-command-supervision/v1",
            "status": "REFUSED",
            "reason": str(error),
        }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(retained_json.dumps(result))
    return 0 if result.get("status") == "COMPLETED" and result.get("returncode") == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
