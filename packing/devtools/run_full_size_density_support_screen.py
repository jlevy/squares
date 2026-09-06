"""Bounded BC-254 source control or explicitly requested target screen.

No target solve is a default. The research coordinator must separately authorize and
freeze --solve-target. JSON goes to stdout only after the bounded worker succeeds.
"""

from __future__ import annotations

import argparse
import json
import signal
import subprocess
import sys
import time
from collections.abc import Sequence
from typing import Any

from devtools.check_full_size_density_support_ceiling import (
    load_source,
    reconstruct_source,
    replay_packet,
)
from sqpack.exact_lp import ExactLPError
from sqpack.full_size_density.support_ceiling import SupportError
from sqpack.full_size_density.support_screen import (
    ScreenResult,
    bind_source,
    make_packet,
    solve_screen,
    support_metadata,
)

SOURCES = ("trump11-v1", "toy-rational-v1", "toy-algebraic-v1")
WALL_CAP_SECONDS = 60


def source_control(source: str) -> dict[str, Any]:
    seeds, side = load_source(source)
    bound = bind_source(seeds, side)
    independent = reconstruct_source(source)
    metadata = support_metadata(bound)
    if json.dumps(metadata, sort_keys=True) != json.dumps(independent[2], sort_keys=True):
        raise SupportError("independent source/preimage replay disagrees")
    mass = sum(
        weight * size for weight, size in zip(bound.baseline, bound.support.sizes, strict=True)
    )
    expected = 11 if source == "trump11-v1" else 1
    if mass != expected:
        raise SupportError("source control has the wrong exact mass")
    return {
        "kind": "source-input-control",
        "source": source,
        "support": metadata,
        "labelled_images": sum(len(labels) for _, labels in bound.preimages),
        "distinct_placements": sum(bound.support.sizes),
        "uniform_mass": str(mass),
        "target_outcome": "unresolved",
        "target_lp_invoked": False,
    }


def _worker(source: str, *, solve_target: bool) -> dict[str, Any]:
    start_wall, start_cpu = time.monotonic(), time.process_time()
    if solve_target:
        seeds, side = load_source(source)
        bound = bind_source(seeds, side)

        def replay_stage(stage: ScreenResult) -> None:
            replay_packet(make_packet(source, bound, stage))

        result = solve_screen(bound, stage_check=replay_stage)
        output = make_packet(source, bound, result)
    else:
        output = source_control(source)
    return {
        "result": output,
        "wall_seconds": time.monotonic() - start_wall,
        "cpu_seconds": time.process_time() - start_cpu,
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--source-control", action="store_true")
    mode.add_argument(
        "--solve-target",
        action="store_true",
        help="requires a separately frozen research commission",
    )
    parser.add_argument("--source", choices=SOURCES, default="trump11-v1")
    parser.add_argument("--timeout-seconds", type=int, default=WALL_CAP_SECONDS)
    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    if not 1 <= args.timeout_seconds <= WALL_CAP_SECONDS:
        parser.error("timeout must be an integer from 1 to 60 seconds")
    if args.solve_target and args.source != "trump11-v1":
        parser.error("--solve-target uses only the declared Trump source")

    def expired(_signal, _frame):
        raise TimeoutError("fixed process wall cap expired")

    try:
        if args.worker:
            # The internal entry also has a wall cap, so --worker cannot bypass it.
            signal.signal(signal.SIGALRM, expired)
            signal.alarm(args.timeout_seconds)
            try:
                receipt = _worker(args.source, solve_target=args.solve_target)
            finally:
                signal.alarm(0)
            print(json.dumps(receipt.pop("result"), sort_keys=True))
            print(json.dumps(receipt, sort_keys=True), file=sys.stderr)
            return 0
        command = [
            sys.executable,
            "-m",
            "devtools.run_full_size_density_support_screen",
            "--worker",
            "--source",
            args.source,
            "--solve-target" if args.solve_target else "--source-control",
        ]
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
    except (SupportError, ExactLPError, OSError) as error:
        print(f"refused: {error}", file=sys.stderr)
        return 2
    else:
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
