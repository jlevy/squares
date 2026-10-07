"""The n17 capture pilot: its cap, its seed, the endpoint control and certified steps."""

from __future__ import annotations

import gzip
import json
import math
import time
from pathlib import Path
from typing import Any

import pytest

from devtools import pilot_n17_capture as pilot
from devtools.provenance import git_blob
from sqpack.hull_kernel import Budget, RefusalError, node, sequential
from sqpack.hull_kernel.frame import Frame
from sqpack.hull_kernel.geometry import area2, trig
from sqpack.hull_kernel.induction import strict_core
from sqpack.hull_kernel.rational import Q

EXCLUSION_CAP = Q(1169, 250)


def test_memory_guard_uses_current_bytes_and_reports_peak_separately(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    samples = iter((1024, 2049))
    monkeypatch.setattr(pilot, "current_memory_bytes", lambda: next(samples))
    monkeypatch.setattr(pilot, "peak_memory_bytes", lambda: 10**9)
    guard = pilot.MemoryGuard(2048)
    assert guard.check("safe")
    assert not guard.check("over")
    assert guard.stop is not None
    assert guard.stop["outcome"] == "memory_cap"
    assert guard.stop["current_rss_bytes"] == 2049
    assert guard.stop["lifetime_peak_rss_bytes"] == 10**9


def test_missing_current_memory_stops_without_peak_fallback(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def unavailable() -> int:
        raise OSError("sampler unavailable")

    monkeypatch.setattr(pilot, "current_memory_bytes", unavailable)
    monkeypatch.setattr(pilot, "peak_memory_bytes", lambda: 1)
    guard = pilot.MemoryGuard(2048)
    assert not guard.check("native_failure")
    assert guard.stop is not None
    assert guard.stop["outcome"] == "memory_unavailable"
    assert guard.stop["current_rss_bytes"] is None


def test_early_memory_stop_retains_incomplete_receipt_and_checks_no_sources(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setattr(pilot, "current_memory_bytes", lambda: 2 * 1024**2)
    monkeypatch.setattr(pilot, "peak_memory_bytes", lambda: 3 * 1024**2)

    def forbidden(*_args: Any, **_kwargs: Any) -> Frame:
        raise AssertionError("guard must stop before loading sources")

    monkeypatch.setattr(pilot, "n11_frame", forbidden)
    partial = tmp_path / "partial.json"
    result = pilot.run(
        system="n11",
        cap="capture",
        bins=4,
        max_rounds=1,
        max_live=8,
        min_width=Q(1, 64),
        hull_limit=16,
        max_seconds=10,
        replay_share=0,
        save_objects=None,
        max_memory_mib=1,
        partial=partial,
    )
    assert result["status"] == "INCOMPLETE_MEMORY_CAP"
    assert result["endpoint_control"] == {"held": None, "checked_after": 0}
    assert result["rounds"] == []
    assert json.loads(partial.read_text())["memory"] == result["memory"]


def test_memory_stop_after_checked_update_keeps_partial_state_without_resumable_round(
    endpoint: pilot.Endpoint,
    frame: Frame,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    readings = iter([1] * 5 + [2049])
    monkeypatch.setattr(pilot, "current_memory_bytes", lambda: next(readings))
    monkeypatch.setattr(pilot, "peak_memory_bytes", lambda: 10**9)
    partial = tmp_path / "partial.json"
    guard = pilot.MemoryGuard(2048)
    result = pilot.run_pilot(
        frame,
        endpoint,
        bins=4,
        max_rounds=2,
        max_live=8,
        min_width=Q(1, 64),
        hull_limit=16,
        max_seconds=120,
        progress=False,
        partial=partial,
        checkpoints=tmp_path,
        memory_guard=guard,
    )
    assert result.outcome == "memory_cap"
    assert result.endpoint_lost is None
    assert len(result.updates) == len(result.node["steps"]) == 1
    assert result.rounds[-1]["complete"] is False
    assert guard.stop is not None
    assert guard.stop["boundary"] == "after_certified_update"
    retained = json.loads(partial.read_text())
    assert retained["outcome"] == "memory_cap"
    assert retained["endpoint_control"]["held"] is True
    checkpoint = tmp_path / "checkpoint-memory-stop.json.gz"
    stopped = json.loads(gzip.decompress(checkpoint.read_bytes()))
    assert stopped["resumable"] is False
    assert len(stopped["node"]["steps"]) == 1
    with pytest.raises(RefusalError, match="not a pilot checkpoint"):
        pilot.load_checkpoint(checkpoint, {})
    replayed = pilot.replay(frame, result, max_seconds=120)
    assert replayed["status"] == "PASS_REPLAYED"
    assert replayed["final_state_agrees"]


def test_no_memory_flag_never_calls_memory_sampler(
    endpoint: pilot.Endpoint,
    frame: Frame,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def forbidden() -> int:
        raise AssertionError("unrequested memory sampler")

    monkeypatch.setattr(pilot, "current_memory_bytes", forbidden)
    monkeypatch.setattr(pilot, "peak_memory_bytes", forbidden)
    result = pilot.run_pilot(
        frame,
        endpoint,
        bins=4,
        max_rounds=1,
        max_live=8,
        min_width=Q(1, 64),
        hull_limit=16,
        max_seconds=120,
        max_steps=0,
        progress=False,
    )
    assert result.outcome == "step_cap"
    assert result.memory is None


@pytest.fixture(scope="module")
def endpoint() -> pilot.Endpoint:
    return pilot.load_endpoint(pilot.capture_frame(None))


@pytest.fixture(scope="module")
def frame(endpoint: pilot.Endpoint) -> Frame:
    return pilot.capture_frame(endpoint.capture_cap)


@pytest.fixture(scope="module")
def seed_rows(frame: Frame, endpoint: pilot.Endpoint) -> dict[int, list[dict[str, Any]]]:
    mask = sorted(endpoint.by_owner())
    budget = Budget(time.monotonic() + 60, pilot.MAX_EVENTS)
    seed = pilot.build_seed(frame, mask, bins=4, seed_grid=0, budget=budget)
    admitted = node.admit_seed(
        frame, seed, mask=mask, bins=4, budget=budget, allow_empty_groups=True
    )
    return admitted.rows


def target(endpoint: pilot.Endpoint, label: int) -> pilot.Target:
    return next(item for item in endpoint.targets if item.label == label)


def test_the_capture_cap_is_the_root_box_enclosure_of_s_star(endpoint: pilot.Endpoint) -> None:
    side = endpoint.side
    assert side.hi - side.lo < Q(1, 10**20)
    assert 0 < endpoint.capture_cap - side.hi <= Q(1, 10**12)
    assert endpoint.capture_cap.denominator <= 10**12
    assert abs(float(side.lo) - 4.675530093604551) < 1e-12
    assert EXCLUSION_CAP - endpoint.capture_cap > Q(4, 10**4)


def test_the_owners_are_the_endpoint_state(endpoint: pilot.Endpoint) -> None:
    cells = {item.label: item.cell for item in endpoint.targets}
    assert cells[6] == "side-S2"
    assert cells[13] == "side-S1"
    assert cells[5] == "corner-SE"
    assert cells[11] == "interior-W"
    assert len({item.owner for item in endpoint.targets}) == 17
    assert abs(target(endpoint, 9).turn - 2 * math.atan(0.3620438933)) < 1e-9
    assert abs(target(endpoint, 16).turn - (math.pi / 2 - 2 * math.atan(0.3309486747))) < 1e-9
    assert target(endpoint, 1).charts == ((Q(0), Q(0)), (Q(1), Q(1)))
    assert target(endpoint, 12).charts[0][0] < target(endpoint, 12).charts[0][1]


def test_frame_a_puts_the_endpoint_just_inside_the_centred_walls(
    endpoint: pilot.Endpoint, frame: Frame
) -> None:
    assert frame.inner_cap == endpoint.capture_cap
    assert frame.cap == EXCLUSION_CAP
    low, high = frame.centre_bounds(Q(1, 2))
    corner = target(endpoint, 1).centre
    far = target(endpoint, 8).centre
    assert low < corner[0].lo
    assert low < corner[1].lo
    assert far[0].hi < high
    assert far[1].hi < high
    assert corner[0].lo - low <= Q(1, 10**12)
    assert high - far[0].hi <= Q(1, 10**12)
    loose = pilot.capture_frame(None)
    assert loose.inner_cap == EXCLUSION_CAP
    assert loose.centre_bounds(Q(1, 2)) == (Q(1, 2), EXCLUSION_CAP - Q(1, 2))


def test_the_seed_holds_the_endpoint_and_a_lost_row_is_seen(
    endpoint: pilot.Endpoint, seed_rows: dict[int, list[dict[str, Any]]]
) -> None:
    for item in endpoint.targets:
        assert pilot.endpoint_holds(item, seed_rows[item.owner]) is not None, item.label
    tilted = target(endpoint, 9)
    rows = [dict(row) for row in seed_rows[tilted.owner]]
    held = pilot.endpoint_holds(tilted, rows)
    assert held is not None
    rows[held["row"]]["residual_polygons"] = []
    assert pilot.endpoint_holds(tilted, rows) is None
    corner = target(endpoint, 1)
    rows = [dict(row) for row in seed_rows[corner.owner]]
    rows[0]["residual_polygons"] = []
    assert pilot.endpoint_holds(corner, rows) is not None, "t = 1 is the same pose"
    rows[-1]["residual_polygons"] = []
    assert pilot.endpoint_holds(corner, rows) is None


def test_refinement_bisects_the_widest_live_rows_and_the_checker_admits_it() -> None:
    piece = [["1", "1"], ["2", "1"], ["2", "2"]]
    rows: list[dict[str, Any]] = [
        {"interval": ["0", "1/2"], "residual_polygons": [piece], "reference": {"row": 0}},
        {"interval": ["1/2", "3/4"], "residual_polygons": [], "reference": {"row": 1}},
        {"interval": ["3/4", "1"], "residual_polygons": [piece], "reference": {"row": 2}},
    ]
    children, splits = pilot.refine(rows, max_live=3, min_width=Q(1, 64))
    assert splits == 1
    assert [(lo, hi) for lo, hi, _ in children] == [
        (Q(0), Q(1, 4)),
        (Q(1, 4), Q(1, 2)),
        (Q(1, 2), Q(3, 4)),
        (Q(3, 4), Q(1)),
    ]
    proposed = [
        {"interval": [str(lo), str(hi)], "prior_reference": parent["reference"]}
        for lo, hi, parent in children
    ]
    predecessors = sequential.complete_refinement(proposed, rows, max_rows=10)
    assert [item["reference"]["row"] for item in predecessors] == [0, 0, 1, 2]
    assert pilot.refine(rows, max_live=2, min_width=Q(1, 64))[1] == 0
    assert pilot.refine(rows, max_live=8, min_width=Q(1, 2))[1] == 0
    assert pilot.refine(rows, max_live=8, min_width=Q(1, 8))[1] == 2


def test_two_certified_steps_keep_the_endpoint_and_replay_agrees(
    endpoint: pilot.Endpoint, frame: Frame, tmp_path: Path
) -> None:
    partial = tmp_path / "run.partial.json"
    result = pilot.run_pilot(
        frame,
        endpoint,
        bins=4,
        max_rounds=1,
        max_live=8,
        min_width=Q(1, 64),
        hull_limit=16,
        max_seconds=120,
        max_steps=2,
        progress=False,
        partial=partial,
    )
    assert result.endpoint_lost is None
    assert result.outcome == "step_cap"
    assert [update["cell"] for update in result.updates] == ["corner-SW", "corner-SE"]
    assert result.updates[0]["splits"] == 4
    assert result.updates[0]["rows"] == 8
    assert result.rounds[0]["round"] == 0
    assert result.rounds[-1]["complete"] is False
    replayed = pilot.replay(frame, result, max_seconds=120)
    assert replayed["status"] == "PASS_REPLAYED"
    assert replayed["steps"] == 2
    assert replayed["final_state_agrees"] is True
    assert replayed["closure"] is None
    written = json.loads(partial.read_text())
    assert written["provenance"] == pilot.PROVENANCE
    assert [entry["round"] for entry in written["rounds"]] == [0, 1]
    assert len(written["updates"]) == 2


def test_a_per_owner_cap_refines_only_the_owners_it_allows(
    endpoint: pilot.Endpoint, frame: Frame
) -> None:
    """`max_live_for` holds a named owner at its own live-row cap while the others refine
    to `max_live`; the steps are certified as before."""
    result = pilot.run_pilot(
        frame,
        endpoint,
        bins=4,
        max_rounds=1,
        max_live=8,
        max_live_for={"corner-SW": 4},
        min_width=Q(1, 64),
        hull_limit=16,
        max_seconds=120,
        max_steps=2,
        progress=False,
    )
    assert result.endpoint_lost is None
    splits = {update["cell"]: (update["splits"], update["rows"]) for update in result.updates}
    assert splits == {"corner-SW": (0, 4), "corner-SE": (4, 8)}
    with pytest.raises(RefusalError, match="names no owner"):
        pilot.run_pilot(
            frame,
            endpoint,
            bins=4,
            max_rounds=1,
            max_live=8,
            max_live_for={"nowhere": 4},
            min_width=Q(1, 64),
            hull_limit=16,
            max_seconds=120,
            max_steps=1,
            progress=False,
        )


def test_per_owner_caps_parse_from_the_command_line() -> None:
    assert pilot.parse_caps(["side-N2=576", "side-W2=400"]) == {"side-N2": 576, "side-W2": 400}
    assert pilot.parse_caps([]) == {}
    for bad in (["side-N2"], ["side-N2=x"], ["side-N2=-1"], ["side-N2=4", "side-N2=8"]):
        with pytest.raises(RefusalError):
            pilot.parse_caps(bad)


def test_turns_are_read_modulo_a_quarter_turn() -> None:
    assert pilot.turn_deviation(0.0, 0.0) == 0
    assert pilot.turn_deviation(1.0, 0.0) < 1e-15
    assert pilot.row_turn_deviation(0.9, 1.0, 0.0) == pytest.approx(
        math.pi / 2 - 2 * math.atan(0.9)
    )
    assert pilot.row_turn_deviation(0.3, 0.5, 0.0) == pytest.approx(math.pi / 4)
    star = 2 * math.atan(0.362)
    assert pilot.row_turn_deviation(0.36, 0.364, star) == pytest.approx(
        max(2 * math.atan(0.364) - star, star - 2 * math.atan(0.36))
    )


def test_target_coordinates_name_the_sliders(endpoint: pilot.Endpoint) -> None:
    assert pilot.coordinates(5, (-0.1, 0.002), endpoint) == {"y": 0.002, "a": 0.1}
    ux, uy = endpoint.u
    vx, vy = endpoint.v
    eleven = pilot.coordinates(11, (0.01 * ux - 0.05 * vx, 0.01 * uy - 0.05 * vy), endpoint)
    assert eleven["u"] == pytest.approx(0.01)
    assert eleven["b"] == pytest.approx(0.05)
    thirteen = pilot.coordinates(13, (0.03 * vx, 0.03 * vy), endpoint)
    assert thirteen["u"] == pytest.approx(0.0, abs=1e-15)
    assert thirteen["z"] == pytest.approx(0.03)
    assert pilot.coordinates(1, (0.1, -0.2), endpoint) == {"x": 0.1, "y": -0.2}


def test_contraction_and_scales_are_read_from_complete_rounds() -> None:
    worst = [0.1, 0.05, 0.025, 0.0125, 0.0001]
    rounds: list[dict[str, Any]] = [
        {
            "round": index,
            "worst": value,
            "worst_position": value,
            "worst_turn": value / 2,
            "complete": index < 4,
        }
        for index, value in enumerate(worst)
    ]
    reading = pilot.contraction(rounds)
    assert reading["ratios"]["worst"] == [0.5, 0.5, 0.5]
    assert reading["g_tail_geometric_mean"] == pytest.approx(0.5)
    assert reading["rounds_more_to_scale"]["0.01"] == pytest.approx(
        math.log(1.25) / math.log(2)
    )
    assert pilot.first_rounds(rounds) == {"0.01": 4, "0.001": 4, "0.0003": 4, "0.0002": 4}
    assert pilot.first_rounds(rounds[:4])["0.01"] is None


def test_the_verdict_refuses_a_lost_endpoint_and_a_contracted_control() -> None:
    passed = {"status": "PASS_REPLAYED"}
    assert (
        pilot.verdict("capture", endpoint_lost=True, replayed=None, worst_final=1.0)
        == "REFUSED_ENDPOINT_LOST"
    )
    assert (
        pilot.verdict("exclusion", endpoint_lost=False, replayed=passed, worst_final=1e-3)
        == "REFUSED_CONTROL_CONTRACTED"
    )
    assert (
        pilot.verdict("exclusion", endpoint_lost=False, replayed=None, worst_final=0.5)
        == "PASS_CONTROL_BLOB_HELD"
    )
    assert (
        pilot.verdict(
            "capture", endpoint_lost=False, replayed={"status": "INCOMPLETE"}, worst_final=1.0
        )
        == "INCOMPLETE_REPLAY"
    )
    assert (
        pilot.verdict("capture", endpoint_lost=False, replayed=None, worst_final=1e-5)
        == "PASS_PILOT_MEASURED"
    )


def test_the_box_sub_case_cuts_every_cell_but_six_around_the_endpoint(
    endpoint: pilot.Endpoint, frame: Frame
) -> None:
    rho = Q(1, 64)
    boxed, renumbered = pilot.box_frame(frame, endpoint, rho)
    assert boxed.inner_cap == endpoint.capture_cap
    assert [action.name for action in boxed.actions] == ["r0"]
    assert sorted(item.owner for item in renumbered.targets) == list(range(17))
    for item in renumbered.targets:
        cell = boxed.cell(item.owner)
        corners = [
            (Q(x), Q(y))
            for x in (item.centre[0].lo, item.centre[0].hi)
            for y in (item.centre[1].lo, item.centre[1].hi)
        ]
        assert all(pilot.in_convex(cell, corner) for corner in corners), item.label
        xs = [x for x, _ in cell]
        if item.label == 6:
            assert cell == frame.cell(target(endpoint, 6).owner)
        elif item.label == 5:
            assert max(xs) - min(xs) > Q(1, 4)
        elif item.label not in (11, 13):
            assert max(xs) - min(xs) <= 2 * rho


def test_the_octagon_core_is_strict_and_beats_the_envelope(frame: Frame) -> None:
    for lo, hi in ((Q(0), Q(1, 32)), (Q(11, 32), Q(3, 8)), (Q(31, 32), Q(1))):
        octagon = pilot.octagon_core(frame, lo, hi)
        envelope = pilot.producer.envelope_core(frame, lo, hi)
        strict_core(frame, octagon, lo, hi)
        assert len(octagon) == 8
        assert area2(octagon) > area2(envelope)
    lo, hi = Q(1, 3), Q(1, 3) + Q(1, 2**12)
    narrow = pilot.octagon_core(frame, lo, hi)
    c, s = trig((lo + hi) / 2)
    for nx, ny in ((c, s), (-s, c), (-c, -s), (s, -c)):
        support = max(nx * x + ny * y for x, y in narrow)
        assert Q(1, 2) - support < Q(1, 10**6), "the face-normal loss is not second order"
    envelope = pilot.producer.envelope_core(frame, lo, hi)
    assert Q(1, 2) - max(c * x + s * y for x, y in envelope) > Q(1, 10**4)


def test_the_n11_control_is_case_438_with_its_optimum_inside_its_cells() -> None:
    n11_frame = pilot.n11_frame()
    optimum = pilot.load_n11_endpoint(n11_frame)
    assert optimum.system == "n11"
    assert optimum.coarse is None
    assert not optimum.slides
    assert sorted(item.owner for item in optimum.targets) == [
        0,
        1,
        2,
        3,
        4,
        8,
        9,
        10,
        11,
        13,
        15,
    ]
    assert 0 < n11_frame.cap - optimum.side.hi < Q(1, 10**20)
    for item in optimum.targets:
        cell = n11_frame.world(item.owner)
        corners = [
            (Q(x), Q(y))
            for x in (item.centre[0].lo, item.centre[0].hi)
            for y in (item.centre[1].lo, item.centre[1].hi)
        ]
        assert all(pilot.in_convex(cell, corner) for corner in corners), item.label
    assert pilot.coordinates(3, (0.1, 0.2), optimum) == {"x": 0.1, "y": 0.2}


def test_partner_pruning_reads_boxes_apart_by_the_reach() -> None:
    first = (Q(0), Q(1), Q(0), Q(1))
    assert pilot.separated(first, (Q(5, 2), Q(3), Q(0), Q(1)), Q(3, 2))
    assert not pilot.separated(first, (Q(2), Q(3), Q(0), Q(1)), Q(3, 2))
    rows: list[dict[str, Any]] = [
        {"outer_domain": [["0", "0"], ["1", "0"], ["1", "2"]], "residual_polygons": []},
        {"outer_domain": [], "residual_polygons": [[["3", "1"]]]},
    ]
    assert pilot.bounding_box(rows, "outer_domain") == (Q(0), Q(1), Q(0), Q(2))
    assert pilot.bounding_box(rows, "residual_polygons") == (Q(3), Q(3), Q(1), Q(1))


def test_the_review_falsifier_and_the_contraction_start_are_read_from_rounds() -> None:
    def entry(index: int, extent: float, ratio: float, *, drop: bool) -> dict[str, Any]:
        return {
            "round": index,
            "worst_position_extent": extent,
            "max_row_to_extent": ratio,
            "median_row_to_extent": ratio,
            "rows_fine": ratio < pilot.FINE_ROWS,
            "rows_past_model_threshold": ratio < pilot.MODEL_THRESHOLD,
            "no_extent_drop": not drop,
            "complete": True,
        }

    flat = [entry(index, 1.0, 0.01, drop=False) for index in range(4)]
    reading = pilot.falsifier_reading(flat)
    assert reading["falsified"] is True
    assert reading["contraction_start"] is None
    falling = [
        entry(0, 1.0, 0.5, drop=False),
        entry(1, 1.0, 0.08, drop=False),
        entry(2, 0.5, 0.04, drop=True),
        entry(3, 0.25, 0.04, drop=True),
    ]
    reading = pilot.falsifier_reading(falling)
    assert reading["falsified"] is False
    assert reading["first_round_rows_under_a_tenth"] == 1
    assert reading["contraction_start"]["round"] == 2
    assert reading["contraction_start"]["max_row_to_extent_before"] == 0.08
    assert reading["g_after_start_geometric_mean"] == pytest.approx(0.5)


def test_a_checkpoint_resumes_after_a_comment_only_kernel_change(
    endpoint: pilot.Endpoint, frame: Frame, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A checkpoint written before a comment was appended to the kernel resumes: the
    change is recorded as drift, the run continues from the next round, and the whole node
    replays. Only other settings refuse a resume."""
    boxed, renumbered = pilot.box_frame(frame, endpoint, Q(1, 64))
    settings: dict[str, Any] = {
        "bins": 2,
        "max_live": 4,
        "min_width": Q(1, 64),
        "hull_limit": 16,
        "max_seconds": 120,
        "progress": False,
    }
    first = pilot.run_pilot(boxed, renumbered, max_rounds=1, checkpoints=tmp_path, **settings)
    saved = tmp_path / "checkpoint-round-001.json.gz"
    assert saved.exists()
    assert first.endpoint_lost is None
    # The provenance a fresh import would read after `# a comment` is appended to the
    # kernel's `__init__.py`, without editing the checkout under a running suite.
    changed = "packing/src/sqpack/hull_kernel/__init__.py"
    data = (pilot.KERNEL_DIR / "__init__.py").read_bytes() + b"# a comment\n"
    after = {
        **pilot.PROVENANCE,
        "dirty": True,
        "files": {**pilot.PROVENANCE["files"], changed: git_blob(data)},
    }
    monkeypatch.setattr(pilot, "PROVENANCE", after)
    resumed = pilot.run_pilot(
        boxed,
        renumbered,
        max_rounds=2,
        max_steps=len(first.node["steps"]) + 1,
        resume=saved,
        **{**settings, "max_live": 8},
    )
    assert resumed.resumed is not None
    assert resumed.resumed["round"] == 1
    assert resumed.resumed["changed_since"] == [changed]
    assert resumed.resumed["written_by"]["files"][changed] != git_blob(data)
    assert resumed.rounds[:2] == first.rounds
    assert resumed.node["steps"][: len(first.node["steps"])] == first.node["steps"]
    assert len(resumed.node["steps"]) == len(first.node["steps"]) + 1
    assert resumed.endpoint_lost is None
    replayed = pilot.replay(boxed, resumed, max_seconds=120)
    assert replayed["status"] == "PASS_REPLAYED"
    assert replayed["final_state_agrees"] is True
    with pytest.raises(RefusalError, match="settings differ"):
        pilot.run_pilot(
            boxed, renumbered, max_rounds=2, resume=saved, **{**settings, "bins": 8}
        )


def test_cli_round_one_resume_produces_no_updates_and_replays_saved_seed(
    endpoint: pilot.Endpoint, frame: Frame, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    boxed, renumbered = pilot.box_frame(frame, endpoint, Q(1, 64))
    first = pilot.run_pilot(
        boxed,
        renumbered,
        bins=2,
        max_rounds=1,
        max_live=4,
        min_width=Q(1, 64),
        hull_limit=16,
        max_seconds=120,
        progress=False,
        checkpoints=tmp_path,
        node_id="n17-capture-pilot",
    )
    saved = tmp_path / "checkpoint-round-001.json.gz"
    assert saved.exists()
    assert first.rounds[-1]["round"] == 1
    assert first.rounds[-1]["complete"] is True
    assert first.endpoint_lost is None

    def forbidden(*_args: Any, **_kwargs: Any) -> Any:
        pytest.fail("round-one replay must not produce an owner update or a new seed")

    original_admit = pilot.node.admit_seed
    admitted_seed_ids: list[str] = []

    def admit_saved_seed(*args: Any, **kwargs: Any) -> Any:
        admitted_seed_ids.append(pilot.producer.content_sha256(args[1]))
        return original_admit(*args, **kwargs)

    monkeypatch.setattr(pilot, "capture_frame", lambda _cap: boxed)
    monkeypatch.setattr(pilot, "load_endpoint", lambda _frame: renumbered)
    monkeypatch.setattr(pilot, "produce_step", forbidden)
    monkeypatch.setattr(pilot, "build_seed", forbidden)
    monkeypatch.setattr(pilot.node, "admit_seed", admit_saved_seed)
    output = tmp_path / "fresh-replay.json"
    assert (
        pilot.main(
            [
                "--max-rounds",
                "1",
                "--resume",
                str(saved),
                "--bins",
                "2",
                "--max-live",
                "4",
                "--min-width-log2",
                "6",
                "--hull-limit",
                "16",
                "--max-seconds",
                "120",
                "--replay-share",
                "0.5",
                "--output",
                str(output),
            ]
        )
        == 0
    )
    result = json.loads(output.read_text())
    assert admitted_seed_ids == [pilot.producer.content_sha256(first.seed)]
    assert result["resumed"]["round"] == 1
    assert result["resumed"]["changed_since"] == []
    assert result["updates"] == first.updates
    assert result["rounds"] == first.rounds
    assert result["seed_sha256"] == pilot.producer.content_sha256(first.seed)
    assert result["node_sha256"] == pilot.producer.content_sha256(first.node)
    assert result["endpoint_control"]["held"] is True
    assert result["replay"]["status"] == "PASS_REPLAYED"
    assert result["replay"]["steps"] == len(first.node["steps"])
    assert result["replay"]["final_state_agrees"] is True
