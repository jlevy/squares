"""Replay fixed-family a.e. density receipts, not a global packing-bound claim.

Positive receipts require the complete independent slab computation. Negative
receipts require only a strict independently checked excess box. Source replay
shares the accepted number field, square validator and exp-113 parent binding;
it uses direct D4 reconstruction and never imports the producer or its facets.
The process ceiling is an implementation guard, not experiment authority.
"""

from __future__ import annotations

import argparse
import json
import signal
import subprocess
import sys
import time
from collections.abc import Callable, Sequence
from fractions import Fraction
from pathlib import Path
from typing import Any

from devtools.check_full_size_density_pair_separator import (
    CANDIDATE_SOURCE,
    CONTROLS,
    candidate_family,
    control_family,
    family_signature,
    parse_rational,
)
from devtools.check_full_size_density_support_ceiling import load_packet
from devtools.density_slab_verifier import (
    SlabWitness,
    check_witness,
    verify_density_slabs,
)
from sqpack.field import NumberField
from sqpack.full_size_density.pair_separator import PairFamily
from sqpack.full_size_density.support_ceiling import Point, SupportError

PROCESS_CEILING_SECONDS = 120
MAX_RECEIPT_BYTES = 2 * 1024 * 1024
SEMANTICS = "lebesgue-ae-unit-square-depth-v1"


def exact_keys(value: Any, expected: set[str]) -> dict[str, Any]:
    if type(value) is not dict or set(value) != expected:
        raise SupportError("receipt object has missing or unexpected keys")
    return value


def explicit_source(control: str | None, parent: Any) -> str:
    if (control is None) == (parent is None):
        raise SupportError("exactly one explicit control or candidate is required")
    if control is not None and control not in CONTROLS:
        raise SupportError("unknown named control")
    return CANDIDATE_SOURCE if control is None else control


def candidate_invariants(family: PairFamily) -> None:
    if (
        len(family.placements) != 60
        or sum(item.weight > 0 for item in family.placements) != 36
        or sum((item.weight for item in family.placements), Fraction()) != Fraction(56, 5)
    ):
        raise SupportError("candidate distinct support, positive support or mass changed")


def _point(value: Any, field: NumberField) -> Point:
    if type(value) is not list or len(value) != 2:
        raise SupportError("point requires two exact coordinates")
    coordinates = []
    for coordinate in value:
        if type(coordinate) is not list or len(coordinate) != field.degree:
            raise SupportError("coordinate has wrong field degree")
        coordinates.append(field.element([parse_rational(item) for item in coordinate]))
    return coordinates[0], coordinates[1]


def replay_packet(
    packet: Any, *, control: str | None = None, parent: Any = None
) -> dict[str, Any]:
    """Reconstruct the declared input before independently checking its result."""
    source = explicit_source(control, parent)
    data = exact_keys(packet, {"version", "source", "semantics", "family", "mass", "result"})
    if type(data["version"]) is not int or data["version"] != 1:
        raise SupportError("unsupported receipt version")
    if data["source"] != source or data["semantics"] != SEMANTICS:
        raise SupportError("receipt source or a.e. semantics differs from explicit mode")
    family = candidate_family(parent) if control is None else control_family(control)
    if control is None:
        candidate_invariants(family)
    if json.dumps(data["family"], sort_keys=True) != json.dumps(
        family_signature(family), sort_keys=True
    ):
        raise SupportError("receipt side, canonical support or weights changed")
    mass = sum((item.weight for item in family.placements), Fraction())
    if parse_rational(data["mass"]) != mass:
        raise SupportError("receipt mass differs from its reconstructed family")
    result = data["result"]
    if type(result) is not dict:
        raise SupportError("result must be an object")
    squares = tuple(item.square for item in family.placements)
    weights = tuple(item.weight for item in family.placements)
    if result.get("kind") == "complete-ae-maximum":
        exact_keys(result, {"kind", "maximum"})
        maximum = parse_rational(result["maximum"])
        if not 0 <= maximum <= 1:
            raise SupportError("positive receipt must claim a maximum between zero and one")
        replay = verify_density_slabs(squares, family.side, weights)
        if replay.maximum != maximum:
            raise SupportError("independent complete slab maximum disagrees")
        decision = "ae-feasible"
    elif result.get("kind") == "strict-excess-box":
        exact_keys(result, {"kind", "point", "radius", "members", "excess"})
        members = result["members"]
        if type(members) is not list or any(type(item) is not int for item in members):
            raise SupportError("witness members must be a list of exact integer indices")
        witness = SlabWitness(
            _point(result["point"], family.side.field),
            parse_rational(result["radius"]),
            tuple(members),
            parse_rational(result["excess"]),
        )
        check_witness(squares, family.side, weights, witness)
        maximum, decision = None, "fixed-weights-refuted"
    else:
        raise SupportError("unknown or incomplete density result")
    return {
        "source": source,
        "decision": decision,
        "mass": str(mass),
        "maximum": None if maximum is None else str(maximum),
        "scope": "fixed weighted family at its exact side; no global packing-bound claim",
    }


