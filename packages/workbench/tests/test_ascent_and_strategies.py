"""Controls for the atlas ascent, the strategy report and the strategy documents.

The owner's rule these hold to: an unchecked arrangement is never presented as a packing.
"""

from __future__ import annotations

import json
import sys
from collections.abc import Callable
from dataclasses import dataclass
from itertools import groupby
from pathlib import Path
from typing import Any, cast

import jsonschema
import numpy as np
import pytest

from devtools.lock_order import lock_order
from devtools.validate_schemas import check as check_enforced_document
from sqpack.project import configured_project_root
from sqpack.render.model import EvidenceTier
from sqpack.yamlio import safe_load
from workbench_tools import ascent, strategy_execution
from workbench_tools.animation_records import (
    ANIMATION_CONTRACT,
    AnimationDocument,
    animation_to_row,
    decode_animation,
)
from workbench_tools.animation_render import trajectory_from_animation
from workbench_tools.packing_contracts import GeometryIssue
from workbench_tools.strategy_execution import State
from workbench_tools.strategy_records import (
    STRATEGY_CONTRACT,
    StrategyPhaseReceipt,
    load_strategy,
    strategy_to_row,
)

STRATEGIES = configured_project_root() / "strategies"
STRATEGY_DOCUMENTS = ("assemble-then-tighten.yaml", "sweep-landing.yaml")
ENFORCED_DOCUMENTS = (*STRATEGY_DOCUMENTS, "lab-components.yaml")


@dataclass(frozen=True, slots=True)
class RenderedAscent:
    document: AnimationDocument
    states: tuple[State, ...]


@pytest.fixture(scope="module")
def small_ascent() -> RenderedAscent:
    """The ascent from one square to three with a one-iteration settle.

    It is the smallest range with padded frames: every frame of the n = 2 step carries a
    waiting third square. The n = 2 step also starts with its arriving square on top of
    the first, and one iteration cannot separate them, so its settle is not a packing.
    """
    states: list[State] = []
    real_run = ascent.run

    def recording_run(*args: Any, **kwargs: Any) -> State:
        state = real_run(*args, **kwargs)
        states.append(state)
        return state

    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(ascent, "run", recording_run)
        document = ascent.render_ascent(1, 3, fair_steps=1)
    return RenderedAscent(document=document, states=tuple(states))


def _padded_frame_count(rendered: RenderedAscent) -> int:
    """Frames from every step below the last: its executed frames and its record frame."""
    last = rendered.document.n
    return sum(len(state.animation) + 1 for state in rendered.states if state.n < last)


def _settle(state: State) -> StrategyPhaseReceipt:
    return next(receipt for receipt in reversed(state.phases) if receipt.mechanism == "project")


# D15: padded frames


def test_ascent_frames_are_the_executed_frames_and_one_record_frame_per_step(
    small_ascent: RenderedAscent,
) -> None:
    expected = sum(len(state.animation) + 1 for state in small_ascent.states)
    assert [state.n for state in small_ascent.states] == [2, 3]
    assert len(small_ascent.document.frames) == expected


def test_padded_ascent_frames_are_never_feasible(small_ascent: RenderedAscent) -> None:
    padded = _padded_frame_count(small_ascent)
    assert padded > 0
    flags = [frame.feasible for frame in small_ascent.document.frames[:padded]]
    assert flags == [False] * padded


def test_padded_ascent_frames_do_not_export_as_numerically_checked(
    small_ascent: RenderedAscent,
) -> None:
    padded = _padded_frame_count(small_ascent)
    trajectory = trajectory_from_animation(small_ascent.document)
    evidence = [frame.evidence for frame in trajectory.frames[:padded]]
    assert EvidenceTier.NUMERICALLY_CHECKED not in evidence


# D53: no phase that holds one picture still


def test_no_ascent_phase_holds_one_picture_for_its_whole_length(
    small_ascent: RenderedAscent,
) -> None:
    # A guide may settle onto its last pose for a frame or two; a phase whose every frame
    # is the same picture showed nothing happening and then let the next phase jump.
    still: list[str] = []
    for phase, grouped in groupby(small_ascent.document.frames, key=lambda frame: frame.phase):
        run = list(grouped)
        first = run[0]
        if len(run) > 1 and all(
            (frame.side, frame.squares) == (first.side, first.squares) for frame in run
        ):
            still.append(phase)
    assert still == []


