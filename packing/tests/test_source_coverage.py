"""Selected overrides may come from any retained source, and every reparsed claim is held."""

from __future__ import annotations

import copy
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest
from jsonschema_rs import Draft202012Validator

from devtools import check_source_coverage as coverage_check
from sqpack.yamlio import safe_load


def _coverage() -> dict[str, Any]:
    def source(identifier: str, values: list[int]) -> dict[str, Any]:
        return {
            "id": identifier,
            "scope": {"n_values": values},
            "evidence": [f"E-{identifier}-report"],
        }

    return {
        "case_corpus": {"n_min": 1, "n_max": 10},
        "sources": [
            source("release", [5, 6]),
            source("repository", [5, 7]),
            source("superseded", [7]),
        ],
        "selected_overrides": [
            {"n": 6, "source_id": "release", "value": "2.9", "evidence": "E-release-report"},
            {
                "n": 5,
                "source_id": "repository",
                "value": "2.8",
                "evidence": "E-repository-report",
            },
            {
                "n": 7,
                "source_id": "repository",
                "value": "2.95",
                "evidence": "E-repository-report",
            },
        ],
        "superseded_reports": [
            {"n": 5, "source_id": "release", "value": "2.85", "superseded_by": "repository"},
            {"n": 7, "source_id": "superseded", "value": "2.97", "superseded_by": "repository"},
        ],
        "beyond_horizon_claims": [],
    }


KINGBIRD = {5: "2.9", 6: "3", 7: "3"}
CLAIMS = {
    "release": {5: "2.85", 6: "2.9"},
    "repository": {5: "2.8", 7: "2.95"},
    "superseded": {7: "2.97"},
}


def _errors(coverage: dict[str, Any], claims: dict[str, dict[int, str]] = CLAIMS) -> list[str]:
    return coverage_check.selection_errors(coverage, KINGBIRD, claims)


def test_overrides_from_several_sources_reconcile() -> None:
    assert _errors(_coverage()) == []


def test_an_override_must_print_what_its_source_prints() -> None:
    coverage = _coverage()
    coverage["selected_overrides"][1]["value"] = "2.81"
    assert any("repository prints 2.8" in error for error in _errors(coverage))


def _against_print(value: str, printed: str, houses: dict[int, str] | None = None) -> list[str]:
    """The errors of n = 6's override at `value` against a catalogue print of `printed`,
    the override's source keyed `[release]`, with `houses` the adopted houses' sources."""
    coverage = _coverage()
    coverage["sources"][0]["source_key"] = "[release]"
    claims = copy.deepcopy(CLAIMS)
    claims["release"][6] = value
    coverage["selected_overrides"][0]["value"] = value
    return coverage_check.selection_errors(coverage, {**KINGBIRD, 6: printed}, claims, houses)


@pytest.mark.parametrize("value", ["3", "3.5", "3.9999999999", "4"])
def test_an_integral_baseline_is_exact_and_refuses_anything_at_or_above_it(value: str) -> None:
    """An integral print is the catalogue's `s = k` or the `ceil(sqrt(n))` fallback, an
    exact side, so it orders every override, a house or not (review C4 of #661)."""
    for houses in (None, {6: "[release]"}):
        (error,) = _against_print(value, "3", houses)
        assert error == "selected override n=6 does not beat the catalogue baseline 3"
    assert _against_print("2.9999999999", "3") == []


@pytest.mark.parametrize(
    ("value", "outcome"),
    [
        # Below the print, the override beats it.
        ("2.9299999999", "beats"),
        # Inside the print's last-place unit nothing is decided: a decimal print is a
        # truncation or a rounding, as at n = 29, where T-195 lies 9.19e-15 above the
        # catalogue's 5.93383346267692 and inside T-009's box for the catalogue's own
        # packing (think-adgd).
        ("2.93", "undecided"),
        ("2.9399999999", "undecided"),
        # From the next unit on, the print shows the override to be larger.
        ("2.94", "loses"),
        ("2.9400000001", "loses"),
    ],
)
def test_a_decimal_print_leaves_its_last_unit_to_the_exact_house_selection(
    value: str, outcome: str
) -> None:
    """Inside the print's last-place unit an override stands only as the count's adopted
    house from its own source, which `select_houses` orders exactly against the verified
    ceiling; anywhere else the window lets nothing through (review C4 of #661)."""
    assert coverage_check.print_order(value, "2.93") == outcome
    alone = _against_print(value, "2.93")
    house = _against_print(value, "2.93", {6: "[release]"})
    other = _against_print(value, "2.93", {6: "[repository]"})
    if outcome == "beats":
        assert alone == house == other == []
    elif outcome == "undecided":
        assert house == []
        for errors in (alone, other):
            (error,) = errors
            assert "within one unit of the print's last place" in error
            assert "not the count's adopted house" in error
    else:
        for errors in (alone, house, other):
            assert errors == ["selected override n=6 does not beat the catalogue baseline 2.93"]


