"""A restatement under the owner's option D improves on nothing and is held to its receipt.

The owner's answer of 17 November 2026 (think-b0w5): a re-certification of a standing
packing, its padding removed or the same arrangement re-solved to its exact local optimum,
is a new result only if its side is below its predecessor's once the predecessor is shrunk
until its squares first touch (`devtools.contraction_margin`); otherwise it restates the
predecessor, credited to the original finder. A register entry that records such a report
names each count in its `restatements`. `check_standing.restated` keeps those counts out of
every improvement, so the entry is adopted nowhere and no profile counts it current, and
`check_results.restatements_problems` holds each item to its scope, its predecessor and the
receipt that measured it.
"""

from __future__ import annotations

import dataclasses
from collections.abc import Mapping
from typing import Any

import pytest

from devtools import check_requests, check_results, check_standing, profile_records
from devtools import render_recent_results as view

#: Kaelan Yim's 130 (T-281) against T-259's certificate: 0.0896 of its margin.
WITHIN = "packing/resources/web/yim-certificates-2026-11-09/measure/contraction-n130.json"
#: The same certificate's predecessor measured at 299 (T-280 against T-277).
ELSEWHERE = "packing/resources/web/yim-certificates-2026-11-09/measure/contraction-n299.json"
#: The project's regularizer candidate at 130 against T-259: outside the margin.
OUTSIDE = (
    "packing/cases/register_candidates/think-ruu2-2026-10-31/measure/contraction-n130-t259.json"
)


@pytest.fixture(scope="module")
def records() -> view.Records:
    return view.load_records()


def _item(**changes: Any) -> dict[str, Any]:
    item: dict[str, Any] = {
        "n": 130,
        "of": "T-259",
        "ruling": "think-b0w5",
        "gain_over_margin": "0.0896",
        "measured_in": WITHIN,
    }
    item.update(changes)
    return item


def _restated(records: view.Records, *items: Mapping[str, Any]) -> dict[str, Any]:
    """T-281 as a record of a restatement at the counts `items` name, and nowhere else."""
    record = {**records.results["T-281"], "restatements": [dict(item) for item in items]}
    record.pop("regularizations", None)
    return record


def _problems(records: view.Records, record: Mapping[str, Any]) -> list[str]:
    results = records.register.results
    dated = {str(other["id"]): check_results.result_date(other) for other in results}
    scopes = {
        str(other["id"]): set(check_results.scope_values(other["scope"])) for other in results
    }
    return check_results.restatements_problems(record, dated, scopes)


def test_a_restated_count_improves_on_nothing(records: view.Records) -> None:
    """Restated at 130, T-281 is better than no case record there, reads superseded, and
    the superseded check does not hold its stated side against the reported lane."""
    record = _restated(records, _item())
    assert check_standing.restated(record) == frozenset({130})
    assert check_standing.improvements(record, records) == []
    assert view.standing(record, records) == view.SUPERSEDED
    assert check_standing.problems(record, view.SUPERSEDED, records) == []
    assert "restates its predecessor at n = 130" in check_standing.summary(
        record, view.SUPERSEDED, records
    )


def test_a_restated_count_is_superseded_by_the_bounds_its_case_rests_on(
    records: view.Records,
) -> None:
    """Restated at 130, T-281's stated side is below T-259's, so no lane there ties or
    beats its words; the mark still names T-259, the bound the case rests on, which the
    predecessor shrunk to first contact proves at least as much as. Without the
    restatement the same words name nothing at 130."""
    record = _restated(records, _item())
    assert view.superseding(record, records) == ("T-259",)
    assert view.position_marks(record, view.SUPERSEDED, records) == ["superseded by T-259"]
    unrestated = {**record, "restatements": []}
    assert view.superseding(unrestated, records) == ()


def test_a_restated_report_is_no_current_record(records: view.Records) -> None:
    """The profile index counts a report that improves nowhere as no current record."""
    record = _restated(records, _item())
    shadow = dataclasses.replace(records, results={**records.results, "T-281": record})
    index = profile_records.build_record_index(shadow)
    assert "T-281" not in index.current_results


def test_a_restatement_is_held_to_its_scope_predecessor_and_receipt(
    records: view.Records,
) -> None:
    assert _problems(records, _restated(records, _item())) == []
    cases = {
        "twice": (_restated(records, _item(), _item()), "listed twice"),
        "scope": (_restated(records, _item(n=131)), "outside this result's scope"),
        "itself": (_restated(records, _item(of="T-281")), "names the result itself"),
        "unknown": (_restated(records, _item(of="T-999")), "not registered"),
        "later": (_restated(records, _item(of="T-286")), "whose scope does not hold"),
        "ruling": (_restated(records, _item(ruling="think-fwa9")), "names no ruling"),
        "share": (_restated(records, _item(gain_over_margin="0.0897")), "is not the receipt"),
        "count": (_restated(records, _item(measured_in=ELSEWHERE)), "receipt at n = 130"),
        "outside": (
            _restated(records, _item(measured_in=OUTSIDE)),
            "outside the predecessor's margin",
        ),
        "missing": (
            _restated(records, _item(measured_in="packing/no-such-receipt.json")),
            "does not name a file",
        ),
    }
    for name, (record, words) in cases.items():
        found = _problems(records, record)
        assert any(words in line for line in found), (name, found)
    regularized = [
        {
            "n": 130,
            "of": "T-259",
            "by": "[Yim certificates 2026-11-09]",
            "method": "T-259's certificate under one common translation",
            "side": "solved",
            "identity": {"basis": "source-claim"},
        }
    ]
    both = {**_restated(records, _item()), "regularizations": regularized}
    assert any("also a regularization" in line for line in _problems(records, both))


def test_the_register_records_the_restatements_option_d_settles(records: view.Records) -> None:
    """T-253, T-260, T-280 and T-281 restate their houses at every count, T-173 at 207;
    none improves on a case record there, so none is pending adoption or a current record,
    and a reply's result mapped to one is settled (`check_requests.RESTATED`)."""
    index = profile_records.load_record_index()
    every = {"T-253": 9, "T-260": 5, "T-280": 2, "T-281": 1}
    for ident, count in every.items():
        record = records.results[ident]
        assert len(check_standing.restated(record)) == count, ident
        assert check_standing.improvements(record, records) == [], ident
        assert view.standing(record, records) == view.SUPERSEDED, ident
        assert ident not in index.current_results, ident
        assert not record.get("regularizations"), ident
    assert check_standing.restated(records.results["T-173"]) == frozenset({207})
    register = check_requests.load_register()
    state = check_requests.result_state(
        {"key": "sub-print", "claim": "c", "register": ["T-260"]}, register
    )
    assert (state.state, state.settled) == (check_requests.RESTATED, True)
    # A new result under option D is no restatement: T-285 and T-286 are confirmed.
    for ident in ("T-285", "T-286"):
        assert not records.results[ident].get("restatements")
        assert (
            records.results[ident]["verification"],
            records.results[ident]["confirmation"],
        ) == (
            "V3",
            "C3",
        )
