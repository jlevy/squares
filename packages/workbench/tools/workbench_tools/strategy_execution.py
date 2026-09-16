"""Execute typed packing strategies with checked phase and final receipts."""

from __future__ import annotations

import argparse
import json
import math
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

from devtools.divide_and_concur import Array, violation
from devtools.known_structure import (
    angle_classes,
    assemble_from_faces,
    contact_edges,
    contact_kinds,
    record,
    rewired,
    thinned,
    wall_contacts,
)
from devtools.run_projection_ratchet import guide_home, match_targets, ratchet, solve
from devtools.sweep_structure_hints import orientation_classes
from workbench_tools.animation_records import (
    ANIMATION_CONTRACT,
    AnimationDocument,
    animation_to_json,
    decode_animation,
)
from workbench_tools.packing_contracts import (
    DEFAULT_VALIDITY_TOLERANCE,
    GeometryCheck,
    GeometryIssue,
    check_unit_square_packing,
)
from workbench_tools.strategy_records import (
    STRATEGY_RUN_CONTRACT,
    Mechanism,
    PackingStrategy,
    StrategyPhase,
    StrategyPhaseReceipt,
    StrategyRun,
    StrategyTraceFrame,
    choose_seed,
    decode_legacy_strategy,
    load_strategy,
    materialize_configuration,
    strategy_to_row,
)


@dataclass(frozen=True, slots=True)
class TraceSnapshot:
    side: float
    poses: Array


@dataclass(slots=True)
class PhaseDetails:
    solved: bool | None = None
    steps: int | None = None
    calls: int | None = None
    settled: bool | None = None
    residual: float | None = None


@dataclass(slots=True)
class State:
    """Mutable execution state used only while the phase sequence is running."""

    configuration: PackingStrategy
    poses: Array
    side: float
    capture_trace: bool = False
    contacts: list[tuple[int, int]] | None = None
    classes: list[list[int]] | None = None
    walls: list[int] | None = None
    rung: str = "none"
    guided: bool = False
    answer_sources: set[str] = field(default_factory=set)
    trace: list[TraceSnapshot] = field(default_factory=list)
    animation: list[StrategyTraceFrame] = field(default_factory=list)
    phases: list[StrategyPhaseReceipt] = field(default_factory=list)
    details: PhaseDetails = field(default_factory=PhaseDetails)

    @property
    def n(self) -> int:
        return self.configuration.n

    @property
    def seed(self) -> int:
        seed = self.configuration.seed
        if seed is None:
            raise AssertionError("effective strategy configuration has no seed")
        return seed


def _structure(state: State, phase: StrategyPhase, rng: np.random.Generator) -> None:
    spec = phase.structure
    if spec is None:
        return
    source = spec.source or "record"
    if source != "record":
        raise ValueError(f"structure source {source!r} is not implemented")
    state.rung = spec.rung
    state.contacts, state.classes, state.walls = None, None, None
    if spec.rung == "none":
        return

    poses, side = record(state.n)
    state.answer_sources.add(f"record-structure:{spec.rung}")
    edges = contact_edges(poses)
    kinds = contact_kinds(poses)
    control = spec.control or "none"
    keep = spec.keep if spec.keep is not None else 0
    if control == "thinned":
        edges = thinned(edges, keep, rng)
    elif control == "rewired":
        edges = rewired(edges, state.n, keep, rng)

    if spec.rung == "partition":
        state.classes = angle_classes(poses)
    elif spec.rung == "contact-graph":
        state.contacts = edges
    elif spec.rung == "contact-graph-with-types":
        state.contacts = edges
        state.classes = orientation_classes(edges, kinds, state.n)
    elif spec.rung == "with-wall-contacts":
        state.contacts = edges
        state.classes = orientation_classes(edges, kinds, state.n)
        state.walls = wall_contacts(poses, side)


def _side_for(state: State, phase: StrategyPhase) -> float:
    spec = phase.side
    if spec is None:
        return state.side
    relative_to = spec.relative_to or "current"
    if relative_to == "record":
        state.answer_sources.add("record-side")
        base = record(state.n)[1]
    elif relative_to == "grid":
        base = float(math.ceil(math.sqrt(state.n)))
    else:
        base = state.side
    return base * (1.0 if spec.factor is None else spec.factor)


def _grid_poses(n: int, side: float) -> Array:
    if not math.isfinite(side) or side <= 0:
        raise ValueError("grid side must be finite and positive")
    width = math.floor(side)
    if width * width < n:
        raise ValueError(f"grid side {side} has {width * width} cells for {n} squares")
    cells = [(i, j) for j in range(width) for i in range(width)][:n]
    return np.array([[i + 0.5, j + 0.5, 0.0] for i, j in cells], dtype=np.float64)


