"""Distinct results and reviewed credit spans have separate counting contracts."""

from __future__ import annotations

from dataclasses import replace
from typing import Any

import pytest

from devtools.result_credit import PROJECT_AUTHOR_ORIGIN
from devtools.site_tallies import (
    person_credit_stats,
    project_credit_count,
    render_tally,
    tally_results,
    years_active,
)
from sqpack.contributor_occurrences import CreditOccurrence, CreditOrigin

BIBLIOGRAPHY = "packing/resources/bibliography.yaml"
REGISTER = "packing/frontier/results.yaml"


def occurrence(
    path: str,
    key: str,
    field: str = "/credit",
    *,
    person: str = "person",
    disposition: str = "resolved",
    role: str = "credited-contributor",
) -> CreditOccurrence:
    return CreditOccurrence(
        CreditOrigin(path, key, field),
        "Person",
        0,
        6,
        "Person",
        role,
        disposition,
        person if disposition == "resolved" else None,
        ("byline",) if disposition == "resolved" else (),
    )


def test_person_joins_multiple_credit_sources_once_and_counts_reviewed_spans() -> None:
    records: list[dict[str, Any]] = [
        {"id": "T-1", "attribution": {"source_keys": ["source-a", "source-b"]}},
        {"id": "T-2", "attribution": {"source_keys": ["source-a"]}},
        {"id": "T-3", "attribution": {"source_keys": ["other"]}},
    ]
    first = occurrence(BIBLIOGRAPHY, "source-a")
    spans = [
        first,
        replace(first, note="A second copy of the same reviewed span."),
        occurrence(BIBLIOGRAPHY, "source-b", "/authors/0", role="source-author"),
        occurrence(REGISTER, "T-1", "/builds_on/credit/0", role="prerequisite"),
        occurrence(BIBLIOGRAPHY, "unused"),
        occurrence(BIBLIOGRAPHY, "other", disposition="unresolved"),
        occurrence(BIBLIOGRAPHY, "other", person="another-person"),
    ]
    stats = person_credit_stats("person", spans, records)
    assert stats.results == ("T-1", "T-2")
    assert stats.credits == 4


def test_case_and_evidence_lineage_mentions_do_not_infer_result_credits() -> None:
    records: list[dict[str, Any]] = [
        {
            "id": "T-1",
            "n": [11],
            "attribution": {"source_keys": ["other"]},
            "evidence": [{"source_key": "lineage"}],
        },
        {"id": "T-2", "builds_on": {"source_keys": ["lineage"]}},
    ]
    spans = [
        occurrence("packing/frontier/n-011.md", "11", "/found_by/0"),
        occurrence(BIBLIOGRAPHY, "lineage"),
        occurrence(REGISTER, "unknown-result"),
    ]
    stats = person_credit_stats("person", spans, records)
    assert stats.results == ()
    assert stats.credits == 3


def test_reviewed_project_author_constant_reaches_only_first_party_results() -> None:
    records: list[dict[str, Any]] = [
        {"id": "T-1"},
        {"id": "T-2", "attribution": None},
        {"id": "T-3", "attribution": {"source_keys": ["source"]}},
    ]
    author = occurrence(
        PROJECT_AUTHOR_ORIGIN.path,
        PROJECT_AUTHOR_ORIGIN.record_key,
        PROJECT_AUTHOR_ORIGIN.field,
        role="project-author",
    )
    stats = person_credit_stats("person", [author, author], records)
    assert stats.results == ("T-1", "T-2")
    assert stats.credits == 1
    unresolved = replace(author, disposition="unresolved")
    assert person_credit_stats("person", [unresolved], records).results == ()


def test_project_credit_count_is_scoped_to_its_sources_and_direct_results() -> None:
    source = occurrence(BIBLIOGRAPHY, "project-source")
    spans = [
        source,
        source,
        occurrence(BIBLIOGRAPHY, "project-source", "/authors/0", person="coauthor"),
        occurrence(REGISTER, "T-1", "/builds_on/credit/0", role="prerequisite"),
        occurrence(BIBLIOGRAPHY, "unrelated-source"),
        occurrence(REGISTER, "T-2"),
        occurrence("packing/frontier/n-011.md", "11", "/found_by/0"),
        occurrence(BIBLIOGRAPHY, "project-source", disposition="unresolved"),
        occurrence(
            PROJECT_AUTHOR_ORIGIN.path,
            PROJECT_AUTHOR_ORIGIN.record_key,
            PROJECT_AUTHOR_ORIGIN.field,
            role="project-author",
        ),
    ]
    assert project_credit_count({"project-source"}, {"T-1"}, spans) == 3
    assert project_credit_count(set(), set(), spans) == 0