# D61: a side is reported only for a checked packing


def test_fair_reach_reports_a_side_only_for_a_settle_that_is_a_packing(
    small_ascent: RenderedAscent,
) -> None:
    settles = {state.n: _settle(state) for state in small_ascent.states}
    assert GeometryIssue.PAIR_OVERLAP in settles[2].geometry.issues
    reach = {item.n: item for item in small_ascent.document.fair_reach}
    assert reach.keys() == settles.keys()
    for n, settle in settles.items():
        item = reach[n]
        assert item.packing_valid is settle.geometry.passed
        if settle.geometry.passed:
            assert item.fair_side == settle.side
            assert item.excess_pct is not None
        else:
            assert item.fair_side is None
            assert item.excess_pct is None

    row = animation_to_row(small_ascent.document)
    stored = cast(list[dict[str, object]], row["fair_reach"])
    assert stored[0] == {
        "n": 2,
        "fair_side": None,
        "record": 2.0,
        "excess_pct": None,
        "packing_valid": False,
    }
    assert decode_animation(row).fair_reach == small_ascent.document.fair_reach


def _animation_with_reach(row: dict[str, object]) -> dict[str, object]:
    return {
        "contract": ANIMATION_CONTRACT,
        "name": "fair-reach-contract",
        "n": 1,
        "fair_reach": [row],
        "frames": [{"t": 0.0, "side": 1.0, "squares": [[0.5, 0.5, 0.0]]}],
    }


@pytest.mark.parametrize(
    "row",
    [
        {"n": 2, "fair_side": 2.0, "record": 2.0, "excess_pct": 0.0, "packing_valid": False},
        {"n": 2, "fair_side": None, "record": 2.0, "excess_pct": 0.0, "packing_valid": False},
        {"n": 2, "fair_side": None, "record": 2.0, "excess_pct": None, "packing_valid": True},
        {"n": 2, "fair_side": None, "record": 2.0, "excess_pct": None},
    ],
)
def test_fair_reach_refuses_a_side_beside_an_invalid_or_absent_packing(
    row: dict[str, object],
) -> None:
    with pytest.raises((jsonschema.ValidationError, TypeError, ValueError)):
        decode_animation(_animation_with_reach(row))


def test_fair_reach_without_a_recorded_validity_decodes_as_unchecked() -> None:
    row: dict[str, object] = {"n": 2, "fair_side": 2.0, "record": 2.0, "excess_pct": 0.0}
    (item,) = decode_animation(_animation_with_reach(row)).fair_reach
    assert item.packing_valid is None
    assert ascent.fair_reach_line(item).endswith("unchecked, not a packing")


def test_ascent_report_prints_no_side_for_a_settle_that_is_not_a_packing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    out = tmp_path / "nested" / "ascent.json"
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "squares-workbench-ascent",
            *("--from", "1", "--to", "3", "--fair-steps", "1"),
            *("--render", "--out", str(out)),
        ],
    )
    assert ascent.main() == 0
    printed = capsys.readouterr().out.splitlines()
    document = decode_animation(json.loads(out.read_text(encoding="utf-8")))
    assert [path.name for path in out.parent.iterdir()] == ["ascent.json"]
    rows = {int(line.split()[0]): line for line in printed if line.split()[0].isdigit()}
    assert rows.keys() == {item.n for item in document.fair_reach}
    for item in document.fair_reach:
        fields = rows[item.n].split()
        if item.packing_valid:
            assert float(fields[1]) == pytest.approx(item.fair_side, abs=1e-7)
        else:
            assert fields[1] == "-"
            assert rows[item.n].endswith("not a packing")
    assert rows[2].split()[1] == "-"


def _strategy_document(tmp_path: Path, *, factor: float) -> Path:
    path = tmp_path / "strategy.yaml"
    document = {
        "softschema": {
            "contract": STRATEGY_CONTRACT,
            "schema": "packing-strategy.schema.yaml",
            "envelope": "strategy",
            "status": "enforced",
        },
        "strategy": {
            "contract": STRATEGY_CONTRACT,
            "name": "container-report",
            "n": 2,
            "seed": 9,
            "phases": [
                {
                    "mechanism": "container",
                    "side": {"relative_to": "current", "factor": factor},
                    "until": {"frames": 1},
                }
            ],
        },
    }
    path.write_text(json.dumps(document), encoding="utf-8")
    return path


