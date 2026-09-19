"""Cheap geometric and MIP tests for the M3 integral-piercing library."""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

import numpy as np
import pytest
from scipy.optimize import OptimizeResult

import sqpack.fractional.integral_piercing as piercing
from sqpack.fractional.integral_piercing import (
    DEFAULT_SQUARE_SIDE,
    T018_SHRINK,
    ClosedSquare,
    M3Verdict,
    SearchStatus,
    axis_aligned,
    cover_matrix_for_squares,
    encode_event_cell_covers,
    geometry_fields,
    load_unique_sites,
    m3_verdict_for,
    solve_integral_set_cover,
    span_and_broadcast_cover_rows,
    t018_certificate_path,
)
from sqpack.fractional.threshold_coverage_encoding import unique_rows

PACKING = Path(__file__).resolve().parents[1]


def _certificate_distinct_xy() -> int:
    path = PACKING / "cases/n11_fractional_certificate/certificate.json"
    raw = json.loads(path.read_text())
    return len({(str(x), str(y)) for x, y, _w in raw["atoms"]})


def test_t018_unique_sites_match_the_certificate() -> None:
    sites = load_unique_sites()
    assert len(sites) == _certificate_distinct_xy()
    assert len(sites) > 0
    assert load_unique_sites(t018_certificate_path()) == sites


def test_three_pairwise_distant_squares_need_three_piercings() -> None:
    axis = axis_aligned()
    squares = (
        ClosedSquare(Fraction(1, 2), Fraction(1, 2), axis),
        ClosedSquare(Fraction(5, 2), Fraction(1, 2), axis),
        ClosedSquare(Fraction(1, 2), Fraction(5, 2), axis),
    )
    sites = tuple((square.center_x, square.center_y) for square in squares)
    rows = cover_matrix_for_squares(sites, squares)
    assert rows.tolist() == [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    outcome = solve_integral_set_cover(rows)
    assert outcome.search_status is SearchStatus.feasible
    assert outcome.piercing == 3
    assert m3_verdict_for(outcome.search_status, outcome.piercing) is M3Verdict.eleven_candidate


def test_two_nested_squares_need_one_piercing() -> None:
    axis = axis_aligned()
    squares = (
        ClosedSquare(Fraction(1), Fraction(1), axis, Fraction(1)),
        ClosedSquare(Fraction(1), Fraction(1), axis, Fraction(2)),
    )
    sites = ((Fraction(1), Fraction(1)), (Fraction(19, 10), Fraction(1)))
    rows = cover_matrix_for_squares(sites, squares)
    assert rows.tolist() == [[1, 0], [1, 1]]
    outcome = solve_integral_set_cover(rows)
    assert outcome.piercing == 1
    assert outcome.selected == (0,)
    assert m3_verdict_for(outcome.search_status, outcome.piercing) is M3Verdict.eleven_candidate


def test_twelve_disjoint_cells_kill_at_cardinality_eleven() -> None:
    rows = np.eye(12, dtype=np.uint8)
    limited = solve_integral_set_cover(rows, cardinality_limit=11)
    assert limited.search_status is SearchStatus.infeasible
    assert limited.piercing is None
    verdict = m3_verdict_for(limited.search_status, limited.piercing)
    assert verdict is M3Verdict.killed_coarse_net
    full = solve_integral_set_cover(rows)
    assert full.piercing == 12
    assert m3_verdict_for(full.search_status, full.piercing) is M3Verdict.killed_coarse_net


def test_timeout_is_unresolved_never_a_kill(monkeypatch: pytest.MonkeyPatch) -> None:
    def timeout_milp(*_args: object, **_kwargs: object) -> OptimizeResult:
        return OptimizeResult(success=False, status=1, x=None, fun=None, message="time limit")

    monkeypatch.setattr(piercing, "milp", timeout_milp)
    outcome = solve_integral_set_cover(np.eye(3, dtype=np.uint8), time_limit_s=0.01)
    assert outcome.search_status is SearchStatus.timeout
    assert outcome.piercing is None
    assert m3_verdict_for(outcome.search_status, outcome.piercing) is M3Verdict.unresolved


def test_solver_error_without_incumbent_is_unresolved_never_a_kill(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def error_milp(*_args: object, **_kwargs: object) -> OptimizeResult:
        return OptimizeResult(success=False, status=4, x=None, fun=None, message="other")

    monkeypatch.setattr(piercing, "milp", error_milp)
    outcome = solve_integral_set_cover(np.eye(3, dtype=np.uint8))
    assert outcome.search_status is SearchStatus.encoding_ready
    assert outcome.piercing is None
    assert outcome.optimizer_ran is True
    assert m3_verdict_for(outcome.search_status, outcome.piercing) is M3Verdict.unresolved


def test_span_cover_matches_cell_broadcast() -> None:
    sites = (
        (Fraction(1), Fraction(1)),
        (Fraction(2), Fraction(1)),
        (Fraction(1), Fraction(2)),
        (Fraction(5, 2), Fraction(5, 2)),
    )
    span_rows, chunk_rows = span_and_broadcast_cover_rows(
        sites, outer_side=Fraction(4), square_side=Fraction(1), direction=axis_aligned()
    )

    def row_keys(rows: np.ndarray) -> set[bytes]:
        if rows.size == 0:
            return set()
        return {bytes(row.tobytes()) for row in unique_rows(rows)}

    assert row_keys(span_rows) == row_keys(chunk_rows)


def test_tiny_event_cell_instance_has_piercing_one() -> None:
    encoding = encode_event_cell_covers(
        ((Fraction(1), Fraction(1)),),
        outer_side=Fraction(2),
        square_side=Fraction(1),
        direction_steps=1,
    )
    assert encoding.site_count == 1
    assert encoding.reachable_cells > 0
    assert encoding.truncated is False
    outcome = solve_integral_set_cover(encoding.rows)
    assert outcome.piercing == 1
    assert m3_verdict_for(outcome.search_status, outcome.piercing) is M3Verdict.eleven_candidate


def test_unit_square_is_the_ownership_object() -> None:
    fields = geometry_fields(DEFAULT_SQUARE_SIDE)
    assert fields["using_unit_squares"] is True
    assert fields["t018_shrink"] == str(T018_SHRINK)
    assert DEFAULT_SQUARE_SIDE != T018_SHRINK


def test_truncated_rows_cannot_nominate_an_eleven_candidate() -> None:
    assert m3_verdict_for(SearchStatus.feasible, 11, truncated=True) is M3Verdict.unresolved
    assert (
        m3_verdict_for(SearchStatus.feasible, 12, truncated=True) is M3Verdict.killed_coarse_net
    )


def test_library_does_not_expose_a_float_lp_path() -> None:
    assert "linprog" not in piercing.__dict__