def test_the_catalogues_integral_baselines_are_read_as_exact() -> None:
    """The 177 integral baselines of the current capture refuse half a unit above them,
    where one unit of their written place would have admitted it: 18.7 at n = 308
    against 18 (review C4 of #661)."""
    coverage = safe_load(coverage_check.COVERAGE.read_text(encoding="utf-8"))
    corpus = coverage["case_corpus"]
    source = coverage_check.source_by_id(coverage, "kingbird-current")
    kingbird = coverage_check.parse_kingbird(
        coverage_check.ROOT / source["local"], corpus["n_min"], corpus["n_max"]
    )
    integral = {n: printed for n, printed in kingbird.items() if "." not in printed}
    assert len(integral) == 177
    assert kingbird[308] == "18"
    for n, printed in integral.items():
        assert coverage_check.print_order(f"{printed}.5", printed) == coverage_check.LOSES, n
        assert coverage_check.print_order(printed, printed) == coverage_check.LOSES, n
    assert coverage_check.print_order("18.7", kingbird[308]) == coverage_check.LOSES


def test_a_superseded_report_must_lose_to_the_selected_source() -> None:
    coverage = _coverage()
    coverage["superseded_reports"][0]["value"] = "2.75"
    claims = copy.deepcopy(CLAIMS)
    claims["release"][5] = "2.75"
    assert any("is not beaten" in error for error in _errors(coverage, claims))
    coverage = _coverage()
    coverage["superseded_reports"][0]["superseded_by"] = "superseded"
    assert any("not the selected source" in error for error in _errors(coverage))


def _catalogue_overtakes_the_release() -> dict[str, Any]:
    """The release's n = 6 report, with no override selected and a catalogue below it."""
    coverage = _coverage()
    coverage["sources"].append(
        {
            "id": "catalogue",
            "scope": {"n_min": 1, "n_max": 10},
            "evidence": [],
            "disposition": "baseline-current",
        }
    )
    del coverage["selected_overrides"][0]
    coverage["superseded_reports"].append(
        {"n": 6, "source_id": "release", "value": "2.9", "superseded_by": "catalogue"}
    )
    return coverage


def test_a_catalogue_capture_that_overtakes_a_release_supersedes_it() -> None:
    # n = 69 on 2026-10-05: no override is selected any more, so the baseline is the
    # report, and the release's claim is held as superseded by it.
    baseline = {**KINGBIRD, 6: "2.88"}
    coverage = _catalogue_overtakes_the_release()
    assert coverage_check.selection_errors(coverage, baseline, CLAIMS) == []
    behind = coverage_check.selection_errors(coverage, {**KINGBIRD, 6: "2.9"}, CLAIMS)
    assert behind == [
        "superseded report n=6 from release is not beaten by the catalogue baseline 2.9"
    ]
    # Only the baseline source may stand in for a selected override.
    coverage["superseded_reports"][-1]["superseded_by"] = "repository"
    assert any(
        "not the selected source" in error
        for error in coverage_check.selection_errors(coverage, baseline, CLAIMS)
    )


def test_every_reparsed_claim_is_accounted_for() -> None:
    coverage = _coverage()
    del coverage["superseded_reports"][1]
    assert any("unaccounted [7]" in error for error in _errors(coverage))


def test_an_override_outside_its_sources_scope_is_refused() -> None:
    coverage = _coverage()
    coverage["selected_overrides"][2]["n"] = 8
    assert any("outside repository's scope" in error for error in _errors(coverage))


def test_both_claims_record_shapes_are_reparsed(tmp_path: Path) -> None:
    release = tmp_path / "results.json"
    release.write_text(json.dumps({"results": [{"n": 5, "offered_side": "2.85"}]}))
    assert coverage_check.load_claims(release) == {5: "2.85"}
    acquisition = tmp_path / "sources.json"
    acquisition.write_text(
        json.dumps(
            {
                "format": coverage_check.ACQUISITION_FORMAT,
                "sources": [{"cases": [{"n": 7, "side": "2.95"}]}],
            }
        )
    )
    assert coverage_check.load_claims(acquisition) == {7: "2.95"}