def _strategy_report(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    *arguments: str,
) -> str:
    monkeypatch.setattr(sys, "argv", ["squares-workbench-strategy", *arguments])
    assert strategy_execution.main() == 0
    return capsys.readouterr().out


def test_strategy_report_labels_an_overlapping_result_not_a_packing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    path = _strategy_document(tmp_path, factor=0.5)
    lines = _strategy_report(monkeypatch, capsys, str(path)).splitlines()
    assert not any("reached" in line for line in lines)
    assert lines[2].endswith("not a packing")
    assert lines[-1] == "best known 2.0000000; final side 1.0000000 is not a packing"
    payload = json.loads(_strategy_report(monkeypatch, capsys, str(path), "--json"))
    assert payload["packing_valid"] is False
    assert payload["excess_pct"] is None


def test_strategy_report_states_the_reach_of_a_checked_packing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    path = _strategy_document(tmp_path, factor=1.0)
    lines = _strategy_report(monkeypatch, capsys, str(path)).splitlines()
    assert lines[2].endswith(" valid")
    assert lines[-1] == "best known 2.0000000, reached 2.0000000 (+0.000 %)"
    payload = json.loads(_strategy_report(monkeypatch, capsys, str(path), "--json"))
    assert payload["packing_valid"] is True
    assert payload["excess_pct"] == 0.0


# D52: the enforced strategy documents and lock_order


@pytest.mark.parametrize("name", ENFORCED_DOCUMENTS)
def test_enforced_strategy_documents_pass_the_soft_schema_check(name: str) -> None:
    assert check_enforced_document(STRATEGIES / name) == []


@pytest.mark.parametrize("name", STRATEGY_DOCUMENTS)
def test_enforced_strategy_documents_decode_without_losing_a_field(name: str) -> None:
    path = STRATEGIES / name
    declared = cast(dict[str, object], safe_load(path.read_text(encoding="utf-8")))
    assert strategy_to_row(load_strategy(path)) == declared["strategy"]


def _unknown_mechanism(document: dict[str, Any]) -> None:
    document["strategy"]["phases"][0]["mechanism"] = "teleport"


def _zero_guide_steps(document: dict[str, Any]) -> None:
    document["strategy"]["phases"][1]["target"]["steps"] = 0


def _unknown_environment(document: dict[str, Any]) -> None:
    document["components"]["parts"][0]["environment"] = "anywhere"


@pytest.mark.parametrize(
    ("name", "mutate"),
    [
        ("assemble-then-tighten.yaml", _unknown_mechanism),
        ("sweep-landing.yaml", _zero_guide_steps),
        ("lab-components.yaml", _unknown_environment),
    ],
)
def test_a_mutated_strategy_document_fails_the_soft_schema_check(
    tmp_path: Path, name: str, mutate: Callable[[dict[str, Any]], None]
) -> None:
    source = STRATEGIES / name
    document = cast(dict[str, Any], safe_load(source.read_text(encoding="utf-8")))
    metadata = document["softschema"]
    metadata["schema"] = str((source.parent / metadata["schema"]).resolve())
    mutate(document)
    mutated = tmp_path / name
    mutated.write_text(json.dumps(document), encoding="utf-8")
    assert check_enforced_document(mutated) != []
    if name in STRATEGY_DOCUMENTS:
        with pytest.raises((jsonschema.ValidationError, TypeError, ValueError)):
            load_strategy(mutated)


def test_lock_order_locks_square_squares_outside_in_before_any_tilted_square() -> None:
    poses = np.array(
        [
            [0.8, 0.8, 0.3],  # tilted, 0.3 from a wall
            [2.0, 2.0, 0.0],  # square to the walls, 1.5 from one
            [1.5, 0.5, np.pi / 2],  # a quarter turn is square to the walls; on the floor
            [0.5, 2.0, 0.0],  # square to the walls, against the left wall
            [2.0, 3.1, 0.4],  # tilted, 0.4 from a wall
        ]
    )
    # Equal wall distances fall back to x, then y: index 3 (x = 0.5) before 2 (x = 1.5).
    assert lock_order(poses, 4.0) == [3, 2, 1, 0, 4]
