"""House selection from a project result's own report and confirming replay."""

from fractions import Fraction
from typing import Any

import pytest

from devtools import select_houses as select

SOURCE = "[project packing]"
REPORT = "E-packing-report"
REPLAY = "E-packing-replay"


@pytest.fixture
def project_result() -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    entry = {
        "id": "T-900",
        "kind": "upper-bound",
        "established": "2026-11-23",
        "registered": "2026-11-24",
        "verification": "V3",
        "confirmation": "C3",
        "scope": {"n_values": [127, 131]},
        "evidence": [REPORT, REPLAY],
        "reviews": [{"verdict": "accepted", "covers": ["T-900"]}],
        "regularizations": [{"n": 127, "of": "T-330"}],
    }
    report = {
        "claim": "upper-bound",
        "assurance": "reported",
        "source_key": SOURCE,
        "scope": {"n_values": [127, 131]},
    }
    replay = {
        **report,
        "assurance": "verified",
        "origin": "replayed-here",
        "performed_by": "repository",
        "replay_status": "passed",
        "scope": {"n_values": [127]},
    }
    return entry, {REPORT: report, REPLAY: replay}


def test_first_party_exact_side_can_become_the_house(
    monkeypatch: pytest.MonkeyPatch,
    project_result: tuple[dict[str, Any], dict[str, dict[str, Any]]],
) -> None:
    entry, evidence = project_result
    side = Fraction("11.800793726614962238623103308879")
    monkeypatch.setitem(select.reports.HOUSES, SOURCE, {127: side}.__getitem__)
    cases = {127: select.Case(127, Fraction(12), Fraction(12), "", ())}
    unread: list[str] = []

    selection = select.select([entry], evidence, cases=cases, unread=unread)

    assert set(selection) == {127}
    house = selection[127].house
    assert house is not None
    assert house.side == side
    assert house.source_key == SOURCE
    assert house.published == "2026-11-23"
    assert house.report_evidence == (REPORT,)
    assert house.confirming_evidence == (REPLAY,)
    assert house.regularizes == "T-330"
    assert not unread


@pytest.mark.parametrize(
    "report_override",
    [
        {"claim": "lower-bound"},
        {"scope": {"n_values": [131]}},
        {"source_key": "[unrelated]"},
    ],
)
def test_first_party_replay_needs_a_matching_bound_report(
    project_result: tuple[dict[str, Any], dict[str, dict[str, Any]]],
    report_override: dict[str, Any],
) -> None:
    entry, evidence = project_result
    evidence[REPORT].update(report_override)

    assert select.source_key_at(entry, evidence, 127) == ""


def test_first_party_source_is_unread_when_confirmations_disagree(
    monkeypatch: pytest.MonkeyPatch,
    project_result: tuple[dict[str, Any], dict[str, dict[str, Any]]],
) -> None:
    entry, evidence = project_result
    entry["evidence"].append("E-unrelated-replay")
    evidence["E-unrelated-replay"] = {**evidence[REPLAY], "source_key": "[unrelated]"}
    monkeypatch.setitem(select.reports.HOUSES, SOURCE, {127: Fraction(11)}.__getitem__)
    unread: list[str] = []

    assert not select.candidates([entry], evidence, unread=unread)
    assert unread == ["T-900"]
