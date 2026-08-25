"""Frits Göbel's proved optimal ten-square packing as an f64 search seed.

The construction is read from Kingbird's primary SVG.  Eight axis-aligned squares form
opposite four-square corners; two central squares form a 45-degree strip.  This module
is an input fixture for numerical search and replay, not an exact verifier.
"""

from __future__ import annotations

import math
from typing import TypedDict

SOURCE_ID = "gobel10-svg-v1"
SOURCE_URL = "https://kingbird.myphotos.cc/packing/square-10.svg"
SOURCE_FIXTURE = "cases/gobel10/packing.py"


class Pose(TypedDict):
    side: float
    x: list[float]
    y: list[float]
    theta: list[float]


def pose() -> Pose:
    """Return the labelled pose encoded by the source SVG."""
    root_two = math.sqrt(2.0)
    side = 3.0 + root_two / 2.0
    x = [
        0.5,
        1.5,
        0.5,
        side - 0.5,
        side - 0.5,
        side - 1.5,
        side - 0.5,
        0.5,
        1.5 + 1.0 / root_two,
        1.5,
    ]
    y = [
        0.5,
        0.5,
        1.5,
        0.5,
        side - 0.5,
        side - 0.5,
        side - 1.5,
        side - 0.5,
        1.5,
        1.5 + 1.0 / root_two,
    ]
    theta = [0.0] * 8 + [math.pi / 4.0] * 2
    return {"side": side, "x": x, "y": y, "theta": theta}
