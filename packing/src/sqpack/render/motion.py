"""Declarative one-pass motion with a final-state static fallback."""

from __future__ import annotations

import math
from decimal import ROUND_HALF_EVEN, Decimal
from itertools import pairwise
from xml.etree import ElementTree as ET

from sqpack.render.model import PackingTrajectory
from sqpack.render.numbers import format_svg_number
from sqpack.render.svg import MOTION_MARKER, sub


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


def validate_trajectory(trajectory: PackingTrajectory) -> None:
    """Reject what the CSS motion model still cannot show, which is now much less.

    It used to refuse rotation outright and refuse any trajectory whose container side
    changed. Both were fatal for the atlas work: six of `n = 11`'s fourteen contacts join
    squares 40.2 degrees apart, and an ascent that adds one square per step resizes the
    container at every step by construction. What remains are the two things the keyframe
    emitters genuinely require -- a pose on every square, and time that does not run
    backwards.
    """
    for track in match_square_tracks(trajectory):
        if any(square.pose is None for square in track):
            raise ValueError("motion requires square poses")
    times = tuple(frame.logical_time for frame in trajectory.frames)
    if any(later < earlier for earlier, later in pairwise(times)):
        raise ValueError("motion requires non-decreasing logical time")


def square_keyframes(trajectory: PackingTrajectory, square_index: int, scale: Decimal) -> str:
    percentages = keyframe_percentages(tuple(frame.logical_time for frame in trajectory.frames))
    final = trajectory.frames[-1].squares[square_index].pose
    if final is None:
        raise ValueError("motion requires square poses")
    rules = []
    for percentage, frame in zip(percentages, trajectory.frames, strict=True):
        pose = frame.squares[square_index].pose
        if pose is None:
            raise ValueError("motion requires square poses")
        dx = (pose.centre.x.projected - final.centre.x.projected) * scale
        dy = -(pose.centre.y.projected - final.centre.y.projected) * scale
        # Negated for the same reason dy is: the drawing's y runs down while the
        # mathematics runs up, so a counter-clockwise turn in the packing is a clockwise
        # one on screen.
        turn = -short_quarter_turn(pose.angle.projected - final.angle.projected)
        degrees = turn * 180 / Decimal(str(math.pi))
        rules.append(
            f"{percentage}{{transform:translate({format_svg_number(dx)}px,"
            f"{format_svg_number(dy)}px) rotate({format_svg_number(degrees)}deg)}}"
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
) -> None:
    validate_trajectory(trajectory)
    rules = []
    for index, track in enumerate(match_square_tracks(trajectory)):
        square_id = track[-1].square_id
        animation = f"sqpack-{square_id}"
        rules.append(f"@keyframes {animation}{{{square_keyframes(trajectory, index, scale)}}}")
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
