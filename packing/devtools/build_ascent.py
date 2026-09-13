#!/usr/bin/env python3
"""The atlas ascent: one strategy document per step, from `n` to `n + 1`.

A single directed film from `n = 1` upward, adding one square per step and landing each
time on the retained record. Directed on purpose -- it is not a search, it uses the known
endpoints, and the point is that it is clean, legible and always arrives.

Each step is six beats, and two of them carry the load. **Settle** is an ordinary `project`
phase with no target, running for real from the arrangement it inherited: whatever it
reaches, it reached. **Close in** is a `guide` phase that takes it the rest of the way onto
the record. Every frame of the guided stretch is marked, so a renderer shows the handoff
rather than hiding it, and what the film shows is a plausible route to the optimum with the
point where plausibility ran out marked on it.

*Open* and *Close* exist because of a measurement, not a hunch. A guided transition between
two different `n` is smooth and lands exactly -- residual 0.0004 to 0.0007 -- but squares
pass through each other on the way, peaking at 0.83 of a unit side at 10 to 11 and 0.86 at
17 to 18, on roughly 100 frames of 126. Between two arrangements of the *same* `n` the same
machinery never overlaps at all. So the transit overlap is not the mechanism: adding a
square is a rearrangement with nowhere to happen, and Open gives it somewhere.

Usage, from `packing/`:
    uv run --frozen python -m devtools.build_ascent --to 20 --out ascent/
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np
from workbench_tools.packing_contracts import check_unit_square_packing

from devtools.export_animation_svg import export_svg
from devtools.known_structure import record
from devtools.lock_order import lock_order
from devtools.packing_strategy import run
from devtools.run_projection_ratchet import match_targets


def step_strategy(n: int, *, fair_steps: int = 3000, seed: int = 11) -> dict[str, Any]:
    """The six beats that carry `n - 1` squares to the retained packing of `n`."""
    return {
        "name": f"ascent-{n:03d}",
        "n": n,
        "seed": seed,
        "phases": [
            {
                "mechanism": "container",
                "label": "open the container",
                "side": {"relative_to": "record", "factor": 1.0},
                "until": {"frames": 18},
            },
            {
                "mechanism": "project",
                "label": "settle",
                "relaxation": 0.1,
                "until": {"steps": fair_steps, "stalled_for": fair_steps // 3},
            },
            {
                "mechanism": "guide",
                "label": "close in",
                "target": {"source": "record", "match": "by-motion", "steps": 220, "pull": 5.0},
            },
        ],
    }


def ascent(first: int, last: int) -> list[dict[str, Any]]:
    return [step_strategy(n) for n in range(first, last + 1)]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--from", dest="first", type=int, default=2)
    ap.add_argument("--to", dest="last", type=int, default=20)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument(
        "--render", action="store_true", help="run every step and emit one animation"
    )
    ap.add_argument("--svg", type=Path, default=None)
    ap.add_argument("--fair-steps", type=int, default=2000)
    o = ap.parse_args()

    if o.render:
        document = render_ascent(o.first, o.last, fair_steps=o.fair_steps)
        o.out.parent.mkdir(parents=True, exist_ok=True)
        o.out.write_text(json.dumps(document), encoding="utf-8")
        print(
            f"{document['name']}: {len(document['frames'])} frames, "
            f"n = {o.first} to {o.last}, {o.out}"
        )
        print(f"{'n':>4} {'fair reach':>12} {'record':>12} {'excess':>9}")
        for row in document["fair_reach"]:
            print(
                f"{row['n']:>4} {row['fair_side']:>12.7f} {row['record']:>12.7f} "
                f"{row['excess_pct']:>+8.3f}%"
            )
        if o.svg:
            o.svg.write_text(export_svg(document), encoding="utf-8")
            print(f"wrote {o.svg}")
        return 0

    o.out.mkdir(parents=True, exist_ok=True)
    written = []
    for strategy in ascent(o.first, o.last):
        path = o.out / f"{strategy['name']}.json"
        path.write_text(json.dumps({"strategy": strategy}, indent=2), encoding="utf-8")
        written.append(path)
    print(f"{len(written)} step strategies in {o.out}, n = {o.first} to {o.last}")
    print(f"  first {written[0].name}, last {written[-1].name}")
    print(f"  record at n = {o.last}: {record(o.last)[1]:.7f}")
    return 0


def render_ascent(first: int, last: int, *, fair_steps: int = 2000) -> dict[str, Any]:
    """Run every step in sequence and return one animation of the whole climb.

    Each step starts from the previous step's arrangement with one square added at the
    container's corner, so the film is continuous: squares that were already placed stay
    where they were and the newcomer arrives from outside rather than appearing.
    """

    poses, side = record(first)
    frames: list[dict[str, Any]] = []
    reach: list[dict[str, Any]] = []

    for n in range(first + 1, last + 1):
        _target, target_side = record(n)
        arriving = np.vstack([poses, [[side - 0.5, side - 0.5, 0.0]]])
        strategy = step_strategy(n, fair_steps=fair_steps)
        state = run(
            strategy, keep_trace=True, start=arriving, start_side=max(side, target_side)
        )

        settled = next(
            (entry for entry in reversed(state.log) if entry["mechanism"] == "project"), None
        )
        if settled is not None:
            reach.append(
                {
                    "n": n,
                    "fair_side": settled["side"],
                    "record": target_side,
                    "excess_pct": 100.0 * (settled["side"] - target_side) / target_side,
                }
            )

        # A record-labelled frame carries the record's actual geometry. The guide lands
        # close to its target but does not establish that it reached it, so preserve its
        # last candidate frame and add one explicit guided endpoint at the retained poses.
        target_poses, target_side = record(n)
        target_poses, _assignment = match_targets(state.poses, target_poses)
        target_check = check_unit_square_packing(
            target_poses,
            side=target_side,
            expected_count=n,
        )
        if not target_check.passed:
            raise ValueError(f"retained n={n} endpoint failed the independent packing check")
        state.poses = target_poses
        state.side = target_side
        state.animation.append(
            {
                "side": target_side,
                "squares": [[float(value) for value in pose] for pose in target_poses],
                "square_ids": list(range(1, n + 1)),
                "phase": "retained record",
                "guided": True,
                "feasible": True,
            }
        )

        # Each square takes its colour as it reaches its place, outside in and
        # axis-aligned first. The order is the geometry's, not the run's: a viewer can
        # predict where a square square to the wall belongs, so those locking first is
        # both the clearest thing to watch and the least surprising.
        order = lock_order(target_poses, target_side)
        produced = list(state.animation)
        for index, entry in enumerate(produced):
            share = (index + 1) / max(1, len(produced))
            settled = set(order[: round(share * len(order))])
            entry["locked"] = [i in settled for i in range(len(entry["squares"]))]
        frames.extend(produced)
        poses, side = state.poses, state.side

    # Every frame carries the final square count, because a trajectory is one fixed set of
    # squares and an ascent changes n at every step. Squares that have not arrived yet wait
    # outside the container, which is also the Enter beat: a square comes from somewhere
    # rather than appearing. Without this the renderer refuses the whole film with
    # "trajectory square identity or order changed", and rightly, since it cannot know
    # which square became which.
    # Waiting squares sit INSIDE the final container, at the corner they will enter from.
    # Parking them outside it put them beyond the viewBox, which the renderer sizes to the
    # largest container in the trajectory: the film then drew squares in the margin and the
    # packing itself came out squashed and overlapping. A square waiting at the corner of a
    # box it has not joined yet reads correctly and costs the layout nothing.
    final_side = float(record(last)[1])
    corner = final_side - 0.5
    for frame in frames:
        missing = last - len(frame["squares"])
        if missing > 0:
            present = len(frame["squares"])
            frame["squares"] = frame["squares"] + [[corner, corner, 0.0]] * missing
            frame["square_ids"] = list(frame.get("square_ids", range(1, present + 1))) + list(
                range(present + 1, last + 1)
            )
            # A square that has not arrived has certainly not locked.
            frame["locked"] = list(frame.get("locked", [])) + [False] * missing

    # Only the last frame of the whole climb claims to be a record. An intermediate step
    # ends on the record for ITS n, which has fewer squares than the padded frames around
    # it, and a frame built from that witness breaks the one-set-of-squares rule the
    # trajectory depends on.
    if frames:
        frames[-1]["record"] = last

    span = max(1, len(frames) - 1)
    for index, frame in enumerate(frames):
        frame["t"] = index / span
    return {
        "name": f"atlas-ascent-{first:03d}-{last:03d}",
        "n": last,
        "guided": any(frame.get("guided") for frame in frames),
        # 0.7 s per step rather than a second: at a second the film drags, and the
        # steps are short enough that the eye keeps up.
        "duration_seconds": max(4.0, 0.7 * (last - first)),
        "palette": {"hue": "angle-class", "shade": "full-side-contact"},
        "reference": {"best_known": float(record(last)[1])},
        "frames": frames,
        "fair_reach": reach,
    }


if __name__ == "__main__":
    raise SystemExit(main())