#: A count the current capture moved below its record: the earlier capture printed 3.
PENDING = {
    "n": 6,
    "record_value": "2.9",
    "catalogue_value": "2.85",
    "capture": coverage_check.INTAKE_CAPTURE_DATE,
    "reason": "a result the register holds first",
    "bead": "think-ab12",
    "recorded": "2026-09-30",
}
CURRENT = {5: "2.9", 6: "2.85", 7: "3"}
EARLIER = {5: "2.9", 6: "3", 7: "3"}
BLOCKER = {
    "kind": "source-evidence",
    "detail": "The catalogue now prints 2.85; see pending_catalogue_intake.",
}
CASES = {6: {"reported_upper_bound": {"value": "2.9"}, "blockers": [BLOCKER]}}


def _pending_errors(**change: str) -> list[str]:
    entry = {**PENDING, **change}
    return coverage_check.pending_intake_errors([entry], CURRENT, EARLIER, CASES)


def test_a_declared_pending_intake_that_both_captures_bear_out_passes() -> None:
    assert _pending_errors() == []


def test_a_pending_intake_must_name_the_side_the_current_capture_prints() -> None:
    errors = _pending_errors(catalogue_value="2.84")
    assert "the current capture prints 2.85, not the declared 2.84" in errors[0]
    # The record's blocker names 2.85, so it no longer bears out the declaration either.
    assert "blocker naming pending_catalogue_intake and the side 2.84" in errors[1]


def test_a_pending_intake_is_refused_once_the_record_has_moved() -> None:
    """The declaration exists to be removed; an intake that landed leaves it stale."""
    moved = {6: {"reported_upper_bound": {"value": "2.85"}, "blockers": [BLOCKER]}}
    (error,) = coverage_check.pending_intake_errors([PENDING], CURRENT, EARLIER, moved)
    assert "remove the declaration once the intake lands" in error


def test_the_record_itself_must_say_it_trails_the_catalogue_and_only_when_declared() -> None:
    """The register has no reader view, so the record carries the pending state too."""
    silent = {6: {"reported_upper_bound": {"value": "2.9"}, "blockers": []}}
    (error,) = coverage_check.pending_intake_errors([PENDING], CURRENT, EARLIER, silent)
    assert "carries no source-evidence blocker naming pending_catalogue_intake" in error

    stray = {**CASES, 5: {"reported_upper_bound": {"value": "2.9"}, "blockers": [BLOCKER]}}
    (error,) = coverage_check.pending_intake_errors([PENDING], CURRENT, EARLIER, stray)
    assert error.startswith("n=5: the record declares a pending catalogue intake")


def test_a_pending_intake_needs_a_capture_that_changed_and_a_side_that_beats() -> None:
    same = coverage_check.pending_intake_errors([PENDING], CURRENT, CURRENT, CASES)
    assert same == [
        "pending catalogue intake n=6: both captures print 2.85; nothing is pending"
    ]
    higher = {6: "2.95"}
    beaten = coverage_check.pending_intake_errors(
        [{**PENDING, "catalogue_value": "2.95"}], higher, EARLIER, CASES
    )
    assert beaten[0] == "pending catalogue intake n=6: 2.95 does not beat the record"
    assert "the one retained earlier capture" in _pending_errors(capture="2026-01-01")[0]


def test_a_pending_intake_names_the_bead_that_owns_it_and_the_day_it_was_deferred() -> None:
    """The three of 2026-09-30 named no owner, and nothing listed them for five days."""
    orphan = {key: value for key, value in PENDING.items() if key not in {"bead", "recorded"}}
    errors = coverage_check.pending_intake_errors([orphan], CURRENT, EARLIER, CASES)
    assert errors == [
        (
            "pending catalogue intake n=6 names no bead (none); a deferral names the open "
            "bead that owns the intake"
        ),
        "pending catalogue intake n=6 records no date (none) it was deferred on",
    ]
    assert "names no bead (bd-12)" in _pending_errors(bead="bd-12")[0]
    assert "records no date (last week)" in _pending_errors(recorded="last week")[0]


def test_the_schema_requires_an_owner_on_every_deferral() -> None:
    """The same rule in the schema, so `validate_schemas` refuses it on its own."""
    schema = safe_load(
        coverage_check.COVERAGE.with_name("source-coverage.schema.yaml").read_text()
    )
    validator = Draft202012Validator(schema)
    document = safe_load(coverage_check.COVERAGE.read_text(encoding="utf-8"))
    document.pop("softschema")
    document["pending_catalogue_intake"] = [dict(PENDING)]
    assert validator.is_valid(document)
    for key in ("bead", "recorded"):
        document["pending_catalogue_intake"] = [
            {name: value for name, value in PENDING.items() if name != key}
        ]
        assert not validator.is_valid(document), key
    conflict = {
        "n": 400,
        "source_id": "kingbird-current",
        "claim": "upper-bound",
        "value": "20.5",
        "assurance": "reported",
        "disposition": "deferred-conflict",
    }
    document["pending_catalogue_intake"] = []
    document["beyond_horizon_claims"] = [conflict]
    assert not validator.is_valid(document)
    document["beyond_horizon_claims"] = [{**conflict, "bead": "think-ab12"}]
    assert validator.is_valid(document)


