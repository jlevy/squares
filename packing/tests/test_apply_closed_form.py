"""The closed form's reported lanes are what `devtools.apply_closed_form` writes."""

from __future__ import annotations

import dataclasses
from decimal import Decimal
from fractions import Fraction

import pytest

from devtools import apply_closed_form as tool
from sqpack.yamlio import safe_load


def _case(n: int) -> dict:
    text = (tool.FRONTIER / f"n-{n:03d}.md").read_text(encoding="utf-8")
    return safe_load(text.split("---\n")[1])["packing"]


def test_every_record_is_written() -> None:
    assert tool.stale() == []


def test_the_lanes_it_raises_and_the_ones_it_leaves() -> None:
    raised = {plan.n for plan in tool.plans()}
    assert len(raised) == 154
    # A registered report pending adoption is stronger at 125 (T-144) and 148 (T-179).
    assert 125 not in raised
    assert 148 not in raised
    assert {126, 149} <= raised


def test_a_raised_lane_rounds_down_and_cites_the_report() -> None:
    field = _case(149)["reported_lower_bound"]
    assert field["evidence"] == [tool.REPORT]
    assert field["source_key"] == tool.SOURCE_KEY
    value, exact = Decimal(field["value"]), Fraction(field["exact_form"])
    plan = next(plan for plan in tool.plans() if plan.n == 149)
    assert Fraction(value) <= exact <= Fraction(plan.a30)
    assert exact > Fraction(plan.a30) - Fraction(1, 10**30)


def test_a_stronger_pending_report_keeps_its_count() -> None:
    assert _case(125)["reported_lower_bound"]["source_key"] != tool.SOURCE_KEY
    assert _case(148)["reported_lower_bound"]["source_key"] != tool.SOURCE_KEY
    assert tool.stronger(148, Decimal("12.2277")) == "T-179"
    assert tool.stronger(149, Decimal("12.2804")) is None


#: A record the tool has not written, at 149: its reported bound, its verified upper
#: bound, one evidence id and one resource, and a body paragraph.
SYNTHETIC = """---
packing:
  n: 149
  source_reviewed: '2026-10-01'
  reported_lower_bound:
    value: '{held}'
    kind: nagamochi
  verified_upper_bound:
    value: '{upper}'
    exact_form: '{upper}'
  evidence:
  - E-nagamochi-lower
  resources:
  - key: '[Nagamochi 2005]'
    role: lower-bound-proof
---
# `s(149)` — open

A paragraph the case already has.
"""


def _plan(n: int = 149) -> tool.Plan:
    return next(plan for plan in tool.plans() if plan.n == n)


def _record(held: str | None = None, upper: str = "12.71") -> str:
    return SYNTHETIC.format(held=held or _plan().held["value"], upper=upper)


def test_a_record_is_written_once_and_a_second_run_changes_nothing() -> None:
    plan = _plan()
    once = tool.apply_text(plan, _record())
    assert tool.apply_text(plan, once) == once
    packing = safe_load(once.split("---\n")[1])["packing"]
    assert packing["reported_lower_bound"]["source_key"] == tool.SOURCE_KEY
    assert packing["evidence"] == ["E-nagamochi-lower", tool.REPORT]
    assert [item["key"] for item in packing["resources"]] == [
        "[Nagamochi 2005]",
        tool.SOURCE_KEY,
    ]
    assert packing["source_reviewed"] == tool.INTAKE
    assert once.split("\n\n")[1].startswith(tool.OPENING)


def test_a_record_whose_reported_bound_has_moved_is_refused() -> None:
    with pytest.raises(ValueError, match="not the"):
        tool.apply_text(_plan(), _record(held="12.2250"))


def test_no_lane_is_raised_where_a_n_is_not_above_the_bound() -> None:
    plan = _plan()
    assert tool.raises(plan.a30, plan.held)
    assert not tool.raises(plan.a30, {"value": str(plan.a30)})
    above = dataclasses.replace(plan, held={**plan.held, "value": "12.29"})
    with pytest.raises(ValueError, match="not above"):
        tool.apply_text(above, _record(held="12.29"))


def test_a_record_whose_verified_upper_bound_is_not_above_a_n_is_refused() -> None:
    with pytest.raises(ValueError, match="verified upper bound"):
        tool.apply_text(_plan(), _record(upper="12.28"))


def test_a_proved_count_is_left_to_its_generator() -> None:
    """At the 33 counts m^2 - j the closed form meets the proved value; the records stay
    as the generator drafts them, and T-064, T-084 and T-086 name the route."""
    packing = _case(63)
    assert packing["reported_lower_bound"]["source_key"] != tool.SOURCE_KEY
    assert tool.REPORT not in packing["evidence"]


def test_the_generator_redrafts_a_raised_record_as_held_and_a_fresh_one_without_it() -> None:
    """`generate_frontier_case` replays the closed form where a record carries it, so a
    check or a refresh keeps the raised lane (review C2 of #602); a fresh draft, which
    knows nothing of it, leaves the lane to this tool."""
    from devtools import generate_frontier_case as generator  # noqa: PLC0415

    n = 106
    held = (tool.FRONTIER / f"n-{n:03d}.md").read_text(encoding="utf-8")
    assert tool.carried(held)
    availability = generator.load_availability()
    catalogue = generator.load_drafting_catalogue([n], availability)
    on = "2026-09-30"
    redrafted = generator.redraft(
        n,
        held,
        availability=availability,
        catalogue=catalogue,
        review_date=on,
        retrieved_date=on,
    )
    assert tool.carried(redrafted)
    assert redrafted.count(tool.OPENING) == 1
    fresh = generator.generate_record(
        n, availability=availability, catalogue=catalogue, review_date=on, retrieved_date=on
    )
    assert not tool.carried(generator.adopt_upper_bound_packet(n, fresh))