def bounded_worker(action: Callable[[], dict[str, Any]], timeout_seconds: int) -> int:
    """Cover parsing, construction, geometry and serialization with the child alarm."""

    def expired(_signal, _frame):
        raise TimeoutError("density worker reached its process wall cap")

    started, cpu = time.monotonic(), time.process_time()
    previous = signal.signal(signal.SIGALRM, expired)
    signal.alarm(timeout_seconds)
    try:
        payload = json.dumps(action(), sort_keys=True, allow_nan=False)
        if len(payload.encode("utf-8")) > MAX_RECEIPT_BYTES:
            raise SupportError("receipt exceeds the bounded file size")
        print(payload)
        print(
            json.dumps(
                {
                    "wall_seconds": time.monotonic() - started,
                    "cpu_seconds": time.process_time() - cpu,
                }
            ),
            file=sys.stderr,
        )
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, previous)
    return 0


def bounded_child(module: str, arguments: list[str], timeout_seconds: int) -> int:
    completed = subprocess.run(
        [sys.executable, "-m", module, "--worker", *arguments],
        capture_output=True,
        text=True,
        timeout=timeout_seconds,
        check=False,
    )
    if completed.returncode:
        sys.stderr.write(completed.stderr)
        return completed.returncode
    if len(completed.stdout.encode("utf-8")) > MAX_RECEIPT_BYTES:
        raise SupportError("child receipt exceeds the bounded file size")
    try:
        data = json.loads(completed.stdout)
    except ValueError as error:
        raise SupportError("child did not return one complete JSON receipt") from error
    if type(data) is not dict:
        raise SupportError("child receipt is not an object")
    sys.stdout.write(completed.stdout)
    sys.stderr.write(completed.stderr)
    return 0


def add_mode_arguments(parser: argparse.ArgumentParser) -> None:
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--control", choices=CONTROLS)
    modes.add_argument("--candidate", type=Path, help="accepted exp-113 parent packet")
    parser.add_argument("--timeout-seconds", type=int, required=True)
    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)


def validate_timeout(parser: argparse.ArgumentParser, seconds: int) -> None:
    if not 1 <= seconds <= PROCESS_CEILING_SECONDS:
        parser.error("timeout must be an integer from 1 to 120 seconds")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packet", type=Path)
    add_mode_arguments(parser)
    args = parser.parse_args(argv)
    validate_timeout(parser, args.timeout_seconds)
    try:
        if args.worker:
            return bounded_worker(
                lambda: replay_packet(
                    load_packet(args.packet),
                    control=args.control,
                    parent=None if args.candidate is None else load_packet(args.candidate),
                ),
                args.timeout_seconds,
            )
        arguments = [str(args.packet), "--timeout-seconds", str(args.timeout_seconds)]
        arguments.extend(
            ["--candidate", str(args.candidate)]
            if args.candidate is not None
            else ["--control", args.control]
        )
        return bounded_child(
            "devtools.check_full_size_density_faces", arguments, args.timeout_seconds
        )
    except subprocess.TimeoutExpired, TimeoutError:
        print("unresolved: process wall cap expired", file=sys.stderr)
        return 1
    except (SupportError, OSError, ValueError) as error:
        print(f"refused: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
