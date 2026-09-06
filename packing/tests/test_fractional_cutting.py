"""Controls for `sqpack.fractional.cutting`, the packing-side cutting-plane loop.

The loop's only claim is a lower bound on the fractional packing value, and the
only ways that claim can overreach are a depth above 1 that the separation
misses, an image that is not the D4 image it says it is, or a family that
leaves the container. Each is refused here on an instance small enough to check
by hand, and the positive control is the loop run end to end on the simplest
ceiling there is: four corner squares in side 2, total 4.
"""

from __future__ import annotations

import json
from fractions import Fraction
from io import StringIO
from pathlib import Path

import numpy as np
import pytest

from sqpack.fractional import cutting as cutting_module
from sqpack.fractional.ceiling import (
    CeilingCertificate,
    CeilingVerdict,
    ConditionReport,
    Placement,
    arrangement_lines,
    container_vertices,
    maximum_depth,
)
from sqpack.fractional.certificate import d4_images
from sqpack.fractional.colgen import LpSolution, Rows, SiteSet, site_set_from_points
from sqpack.fractional.cutting import (
    Separation,
    SupportEntry,
    cutting_plane_loop,
    depths_above,
    initial_sites,
    load_state,
    screened_separation,
    select_site_orbits,
    symmetric_placements,
    tidy_family,
    warm_start,
)

B = Fraction(9977, 10000)
LIMIT = Fraction(207107, 500000)
COARSE = (Fraction(0), LIMIT)
TWO = Fraction(2)


def stubbed_cutting_run(
    monkeypatch: pytest.MonkeyPatch,
    *,
    rows_objective: float,
    stop_on_covering_below_n: bool,
    rows_converged: bool = True,
    max_depth: Fraction = Fraction(2),
    family_total: Fraction = Fraction(1),
    state_path: Path | None = None,
    log_sinks: tuple[StringIO, ...] = (),
    verify_verdict: CeilingVerdict | None = None,
) -> tuple[cutting_module.CuttingLog, SiteSet, list[CeilingCertificate]]:
    """Run one deterministic loop iteration at the stop/site-addition boundary."""

    sites = site_set_from_points(TWO, {(Fraction(1), Fraction(1))})
    matrix = np.ones((1, 1))
    rows = Rows(
        directions=[0],
        centres=[(1.0, 1.0)],
        matrix=matrix,
        keys={matrix[0].tobytes()},
    )
    exact_rows = [(0, Fraction(1), Fraction(1))]
    solution = LpSolution(
        np.ones(1),
        np.ones(1),
        objective=rows_objective,
        stopped=(
            "converged: every placement covers mass 1"
            if rows_converged
            else "round cap reached"
        ),
    )
    new_orbit = site_set_from_points(TWO, {(Fraction(1, 2), Fraction(1, 2))}).orbits[0]
    separation = Separation(max_depth, 1, 1, 1, [(Fraction(2), new_orbit)])
    monkeypatch.setattr(cutting_module, "solve_rows", lambda *_args, **_kwargs: solution)
    monkeypatch.setattr(
        cutting_module,
        "solve_lp",
        lambda *_args, **_kwargs: (np.ones(1), np.ones(1), 10.5),
    )
    monkeypatch.setattr(
        cutting_module,
        "support_entries",
        lambda *_args, **_kwargs: (
            SupportEntry(0, Fraction(0), Fraction(1), Fraction(1), family_total),
        ),
    )
    monkeypatch.setattr(cutting_module, "arrangement_lines", lambda _family: [])
    monkeypatch.setattr(
        cutting_module, "screened_separation", lambda *_args, **_kwargs: separation
    )
    verified: list[CeilingCertificate] = []
    if verify_verdict is not None:

        def fake_verify(family: CeilingCertificate) -> CeilingVerdict:
            verified.append(family)
            return verify_verdict

        monkeypatch.setattr(cutting_module, "verify_ceiling", fake_verify)
    log = cutting_plane_loop(
        11,
        TWO,
        B,
        COARSE,
        sites=sites,
        rows=rows,
        exact_rows=exact_rows,
        max_iterations=1,
        stop_on_covering_below_n=stop_on_covering_below_n,
        log_sinks=log_sinks,
        state_path=state_path,
    )
    return log, sites, verified


