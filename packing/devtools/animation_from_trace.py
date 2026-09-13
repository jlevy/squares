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
import math
from dataclasses import replace
from decimal import Decimal
from pathlib import Path

from workbench_tools.animation_records import (
    AnimationDocument,
    AnimationFrame,
    decode_animation,
)
from workbench_tools.packing_contracts import (
    GeometryCheck,
)

from devtools.build_known_best_atlas import frame_from_witness
from devtools.known_structure import WITNESSES, record
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
from sqpack.witness import load_witness

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = ROOT / "strategies/packing-animation.schema.yaml"
RECORD_REFERENCE_TOLERANCE = 1e-7


def _renamed(
    frame: PackingFrame,
    locked: tuple[bool, ...] | None = None,
    square_ids: tuple[int, ...] | None = None,
) -> PackingFrame:
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
                square_id=f"square-{square_id:03d}",
                corners=square.corners,
                pose=square.pose,
                label=str(square_id),
                locked=True if locked is None else bool(locked[index - 1]),
            )
            for index, (square_id, square) in enumerate(
                zip(
                    square_ids or list(range(1, len(frame.squares) + 1)),
                    frame.squares,
                    strict=True,
                ),
                start=1,
            )
        ),
        evidence=frame.evidence,
        check=frame.check,
        label=frame.label,
        logical_time=frame.logical_time,
        source_id=frame.source_id,
        source_url=frame.source_url,
        features=frame.features,
    )


def _label(document: AnimationDocument, entry: AnimationFrame) -> str:
    """What to show while a frame is on screen, with the marks a viewer must not lose."""
    marks = []
    if document.frame_is_guided(entry):
        marks.append("guided")
    if not entry.geometry.passed:
        marks.append("not a packing")
    elif entry.feasible is not True:
        marks.append("candidate")
    label = entry.label or entry.phase
    return f"{label} ({', '.join(marks)})" if marks else label


def _check_summary(check: GeometryCheck) -> CheckSummary:
    return CheckSummary(
        passed=check.passed,
        kind=CheckKind.NUMERICAL,
        method="independent separating-axis and container check",
        arithmetic="binary64",
        precision="53",
        rounding="nearest-even",
        tolerance=str(check.tolerance),
        detail=(
            f"overlap pairs={check.pair_failures or 0}; "
            f"container failures={check.wall_failures or 0}"
        ),
    )


def _record_order(entry: AnimationFrame, n: int) -> list[int]:
    record_n = entry.record
    if record_n is None:
        raise ValueError("record order requires a record reference")
    if record_n != n:
        raise ValueError("record reference must name the animation's square count")
    reference, reference_side = record(record_n)
    side = entry.side
    if not math.isclose(
        side,
        reference_side,
        rel_tol=RECORD_REFERENCE_TOLERANCE,
        abs_tol=RECORD_REFERENCE_TOLERANCE,
    ):
        raise ValueError("record reference side does not match the retained record")

    remaining = set(range(n))
    order: list[int] = []
    for pose in entry.squares:
        best = min(
            remaining,
            key=lambda index: max(
                abs(float(pose[0]) - float(reference[index, 0])),
                abs(float(pose[1]) - float(reference[index, 1])),
                abs(
                    math.remainder(
                        float(pose[2]) - float(reference[index, 2]),
                        math.pi / 2,
                    )
                ),
            ),
        )
        distance = max(
            abs(float(pose[0]) - float(reference[best, 0])),
            abs(float(pose[1]) - float(reference[best, 1])),
            abs(
                math.remainder(
                    float(pose[2]) - float(reference[best, 2]),
                    math.pi / 2,
                )
            ),
        )
        if distance > RECORD_REFERENCE_TOLERANCE:
            raise ValueError("record reference poses do not match the retained record")
        remaining.remove(best)
        order.append(best)
    return order