def test_the_recorded_coverage_reconciles() -> None:
    assert coverage_check.main() == 0


def _named_houses() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """n = 7 moved twice: T-800 adopted on 11 October, then T-900 on 12 October."""
    coverage: dict[str, Any] = {
        "sources": [
            {"id": "older", "source_key": "[older]"},
            {"id": "earlier", "source_key": "[earlier]"},
            {"id": "later", "source_key": "[later]"},
            {"id": "later-in-corpus", "source_key": "[later]"},
            {"id": "sibling", "source_key": "[sibling]"},
        ],
        "selected_overrides": [
            {
                "n": 7,
                "source_id": "later-in-corpus",
                "reason": "The smallest exact side ..., adopted on 2026-10-12 (T-900).",
            }
        ],
        "superseded_reports": [
            {
                "n": 7,
                "source_id": "older",
                "reason": (
                    "The house until 2026-10-11; its certificate stays retained and "
                    "verified, and T-900's exact side is smaller."
                ),
                "superseded_by": "later-in-corpus",
            },
            {
                "n": 7,
                "source_id": "earlier",
                "reason": (
                    "The house from 2026-10-11 until 2026-10-12; its certificate stays "
                    "retained and verified, and T-900's exact side is smaller."
                ),
                "superseded_by": "later-in-corpus",
            },
            {
                "n": 7,
                "source_id": "sibling",
                "reason": (
                    "A certificate of the same release that no register entry cites; its "
                    "exact side equals the house adopted here on 2026-10-12, which "
                    "T-900's registered certificate holds."
                ),
                "superseded_by": "later-in-corpus",
            },
        ],
    }
    results = [
        {"id": "T-800", "attribution": {"source_keys": ["[earlier]"]}},
        {"id": "T-900", "attribution": {"source_keys": ["[later]"]}},
    ]
    return coverage, results


def test_a_reason_that_names_the_house_names_the_one_that_supersedes_it() -> None:
    """Both ways a reason names its house hold to `superseded_by`, the source key matched
    through any of the source's coverage entries."""
    coverage, results = _named_houses()
    assert coverage_check.house_reason_errors(coverage, results) == []
    unnamed = copy.deepcopy(coverage)
    unnamed["superseded_reports"][0]["reason"] = "Grid."
    assert coverage_check.house_reason_errors(unnamed, results) == []


def test_a_reason_left_naming_the_earlier_house_is_refused() -> None:
    """The stale rows of #518 (A1) and #553 (B3): the count moved again, the row was
    re-pointed at the new house, and its reason still names the old one."""
    coverage, results = _named_houses()
    stale = copy.deepcopy(coverage)
    stale["superseded_reports"][0]["reason"] = (
        "The house until 2026-10-11; its certificate stays retained and verified, and "
        "T-800's exact side is smaller."
    )
    (error,) = coverage_check.house_reason_errors(stale, results)
    assert "n=7 from older names T-800" in error
    assert "later-in-corpus, which is not T-800's source" in error
    dated = copy.deepcopy(coverage)
    dated["superseded_reports"][2]["reason"] = (
        "A certificate of the same release that no register entry cites; the side it prints "
        "is above the house adopted here on 2026-10-11."
    )
    (error,) = coverage_check.house_reason_errors(dated, results)
    assert "names the house adopted on 2026-10-11" in error
    assert "was adopted on 2026-10-12" in error
    unadopted = copy.deepcopy(coverage)
    unadopted["selected_overrides"][0]["reason"] = "Selected by hand."
    errors = coverage_check.house_reason_errors(unadopted, results)
    assert errors == [
        (
            "superseded report n=7 from sibling names the house adopted on 2026-10-12, but "
            "later-in-corpus, which supersedes it, was adopted on no day"
        )
    ]


def _dated_source(identifier: str, day: str | None, values: list[int]) -> dict[str, Any]:
    return {
        "id": identifier,
        "scope": {"n_values": values},
        "evidence": [f"E-{identifier}-report"],
        "source_date": day,
        "claims_record": f"resources/web/{identifier}/acquisition/sources.json",
    }


def _row(
    source_id: str, n: int, value: str, superseded_by: str | None = None
) -> dict[str, Any]:
    row: dict[str, Any] = {
        "n": n,
        "source_id": source_id,
        "claim": "upper-bound",
        "value": value,
        "assurance": "reported",
        "disposition": "tracked-outside-case-corpus",
    }
    if superseded_by is not None:
        row |= {"disposition": "superseded", "superseded_by": superseded_by}
    return row


