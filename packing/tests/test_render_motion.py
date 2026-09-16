"""What the CSS motion model can express, asserted on cases it used to refuse.

Both trajectories here were rejected outright before: one rotates, and one resizes its
container. They are the two shapes the atlas work needs -- six of `n = 11`'s fourteen
contacts join squares 40.2 degrees apart, and an ascent that adds one square per step
changes the container at every step -- so each test fails against the old validator and
passes against the new one.
"""

from __future__ import annotations

import math
import re
from dataclasses import replace
from decimal import Decimal
from itertools import pairwise
from xml.etree import ElementTree as ET

import pytest

from sqpack.render import RenderSpec, ViewLevel, render_packing_svg
from sqpack.render.model import (
    CheckKind,
    CheckSummary,
    EvidenceTier,
    PackingFrame,
    PackingTrajectory,
    Point2,
    RigidPose,
    SquareGeometry,
    TrajectoryKind,
)
from sqpack.render.motion import (
    QUARTER_TURN,
    append_motion_styles,
    short_quarter_turn,
    square_keyframes,
    validate_motion_trajectory,
)
from sqpack.render.numbers import scalar_from_float as _scalar


def _square(name: str, x: float, y: float, angle: float) -> SquareGeometry:
    c, s = math.cos(angle) / 2, math.sin(angle) / 2
    corners = tuple(
        Point2(_scalar(x + px), _scalar(y + py))
        for px, py in ((c - s, s + c), (-c - s, -s + c), (-c + s, -s - c), (c + s, s - c))
    )
    return SquareGeometry(
        name, corners, RigidPose(Point2(_scalar(x), _scalar(y)), _scalar(angle))
    )


def _trajectory(frames: list[tuple[float, float, list[tuple[float, float, float]]]]):
    return PackingTrajectory(
        frames=tuple(
            PackingFrame(
                container_side=_scalar(side),
                squares=tuple(
                    _square(f"square-{i:02d}", *pose) for i, pose in enumerate(poses)
                ),
                logical_time=Decimal(str(t)),
            )
            for t, side, poses in frames
        ),
        kind=TrajectoryKind.ILLUSTRATIVE,
        label="test",
    )


def test_a_rotating_trajectory_is_accepted_and_emits_its_rotation() -> None:
    """Rotation was refused outright; it is the motion the packings actually make."""
    traj = _trajectory(
        [
            (0.0, 4.0, [(1.0, 1.0, 0.0), (2.5, 1.0, 0.0)]),
            (1.0, 4.0, [(1.0, 1.0, 0.4), (2.5, 1.0, 0.0)]),
        ]
    )
    validate_motion_trajectory(traj)
    css = square_keyframes(traj, 0, Decimal(100))
    assert "rotate(" in css
    # 0 rad at the first frame against 0.4 at the last, so the keyframe turns the square
    # back by -0.4 rad, negated for the drawing's y: CSS turns clockwise for a positive
    # angle, which is the way a counter-clockwise packing turn is undone on screen.
    assert "rotate(22.9" in css
    assert "rotate(-22.9" not in css


def test_rotation_takes_the_short_way_round_a_quarter_turn() -> None:
    """A square is unchanged by a quarter turn, so 1 degree to 89 is two degrees of motion.

    Without this a square asked for that pair spins through 88 degrees to arrive at a
    picture it was already showing.
    """
    nearly_a_quarter = QUARTER_TURN - Decimal("0.02")
    assert abs(short_quarter_turn(nearly_a_quarter)) <= Decimal("0.03")
    assert abs(short_quarter_turn(-nearly_a_quarter)) <= Decimal("0.03")
    assert short_quarter_turn(Decimal("0.1")) == Decimal("0.1")


def _rotations(css: str) -> list[Decimal]:
    return [Decimal(value) for value in re.findall(r"rotate\((-?[0-9.]+)deg\)", css)]


def test_rotation_unwraps_along_the_track_across_the_eighth_turn() -> None:
    """Each step turns the short way from the step before it, not from the final pose.

    Reducing every keyframe against the final angle on its own makes a track that crosses
    45 degrees from it jump from +44 to -44 between neighbours, and CSS interpolates that
    as 88 degrees of spin where the square turned two.
    """
    degrees = [50, 48, 46, 44, 42, 0]
    angles = [math.radians(angle) for angle in degrees]
    traj = _trajectory([(float(t), 4.0, [(1.0, 1.0, angle)]) for t, angle in enumerate(angles)])
    turns = _rotations(square_keyframes(traj, 0, Decimal(100)))
    assert len(turns) == len(degrees)
    # Negated for the drawing's y, so a square starting 50 degrees counter-clockwise of its
    # final pose starts 50 degrees clockwise on screen and turns back from there.
    assert [round(turn, 9) for turn in turns] == [-50, -48, -46, -44, -42, 0]
    to_degrees = Decimal(180) / Decimal(str(math.pi))
    for index, (earlier, later) in enumerate(pairwise(turns)):
        delta = _scalar(angles[index]).projected - _scalar(angles[index + 1]).projected
        assert abs(earlier - later) <= 45
        assert abs((earlier - later) + short_quarter_turn(delta) * to_degrees) < Decimal("1e-9")


def _container_outlines(svg: str) -> list[str]:
    return re.findall(r'<rect\b[^>]*data-feature="container-outline"[^>]*>', svg)