def upright(x: Fraction, y: Fraction, weight: Fraction, side: Fraction = B) -> Placement:
    return Placement(Fraction(0), x, y, weight, side)


def test_symmetric_placements_are_the_eight_d4_images_of_the_entry() -> None:
    side = Fraction(3)
    entry = SupportEntry(1, LIMIT, Fraction(6, 5), Fraction(7, 4), Fraction(1))
    family = symmetric_placements([entry], side, B)
    assert len(family) == 8
    assert sum(p.weight for p in family) == 1
    original = Placement(LIMIT, entry.centre_x, entry.centre_y, Fraction(1, 8), B)
    expected = {
        frozenset(d4_images(x, y, side)[k] for x, y in original.corners()) for k in range(8)
    }
    assert {frozenset(p.corners()) for p in family} == expected
    # Four rotations keep the angle; four reflections take its mirror.
    assert sorted(p.half_tangent for p in family) == sorted(
        [LIMIT] * 4 + [(1 - LIMIT) / (1 + LIMIT)] * 4
    )


def test_a_centre_outside_the_container_is_refused() -> None:
    entry = SupportEntry(0, Fraction(0), Fraction(5, 2), Fraction(1), Fraction(1))
    with pytest.raises(ValueError, match="outside"):
        symmetric_placements([entry], TWO, B)
    with pytest.raises(ValueError, match="support weights must be non-negative"):
        symmetric_placements(
            [SupportEntry(0, Fraction(0), Fraction(1), Fraction(1), Fraction(-1))], TWO, B
        )


def test_depths_above_finds_exactly_the_overlap_vertices_at_depth_two() -> None:
    overlapping = (
        upright(Fraction(1, 2), Fraction(1, 2), Fraction(1), Fraction(1)),
        upright(Fraction(1), Fraction(1), Fraction(1), Fraction(1)),
    )
    certificate = CeilingCertificate(2, TWO, Fraction(1), COARSE, overlapping)
    vertices = container_vertices(certificate, arrangement_lines(certificate))
    deep, worst, decided = depths_above(certificate, vertices)
    assert worst == 2
    assert worst == maximum_depth(certificate, vertices)[0]
    assert decided >= 4
    assert {(x, y) for _, x, y in deep} == {
        (Fraction(1, 2), Fraction(1, 2)),
        (Fraction(1), Fraction(1, 2)),
        (Fraction(1, 2), Fraction(1)),
        (Fraction(1), Fraction(1)),
    }
    assert all(depth == 2 for depth, _, _ in deep)


def test_select_site_orbits_groups_vertices_into_new_d4_orbits() -> None:
    deep = [
        (Fraction(2), Fraction(1, 2), Fraction(1, 2)),
        (Fraction(2), Fraction(1), Fraction(1, 2)),
        (Fraction(2), Fraction(1, 2), Fraction(1)),
        (Fraction(2), Fraction(1), Fraction(1)),
    ]
    held = site_set_from_points(TWO, {(Fraction(1), Fraction(1))})
    chosen = select_site_orbits(deep, held, TWO, cap=10)
    # The centre is already held; the two remaining orbits have four members each.
    assert [len(orbit) for _, orbit in chosen] == [4, 4]
    assert select_site_orbits(deep, held, TWO, cap=1)[0][1] == chosen[0][1]
    assert select_site_orbits(deep, SiteSet(TWO, ()), TWO, cap=10)[1:]
    assert len(select_site_orbits(deep, SiteSet(TWO, ()), TWO, cap=10)) == 3


