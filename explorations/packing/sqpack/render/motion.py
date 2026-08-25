"""Declarative one-pass motion with a final-state static fallback."""

from __future__ import annotations

import math
from decimal import Decimal
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


def unwrap_quarter_turn_angles(angles: tuple[float, ...]) -> tuple[float, ...]:
    if not angles:
        return ()
    result = [angles[0]]
    quarter_turn = math.pi / 2
    for angle in angles[1:]:
        candidates = [angle + multiple * quarter_turn for multiple in range(-4, 5)]
        result.append(
            min(candidates, key=lambda candidate: (abs(candidate - result[-1]), candidate))
        )
    return tuple(result)


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
        rules.append(
            f"{percentage}{{transform:translate({format_svg_number(dx)}px,{format_svg_number(dy)}px)}}"
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
    rules = []
    for index, track in enumerate(match_square_tracks(trajectory)):
        square_id = track[-1].square_id
        animation = f"sqpack-{square_id}"
        rules.append(f"@keyframes {animation}{{{square_keyframes(trajectory, index, scale)}}}")
        rules.append(
            f".motion-{square_id}{{animation:{animation} "
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
