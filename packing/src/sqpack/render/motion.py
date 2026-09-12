"""Declarative one-pass motion with a final-state static fallback."""

from __future__ import annotations

import math
from decimal import ROUND_HALF_EVEN, Decimal
from itertools import pairwise
from xml.etree import ElementTree as ET

from sqpack.render.model import EvidenceTier, PackingTrajectory
from sqpack.render.numbers import format_svg_number
from sqpack.render.svg import MOTION_MARKER, sub


def pose_of(square):
    """A square's centre and angle, from its pose when it has one and its corners when not.

    A frame built from a retained witness carries exact corners and no pose, and it must
    stay that way: attaching a float pose to it changes what the renderer draws. Full-side
    contact shading needs two edges exactly parallel, and a float angle is not exactly
    anything, so two of `n = 11`'s eleven squares came out a different green. Deriving the
    pose here instead means a record frame is the same drawing as its atlas rendering while
    the motion still has the numbers it needs.
    """
    if square.pose is not None:
        return (
            square.pose.centre.x.projected,
            square.pose.centre.y.projected,
            square.pose.angle.projected,
        )
    xs = [corner.x.projected for corner in square.corners]
    ys = [corner.y.projected for corner in square.corners]
    cx = sum(xs) / len(xs)
    cy = sum(ys) / len(ys)
    edge_x = xs[1] - xs[0]
    edge_y = ys[1] - ys[0]
    return cx, cy, Decimal(str(math.atan2(float(edge_y), float(edge_x))))


def match_square_tracks(trajectory: PackingTrajectory):
    final_order = tuple(square.square_id for square in trajectory.frames[-1].squares)
    tracks = []
    for index, square_id in enumerate(final_order):
        track = tuple(frame.squares[index] for frame in trajectory.frames)
        if any(square.square_id != square_id for square in track):
            raise ValueError("trajectory square identity or order changed")
        tracks.append(track)
    return tuple(tracks)


def keyframe_percentages(times: tuple[Decimal, ...]) -> tuple[str, ...]:
    if len(times) < 2 or times[-1] <= times[0]:
        raise ValueError("motion times require a positive range")
    span = times[-1] - times[0]
    return tuple(f"{format_svg_number((time - times[0]) * 100 / span)}%" for time in times)


QUARTER_TURN = Decimal(str(math.pi / 2))
"""A square is unchanged by a quarter turn, so every angle difference is reduced to the
smallest equivalent one before it is animated. Without that a square asked to go from
1 degree to 89 takes the long way round through 88 degrees of visible spin, when the two
poses differ by two degrees of actual square."""


def short_quarter_turn(delta: Decimal) -> Decimal:
    """The smallest rotation, in radians, that carries one square orientation to another."""
    turns = (delta / QUARTER_TURN).to_integral_value(rounding=ROUND_HALF_EVEN)
    return delta - turns * QUARTER_TURN


def validate_motion_trajectory(trajectory: PackingTrajectory) -> None:
    """Reject what the CSS motion model still cannot show, which is now much less.

    It used to refuse rotation outright and refuse any trajectory whose container side
    changed. Both were fatal for the atlas work: six of `n = 11`'s fourteen contacts join
    squares 40.2 degrees apart, and an ascent that adds one square per step resizes the
    container at every step by construction. What remains are the two things the keyframe
    emitters genuinely require -- a pose on every square, and time that does not run
    backwards.
    """
    for track in match_square_tracks(trajectory):
        if any(len(square.corners) < 2 for square in track):
            raise ValueError("motion requires square corners or poses")
    times = tuple(frame.logical_time for frame in trajectory.frames)
    if any(later < earlier for earlier, later in pairwise(times)):
        raise ValueError("motion requires non-decreasing logical time")


MUTED_SATURATION = "0.12"
"""How far the colour drops on a frame that is not a packing.

Saturation carries meaning here rather than mood. A square at full colour is one that has
locked into its final place; a muted one has not, and neither has the frame around it if
nothing in it is a packing. Tying colour to that means a viewer cannot mistake the
interesting middle of an animation for its answer, and it reads as the packing assembling
itself rather than as a crossfade.

Low on purpose. At a third of full saturation the muted state still competed with the
locked one for attention; an eighth lets the locked squares carry the picture, which is the
point of locking them one at a time."""


