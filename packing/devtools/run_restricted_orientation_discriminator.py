"""Bounded exact-angle BC-255 auxiliary discriminator, with no target default.

The coordinator must commit a prospective experiment before --target-fixed-side.
This command does not inspect or certify that research authorization. It checks only
the fixed point-set mechanism, never H-036's continuous-angle or packing claim.
"""

from __future__ import annotations

import argparse
import json
import re
import signal
import subprocess
import sys
import time
from collections.abc import Callable, Sequence
from fractions import Fraction
from typing import Any

from cases.stromquist.restricted_orientation import (
    ANGLE_OBLIGATIONS,
    OBLIGATIONS,
    Point,
    direct_membership,
    point_sets,
    replay_point_sets,
    source_field,
    source_points,
)
from sqpack.field import FieldElement, NumberField

WALL_CAP_SECONDS = 10
MODES = ("source-control", "target-fixed-side")
SIDE_TEXT = {
    "source-control": "poly[2,4/3]",
    "target-fixed-side": "poly[1939/500,0]",
}
_RATIONAL = re.compile(r"-?(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?", re.ASCII)


def parse_coordinate(value: Any, field: NumberField) -> FieldElement:
    """Decode only bounded canonical Q(sqrt(2)) power-basis output, without eval."""
    if not isinstance(value, str) or len(value) > 520:
        raise ValueError("escape coordinate must be a bounded power-basis string")
    if not value.startswith("poly[") or not value.endswith("]"):
        raise ValueError("escape coordinate requires poly[a,b]")
    parts = value[5:-1].split(",")
    if len(parts) != 2:
        raise ValueError("escape coordinate needs exactly two coefficients")
    coefficients: list[Fraction] = []
    for part in parts:
        if len(part) > 256 or _RATIONAL.fullmatch(part) is None:
            raise ValueError("escape coefficient must be a bounded canonical rational")
        coefficient = Fraction(part)
        if str(coefficient) != part:
            raise ValueError("escape coefficient is not a canonical rational")
        coefficients.append(coefficient)
    return field.element(coefficients)


def verify_escape(
    side: FieldElement,
    ten: tuple[Point, ...],
    twelve: tuple[Point, ...],
    row: dict[str, Any],
) -> None:
    """Replay a returned escape with corners/determinants, not producer cell masks."""
    name, angle = row.get("obligation"), row.get("angle_degrees")
    if type(angle) is not int or angle not in ANGLE_OBLIGATIONS:
        raise ValueError("escape angle must be exactly 0 or 45 degrees")
    if not isinstance(name, str) or name not in ANGLE_OBLIGATIONS[angle]:
        raise ValueError("escape obligation does not belong to its angle")
    if row.get("square_side") != "1" or row.get("square_semantics") != "closed":
        raise ValueError("escape must describe a closed unit square")
    center = row.get("center_power_basis")
    if not isinstance(center, list) or len(center) != 2:
        raise ValueError("escape needs two exact center coordinates")
    x, y = (parse_coordinate(value, side.field) for value in center)
    actual_ten = direct_membership(side, angle, (x, y), ten)
    actual_twelve = direct_membership(side, angle, (x, y), twelve)
    for key, actual in (
        ("ten_membership_mask", actual_ten),
        ("twelve_membership_mask", actual_twelve),
    ):
        if type(row.get(key)) is not int or row[key] != actual:
            raise ValueError("escape mask disagrees with direct determinant geometry")
    if name.startswith("twelve_cover_"):
        valid = actual_twelve == 0
    elif name == "axis_ten_cover":
        valid = actual_ten == 0
    elif name == "localization":
        localized = 1 <= x <= side - 1 and (y <= 1 or y >= side - 1)
        valid = actual_ten == 0 and not localized
    else:
        index = int(name.removeprefix("forced_A")) - 1
        canonical = 1 <= x <= side / 2 and 0 <= y <= 1
        valid = actual_ten == 0 and canonical and not actual_twelve & (1 << index)
    if not valid:
        raise ValueError("returned square does not violate the named auxiliary obligation")
    if row.get("strict_box_counterexample_established") is not False:
        raise ValueError("an auxiliary escape cannot claim a strict-box counterexample")


