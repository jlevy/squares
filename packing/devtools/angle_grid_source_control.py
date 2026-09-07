"""One fixed-grid original-source axis-ten-cover control through the tile kernel.

The complete 6x3 grid has 36 closed triangles and 432 signed vertex obligations.
The source side, ten-set, labels, singleton angle and ten-second child cap have
no CLI overrides. This is one original-source clause, not H-036, H-102 or a
continuous-angle target. The separate reader must independently replay a proof.
Explicit output paths are atomically replaced; two-file atomicity and crash
durability are not promised. Timers and raw worker output belong only in the log.
"""

from __future__ import annotations

import argparse
import json
import resource
import signal
import subprocess
import sys
import time
from collections.abc import Sequence
from pathlib import Path
from typing import Any

from devtools.angle_source_control import source_input
from devtools.angle_tile_certificate import GridObligation, grid_obligations
from sqpack.cover import write_text_atomic

WALL_CAP_SECONDS = 10
PACKET_BYTE_CAP = 262144
OBLIGATION_COUNT = 432
KIND = "original-source-axis-ten-cover-grid"
ASSIGNMENTS = ((1, 1, 4, 4, 7, 7), (0, 3, 3, 6, 6, 9), (2, 2, 5, 5, 8, 8))


def packet(checked: int, unresolved: list[GridObligation]) -> dict[str, Any]:
    """The fixed eight-key wire object; incomplete work is always unresolved."""
    return {
        "version": 1,
        "kind": KIND,
        "grid": [6, 3],
        "angle_slab": ["0", "0"],
        "assignments": [list(row) for row in ASSIGNMENTS],
        "status": "proved" if checked == OBLIGATION_COUNT and not unresolved else "unresolved",
        "inequalities_checked": checked,
        "unresolved": [list(index) for index in unresolved],
    }


def run_source() -> dict[str, Any]:
    """Execute the fixed original source once, retaining a completed prefix.

    Appending a yielded outcome publishes the count and its truth value together.
    An alarm before that append may omit work, but cannot count unchecked work.
    All failed assigned-point obligations remain unresolved, never escapes.
    """
    completed: list[tuple[GridObligation, bool]] = []
    try:
        side, points = source_input()
        for outcome in grid_obligations(side, points, ASSIGNMENTS):
            # list(iterator) would lose the completed prefix on an alarm.
            completed.append(outcome)  # noqa: PERF402
    except TimeoutError:
        pass
    return packet(len(completed), [index for index, proved in completed if not proved])


def parse_worker(stdout: str) -> dict[str, Any]:
    """Validate our worker's fixed wire shape, not its mathematical conclusion."""
    if len(stdout.encode()) > PACKET_BYTE_CAP:
        raise ValueError("source packet exceeds 256 KiB")
    result = json.loads(stdout)
    if type(result) is not dict or set(result) != set(packet(0, [])):
        raise ValueError("worker packet must have exactly the frozen eight keys")
    if type(result["version"]) is not int or result["version"] != 1:
        raise ValueError("worker version is invalid")
    if result["kind"] != KIND or result["angle_slab"] != ["0", "0"]:
        raise ValueError("worker source or angle identity is invalid")
    if result["grid"] != [6, 3] or any(type(item) is not int for item in result["grid"]):
        raise ValueError("worker grid is invalid")
    assignments = result["assignments"]
    if assignments != [list(row) for row in ASSIGNMENTS] or any(
        type(label) is not int for row in assignments for label in row
    ):
        raise ValueError("worker assignments differ from the frozen source labels")
    checked = result["inequalities_checked"]
    if type(checked) is not int or not 0 <= checked <= OBLIGATION_COUNT:
        raise ValueError("worker completed-prefix count is invalid")
    failures = result["unresolved"]
    if type(failures) is not list or len(failures) > checked:
        raise ValueError("worker unresolved inventory is invalid")
    previous = -1
    for index in failures:
        if (
            type(index) is not list
            or len(index) != 5
            or any(
                type(value) is not int or not 0 <= value < bound
                for value, bound in zip(index, (3, 6, 2, 3, 4), strict=True)
            )
        ):
            raise ValueError("worker unresolved index is invalid")
        row, column, triangle, vertex, axis = index
        ordinal = ((((row * 6 + column) * 2 + triangle) * 3 + vertex) * 4) + axis
        if not previous < ordinal < checked:
            raise ValueError("worker failures must be an ordered subset of the checked prefix")
        previous = ordinal
    if result["status"] not in ("proved", "unresolved") or (
        result["status"] == "proved" and (checked != OBLIGATION_COUNT or failures)
    ):
        raise ValueError("worker status exceeds its completed inventory")
    return result


