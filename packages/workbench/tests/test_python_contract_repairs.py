"""Regression controls for imported animations and executable Python strategies."""

from __future__ import annotations

import json
import math
from dataclasses import replace
from pathlib import Path
from typing import Any

import jsonschema
import numpy as np
import pytest

from sqpack.render.model import EvidenceTier, PackingTrajectory
from workbench_tools.animation_records import (
    ANIMATION_CONTRACT,
    animation_to_row,
    decode_animation,
    decode_legacy_animation,
)
from workbench_tools.animation_render import (
    describe_animation,
    export_svg,
    muting_from_animation,
    trajectory_from_animation,
)
from workbench_tools.ascent import render_ascent
from workbench_tools.packing_contracts import (
    GeometryIssue,
    PackingContractError,
    check_unit_square_packing,
)
from workbench_tools.strategy_execution import animation_document, execute_strategy, run
from workbench_tools.strategy_records import (
    STRATEGY_CONTRACT,
    UntilSpec,
    decode_strategy,
    materialize_configuration,
)

FIXTURES = Path(__file__).parent / "fixtures"


def _animation(
    squares: list[list[float]],
    *,
    side: float = 2.0,
    feasible: bool | None = True,
) -> dict[str, Any]:
    frame: dict[str, object] = {"t": 0.0, "side": side, "squares": squares}
    if feasible is not None:
        frame["feasible"] = feasible
    return {
        "contract": ANIMATION_CONTRACT,
        "name": "fixture",
        "n": len(squares),
        "frames": [frame],
    }


def _trajectory(value: object) -> PackingTrajectory:
    return trajectory_from_animation(decode_animation(value))


def test_geometry_check_fails_closed_for_count_finite_pairs_and_walls() -> None:
    valid = ((0.5, 0.5, 0.0), (1.5, 0.5, 0.0))
    assert check_unit_square_packing(valid, side=2.0, expected_count=2).passed
    cases = (
        (valid[:1], GeometryIssue.COUNT),
        (((math.nan, 0.5, 0.0), (1.5, 0.5, 0.0)), GeometryIssue.NONFINITE),
        (((0.5, 0.5, 0.0), (0.5, 0.5, 0.0)), GeometryIssue.PAIR_OVERLAP),
        (((0.4, 0.5, 0.0), (1.5, 0.5, 0.0)), GeometryIssue.WALL_ESCAPE),
    )
    for poses, issue in cases:
        check = check_unit_square_packing(poses, side=2.0, expected_count=2)
        assert check.passed is False
        assert issue in check.issues


@pytest.mark.parametrize(
    ("poses", "side", "issue"),
    [
        ([[0.5, 0.5, False]], 1.0, GeometryIssue.SHAPE),
        ([[10**1000, 0.5, 0.0]], 1.0, GeometryIssue.SHAPE),
        ([[0.5, 0.5, 0.0]], 10**1000, GeometryIssue.NONFINITE),
    ],
)
def test_geometry_check_rejects_boolean_and_overflow_boundaries(
    poses: list[list[object]], side: object, issue: GeometryIssue
) -> None:
    check = check_unit_square_packing(poses, side=side, expected_count=1)
    assert check.passed is False
    assert issue in check.issues


