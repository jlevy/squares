"""Checked adapters from packing-animation records to repository renderers."""

from __future__ import annotations

import math
import re
from dataclasses import replace
from decimal import Decimal

from devtools.build_known_best_atlas import frame_from_witness
from devtools.known_structure import WITNESSES, record
from devtools.packing_render_adapters import frame_from_pose_arrays
from sqpack.render import render_packing_svg
from sqpack.render.model import (
    AnnotationLevel,
    CheckKind,
    CheckSummary,
    EvidenceTier,
    HueScheme,
    PackingFrame,
    PackingTrajectory,
    RenderSpec,
    ShadeScheme,
    SquareGeometry,
    TrajectoryKind,
    ViewLevel,
)
from sqpack.witness import load_witness
from workbench_tools.animation_records import (
    AnimationDocument,
    AnimationFrame,
    decode_animation,
)
from workbench_tools.packing_contracts import GeometryCheck

#: How far a frame that names a retained record may sit from that record's witness before it
#: is refused as a different arrangement: in side units for centres, radians for angles, and
#: relative to the record side (with this as its floor) for the container.
#:
#: A matching tolerance, not packing validity, which is `packing_contracts` at 1e-9. A frame
#: that names a record is drawn from the witness's exact geometry, so what it must show is
#: that its own poses are that witness. The witnesses are stored as exact decimals and read
#: as binary64: over all 324 on 2026-09-14 that moved a centre by at most 2.4e-15 and a
#: side by 1.7e-15. 1e-7 admits any faithful binary64 copy with seven orders of room, and
#: refuses a coarser one, including a copy at the page's catalogue precision (centres to
#: 1e-6, angles to 1e-4 degrees), which is a rounded arrangement rather than the witness.
#: `tests/test_record_reference_tolerance.py` pins both edges.
RECORD_REFERENCE_TOLERANCE = 1e-7

#: What an export says about its motion. It goes in the SVG's `<desc>` and the export receipt,
#: never on the picture: the owner removed the page's visible kind tag, and a caption line
#: drawn over the figure would put it back by another route.
TRANSITIONS_STATEMENT = "Transitions are illustrative, not packings."

#: Why no exported animation's in-between states are packings, whatever its frames are.
INTERPOLATION_REASON = (
    "The SVG interpolates between the animation's frames, and the in-between states are "
    "illustrative tweens that nothing checks as packings."
)


