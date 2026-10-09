"""Private #399 house checks retain complete custody within one invocation."""

from __future__ import annotations

import copy
from typing import cast

import pytest

from devtools import evand_arrangement_houses as houses
from devtools import evand_arrangement_reports as reports


def test_one_explicit_house_context_reuses_complete_custody(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls = []
    original = reports.check_certification

    def counted():
        calls.append(True)
        return original()

    monkeypatch.setattr(reports, "check_certification", counted)
    inputs = houses.VerifiedInputs()
    for n in reports.NUMBERS:
        houses.check_houses([n], verified_inputs=inputs)
    assert len(calls) == 1


def test_default_house_checks_read_new_custody_on_a_later_invocation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    houses.check_houses([266])

    def refused():
        raise reports.ReportError("changed complete receipt")

    monkeypatch.setattr(reports, "check_certification", refused)
    with pytest.raises(reports.ReportError, match="changed complete receipt"):
        houses.check_houses([266])


def test_house_context_cannot_be_an_unvalidated_dictionary() -> None:
    with pytest.raises(reports.ReportError, match="complete validated #399 custody"):
        houses.check_houses([266], verified_inputs=cast(houses.VerifiedInputs, {}))


def test_shared_custody_still_checks_the_entire_current_house(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    inputs = houses.VerifiedInputs()
    path = houses.house_path(270)
    original = houses.house.bounded_house
    changed = copy.deepcopy(original(path))
    changed["source"]["revision"] = "0" * 40
    monkeypatch.setattr(
        houses.house,
        "bounded_house",
        lambda selected: changed if selected == path else original(selected),
    )
    with pytest.raises(reports.ReportError, match="geometry or metadata differs"):
        houses.check_houses([270], verified_inputs=inputs)