def muting_from_animation(
    value: object | AnimationDocument,
) -> tuple[tuple[bool, ...], ...]:
    """Which squares are muted in which frame.

    A frame that declares `locked` decides square by square; one that does not falls back
    to its own feasibility, which is all an animation without a locking notion can say.
    """
    document = decode_animation(value)
    out: list[tuple[bool, ...]] = []
    for entry in document.frames:
        if not entry.geometry.passed:
            out.append(tuple(True for _ in entry.squares))
        elif entry.locked is None:
            out.append(tuple(entry.feasible is not True for _ in entry.squares))
        else:
            out.append(tuple(not flag for flag in entry.locked))
    return tuple(out)


def trajectory_from_animation(value: object | AnimationDocument) -> PackingTrajectory:
    """A PackingAnimation in, a PackingTrajectory out.

    `guided` and `feasible` are folded into each frame's label rather than dropped, because
    a renderer that cannot see them can draw a pulled frame as though a search had found
    it. The label is the only channel `PackingFrame` offers, so it is the one used.
    """
    document = decode_animation(value)
    frames: list[PackingFrame] = []
    for entry in document.frames:
        # A frame that IS a retained record is built the way the atlas builds it, from the
        # witness, through the same function. Rebuilding it from the float poses the run
        # carried gives a picture that differs in the tenth significant digit -- invisible,
        # but not the same drawing, and "the same as our SVGs" is a byte claim rather than
        # a visual one.
        if entry.record is not None:
            if not entry.geometry.passed:
                raise ValueError("record reference requires valid supplied geometry")
            source_order = _record_order(entry, document.n)
            witness = load_witness(WITNESSES / f"n-{entry.record:03d}.yaml")
            base = frame_from_witness(witness)
            # The witness frame is used exactly as the atlas uses it: exact corners and
            # NO pose. Attaching a float pose changes what the renderer draws, because
            # full-side contact shading needs two edges exactly parallel and a float angle
            # is not exactly anything -- two of n = 11's eleven squares came out a different
            # green. The motion model derives the pose it needs from these corners instead.
            frames.append(
                PackingFrame(
                    container_side=base.container_side,
                    squares=tuple(
                        replace(
                            base.squares[record_index],
                            square_id=f"square-{square_id:03d}",
                            label=str(square_id),
                            locked=(
                                True if entry.locked is None else entry.locked[identity_index]
                            ),
                        )
                        for identity_index, (square_id, record_index) in enumerate(
                            zip(
                                entry.square_ids,
                                source_order,
                                strict=True,
                            )
                        )
                    ),
                    evidence=base.evidence,
                    check=base.check,
                    label=_label(document, entry),
                    logical_time=Decimal(str(entry.logical_time)),
                    source_id=base.source_id,
                    source_url=base.source_url,
                    features=base.features,
                )
            )
            continue
        squares = entry.squares
        frames.append(
            _renamed(
                frame_from_pose_arrays(
                    entry.side,
                    [pose[0] for pose in squares],
                    [pose[1] for pose in squares],
                    [pose[2] for pose in squares],
                    label=_label(document, entry),
                    logical_time=Decimal(str(entry.logical_time)),
                    # A frame that is a packing establishes something; one mid-transition
                    # establishes nothing. Saying so here rather than in a side channel is what
                    # lets the renderer mute the second without being told which is which.
                    evidence=(
                        EvidenceTier.NUMERICALLY_CHECKED
                        if entry.feasible is True and entry.geometry.passed
                        else EvidenceTier.CANDIDATE
                    ),
                    check=_check_summary(entry.geometry),
                    source_id=document.name,
                ),
                entry.locked,
                entry.square_ids,
            )
        )
    return PackingTrajectory(
        frames=tuple(frames),
        # Illustrative is the honest kind for anything a strategy produced: retained and
        # certified mean a record and a proof, and an animation is neither even when every
        # frame of it happens to be a packing.
        kind=TrajectoryKind.ILLUSTRATIVE,
        label=document.name,
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
