"""Bind complete graph certificates to explicit retained density sources.

Scientific source controls and the fixed candidate require their own prospective
protocol. No source is loaded on import. The independent replay route reconstructs
the source without the producer's support constructor and checks containment before
using the independent geometry reader. A graph obstruction remains unresolved.
"""

from __future__ import annotations

import argparse
import json
import signal
import subprocess
import sys
import time
from collections.abc import Sequence
from fractions import Fraction
from pathlib import Path
from typing import Any

from cases.trump11.packing import U_MIN_POLY
from devtools.check_full_size_density_pair_separator import (
    CANDIDATE_SOURCE,
    candidate_family,
    control_family,
)
from devtools.check_full_size_density_support_ceiling import PACKET_BYTES, load_packet
from devtools.check_geometric_graph_certificate import (
    MAX_FIELD_DEGREE as READER_MAX_FIELD_DEGREE,
)
from devtools.check_geometric_graph_certificate import GuardError, check_packet
from devtools.geometric_graph_certificate import MAX_FIELD_DEGREE as PRODUCER_MAX_FIELD_DEGREE
from devtools.geometric_graph_certificate import produce
from devtools.run_full_size_density_pair_separator import frozen_candidate
from sqpack.full_size_density.pair_separator import PairFamily
from sqpack.full_size_density.support_ceiling import Square, SupportError

CONTROL_NAMES = (
    "toy-edge-v1",
    "toy-equal-v1",
    "toy-overlap-v1",
    "trump-original-control-v1",
    "trump-uniform-control-v1",
    "trump-perturbed-control-v1",
)
MAX_SECONDS = 60
MAX_NODES = 10000


def declared_source_preflight() -> None:
    """Compare static source metadata before constructing its field or placements."""
    degree = len(U_MIN_POLY) - 1
    if not 1 <= degree <= min(PRODUCER_MAX_FIELD_DEGREE, READER_MAX_FIELD_DEGREE):
        raise SupportError("declared source degree is outside both adapters' admission")


def serialize_packet(raw: Any) -> str:
    """Respect the unchanged reader byte cap, including the printed newline."""
    serialized = json.dumps(raw, sort_keys=True, allow_nan=False)
    if len(serialized.encode("utf-8")) + 1 > PACKET_BYTES:
        raise SupportError("serialized graph packet exceeds the existing input byte cap")
    return serialized


def _canonical_square(square: Square) -> Square:
    """Normalize cyclic origin and traversal, without changing the geometric square."""
    cycles = [
        current[offset:] + current[:offset]
        for current in (square, tuple(reversed(square)))
        for offset in range(4)
    ]
    return min(
        cycles,
        key=lambda cycle: tuple(tuple(tuple(v.coeffs) for v in p) for p in cycle),
    )


def family_source(family: PairFamily) -> dict[str, Any]:
    """Serialize every validated source member, including zero weights.

    PairFamily is built by the accepted source reconstruction, which verifies
    contained unit squares. This function only normalizes representation; it does
    not deduplicate, drop zeros, add weights or infer a source from an input packet.
    """
    certificate = family.side.field.precondition_certificate()
    return {
        "field": {
            "minimal_polynomial": certificate["normalized_minimal_polynomial"],
            "isolating_interval": certificate["declared_isolating_interval"],
        },
        "squares": [
            {
                "id": f"square-{index}",
                "vertices": [
                    [[str(value) for value in coordinate.coeffs] for coordinate in point]
                    for point in _canonical_square(entry.square)
                ],
                "weight": str(entry.weight),
            }
            for index, entry in enumerate(family.placements)
        ],
    }


def produce_bound(family: PairFamily, source: str, *, node_limit: int) -> dict[str, Any]:
    return {
        "version": 1,
        "source": source,
        "side": [str(value) for value in family.side.coeffs],
        "certificate": produce(
            family_source(family),
            field=family.side.field,
            threshold=Fraction(1),
            node_limit=node_limit,
        ),
    }


