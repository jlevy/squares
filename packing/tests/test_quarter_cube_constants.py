"""Refusal controls for the retained quarter/cube arithmetic consequences."""

from dataclasses import replace
from typing import Any

import pytest
from mpmath.ctx_iv import MPIntervalContext

from cases.asymptotic.quarter_cube_constants import (
    CUBE_ROWS,
    QUARTER_ROWS,
    check_constants,
    interval_max,
)


def test_published_consequences_hold() -> None:
    checks = check_constants()
    assert all(check.holds for check in checks)
    assert len([c for c in checks if "asymptotic floor" in c.name]) == 4
    assert len([c for c in checks if "main margin" in c.name]) == 8


@pytest.mark.parametrize("claim", ["0.2", "1"])
def test_stronger_quarter_claim_is_refused(claim: str) -> None:
    assert not all(c.holds for c in check_constants(quarter_claim=claim))


@pytest.mark.parametrize(("field", "value"), [("c0", "1"), ("threshold", 10**11)])
def test_quarter_domain_or_threshold_mutant_is_refused(field: str, value: Any) -> None:
    row = replace(QUARTER_ROWS[0], **{field: value})
    assert not all(c.holds for c in check_constants(quarter_rows=(row, QUARTER_ROWS[1])))


@pytest.mark.parametrize(
    ("field", "value"),
    [("gamma", "0.1"), ("tau0", "0.01"), ("right_cap", "0.1"), ("end", 10**20)],
)
def test_cube_margin_branch_or_outward_bound_mutant_is_refused(field: str, value: Any) -> None:
    row = replace(CUBE_ROWS[0], **{field: value})
    assert not all(c.holds for c in check_constants(cube_rows=(row, *CUBE_ROWS[1:])))


def test_range_gap_is_refused_even_when_local_bounds_hold() -> None:
    row = replace(CUBE_ROWS[1], start=CUBE_ROWS[1].start + 1)
    checks = check_constants(cube_rows=(CUBE_ROWS[0], row, *CUBE_ROWS[2:]))
    assert not next(c for c in checks if c.name == "cube roster").holds
    assert all(c.holds for c in checks if c.name.startswith("cube case2 "))


def test_missing_range_is_refused() -> None:
    assert not all(c.holds for c in check_constants(cube_rows=CUBE_ROWS[1:]))


def test_duplicate_quarter_route_is_refused() -> None:
    assert not all(c.holds for c in check_constants(quarter_rows=(QUARTER_ROWS[0],) * 2))


@pytest.mark.parametrize(
    ("field", "value"), [("b", "0"), ("nu", "-0.01"), ("exponent_denominator", 0)]
)
def test_nonphysical_cube_parameters_raise(field: str, value: Any) -> None:
    row = replace(CUBE_ROWS[0], **{field: value})
    with pytest.raises(ValueError, match=r"domain|parameters"):
        check_constants(cube_rows=(row, *CUBE_ROWS[1:]))


def test_asymptotic_overclaim_is_refused() -> None:
    assert not all(c.holds for c in check_constants(quarter_asymptotic=("1", "1")))
    assert not all(c.holds for c in check_constants(cube_asymptotic=("1", "1")))


def testinterval_max_keeps_overlap_upper_endpoint() -> None:
    ctx: Any = MPIntervalContext()
    ctx.dps = 60
    result = interval_max(ctx, ctx.mpf([2, 4]), ctx.mpf([1, 3]))
    assert result.a <= 2
    assert result.b >= 4