#: Three dated reports of one upper bound at n = 400, each beating the last by less than
#: a binary64 value can show, and two at n = 401.
FIRST_SIDE, SECOND_SIDE, THIRD_SIDE = (
    "20.00000000000000000002",
    "20.00000000000000000001",
    "20.0",
)


def _beyond() -> tuple[dict[str, Any], dict[str, dict[int, str]]]:
    coverage = _coverage()
    coverage["sources"] += [
        _dated_source("first", "2026-10-01", [400, 401]),
        _dated_source("second", "2026-10-02", [400]),
        _dated_source("third", "2026-10-02", [400]),
        _dated_source("late", "2026-10-03", [401]),
    ]
    coverage["beyond_horizon_claims"] = [
        _row("first", 400, FIRST_SIDE, superseded_by="second"),
        _row("second", 400, SECOND_SIDE, superseded_by="third"),
        _row("third", 400, THIRD_SIDE),
        _row("first", 401, "20.1", superseded_by="late"),
        _row("late", 401, "20.05"),
    ]
    claims = {
        **CLAIMS,
        "first": {400: FIRST_SIDE, 401: "20.1"},
        "second": {400: SECOND_SIDE},
        "third": {400: THIRD_SIDE},
        "late": {401: "20.05"},
    }
    return coverage, claims


def _beyond_errors(coverage: dict[str, Any], claims: dict[str, dict[int, str]]) -> list[str]:
    return coverage_check.beyond_horizon_errors(coverage, claims)[0]


def test_dated_beyond_horizon_rows_reconcile_by_exact_comparison() -> None:
    """Each successor beats its predecessor below binary64 resolution, and is accepted."""
    assert float(FIRST_SIDE) == float(SECOND_SIDE) == float(THIRD_SIDE)
    coverage, claims = _beyond()
    assert _errors(coverage, claims) == []
    errors, inventory = coverage_check.beyond_horizon_errors(coverage, claims)
    assert errors == []
    assert inventory == {"first": {400, 401}, "second": {400}, "third": {400}, "late": {401}}
    current = coverage_check.current_beyond_horizon(coverage)
    assert {n: row["source_id"] for n, row in current.items()} == {400: "third", 401: "late"}


def test_the_current_row_is_found_wherever_it_is_listed_and_never_chosen() -> None:
    coverage, claims = _beyond()
    rows = coverage["beyond_horizon_claims"]
    # Each count's current row listed before the rows it supersedes.
    rows.insert(0, rows.pop(2))
    rows.insert(0, rows.pop())
    assert [(row["n"], row["source_id"]) for row in rows[:3]] == [
        (401, "late"),
        (400, "third"),
        (400, "first"),
    ]
    assert _beyond_errors(coverage, claims) == []
    current = coverage_check.current_beyond_horizon(coverage)
    assert {n: row["source_id"] for n, row in current.items()} == {400: "third", 401: "late"}
    rows[2] = _row("first", 400, FIRST_SIDE)
    with pytest.raises(
        ValueError, match=r"n=400 has more than one current row \(third, first\)"
    ):
        coverage_check.current_beyond_horizon(coverage)


def test_a_beyond_horizon_row_is_unique_by_count_and_source() -> None:
    coverage, claims = _beyond()
    coverage["beyond_horizon_claims"].append(_row("third", 400, THIRD_SIDE))
    assert _beyond_errors(coverage, claims) == [
        "beyond-horizon n=400 from third is listed twice; a count has one row per source"
    ]


def test_a_count_has_at_most_one_current_row() -> None:
    coverage, claims = _beyond()
    coverage["beyond_horizon_claims"][0] = _row("first", 400, FIRST_SIDE)
    assert _beyond_errors(coverage, claims) == [
        (
            "beyond-horizon n=400 has 2 current rows (first, third); a count has at most one, "
            "and each earlier report names the row that supersedes it"
        )
    ]


def test_only_a_superseded_row_names_a_successor_and_it_always_does() -> None:
    coverage, claims = _beyond()
    del coverage["beyond_horizon_claims"][1]["superseded_by"]
    coverage["beyond_horizon_claims"][2]["superseded_by"] = "second"
    errors = _beyond_errors(coverage, claims)
    assert "beyond-horizon n=400 from second is superseded but names no successor" in errors
    assert (
        "beyond-horizon n=400 from third names successor second but is not superseded" in errors
    )