def replay_bound(raw: Any, family: PairFamily, source: str) -> dict[str, Any]:
    """Bind the caller's separately reconstructed source before proof replay."""
    if type(raw) is not dict or set(raw) != {"version", "source", "side", "certificate"}:
        raise SupportError("density graph packet has missing or unexpected keys")
    if type(raw["version"]) is not int or raw["version"] != 1:
        raise SupportError("density graph packet version must be integer one")
    if raw["source"] != source or raw["side"] != [str(v) for v in family.side.coeffs]:
        raise SupportError("density graph source or side differs from the caller binding")
    checked = check_packet(
        raw["certificate"],
        expected_source=family_source(family),
        field=family.side.field,
        threshold=Fraction(1),
    )
    proved = checked["status"] == "verified_depth_bound" and checked["bound_proved"] is True
    return {
        "source": source,
        "status": "verified_density_bound" if proved else "unresolved",
        "bound_proved": proved,
        "mass": str(sum((entry.weight for entry in family.placements), Fraction(0))),
        "containment": "validated during independent source reconstruction",
        "verification": checked,
        "scope": "Specified contained family only; no below-Trump density or packing bound.",
    }


def worker(
    *, control: str | None, candidate: Path | None, packet: Path | None, node_limit: int
) -> dict[str, Any]:
    """Construct only the explicitly requested source; target is never a default."""
    if (control is None) == (candidate is None):
        raise SupportError("exactly one named control or explicit candidate is required")
    if type(node_limit) is not int or not 1 <= node_limit <= MAX_NODES:
        raise SupportError("node limit is outside the admitted fixed budget")
    if candidate is not None or control in (
        "trump-original-control-v1",
        "trump-uniform-control-v1",
        "trump-perturbed-control-v1",
    ):
        declared_source_preflight()
    if candidate is not None:
        parent = load_packet(candidate)
        family = candidate_family(parent) if packet is not None else frozen_candidate(parent)
        source = CANDIDATE_SOURCE
    else:
        if control not in CONTROL_NAMES:
            raise SupportError("unknown graph control")
        assert control is not None
        family, source = control_family(control), control
    if packet is not None:
        return replay_bound(load_packet(packet), family, source)
    return produce_bound(family, source, node_limit=node_limit)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--control", choices=CONTROL_NAMES)
    modes.add_argument(
        "--candidate", type=Path, help="accepted exp113 parent; requires protocol"
    )
    parser.add_argument("--input", type=Path, help="independently replay this packet")
    parser.add_argument("--node-limit", type=int, required=True)
    parser.add_argument("--timeout-seconds", type=int, required=True)
    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    if not 1 <= args.timeout_seconds <= MAX_SECONDS:
        parser.error("timeout must be an integer from1 through60 seconds")
    if not 1 <= args.node_limit <= MAX_NODES:
        parser.error("node limit must be an integer from1 through10000")

    def expired(_signal: int, _frame: Any) -> None:
        raise TimeoutError("density graph worker reached its fixed process cap")

    try:
        if args.worker:
            started, cpu = time.monotonic(), time.process_time()
            previous = signal.signal(signal.SIGALRM, expired)
            signal.alarm(args.timeout_seconds)
            try:
                payload = worker(
                    control=args.control,
                    candidate=args.candidate,
                    packet=args.input,
                    node_limit=args.node_limit,
                )
                serialized = serialize_packet(payload)
            finally:
                signal.alarm(0)
                signal.signal(signal.SIGALRM, previous)
            print(serialized)
            print(
                json.dumps(
                    {
                        "wall_seconds": time.monotonic() - started,
                        "cpu_seconds": time.process_time() - cpu,
                    },
                    sort_keys=True,
                ),
                file=sys.stderr,
            )
            return 0
        command = [
            sys.executable,
            "-m",
            "devtools.run_full_size_density_graph",
            "--worker",
            "--node-limit",
            str(args.node_limit),
            "--timeout-seconds",
            str(args.timeout_seconds),
        ]
        command.extend(
            ["--candidate", str(args.candidate)]
            if args.candidate is not None
            else ["--control", args.control]
        )
        if args.input is not None:
            command.extend(["--input", str(args.input)])
        completed = subprocess.run(
            command, capture_output=True, text=True, timeout=args.timeout_seconds, check=False
        )
        sys.stderr.write(completed.stderr)
        if completed.returncode == 0:
            sys.stdout.write(completed.stdout)
    except subprocess.TimeoutExpired, TimeoutError:
        print(
            "unresolved: complete scientific subprocess exceeded its original cap",
            file=sys.stderr,
        )
        return 1
    except (SupportError, GuardError, OSError, ArithmeticError, ValueError) as error:
        print(f"refused: {error}", file=sys.stderr)
        return 2
    else:
        return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
