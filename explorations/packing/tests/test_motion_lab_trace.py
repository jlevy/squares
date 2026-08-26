"""Behavior-preserving observation and Motion Lab trace projection."""

from __future__ import annotations

from sqpack.motion_lab.contracts import (
    Phase,
    QuenchRequest,
    TimelineEventKind,
)
from sqpack.motion_lab.trace import trace_quench_bracket
from sqpack.research.quench import (
    QuenchObservation,
    QuenchObservationKind,
    quench_bracket,
)

TEST_MAX_SWEEPS = 1
TEST_SPAN = 1e-6
TEST_TIME_BUDGET_SECONDS = 10.0


def test_observer_records_existing_solver_work_without_changing_result() -> None:
    baseline = quench_bracket(
        [0.5],
        [0.5],
        [0.0],
        max_sweeps=TEST_MAX_SWEEPS,
        span=TEST_SPAN,
        span_min=TEST_SPAN,
        time_budget=TEST_TIME_BUDGET_SECONDS,
        free_pass=False,
    )
    observations: list[QuenchObservation] = []
    observed = quench_bracket(
        [0.5],
        [0.5],
        [0.0],
        max_sweeps=TEST_MAX_SWEEPS,
        span=TEST_SPAN,
        span_min=TEST_SPAN,
        time_budget=TEST_TIME_BUDGET_SECONDS,
        free_pass=False,
        observer=observations.append,
    )

    assert observed == baseline
    assert (
        sum(
            observation.kind is QuenchObservationKind.FIXED_POINT
            for observation in observations
        )
        == observed.fixed_point_evaluations
    )
    assert observations[-1].kind is QuenchObservationKind.STOP
    assert observations[-1].detail == observed.reason
    assert any(
        observation.kind is QuenchObservationKind.ANGLE_PROBE for observation in observations
    )


def test_trace_adapter_labels_setup_lp_rotation_and_stop_without_editor_groups() -> None:
    request = QuenchRequest(
        side=1.6,
        x=(0.5,),
        y=(0.5,),
        theta=(0.0,),
        max_sweeps=TEST_MAX_SWEEPS,
        time_budget=TEST_TIME_BUDGET_SECONDS,
    )
    trace = trace_quench_bracket(
        request,
        span=TEST_SPAN,
        span_min=TEST_SPAN,
        free_pass=False,
    )

    assert trace.events[0].event_kind is TimelineEventKind.SETUP_RELEASED
    assert trace.events[0].phase is Phase.SETUP
    assert trace.events[-1].event_kind is TimelineEventKind.STOP
    assert trace.events[-1].phase is Phase.STOP
    assert any(event.phase is Phase.FIXED_ANGLE_LP for event in trace.events)
    assert any(event.phase is Phase.ANGULAR_PROBE for event in trace.events)
    assert trace.result.fixed_point_evaluations == sum(
        event.event_kind is TimelineEventKind.FIXED_POINT for event in trace.events
    )
    assert "groups" not in trace.request.to_record()