def _renamed(
    frame: PackingFrame,
    locked: tuple[bool, ...] | None = None,
    square_ids: tuple[int, ...] | None = None,
) -> PackingFrame:
    """Align pose-built square names with the atlas witness convention."""
    ids = square_ids or tuple(range(1, len(frame.squares) + 1))
    locks = locked or tuple(True for _ in frame.squares)
    ordered = sorted(zip(ids, frame.squares, locks, strict=True), key=lambda item: item[0])
    return PackingFrame(
        container_side=frame.container_side,
        squares=tuple(
            SquareGeometry(
                square_id=f"square-{square_id:03d}",
                corners=square.corners,
                pose=square.pose,
                label=str(square_id),
                locked=bool(is_locked),
            )
            for square_id, square, is_locked in ordered
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
    marks: list[str] = []
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
    if not math.isclose(
        entry.side,
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
                abs(pose[0] - float(reference[index, 0])),
                abs(pose[1] - float(reference[index, 1])),
                abs(math.remainder(pose[2] - float(reference[index, 2]), math.pi / 2)),
            ),
        )
        distance = max(
            abs(pose[0] - float(reference[best, 0])),
            abs(pose[1] - float(reference[best, 1])),
            abs(math.remainder(pose[2] - float(reference[best, 2]), math.pi / 2)),
        )
        if distance > RECORD_REFERENCE_TOLERANCE:
            raise ValueError("record reference poses do not match the retained record")
        remaining.remove(best)
        order.append(best)
    return order


def muting_from_animation(document: AnimationDocument) -> tuple[tuple[bool, ...], ...]:
    """Return muted-square flags derived from checked geometry and explicit locking."""
    document = decode_animation(document)
    out: list[tuple[bool, ...]] = []
    for entry in document.frames:
        if not entry.geometry.passed:
            out.append(tuple(True for _ in entry.squares))
        elif entry.locked is None:
            out.append(tuple(entry.feasible is not True for _ in entry.squares))
        else:
            out.append(tuple(not flag for flag in entry.locked))
    return tuple(out)


def trajectory_from_animation(document: AnimationDocument) -> PackingTrajectory:
    """Adapt a checked animation to the renderer's trajectory model."""
    document = decode_animation(document)
    frames: list[PackingFrame] = []
    for entry in document.frames:
        if entry.record is not None:
            if not entry.geometry.passed:
                raise ValueError("record reference requires valid supplied geometry")
            source_order = _record_order(entry, document.n)
            witness = load_witness(WITNESSES / f"n-{entry.record:03d}.yaml")
            base = frame_from_witness(witness)
            locks = entry.locked or tuple(True for _ in entry.square_ids)
            ordered = sorted(
                zip(entry.square_ids, source_order, locks, strict=True),
                key=lambda item: item[0],
            )
            frames.append(
                PackingFrame(
                    container_side=base.container_side,
                    squares=tuple(
                        replace(
                            base.squares[record_index],
                            square_id=f"square-{square_id:03d}",
                            label=str(square_id),
                            locked=is_locked,
                        )
                        for square_id, record_index, is_locked in ordered
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
        kind=TrajectoryKind.ILLUSTRATIVE,
        label=document.name,
    )


def _numerically_checked(entry: AnimationFrame) -> bool:
    """Whether a frame is a checked packing: a retained record, or checked feasible geometry."""
    if entry.record is not None:
        return entry.geometry.passed
    return entry.feasible is True and entry.geometry.passed


def transitions_reason(document: AnimationDocument) -> str | None:
    """Why this animation's motion must not be read as packings, or None if nothing says so.

    The statement is owed whenever any frame is guided or not numerically checked: a guided
    frame was pulled onto its packing, and an unchecked one is not known to be a packing, so
    a file that shows either moving is showing an illustration of a search, not a result.
    """
    document = decode_animation(document)
    total = len(document.frames)
    guided = sum(document.frame_is_guided(frame) for frame in document.frames)
    unchecked = sum(not _numerically_checked(frame) for frame in document.frames)
    if not guided and not unchecked:
        return None
    return (
        f"{TRANSITIONS_STATEMENT} {guided} of {total} frames are guided and {unchecked} of "
        f"{total} are not numerically checked."
    )


def describe_animation(document: AnimationDocument) -> str:
    """Describe evidence ancestry and independently checked invalid frames."""
    document = decode_animation(document)
    parts = [f"An animation of {document.n} unit squares in a square container."]
    if any(document.frame_is_guided(frame) for frame in document.frames):
        parts.append(
            "Some frames were guided onto a known packing rather than found by search."
        )
    unpacked = sum(not frame.geometry.passed for frame in document.frames)
    if unpacked:
        parts.append(f"{unpacked} of {len(document.frames)} frames are not valid packings.")
    # Any SVG with more than one frame moves, and what it draws between frames is a tween
    # nothing checks, so the statement is owed whether or not the frames themselves are checked.
    if len(document.frames) > 1:
        parts.append(TRANSITIONS_STATEMENT)
    return " ".join(parts)


def refuse_script(svg: str) -> None:
    """Refuse an SVG that carries a script: the export's promise is a file with none."""
    if re.search(r"<(?:[A-Za-z_][\w.-]*:)?script\b", svg, flags=re.IGNORECASE):
        raise ValueError("the rendered SVG contains a script element; it would not be inert")


def export_svg(document: AnimationDocument, *, width: int = 960) -> str:
    """Render one checked animation as a self-contained SVG with no script in it."""
    trajectory = trajectory_from_animation(document)
    palette = document.palette
    hue_name = palette.hue if palette is not None else None
    shade_name = palette.shade if palette is not None else None
    if hue_name == "uniform":
        raise ValueError("the SVG renderer does not support the uniform hue scheme")
    if shade_name in {"none", "evidence"}:
        raise ValueError(f"the SVG renderer does not support the {shade_name} shade scheme")
    spec = RenderSpec(
        hue_scheme=(HueScheme.INDEX if hue_name == "identity" else HueScheme.ANGLE),
        shade_scheme=ShadeScheme.CONTACTS,
        title=document.name,
        description=describe_animation(document),
        duration_seconds=Decimal(str(document.duration_seconds or 8.0)),
        width=width,
        annotations=AnnotationLevel.MINIMAL,
        overlays=frozenset(),
        view=ViewLevel.TRAJECTORY,
    )
    svg = render_packing_svg(trajectory.frames[-1], trajectory=trajectory, spec=spec)
    if len(trajectory.frames) > 1 and "@keyframes" not in svg:
        raise ValueError("an animation of several frames rendered without motion")
    refuse_script(svg)
    return svg
