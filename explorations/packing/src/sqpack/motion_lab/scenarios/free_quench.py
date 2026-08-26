"""Deterministic editable starts and the unconstrained free-quench scenario."""

from __future__ import annotations

import math
import random

from sqpack.motion_lab.contracts import (
    MAX_INTERACTIVE_SQUARES,
    Capability,
    Evidence,
    EvidenceStatus,
    FrameKind,
    Phase,
    PoseFrame,
    ScenarioDefinition,
    ScenarioRunner,
    SquarePose,
)
from sqpack.motion_lab.snap import EditorSquare, EditorState

FREE_QUENCH_SCENARIO_ID = "free-quench"
_PROPOSER_MULTIPLIER = 1_000_003


def deterministic_editor_start(*, n: int, seed: int, side: float) -> EditorState:
    """Replay the campaign's independently addressable uniform pose proposer."""
    if isinstance(n, bool) or not isinstance(n, int) or not 1 <= n <= MAX_INTERACTIVE_SQUARES:
        raise ValueError(
            f"square count must be an integer from 1 through {MAX_INTERACTIVE_SQUARES}"
        )
    if isinstance(seed, bool) or not isinstance(seed, int):
        raise TypeError("seed must be an integer")
    if not math.isfinite(side) or side <= 1:
        raise ValueError("starting container side must be finite and greater than one")
    generator = random.Random(_PROPOSER_MULTIPLIER * n + seed)
    x = [generator.uniform(0.5, side - 0.5) for _ in range(n)]
    y = [generator.uniform(0.5, side - 0.5) for _ in range(n)]
    theta = [generator.uniform(0, math.pi / 2) for _ in range(n)]
    return EditorState.with_singletons(
        side=side,
        squares=tuple(
            EditorSquare(square_id=index, x=x[index], y=y[index], theta=theta[index])
            for index in range(n)
        ),
    )


def free_quench_scenario(*, n: int, seed: int, side: float) -> ScenarioDefinition:
    """Build the interactive scenario declaration for one seeded editor baseline."""
    state = deterministic_editor_start(n=n, seed=seed, side=side)
    frame = PoseFrame(
        scenario_id=FREE_QUENCH_SCENARIO_ID,
        frame_kind=FrameKind.EDITOR_PREVIEW,
        container_side=state.side,
        squares=tuple(
            SquarePose(
                square_id=square.square_id,
                x=square.x,
                y=square.y,
                theta=square.theta,
                palette_index=square.square_id,
            )
            for square in state.squares
        ),
        phase=Phase.SETUP,
        evidence=Evidence(
            status=EvidenceStatus.EDITOR_INPUT,
            claim="A deterministic editable start; overlaps are allowed and marked.",
            source=f"uniform proposer n={n}, seed={seed}, side={side:.17g}",
        ),
    )
    return ScenarioDefinition(
        scenario_id=FREE_QUENCH_SCENARIO_ID,
        title="Setup and free quench",
        runner=ScenarioRunner.INTERACTIVE_SOLVER,
        capabilities=(
            Capability.EDIT_POSE,
            Capability.SETUP_SNAPPING,
            Capability.RANDOMIZE,
            Capability.RUN_QUENCH,
            Capability.PLAYBACK,
            Capability.SCRUB,
            Capability.DOWNLOAD_TRACE,
        ),
        initial_frame=frame,
    )