@pytest.mark.parametrize(
    ("expected_count", "tolerance"),
    [(1.5, 1e-9), (True, 1e-9), (1, "1e-9"), (1, 10**1000)],
)
def test_geometry_check_rejects_invalid_checker_contracts(
    expected_count: object, tolerance: object
) -> None:
    with pytest.raises(PackingContractError):
        check_unit_square_packing(
            [[0.5, 0.5, 0.0]],
            side=1.0,
            expected_count=expected_count,  # type: ignore[arg-type]
            tolerance=tolerance,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize(
    ("squares", "side", "issue"),
    [
        ([[0.5, 0.5, 0.0], [0.5, 0.5, 0.0]], 1.0, "overlap"),
        ([[0.4, 0.5, 0.0]], 1.0, "container"),
    ],
)
def test_animation_import_retains_the_actual_failed_check(
    squares: list[list[float]], side: float, issue: str
) -> None:
    trajectory = _trajectory(_animation(squares, side=side))
    frame = trajectory.frames[0]
    assert frame.evidence is EvidenceTier.CANDIDATE
    assert frame.check is not None
    assert frame.check.passed is False
    assert issue in frame.check.detail


def test_animation_import_does_not_promote_an_omitted_feasibility_claim() -> None:
    trajectory = _trajectory(_animation([[0.5, 0.5, 0.0]], side=1.0, feasible=None))
    frame = trajectory.frames[0]
    assert frame.evidence is EvidenceTier.CANDIDATE
    assert frame.check is not None
    assert frame.check.passed


def test_animation_muting_rechecks_geometry_instead_of_trusting_feasible() -> None:
    document = _animation([[0.5, 0.5, 0.0], [0.5, 0.5, 0.0]], side=1.0, feasible=True)
    assert muting_from_animation(decode_animation(document)) == ((True, True),)


def test_typed_animation_cannot_forge_a_geometry_receipt() -> None:
    document = decode_animation(
        _animation([[0.5, 0.5, 0.0], [0.5, 0.5, 0.0]], side=1.0, feasible=True)
    )
    frame = document.frames[0]
    forged = replace(
        document,
        frames=(replace(frame, geometry=replace(frame.geometry, issues=())),),
    )
    assert muting_from_animation(forged) == ((True, True),)


def test_shared_animation_v1_preserves_checked_fields_and_guidance_ancestry() -> None:
    raw = json.loads((FIXTURES / "packing-animation-v1.json").read_text(encoding="utf-8"))
    document = decode_animation(raw)
    assert document.palette is not None
    assert (document.palette.hue, document.palette.shade) == ("identity", "evidence")
    assert document.reference is not None
    assert document.reference.best_known == 2.0
    assert document.frames[0].square_ids == (2, 1)
    assert [document.frame_is_guided(frame) for frame in document.frames] == [
        False,
        True,
        True,
    ]
    assert document.frames[1].feasible is True
    assert document.frames[1].geometry.passed is False
    assert muting_from_animation(document)[1] == (True, True)

    encoded = animation_to_row(document)
    encoded_frames = encoded["frames"]
    assert isinstance(encoded_frames, list)
    assert [frame["guided"] for frame in encoded_frames] == [False, True, True]
    assert decode_animation(encoded).fair_reach == document.fair_reach


def test_animation_version_is_explicit_with_a_named_legacy_adapter() -> None:
    legacy = _animation([[0.5, 0.5, 0.0]], side=1.0)
    legacy.pop("contract")
    with pytest.raises(jsonschema.ValidationError, match="contract"):
        decode_animation(legacy)
    assert decode_legacy_animation(legacy).contract == ANIMATION_CONTRACT


@pytest.mark.parametrize("configuration", [{"x": math.nan}, {"x": (1, 2)}])
def test_animation_source_configuration_is_finite_json(configuration: object) -> None:
    raw = _animation([[0.5, 0.5, 0.0]], side=1.0)
    raw["source"] = {"configuration": configuration}
    with pytest.raises((TypeError, ValueError), match=r"source configuration|finite"):
        decode_animation(raw)


def test_animation_allows_an_explicit_empty_display_label() -> None:
    raw = _animation([[0.5, 0.5, 0.0]], side=1.0)
    raw["frames"][0]["label"] = ""
    assert decode_animation(raw).frames[0].label == ""


def test_svg_description_uses_checked_geometry_and_prefix_guidance() -> None:
    raw = json.loads((FIXTURES / "packing-animation-v1.json").read_text(encoding="utf-8"))
    document = decode_animation(raw)
    description = describe_animation(document)
    assert "guided onto a known packing" in description
    assert "1 of 3 frames are not valid packings" in description
    assert document.palette is not None
    svg = export_svg(
        replace(document, palette=replace(document.palette, shade="full-side-contact")),
        width=320,
    )
    assert "guided onto a known packing" in svg


@pytest.mark.parametrize(
    "palette",
    [
        {"hue": "uniform", "shade": "full-side-contact"},
        {"hue": "identity", "shade": "none"},
        {"hue": "identity", "shade": "evidence"},
    ],
)
def test_svg_export_rejects_admitted_palette_modes_it_cannot_render(
    palette: dict[str, str],
) -> None:
    raw = _animation([[0.5, 0.5, 0.0]], side=1.0)
    raw["palette"] = palette
    with pytest.raises(ValueError, match=r"SVG renderer does not support"):
        export_svg(decode_animation(raw))


@pytest.mark.parametrize(
    "ancestry",
    [
        {"guided": True},
        {"source": {"records": [1]}},
    ],
)
def test_animation_guidance_ancestry_cannot_be_erased_by_a_frame(
    ancestry: dict[str, object],
) -> None:
    document = _animation([[0.5, 0.5, 0.0]], side=1.0, feasible=True)
    document.update(ancestry)
    document["frames"][0]["guided"] = False
    assert "guided" in _trajectory(document).frames[0].label


@pytest.mark.parametrize(
    "document",
    [
        {
            "contract": ANIMATION_CONTRACT,
            "name": "wrong-count",
            "n": 2,
            "frames": [{"t": 0, "side": 2, "squares": [[0.5, 0.5, 0]]}],
        },
        {
            "contract": ANIMATION_CONTRACT,
            "name": "nonfinite",
            "n": 1,
            "frames": [{"t": 0, "side": 1, "squares": [[math.nan, 0.5, 0]]}],
        },
        {
            "contract": ANIMATION_CONTRACT,
            "name": "backwards",
            "n": 1,
            "frames": [
                {"t": 1, "side": 1, "squares": [[0.5, 0.5, 0]]},
                {"t": 0, "side": 1, "squares": [[0.5, 0.5, 0]]},
            ],
        },
    ],
)
def test_animation_import_rejects_malformed_or_unstable_frames(
    document: dict[str, object],
) -> None:
    with pytest.raises(ValueError, match=r"(square count|finite|non-decreasing)"):
        _trajectory(document)


def test_animation_record_reference_cannot_replace_unrelated_geometry() -> None:
    document = _animation([[0.6, 0.5, 0.0]], side=1.0)
    document["frames"][0]["record"] = 1
    with pytest.raises(ValueError, match="record reference"):
        _trajectory(document)


def test_animation_record_reference_rejects_a_different_valid_packing() -> None:
    document = _animation([[0.5, 0.5, 0.0], [0.5, 1.5, 0.0]], side=2.0)
    document["frames"][0]["record"] = 2
    with pytest.raises(ValueError, match="record reference poses"):
        _trajectory(document)


def test_animation_record_reference_is_checked_before_canonical_substitution() -> None:
    document = _animation([[0.5, 0.5, 0.0]], side=1.0)
    document["frames"][0]["record"] = 1
    frame = _trajectory(document).frames[0]
    assert len(frame.squares) == 1
    assert frame.check is not None
    assert frame.check.passed


def test_ascent_record_reference_carries_checked_record_geometry() -> None:
    document = render_ascent(1, 3, fair_steps=3)
    trajectory = trajectory_from_animation(document)
    assert trajectory.frames[-1].evidence is not EvidenceTier.CANDIDATE


def test_strategy_version_and_checked_result_are_explicit() -> None:
    strategy = decode_strategy(
        {
            "contract": STRATEGY_CONTRACT,
            "name": "invalid-container",
            "n": 2,
            "seed": 9,
            "phases": [
                {
                    "mechanism": "container",
                    "side": {"relative_to": "current", "factor": 0.5},
                    "until": {"frames": 1},
                }
            ],
        }
    )
    result = execute_strategy(strategy)
    assert result.configuration.seed == 9
    assert result.geometry.passed is False
    assert GeometryIssue.PAIR_OVERLAP in result.geometry.issues
    assert result.phases[-1].geometry == result.geometry


def test_typed_strategy_cannot_bypass_capability_or_seed_validation() -> None:
    strategy = decode_strategy(
        {
            "contract": STRATEGY_CONTRACT,
            "name": "typed-bypass",
            "n": 1,
            "phases": [{"mechanism": "project", "until": {"steps": 1}}],
        }
    )
    phase = replace(strategy.phases[0], until=UntilSpec(feasible=True, steps=1))
    with pytest.raises(ValueError, match=r"until\.feasible"):
        execute_strategy(replace(strategy, phases=(phase,)))
    with pytest.raises(ValueError, match="seed"):
        materialize_configuration(strategy, seed=True)  # type: ignore[arg-type]


def test_grid_refuses_a_side_that_cannot_hold_the_requested_count() -> None:
    strategy = {
        "name": "small-grid",
        "n": 5,
        "seed": 1,
        "phases": [
            {
                "mechanism": "grid",
                "side": {"relative_to": "grid", "factor": 2 / 3},
            }
        ],
    }
    with pytest.raises(ValueError, match="grid side"):
        run(strategy)


@pytest.mark.parametrize("source", ["given", "random"])
def test_strategy_rejects_admitted_but_unimplemented_structure_sources(source: str) -> None:
    strategy = {
        "name": "unsupported-source",
        "n": 1,
        "seed": 1,
        "phases": [
            {
                "mechanism": "project",
                "structure": {"rung": "partition", "source": source},
                "until": {"steps": 1},
            }
        ],
    }
    with pytest.raises(ValueError, match=f"structure source {source!r}"):
        run(strategy)


def test_strategy_rejects_fields_the_selected_mechanism_does_not_execute() -> None:
    strategy = {
        "name": "ignored-target",
        "n": 1,
        "seed": 1,
        "phases": [
            {"mechanism": "grid", "target": {"source": "record", "steps": 1, "pull": 1.0}}
        ],
    }
    with pytest.raises(ValueError, match=r"grid.*target"):
        run(strategy)


@pytest.mark.parametrize(
    ("phase", "message"),
    [
        (
            {"mechanism": "project", "until": {"feasible": True}},
            "until.feasible",
        ),
        (
            {"mechanism": "ratchet", "schedule": {"start": 2.0}},
            "schedule.start",
        ),
        (
            {"mechanism": "ratchet", "schedule": {"halve_on_failure": False}},
            "halve_on_failure=false",
        ),
        (
            {"mechanism": "relax", "constraints": {"weight": 2.0}},
            "relax does not support phase field",
        ),
        (
            {"mechanism": "assemble"},
            "assemble requires record contact-graph-with-types",
        ),
    ],
)
def test_strategy_rejects_declared_options_it_cannot_honor(
    phase: dict[str, object], message: str
) -> None:
    strategy = {"name": "unsupported", "n": 1, "seed": 1, "phases": [phase]}
    with pytest.raises(ValueError, match=message):
        run(strategy)


def test_explicit_seed_replays_the_same_scatter() -> None:
    strategy = {
        "name": "repeatable",
        "n": 2,
        "seed": 42,
        "phases": [
            {
                "mechanism": "scatter",
                "side": {"relative_to": "grid", "factor": 1.5},
            }
        ],
    }
    first = run(strategy)
    second = run(strategy)
    np.testing.assert_array_equal(first.poses, second.poses)


@pytest.mark.parametrize(
    "start",
    [np.array([[0.5, 0.5, 0.0]]), np.array([[math.nan, 0.5, 0.0], [1.5, 0.5, 0.0]])],
)
def test_strategy_rejects_wrong_count_or_nonfinite_supplied_starts(start: np.ndarray) -> None:
    strategy = {"name": "start", "n": 2, "seed": 1, "phases": [{"mechanism": "grid"}]}
    with pytest.raises(ValueError, match="start"):
        run(strategy, start=start, start_side=2.0)


def test_container_trace_keeps_each_intermediate_side() -> None:
    strategy = {
        "name": "open",
        "n": 1,
        "seed": 1,
        "phases": [
            {
                "mechanism": "container",
                "side": {"relative_to": "current", "factor": 2.0},
                "until": {"frames": 2},
            }
        ],
    }
    state = run(strategy, keep_trace=True)
    assert [frame.side for frame in state.animation] == [1.5, 2.0]


def test_generated_seed_and_effective_configuration_survive_export() -> None:
    strategy = {
        "name": "generated-seed",
        "n": 1,
        "phases": [{"mechanism": "project", "until": {"steps": 1}}],
    }
    state = run(strategy, seed_source=lambda: 123_456)
    document = animation_document(strategy, state)
    assert state.seed == 123_456
    assert document.source is not None
    assert document.source.seed == 123_456
    assert state.configuration.seed == 123_456
    phase = state.configuration.phases[0]
    assert phase.relaxation == 0.1
    assert phase.until is not None
    assert (phase.until.steps, phase.until.stalled_for) == (1, 1)
    assert phase.constraints is not None
    assert (phase.constraints.band, phase.constraints.weight) == (0.02, 1.0)


def test_guidance_ancestry_survives_later_phases() -> None:
    strategy = {
        "name": "guided-then-open",
        "n": 1,
        "seed": 1,
        "phases": [
            {"mechanism": "guide", "target": {"source": "record", "steps": 1, "pull": 1.0}},
            {
                "mechanism": "container",
                "side": {"relative_to": "current", "factor": 2.0},
                "until": {"frames": 1},
            },
        ],
    }
    state = run(strategy, keep_trace=True)
    assert state.animation
    assert all(frame.guided for frame in state.animation)