def square_keyframes(
    trajectory: PackingTrajectory,
    square_index: int,
    scale: Decimal,
    muted: tuple[tuple[bool, ...], ...] | None = None,
) -> str:
    percentages = keyframe_percentages(tuple(frame.logical_time for frame in trajectory.frames))
    final_x, final_y, final_angle = pose_of(trajectory.frames[-1].squares[square_index])
    rules = []
    for percentage, frame in zip(percentages, trajectory.frames, strict=True):
        px, py, angle = pose_of(frame.squares[square_index])
        dx = (px - final_x) * scale
        dy = -(py - final_y) * scale
        # Negated for the same reason dy is: the drawing's y runs down while the
        # mathematics runs up, so a counter-clockwise turn in the packing is a clockwise
        # one on screen.
        turn = -short_quarter_turn(angle - final_angle)
        degrees = turn * 180 / Decimal(str(math.pi))
        # Per square AND per frame, because locking is a property of one square at one
        # moment: the corner squares settle first and take their colour while the tilted
        # core is still moving, which is the whole reason to show the assembly this way.
        filter_rule = ""
        if muted is not None and muted[len(rules)][square_index]:
            filter_rule = f";filter:saturate({MUTED_SATURATION})"
        rules.append(
            f"{percentage}{{transform:translate({format_svg_number(dx)}px,"
            f"{format_svg_number(dy)}px) rotate({format_svg_number(degrees)}deg)"
            f"{filter_rule}}}"
        )
    return "".join(rules)


def container_keyframes(trajectory: PackingTrajectory) -> str:
    percentages = keyframe_percentages(tuple(frame.logical_time for frame in trajectory.frames))
    return "".join(f"{percentage}{{opacity:1}}" for percentage in percentages)


def append_square_motion(node: ET.Element, square_id: str) -> None:
    node.set("class", f"motion-{square_id}")


def append_container_motion(node: ET.Element) -> None:
    node.set("class", "motion-container")


def append_final_overlay_motion(node: ET.Element) -> None:
    node.set("class", "motion-final-overlay")


def append_motion_styles(
    root: ET.Element,
    trajectory: PackingTrajectory,
    *,
    scale: Decimal,
    duration_seconds: Decimal,
    reveal_final_overlay: bool = False,
    muted: tuple[tuple[bool, ...], ...] | None = None,
) -> None:
    validate_motion_trajectory(trajectory)
    if muted is None:
        # Derived from what each frame says it establishes, not passed in beside it. A
        # CANDIDATE frame is one nobody checked or one that is not a packing at all, and
        # those are exactly the frames whose colour should say so.
        # A square that says it has not locked is muted; otherwise the frame's own
        # evidence decides for all of them, which is what an animation with no notion of
        # locking can say.
        muted = tuple(
            tuple(
                not square.locked or frame.evidence is EvidenceTier.CANDIDATE
                for square in frame.squares
            )
            for frame in trajectory.frames
        )
    rules = []
    for index, track in enumerate(match_square_tracks(trajectory)):
        square_id = track[-1].square_id
        animation = f"sqpack-{square_id}"
        rules.append(
            f"@keyframes {animation}{{{square_keyframes(trajectory, index, scale, muted)}}}"
        )
        # transform-box and transform-origin are not decoration: CSS rotates about the
        # element's origin, which for an SVG child is the viewport's corner unless told
        # otherwise, so a square without them swings around the page instead of spinning
        # where it stands.
        rules.append(
            f".motion-{square_id}{{transform-box:fill-box;transform-origin:center;"
            f"animation:{animation} "
            f"{format_svg_number(duration_seconds)}s ease-in-out 1 forwards}}"
        )
    if reveal_final_overlay:
        rules.append("@keyframes sqpack-final-overlay{0%{opacity:0}100%{opacity:1}}")
        rules.append(
            ".motion-final-overlay{animation:sqpack-final-overlay "
            f"{format_svg_number(duration_seconds)}s step-end 1 forwards}}"
        )
    css = "@media (prefers-reduced-motion: no-preference){" + "".join(rules) + "}"
    style = sub(root, "style", {"data-sqpack-style": MOTION_MARKER})
    style.text = css