def _expired(_signum: int, _frame: Any) -> None:
    raise TimeoutError("fixed ten-second grid-source cap")


def _text(value: str | bytes | None) -> str:
    return value.decode(errors="replace") if isinstance(value, bytes) else value or ""


def _run_child() -> tuple[dict[str, Any], dict[str, Any], int]:
    command = [
        sys.executable,
        "-m",
        "devtools.angle_grid_source_control",
        "--source-control",
        "--worker",
    ]
    before = resource.getrusage(resource.RUSAGE_CHILDREN)
    started = time.monotonic()
    note = "complete worker return"
    try:
        process = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
            timeout=WALL_CAP_SECONDS,
        )
        stdout, stderr, child_exit = process.stdout, process.stderr, process.returncode
        try:
            result = parse_worker(stdout)
            if child_exit != 0:
                result["status"] = "unresolved"
            code = 0 if child_exit == 0 and result["status"] == "proved" else 1
        except (ValueError, TypeError) as error:
            result, code = packet(0, []), 2
            note = f"worker packet refused: {error}"
    except subprocess.TimeoutExpired as error:
        stdout, stderr, child_exit = _text(error.stdout), _text(error.stderr), None
        result, code = packet(0, []), 1
        note = "child process cap; no complete worker packet retained"
    after = resource.getrusage(resource.RUSAGE_CHILDREN)
    log = {
        "command": command,
        "child_exit_code": child_exit,
        "parent_exit_code": code,
        "child_wall_cap_seconds": WALL_CAP_SECONDS,
        "process_wall_seconds": time.monotonic() - started,
        "child_cpu_seconds": after.ru_utime
        - before.ru_utime
        + after.ru_stime
        - before.ru_stime,
        "note": note,
        "stdout": stdout,
        "stderr": stderr,
    }
    return result, log, code


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-control", action="store_true", required=True)
    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--output", type=Path, help="atomically replace this proof packet")
    parser.add_argument("--log", type=Path, help="atomically replace this execution log")
    args = parser.parse_args(argv)
    if args.worker and (args.output is not None or args.log is not None):
        parser.error("only the parent publishes output files")
    if (
        args.output is not None
        and args.log is not None
        and args.output.resolve() == args.log.resolve()
    ):
        parser.error("packet and log paths must differ")
    try:
        if args.worker:
            previous = signal.signal(signal.SIGALRM, _expired)
            signal.alarm(WALL_CAP_SECONDS)
            try:
                result = run_source()
            finally:
                signal.alarm(0)
                signal.signal(signal.SIGALRM, previous)
            print(json.dumps(result, sort_keys=True))
            return 0 if result["status"] == "proved" else 1
        result, log, code = _run_child()
        if args.log is not None:
            write_text_atomic(args.log, json.dumps(log, indent=2, sort_keys=True) + "\n")
        if args.output is not None:
            write_text_atomic(args.output, json.dumps(result, indent=2, sort_keys=True) + "\n")
        print(json.dumps(result, sort_keys=True))
    except TimeoutError:
        print(json.dumps(packet(0, []), sort_keys=True))
        return 1
    except (OSError, ValueError, TypeError) as error:
        print(f"refused: {error}", file=sys.stderr)
        return 2
    else:
        return code


if __name__ == "__main__":
    raise SystemExit(main())
