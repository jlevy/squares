#!/usr/bin/env python3
"""Execute a PackingStrategy: an ordered sequence of optimisation phases, declared as data.

The contract is `strategies/packing-strategy.schema.yaml`, and the point of having one is
that the same document runs in more than one place. Python executes it here, the workbench
plays it, and the Rust engine can read it through `serde` -- `jsonschema-rs` is already a
dependency, so the validation is shared too.

**`MECHANISMS` is the only place that knows how to run a phase.** That table is the seam:
a new mechanism, or a faster implementation of an existing one, is an entry rather than a
change to the executor, and the workbench discovers what is available from the schema
rather than from a hard-coded menu. It is also how the performance path stays honest -- a
Rust-backed `project` is a different implementation of the same phase, selected by a field,
so one strategy runs in both and the two compare on the same document.

Usage, from `packing/`:
    uv run --frozen python -m devtools.packing_strategy strategies/assemble-then-tighten.yaml
    uv run --frozen python -m devtools.packing_strategy FILE --trace /tmp/run.json
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import jsonschema
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
from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = ROOT / "strategies/packing-strategy.schema.yaml"


@dataclass
class State:
    """What one phase hands the next: an arrangement, a container, and what it was told."""

    n: int
    poses: Array
    side: float
    contacts: list[tuple[int, int]] | None = None
    classes: list[list[int]] | None = None
    walls: list[int] | None = None
    rung: str = "none"
    trace: list[Array] = field(default_factory=list)
    animation: list[dict[str, Any]] = field(default_factory=list)
    log: list[dict[str, Any]] = field(default_factory=list)


def _structure(state: State, spec: dict[str, Any], rng: np.random.Generator) -> None:
    """Read a rung of the ladder onto the state, with its control if one is asked for."""
    rung = spec["rung"]
    state.rung = rung
    if rung == "none":
        state.contacts, state.classes, state.walls = None, None, None
        return

    poses, side = record(state.n)
    edges = contact_edges(poses)
    kinds = contact_kinds(poses)
    control = spec.get("control", "none")
    if control == "thinned":
        edges = thinned(edges, spec.get("keep", len(edges) // 2), rng)
    elif control == "rewired":
        edges = rewired(edges, state.n, spec.get("keep", len(edges) // 4), rng)

    if rung == "partition":
        state.classes = angle_classes(poses)
        state.contacts = None
    elif rung == "contact-graph":
        state.contacts = edges
    elif rung == "contact-graph-with-types":
        # All contacts, not just the faces, and the basin map is why. Declaring every
        # contact holds the record exactly at n = 5, 10, 11 and 17; declaring only the
        # faces lets it drift and stop being a packing at 10 and 11, and never holds it at
        # 17. Faces-only settles a built assembly better and holds the answer worse, so
        # which subset a phase declares belongs in the strategy document rather than being
        # decided once here for every phase.
        state.contacts = edges
        state.classes = orientation_classes(edges, kinds, state.n)
    elif rung == "with-wall-contacts":
        state.contacts = edges
        state.classes = orientation_classes(edges, kinds, state.n)
        state.walls = wall_contacts(poses, side)


def _side_for(state: State, spec: dict[str, Any] | None) -> float:
    if not spec:
        return state.side
    base = {
        "record": lambda: record(state.n)[1],
        "grid": lambda: float(math.ceil(math.sqrt(state.n))),
        "current": lambda: state.side,
    }[spec.get("relative_to", "current")]()
    return base * float(spec.get("factor", 1.0))


def _grid_poses(n: int, side: float) -> Array:
    k = round(side)
    cells = [(i, j) for j in range(k) for i in range(k)][:n]
    return np.array([[i + 0.5, j + 0.5, 0.0] for i, j in cells])


def _run_scatter(state: State, phase: dict[str, Any], rng: np.random.Generator) -> None:
    side = _side_for(state, phase.get("side"))
    state.side = side
    state.poses = np.stack(
        [
            rng.uniform(0.5, side - 0.5, state.n),
            rng.uniform(0.5, side - 0.5, state.n),
            rng.uniform(0, np.pi / 2, state.n),
        ],
        axis=-1,
    )


def _run_grid(state: State, phase: dict[str, Any], _rng: np.random.Generator) -> None:
    side = _side_for(state, phase.get("side")) or float(math.ceil(math.sqrt(state.n)))
    state.side = float(math.ceil(math.sqrt(state.n))) if not phase.get("side") else side
    state.poses = _grid_poses(state.n, state.side)


def _run_assemble(state: State, phase: dict[str, Any], rng: np.random.Generator) -> None:
    """Build the face-contact groups by construction rather than discovering them.

    Measured: this builds 7 of 8 face contacts exactly at n=11 and 11 of 13 at n=17 before
    any relaxation, and handing the result to the same solver takes 1 run in 8 to 5 in 8.
    Discovering the same graph from a scatter instead realises it inside a degenerate
    45-degree lattice with two undeclared squares 0.012 apart.
    """
    poses, _ = record(state.n)
    state.side = _side_for(state, phase.get("side"))
    state.poses = assemble_from_faces(
        state.n, contact_edges(poses), contact_kinds(poses), state.side, rng
    )


def _stop(phase: dict[str, Any], default_steps: int = 6000) -> tuple[int, int]:
    until = phase.get("until") or {}
    steps = int(until.get("steps", default_steps))
    return steps, int(until.get("stalled_for", max(1, steps // 3)))


def _run_project(state: State, phase: dict[str, Any], rng: np.random.Generator) -> None:
    c = phase.get("constraints") or {}
    steps, stalled = _stop(phase)
    state.side = _side_for(state, phase.get("side"))
    out = solve(
        state.n,
        state.side,
        rng,
        beta=float(phase.get("relaxation", 0.1)),
        iters=steps,
        monotone=stalled,
        band=float(c.get("band", 0.02)),
        contact_weight=float(c.get("weight", 1.0)),
        classes=state.classes,
        contacts=state.contacts,
        walls=state.walls,
        start=state.poses,
        trace=state.trace,
    )
    state.poses = out.poses
    state.log[-1] |= {"solved": bool(out.solved), "steps": out.steps}


def _run_relax(state: State, phase: dict[str, Any], rng: np.random.Generator) -> None:
    """The same projection with the structure released, so angles may perturb.

    A constraint that is right early is wrong late: at n=11 six of the fourteen contacts
    are corner-on-edge between squares 40.2 degrees apart, which no shared-orientation
    class can produce, so holding the grouping to the end forbids the tilt that makes the
    packing optimal.
    """
    state.contacts, state.classes, state.walls = None, None, None
    _run_project(state, phase, rng)


def _run_ratchet(state: State, phase: dict[str, Any], rng: np.random.Generator) -> None:
    c = phase.get("constraints") or {}
    s = phase.get("schedule") or {}
    steps, stalled = _stop(phase)
    row = ratchet(
        state.n,
        rng,
        beta=float(phase.get("relaxation", 0.1)),
        iters=steps,
        monotone=stalled,
        attempts=int(s.get("attempts", 5)),
        steps=int(s.get("attempts_ceiling", 24)),
        floor=float(s.get("floor", 1e-3)),
        cold=float(s.get("cold", 0.0)),
        band=float(c.get("band", 0.02)),
        contact_weight=float(c.get("weight", 1.0)),
        classes=state.classes,
        contacts=state.contacts,
        walls=state.walls,
        start_from=state.poses,
        start_side=state.side,
    )
    state.poses = np.array(row["poses"])
    state.side = float(row["side"])
    state.log[-1] |= {"calls": row["calls"], "settled": row.get("settled", True)}


def _run_guide(state: State, phase: dict[str, Any], _rng: np.random.Generator) -> None:
    """Drive onto a chosen target. ANIMATION MACHINERY -- never a search result.

    A run that ends on a retained packing ended there because it was pulled there. The
    executor marks the phase `guided` so no frame of it can later be read as something a
    search found.
    """
    t = phase.get("target") or {}
    targets, side = record(state.n)
    if t.get("match", "by-motion") == "by-motion":
        targets, _spare = match_targets(state.poses, targets)
    state.side = side
    landed, _frames = guide_home(
        state.n,
        side,
        state.poses,
        targets,
        steps=int(t.get("steps", 400)),
        pull_to=float(t.get("pull", 5.0)),
        trace=state.trace,
    )
    state.poses = landed
    state.log[-1] |= {
        "guided": True,
        "residual": float(np.abs(landed[:, :2] - targets[:, :2]).max()),
    }


def _run_container(state: State, phase: dict[str, Any], _rng: np.random.Generator) -> None:
    """Resize the box, carrying the arrangement with it, as a phase of its own.

    The ascent's *Open* and *Close* beats are this mechanism run twice. Open grows the
    container to whichever of the two sides is larger, because adding a square is a genuine
    rearrangement and it needs somewhere to happen: measured without it, a guided step
    between two different `n` peaks at 0.83 of a unit side of overlap, while the same
    machinery between two arrangements of the same `n` never overlaps at all. Close then
    contracts to the new record's side with the squares riding it down.

    Centres scale about the container's middle so a square that was against a wall stays
    against it, and the squares themselves do not scale, because they are unit squares and
    that is the whole problem.
    """
    was = state.side
    state.side = _side_for(state, phase.get("side"))
    if was <= 0:
        return
    factor = state.side / was
    moved = state.poses.copy()
    moved[:, :2] = (state.poses[:, :2] - was / 2) * factor + state.side / 2
    state.poses = moved
    frames = int((phase.get("until") or {}).get("frames", 24))
    for step in range(1, frames + 1):
        u = step / frames
        ease = u * u * (3 - 2 * u)
        between = state.poses.copy()
        side_now = was + ease * (state.side - was)
        between[:, :2] = (state.poses[:, :2] - state.side / 2) * (side_now / state.side)
        between[:, :2] += side_now / 2
        state.trace.append(between)


MECHANISMS = {
    "container": _run_container,
    "scatter": _run_scatter,
    "grid": _run_grid,
    "assemble": _run_assemble,
    "project": _run_project,
    "relax": _run_relax,
    "ratchet": _run_ratchet,
    "guide": _run_guide,
}
"""The one table that knows how to run a phase. Adding a mechanism, or a faster backend for
one that exists, is an entry here and a branch of the schema's `mechanism` enum -- never a
change to `run`."""


def load(path: Path) -> dict[str, Any]:
    """Read a strategy and check it against the contract before anything runs."""
    doc = safe_load(path.read_text(encoding="utf-8"))
    strategy = doc.get("strategy", doc)
    jsonschema.validate(strategy, safe_load(SCHEMA.read_text(encoding="utf-8")))
    return strategy


def run(
    strategy: dict[str, Any],
    *,
    keep_trace: bool = False,
    start: Array | None = None,
    start_side: float | None = None,
) -> State:
    """Execute the phases in order, threading one arrangement through them.

    `start` is what makes an ascent possible: step `n` begins from step `n - 1`'s result
    rather than from the grid, which is the whole point of a film that adds one square at a
    time. Without it each step would restart and the squares would teleport between steps.
    """
    n = int(strategy["n"])
    seed = int(strategy.get("seed", 0))
    rng = np.random.default_rng(seed)
    state = State(
        n=n,
        poses=_grid_poses(n, float(math.ceil(math.sqrt(n)))) if start is None else start,
        side=float(math.ceil(math.sqrt(n))) if start_side is None else start_side,
    )
    if not keep_trace:
        state.trace = []

    for index, phase in enumerate(strategy["phases"]):
        mechanism = phase["mechanism"]
        state.log.append(
            {
                "phase": index,
                "mechanism": mechanism,
                "label": phase.get("label", mechanism),
                "rung": state.rung,
            }
        )
        if "structure" in phase:
            _structure(state, phase["structure"], rng)
            state.log[-1]["rung"] = state.rung
        before = len(state.trace)
        MECHANISMS[mechanism](state, phase, rng)
        # Frames are tagged with the phase that produced them as they arrive, because
        # afterwards nothing can tell them apart -- and whether a frame was guided is the
        # one thing an exporter is required to carry.
        guided = bool(state.log[-1].get("guided"))
        for poses in state.trace[before:]:
            state.animation.append(
                {
                    "side": state.side,
                    "squares": [[float(v) for v in pose] for pose in poses],
                    "phase": phase.get("label", mechanism),
                    "guided": guided,
                    "feasible": violation(poses, state.side) <= 1e-9,
                }
            )
        state.log[-1] |= {
            "side": state.side,
            "violation": violation(state.poses, state.side),
            "frames": len(state.trace) - before,
        }
    return state


def animation_document(
    strategy: dict[str, Any], state: State, *, duration_seconds: float = 8.0
) -> dict[str, Any]:
    """Turn a finished run into a PackingAnimation, the format the renderers read.

    Logical time is evenly spaced over the frames rather than proportional to the work each
    phase did. A phase that needed four thousand iterations and one that needed forty are
    equally interesting to watch, and pacing by iteration count would give the whole screen
    to whichever mechanism happened to be slowest.
    """
    frames = state.animation or [
        {
            "side": state.side,
            "squares": [[float(v) for v in pose] for pose in state.poses],
            "phase": "final",
            "guided": any(p.get("guided") for p in state.log),
            "feasible": violation(state.poses, state.side) <= 1e-9,
        }
    ]
    span = max(1, len(frames) - 1)
    known = record(state.n)[1]
    return {
        "name": strategy["name"],
        "n": state.n,
        "guided": any(f["guided"] for f in frames),
        "source": {"strategy": strategy["name"]},
        "duration_seconds": duration_seconds,
        "palette": {"hue": "angle-class", "shade": "full-side-contact"},
        "reference": {"best_known": float(known)},
        "frames": [dict(f, t=index / span) for index, f in enumerate(frames)],
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("strategy", type=Path)
    ap.add_argument("--trace", type=Path, default=None)
    ap.add_argument("--json", action="store_true")
    o = ap.parse_args()

    strategy = load(o.strategy)
    state = run(strategy, keep_trace=o.trace is not None)
    known = record(state.n)[1]
    payload = {
        "name": strategy["name"],
        "n": state.n,
        "side": state.side,
        "excess_pct": 100.0 * (state.side - known) / known,
        "violation": state.log[-1]["violation"],
        "guided": any(p.get("guided") for p in state.log),
        "phases": state.log,
    }
    if o.trace:
        o.trace.write_text(
            json.dumps(animation_document(strategy, state), sort_keys=True), encoding="utf-8"
        )
    if o.json:
        print(json.dumps(payload, default=str, sort_keys=True))
        return 0

    tag = "  [GUIDED, not a search result]" if payload["guided"] else ""
    print(f"{strategy['name']}  n = {state.n}{tag}")
    print(
        f"{'#':>2} {'mechanism':>10} {'rung':>26} {'side':>12} {'violation':>10} {'frames':>7}"
    )
    for p in state.log:
        print(
            f"{p['phase']:>2} {p['mechanism']:>10} {p['rung']:>26} {p['side']:>12.7f} "
            f"{p['violation']:>10.1e} {p['frames']:>7}"
        )
    print(f"best known {known:.7f}, reached {state.side:.7f} ({payload['excess_pct']:+.3f} %)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
