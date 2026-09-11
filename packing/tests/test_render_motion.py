"""What the CSS motion model can express, asserted on cases it used to refuse.

Both trajectories here were rejected outright before: one rotates, and one resizes its
container. They are the two shapes the atlas work needs -- six of `n = 11`'s fourteen
contacts join squares 40.2 degrees apart, and an ascent that adds one square per step
changes the container at every step -- so each test fails against the old validator and
passes against the new one.
"""

from __future__ import annotations

import math
from decimal import Decimal
from xml.etree import ElementTree as ET

import pytest

from sqpack.render.model import (
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
    # 0.4 rad at the first frame against 0 at the last, negated for the drawing's y.
    assert "rotate(-22.9" in css or "rotate(22.9" in css


def test_rotation_takes_the_short_way_round_a_quarter_turn() -> None:
    """A square is unchanged by a quarter turn, so 1 degree to 89 is two degrees of motion.

    Without this a square asked for that pair spins through 88 degrees to arrive at a
    picture it was already showing.
    """
    nearly_a_quarter = QUARTER_TURN - Decimal("0.02")
    assert abs(short_quarter_turn(nearly_a_quarter)) <= Decimal("0.03")
    assert abs(short_quarter_turn(-nearly_a_quarter)) <= Decimal("0.03")
    assert short_quarter_turn(Decimal("0.1")) == Decimal("0.1")


def test_a_resizing_container_is_accepted() -> None:
    """A changing side was refused, and the atlas ascent changes it at every step."""
    traj = _trajectory(
        [
            (0.0, 4.5, [(1.0, 1.0, 0.0)]),
            (1.0, 4.0, [(1.0, 1.0, 0.0)]),
        ]
    )
    validate_motion_trajectory(traj)


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
    from sqpack.render.model import CheckKind, CheckSummary, EvidenceTier

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
    css = square_keyframes(settled, 0, Decimal(100), (True, False))
    assert css.count("filter:saturate") == 1, "only the unchecked frame is muted"
    assert css.index("filter:saturate") < css.index("100%"), "and it is the first one"