def run_geometry(mode: str, emit: Callable[[dict[str, Any]], None]) -> None:
    """Worker body; the CLI installs a process timer before entering this function."""
    if mode not in MODES:
        raise ValueError("unknown discriminator mode")
    wall_start, cpu_start = time.monotonic(), time.process_time()
    field = source_field()
    if mode == "source-control":
        side, ten, twelve = source_points(field)
    else:
        # This is the only target construction, reached only by explicit target mode.
        side = field.rational(Fraction(1939, 500))
        ten, twelve = point_sets(side)
    if side.text() != SIDE_TEXT[mode]:
        raise ValueError("discriminator side differs from its fixed mode")
    emit(
        {
            "kind": "input",
            "mode": mode,
            "container_side_power_basis": side.text(),
            "field": "Q(sqrt(2)), positive root in (1,2)",
            "ten_points_power_basis": [[x.text(), y.text()] for x, y in ten],
            "twelve_points_power_basis": [[x.text(), y.text()] for x, y in twelve],
        }
    )

    def completed_angle(report: dict[str, Any]) -> None:
        for obstruction in report["obstructions"]:
            verify_escape(side, ten, twelve, obstruction)
        emit({"kind": "angle_complete", **report})

    replay_point_sets(side, ten, twelve, on_angle_complete=completed_angle)
    emit(
        {
            "kind": "finished",
            "worker_wall_seconds": time.monotonic() - wall_start,
            "worker_cpu_seconds": time.process_time() - cpu_start,
        }
    )