def test_a_resizing_container_is_accepted() -> None:
    """A changing side was refused, and the atlas ascent changes it at every step.

    Accepted is not animated: the outline is drawn once, at the final frame's side, and no
    container keyframes are emitted, so the drawing matches one whose side never changed.
    """
    traj = _trajectory(
        [
            (0.0, 4.5, [(1.0, 1.0, 0.0)]),
            (1.0, 4.0, [(1.0, 1.0, 0.0)]),
        ]
    )
    validate_motion_trajectory(traj)
    fixed = _trajectory([(0.0, 4.0, [(1.0, 1.0, 0.0)]), (1.0, 4.0, [(1.0, 1.0, 0.0)])])
    spec = RenderSpec(view=ViewLevel.TRAJECTORY)
    resizing_svg = render_packing_svg(traj.frames[-1], trajectory=traj, spec=spec)
    fixed_svg = render_packing_svg(fixed.frames[-1], trajectory=fixed, spec=spec)
    assert len(_container_outlines(resizing_svg)) == 1
    # The outline rect alone cannot say which side it is drawn at, because the panel scale
    # follows that side; equality with the fixed-side drawing can.
    assert resizing_svg == fixed_svg
    assert "motion-container" not in resizing_svg
    assert "sqpack-container" not in resizing_svg


def test_motion_still_refuses_what_it_cannot_draw() -> None:
    """Lifting two restrictions is not lifting all of them."""
    traj = _trajectory([(0.0, 4.0, [(1.0, 1.0, 0.0)]), (1.0, 4.0, [(1.0, 1.0, 0.0)])])
    backwards = PackingTrajectory(
        frames=(traj.frames[1], traj.frames[0]), kind=traj.kind, label=traj.label
    )
    with pytest.raises(ValueError, match="non-decreasing"):
        validate_motion_trajectory(backwards)


def test_a_rotating_square_spins_where_it_stands() -> None:
    """CSS rotates about the element's origin, which is not the square unless it is told.

    Without `transform-box`/`transform-origin` a square swings around the viewport corner
    instead of turning in place, which looks like a bug and is one.
    """
    traj = _trajectory([(0.0, 4.0, [(1.0, 1.0, 0.3)]), (1.0, 4.0, [(1.0, 1.0, 0.0)])])
    root = ET.Element("svg")
    append_motion_styles(root, traj, scale=Decimal(100), duration_seconds=Decimal(4))
    css = "".join(node.text or "" for node in root.iter())
    assert "transform-box:fill-box" in css
    assert "transform-origin:center" in css


def test_colour_is_muted_exactly_where_a_frame_is_not_a_packing() -> None:
    """Saturation carries meaning rather than mood.

    A frame at full colour is an arrangement that actually is a packing; a muted one is
    not. Tying the two together is what stops a viewer reading the interesting middle of a
    transition as its answer, and it costs nothing because the frame already declares what
    it establishes.
    """
    checked = CheckSummary(
        passed=True,
        kind=CheckKind.NUMERICAL,
        method="test",
        arithmetic="binary64",
        precision="53",
        rounding="nearest-even",
        tolerance="1e-9",
    )
    traj = _trajectory([(0.0, 4.0, [(1.0, 1.0, 0.0)]), (1.0, 4.0, [(1.5, 1.0, 0.0)])])
    settled = PackingTrajectory(
        frames=(
            PackingFrame(
                container_side=traj.frames[0].container_side,
                squares=traj.frames[0].squares,
                logical_time=traj.frames[0].logical_time,
                evidence=EvidenceTier.CANDIDATE,
            ),
            PackingFrame(
                container_side=traj.frames[1].container_side,
                squares=traj.frames[1].squares,
                logical_time=traj.frames[1].logical_time,
                evidence=EvidenceTier.NUMERICALLY_CHECKED,
                check=checked,
            ),
        ),
        kind=traj.kind,
        label=traj.label,
    )
    css = square_keyframes(settled, 0, Decimal(100), ((True,), (False,)))
    assert css.count("filter:saturate") == 1, "only the unchecked frame is muted"
    assert css.index("filter:saturate") < css.index("100%"), "and it is the first one"


def test_muting_is_derived_from_locking_and_evidence_when_not_passed_in() -> None:
    """With no mask given, a square is muted where it has not locked or nothing is checked.

    The renderer calls `append_motion_styles` without a mask, so this derivation, not the
    pass-in path above, is what every rendered trajectory's colour actually comes from.
    """
    checked = CheckSummary(
        passed=True,
        kind=CheckKind.NUMERICAL,
        method="test",
        arithmetic="binary64",
        precision="53",
        rounding="nearest-even",
        tolerance="1e-9",
    )
    traj = _trajectory(
        [
            (0.0, 4.0, [(1.0, 1.0, 0.0), (2.5, 1.0, 0.0)]),
            (1.0, 4.0, [(1.5, 1.0, 0.0), (2.5, 1.0, 0.0)]),
        ]
    )
    first, last = traj.frames
    unlocked = replace(last.squares[0], locked=False)
    derived = replace(
        traj,
        frames=(
            first,
            replace(
                last,
                squares=(unlocked, last.squares[1]),
                evidence=EvidenceTier.NUMERICALLY_CHECKED,
                check=checked,
            ),
        ),
    )
    root = ET.Element("svg")
    append_motion_styles(root, derived, scale=Decimal(100), duration_seconds=Decimal(4))
    css = "".join(node.text or "" for node in root.iter())
    blocks = re.findall(r"@keyframes sqpack-(square-[0-9]+)\{((?:[^{}]*\{[^}]*\})+)\}", css)
    muted = {
        square_id: ["filter:saturate(" in rule for rule in re.findall(r"%\{([^}]*)\}", body)]
        for square_id, body in blocks
    }
    # The first frame is a CANDIDATE, so both squares are muted there; in the checked last
    # frame only the square that says it has not locked stays muted.
    assert muted == {"square-00": [True, True], "square-01": [True, False]}