def test_a_successor_is_a_row_at_the_same_count() -> None:
    coverage, claims = _beyond()
    coverage["beyond_horizon_claims"][1]["superseded_by"] = "late"
    assert _beyond_errors(coverage, claims) == [
        (
            "beyond-horizon n=400 from second names successor late, which has no row at "
            "n=400; its rows are at n=[401]"
        )
    ]
    coverage["beyond_horizon_claims"][1]["superseded_by"] = "unknown"
    assert _beyond_errors(coverage, claims) == [
        ("beyond-horizon n=400 from second names successor unknown, which has no row at n=400")
    ]


def test_a_successor_is_dated_no_earlier() -> None:
    coverage, claims = _beyond()
    coverage["sources"][-2]["source_date"] = "2026-09-30"
    assert _beyond_errors(coverage, claims) == [
        (
            "beyond-horizon n=400 from second is dated 2026-10-02, after its successor from "
            "third, dated 2026-09-30"
        )
    ]
    coverage["sources"][-2]["source_date"] = None
    assert _beyond_errors(coverage, claims) == [
        (
            "beyond-horizon n=400 from second: third has no source_date, and a supersession "
            "orders dated reports"
        )
    ]


def test_a_successor_is_strictly_better_compared_exactly() -> None:
    coverage, claims = _beyond()
    # Equal to its predecessor, and then above it: by less than binary64 can show.
    for value in (SECOND_SIDE, "20.000000000000000000015"):
        coverage["beyond_horizon_claims"][2]["value"] = value
        claims["third"][400] = value
        assert _beyond_errors(coverage, claims) == [
            (
                f"beyond-horizon n=400 from second: {SECOND_SIDE} is not strictly beaten by "
                f"{value} from third, compared exactly"
            )
        ]


def test_a_lower_bound_is_beaten_from_below_and_an_exact_value_never_is() -> None:
    coverage, claims = _beyond()
    rows = coverage["beyond_horizon_claims"]
    for row in rows[:3]:
        row["claim"] = "lower-bound"
    # Each later side is smaller, which loses as a lower bound.
    assert _beyond_errors(coverage, claims) == [
        (
            f"beyond-horizon n=400 from {owner}: {earlier} is not strictly beaten by "
            f"{later} from {successor}, compared exactly"
        )
        for owner, earlier, successor, later in (
            ("first", FIRST_SIDE, "second", SECOND_SIDE),
            ("second", SECOND_SIDE, "third", THIRD_SIDE),
        )
    ]
    for row, value in zip(rows[:3], (THIRD_SIDE, SECOND_SIDE, FIRST_SIDE), strict=True):
        row["value"] = value
        claims[row["source_id"]][400] = value
    assert _beyond_errors(coverage, claims) == []
    # A lower bound, too, must be beaten strictly: an equal later report does not.
    rows[2]["value"] = claims["third"][400] = SECOND_SIDE
    assert _beyond_errors(coverage, claims) == [
        (
            f"beyond-horizon n=400 from second: {SECOND_SIDE} is not strictly beaten by "
            f"{SECOND_SIDE} from third, compared exactly"
        )
    ]
    rows[2]["value"] = claims["third"][400] = FIRST_SIDE
    rows[2]["claim"] = "upper-bound"
    assert _beyond_errors(coverage, claims) == [
        (
            "beyond-horizon n=400 from second claims lower-bound, and its successor from "
            "third claims upper-bound"
        )
    ]
    for row in rows[:3]:
        row["claim"] = "exact-value"
    message = (
        "an exact-value claim is never superseded; a later report that differs from it "
        "conflicts with it, and one that agrees adds nothing"
    )
    assert _beyond_errors(coverage, claims) == [
        f"beyond-horizon n=400 from {owner}: {message}" for owner in ("first", "second")
    ]
    # Equal exact values are refused the same way.
    for row in rows[:3]:
        row["value"] = claims[row["source_id"]][400] = THIRD_SIDE
    assert _beyond_errors(coverage, claims) == [
        f"beyond-horizon n=400 from {owner}: {message}" for owner in ("first", "second")
    ]


def test_a_row_never_names_itself_as_its_successor() -> None:
    """Longer cycles need no check of their own: a cycle of strictly better links would
    make some value strictly better than itself, so the strictness rule refuses one."""
    coverage, claims = _beyond()
    rows = coverage["beyond_horizon_claims"]
    rows[0]["superseded_by"] = "first"
    assert _beyond_errors(coverage, claims) == [
        "beyond-horizon n=400 from first names itself as its successor"
    ]


