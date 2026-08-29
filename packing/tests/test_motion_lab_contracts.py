"""Versioned contracts shared by every Motion Lab scenario."""

from __future__ import annotations

import json
import math
from typing import cast

import pytest

from sqpack.motion_lab.contracts import (
    Capability,
    Evidence,
    EvidenceStatus,
    FrameKind,
    FrameOverlay,
    OverlayKind,
    Phase,
    PoseFrame,
    QuenchRequest,
    QuenchResultRecord,
    QuenchTrace,
    ScenarioDefinition,
    ScenarioRunner,
    SolverKind,
    SquarePose,
    TimelineEvent,
    TimelineEventKind,
    canonical_json,
    quench_request_from_record,
)


def _frame() -> PoseFrame:
    return PoseFrame(
        scenario_id="free-quench",
        frame_kind=FrameKind.NUMERICAL_STATE,
        container_side=2.25,
        squares=(
            SquarePose(square_id=0, x=0.5, y=0.5, theta=0.0, palette_index=0),
            SquarePose(square_id=1, x=1.5, y=1.5, theta=0.25, palette_index=1),
        ),
        phase=Phase.FIXED_ANGLE_LP,
        evidence=Evidence(
            status=EvidenceStatus.NUMERICALLY_CHECKED,
            claim="One retained floating-point solver state.",
            source="sqpack.research.quench",
        ),
        overlays=(
            FrameOverlay(
                kind=OverlayKind.CONTACT,
                square_ids=(0, 1),
                label="numerically detected contact",
            ),
        ),
    )


def _request() -> QuenchRequest:
    return QuenchRequest(
        side=2.25,
        x=(0.5, 1.5),
        y=(0.5, 1.5),
        theta=(0.0, 0.25),
        solver=SolverKind.QUENCH_BRACKET,
        max_sweeps=4,
        time_budget=3.0,
    )


def test_scenario_contract_declares_runner_capabilities_and_initial_evidence() -> None:
    scenario = ScenarioDefinition(
        scenario_id="free-quench",
        title="Setup and free quench",
        runner=ScenarioRunner.INTERACTIVE_SOLVER,
        capabilities=(
            Capability.EDIT_POSE,
            Capability.SETUP_SNAPPING,
            Capability.RUN_QUENCH,
        ),
        initial_frame=_frame(),
    )

    record = scenario.to_record()
    assert record["contract"] == "packing.squares:MotionLabScenario/v1"
    assert record["schema_version"] == 1
    assert record["runner"] == "interactive-solver"
    assert record["capabilities"] == [
        "edit-pose",
        "setup-snapping",
        "run-quench",
    ]
    initial_frame = cast(dict[str, object], record["initial_frame"])
    evidence = cast(dict[str, object], initial_frame["evidence"])
    assert evidence["status"] == "numerically-checked"
    overlays = cast(list[dict[str, object]], initial_frame["overlays"])
    assert overlays == [
        {
            "kind": "contact",
            "square_ids": [0, 1],
            "points": [],
            "label": "numerically detected contact",
        }
    ]


def test_scenario_contract_rejects_ambiguous_or_unstable_capabilities() -> None:
    with pytest.raises(ValueError, match="stable order"):
        ScenarioDefinition(
            scenario_id="free-quench",
            title="Setup and free quench",
            runner=ScenarioRunner.INTERACTIVE_SOLVER,
            capabilities=(Capability.RUN_QUENCH, Capability.EDIT_POSE),
            initial_frame=_frame(),
        )
    with pytest.raises(ValueError, match="unique"):
        ScenarioDefinition(
            scenario_id="free-quench",
            title="Setup and free quench",
            runner=ScenarioRunner.INTERACTIVE_SOLVER,
            capabilities=(Capability.EDIT_POSE, Capability.EDIT_POSE),
            initial_frame=_frame(),
        )


def test_pose_frame_requires_finite_stably_ordered_geometry() -> None:
    with pytest.raises(ValueError, match="finite"):
        SquarePose(square_id=0, x=math.nan, y=0.5, theta=0.0, palette_index=0)
    with pytest.raises(ValueError, match="stable square-ID order"):
        PoseFrame(
            scenario_id="free-quench",
            frame_kind=FrameKind.EDITOR_PREVIEW,
            container_side=2.25,
            squares=tuple(reversed(_frame().squares)),
            phase=Phase.SETUP,
            evidence=_frame().evidence,
        )


def test_quench_request_round_trip_accepts_only_phase_one_solver_fields() -> None:
    request = _request()
    record = request.to_record()

    assert quench_request_from_record(record) == request
    assert set(record) == {
        "contract",
        "schema_version",
        "side",
        "x",
        "y",
        "theta",
        "solver",
        "max_sweeps",
        "time_budget",
    }

    with pytest.raises(ValueError, match="unknown quench-request fields: groups"):
        quench_request_from_record(record | {"groups": [[0, 1]]})
    with pytest.raises(ValueError, match="same non-zero length"):
        quench_request_from_record(record | {"theta": [0.0]})
    with pytest.raises(ValueError, match="contract"):
        quench_request_from_record(record | {"contract": "unversioned"})


def test_quench_trace_has_stable_sequence_and_canonical_serialization() -> None:
    frame = _frame()
    request = _request()
    trace = QuenchTrace(
        request=request,
        events=(
            TimelineEvent(
                sequence=0,
                event_kind=TimelineEventKind.SETUP_RELEASED,
                phase=Phase.SETUP,
                frame=PoseFrame(
                    scenario_id=frame.scenario_id,
                    frame_kind=FrameKind.EDITOR_PREVIEW,
                    container_side=frame.container_side,
                    squares=frame.squares,
                    phase=Phase.SETUP,
                    evidence=frame.evidence,
                ),
                detail="Editor groups released; request contains poses only.",
            ),
            TimelineEvent(
                sequence=1,
                event_kind=TimelineEventKind.FIXED_POINT,
                phase=Phase.FIXED_ANGLE_LP,
                frame=frame,
                detail="Fixed-angle cell settled.",
            ),
            TimelineEvent(
                sequence=2,
                event_kind=TimelineEventKind.STOP,
                phase=Phase.STOP,
                frame=frame,
                detail="Sweep limit.",
            ),
        ),
        result=QuenchResultRecord(
            side=2.25,
            x=(0.5, 1.5),
            y=(0.5, 1.5),
            theta=(0.0, 0.25),
            lp_solves=7,
            angle_steps=1,
            converged=False,
            cell_changes=0,
            reason="sweep limit",
        ),
    )

    first = canonical_json(trace)
    second = canonical_json(trace)
    decoded = json.loads(first)
    assert first == second
    assert decoded["contract"] == "packing.squares:QuenchTrace/v1"
    assert [event["sequence"] for event in decoded["events"]] == [0, 1, 2]
    assert decoded["events"][0]["event_kind"] == "setup-released"
    assert decoded["events"][1]["frame"]["frame_kind"] == "numerical-state"

    with pytest.raises(ValueError, match="contiguous"):
        QuenchTrace(
            request=request,
            events=(trace.events[0], trace.events[2]),
            result=trace.result,
        )
