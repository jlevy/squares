#!/usr/bin/env python3
"""Turn a PackingAnimation document into the trajectory the renderers already understand.

The one adapter between what a run produces and what `sqpack.render` draws. It exists so
that everything built for the campaign -- the projection search, the guided landing, the
contact-graph assembly -- reaches the renderer without any of them knowing the renderer
exists, and without the renderer learning what a strategy is.

Corners are not recomputed here. `frame_from_pose_arrays` is the repository's door between
poses and corners, and it cross-checks its own fixed-precision projection against the
geometry module before returning; going around it would be a second opinion on a question
that already has an answer.
"""

from __future__ import annotations

import argparse
import json
from decimal import Decimal
from pathlib import Path
from typing import Any

from devtools.build_known_best_atlas import frame_from_witness
from devtools.known_structure import WITNESSES
from devtools.packing_render_adapters import frame_from_pose_arrays
from sqpack.render.model import (
    CheckKind,
    CheckSummary,
    EvidenceTier,
    PackingFrame,
    PackingTrajectory,
    SquareGeometry,
    TrajectoryKind,
)
from sqpack.yamlio import safe_load


def _renamed(frame: PackingFrame, locked: list[bool] | None = None) -> PackingFrame:
    """Give pose-built squares the names the witness uses.

    `frame_from_pose_arrays` numbers from zero in two digits and the atlas witness numbers
    from one in three, and a trajectory whose frames disagree about a square's identity is
    refused outright -- correctly, since it cannot know which square became which. Aligning
    on the atlas convention is what lets a record frame and a computed one sit in the same
    animation, and is also what makes a final still the same drawing as the atlas rendering
    rather than one with different ids on identical shapes.
    """
    return PackingFrame(
        container_side=frame.container_side,
        squares=tuple(
            SquareGeometry(
                square_id=f"square-{index:03d}",
                corners=square.corners,
                pose=square.pose,
                label=str(index),
                locked=True if locked is None else bool(locked[index - 1]),
            )
            for index, square in enumerate(frame.squares, start=1)
        ),
        evidence=frame.evidence,
        check=frame.check,
        label=frame.label,
        logical_time=frame.logical_time,
        source_id=frame.source_id,
        source_url=frame.source_url,
        features=frame.features,
    )


def _label(entry: dict[str, Any]) -> str:
    """What to show while a frame is on screen, with the marks a viewer must not lose."""
    marks = []
    if entry.get("guided"):
        marks.append("guided")
    if not entry.get("feasible", True):
        marks.append("not a packing")
    label = entry.get("phase", "frame")
    return f"{label} ({', '.join(marks)})" if marks else label


def muting_from_animation(document: dict[str, Any]) -> tuple[tuple[bool, ...], ...]:
    """Which squares are muted in which frame.

    A frame that declares `locked` decides square by square; one that does not falls back
    to its own feasibility, which is all an animation without a locking notion can say.
    """
    out = []
    for entry in document["frames"]:
        locked = entry.get("locked")
        if locked is None:
            out.append(tuple(not entry.get("feasible", True) for _ in entry["squares"]))
        else:
            out.append(tuple(not flag for flag in locked))
    return tuple(out)


def trajectory_from_animation(document: dict[str, Any]) -> PackingTrajectory:
    """A PackingAnimation in, a PackingTrajectory out.

    `guided` and `feasible` are folded into each frame's label rather than dropped, because
    a renderer that cannot see them can draw a pulled frame as though a search had found
    it. The label is the only channel `PackingFrame` offers, so it is the one used.
    """
    frames = []
    for entry in document["frames"]:
        # A frame that IS a retained record is built the way the atlas builds it, from the
        # witness, through the same function. Rebuilding it from the float poses the run
        # carried gives a picture that differs in the tenth significant digit -- invisible,
        # but not the same drawing, and "the same as our SVGs" is a byte claim rather than
        # a visual one.
        if entry.get("record") is not None:
            witness = safe_load(
                (WITNESSES / f"n-{int(entry['record']):03d}.yaml").read_text(encoding="utf-8")
            )["witness"]
            base = frame_from_witness(witness)
            # The witness frame is used exactly as the atlas uses it: exact corners and
            # NO pose. Attaching a float pose changes what the renderer draws, because
            # full-side contact shading needs two edges exactly parallel and a float angle
            # is not exactly anything -- two of n = 11's eleven squares came out a different
            # green. The motion model derives the pose it needs from these corners instead.
            frames.append(
                PackingFrame(
                    container_side=base.container_side,
                    squares=base.squares,
                    evidence=base.evidence,
                    check=base.check,
                    label=_label(entry),
                    logical_time=Decimal(str(entry["t"])),
                    source_id=base.source_id,
                    source_url=base.source_url,
                    features=base.features,
                )
            )
            continue
        squares = entry["squares"]
        frames.append(
            _renamed(
                frame_from_pose_arrays(
                    entry["side"],
                    [pose[0] for pose in squares],
                    [pose[1] for pose in squares],
                    [pose[2] for pose in squares],
                    label=_label(entry),
                    logical_time=Decimal(str(entry["t"])),
                    # A frame that is a packing establishes something; one mid-transition
                    # establishes nothing. Saying so here rather than in a side channel is what
                    # lets the renderer mute the second without being told which is which.
                    evidence=(
                        EvidenceTier.NUMERICALLY_CHECKED
                        if entry.get("feasible", True)
                        else EvidenceTier.CANDIDATE
                    ),
                    # The tier is a claim about evidence, so the renderer requires the
                    # receipt with it -- and refuses the claim without one, which is how this
                    # got caught. The check is real: the producer measured the deepest
                    # penetration by the separating-axis theorem and compared it to 1e-9.
                    check=(
                        CheckSummary(
                            passed=True,
                            kind=CheckKind.NUMERICAL,
                            method="separating-axis violation at most 1e-9",
                            arithmetic="binary64",
                            precision="53",
                            rounding="nearest-even",
                            tolerance="1e-9",
                        )
                        if entry.get("feasible", True)
                        else None
                    ),
                    source_id=document.get("name", "animation"),
                ),
                entry.get("locked"),
            )
        )
    return PackingTrajectory(
        frames=tuple(frames),
        # Illustrative is the honest kind for anything a strategy produced: retained and
        # certified mean a record and a proof, and an animation is neither even when every
        # frame of it happens to be a packing.
        kind=TrajectoryKind.ILLUSTRATIVE,
        label=document.get("name", "animation"),
    )


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("animation", type=Path)
    o = ap.parse_args()
    document = json.loads(o.animation.read_text(encoding="utf-8"))
    trajectory = trajectory_from_animation(document)
    sides = {str(frame.container_side.projected) for frame in trajectory.frames}
    print(
        f"{trajectory.label}: {len(trajectory.frames)} frames, "
        f"{len(trajectory.frames[0].squares)} squares, "
        f"{len(sides)} distinct container side(s)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
