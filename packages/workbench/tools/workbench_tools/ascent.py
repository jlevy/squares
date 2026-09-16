"""Build the guided atlas ascent as typed strategies and animation records."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from devtools.known_structure import record
from devtools.lock_order import lock_order
from devtools.run_projection_ratchet import match_targets
from sqpack.cover import write_text_atomic
from workbench_tools.animation_records import (
    ANIMATION_CONTRACT,
    AnimationDocument,
    FairReach,
    animation_to_json,
    decode_animation,
)
from workbench_tools.animation_render import export_svg
from workbench_tools.packing_contracts import check_unit_square_packing
from workbench_tools.strategy_execution import run
from workbench_tools.strategy_records import (
    STRATEGY_CONTRACT,
    PackingStrategy,
    decode_strategy,
    strategy_to_row,
)

type Pose = tuple[float, float, float]


@dataclass(slots=True)
class _AscentFrame:
    side: float
    squares: list[Pose]
    square_ids: list[int]
    phase: str
    guided: bool
    feasible: bool
    locked: list[bool]
    record: int | None = None


def step_strategy(n: int, *, fair_steps: int = 3000, seed: int = 11) -> PackingStrategy:
    """Declare the settle-and-guide step from `n - 1` squares to retained `n`.

    The settle runs at the record side for `n`. There is no separate container phase: a
    rendered step already starts at that side, so one would only repeat a still frame.
    """
    return decode_strategy(
        {
            "contract": STRATEGY_CONTRACT,
            "name": f"ascent-{n:03d}",
            "n": n,
            "seed": seed,
            "phases": [
                {
                    "mechanism": "project",
                    "label": "settle",
                    "side": {"relative_to": "record", "factor": 1.0},
                    "relaxation": 0.1,
                    "until": {"steps": fair_steps, "stalled_for": max(1, fair_steps // 3)},
                },
                {
                    "mechanism": "guide",
                    "label": "close in",
                    "target": {
                        "source": "record",
                        "match": "by-motion",
                        "steps": 220,
                        "pull": 5.0,
                    },
                },
            ],
        }
    )


def ascent(first: int, last: int) -> tuple[PackingStrategy, ...]:
    """Return the versioned strategy sequence for an increasing nonempty range."""
    _validate_range(first, last)
    return tuple(step_strategy(n) for n in range(first, last + 1))


def render_ascent(first: int, last: int, *, fair_steps: int = 2000) -> AnimationDocument:
    """Run each step and return one checked, explicitly guided animation."""
    _validate_range(first, last)
    if fair_steps < 1:
        raise ValueError("fair steps must be positive")
    poses, side = record(first)
    frames: list[_AscentFrame] = []
    reach: list[dict[str, object]] = []
    configurations: list[dict[str, object]] = []

    for n in range(first + 1, last + 1):
        _target, target_side = record(n)
        arriving = np.vstack([poses, [[side - 0.5, side - 0.5, 0.0]]])
        strategy = step_strategy(n, fair_steps=fair_steps)
        state = run(
            strategy,
            keep_trace=True,
            start=arriving,
            start_side=max(side, target_side),
        )
        configurations.append(strategy_to_row(state.configuration))

        settled = next(
            (receipt for receipt in reversed(state.phases) if receipt.mechanism == "project"),
            None,
        )
        if settled is not None:
            # The receipt's geometry is the independent unit-square check the animation
            # decoder applies to every frame. A settle it rejects reached no side.
            packed = settled.geometry.passed
            reach.append(
                {
                    "n": n,
                    "fair_side": settled.side if packed else None,
                    "record": target_side,
                    "excess_pct": (
                        100.0 * (settled.side - target_side) / target_side if packed else None
                    ),
                    "packing_valid": packed,
                }
            )

        target_poses, target_side = record(n)
        target_poses, _assignment = match_targets(state.poses, target_poses)
        target_check = check_unit_square_packing(
            target_poses,
            side=target_side,
            expected_count=n,
        )
        if not target_check.passed:
            raise ValueError(f"retained n={n} endpoint failed the independent packing check")

        produced = [
            _AscentFrame(
                side=frame.side,
                squares=list(frame.poses),
                square_ids=list(range(1, n + 1)),
                phase=frame.phase,
                guided=frame.guided,
                feasible=frame.geometry.passed,
                locked=[],
            )
            for frame in state.animation
        ]
        produced.append(
            _AscentFrame(
                side=target_side,
                squares=_poses(target_poses),
                square_ids=list(range(1, n + 1)),
                phase="retained record",
                guided=True,
                feasible=True,
                locked=[],
            )
        )
        order = lock_order(target_poses, target_side)
        for index, frame in enumerate(produced):
            share = (index + 1) / max(1, len(produced))
            locked = set(order[: round(share * len(order))])
            frame.locked = [square in locked for square in range(len(frame.squares))]
        frames.extend(produced)
        poses, side = target_poses, target_side

    final_side = float(record(last)[1])
    corner = final_side - 0.5
    for frame in frames:
        missing = last - len(frame.squares)
        if missing > 0:
            present = len(frame.squares)
            frame.squares.extend([(corner, corner, 0.0)] * missing)
            frame.square_ids.extend(range(present + 1, last + 1))
            frame.locked.extend([False] * missing)
            # Feasibility was measured on the step's own squares, before the waiting ones
            # were parked in a corner, so a padded frame is never offered as a packing.
            frame.feasible = False
    frames[-1].record = last

    span = max(1, len(frames) - 1)
    row: dict[str, object] = {
        "contract": ANIMATION_CONTRACT,
        "name": f"atlas-ascent-{first:03d}-{last:03d}",
        "n": last,
        "guided": True,
        "source": {
            "strategy": "generated atlas ascent",
            "records": list(range(first, last + 1)),
            "seed": 11,
            "configuration": {"steps": configurations},
        },
        "duration_seconds": max(4.0, 0.7 * (last - first)),
        "palette": {"hue": "angle-class", "shade": "full-side-contact"},
        "reference": {"best_known": final_side},
        "fair_reach": reach,
        "frames": [
            {
                "t": index / span,
                "side": frame.side,
                "squares": [list(pose) for pose in frame.squares],
                "square_ids": frame.square_ids,
                "phase": frame.phase,
                "guided": frame.guided,
                "feasible": frame.feasible,
                "locked": frame.locked,
                **({"record": frame.record} if frame.record is not None else {}),
            }
            for index, frame in enumerate(frames)
        ],
    }
    return decode_animation(row)


def _validate_range(first: int, last: int) -> None:
    if first < 1 or last <= first:
        raise ValueError("ascent range must contain at least one increasing step")


def _poses(values: np.ndarray) -> list[Pose]:
    return [(float(pose[0]), float(pose[1]), float(pose[2])) for pose in values]


def fair_reach_line(item: FairReach) -> str:
    """Format one report row, printing a reached side only beside a checked packing."""
    head = f"{item.n:>4}"
    record_side = f"{item.record:>12.7f}"
    if item.packing_valid is False or item.fair_side is None or item.excess_pct is None:
        return f"{head} {'-':>12} {record_side} {'-':>9}  not a packing"
    reached = f"{head} {item.fair_side:>12.7f} {record_side} {item.excess_pct:>+8.3f}%"
    return reached if item.packing_valid else f"{reached}  unchecked, not a packing"


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
    options = ap.parse_args()

    if options.render:
        document = render_ascent(options.first, options.last, fair_steps=options.fair_steps)
        write_text_atomic(options.out, animation_to_json(document))
        print(
            f"{document.name}: {len(document.frames)} frames, "
            f"n = {options.first} to {options.last}, {options.out}"
        )
        print(f"{'n':>4} {'fair reach':>12} {'record':>12} {'excess':>9}")
        for item in document.fair_reach:
            print(fair_reach_line(item))
        if options.svg:
            write_text_atomic(options.svg, export_svg(document))
            print(f"wrote {options.svg}")
        return 0

    options.out.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for strategy in ascent(options.first, options.last):
        path = options.out / f"{strategy.name}.json"
        document = {
            "softschema": {
                "contract": STRATEGY_CONTRACT,
                "schema": "packing-strategy.schema.yaml",
                "envelope": "strategy",
                "status": "enforced",
            },
            "strategy": strategy_to_row(strategy),
        }
        write_text_atomic(path, json.dumps(document, indent=2, allow_nan=False))
        written.append(path)
    print(
        f"{len(written)} step strategies in {options.out}, "
        f"n = {options.first} to {options.last}"
    )
    print(f"  first {written[0].name}, last {written[-1].name}")
    print(f"  record at n = {options.last}: {record(options.last)[1]:.7f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