def test_result_tally_deduplicates_ids_orders_levels_and_keeps_real_dates() -> None:
    tally = tally_results(
        ["T-2", "T-1", "T-2", "T-3"],
        {"T-1": (5, "2026-10-01"), "T-2": (3, "2026-10-03"), "T-3": (3, "")},
        [1, 5, 3, 4, 2],
    )
    assert tally.results == ("T-2", "T-1", "T-3")
    assert tally.counts == ((5, 1), (4, 0), (3, 2), (2, 0), (1, 0))
    assert tally.latest == "2026-10-03"
    with pytest.raises(KeyError):
        tally_results(["unknown"], {}, [5, 4, 3, 2, 1])
    with pytest.raises(ValueError, match="significance"):
        tally_results(["T-1"], {"T-1": (6, "")}, [5, 4, 3, 2, 1])


@pytest.mark.parametrize(
    ("ids", "measures", "credit_count", "expected"),
    [
        ([], {}, None, "0 results"),
        ([], {}, 0, "0 results, 0 credits"),
        (["a"], {"a": (5, "")}, 1, "1 result at S5, 1 credit"),
        (["a", "b", "c"], dict.fromkeys("abc", (4, "")), None, "3 results at S4"),
        (
            ["a", "b", "c"],
            {"a": (5, ""), "b": (4, ""), "c": (4, "")},
            73,
            "3 results (1 at S5, 2 at S4), 73 credits",
        ),
    ],
)
def test_render_tally_grammar(
    ids: list[str],
    measures: dict[str, tuple[int, str]],
    credit_count: int | None,
    expected: str,
) -> None:
    rendered = render_tally(
        tally_results(ids, measures, [5, 4, 3, 2, 1]), credit_count=credit_count
    )
    assert rendered == expected


def test_render_tally_links_escape_attributes_and_link_single_levels() -> None:
    tally = tally_results(["a"], {"a": (5, "")}, [5, 4, 3, 2, 1])
    assert render_tally(tally, total_href="#credited-work") == (
        '<a href="#credited-work">1 result</a> at S5'
    )
    assert render_tally(
        tally,
        total_href='results.html?q="quoted"&all=1',
        level_hrefs={5: 'results.html?s=5&x="<tag>"'},
    ) == (
        '<a href="results.html?q=&quot;quoted&quot;&amp;all=1">1 result</a> at '
        '<a href="results.html?s=5&amp;x=&quot;&lt;tag&gt;&quot;">S5</a>'
    )
    mixed = tally_results(["a", "b"], {"a": (5, ""), "b": (3, "")}, [5, 4, 3, 2, 1])
    assert render_tally(mixed, level_hrefs={5: "?s=5", 3: "?s=3"}) == (
        '2 results (<a href="?s=5">1 at S5</a>, <a href="?s=3">1 at S3</a>)'
    )


@pytest.mark.parametrize(
    ("ids", "measures", "expected"),
    [
        (
            ["early", "late"],
            {"early": (3, "2026-01-01"), "late": (5, "2026-10-21")},
            "2026",
        ),
        (
            ["late", "early", "late"],
            {
                "early": (3, "2019-01-01"),
                "late": (5, "2026-10-21"),
                "uncredited": (4, "2001-01-01"),
            },
            "2019\u20132026",
        ),
        (
            ["year", "month", "day"],
            {"year": (3, "1979"), "month": (4, "2005-03"), "day": (5, "2018-04-05")},
            "1979\u20132018",
        ),
        (
            ["year", "month", "day"],
            {"year": (3, "2005"), "month": (4, "2005-03"), "day": (5, "2005-04-05")},
            "2005",
        ),
        ([], {"uncredited": (5, "2026-10-21")}, None),
        (
            ["undated"],
            {"undated": (3, ""), "uncredited": (5, "2026-10-21")},
            None,
        ),
    ],
)
def test_years_active_uses_only_dated_selected_results(
    ids: list[str], measures: dict[str, tuple[int, str]], expected: str | None
) -> None:
    assert years_active(ids, measures) == expected


@pytest.mark.parametrize(
    "dated",
    ["sometime in 2026", "2005-13", "2005-02-29", "0000", "2005-1", "20050101"],
)
def test_years_active_refuses_malformed_dates_instead_of_guessing(dated: str) -> None:
    with pytest.raises(ValueError, match=r"Invalid result date|month|day|year"):
        years_active(["result"], {"result": (3, dated)})
