"""One bounded original-source axis-ten-cover control through the tile kernel.

No target-side mode or parameter overrides exist. The original source is built
only by explicit --source-control dispatch. This checks one clause at theta=0,
not the other six source clauses, H-036, H-102, or any angle neighborhood.
Output files are atomically replaced when explicitly requested; crash durability
and an atomic transaction across both output files are not promised.
"""

from __future__ import annotations

import argparse
import json
import resource
import signal
import subprocess
import sys
import time
from collections import deque
from collections.abc import Sequence
from fractions import Fraction
from pathlib import Path
from typing import Any

from cases.stromquist.restricted_orientation import Point as SourcePoint
from cases.stromquist.restricted_orientation import source_field, source_points
from devtools.angle_tile_certificate import (
    Point,
    RationalPoint,
    Scalar,
    TileSlab,
    certify_nonnegative,
    check_cover,
    closed_tiles,
    membership_polynomials,
)
from sqpack.cover import write_text_atomic
from sqpack.field import FieldElement

WALL_CAP_SECONDS = 10
DEPTH_CAP = 10
LEAF_CAP = 256
PACKET_BYTE_CAP = 262144
ZERO = Fraction(0)


def source_input() -> tuple[FieldElement, tuple[SourcePoint, ...]]:
    """Original s=2+(4/3)sqrt(2), with unchanged sorted K4 ten-set formulas."""
    side, ten, _twelve = source_points(source_field())
    if side != 2 + Fraction(4, 3) * side.field.alpha or len(ten) != 10:
        raise ValueError("original Theorem 3 source identity mismatch")
    if tuple(sorted(ten)) != ten or len(set(ten)) != 10:
        raise ValueError("source labels must be distinct exact lexicographic coordinates")
    return side, ten


def build_cover(side: Scalar, points: tuple[Point, ...]) -> dict[str, Any]:
    """Fixed singleton-slab BFS; toys may call this without source construction.

    Every state retains a complete closed leaf partition, with null labels for
    unresolved leaves. Splits publish a complete replacement dictionary, so an
    alarm between operations cannot erase a boundary or parent from the record.
    First successful labels are retained; failure never means a geometric escape.
    """
    # This tiny check validates the geometry/field preconditions, not coverage.
    # Its result is deliberately unused; point labels may fail on the root tiles.
    check_cover(side, points, (ZERO, ZERO), (TileSlab(ZERO, ZERO, (("0", 0), ("1", 0))),))
    if tuple(sorted(points)) != points:
        raise ValueError("builder points must be in exact lexicographic order")
    leaves: dict[str, int | None] = {"0": None, "1": None}
    pending: deque[str] = deque(("0", "1"))
    cached: dict[tuple[int, RationalPoint], bool] = {}
    trials = 0
    stop_reason = "complete"
    active_path: str | None = None
    try:
        while pending:
            path = pending.popleft()
            active_path = path
            triangle = closed_tiles(tuple(leaves))[path]
            chosen: int | None = None
            for label, point in enumerate(points):
                trials += 1
                succeeds = True
                for vertex in triangle:
                    key = (label, vertex)
                    if key not in cached:
                        cached[key] = all(
                            certify_nonnegative(polynomial, ZERO, ZERO, max_depth=0).proved
                            for polynomial in membership_polynomials(
                                side, point, vertex, ZERO, ZERO
                            )
                        )
                    if not cached[key]:
                        succeeds = False
                        break
                if succeeds:
                    chosen = label
                    break
            if chosen is not None:
                leaves[path] = chosen
            elif len(path) - 1 >= DEPTH_CAP:
                stop_reason = "tile depth cap"
                break
            elif len(leaves) >= LEAF_CAP:
                stop_reason = "leaf cap"
                break
            else:
                replacement = dict(leaves)
                del replacement[path]
                replacement[path + "0"] = None
                replacement[path + "1"] = None
                leaves = replacement
                pending.extend((path + "0", path + "1"))
    except TimeoutError:
        stop_reason = "worker alarm"
    unchecked = sorted(path for path, label in leaves.items() if label is None)
    return {
        "status": "unresolved" if unchecked else "certified",
        "stop_reason": stop_reason,
        "stopped_tile": active_path if unchecked else None,
        "angle_slab": ["0", "0"],
        "leaves": [[path, label] for path, label in sorted(leaves.items())],
        "unchecked_paths": unchecked,
        "point_trials": trials,
        "cached_vertex_checks": len(cached),
        "depth_cap": DEPTH_CAP,
        "leaf_cap": LEAF_CAP,
        "sign_depth": 0,
    }