def _run_scatter(state: State, phase: StrategyPhase, rng: np.random.Generator) -> None:
    side = _side_for(state, phase)
    if side < 1:
        raise ValueError("scatter side must be at least one unit")
    state.side = side
    state.poses = np.stack(
        [
            rng.uniform(0.5, side - 0.5, state.n),
            rng.uniform(0.5, side - 0.5, state.n),
            rng.uniform(0, np.pi / 2, state.n),
        ],
        axis=-1,
    )


def _run_grid(state: State, phase: StrategyPhase, _rng: np.random.Generator) -> None:
    state.side = (
        float(math.ceil(math.sqrt(state.n))) if phase.side is None else _side_for(state, phase)
    )
    state.poses = _grid_poses(state.n, state.side)


def _run_assemble(state: State, phase: StrategyPhase, rng: np.random.Generator) -> None:
    poses, _ = record(state.n)
    state.answer_sources.add("record-assembly")
    state.side = _side_for(state, phase)
    state.poses = assemble_from_faces(
        state.n, contact_edges(poses), contact_kinds(poses), state.side, rng
    )


def _stop(phase: StrategyPhase, default_steps: int = 6000) -> tuple[int, int]:
    until = phase.until
    steps = default_steps if until is None or until.steps is None else until.steps
    stalled = (
        max(1, steps // 3) if until is None or until.stalled_for is None else until.stalled_for
    )
    return steps, stalled


def _run_project(state: State, phase: StrategyPhase, rng: np.random.Generator) -> None:
    constraints = phase.constraints
    steps, stalled = _stop(phase)
    state.side = _side_for(state, phase)
    trace: list[Array] | None = [] if state.capture_trace else None
    outcome = solve(
        state.n,
        state.side,
        rng,
        beta=0.1 if phase.relaxation is None else phase.relaxation,
        iters=steps,
        monotone=stalled,
        band=0.02 if constraints is None or constraints.band is None else constraints.band,
        contact_weight=(
            1.0 if constraints is None or constraints.weight is None else constraints.weight
        ),
        classes=state.classes,
        contacts=state.contacts,
        walls=state.walls,
        start=state.poses,
        trace=trace,
    )
    state.trace.extend(
        TraceSnapshot(side=state.side, poses=poses.copy()) for poses in trace or ()
    )
    state.poses = outcome.poses
    state.details.solved = bool(outcome.solved)
    state.details.steps = outcome.steps


def _run_relax(state: State, phase: StrategyPhase, rng: np.random.Generator) -> None:
    state.contacts, state.classes, state.walls = None, None, None
    state.rung = "none"
    _run_project(state, phase, rng)


def _run_ratchet(state: State, phase: StrategyPhase, rng: np.random.Generator) -> None:
    constraints = phase.constraints
    schedule = phase.schedule
    if schedule is None:
        raise AssertionError("effective ratchet configuration has no schedule")
    steps, stalled = _stop(phase)
    row = ratchet(
        state.n,
        rng,
        beta=0.1 if phase.relaxation is None else phase.relaxation,
        iters=steps,
        monotone=stalled,
        attempts=5 if schedule.attempts is None else schedule.attempts,
        steps=24 if schedule.attempts_ceiling is None else schedule.attempts_ceiling,
        floor=1e-3 if schedule.floor is None else schedule.floor,
        cold=0.0 if schedule.cold is None else schedule.cold,
        band=0.02 if constraints is None or constraints.band is None else constraints.band,
        contact_weight=(
            1.0 if constraints is None or constraints.weight is None else constraints.weight
        ),
        classes=state.classes,
        contacts=state.contacts,
        walls=state.walls,
        start_from=state.poses,
        start_side=state.side,
    )
    state.poses = np.asarray(row["poses"], dtype=np.float64)
    state.side = float(row["side"])
    state.details.calls = int(row["calls"])
    state.details.settled = bool(row.get("settled", True))


def _run_guide(state: State, phase: StrategyPhase, _rng: np.random.Generator) -> None:
    target = phase.target
    if target is None:
        raise AssertionError("effective guide configuration has no target")
    targets, side = record(state.n)
    state.answer_sources.add("record-target")
    if (target.match or "by-motion") == "by-motion":
        targets, _spare = match_targets(state.poses, targets)
    state.side = side
    trace: list[Array] | None = [] if state.capture_trace else None
    landed, _frames = guide_home(
        state.n,
        side,
        state.poses,
        targets,
        steps=400 if target.steps is None else target.steps,
        pull_to=5.0 if target.pull is None else target.pull,
        trace=trace,
    )
    state.trace.extend(TraceSnapshot(side=side, poses=poses.copy()) for poses in trace or ())
    state.poses = landed
    state.guided = True
    state.details.residual = float(np.abs(landed[:, :2] - targets[:, :2]).max())


def _run_container(state: State, phase: StrategyPhase, _rng: np.random.Generator) -> None:
    previous_side = state.side
    state.side = _side_for(state, phase)
    if previous_side <= 0:
        return
    factor = state.side / previous_side
    moved = state.poses.copy()
    moved[:, :2] = (state.poses[:, :2] - previous_side / 2) * factor + state.side / 2
    state.poses = moved
    frames = 24 if phase.until is None or phase.until.frames is None else phase.until.frames
    for step in range(1, frames + 1):
        u = step / frames
        ease = u * u * (3 - 2 * u)
        between = state.poses.copy()
        side_now = previous_side + ease * (state.side - previous_side)
        between[:, :2] = (state.poses[:, :2] - state.side / 2) * (side_now / state.side)
        between[:, :2] += side_now / 2
        if state.capture_trace:
            state.trace.append(TraceSnapshot(side=side_now, poses=between))


type PhaseRunner = Callable[[State, StrategyPhase, np.random.Generator], None]

MECHANISMS: dict[Mechanism, PhaseRunner] = {
    "container": _run_container,
    "scatter": _run_scatter,
    "grid": _run_grid,
    "assemble": _run_assemble,
    "project": _run_project,
    "relax": _run_relax,
    "ratchet": _run_ratchet,
    "guide": _run_guide,
}


def _require_finite_geometry(check: GeometryCheck, *, label: str) -> None:
    malformed = {GeometryIssue.SHAPE, GeometryIssue.COUNT, GeometryIssue.NONFINITE}
    if malformed.intersection(check.issues):
        raise ValueError(f"{label} must contain exactly the declared finite square poses")


def _check_state(state: State, *, label: str) -> GeometryCheck:
    check = check_unit_square_packing(
        state.poses,
        side=state.side,
        expected_count=state.n,
        tolerance=DEFAULT_VALIDITY_TOLERANCE,
    )
    _require_finite_geometry(check, label=label)
    return check


def run(
    strategy: object | PackingStrategy,
    *,
    keep_trace: bool = False,
    start: Array | None = None,
    start_side: float | None = None,
    seed_source: Callable[[], int] | None = None,
) -> State:
    """Execute phases in order and retain typed receipts for every result."""
    declared = decode_legacy_strategy(strategy)
    seed = choose_seed(declared, seed_source)
    configuration = materialize_configuration(
        declared,
        seed=seed,
        record_contact_count=lambda n: len(contact_edges(record(n)[0])),
    )
    n = configuration.n
    rng = np.random.default_rng(seed)
    side = float(math.ceil(math.sqrt(n))) if start_side is None else start_side
    poses = _grid_poses(n, side) if start is None else start
    start_check = check_unit_square_packing(
        poses,
        side=side,
        expected_count=n,
        tolerance=DEFAULT_VALIDITY_TOLERANCE,
    )
    _require_finite_geometry(start_check, label="strategy start")
    state = State(
        configuration=configuration,
        poses=np.asarray(poses, dtype=np.float64).copy(),
        side=float(side),
        capture_trace=keep_trace,
    )

    for index, phase in enumerate(configuration.phases):
        if phase.structure is not None:
            _structure(state, phase, rng)
        before = len(state.trace)
        state.details = PhaseDetails()
        MECHANISMS[phase.mechanism](state, phase, rng)
        phase_check = _check_state(state, label=f"{phase.mechanism} phase result")
        phase_label = phase.label or phase.mechanism
        for snapshot in state.trace[before:]:
            trace_check = check_unit_square_packing(
                snapshot.poses,
                side=snapshot.side,
                expected_count=state.n,
                tolerance=DEFAULT_VALIDITY_TOLERANCE,
            )
            _require_finite_geometry(trace_check, label=f"{phase.mechanism} trace frame")
            state.animation.append(
                StrategyTraceFrame(
                    side=snapshot.side,
                    poses=_poses(snapshot.poses),
                    phase=phase_label,
                    guided=state.guided,
                    geometry=trace_check,
                )
            )
        state.phases.append(
            StrategyPhaseReceipt(
                index=index,
                mechanism=phase.mechanism,
                label=phase_label,
                rung=state.rung,
                side=state.side,
                violation=float(violation(state.poses, state.side)),
                geometry=phase_check,
                frame_count=len(state.trace) - before,
                solved=state.details.solved,
                steps=state.details.steps,
                calls=state.details.calls,
                settled=state.details.settled,
                residual=state.details.residual,
            )
        )
    return state


def execute_strategy(
    strategy: object | PackingStrategy,
    *,
    keep_trace: bool = False,
    start: Array | None = None,
    start_side: float | None = None,
    seed_source: Callable[[], int] | None = None,
) -> StrategyRun:
    """Execute a strategy and expose only immutable checked result records."""
    state = run(
        strategy,
        keep_trace=keep_trace,
        start=start,
        start_side=start_side,
        seed_source=seed_source,
    )
    geometry = _check_state(state, label="strategy final result")
    return StrategyRun(
        contract=STRATEGY_RUN_CONTRACT,
        configuration=state.configuration,
        poses=_poses(state.poses),
        side=state.side,
        geometry=geometry,
        phases=tuple(state.phases),
        trace=tuple(state.animation),
        guided=state.guided,
        answer_sources=tuple(sorted(state.answer_sources)),
    )


def animation_document(
    strategy: object | PackingStrategy,
    state: State,
    *,
    duration_seconds: float = 5.0,
) -> AnimationDocument:
    """Turn one completed run into an explicitly versioned checked animation."""
    declared = decode_legacy_strategy(strategy)
    if declared.name != state.configuration.name or declared.n != state.n:
        raise ValueError("animation strategy does not match its execution state")
    final_check = _check_state(state, label="animation final frame")
    trace = state.animation or [
        StrategyTraceFrame(
            side=state.side,
            poses=_poses(state.poses),
            phase="final",
            guided=state.guided,
            geometry=final_check,
        )
    ]
    span = max(1, len(trace) - 1)
    known = record(state.n)[1]
    source: dict[str, object] = {
        "strategy": state.configuration.name,
        "seed": state.seed,
        "configuration": strategy_to_row(state.configuration),
    }
    if state.answer_sources:
        source["records"] = [state.n]
    row: dict[str, object] = {
        "contract": ANIMATION_CONTRACT,
        "name": state.configuration.name,
        "n": state.n,
        "guided": state.guided,
        "source": source,
        "duration_seconds": duration_seconds,
        "palette": {"hue": "angle-class", "shade": "full-side-contact"},
        "reference": {"best_known": float(known)},
        "frames": [
            {
                "t": index / span,
                "side": frame.side,
                "squares": [list(pose) for pose in frame.poses],
                "square_ids": list(range(1, state.n + 1)),
                "phase": frame.phase,
                "guided": frame.guided,
                "feasible": frame.geometry.passed,
            }
            for index, frame in enumerate(trace)
        ],
    }
    return decode_animation(row)


def _poses(values: Array) -> tuple[tuple[float, float, float], ...]:
    return tuple((float(pose[0]), float(pose[1]), float(pose[2])) for pose in values)


def _phase_payload(receipt: StrategyPhaseReceipt) -> dict[str, object]:
    return {
        "phase": receipt.index,
        "mechanism": receipt.mechanism,
        "label": receipt.label,
        "rung": receipt.rung,
        "side": receipt.side,
        "violation": receipt.violation,
        "packing_valid": receipt.geometry.passed,
        "frames": receipt.frame_count,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("strategy", type=Path)
    ap.add_argument("--trace", type=Path, default=None)
    ap.add_argument("--json", action="store_true")
    options = ap.parse_args()

    strategy = load_strategy(options.strategy)
    state = run(strategy, keep_trace=options.trace is not None)
    known = record(state.n)[1]
    packed = state.phases[-1].geometry.passed
    payload: dict[str, object] = {
        "name": strategy.name,
        "n": state.n,
        "side": state.side,
        # An excess over the record is a claim about a packing, so an arrangement that
        # failed the geometry check has none.
        "excess_pct": 100.0 * (state.side - known) / known if packed else None,
        "violation": state.phases[-1].violation,
        "packing_valid": packed,
        "guided": state.guided,
        "phases": [_phase_payload(phase) for phase in state.phases],
        "configuration": strategy_to_row(state.configuration),
    }
    if options.trace:
        options.trace.write_text(
            animation_to_json(animation_document(strategy, state)), encoding="utf-8"
        )
    if options.json:
        print(json.dumps(payload, allow_nan=False, sort_keys=True))
        return 0

    tag = "  [GUIDED, not a search result]" if state.guided else ""
    print(f"{strategy.name}  n = {state.n}{tag}")
    print(
        f"{'#':>2} {'mechanism':>10} {'rung':>26} {'side':>12} {'violation':>10} {'frames':>7}"
        f"  packing"
    )
    for phase in state.phases:
        print(
            f"{phase.index:>2} {phase.mechanism:>10} {phase.rung:>26} {phase.side:>12.7f} "
            f"{phase.violation:>10.1e} {phase.frame_count:>7}  "
            f"{'valid' if phase.geometry.passed else 'not a packing'}"
        )
    if packed:
        excess = 100.0 * (state.side - known) / known
        print(f"best known {known:.7f}, reached {state.side:.7f} ({excess:+.3f} %)")
    else:
        print(f"best known {known:.7f}; final side {state.side:.7f} is not a packing")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
