"""Private #399 house checks retain complete custody within one invocation."""

from __future__ import annotations

import copy
from pathlib import Path
from typing import cast

import pytest

from devtools import evand_arrangement_houses as houses
from devtools import evand_arrangement_reports as reports
from sqpack.witness import witness_document


@pytest.fixture
def historical_houses(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Retain all three #399 poses after later sources replace live atlas leaves."""
    original_repo = houses.REPO
    private = tmp_path / "historical-arrangement-houses"
    packet = private / reports.PACKET.relative_to(original_repo)
    for source in houses.private_input_paths():
        destination = private / source.relative_to(original_repo)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(source.read_bytes())
    monkeypatch.setattr(reports, "REPO", private)
    monkeypatch.setattr(reports, "PACKET", packet)
    monkeypatch.setattr(houses, "REPO", private)
    facts = reports.read_facts()
    positives = reports.check_certification()
    for n in reports.NUMBERS:
        path = houses.house_path(n)
        path.parent.mkdir(parents=True, exist_ok=True)
        witness = houses.expected_house(facts[n], positives[n])
        assert witness["source"]["key"] == reports.SOURCE_KEY
        path.write_text(witness_document(witness, schema="../witness.schema.yaml"))


@pytest.mark.usefixtures("historical_houses")
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


@pytest.mark.usefixtures("historical_houses")
def test_shared_custody_still_checks_the_entire_current_house(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    inputs = houses.VerifiedInputs()
    path = houses.house_path(270)
    houses.check_houses([270], verified_inputs=inputs)
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