def run_source() -> dict[str, Any]:
    """Construct and execute the original source once; called only by the worker."""
    started, cpu_started = time.monotonic(), time.process_time()
    side, points = source_input()
    result = build_cover(side, points)
    result.update(
        {
            "kind": "original-source-axis-ten-cover-tiles",
            "container_side": side.text(),
            "ten_points": [[coordinate.text() for coordinate in point] for point in points],
            "scope": "original Theorem 3 axis-ten-cover at theta=0 only",
            "worker_wall_seconds": time.monotonic() - started,
            "worker_cpu_seconds": time.process_time() - cpu_started,
            "h036_outcome": "unresolved",
            "h102_outcome": "unresolved",
        }
    )
    return result


def _expired(_signum: int, _frame: Any) -> None:
    raise TimeoutError("fixed ten-second source cap")


def _unresolved(reason: str) -> dict[str, Any]:
    return {
        "kind": "original-source-axis-ten-cover-tiles",
        "status": "unresolved",
        "stop_reason": reason,
        "h036_outcome": "unresolved",
        "h102_outcome": "unresolved",
    }


def _parse_worker(stdout: str) -> dict[str, Any]:
    if len(stdout.encode()) > PACKET_BYTE_CAP:
        raise ValueError("source packet exceeds 256 KiB")
    if not stdout.strip():
        return _unresolved("worker returned no packet")
    result = json.loads(stdout)
    if type(result) is not dict:
        raise ValueError("worker packet must be an object")
    if result.get("kind") != "original-source-axis-ten-cover-tiles" or result.get(
        "status"
    ) not in (
        "certified",
        "unresolved",
    ):
        raise ValueError("worker packet kind or status is invalid")
    if result.get("h036_outcome") != "unresolved" or result.get("h102_outcome") != "unresolved":
        raise ValueError("worker packet exceeds the source auxiliary scope")
    return result


def _run_child() -> tuple[dict[str, Any], dict[str, Any], int]:
    command = [
        sys.executable,
        "-m",
        "devtools.angle_source_control",
        "--source-control",
        "--worker",
    ]
    before = resource.getrusage(resource.RUSAGE_CHILDREN)
    started = time.monotonic()
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
            result = _parse_worker(stdout)
            if child_exit != 0:
                result["status"] = "unresolved"
            code = 0 if child_exit == 0 and result.get("status") == "certified" else 1
        except (ValueError, TypeError) as error:
            result = _unresolved(f"worker packet refused: {error}")
            code = 2
    except subprocess.TimeoutExpired as error:
        stdout = error.stdout or b""
        stderr = error.stderr or b""
        stdout = stdout.decode() if isinstance(stdout, bytes) else stdout
        stderr = stderr.decode() if isinstance(stderr, bytes) else stderr
        child_exit = None
        result = _unresolved("child process cap")
        code = 1
    after = resource.getrusage(resource.RUSAGE_CHILDREN)
    log = {
        "command": command,
        "child_exit_code": child_exit,
        "parent_exit_code": code,
        "child_wall_cap_seconds": WALL_CAP_SECONDS,
        "process_wall_seconds": time.monotonic() - started,
        "child_cpu_seconds": (after.ru_utime - before.ru_utime)
        + (after.ru_stime - before.ru_stime),
        "stdout": stdout,
        "stderr": stderr,
    }
    result["child_exit_code"] = child_exit
    result["child_wall_cap_seconds"] = WALL_CAP_SECONDS
    return result, log, code


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-control", action="store_true", required=True)
    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--output", type=Path, help="atomically replace this result file")
    parser.add_argument("--log", type=Path, help="atomically replace this execution log")
    args = parser.parse_args(argv)
    if args.worker and (args.output is not None or args.log is not None):
        parser.error("only the parent publishes output files")
    if (
        args.output is not None
        and args.log is not None
        and args.output.resolve() == args.log.resolve()
    ):
        parser.error("result and log paths must differ")
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
            return 0 if result["status"] == "certified" else 1
        result, log, code = _run_child()
        if args.log is not None:
            write_text_atomic(args.log, json.dumps(log, indent=2, sort_keys=True) + "\n")
        if args.output is not None:
            write_text_atomic(args.output, json.dumps(result, indent=2, sort_keys=True) + "\n")
        print(json.dumps(result, sort_keys=True))
    except TimeoutError as error:
        print(json.dumps(_unresolved(str(error)), sort_keys=True))
        return 1
    except (OSError, ValueError, TypeError, KeyError) as error:
        print(f"refused: {error}", file=sys.stderr)
        return 2
    else:
        return code


if __name__ == "__main__":
    raise SystemExit(main())
