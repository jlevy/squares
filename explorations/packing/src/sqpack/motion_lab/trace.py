"""Project read-only quench observations into the shared Motion Lab timeline."""

from __future__ import annotations

from sqpack.motion_lab.contracts import (
    Evidence,
    EvidenceStatus,
    FrameKind,
    Phase,
    PoseFrame,
    ProbeOutcome,
    QuenchRequest,
    QuenchResultRecord,
    QuenchTrace,
    SolverKind,
    SquarePose,
    TimelineEvent,
    TimelineEventKind,
)
from sqpack.research.quench import (
    QuenchObservation,
    QuenchObservationKind,
    QuenchObservationOutcome,
    QuenchResult,
    quench_bracket,
)

FREE_QUENCH_SCENARIO_ID = "free-quench"

_NUMERICAL_EVIDENCE = Evidence(
    status=EvidenceStatus.NUMERICALLY_CHECKED,
    claim="A retained binary64 state computed by the numerical quench.",
    source="sqpack.research.quench",
)
_EDITOR_EVIDENCE = Evidence(
    status=EvidenceStatus.EDITOR_INPUT,
    claim="An editable starting pose; feasibility has not been established.",
    source="Motion Lab editor",
)

_EVENT_PRESENTATION = {
    QuenchObservationKind.FIXED_POINT: (
        TimelineEventKind.FIXED_POINT,
        Phase.FIXED_ANGLE_LP,
        FrameKind.NUMERICAL_STATE,
    ),
    QuenchObservationKind.ANGLE_PROBE: (
        TimelineEventKind.ANGLE_PROBE,
        Phase.ANGULAR_PROBE,
        FrameKind.PROBE,
    ),
    QuenchObservationKind.ANGLE_ACCEPTED: (
        TimelineEventKind.ANGLE_ACCEPTED,
        Phase.ANGLE_ACCEPTED,
        FrameKind.NUMERICAL_STATE,
    ),
    QuenchObservationKind.CELL_CHANGED: (
        TimelineEventKind.CELL_CHANGED,
        Phase.CELL_CHANGE,
        FrameKind.NUMERICAL_STATE,
    ),
    QuenchObservationKind.STOP: (
        TimelineEventKind.STOP,
        Phase.STOP,
        FrameKind.NUMERICAL_STATE,
    ),
}

_PROBE_OUTCOMES = {
    QuenchObservationOutcome.EVALUATED: ProbeOutcome.EVALUATED,
    QuenchObservationOutcome.ACCEPTED: ProbeOutcome.ACCEPTED,
    QuenchObservationOutcome.REJECTED: ProbeOutcome.REJECTED,
    QuenchObservationOutcome.UNSETTLED: ProbeOutcome.UNSETTLED,
    QuenchObservationOutcome.BUDGET_CUTOFF: ProbeOutcome.BUDGET_CUTOFF,
}

# Probes and stops are the two events whose disposition is a decision rather than a
# state: a probe was accepted or rejected, and a run stopped on its budget, on
# convergence, or unconverged. Every other kind reports geometry and carries no verdict.
_OUTCOME_KINDS = frozenset({QuenchObservationKind.ANGLE_PROBE, QuenchObservationKind.STOP})


def _event_outcome(observation: QuenchObservation) -> ProbeOutcome | None:
    if observation.kind not in _OUTCOME_KINDS:
        return None
    outcome = _PROBE_OUTCOMES.get(observation.outcome)
    if outcome is None:
        raise ValueError(f"unmapped quench observation outcome: {observation.outcome}")
    return outcome


def _pose_frame(
    *,
    side: float,
    x: tuple[float, ...],
    y: tuple[float, ...],
    theta: tuple[float, ...],
    frame_kind: FrameKind,
    phase: Phase,
    evidence: Evidence,
) -> PoseFrame:
    return PoseFrame(
        scenario_id=FREE_QUENCH_SCENARIO_ID,
        frame_kind=frame_kind,
        container_side=side,
        squares=tuple(
            SquarePose(
                square_id=index,
                x=center_x,
                y=center_y,
                theta=angle,
                palette_index=index,
            )
            for index, (center_x, center_y, angle) in enumerate(zip(x, y, theta, strict=True))
        ),
        phase=phase,
        evidence=evidence,
    )


def _result_record(result: QuenchResult) -> QuenchResultRecord:
    return QuenchResultRecord(
        side=result.side,
        x=tuple(result.x),
        y=tuple(result.y),
        theta=tuple(result.theta),
        lp_solves=result.lp_solves,
        angle_steps=result.angle_steps,
        converged=result.converged,
        cell_changes=result.cell_changes,
        reason=result.reason,
        contacts=tuple(sorted(result.contacts)),
        fixed_point_evaluations=result.fixed_point_evaluations,
        fixed_point_settled=result.fixed_point_settled,
        fixed_point_unsettled=result.fixed_point_unsettled,
    )


def _project_trace(
    request: QuenchRequest,
    observations: list[QuenchObservation],
    result: QuenchResult,
) -> QuenchTrace:
    events = [
        TimelineEvent(
            sequence=0,
            event_kind=TimelineEventKind.SETUP_RELEASED,
            phase=Phase.SETUP,
            frame=_pose_frame(
                side=request.side,
                x=request.x,
                y=request.y,
                theta=request.theta,
                frame_kind=FrameKind.EDITOR_PREVIEW,
                phase=Phase.SETUP,
                evidence=_EDITOR_EVIDENCE,
            ),
            detail="Editor groups released; numerical request contains poses only.",
        )
    ]
    for observation in observations:
        event_kind, phase, frame_kind = _EVENT_PRESENTATION[observation.kind]
        events.append(
            TimelineEvent(
                sequence=len(events),
                event_kind=event_kind,
                phase=phase,
                frame=_pose_frame(
                    side=observation.side,
                    x=observation.x,
                    y=observation.y,
                    theta=observation.theta,
                    frame_kind=frame_kind,
                    phase=phase,
                    evidence=_NUMERICAL_EVIDENCE,
                ),
                detail=observation.detail,
                outcome=_event_outcome(observation),
                call_lp_solves=observation.call_lp_solves,
                call_cell_changes=observation.call_cell_changes,
            )
        )
    return QuenchTrace(
        request=request,
        events=tuple(events),
        result=_result_record(result),
    )


def trace_quench_bracket(
    request: QuenchRequest,
    *,
    span: float = 0.05,
    span_min: float = 1e-9,
    span_shrink: float = 0.1,
    tol: float = 1e-12,
    class_tol: float = 1e-2,
    free_pass: bool = True,
) -> QuenchTrace:
    """Run the declared solver once and retain only events emitted by that call."""
    if request.solver is not SolverKind.QUENCH_BRACKET:
        raise ValueError(f"unsupported Motion Lab solver: {request.solver}")
    observations: list[QuenchObservation] = []
    result = quench_bracket(
        request.x,
        request.y,
        request.theta,
        max_sweeps=request.max_sweeps,
        span=span,
        span_min=span_min,
        span_shrink=span_shrink,
        tol=tol,
        class_tol=class_tol,
        time_budget=request.time_budget,
        free_pass=free_pass,
        observer=observations.append,
    )
    return _project_trace(request, observations, result)