def test_a_dated_row_keeps_its_sources_facts_byte_for_byte() -> None:
    coverage, claims = _beyond()
    coverage["beyond_horizon_claims"][3]["value"] = "20.10"
    assert _beyond_errors(coverage, claims) == [
        (
            "beyond-horizon n=401 from first reads '20.10', not '20.1' as its source prints "
            "it; a dated row keeps its source's facts byte for byte"
        )
    ]
    coverage["beyond_horizon_claims"][3]["value"] = "20.2"
    assert _beyond_errors(coverage, claims) == [
        "beyond-horizon n=401 from first: first prints 20.1, the inventory says 20.2"
    ]


def test_every_beyond_horizon_row_names_a_source_with_a_claims_record() -> None:
    """A row is held to what its source prints, so its source must retain a record."""
    coverage, claims = _beyond()
    # A caller may pass only the claims it loaded; what decides is the source's record.
    del claims["late"]
    assert _beyond_errors(coverage, claims) == []
    del coverage["sources"][-1]["claims_record"]
    assert _beyond_errors(coverage, claims) == [
        (
            "beyond-horizon n=401 from late: late declares no claims record, so the row "
            "is compared with nothing its source prints"
        )
    ]


def test_the_schema_names_a_successor_exactly_when_a_row_is_superseded() -> None:
    schema = safe_load(
        coverage_check.COVERAGE.with_name("source-coverage.schema.yaml").read_text()
    )
    validator = Draft202012Validator(schema)
    document = safe_load(coverage_check.COVERAGE.read_text(encoding="utf-8"))
    document.pop("softschema")
    later = {**_row("later", 400, "20.0"), "bead": "think-ab12"}
    earlier = {**_row("earlier", 400, "20.1", superseded_by="later"), "bead": "think-ab12"}
    document["beyond_horizon_claims"] = [earlier, later]
    assert validator.is_valid(document)
    document["beyond_horizon_claims"] = [
        {key: value for key, value in earlier.items() if key != "superseded_by"},
        later,
    ]
    assert not validator.is_valid(document)
    document["beyond_horizon_claims"] = [earlier, {**later, "superseded_by": "earlier"}]
    assert not validator.is_valid(document)


def _above(row: dict[str, Any], construction: str = "19 + 1/2*sqrt(2)") -> dict[str, Any]:
    """A row marked above a classical construction (`ABOVE_CONSTRUCTION`)."""
    kept = {key: value for key, value in row.items() if key != "superseded_by"}
    return kept | {
        "disposition": coverage_check.ABOVE_CONSTRUCTION,
        "construction": construction,
    }


def test_a_row_above_a_classical_construction_is_kept_and_holds_no_count() -> None:
    """The owner's answer of 23 October 2026 on #613 (think-8krd): Göbel's construction is
    an earlier report, so a row above it stays listed as its source printed it, holds no
    count and names no successor, and a count may then have no current row."""
    coverage, claims = _beyond()
    coverage["sources"].append(_dated_source("over", "2026-10-01", [369]))
    coverage["beyond_horizon_claims"].append(_above(_row("over", 369, "19.740417287556077")))
    claims = {**claims, "over": {369: "19.740417287556077"}}
    assert _beyond_errors(coverage, claims) == []
    assert 369 not in coverage_check.current_beyond_horizon(coverage)
    rows = coverage["beyond_horizon_claims"]
    rows[-1] = _above(rows[-1], "19 + 1/2*sqrt(3)")
    rows.append(_above(_row("late", 401, "20.05")))
    rows[3] = _row("first", 401, "20.1", superseded_by="late")
    assert _beyond_errors(coverage, claims) == [
        (
            "beyond-horizon n=369 from over states no construction p + q*sqrt(2), only "
            "'19 + 1/2*sqrt(3)'"
        ),
        "beyond-horizon n=401 from late is listed twice; a count has one row per source",
    ]
    rows.pop()
    rows[-1] = _above(_row("over", 369, "19.740417287556077"), "20 + 1/2*sqrt(2)")
    rows[4] = _above(rows[4], "19 + 1/2*sqrt(2)")
    assert _beyond_errors(coverage, claims) == [
        (
            "beyond-horizon n=369 from over: 19.740417287556077 is not above its "
            "construction 20 + 1/2*sqrt(2)"
        ),
        (
            "beyond-horizon n=401 from first names successor late, whose row is above a "
            "classical construction and holds no count"
        ),
    ]


def test_a_construction_is_compared_exactly() -> None:
    """``p + q sqrt 2`` against a rational, by exact sign; no rational equals it."""
    sign = coverage_check.construction_sign
    assert sign(Fraction("19.707106781187"), "19 + 1/2*sqrt(2)") == 1
    assert sign(Fraction("19.707106781186"), "19 + 1/2*sqrt(2)") == -1
    assert sign(Fraction(19), "19 + 0*sqrt(2)") == 0
    assert sign(Fraction(19), "19 - 1/2*sqrt(2)") is None


