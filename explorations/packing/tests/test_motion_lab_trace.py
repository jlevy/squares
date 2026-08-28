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


def test_free_pass_observation_preserves_the_result_and_its_counters() -> None:
    """The free sweep is the one path where the observer replaces an existing callback.

    Every other emission site appends a receipt after work already done, so it cannot
    change a result. `_free_sweep` instead receives a wrapped `solve_fixed`, which is
    the substitution most able to perturb the run, and the sweep-limited case above
    disables it. This is the same equivalence assertion with `free_pass` left on.
    """
    poses = (
        [0.5, 1.6, 0.5, 1.6, 1.05],
        [0.5, 0.5, 1.6, 1.6, 1.05],
        [0.0, 0.0, 0.0, 0.0, 0.3],
    )
    arguments = {
        "max_sweeps": 2,
        "span": TEST_SPAN,
        "span_min": TEST_SPAN,
        "time_budget": TEST_TIME_BUDGET_SECONDS,
        "free_pass": True,
    }
    baseline = quench_bracket(*poses, **arguments)
    observations: list[QuenchObservation] = []
    observed = quench_bracket(*poses, **arguments, observer=observations.append)

    assert observed == baseline
    assert observed.lp_solves == baseline.lp_solves
    assert observed.cell_changes == baseline.cell_changes
    assert observations[-1].kind is QuenchObservationKind.STOP


def test_event_counters_are_per_call_and_the_stop_carries_only_the_result_total() -> None:
    """`fixed-point` events are the ones in bijection with LP calls.

    Probes re-report the solve they asked for, so summing across kinds double-counts;
    the stop used to add the run total on top of that, making the column unsummable in
    three different ways at once.
    """
    request = QuenchRequest(
        side=1.6,
        x=(0.5,),
        y=(0.5,),
        theta=(0.0,),
        max_sweeps=4,
        time_budget=TEST_TIME_BUDGET_SECONDS,
    )
    trace = trace_quench_bracket(request)

    fixed_point_solves = sum(
        event.call_lp_solves or 0
        for event in trace.events
        if event.event_kind is TimelineEventKind.FIXED_POINT
    )
    assert fixed_point_solves == trace.result.lp_solves
    assert trace.events[-1].call_lp_solves == 0
    assert trace.events[-1].call_cell_changes == 0
    assert trace.events[-1].outcome is not None
