#!/usr/bin/env python3
"""Run and replay resumable full-pose basin endpoint observations.

This is deliberately an *event* producer, not a basin counter.  Each completed seed
retains the start, full endpoint pose, quench termination data, canonical diagnostics,
and an independent ``sqpack.verify`` screen.  Connected-component classification and
unseen-mass inference are later derived steps; this file never promotes an endpoint key
to a basin by itself.

Examples::

    uv run --frozen python tools/basin_census.py --selftest
    uv run --frozen python tools/basin_census.py run --n 5 --seeds 0 \
      --output /tmp/n5.jsonl
    uv run --frozen python tools/basin_census.py replay /tmp/n5.jsonl
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import sys
import tempfile
from pathlib import Path
from typing import Any

import yaml
from strif import atomic_output_file

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from sqpack.canonical import canonical_key
from sqpack.quench import QuenchResult, quench_bracket
from sqpack.verify import corners_from_poses, float_sign, verify_packing

CONTRACT = "packing.squares:BasinEvent/v1"
REGIME = "uniform-independent-v1+quench-bracket-v1"
ORACLE_TOL = 1e-10


class EventError(ValueError):
    """A retained event is incomplete, inconsistent, or invalid."""


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode()).hexdigest()


def standing_side(n: int) -> float:
    path = ROOT / "frontier" / f"n-{n:03d}.md"
    if not path.exists():
        raise EventError(f"no frontier artifact for n={n}")
    text = path.read_text()
    front = yaml.safe_load(text.split("---\n")[1])
    return float(front["packing"]["upper_bound"]["value"])


def deterministic_start(n: int, seed: int, side: float) -> tuple[list[float], ...]:
    """One independently addressable draw from the declared proposer."""
    if side <= 1:
        raise EventError(f"start side must exceed 1, got {side}")
    rng = random.Random(1_000_003 * n + seed)
    return (
        [rng.uniform(0.5, side - 0.5) for _ in range(n)],
        [rng.uniform(0.5, side - 0.5) for _ in range(n)],
        [rng.uniform(0, math.pi / 2) for _ in range(n)],
    )


def enclosing_side(x: list[float], y: list[float], theta: list[float]) -> float:
    half = [0.5 * (abs(math.cos(t)) + abs(math.sin(t))) for t in theta]
    return max(
        max(a + h for a, h in zip(x, half, strict=True))
        - min(a - h for a, h in zip(x, half, strict=True)),
        max(b + h for b, h in zip(y, half, strict=True))
        - min(b - h for b, h in zip(y, half, strict=True)),
    )


def normalize(x: list[float], y: list[float], theta: list[float]) -> tuple[list[float], ...]:
    half = [0.5 * (abs(math.cos(t)) + abs(math.sin(t))) for t in theta]
    lo_x = min(a - h for a, h in zip(x, half, strict=True))
    lo_y = min(b - h for b, h in zip(y, half, strict=True))
    return [a - lo_x for a in x], [b - lo_y for b in y]


def screen_pose(pose: dict[str, Any]) -> dict[str, Any]:
    x = [float(v) for v in pose["x"]]
    y = [float(v) for v in pose["y"]]
    theta = [float(v) for v in pose["theta"]]
    side = float(pose["side"])
    if not (len(x) == len(y) == len(theta) and x):
        raise EventError("pose arrays must have one common non-zero length")
    if not all(math.isfinite(v) for v in [side, *x, *y, *theta]):
        raise EventError("pose contains a non-finite value")
    actual = enclosing_side(x, y, theta)
    nx, ny = normalize(x, y, theta)
    report = verify_packing(
        corners_from_poses(nx, ny, theta),
        side + ORACLE_TOL,
        sign=float_sign(ORACLE_TOL),
    )
    failures = [f"{kind}: {detail}" for kind, detail in report.failures]
    if actual > side + ORACLE_TOL:
        failures.append(f"reported side {side:.17g} but pose needs {actual:.17g}")
    return {
        "oracle": "sqpack.verify/f64-tol-1e-10",
        "valid": not failures,
        "required_side": actual,
        "reported_minus_required": side - actual,
        "pairs_tested": report.pairs_tested,
        "touching_pairs": report.touching_pairs,
        "failures": failures,
    }


def result_fields(result: QuenchResult) -> dict[str, Any]:
    return {
        "side": result.side,
        "x": result.x,
        "y": result.y,
        "theta": result.theta,
    }


def make_event(
    n: int,
    seed: int,
    *,
    start_side: float,
    time_budget: float,
) -> dict[str, Any]:
    start_x, start_y, start_theta = deterministic_start(n, seed, start_side)
    result = quench_bracket(
        start_x,
        start_y,
        start_theta,
        time_budget=time_budget,
    )
    pose = result_fields(result)
    verification = screen_pose(pose)
    key = canonical_key(result.x, result.y, result.theta, result.side)
    regime = {
        "id": REGIME,
        "start_side": start_side,
        "quench_time_budget_seconds": time_budget,
        "oracle_tolerance": ORACLE_TOL,
    }
    event_id = digest({"contract": CONTRACT, "regime": regime, "n": n, "seed": seed})
    event = {
        "contract": CONTRACT,
        "event_id": event_id,
        "n": n,
        "seed": seed,
        "regime": regime,
        "start": {"x": start_x, "y": start_y, "theta": start_theta},
        "endpoint": pose,
        "termination": {
            "producer_converged": result.converged,
            "reason": result.reason,
            "lp_solves": result.lp_solves,
            "angle_steps": result.angle_steps,
            "cell_changes": result.cell_changes,
            # ``converged`` is now unreachable unless every fixed-cell evaluation used
            # by the quench settled; D-132's typed result is the enforcement boundary.
            "fixed_cell_settlement_certified": result.converged,
        },
        "verification": verification,
        "endpoint_key": {
            "geometric": key.geometric,
            "contact": key.contact,
            "side": key.side,
            "angle_signature": list(key.angle_signature),
            "contact_count": key.contact_count,
        },
    }
    validate_event(event)
    return event


def validate_event(event: dict[str, Any]) -> None:
    required = {
        "contract",
        "event_id",
        "n",
        "seed",
        "regime",
        "start",
        "endpoint",
        "termination",
        "verification",
        "endpoint_key",
    }
    if set(event) != required or event.get("contract") != CONTRACT:
        raise EventError("event has the wrong contract fields")
    n, seed = event["n"], event["seed"]
    if isinstance(n, bool) or not isinstance(n, int) or n < 1:
        raise EventError("event n must be a positive integer")
    if isinstance(seed, bool) or not isinstance(seed, int):
        raise EventError("event seed must be an integer")
    expected_id = digest(
        {"contract": CONTRACT, "regime": event["regime"], "n": n, "seed": seed}
    )
    if event["event_id"] != expected_id:
        raise EventError("event id does not bind its regime, n, and seed")

    expected_start = deterministic_start(n, seed, float(event["regime"]["start_side"]))
    retained_start = event["start"]
    if retained_start != {
        "x": expected_start[0],
        "y": expected_start[1],
        "theta": expected_start[2],
    }:
        raise EventError("retained start does not replay from n, seed, and regime")

    observed_screen = screen_pose(event["endpoint"])
    if event["verification"] != observed_screen:
        raise EventError("retained independent verification does not replay")
    if not observed_screen["valid"]:
        raise EventError("endpoint fails the independent validity screen")

    endpoint = event["endpoint"]
    key = canonical_key(endpoint["x"], endpoint["y"], endpoint["theta"], endpoint["side"])
    observed_key = {
        "geometric": key.geometric,
        "contact": key.contact,
        "side": key.side,
        "angle_signature": list(key.angle_signature),
        "contact_count": key.contact_count,
    }
    if event["endpoint_key"] != observed_key:
        raise EventError("retained endpoint key does not replay from the full pose")


def read_events(path: Path) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    if not path.exists():
        return events
    for line_number, line in enumerate(path.read_text().splitlines(), start=1):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
            if not isinstance(event, dict):
                raise EventError("event is not an object")
            validate_event(event)
        except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
            raise EventError(f"{path}:{line_number}: {exc}") from exc
        events.append(event)
    ids = [event["event_id"] for event in events]
    if len(ids) != len(set(ids)):
        raise EventError(f"{path}: duplicate event id")
    return events


def write_events(path: Path, events: list[dict[str, Any]]) -> None:
    with atomic_output_file(path, make_parents=True) as temporary:
        temporary.write_text("".join(canonical_json(event) + "\n" for event in events))


def parse_seeds(value: str) -> list[int]:
    seeds: list[int] = []
    for part in value.split(","):
        if "-" in part:
            lo, hi = (int(v) for v in part.split("-", 1))
            seeds.extend(range(lo, hi + 1))
        else:
            seeds.append(int(part))
    if not seeds or len(seeds) != len(set(seeds)):
        raise argparse.ArgumentTypeError("seeds must be a non-empty unique list/range")
    return seeds


def run(args: argparse.Namespace) -> int:
    path = Path(args.output)
    events = read_events(path)
    by_id = {event["event_id"]: event for event in events}
    start_side = args.start_side or standing_side(args.n) + 0.6
    regime = {
        "id": REGIME,
        "start_side": start_side,
        "quench_time_budget_seconds": args.time_budget,
        "oracle_tolerance": ORACLE_TOL,
    }
    for seed in args.seeds:
        event_id = digest({"contract": CONTRACT, "regime": regime, "n": args.n, "seed": seed})
        if event_id in by_id:
            print(f"SKIP n={args.n} seed={seed}: already retained")
            continue
        event = make_event(
            args.n,
            seed,
            start_side=start_side,
            time_budget=args.time_budget,
        )
        events.append(event)
        by_id[event_id] = event
        write_events(path, events)
        term = event["termination"]
        print(
            f"OK n={args.n} seed={seed} side={event['endpoint']['side']:.12f} "
            f"converged={term['producer_converged']} reason={term['reason']}"
        )
    print(f"RETAINED {len(events)} events in {path}")
    return 0


def selftest() -> None:
    valid_pose = {"side": 1.0, "x": [0.5], "y": [0.5], "theta": [0.0]}
    if not screen_pose(valid_pose)["valid"]:
        raise EventError("known valid one-square pose was rejected")
    invalid_pose = {
        "side": 1.0,
        "x": [0.5, 0.5],
        "y": [0.5, 0.5],
        "theta": [0.0, 0.0],
    }
    if screen_pose(invalid_pose)["valid"]:
        raise EventError("overlapping two-square pose was accepted")
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "events.jsonl"
        # No quench: construct the smallest valid replay fixture around the exact n=1
        # pose so this check remains sub-second.
        regime = {
            "id": REGIME,
            "start_side": 1.6,
            "quench_time_budget_seconds": 1.0,
            "oracle_tolerance": ORACLE_TOL,
        }
        start = deterministic_start(1, 0, 1.6)
        key = canonical_key([0.5], [0.5], [0.0], 1.0)
        event = {
            "contract": CONTRACT,
            "event_id": digest({"contract": CONTRACT, "regime": regime, "n": 1, "seed": 0}),
            "n": 1,
            "seed": 0,
            "regime": regime,
            "start": {"x": start[0], "y": start[1], "theta": start[2]},
            "endpoint": valid_pose,
            "termination": {
                "producer_converged": True,
                "reason": "selftest",
                "lp_solves": 0,
                "angle_steps": 0,
                "cell_changes": 0,
                "fixed_cell_settlement_certified": False,
            },
            "verification": screen_pose(valid_pose),
            "endpoint_key": {
                "geometric": key.geometric,
                "contact": key.contact,
                "side": key.side,
                "angle_signature": list(key.angle_signature),
                "contact_count": key.contact_count,
            },
        }
        write_events(path, [event])
        read_events(path)
        tampered = json.loads(path.read_text())
        tampered["endpoint"]["side"] = 0.9
        path.write_text(canonical_json(tampered) + "\n")
        try:
            read_events(path)
        except EventError:
            pass
        else:
            raise EventError("tampered endpoint replayed successfully")
    print("BASIN EVENT SELFTEST PASSED")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--selftest", action="store_true")
    sub = parser.add_subparsers(dest="command")
    run_parser = sub.add_parser("run")
    run_parser.add_argument("--n", type=int, required=True)
    run_parser.add_argument("--seeds", type=parse_seeds, required=True)
    run_parser.add_argument("--output", type=Path, required=True)
    run_parser.add_argument("--start-side", type=float)
    run_parser.add_argument("--time-budget", type=float, default=30.0)
    replay_parser = sub.add_parser("replay")
    replay_parser.add_argument("path", type=Path)
    args = parser.parse_args()
    if args.selftest:
        selftest()
        return 0
    if args.command == "run":
        return run(args)
    if args.command == "replay":
        events = read_events(args.path)
        print(f"REPLAYED {len(events)} basin events from {args.path}")
        return 0
    parser.error("choose --selftest, run, or replay")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