def test_the_schema_names_a_construction_exactly_when_a_row_is_above_one() -> None:
    schema = safe_load(
        coverage_check.COVERAGE.with_name("source-coverage.schema.yaml").read_text()
    )
    validator = Draft202012Validator(schema)
    document = safe_load(coverage_check.COVERAGE.read_text(encoding="utf-8"))
    document.pop("softschema")
    above = {**_above(_row("over", 369, "19.75")), "bead": "think-ab12"}
    document["beyond_horizon_claims"] = [above]
    assert validator.is_valid(document)
    document["beyond_horizon_claims"] = [{**above, "construction": "19 + sqrt(2)/2"}]
    assert not validator.is_valid(document)
    plain = {**_row("over", 369, "19.75"), "construction": "19 + 1/2*sqrt(2)"}
    document["beyond_horizon_claims"] = [plain]
    assert not validator.is_valid(document)
    document["beyond_horizon_claims"] = [
        {key: value for key, value in above.items() if key != "construction"}
    ]
    assert not validator.is_valid(document)


def _live_register() -> tuple[
    dict[str, Any], list[dict[str, Any]], dict[str, Any], dict[str, Any]
]:
    """The live coverage record, register, evidence index and bibliography."""
    coverage = safe_load(coverage_check.COVERAGE.read_text(encoding="utf-8"))
    results = safe_load(coverage_check.RESULTS.read_text(encoding="utf-8"))["results"]
    evidence = {
        entry["id"]: entry
        for entry in safe_load(coverage_check.EVIDENCE.read_text(encoding="utf-8"))["evidence"]
    }
    bibliography = {
        source["key"]: source
        for source in safe_load(coverage_check.BIBLIOGRAPHY.read_text(encoding="utf-8"))[
            "sources"
        ]
    }
    return coverage, results, evidence, bibliography


def test_every_recent_source_the_register_cites_has_a_coverage_source() -> None:
    """Stage 3 records a reported claim with a coverage entry that cites it; the import
    review of 2026-10-01 found two wand125 keys without one, and the gate passed."""
    coverage, results, evidence, bibliography = _live_register()
    assert (
        coverage_check.register_source_errors(coverage, results, evidence, bibliography) == []
    )


def test_a_cited_recent_source_with_no_coverage_source_is_refused() -> None:
    """The negative control: the live record with the tools' coverage source taken out."""
    coverage, results, evidence, bibliography = _live_register()
    coverage["sources"] = [
        source
        for source in coverage["sources"]
        if source["source_key"] != "[wand125 tools 2026]"
    ]
    assert coverage_check.register_source_errors(coverage, results, evidence, bibliography) == [
        (
            "[wand125 tools 2026], dated 2026-09-29 and cited by T-058, T-059, has no coverage "
            "source: none carries the key or cites evidence that does"
        )
    ]


def test_a_coverage_source_that_cites_a_keys_evidence_holds_the_key() -> None:
    """The Kingbird catalogue's entry holds each finder's own key by citing its evidence:
    without those citations, Chang's n = 83 key is unheld."""
    coverage, results, evidence, bibliography = _live_register()
    (kingbird,) = [s for s in coverage["sources"] if s["id"] == "kingbird-current"]
    kingbird["evidence"] = [
        ref for ref in kingbird["evidence"] if not ref.startswith("E-n083-")
    ]
    (problem,) = coverage_check.register_source_errors(
        coverage, results, evidence, bibliography
    )
    assert problem.startswith("[Chang n83 2026-09-24], dated 2026-09-24 and cited by T-089,")


#: The key of Burns's and Massaccesi's August 2026 posts, spelled with its en dash.
BURNS_MASSACCESI = "[Burns\N{EN DASH}Massaccesi n17]"


def test_a_source_dated_before_the_project_began_needs_no_coverage_source() -> None:
    """The register's rule for results by others starts on 22 August 2026; Nagamochi 2005
    and the Burns and Massaccesi posts of August are cited and are not coverage sources."""
    coverage, results, evidence, bibliography = _live_register()
    keys = {
        key
        for record in results
        for key in coverage_check.register_source_keys(record, evidence)
    }
    held = {source["source_key"] for source in coverage["sources"]}
    assert {"[Nagamochi 2005]", BURNS_MASSACCESI} <= keys - held
    assert bibliography[BURNS_MASSACCESI]["dated"] == "2026-08-21"
    bibliography[BURNS_MASSACCESI]["dated"] = "2026-08-22"
    (problem,) = coverage_check.register_source_errors(
        coverage, results, evidence, bibliography
    )
    assert problem.startswith(f"{BURNS_MASSACCESI}, dated 2026-08-22")
