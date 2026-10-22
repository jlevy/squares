"""Authored results, nonprimary credits and original activity dates have separate contracts."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from typing import Any, Literal

import pytest

from devtools.result_credit import PROJECT_AUTHOR_ORIGIN
from devtools.site_tallies import (
    person_activity_years,
    person_credit_stats,
    project_credit_associations,
    project_primary_results,
    render_tally,
    tally_credits,
    tally_results,
    years_active,
)
from sqpack.contributor_occurrences import (
    CreditOccurrence,
    CreditOrigin,
    load_occurrences,
    source_document,
)
from sqpack.contributors import load_contributors
from sqpack.yamlio import load_yaml

BIBLIOGRAPHY = "packing/resources/bibliography.yaml"
REGISTER = "packing/frontier/results.yaml"
LEVELS = (5, 4, 3, 2, 1)


def occurrence(
    path: str,
    key: str,
    field: str = "/credit",
    *,
    person: str = "person",
    disposition: str = "resolved",
    role: str = "credited-contributor",
    start: int = 0,
) -> CreditOccurrence:
    return CreditOccurrence(
        CreditOrigin(path, key, field),
        "Person after Person" if start else "Person",
        start,
        start + 6,
        "Person",
        role,
        disposition,
        person if disposition == "resolved" else None,
        ("byline",) if disposition == "resolved" else (),
    )


def author(key: str, person: str = "person", index: int = 0) -> CreditOccurrence:
    return occurrence(
        BIBLIOGRAPHY, key, f"/authors/{index}", person=person, role="source-author"
    )


def project_author(person: str = "person") -> CreditOccurrence:
    return occurrence(
        PROJECT_AUTHOR_ORIGIN.path,
        PROJECT_AUTHOR_ORIGIN.record_key,
        PROJECT_AUTHOR_ORIGIN.field,
        person=person,
        role="project-author",
    )


def test_primary_author_gets_result_and_other_people_get_disjoint_s5_credits() -> None:
    record = {"id": "T-1", "attribution": {"source_keys": ["source"]}}
    acknowledgment = occurrence(BIBLIOGRAPHY, "source", person="B", role="prerequisite")
    spans = [
        author("source", "A"),
        occurrence(BIBLIOGRAPHY, "source", person="A"),
        acknowledgment,
        replace(acknowledgment, note="Repeated metadata must not create another credit."),
        occurrence(BIBLIOGRAPHY, "source", person="C", start=13, role="prerequisite"),
    ]
    stats = {person: person_credit_stats(person, spans, [record]) for person in "ABC"}
    assert stats["A"].results == ("T-1",)
    assert stats["A"].credited_results == ()
    assert stats["B"].results == stats["C"].results == ()
    assert stats["B"].credited_results == stats["C"].credited_results == ("T-1",)
    assert stats["B"].reviewed_spans == 1
    measures = {"T-1": (5, "2026")}
    assert (
        render_tally(tally_results(stats["A"].results, measures, LEVELS))
        == '1 result <span class="site-tally-levels">(at S5)</span>'
    )
    credit_tally = tally_credits(
        ((person, result) for person in "BC" for result in stats[person].credited_results),
        measures,
        LEVELS,
    )
    assert credit_tally.counts == ((5, 2), (4, 0), (3, 0), (2, 0), (1, 0))
    assert (
        render_tally(credit_tally, noun="credit")
        == '2 credits <span class="site-tally-levels">(at S5)</span>'
    )


def test_multiple_sources_and_coauthors_do_not_double_count_results_or_add_credits() -> None:
    records: list[dict[str, Any]] = [
        {"id": "T-1", "attribution": {"source_keys": ["a", "b"]}},
        {"id": "T-2", "attribution": {"source_keys": ["a"]}},
    ]
    spans = [
        author("a", "A"),
        author("b", "A"),
        author("b", "B", 1),
        occurrence(BIBLIOGRAPHY, "a", person="A"),
        occurrence(BIBLIOGRAPHY, "b", person="A", role="prerequisite"),
    ]
    a = person_credit_stats("A", spans, records)
    b = person_credit_stats("B", spans, records)
    assert a.results == ("T-1", "T-2")
    assert b.results == ("T-1",)
    assert a.credited_results == b.credited_results == ()


def test_packet_authors_with_explicit_prerequisite_role_are_not_primary_for_that_source() -> (
    None
):
    spans = [
        author("massaccesi-packet", "massaccesi"),
        author("massaccesi-packet", "burns", 1),
        occurrence(BIBLIOGRAPHY, "massaccesi-packet", person="burns", role="prerequisite"),
        author("burns-own-paper", "burns"),
    ]
    records = [
        {"id": "T-015", "attribution": {"source_keys": ["massaccesi-packet"]}},
        {
            "id": "T-joint",
            "attribution": {"source_keys": ["massaccesi-packet", "burns-own-paper"]},
        },
    ]
    burns = person_credit_stats("burns", spans, records)
    assert burns.results == ("T-joint",)
    assert burns.credited_results == ("T-015",)
    assert person_credit_stats("massaccesi", spans, records).results == ("T-015", "T-joint")


def test_only_reviewed_personal_credits_count_not_case_lineage_or_source_citations() -> None:
    records = [
        {"id": "T-1", "builds_on": {"source_keys": ["basis"]}},
        {"id": "T-2", "builds_on": {"source_keys": ["basis"]}},
    ]
    spans = [
        author("basis"),
        occurrence("packing/frontier/n-011.md", "11", "/found_by/0"),
        occurrence(REGISTER, "T-1", "/builds_on/credit/0", role="prerequisite"),
        occurrence(REGISTER, "T-2", "/notes", role="prerequisite"),
        occurrence(BIBLIOGRAPHY, "basis", "/notes", role="prerequisite"),
        occurrence(REGISTER, "T-2", "/builds_on/credit/0", disposition="unresolved"),
    ]
    stats = person_credit_stats("person", spans, records)
    assert stats.results == ()
    assert stats.credited_results == ("T-1",)
    assert stats.reviewed_spans == 5


def test_project_author_is_primary_only_for_first_party_results() -> None:
    records = [
        {"id": "T-1"},
        {"id": "T-2", "attribution": None},
        {"id": "T-3", "attribution": {"source_keys": ["source"]}},
    ]
    span = project_author()
    stats = person_credit_stats("person", [span, span], records)
    assert stats.results == ("T-1", "T-2")
    assert stats.credited_results == ()
    assert stats.reviewed_spans == 1
    assert (
        person_credit_stats(
            "person", [replace(span, disposition="unresolved")], records
        ).results
        == ()
    )


def test_project_counts_received_credits_only_for_its_explicitly_linked_work() -> None:
    records: list[dict[str, Any]] = [
        {"id": "own", "attribution": {"source_keys": ["project-a"]}},
        {"id": "received", "builds_on": {"source_keys": ["project-a"]}},
        {"id": "unrelated-project", "builds_on": {"source_keys": ["project-b"]}},
        {"id": "unscoped-credit", "attribution": {"source_keys": ["modern"]}},
        {"id": "citation-only", "builds_on": {"source_keys": ["project-a"]}},
    ]
    spans = [
        author("project-a", "A"),
        author("project-b", "A"),
        author("modern", "B"),
        occurrence(
            REGISTER, "received", "/builds_on/credit/0", person="A", role="prerequisite"
        ),
        occurrence(
            REGISTER, "received", "/builds_on/credit/1", person="C", role="prerequisite"
        ),
        occurrence(
            REGISTER,
            "unrelated-project",
            "/builds_on/credit/0",
            person="A",
            role="prerequisite",
        ),
        occurrence(BIBLIOGRAPHY, "modern", person="A", role="prerequisite"),
    ]
    assert project_primary_results({"A"}, {"project-a"}, spans, records) == ("own",)
    assert project_credit_associations({"A"}, {"project-a"}, spans, records) == (
        ("A", "received"),
    )
    assert project_credit_associations({"A"}, {"unused"}, spans, records) == ()
    assert project_credit_associations({"A"}, set(), spans, records) is None
    assert project_credit_associations(set(), {"project-a"}, spans, records) is None


def test_shared_packet_project_primary_and_credit_totals_respect_specific_roles() -> None:
    spans = [
        author("shared-packet", "massaccesi"),
        author("shared-packet", "burns", 1),
        occurrence(BIBLIOGRAPHY, "shared-packet", person="burns", role="prerequisite"),
    ]
    records = [
        {"id": "T-015", "attribution": {"source_keys": ["shared-packet"]}},
        {"id": "T-016", "attribution": {"source_keys": ["shared-packet"]}},
    ]
    assert project_primary_results({"burns"}, {"shared-packet"}, spans, records) == ()
    assert project_primary_results({"massaccesi"}, {"shared-packet"}, spans, records) == (
        "T-015",
        "T-016",
    )
    assert project_credit_associations({"burns"}, {"shared-packet"}, spans, records) == (
        ("burns", "T-015"),
        ("burns", "T-016"),
    )
    assert project_credit_associations({"massaccesi"}, {"shared-packet"}, spans, records) == ()


@pytest.mark.parametrize("disposition", ["non-person", "unresolved"])
def test_projects_without_profile_ids_require_exact_reviewed_source_authorship(
    disposition: str,
) -> None:
    spans = [
        replace(author("own"), disposition=disposition, contributor_id=None),
        replace(author("unrelated"), disposition=disposition, contributor_id=None),
        occurrence(BIBLIOGRAPHY, "acknowledgment", disposition=disposition),
        occurrence(
            BIBLIOGRAPHY,
            "prerequisite",
            "/authors/0",
            disposition=disposition,
            role="prerequisite",
        ),
        occurrence(BIBLIOGRAPHY, "credit-only", disposition=disposition, role="source-author"),
        author("resolved-person"),
    ]
    keys = {
        "own",
        "acknowledgment",
        "prerequisite",
        "credit-only",
        "unreviewed",
        "resolved-person",
    }
    records = [
        {"id": key, "attribution": {"source_keys": [key]}}
        for key in sorted(keys | {"unrelated"})
    ]
    records.extend(
        [
            {
                "id": "later-credit",
                "attribution": {"source_keys": ["unrelated"]},
                "builds_on": {"source_keys": ["own"]},
            },
            {"id": "first-party", "builds_on": {"source_keys": ["own"]}},
            {"id": "own", "attribution": {"source_keys": ["own"]}},
        ]
    )
    assert project_primary_results((), keys, iter(spans), records) == ("own",)
    assert project_primary_results({"another-person"}, keys, spans, records) == ()
    assert person_credit_stats("person", spans, records).results == ("resolved-person",)
    assert project_credit_associations((), keys, spans, records) is None


def test_tallies_deduplicate_their_own_units_and_use_the_citing_results_significance() -> None:
    measures = {"T-1": (5, "2026-10-01"), "T-2": (3, "2026-10-03"), "T-3": (3, "")}
    tally = tally_results(["T-2", "T-1", "T-2", "T-3"], measures, [1, 5, 3, 4, 2])
    assert tally.results == ("T-2", "T-1", "T-3")
    assert tally.counts == ((5, 1), (4, 0), (3, 2), (2, 0), (1, 0))
    assert tally.latest == "2026-10-03"
    pairs = [("B", "T-1"), ("C", "T-1"), ("B", "T-1"), ("B", "T-2")]
    credit_tally = tally_credits(pairs, measures, LEVELS)
    assert credit_tally.associations == (("B", "T-1"), ("C", "T-1"), ("B", "T-2"))
    assert credit_tally.counts == ((5, 2), (4, 0), (3, 1), (2, 0), (1, 0))
    with pytest.raises(KeyError):
        tally_results(["unknown"], {}, LEVELS)
    with pytest.raises(ValueError, match="significance"):
        tally_credits([("B", "T-1")], {"T-1": (6, "")}, LEVELS)


@pytest.mark.parametrize(
    ("ids", "measures", "noun", "expected"),
    [
        ([], {}, "result", "0 results"),
        ([], {}, "credit", "0 credits"),
        (
            ["a"],
            {"a": (5, "")},
            "result",
            '1 result <span class="site-tally-levels">(at S5)</span>',
        ),
        (
            ["a"],
            {"a": (5, "")},
            "credit",
            '1 credit <span class="site-tally-levels">(at S5)</span>',
        ),
        (
            ["a", "b", "c"],
            dict.fromkeys("abc", (4, "")),
            "result",
            '3 results <span class="site-tally-levels">(at S4)</span>',
        ),
        (
            ["a", "b", "c"],
            {"a": (5, ""), "b": (4, ""), "c": (4, "")},
            "credit",
            '3 credits <span class="site-tally-levels">(1 at S5, 2 at S4)</span>',
        ),
    ],
)
def test_render_tally_grammar(
    ids: list[str],
    measures: dict[str, tuple[int, str]],
    noun: Literal["result", "credit"],
    expected: str,
) -> None:
    tally = (
        tally_results(ids, measures, LEVELS)
        if noun == "result"
        else tally_credits((("p", identifier) for identifier in ids), measures, LEVELS)
    )
    assert render_tally(tally, noun=noun) == expected


def test_render_tally_links_escape_attributes_and_link_single_levels() -> None:
    tally = tally_results(["a"], {"a": (5, "")}, LEVELS)
    assert (
        render_tally(tally, total_href="#credited-work")
        == '<a href="#credited-work">1 result</a> '
        '<span class="site-tally-levels">(at S5)</span>'
    )
    assert render_tally(
        tally,
        total_href='results.html?q="quoted"&all=1',
        level_hrefs={5: 'results.html?s=5&x="<tag>"'},
    ) == (
        '<a href="results.html?q=&quot;quoted&quot;&amp;all=1">1 result</a> '
        '<span class="site-tally-levels">(at '
        '<a href="results.html?s=5&amp;x=&quot;&lt;tag&gt;&quot;">S5</a>)</span>'
    )
    credit_tally = tally_credits([("B", "a"), ("C", "b")], {"a": (5, ""), "b": (3, "")}, LEVELS)
    assert (
        render_tally(credit_tally, noun="credit", level_hrefs={5: "?s=5", 3: "?s=3"})
        == '2 credits <span class="site-tally-levels">(<a href="?s=5">1 at S5</a>, '
        '<a href="?s=3">1 at S3</a>)</span>'
    )


def test_stromquist_original_publication_does_not_become_2026_activity_through_reuse() -> None:
    spans = [
        author("Stromquist2003", "stromquist"),
        author("modern2026", "modern"),
        occurrence(BIBLIOGRAPHY, "modern2026", person="stromquist", role="prerequisite"),
        occurrence(
            REGISTER, "T-new", "/builds_on/credit/0", person="stromquist", role="prerequisite"
        ),
    ]
    records = [
        {
            "id": "T-new",
            "attribution": {"source_keys": ["modern2026"], "published": "2026"},
            "registered": "2026-10-21",
        }
    ]
    bibliography = {"Stromquist2003": {"year": 2003}, "modern2026": {"year": 2026}}
    stats = person_credit_stats("stromquist", spans, records)
    assert stats.results == ()
    assert stats.credited_results == ("T-new",)
    years = person_activity_years("stromquist", spans, bibliography, {}, records)
    assert years == (2003,)
    assert years_active(years) == "2003"


def test_source_activity_years_are_independent_of_shared_result_publication_dates() -> None:
    spans = [author("Bentz2010", "bentz"), author("Daniel2026", "daniel")]
    bibliography = {"Bentz2010": {"year": 2010}, "Daniel2026": {"year": 2026}}
    records = [
        {
            "id": "T-006",
            "attribution": {"source_keys": ["Bentz2010", "Daniel2026"], "published": "2010"},
        }
    ]
    assert person_credit_stats("daniel", spans, records).results == ("T-006",)
    assert person_activity_years("daniel", spans, bibliography, {}, records) == (2026,)
    assert person_activity_years("bentz", spans, bibliography, {}, records) == (2010,)
    assert person_activity_years("bentz", spans, bibliography, {}, []) == (2010,)


def test_case_activity_does_not_borrow_improvement_or_capture_dates() -> None:
    path = "packing/frontier/n-017.md"
    spans = [
        occurrence(path, "17", "/reported_upper_bound/found_by/0", role="construction-finder"),
        occurrence(path, "17", "/reported_lower_bound/proved_by/0", role="lower-bound-prover"),
        occurrence(
            path,
            "17",
            "/reported_upper_bound/improved_by/0",
            person="improver",
            role="construction-improver",
        ),
    ]
    cases = {
        path: {
            "reported_upper_bound": {"found_year": 1998, "retrieved_date": "2026-08-22"},
            "reported_lower_bound": {"proved_year": 2003, "source_date": "2026-10-21"},
        }
    }
    assert person_activity_years("person", spans, {}, cases, []) == (1998, 2003)
    assert person_activity_years("improver", spans, {}, cases, []) == ()


@pytest.mark.parametrize("dated", ["1979", "2005-03", "2018-04-05"])
def test_actual_project_authorship_uses_established_dates_without_import_fallback(
    dated: str,
) -> None:
    records = [
        {"id": "own", "established": dated, "registered": "2026-10-21"},
        {"id": "undated", "registered": "2026-10-21"},
        {"id": "external", "established": "2026", "attribution": {"source_keys": ["other"]}},
    ]
    assert person_activity_years("person", [project_author()], {}, {}, records) == (
        int(dated[:4]),
    )


def test_unknown_activity_stays_blank_without_mining_names_urls_or_unreviewed_authors() -> None:
    spans = [
        author("undated"),
        occurrence(
            BIBLIOGRAPHY, "dated", "/authors/0", role="source-author", disposition="unresolved"
        ),
        occurrence(BIBLIOGRAPHY, "dated", person="person", role="prerequisite"),
    ]
    bibliography = {
        "undated": {"year": None, "dated": "2026-10-21", "url": "https://example.com/2003"},
        "dated": {"year": 2026},
    }
    years = person_activity_years("person", spans, bibliography, {}, [])
    assert years == ()
    assert person_activity_years("person", [author("missing")], {}, {}, []) == ()
    assert years_active(years) is None
    assert years_active([2026, 2003, 2026]) == "2003\u20132026"


@pytest.mark.parametrize(
    "dated", ["sometime in 2026", "2005-13", "2005-02-29", "0000", "2005-1", "20050101"]
)
def test_activity_refuses_invalid_authored_dates(dated: str) -> None:
    with pytest.raises(ValueError, match=r"Invalid activity date|month|day|year"):
        person_activity_years(
            "person", [project_author()], {}, {}, [{"id": "own", "established": dated}]
        )


def test_all_45_profiles_have_reviewed_original_activity_years_and_disjoint_work() -> None:
    packing = Path(__file__).resolve().parents[1]
    repo = packing.parent
    profiles = load_contributors(packing / "contributors/people", repo=repo)
    occurrences = load_occurrences(repo=repo, profiles=profiles).occurrences
    sources = {
        source["key"]: source
        for source in load_yaml((packing / "resources/bibliography.yaml").read_text())[
            "sources"
        ]
    }
    records = load_yaml((packing / "frontier/results.yaml").read_text())["results"]
    cases = {
        path: source_document(repo / path)["packing"]
        for path in {item.origin.path for item in occurrences}
        if path.startswith("packing/frontier/n-")
    }
    modern = (
        "benjamin-greff",
        "can-li",
        "daniil-ostashev",
        "darius-muglich",
        "david-r-maciver",
        "eric-deleeuw",
        "evan-daniel",
        "francisco-couzo",
        "griffin-casson",
        "gustavo-massaccesi",
        "guzhou0806",
        "hiroaki-hosono",
        "joost-de-winter",
        "joshua-levy",
        "ke-wang",
        "kevin-fang",
        "manasseh-ahmed",
        "marc-leonard-overbeck",
        "mira",
        "mykhailo-polkovskyi",
        "nate-chaoweeraprasit",
        "oscar-fitzharding",
        "rio-calle",
        "robert-barnett",
        "ryan-xu",
        "ryu-sungjoon",
        "sam-burns",
        "seth-rehwaldt",
        "siddharth-gupta",
        "tokoharu",
    )
    expected: dict[str, tuple[int, ...]] = dict.fromkeys(modern, (2026,))
    expected.update(
        {
            "ahyangyi": (),
            "anabologyco-maker": (),
            "david-ellsworth": (2024, 2025, 2026),
            "erich-friedman": (1997, 1999, 2009),
            "f-gobel": (1979,),
            "hiroshi-nagamochi": (2005,),
            "john-bidwell": (1998,),
            "michael-j-kearney": (2001, 2002),
            "peter-shiu": (2001, 2002),
            "philippe-ryckelynck": (2005,),
            "thierry-gensane": (2004, 2005),
            # Retained Kingbird n39/n51/n55 explicitly credit discoveries in January 2026.
            "thomas-schadt": (2025, 2026),
            "walter-stromquist": (2003,),
            "walter-trump": (1979, 2023),
            "wolfram-bentz": (2009, 2010, 2016, 2018),
        }
    )
    assert set(expected) <= set(profiles.by_id)
    assert {
        identifier: person_activity_years(identifier, occurrences, sources, cases, records)
        for identifier in expected
    } == expected
    for identifier in profiles.by_id:
        stats = person_credit_stats(identifier, occurrences, records)
        assert set(stats.results).isdisjoint(stats.credited_results)
    stromquist = person_credit_stats("walter-stromquist", occurrences, records)
    assert stromquist.results == ()
    assert "T-010" in stromquist.credited_results
    assert person_credit_stats("sam-burns", occurrences, records).results == ()
    assert person_credit_stats("gustavo-massaccesi", occurrences, records).results == (
        "T-015",
        "T-016",
    )


def test_formalization_infrastructure_and_hpc_support_are_credits_not_primary_results() -> None:
    key = "[Ahmed 11SquaresFormalized 2026]"
    spans = [
        item
        for item in load_occurrences().occurrences
        if item.origin.path == BIBLIOGRAPHY and item.origin.record_key == key
    ]
    record = {"id": "synthetic-formalization", "attribution": {"source_keys": [key]}}
    for identifier in ("ctjlewis", "julian-jj"):
        stats = person_credit_stats(identifier, spans, [record])
        assert stats.results == ()
        assert stats.credited_results == ("synthetic-formalization",)
    assert person_credit_stats("hiroaki-hosono", spans, [record]).results == (
        "synthetic-formalization",
    )


def test_formalization_support_acknowledgments_date_own_work_not_later_citations() -> None:
    key = "[Ahmed 11SquaresFormalized 2026]"
    spans = load_occurrences().occurrences
    for identifier in ("ctjlewis", "julian-jj"):
        assert person_activity_years(identifier, spans, {key: {"year": 2026}}, {}, ()) == (
            2026,
        )
    later = occurrence(BIBLIOGRAPHY, "later-citation", person="stromquist")
    assert person_activity_years(
        "stromquist",
        [author("original", "stromquist"), later],
        {"original": {"year": 2003}, "later-citation": {"year": 2026}},
        {},
        (),
    ) == (2003,)
