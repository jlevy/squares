"""Bounded exact pair screening. Target mode requires a new frozen experiment.

Controls never load exp-113 weights. A successful pair witness refutes only that
fixed weight assignment; absence of a pair obstruction is not feasibility.
"""

from __future__ import annotations

import argparse
import json
import signal
import subprocess
import sys
import time
from collections.abc import Sequence
from pathlib import Path
from typing import Any

from devtools.check_full_size_density_pair_separator import (
    CANDIDATE_SOURCE,
    CANDIDATE_WEIGHTS,
    CONTROLS,
    WALL_CAP_SECONDS,
    bind_parent,
    control_family,
    family_signature,
)
from devtools.check_full_size_density_support_ceiling import load_packet, load_source
from sqpack.full_size_density.pair_separator import (
    PAIR_CAP,
    PairFamily,
    PairResult,
    eligible_pairs,
    make_family,
    separate,
)
from sqpack.full_size_density.support_ceiling import Point, SupportError
from sqpack.full_size_density.support_screen import bind_source, support_metadata


def frozen_candidate(parent: Any) -> PairFamily:
    """Build only the fixed exp-113 candidate after checking its accepted binding."""
    seeds, side = load_source("trump11-v1")
    bound = bind_source(seeds, side)
    bind_parent(parent, support_metadata(bound))
    family = make_family(
        tuple(square for orbit in bound.support.orbits for square in orbit),
        side,
        tuple(
            weight
            for orbit, weight in zip(bound.support.orbits, CANDIDATE_WEIGHTS, strict=True)
            for _ in orbit
        ),
    )
    if len(eligible_pairs(family)) != PAIR_CAP:
        raise SupportError("frozen candidate must have exactly 134 eligible pairs")
    return family


def _point(point: Point) -> list[list[str]]:
    return [[str(value) for value in coordinate.coeffs] for coordinate in point]


def make_packet(source: str, family: PairFamily, result: PairResult) -> dict[str, Any]:
    witness = result.witness
    return {
        "version": 1,
        "source": source,
        "family": family_signature(family),
        "eligible": result.eligible,
        "separations": [
            {"pair": list(item.pair), "axis": _point(item.axis)} for item in result.separations
        ],
        "witness": None
        if witness is None
        else {
            "pair": list(witness.pair),
            "point": _point(witness.point),
            "radius": str(witness.radius),
            "excess": str(witness.excess),
        },
    }


def worker(*, control: str | None, candidate: Path | None) -> dict[str, Any]:
    if (control is None) == (candidate is None):
        raise SupportError("exactly one explicit control or target mode is required")
    started, cpu = time.monotonic(), time.process_time()
    if candidate is not None:
        family, source = frozen_candidate(load_packet(candidate)), CANDIDATE_SOURCE
    else:
        if control is None:
            raise SupportError("missing named control")
        family, source = control_family(control), control
    result = separate(family)
    return {
        "result": make_packet(source, family, result),
        "wall_seconds": time.monotonic() - started,
        "cpu_seconds": time.process_time() - cpu,
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--control", choices=CONTROLS)
    modes.add_argument(
        "--candidate",
        type=Path,
        help="accepted parent packet; requires a separately frozen experiment",
    )
    parser.add_argument("--timeout-seconds", type=int, default=WALL_CAP_SECONDS)
    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    if not 1 <= args.timeout_seconds <= WALL_CAP_SECONDS:
        parser.error("timeout must be an integer from 1 to 30 seconds")

    def expired(_signal, _frame):
        raise TimeoutError("pair worker reached its fixed process wall cap")

    try:
        if args.worker:
            previous = signal.signal(signal.SIGALRM, expired)
            signal.alarm(args.timeout_seconds)
            try:
                receipt = worker(control=args.control, candidate=args.candidate)
                payload = json.dumps(receipt.pop("result"), sort_keys=True)
            finally:
                signal.alarm(0)
                signal.signal(signal.SIGALRM, previous)
            print(payload)
            print(json.dumps(receipt, sort_keys=True), file=sys.stderr)
            return 0
        command = [
            sys.executable,
            "-m",
            "devtools.run_full_size_density_pair_separator",
            "--worker",
            "--timeout-seconds",
            str(args.timeout_seconds),
        ]
        command.extend(
            ["--candidate", str(args.candidate)]
            if args.candidate is not None
            else ["--control", args.control]
        )
        completed = subprocess.run(
            command, capture_output=True, text=True, timeout=args.timeout_seconds, check=False
        )
        if completed.returncode:
            sys.stderr.write(completed.stderr)
            return completed.returncode
        sys.stdout.write(completed.stdout)
        sys.stderr.write(completed.stderr)
    except subprocess.TimeoutExpired, TimeoutError:
        print("unresolved: fixed process wall cap expired", file=sys.stderr)
        return 1
    except (SupportError, OSError) as error:
        print(f"refused: {error}", file=sys.stderr)
        return 2
    else:
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
