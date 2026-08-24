#!/usr/bin/env python3
"""Run and replay resumable full-pose basin endpoint observations.

This is deliberately an *event* producer, not a basin counter.  Each completed seed
retains the start, full endpoint pose, quench termination data, canonical diagnostics,
and an independent ``sqpack.verify`` screen.  Connected-component classification and
unseen-mass inference are later derived steps; this file never promotes an endpoint key
to a basin by itself.

Examples::

    uv run --frozen python -m cases.campaign_smoke.basin_events --selftest
    uv run --frozen python -m cases.campaign_smoke.basin_events run --n 5 --seeds 0 \
      --output /tmp/n5.jsonl
    uv run --frozen python -m cases.campaign_smoke.basin_events run --n 10 --seeds 0 \
      --start-source gobel10-svg-v1 --perturbation-scale 1e-4 \
      --output /tmp/n10.jsonl
    uv run --frozen python -m cases.campaign_smoke.basin_events replay /tmp/n5.jsonl
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import tempfile
import time
from collections.abc import Mapping
from pathlib import Path
from typing import Any

import yaml
from strif import atomic_output_file

from cases.gobel10.packing import (
    SOURCE_ID as GOBEL10_SOURCE_ID,
)
from cases.gobel10.packing import (
    SOURCE_SHA256 as GOBEL10_SOURCE_SHA256,
)
from cases.gobel10.packing import (
    SOURCE_URL as GOBEL10_SOURCE_URL,
)
from cases.gobel10.packing import (
    pose as gobel10_pose,
)
from sqpack.research.canonical import canonical_key
from sqpack.research.quench import QuenchResult, quench_bracket
from sqpack.verify import corners_from_poses, float_sign, verify_packing

ROOT = Path(__file__).resolve().parents[2]
CONTRACT_V2 = "packing.squares:BasinEvent/v2"
CONTRACT = "packing.squares:BasinEvent/v3"
REGIME = "uniform-independent-v1+quench-bracket-v1"
SOURCE_REGIME = "source-perturbation-v1+quench-bracket-v1"
ORACLE_TOL = 1e-10


class EventError(ValueError):
    """A retained event is incomplete or internally inconsistent."""


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


def deterministic_source_start(
    n: int,
    seed: int,
    source_id: str,
    perturbation_scale: float,
) -> tuple[list[float], ...]:
    """Replay one bounded perturbation of a named, source-bound reference pose."""
    if source_id != GOBEL10_SOURCE_ID or n != 10:
        raise EventError(f"source {source_id!r} does not define a pose for n={n}")
    if (
        not math.isfinite(perturbation_scale)
        or perturbation_scale <= 0
        or perturbation_scale > 1e-2
    ):
        raise EventError("source perturbation scale must be in (0, 1e-2]")
    base = gobel10_pose()
    x = [float(value) for value in base["x"]]
    y = [float(value) for value in base["y"]]
    theta = [float(value) for value in base["theta"]]
    rng = random.Random(9_000_031 * n + seed)
    return (
        [value + rng.uniform(-perturbation_scale, perturbation_scale) for value in x],
        [value + rng.uniform(-perturbation_scale, perturbation_scale) for value in y],
        [value + rng.uniform(-perturbation_scale, perturbation_scale) for value in theta],
    )


def make_regime(
    n: int,
    *,
    start_side: float | None,
    time_budget: float,
    start_source: str | None,
    perturbation_scale: float | None,
) -> dict[str, Any]:
    """Build the complete replay recipe for one event start."""
    if not math.isfinite(time_budget) or time_budget <= 0:
        raise EventError("quench time budget must be finite and positive")
    if start_source is None:
        if perturbation_scale is not None:
            raise EventError("--perturbation-scale requires --start-source")
        resolved_side = start_side if start_side is not None else standing_side(n) + 0.6
        return {
            "id": REGIME,
            "start_side": resolved_side,
            "quench_time_budget_seconds": time_budget,
            "oracle_tolerance": ORACLE_TOL,
        }
    if start_side is not None:
        raise EventError("--start-side cannot be combined with --start-source")
    scale = perturbation_scale if perturbation_scale is not None else 1e-3
    if start_source != GOBEL10_SOURCE_ID or n != 10:
        raise EventError(f"source {start_source!r} does not define a pose for n={n}")
    if not math.isfinite(scale) or scale <= 0 or scale > 1e-2:
        raise EventError("source perturbation scale must be in (0, 1e-2]")
    base_side = float(gobel10_pose()["side"])
    return {
        "id": SOURCE_REGIME,
        "start_side": base_side + 4.0 * scale,
        "quench_time_budget_seconds": time_budget,
        "oracle_tolerance": ORACLE_TOL,
        "source_id": GOBEL10_SOURCE_ID,
        "source_url": GOBEL10_SOURCE_URL,
        "source_sha256": GOBEL10_SOURCE_SHA256,
        "perturbation_scale": scale,
    }


def start_from_regime(
    n: int,
    seed: int,
    regime: dict[str, Any],
) -> tuple[list[float], ...]:
    """Validate a retained regime and replay its start exactly."""
    regime_id = regime.get("id")
    common = {
        "id",
        "start_side",
        "quench_time_budget_seconds",
        "oracle_tolerance",
    }
    if regime_id == REGIME:
        if set(regime) != common:
            raise EventError("uniform-independent regime has the wrong fields")
        start_side = regime["start_side"]
        if (
            isinstance(start_side, bool)
            or not isinstance(start_side, (int, float))
            or not math.isfinite(start_side)
            or start_side <= 1
        ):
            raise EventError("uniform-independent start side must be finite and exceed 1")
        start = deterministic_start(n, seed, float(start_side))
    elif regime_id == SOURCE_REGIME:
        expected_fields = common | {
            "source_id",
            "source_url",
            "source_sha256",
            "perturbation_scale",
        }
        if set(regime) != expected_fields:
            raise EventError("source-perturbation regime has the wrong fields")
        if (
            regime["source_id"] != GOBEL10_SOURCE_ID
            or regime["source_url"] != GOBEL10_SOURCE_URL
            or regime["source_sha256"] != GOBEL10_SOURCE_SHA256
        ):
            raise EventError("source-perturbation regime is not bound to the Göbel fixture")
        scale = regime["perturbation_scale"]
        if (
            isinstance(scale, bool)
            or not isinstance(scale, (int, float))
            or not math.isfinite(scale)
            or scale <= 0
            or scale > 1e-2
        ):
            raise EventError("source perturbation scale must be in (0, 1e-2]")
        expected_side = float(gobel10_pose()["side"]) + 4.0 * float(scale)
        if regime["start_side"] != expected_side:
            raise EventError("source start side does not derive from its perturbation scale")
        start = deterministic_source_start(n, seed, GOBEL10_SOURCE_ID, float(scale))
        if enclosing_side(*start) > expected_side + 1e-12:
            raise EventError("source perturbation exceeds its declared start side")
    else:
        raise EventError(f"unknown event regime {regime_id!r}")
    budget = regime["quench_time_budget_seconds"]
    if (
        isinstance(budget, bool)
        or not isinstance(budget, (int, float))
        or not math.isfinite(budget)
        or budget <= 0
    ):
        raise EventError("quench time budget must be finite and positive")
    if regime["oracle_tolerance"] != ORACLE_TOL:
        raise EventError("event regime changes the independent oracle tolerance")
    return start


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


def screen_pose(pose: Mapping[str, Any]) -> dict[str, Any]:
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
    regime: dict[str, Any],
) -> dict[str, Any]:
    start_x, start_y, start_theta = start_from_regime(n, seed, regime)
    time_budget = float(regime["quench_time_budget_seconds"])
    started = time.monotonic()
    result = quench_bracket(
        start_x,
        start_y,
        start_theta,
        time_budget=time_budget,
    )
    wall_seconds = time.monotonic() - started
    pose = result_fields(result)
    verification = screen_pose(pose)
    key = canonical_key(result.x, result.y, result.theta, result.side)
    event_id = digest({"contract": CONTRACT, "regime": regime, "n": n, "seed": seed})
    all_accounted = (
        result.fixed_point_evaluations > 0
        and result.fixed_point_evaluations
        == result.fixed_point_settled + result.fixed_point_unsettled
    )
    promotion_blockers = []
    if not result.converged:
        promotion_blockers.append("producer_not_converged")
    if result.fixed_point_unsettled:
        promotion_blockers.append("unsettled_fixed_point_evaluation")
    if not verification["valid"]:
        promotion_blockers.append("independent_validity_failure")
    scientifically_admissible = (
        result.converged
        and all_accounted
        and result.fixed_point_unsettled == 0
        and verification["valid"]
    )
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
            "wall_seconds": wall_seconds,
            "fixed_point_evaluations": result.fixed_point_evaluations,
            "fixed_point_settled": result.fixed_point_settled,
            "fixed_point_unsettled": result.fixed_point_unsettled,
            "all_probe_evaluations_accounted_for": all_accounted,
            "scientifically_admissible_terminal_event": scientifically_admissible,
            "promotion_blockers": promotion_blockers,
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
    contract = event.get("contract")
    if set(event) != required or contract not in {CONTRACT_V2, CONTRACT}:
        raise EventError("event has the wrong contract fields")
    n, seed = event["n"], event["seed"]
    if isinstance(n, bool) or not isinstance(n, int) or n < 1:
        raise EventError("event n must be a positive integer")
    if isinstance(seed, bool) or not isinstance(seed, int):
        raise EventError("event seed must be an integer")
    regime = event["regime"]
    if not isinstance(regime, dict):
        raise EventError("event regime must be an object")
    expected_start = start_from_regime(n, seed, regime)
    expected_id = digest({"contract": contract, "regime": regime, "n": n, "seed": seed})
    if event["event_id"] != expected_id:
        raise EventError("event id does not bind its regime, n, and seed")

    termination = event["termination"]
    expected_termination_fields = {
        "producer_converged",
        "reason",
        "lp_solves",
        "angle_steps",
        "cell_changes",
        "wall_seconds",
        "all_probe_evaluations_accounted_for",
        "scientifically_admissible_terminal_event",
        "promotion_blockers",
    }
    if contract == CONTRACT:
        expected_termination_fields |= {
            "fixed_point_evaluations",
            "fixed_point_settled",
            "fixed_point_unsettled",
        }
    if set(termination) != expected_termination_fields:
        raise EventError("termination evidence has the wrong fields")
    if contract == CONTRACT_V2 and (
        termination["all_probe_evaluations_accounted_for"] is not False
        or termination["scientifically_admissible_terminal_event"] is not False
        or termination["promotion_blockers"] != ["D-165"]
    ):
        raise EventError("current quench events must remain blocked by D-165")
    if contract == CONTRACT:
        counts = [
            termination["fixed_point_evaluations"],
            termination["fixed_point_settled"],
            termination["fixed_point_unsettled"],
        ]
        if any(
            isinstance(value, bool) or not isinstance(value, int) or value < 0
            for value in counts
        ):
            raise EventError("fixed-point receipt counts must be non-negative integers")
    if (
        isinstance(termination["wall_seconds"], bool)
        or not isinstance(termination["wall_seconds"], (int, float))
        or not math.isfinite(termination["wall_seconds"])
        or termination["wall_seconds"] < 0
    ):
        raise EventError("termination wall_seconds must be finite and non-negative")

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
    if contract == CONTRACT_V2 and not observed_screen["valid"]:
        raise EventError("historical v2 endpoint fails the independent validity screen")

    if contract == CONTRACT:
        evaluations = termination["fixed_point_evaluations"]
        settled = termination["fixed_point_settled"]
        unsettled = termination["fixed_point_unsettled"]
        expected_accounted = evaluations > 0 and evaluations == settled + unsettled
        expected_blockers = []
        if not termination["producer_converged"]:
            expected_blockers.append("producer_not_converged")
        if unsettled:
            expected_blockers.append("unsettled_fixed_point_evaluation")
        if not observed_screen["valid"]:
            expected_blockers.append("independent_validity_failure")
        expected_admissible = (
            termination["producer_converged"]
            and expected_accounted
            and unsettled == 0
            and observed_screen["valid"]
        )
        if termination["all_probe_evaluations_accounted_for"] is not expected_accounted:
            raise EventError("all-probes-accounted claim does not derive from the receipt")
        if termination["scientifically_admissible_terminal_event"] is not expected_admissible:
            raise EventError("scientific-admissibility claim does not derive from the evidence")
        if termination["promotion_blockers"] != expected_blockers:
            raise EventError("promotion blockers do not derive from the stopping evidence")

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


def retain_event(
    path: Path,
    events: list[dict[str, Any]],
    by_id: dict[str, dict[str, Any]],
    event: dict[str, Any],
) -> None:
    """Validate and atomically append one terminal outcome to a resumable archive."""
    validate_event(event)
    event_id = event["event_id"]
    if event_id in by_id:
        raise EventError(f"duplicate event id {event_id}")
    events.append(event)
    by_id[event_id] = event
    write_events(path, events)


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
    regime = make_regime(
        args.n,
        start_side=args.start_side,
        time_budget=args.time_budget,
        start_source=args.start_source,
        perturbation_scale=args.perturbation_scale,
    )
    for seed in args.seeds:
        event_id = digest({"contract": CONTRACT, "regime": regime, "n": args.n, "seed": seed})
        if event_id in by_id:
            print(f"SKIP n={args.n} seed={seed}: already retained")
            continue
        event = make_event(
            args.n,
            seed,
            regime=regime,
        )
        retain_event(path, events, by_id, event)
        term = event["termination"]
        status = "OK" if term["scientifically_admissible_terminal_event"] else "STOP"
        print(
            f"{status} n={args.n} seed={seed} side={event['endpoint']['side']:.12f} "
            f"converged={term['producer_converged']} "
            f"valid={event['verification']['valid']} "
            f"blockers={term['promotion_blockers']} reason={term['reason']}"
        )
    print(f"RETAINED {len(events)} events in {path}")
    return 0


def selftest() -> None:
    valid_pose = {"side": 1.0, "x": [0.5], "y": [0.5], "theta": [0.0]}
    if not screen_pose(valid_pose)["valid"]:
        raise EventError("known valid one-square pose was rejected")
    audited = quench_bracket([0.5], [0.5], [0.0], time_budget=1.0)
    if (
        audited.fixed_point_evaluations <= 0
        or audited.fixed_point_evaluations
        != audited.fixed_point_settled + audited.fixed_point_unsettled
    ):
        raise EventError("quench fixed-point receipt is incomplete")
    invalid_pose = {
        "side": 1.0,
        "x": [0.5, 0.5],
        "y": [0.5, 0.5],
        "theta": [0.0, 0.0],
    }
    if screen_pose(invalid_pose)["valid"]:
        raise EventError("overlapping two-square pose was accepted")
    source_pose = gobel10_pose()
    if not screen_pose(source_pose)["valid"]:
        raise EventError("source-bound Göbel n=10 pose was rejected")
    source_regime = make_regime(
        10,
        start_side=None,
        time_budget=1.0,
        start_source=GOBEL10_SOURCE_ID,
        perturbation_scale=1e-4,
    )
    source_start = start_from_regime(10, 0, source_regime)
    if source_start != deterministic_source_start(10, 0, GOBEL10_SOURCE_ID, 1e-4):
        raise EventError("source-bound start is not deterministic")
    if source_start[0] == source_pose["x"]:
        raise EventError("source-bound start did not perturb the reference pose")
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
                "wall_seconds": 0.0,
                "fixed_point_evaluations": 1,
                "fixed_point_settled": 1,
                "fixed_point_unsettled": 0,
                "all_probe_evaluations_accounted_for": True,
                "scientifically_admissible_terminal_event": True,
                "promotion_blockers": [],
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
        event["endpoint"] = valid_pose
        event["termination"]["all_probe_evaluations_accounted_for"] = False
        write_events(path, [event])
        try:
            read_events(path)
        except EventError:
            pass
        else:
            raise EventError("forged all-probes-accounted claim replayed successfully")
        event["termination"]["all_probe_evaluations_accounted_for"] = True
        event["termination"]["wall_seconds"] = -1.0
        write_events(path, [event])
        try:
            read_events(path)
        except EventError:
            pass
        else:
            raise EventError("negative event wall time replayed successfully")

        source_key = canonical_key(
            source_pose["x"],
            source_pose["y"],
            source_pose["theta"],
            source_pose["side"],
        )
        source_event = {
            "contract": CONTRACT,
            "event_id": digest(
                {"contract": CONTRACT, "regime": source_regime, "n": 10, "seed": 0}
            ),
            "n": 10,
            "seed": 0,
            "regime": source_regime,
            "start": {
                "x": source_start[0],
                "y": source_start[1],
                "theta": source_start[2],
            },
            "endpoint": source_pose,
            "termination": {
                "producer_converged": True,
                "reason": "source-bound selftest",
                "lp_solves": 1,
                "angle_steps": 0,
                "cell_changes": 0,
                "wall_seconds": 0.0,
                "fixed_point_evaluations": 1,
                "fixed_point_settled": 1,
                "fixed_point_unsettled": 0,
                "all_probe_evaluations_accounted_for": True,
                "scientifically_admissible_terminal_event": True,
                "promotion_blockers": [],
            },
            "verification": screen_pose(source_pose),
            "endpoint_key": {
                "geometric": source_key.geometric,
                "contact": source_key.contact,
                "side": source_key.side,
                "angle_signature": list(source_key.angle_signature),
                "contact_count": source_key.contact_count,
            },
        }
        write_events(path, [source_event])
        if read_events(path) != [source_event]:
            raise EventError("source-bound event did not replay")
        tampered_source = json.loads(canonical_json(source_event))
        tampered_source["regime"]["source_sha256"] = "0" * 64
        write_events(path, [tampered_source])
        try:
            read_events(path)
        except EventError:
            pass
        else:
            raise EventError("source-bound event accepted a changed source digest")
        tampered_start = json.loads(canonical_json(source_event))
        tampered_start["start"]["x"][0] += 1e-6
        write_events(path, [tampered_start])
        try:
            read_events(path)
        except EventError:
            pass
        else:
            raise EventError("source-bound event accepted a changed retained start")

        invalid_start = deterministic_start(2, 1, 1.6)
        invalid_key = canonical_key(
            invalid_pose["x"],
            invalid_pose["y"],
            invalid_pose["theta"],
            invalid_pose["side"],
        )
        blocked = {
            "contract": CONTRACT,
            "event_id": digest({"contract": CONTRACT, "regime": regime, "n": 2, "seed": 1}),
            "n": 2,
            "seed": 1,
            "regime": regime,
            "start": {
                "x": invalid_start[0],
                "y": invalid_start[1],
                "theta": invalid_start[2],
            },
            "endpoint": invalid_pose,
            "termination": {
                "producer_converged": True,
                "reason": "selftest invalid endpoint",
                "lp_solves": 1,
                "angle_steps": 0,
                "cell_changes": 0,
                "wall_seconds": 0.0,
                "fixed_point_evaluations": 1,
                "fixed_point_settled": 1,
                "fixed_point_unsettled": 0,
                "all_probe_evaluations_accounted_for": True,
                "scientifically_admissible_terminal_event": False,
                "promotion_blockers": ["independent_validity_failure"],
            },
            "verification": screen_pose(invalid_pose),
            "endpoint_key": {
                "geometric": invalid_key.geometric,
                "contact": invalid_key.contact,
                "side": invalid_key.side,
                "angle_signature": list(invalid_key.angle_signature),
                "contact_count": invalid_key.contact_count,
            },
        }
        retained: list[dict[str, Any]] = []
        retained_by_id: dict[str, dict[str, Any]] = {}
        retain_event(path, retained, retained_by_id, blocked)
        if read_events(path) != [blocked]:
            raise EventError("invalid endpoint did not survive the run-path retention helper")
        blocked["termination"]["scientifically_admissible_terminal_event"] = True
        write_events(path, [blocked])
        try:
            read_events(path)
        except EventError:
            pass
        else:
            raise EventError("invalid endpoint forged scientific admissibility")
        blocked["termination"]["scientifically_admissible_terminal_event"] = False
        blocked["termination"]["promotion_blockers"] = []
        write_events(path, [blocked])
        try:
            read_events(path)
        except EventError:
            pass
        else:
            raise EventError("invalid endpoint omitted its promotion blocker")
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
    run_parser.add_argument("--start-source", choices=[GOBEL10_SOURCE_ID])
    run_parser.add_argument("--perturbation-scale", type=float)
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