def test_opt_in_covering_stop_records_the_exact_iteration_before_site_addition(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    state = tmp_path / "state.json"
    transcript = StringIO()
    log, sites, _ = stubbed_cutting_run(
        monkeypatch,
        rows_objective=10.75,
        stop_on_covering_below_n=True,
        state_path=state,
        log_sinks=(transcript,),
    )
    reason = "row-converged covering objective below n at iteration 0"
    assert log.stopped == reason
    assert len(log.iterations) == 1
    assert log.iterations[0].rows_converged
    assert log.iterations[0].rows_objective == 10.75
    assert log.iterations[0].max_depth == 2
    assert log.iterations[0].added == 0
    assert log.best_iteration == 0
    assert log.best_family is not None
    assert log.sites == sites
    saved = json.loads(state.read_text())
    assert saved["stopped"] == reason
    assert saved["iterations"][0]["note"] == reason
    assert len(saved["sites"]) == sites.size
    assert f"stopped: {reason}" in transcript.getvalue()


def test_covering_stop_is_opt_in_and_requires_a_converged_row_solve(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    default, _, _ = stubbed_cutting_run(
        monkeypatch,
        rows_objective=10.75,
        stop_on_covering_below_n=False,
    )
    assert default.stopped == "iteration cap 1 reached"
    assert default.iterations[0].added == 1

    default_non_finite, _, _ = stubbed_cutting_run(
        monkeypatch,
        rows_objective=float("inf"),
        stop_on_covering_below_n=False,
    )
    assert default_non_finite.stopped == "iteration cap 1 reached"
    assert default_non_finite.iterations[0].added == 1

    unfinished, _, _ = stubbed_cutting_run(
        monkeypatch,
        rows_objective=10.75,
        stop_on_covering_below_n=True,
        rows_converged=False,
    )
    assert unfinished.stopped == "iteration cap 1 reached"
    assert unfinished.iterations[0].added == 1


def test_opt_in_covering_stop_refuses_a_non_finite_converged_objective(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    transcript = StringIO()
    reason = "technical refusal: non-finite row-converged covering objective at iteration 0"
    new_state = tmp_path / "new-state.json"
    with pytest.raises(RuntimeError, match=reason):
        stubbed_cutting_run(
            monkeypatch,
            rows_objective=float("inf"),
            stop_on_covering_below_n=True,
            state_path=new_state,
            log_sinks=(transcript,),
        )
    assert not new_state.exists()
    assert "rows_objective=" not in transcript.getvalue()
    assert f"failed: {reason}" in transcript.getvalue()

    old_state = tmp_path / "old-state.json"
    checkpoint = b'{"stopped":"prior checkpoint"}\n'
    old_state.write_bytes(checkpoint)
    with pytest.raises(RuntimeError, match=reason):
        stubbed_cutting_run(
            monkeypatch,
            rows_objective=float("nan"),
            stop_on_covering_below_n=True,
            state_path=old_state,
        )
    assert old_state.read_bytes() == checkpoint


def test_opt_in_covering_stop_is_strict_at_equality(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    log, _, _ = stubbed_cutting_run(
        monkeypatch,
        rows_objective=11.0,
        stop_on_covering_below_n=True,
    )
    assert log.stopped == "iteration cap 1 reached"
    assert log.iterations[0].added == 1


def test_opt_in_covering_stop_continues_above_n(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    log, _, _ = stubbed_cutting_run(
        monkeypatch,
        rows_objective=11.25,
        stop_on_covering_below_n=True,
    )
    assert log.stopped == "iteration cap 1 reached"
    assert log.iterations[0].added == 1


def test_exact_ceiling_verification_precedes_the_opt_in_covering_stop(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    verdict = CeilingVerdict(
        (ConditionReport("exact ceiling", "synthetic precedence control", holds=True),),
        total_weight=Fraction(11),
        max_depth=Fraction(1),
        vertices=1,
        decided_exactly=1,
        regime="fixed-B",
        symmetric_only=False,
    )
    log, _, verified = stubbed_cutting_run(
        monkeypatch,
        rows_objective=10.75,
        stop_on_covering_below_n=True,
        max_depth=Fraction(1),
        family_total=Fraction(11),
        verify_verdict=verdict,
    )
    assert len(verified) == 1
    assert log.verdict is verdict
    assert log.stopped == "ceiling proved at iteration 0"


def test_the_loop_reaches_the_corner_ceiling_at_side_two(tmp_path: Path) -> None:
    """Four disjoint B-squares fit in side 2, so the packing value there is at
    least 4, and the loop must find a feasible family at that total."""

    sites = initial_sites(TWO, B, grid_counts=(5, 7))
    rows = Rows()
    exact_rows: list = []
    state = tmp_path / "state.json"
    log = cutting_plane_loop(
        4,
        TWO,
        B,
        COARSE,
        sites=sites,
        rows=rows,
        exact_rows=exact_rows,
        cap=20,
        max_iterations=12,
        state_path=state,
    )
    assert log.iterations, log.stopped
    assert log.best_family is not None
    assert log.best_scaled_total >= Fraction(399, 100)
    assert (
        maximum_depth(
            log.best_family,
            container_vertices(log.best_family, arrangement_lines(log.best_family)),
        )[0]
        <= 1
    )
    assert len(exact_rows) == len(rows)
    old_side, points, carried = load_state(state)
    assert log.sites is not None
    assert old_side == TWO
    assert len(points) == log.sites.size
    assert len(carried) == len(rows)
    warm_sites, warm_rows = warm_start(
        points,
        carried,
        old_side=TWO,
        new_side=Fraction(21, 10),
        square_side=B,
        half_tangents=COARSE,
    )
    assert warm_sites.size >= len(points)
    assert all(
        0 <= x <= Fraction(21, 10) and 0 <= y <= Fraction(21, 10) for _, x, y in warm_rows
    )


def test_malformed_inputs_are_refused(tmp_path: Path) -> None:
    sites = initial_sites(TWO, B, grid_counts=(5,))
    with pytest.raises(ValueError, match="positive"):
        cutting_plane_loop(0, TWO, B, COARSE, sites=sites, rows=Rows(), exact_rows=[])
    with pytest.raises(ValueError, match="larger"):
        cutting_plane_loop(
            4, Fraction(1, 2), B, COARSE, sites=sites, rows=Rows(), exact_rows=[]
        )
    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps({"outer_side": "2", "sites": []}))
    with pytest.raises(ValueError, match="rows"):
        load_state(bad)
    bad.write_text(json.dumps({"outer_side": "2", "sites": [], "rows": [[0, "5", "1"]]}))
    with pytest.raises(ValueError, match="outside"):
        load_state(bad)
    with pytest.raises(ValueError, match="larger side"):
        warm_start(
            [], [], old_side=TWO, new_side=Fraction(1), square_side=B, half_tangents=COARSE
        )


def test_screened_separation_certifies_the_same_maximum_as_the_full_scan() -> None:
    overlapping = (
        upright(Fraction(1, 2), Fraction(1, 2), Fraction(1), Fraction(1)),
        upright(Fraction(1), Fraction(1), Fraction(1), Fraction(1)),
        upright(Fraction(3, 2), Fraction(1, 2), Fraction(1, 2), Fraction(1)),
    )
    certificate = CeilingCertificate(2, TWO, Fraction(1), COARSE, overlapping)
    lines = arrangement_lines(certificate)
    held = site_set_from_points(TWO, {(Fraction(1), Fraction(1))})
    found = screened_separation(
        certificate, lines, held, cap=10, select_above=Fraction(1000001, 1000000)
    )
    full = maximum_depth(certificate, container_vertices(certificate, lines))[0]
    assert found.max_depth == full == Fraction(5, 2)
    assert found.vertices >= len(container_vertices(certificate, lines))
    # The centre is held; the deepest new site is the corner all three squares share.
    depths = [depth for depth, _ in found.chosen]
    assert depths[0] == Fraction(5, 2)
    assert depths == sorted(depths, reverse=True)
    assert all(depth > 1 for depth in depths)
    assert all(
        point not in {p for orbit in held.orbits for p in orbit}
        for _, orbit in found.chosen
        for point in orbit
    )
    assert found.decided >= len(found.chosen)


def test_tidy_family_rounds_weights_down_and_keeps_the_family_feasible() -> None:
    ugly = Fraction(1, 3)
    family = CeilingCertificate(
        2,
        TWO,
        Fraction(1),
        COARSE,
        (
            upright(Fraction(1, 2), Fraction(1, 2), ugly, Fraction(1)),
            upright(Fraction(1), Fraction(1), 1 - ugly, Fraction(1)),
        ),
    )
    tidy = tidy_family(family, 1000)
    assert [p.weight for p in tidy.placements] == [Fraction(333, 1000), Fraction(666, 1000)]
    assert tidy.total_weight <= family.total_weight
    assert family.total_weight - tidy.total_weight <= Fraction(2, 1000)
    assert maximum_depth(tidy, container_vertices(tidy, arrangement_lines(tidy)))[0] <= 1
    with pytest.raises(ValueError, match="positive"):
        tidy_family(family, 0)
