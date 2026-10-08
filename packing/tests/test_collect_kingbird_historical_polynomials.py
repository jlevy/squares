"""The retained history pages are a reproducible, algebraically checked corpus."""

from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from devtools.collect_kingbird_historical_polynomials import (
    DEFAULT_OUTPUT,
    HistoricalPolynomialError,
    collect_source,
    read_latex_integer_polynomial,
    validate,
    verify_source_identity,
)


def test_reads_a_printed_integer_polynomial_without_accepting_an_extension() -> None:
    assert read_latex_integer_polynomial("s^4-20s^3+151s^2-468s+12=0") == (
        1,
        -20,
        151,
        -468,
        12,
    )
    assert read_latex_integer_polynomial("6208s^8-533120s^7+891886272841=0") == (
        6208,
        -533120,
        0,
        0,
        0,
        0,
        0,
        0,
        891886272841,
    )
    assert read_latex_integer_polynomial("s^2 - 5s + 6 = 0") == (1, -5, 6)
    with pytest.raises(HistoricalPolynomialError, match="not a printed integer"):
        read_latex_integer_polynomial("s^2-(2+3\\sqrt{2})s+1=0")


def test_the_bounded_retained_corpus_decodes_every_comparison_row() -> None:
    document = collect_source()
    assert document["scope"]["comparison_equation_rows"] == 189
    assert document["scope"]["decoded_source_rows"] == 201
    assert document["scope"]["unique_polynomial_side_pairs"] == 182
    assert document["scope"]["unparsed_source_rows"] == 0
    assert not document["unparsed_rows"]
    assert max(entry["n"] for entry in document["entries"]) == 2135
    assert {
        (entry["historical_side"], entry["degree"])
        for entry in document["entries"]
        if entry["n"] == 71
    } == {("8.96326750850139", 8), ("8.96028765944389", 4)}
    assert {
        (entry["historical_side"], entry["degree"])
        for entry in document["entries"]
        if entry["n"] == 11
    } >= {("3.87708359002281", 8)}
    n259 = {
        entry["historical_side"]: entry for entry in document["entries"] if entry["n"] == 259
    }
    assert n259["16.60255251726339"]["source_statuses"] == ["invalid"]
    assert n259["16.60257141234448"]["source_statuses"] == ["fixed"]
    assert n259["16.60255251726339"]["attribution"]["date_mentions"] == ["December 2024"]
    assert n259["16.60257141234448"]["attribution"]["date_mentions"] == ["January 2026"]
    assert all(
        occurrence["degree_marker_matches"]
        for entry in document["entries"]
        for occurrence in entry["occurrences"]
    )


@pytest.mark.slow
def test_the_saved_corpus_rebuilds_from_source_and_exact_checks() -> None:
    saved = json.loads(Path(DEFAULT_OUTPUT).read_text(encoding="utf-8"))
    verify_source_identity(saved)
    rebuilt = collect_source()
    validate(rebuilt, None)
    assert rebuilt == saved
    assert sum(entry["validation"]["status"] == "verified" for entry in saved["entries"]) == 182
    assert all(
        entry["validation"]["status"] == "verified"
        for entry in saved["entries"]
        if entry["n"] == 71
    )


@pytest.mark.parametrize("mutation", ["flag", "equation", "omitted-row"])
def test_source_identity_refuses_mutated_source_facts(mutation: str) -> None:
    saved = json.loads(Path(DEFAULT_OUTPUT).read_text(encoding="utf-8"))
    changed = copy.deepcopy(saved)
    if mutation == "flag":
        entry = next(
            item
            for item in changed["entries"]
            if item["n"] == 259 and item["historical_side"] == "16.60255251726339"
        )
        entry["occurrences"][0]["source_flags"] = []
    elif mutation == "equation":
        changed["entries"][0]["occurrences"][0]["printed_equation"] += "+1"
    else:
        changed["entries"].pop()
    with pytest.raises(HistoricalPolynomialError, match="source identity differs"):
        verify_source_identity(changed)


def test_source_identity_ignores_generated_relationships_and_checks() -> None:
    saved = json.loads(Path(DEFAULT_OUTPUT).read_text(encoding="utf-8"))
    saved["entries"][0]["relationship_to_current"] = {"status": "changed"}
    saved["entries"][0]["validation"] = {"status": "changed"}
    verify_source_identity(saved)


def test_thematic_attribution_does_not_cross_into_neighboring_polynomials() -> None:
    document = collect_source()
    rows = {entry["degree"]: entry for entry in document["entries"] if entry["n"] == 71}
    assert rows[8]["attribution"]["date_mentions"] == ["October 2005"]
    assert rows[4]["attribution"]["date_mentions"] == ["April 2014"]
    assert all("Cantrell" not in text for text in rows[4]["attribution"]["source_text"])
    assert all("DeVincentis" not in text for text in rows[8]["attribution"]["source_text"])
