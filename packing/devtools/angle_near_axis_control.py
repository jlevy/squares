"""Fixed-side near-axis P10 coverage on a complete closed 6x3 center grid.

Target geometry is constructed only by explicit --target-near-axis dispatch.
The four Theorem 3 seeds are evaluated at q=1939/500, not scaled from the
original algebraic side: cases/stromquist/restricted_orientation.py:point_sets.
Both closed half-angle slabs [-T,0] and [0,T] use the same fixed source-grid
labels, 36 triangles each, and unsplit Bernstein certificates (864 inequalities).

Here x+=11/5040 and T=x+/(1-x+^2/2). The bounds pi<22/7, sin(x)<=x and
cos(x)>=1-x^2/2>0 give tan(pi/1440)<T. Thus a proof covers the actual closed
+/-0.25-degree angle neighborhood; a failure in the added sliver is not a
counterexample. Any failed label or sign certificate is unresolved, not an escape.
This is one auxiliary clause, never H-036, H-102 or the seven-clause theorem.
Acceptance needs a separately implemented continuous reader and prospective run.

Design: campaign/series/series-000-smoke-and-calibration/results/agenda-026/
bc-255-angle-instrument-design.md, "Next Allocation After H-104".
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
from fractions import Fraction
from pathlib import Path
from typing import Any

from devtools.angle_tile_certificate import RationalPoint, grid_obligations
from sqpack.cover import write_text_atomic

type Failure = tuple[int, int, int, int, int, int]

ZERO = Fraction(0)
SIDE = Fraction(1939, 500)
OUTER_ARGUMENT = Fraction(11, 5040)
T = OUTER_ARGUMENT / (1 - OUTER_ARGUMENT**2 / 2)
SLABS = ((-T, ZERO), (ZERO, T))
ASSIGNMENTS = ((1, 1, 4, 4, 7, 7), (0, 3, 3, 6, 6, 9), (2, 2, 5, 5, 8, 8))
KIND = "fixed-side-near-axis-ten-cover-grid"
OBLIGATION_COUNT = 864
WALL_CAP_SECONDS = 10
PACKET_BYTE_CAP = 262144


def ten_set(side: Fraction) -> tuple[RationalPoint, ...]:
    """Evaluate the unchanged four seeds and K4 reflections, including for toys."""
    if (
        type(side) is not Fraction
        or max(side.numerator.bit_length(), side.denominator.bit_length()) > 2048
    ):
        raise ValueError("a bounded exact Fraction side is required")
    one = Fraction(1)
    seeds = (
        (one, one),
        (side / 2, one),
        (Fraction(3, 2) - side / 4, side / 2),
        (Fraction(1, 2) + side / 4, side / 2),
    )
    points = {
        (side - x if flip_x else x, side - y if flip_y else y)
        for x, y in seeds
        for flip_x in (False, True)
        for flip_y in (False, True)
    }
    if side <= 1 or len(points) != 10:
        raise ValueError("the formula source must give ten points and a positive center width")
    return tuple(sorted(points))


def target_input() -> tuple[Fraction, tuple[RationalPoint, ...]]:
    """Construct the fixed target only after explicit future experiment dispatch."""
    return SIDE, ten_set(SIDE)


def packet(
    checked: int, failures: list[Failure], *, interrupted: bool = False
) -> dict[str, Any]:
    """Fixed identity and a completed prefix; no coefficients or target-chosen labels."""
    return {
        "version": 1,
        "kind": KIND,
        "side": str(SIDE),
        "grid": [6, 3],
        "half_angle_slabs": [[str(low), str(high)] for low, high in SLABS],
        "assignments": [list(row) for row in ASSIGNMENTS],
        "status": "proved"
        if checked == OBLIGATION_COUNT and not failures and not interrupted
        else "unresolved",
        "inequalities_checked": checked,
        "unresolved": [list(index) for index in failures],
    }


def run_target() -> dict[str, Any]:
    """Explicit worker body; never used by source controls without a mocked input.

    Each append publishes a completed inequality and its truth value together.
    The canonical prefix is slab, row, column, triangle, vertex, then signed axis.
    No subdivision, label search, skipped failures or altered range is permitted.
    """
    completed: list[tuple[Failure, bool]] = []
    interrupted = False
    try:
        side, points = target_input()
        for slab, (low, high) in enumerate(SLABS):
            for index, proved in grid_obligations(
                side, points, ASSIGNMENTS, low=low, high=high
            ):
                completed.append(((slab, *index), proved))
    except TimeoutError as error:
        interrupted = True
        print(
            f"unresolved: alarm after {len(completed)} inequalities: {error}", file=sys.stderr
        )
    return packet(
        len(completed),
        [index for index, proved in completed if not proved],
        interrupted=interrupted,
    )


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result = dict(pairs)
    if len(result) != len(pairs):
        raise ValueError("packet contains duplicate object keys")
    return result


def parse_worker(stdout: str) -> dict[str, Any]:
    """Admit the fixed worker envelope, not its mathematical conclusion.

    This is not the independent continuous reader. Exact string identity checks
    reject altered sides/endpoints without constructing numbers from their text.
    """
    if len(stdout.encode()) > PACKET_BYTE_CAP:
        raise ValueError("packet exceeds 256 KiB")
    result = json.loads(stdout, object_pairs_hook=_unique_object)
    template = packet(0, [])
    if type(result) is not dict or set(result) != set(template):
        raise ValueError("packet must have exactly the frozen nine keys")
    if type(result["version"]) is not int or result["version"] != 1:
        raise ValueError("packet version is invalid")
    if any(result[key] != template[key] for key in ("kind", "side", "half_angle_slabs")):
        raise ValueError("packet changes the fixed source or closed half-angle slabs")
    if result["grid"] != [6, 3] or any(type(value) is not int for value in result["grid"]):
        raise ValueError("packet changes the complete fixed grid")
    if result["assignments"] != template["assignments"] or any(
        type(label) is not int for row in result["assignments"] for label in row
    ):
        raise ValueError("packet changes the frozen point labels")
    checked = result["inequalities_checked"]
    if type(checked) is not int or not 0 <= checked <= OBLIGATION_COUNT:
        raise ValueError("packet completed-prefix count is invalid")
    failures = result["unresolved"]
    if type(failures) is not list or len(failures) > checked:
        raise ValueError("packet unresolved inventory is invalid")
    previous = -1
    for index in failures:
        if (
            type(index) is not list
            or len(index) != 6
            or any(
                type(value) is not int or not 0 <= value < bound
                for value, bound in zip(index, (2, 3, 6, 2, 3, 4), strict=True)
            )
        ):
            raise ValueError("packet unresolved index is invalid")
        slab, row, column, triangle, vertex, axis = index
        ordinal = (((((slab * 3 + row) * 6 + column) * 2 + triangle) * 3 + vertex) * 4) + axis
        if not previous < ordinal < checked:
            raise ValueError("packet failures must be ordered unique members of the prefix")
        previous = ordinal
    if result["status"] not in ("proved", "unresolved") or (
        result["status"] == "proved" and (checked != OBLIGATION_COUNT or failures)
    ):
        raise ValueError("packet status exceeds its completed inventory")
    return result


def _expired(_signum: int, _frame: Any) -> None:
    raise TimeoutError("fixed ten-second near-axis cap")


def _text(value: str | bytes | None) -> str:
    return value.decode(errors="replace") if isinstance(value, bytes) else value or ""


def _run_child() -> tuple[dict[str, Any], dict[str, Any], int]:
    command = [
        sys.executable,
        "-m",
        "devtools.angle_near_axis_control",
        "--target-near-axis",
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
        except (ValueError, TypeError, RecursionError) as error:
            result, code = packet(0, []), 2
            note = f"worker packet refused: {error}"
    except subprocess.TimeoutExpired as error:
        stdout, stderr, child_exit = _text(error.stdout), _text(error.stderr), None
        result, code = packet(0, []), 1
        note = "child process cap; no complete packet retained"
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
    """Explicit target command; publication is atomic per file, not across both files."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target-near-axis", action="store_true", required=True)
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
                result = run_target()
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
    except TimeoutError as error:
        print(json.dumps(packet(0, []), sort_keys=True))
        print(f"unresolved: {error}", file=sys.stderr)
        return 1
    except (OSError, ValueError, TypeError) as error:
        print(f"refused: {error}", file=sys.stderr)
        return 2
    else:
        return code


if __name__ == "__main__":
    raise SystemExit(main())