def collect_receipts(
    output: str,
    mode: str,
    *,
    worker_succeeded: bool,
    interrupted: bool = False,
) -> dict[str, Any]:
    """Retain completed angles only; a cut-off JSON line carries no checked claim.

    These are receipts from this command's own child, not an external proof format.
    Exact escape replay has already run inside the same bounded worker before emit.
    """
    if mode not in MODES:
        raise ValueError("unknown discriminator mode")
    lines = output.splitlines(keepends=True)
    if interrupted and lines and not lines[-1].endswith("\n"):
        lines.pop()
    inputs = None
    angles: list[int] = []
    cases: list[dict[str, Any]] = []
    obligations: dict[str, bool | None] = dict.fromkeys(OBLIGATIONS)
    obstructions: list[dict[str, Any]] = []
    timing = None
    for line in lines:
        row = json.loads(line)
        if not isinstance(row, dict):
            raise TypeError("worker receipt must be an object")
        kind = row.get("kind")
        if kind == "input":
            if inputs is not None or angles or row.get("mode") != mode:
                raise ValueError("duplicate or mismatched input receipt")
            if row.get("container_side_power_basis") != SIDE_TEXT[mode]:
                raise ValueError("worker receipt has the wrong fixed side")
            if (
                len(row.get("ten_points_power_basis", [])) != 10
                or len(row.get("twelve_points_power_basis", [])) != 12
            ):
                raise ValueError("worker receipt has the wrong point inventory")
            inputs = row
        elif kind == "angle_complete":
            angle = row.get("angle_degrees")
            if inputs is None or timing is not None or type(angle) is not int:
                raise ValueError("angle receipt is out of order")
            if angles != ([] if angle == 0 else [0]) or angle not in (0, 45):
                raise ValueError("completed angles must occur once in order 0, 45")
            named = row.get("obligations")
            if not isinstance(named, dict) or set(named) != set(ANGLE_OBLIGATIONS[angle]):
                raise ValueError("angle receipt omits or adds an obligation")
            if any(type(value) is not bool for value in named.values()):
                raise ValueError("completed obligations must be Boolean")
            failures = row.get("obstructions")
            if not isinstance(failures, list) or any(not isinstance(x, dict) for x in failures):
                raise ValueError("obstructions must be a list of records")
            failed_names = [item.get("obligation") for item in failures]
            if len(set(failed_names)) != len(failed_names) or set(failed_names) != {
                name for name, value in named.items() if not value
            }:
                raise ValueError("each failed obligation requires exactly one checked escape")
            case = row.get("case")
            if not isinstance(case, dict) or case.get("angle_degrees") != angle:
                raise ValueError("angle receipt needs its matching case counts")
            counts = case.get("reachable_event_strata_by_dimension")
            if (
                not isinstance(counts, list)
                or len(counts) != 3
                or any(type(value) is not int or value < 0 for value in counts)
                or sum(counts) == 0
            ):
                raise ValueError("angle receipt has empty or invalid stratum counts")
            angles.append(angle)
            cases.append(case)
            obligations.update(named)
            obstructions.extend(failures)
        elif kind == "finished":
            if inputs is None or angles != [0, 45] or timing is not None:
                raise ValueError("finished receipt lacks both completed angles")
            timing = row
        else:
            raise ValueError("unknown worker receipt kind")
    if worker_succeeded and (angles != [0, 45] or timing is None):
        raise ValueError("successful worker omitted required completed obligations")
    complete = worker_succeeded and timing is not None
    return {
        "kind": "restricted-orientation-auxiliary-discriminator",
        "mode": mode,
        "scope": "fixed-side closed-unit one-square clauses at exactly 0 and 45 degrees",
        "complete": complete,
        "status": (
            "auxiliary_obstruction_retained"
            if obstructions
            else "auxiliary_checks_complete"
            if complete
            else "unresolved"
        ),
        "inputs": inputs,
        "cases": cases,
        "obligations": obligations,
        "checked_obligations": [
            name for name, value in obligations.items() if value is not None
        ],
        "unchecked_obligations": [name for name, value in obligations.items() if value is None],
        "obstructions": obstructions,
        "worker_timing": timing,
        "h036_outcome": "unresolved",
        "perturbed_angles_evaluated": False,
        "theorem_acceptance": False,
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument("--source-control", action="store_true")
    mode_group.add_argument(
        "--target-fixed-side",
        action="store_true",
        help="requires a separately frozen experiment",
    )
    parser.add_argument("--timeout-seconds", type=int, default=WALL_CAP_SECONDS)
    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    if not 1 <= args.timeout_seconds <= WALL_CAP_SECONDS:
        parser.error("timeout must be an integer from 1 to 10 seconds")
    mode = "source-control" if args.source_control else "target-fixed-side"

    def emit(receipt: dict[str, Any]) -> None:
        print(json.dumps(receipt, sort_keys=True), flush=True)

    def expired(_signal, _frame) -> None:
        raise TimeoutError("fixed process wall cap expired")

    try:
        if args.worker:
            # The internal mode has its own timer; it cannot bypass the parent cap.
            previous = signal.signal(signal.SIGALRM, expired)
            signal.alarm(args.timeout_seconds)
            try:
                run_geometry(mode, emit)
            finally:
                signal.alarm(0)
                signal.signal(signal.SIGALRM, previous)
            return 0
        command = [
            sys.executable,
            "-m",
            "devtools.run_restricted_orientation_discriminator",
            f"--{mode}",
            "--worker",
            "--timeout-seconds",
            str(args.timeout_seconds),
        ]
        started = time.monotonic()
        try:
            process = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=False,
                timeout=args.timeout_seconds,
            )
            result = collect_receipts(
                process.stdout,
                mode,
                worker_succeeded=process.returncode == 0,
                interrupted=process.returncode != 0,
            )
            exit_code = 0 if process.returncode == 0 else 1
            if process.returncode:
                result["stop_reason"] = f"worker exited {process.returncode}"
                sys.stderr.write(process.stderr)
        except subprocess.TimeoutExpired as error:
            partial = error.stdout or ""
            if isinstance(partial, bytes):
                partial = partial.decode("utf-8")
            result = collect_receipts(partial, mode, worker_succeeded=False, interrupted=True)
            result["stop_reason"] = "fixed process wall cap expired"
            print("unresolved: fixed process wall cap expired", file=sys.stderr)
            exit_code = 1
        result["process_wall_seconds"] = time.monotonic() - started
        result["process_wall_cap_seconds"] = args.timeout_seconds
        emit(result)
    except TimeoutError as error:
        print(f"unresolved: {error}", file=sys.stderr)
        return 1
    except (OSError, ValueError, TypeError, KeyError) as error:
        print(f"refused: {error}", file=sys.stderr)
        return 2
    else:
        return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
