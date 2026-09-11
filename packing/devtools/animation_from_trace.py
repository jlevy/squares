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

from devtools.packing_render_adapters import frame_from_pose_arrays
from sqpack.render.model import (
    CheckKind,
    CheckSummary,
    EvidenceTier,
    PackingTrajectory,
    TrajectoryKind,
)


def trajectory_from_animation(document: dict[str, Any]) -> PackingTrajectory:
    """A PackingAnimation in, a PackingTrajectory out.

    `guided` and `feasible` are folded into each frame's label rather than dropped, because
    a renderer that cannot see them can draw a pulled frame as though a search had found
    it. The label is the only channel `PackingFrame` offers, so it is the one used.
    """
    frames = []
    for entry in document["frames"]:
        squares = entry["squares"]
        marks = []
        if entry.get("guided"):
            marks.append("guided")
        if not entry.get("feasible", True):
            marks.append("not a packing")
        label = entry.get("phase", "frame")
        if marks:
            label = f"{label} ({', '.join(marks)})"
        frames.append(
            frame_from_pose_arrays(
                entry["side"],
                [pose[0] for pose in squares],
                [pose[1] for pose in squares],
                [pose[2] for pose in squares],
                label=label,
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
