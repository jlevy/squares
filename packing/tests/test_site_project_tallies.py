"""The other projects' order, their tallies of results, and the links the tallies carry.

The overview and profile resources rank catalogues, repositories and websites together
by the significance of the primary results the register attributes to each. A card
with registered results ends with a tally, `6 results (3 at S4, 3 at
S3)`, whose total opens the results table on that project's results and whose counts
open it at one significance level.

The order is one small function over the register, tested here on a synthetic register
with a tie at each step, and the rendered page is held to it. The tallies are held to the
same counts, their links to the rows they name, and their markup to valid HTML: every
card is a box holding the project link and then the author and tally links, since a
link cannot hold a link. The last tests follow a card's links in Chromium and read the
table they open. Skipped where no Chromium can be launched; `SQPACK_CHROMIUM` names one the
environment supplies.
"""

from __future__ import annotations

import html
import itertools
import os
import re
from collections.abc import Iterator, Mapping
from dataclasses import dataclass
from datetime import datetime, time
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, cast

import pytest

from devtools import (
    overview_data,
    overview_sections,
    profile_links,
    record_presentation,
    render_contributors,
    render_overview,
    site_resources,
    site_tallies,
)
from devtools.overview_sections import Cited, ProjectTally, project_order, project_tallies
from devtools.render_n11_lower_bounds_explainer_pdf import BROWSER_OVERRIDE
from sqpack.contributor_occurrences import CreditOccurrence, load_occurrences
from sqpack.probes import probe
from sqpack.yamlio import safe_load
from tests import site_renders

PROBES = Path(__file__).resolve().parent / "probes"
PRESETS = probe(PROBES, "site_result_filters/presets")
LEVELS = (5, 4, 3, 2, 1)
SECTION = 'id="other-square-packing-projects"'


def _order(results: list[Cited], projects: str) -> str:
    names = {name: name for name in projects}
    return "".join(project_order(project_tallies(list(projects), results, LEVELS), names))


def test_a_tally_counts_each_level_and_a_shared_result_for_each_project() -> None:
    results = [
        Cited("T-1", 5, "2026-09-01", ("a",)),
        Cited("T-2", 3, "2026-09-20", ("a", "b")),
        Cited("T-3", 3, "2026-09-10", ("b",)),
        Cited("T-4", 4, "2026-09-05", ()),
    ]
    tallies = project_tallies(["a", "b", "c"], results, LEVELS)
    assert tallies["a"] == ProjectTally(
        ("T-1", "T-2"), ((5, 1), (4, 0), (3, 1), (2, 0), (1, 0)), "2026-09-20"
    )
    assert tallies["b"] == ProjectTally(
        ("T-2", "T-3"), ((5, 0), (4, 0), (3, 2), (2, 0), (1, 0)), "2026-09-20"
    )
    assert tallies["c"] == ProjectTally((), ((5, 0), (4, 0), (3, 0), (2, 0), (1, 0)), "")


def test_the_order_is_by_the_counts_from_the_highest_level_down() -> None:
    """One result at S5 stands before any number below it; among projects with the same
    count at a level the next level decides, and so on down the scale."""
    results = [
        Cited("T-1", 5, "2026-01-01", ("a",)),
        *(Cited(f"T-b{i}", 4, "2026-09-01", ("b",)) for i in range(9)),
        Cited("T-2", 5, "2026-01-01", ("c",)),
        Cited("T-3", 5, "2026-01-01", ("c",)),
        # d and e tie at S5 and S4, and S3 decides; f and g tie through S3, and S2 decides.
        Cited("T-4", 5, "2026-01-01", ("d",)),
        Cited("T-5", 4, "2026-01-01", ("d",)),
        Cited("T-6", 5, "2026-01-01", ("e",)),
        Cited("T-7", 4, "2026-01-01", ("e",)),
        Cited("T-8", 3, "2026-01-01", ("e",)),
        Cited("T-9", 3, "2026-01-01", ("f",)),
        Cited("T-10", 3, "2026-01-01", ("g",)),
        Cited("T-11", 2, "2026-01-01", ("g",)),
        Cited("T-12", 1, "2026-01-01", ("h",)),
    ]
    assert _order(results, "abcdefgh") == "cedabgfh"
    # The order the projects are given in is not an input.
    assert _order(results, "hgfedcba") == "cedabgfh"


def test_projects_level_on_every_count_stand_newest_first_then_by_name() -> None:
    """After the whole tuple, the newest cited result first; after that, the name, read
    without regard to case; and a project with no result comes last, by name."""
    results = [
        Cited("T-1", 4, "2026-09-01", ("b",)),
        Cited("T-2", 4, "2026-09-22", ("c",)),
        Cited("T-3", 4, "2026-09-22", ("a",)),
        Cited("T-4", 3, "2026-09-30", ("d",)),
    ]
    tallies = project_tallies(["z", "Y", "d", "c", "b", "a"], results, LEVELS)
    names = {name: name for name in tallies}
    assert project_order(tallies, names) == ["a", "c", "b", "d", "Y", "z"]
    # The name that breaks a tie is the one given for the project, not its key.
    renamed = {**names, "a": "zeta"}
    assert project_order(tallies, renamed) == ["c", "a", "b", "d", "Y", "z"]


@pytest.mark.parametrize("on_profile", [False, True], ids=["homepage", "profile"])
def test_shared_resource_cards_rank_every_kind_and_ignore_inventory_order(
    monkeypatch: pytest.MonkeyPatch, *, on_profile: bool
) -> None:
    """A pinned catalogue or an unranked personal site cannot jump above S5 work."""
    titles = {
        "catalogue": "Catalogue",
        "strong": "Strong",
        "mixed": "Mixed",
        "recent": "Recent",
        "old": "Old",
        "zero-a": "Shared",
        "zero-b": "Shared",
        "personal": "Personal website",
    }
    urls = {name: f"https://example.org/{name}" for name in titles}
    records = tuple(
        site_resources.Resource(
            urls[name], title, "", "", (), "catalogue" if name == "catalogue" else "website"
        )
        for name, title in titles.items()
    )
    cited = [
        Cited("T-1", 5, "2025-01-01", tuple(urls[name] for name in ("strong", "mixed", "old"))),
        Cited("T-2", 5, "2026-01-01", (urls["strong"], urls["recent"])),
        Cited("T-3", 4, "2026-01-01", (urls["mixed"],)),
        *(Cited(f"T-c{i}", 4, "2026-10-01", (urls["catalogue"],)) for i in range(9)),
    ]
    tallies = project_tallies(
        [url for name, url in urls.items() if name != "personal"], cited, LEVELS
    )
    monkeypatch.setattr(overview_sections, "_profile_resource_tallies", lambda: tallies)
    monkeypatch.setattr(overview_sections, "listed_projects", lambda _: list(tallies.items()))
    monkeypatch.setattr(overview_sections, "significance_levels", lambda: LEVELS)

    def card(resource: site_resources.Resource, _tally: ProjectTally, **_kwargs: object) -> str:
        return f'<a href="{resource.url}">{resource.title}</a>'

    monkeypatch.setattr(overview_sections, "resource_card", card)
    expected = [
        urls[name]
        for name in (
            "strong",
            "mixed",
            "recent",
            "old",
            "catalogue",
            "personal",
            "zero-a",
            "zero-b",
        )
    ]
    for supplied in (records, tuple(reversed(records))):
        rendered = overview_sections.resource_cards(
            supplied,
            overview=None if on_profile else cast(overview_data.Overview, object()),
            current_profile="person" if on_profile else None,
        )
        assert re.findall(r'href="([^"]+)"', rendered) == expected


def test_project_bylines_link_known_people_and_keep_organizations_plain(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    index = profile_links.profile_index(
        {
            "nate-chaoweeraprasit": {
                "display_name": "Nate Chaoweeraprasit",
                "surname": "Chaoweeraprasit",
                "aliases": ["natcha"],
            },
            "mykhailo-polkovskyi": {
                "display_name": "Mykhailo Polkovskyi",
                "surname": "Polkovskyi",
                "aliases": ["Mishapolk"],
            },
            "ke-wang": {"display_name": "Ke Wang", "surname": "Wang"},
            "can-li": {"display_name": "Can Li", "surname": "Li"},
        }
    )
    monkeypatch.setattr(overview_sections, "public_index", lambda: index)
    assert overview_sections.project_author("Nate Chaoweeraprasit") == (
        'By <a href="profiles/nate-chaoweeraprasit.html" '
        'data-profile-name="full">Nate Chaoweeraprasit</a>'
    )
    assert overview_sections.project_author("Mishapolk") == (
        'By <a href="profiles/mykhailo-polkovskyi.html" '
        'data-profile-name="full">Mykhailo Polkovskyi</a>'
    )
    assert overview_sections.project_author("Ke Wang and Can Li") == (
        'By <a href="profiles/ke-wang.html" data-profile-name="full">Ke Wang</a> '
        'and <a href="profiles/can-li.html" data-profile-name="full">Can Li</a>'
    )
    assert overview_sections.project_author("PingYou Ltd") == "By PingYou Ltd"
    assert overview_sections.project_author("Unlisted & Associates") == (
        "By Unlisted &amp; Associates"
    )


def test_project_bylines_do_not_guess_a_shared_alias(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    index = profile_links.profile_index(
        {
            "alex-one": {"display_name": "Alex One", "aliases": ["shared"]},
            "alex-two": {"display_name": "Alex Two", "aliases": ["shared"]},
        }
    )
    monkeypatch.setattr(overview_sections, "public_index", lambda: index)
    assert overview_sections.project_author("shared") == "By shared"


def test_shared_resources_match_homepage_bylines_and_profile_counts() -> None:
    records = site_resources.resources()
    assert len({record.url for record in records}) == len(records)
    assert {record.url for record in records} == set(overview_sections.project_urls())
    assert overview_sections.OTHER_PROJECTS is site_resources.OTHER_PROJECTS
    for record in records:
        linked = tuple(
            re.findall(
                r'href="profiles/([a-z0-9-]+)\.html"',
                overview_sections.resource_byline(record),
            )
        )
        assert linked == record.profile_ids, record.byline
        for identifier in linked:
            selected = site_resources.resources_for_profile(identifier)
            assert record in selected
            assert len({item.url for item in selected}) == len(selected)
            assert f'href="{html.escape(record.url)}"' in render_contributors.resource_list(
                identifier
            )
    catalogue = next(record for record in records if record.url == site_resources.KINGBIRD)
    assert catalogue.byline == "David Ellsworth after Erich Friedman"
    assert catalogue.profile_ids == ("david-ellsworth", "erich-friedman")
    wang = next(
        record for record in records if record.url == "https://doi.org/10.5281/zenodo.23038546"
    )
    assert wang.profile_ids == ("ke-wang", "can-li")
    nate = site_resources.resources_for_profile("nate-chaoweeraprasit")
    assert len({record.url for record in nate if "#issuecomment-" in record.url}) == 2
    xu = site_resources.resources_for_profile("ryan-xu")
    assert any("/blob/" in record.url for record in xu)
    assert any(record.url == "https://github.com/ry-xu/square_packing" for record in xu)
    gupta = render_contributors.resource_list("siddharth-gupta")
    assert (
        'href="profiles/nate-chaoweeraprasit.html" data-profile-name="full">Nate '
        "Chaoweeraprasit</a>" in gupta
    )
    assert 'href="profiles/evan-daniel.html" data-profile-name="full">Evan Daniel</a>' in gupta
    assert 'href="profiles/siddharth-gupta.html"' not in gupta


def test_resource_matching_refuses_ambiguous_aliases_and_uncredited_mentions(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    index = profile_links.profile_index(
        {
            "alex": {"display_name": "Alex One", "surname": "One"},
            "beth": {"display_name": "Beth Two", "aliases": ["Alex One"], "surname": "Two"},
        }
    )
    monkeypatch.setattr(overview_sections, "public_index", lambda: index)
    assert site_resources.profile_ids_for_byline("Alex One", index) == ()
    assert overview_sections.project_author("Alex One") == "By Alex One"
    assert site_resources.profile_ids_for_byline("Alex\nOne after Beth Two", index) == (
        "alex",
        "beth",
    )
    assert site_resources.profile_ids_for_byline("One", index) == ("alex",)
    monkeypatch.setattr(site_resources, "CATALOGUE_SITES", ())
    monkeypatch.setattr(site_resources, "OTHER_SITES", ())
    monkeypatch.setattr(
        site_resources,
        "OTHER_PROJECTS",
        (("https://github.com/alex/work", "Unlisted Organization", "Alex One built it."),),
    )
    (record,) = site_resources.resource_records(index)
    assert record.profile_ids == ()


def test_resource_projection_rejects_conflicting_urls_and_deduplicates_equal_records(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    index = profile_links.profile_index({"alex": {"display_name": "Alex One"}})
    first = ("https://example.org/work#one", "Work", "Alex One", "A result.")
    monkeypatch.setattr(site_resources, "OTHER_PROJECTS", ())
    monkeypatch.setattr(site_resources, "CATALOGUE_SITES", ())
    monkeypatch.setattr(site_resources, "OTHER_SITES", (first, first))
    assert len(site_resources.resource_records(index)) == 1
    conflicting = (first[0], "Different title", first[2], first[3])
    monkeypatch.setattr(site_resources, "OTHER_SITES", (first, conflicting))
    with pytest.raises(ValueError, match="conflicting external resource"):
        site_resources.resource_records(index)


@pytest.fixture(scope="module")
def overview() -> overview_data.Overview:
    return site_renders.overview()


@pytest.fixture(scope="module")
def page() -> str:
    return site_renders.html("index.html")


@pytest.fixture(scope="module")
def results_page() -> str:
    return site_renders.html(render_overview.RESULTS_PAGE)


@dataclass(frozen=True)
class _ProjectInputs:
    coverage: tuple[Mapping[str, Any], ...]
    bibliography: tuple[Mapping[str, Any], ...]
    occurrences: tuple[CreditOccurrence, ...]
    resources: tuple[site_resources.Resource, ...]


@pytest.fixture(scope="module")
def project_inputs() -> _ProjectInputs:
    """Validate the unchanged raw records once, then reuse them across every project.

    Keep these inputs separate from the production source-key map so the oracle still
    derives each project's coverage independently. The low-level loader stays uncached
    for tests that mutate source records or load another repository.
    """
    coverage = safe_load(overview_sections.SOURCE_COVERAGE.read_text(encoding="utf-8"))
    bibliography = safe_load(overview_data.BIBLIOGRAPHY.read_text(encoding="utf-8"))
    return _ProjectInputs(
        tuple(coverage["sources"]),
        tuple(bibliography["sources"]),
        load_occurrences().occurrences,
        site_resources.resources(),
    )


def _attributed(
    overview: overview_data.Overview, url: str, inputs: _ProjectInputs
) -> list[overview_data.Result]:
    """A project's results, read from the register here and not through the mapping the
    page uses: those whose attribution names a key the coverage register gives a source
    at the project's address, a key `PROJECT_EXTRA_KEYS` adds, or a key the bibliography
    files under the project's venue in `SOURCE_VENUES`."""
    venue = overview_sections.SOURCE_VENUES.get(url)
    keys = (
        {
            source["source_key"]
            for source in inputs.coverage
            if re.sub(r"/tree/.*", "", source["url"]).rstrip("/") == url.rstrip("/")
        }
        | set(overview_sections.PROJECT_EXTRA_KEYS.get(url, ()))
        | {
            entry["key"]
            for entry in inputs.bibliography
            if venue and entry.get("venue") == venue
        }
    )
    authors = next((record.profile_ids for record in inputs.resources if record.url == url), ())
    ids = set(
        site_tallies.project_primary_results(
            authors,
            keys,
            inputs.occurrences,
            [result.record for result in overview.results],
        )
    )
    return [result for result in overview.results if result.id in ids]


@pytest.mark.parametrize(
    ("url", "expected"),
    [
        ("https://github.com/BuddenPing/squares", {"T-174", "T-195"}),
        (
            "https://github.com/BuddenPing/square-packing-certificates",
            {"T-147", "T-148", "T-164", "T-167", "T-168", "T-169", "T-166", "T-170", "T-171"},
        ),
    ],
)
def test_corporate_project_cards_and_filters_retain_canonical_primary_results(
    url: str,
    expected: set[str],
    *,
    overview: overview_data.Overview,
    project_inputs: _ProjectInputs,
    page: str,
    results_page: str,
) -> None:
    """These reviewed source-authored IDs belong to PingYou Ltd without a human join."""
    resource = next(record for record in project_inputs.resources if record.url == url)
    assert resource.profile_ids == ()
    ranked = overview_sections.ranked_projects(overview)
    tally = dict(ranked)[url]
    assert set(tally.results) == expected
    levels = [
        overview_sections.significance(result)
        for result in overview.results
        if result.id in expected
    ]
    counts = tuple((level, levels.count(level)) for level in LEVELS)
    assert tally.counts == counts
    position = next(index for index, (project, _) in enumerate(ranked) if project == url)
    assert all(any(count for _, count in earlier.counts) for _, earlier in ranked[:position])
    assert all(
        tuple(count for _, count in later.counts) <= tuple(count for _, count in counts)
        for _, later in ranked[position + 1 :]
    )
    cards = _cards(page)
    assert cards[position][0] == url
    foot = dict(cards)[url]
    assert f">{len(expected)} results</a>" in foot
    slug = overview_sections.project_slug(url)
    assert f'href="results.html?project={slug}"' in foot
    for level, count in counts:
        if count:
            assert f'href="results.html?project={slug}&amp;s={level}"' in foot
    assert overview_sections.resource_byline(resource) == "By PingYou Ltd"
    memberships = {
        result.id
        for result in overview.results
        if slug in overview_sections.result_projects(result)
    }
    assert memberships == expected
    facets = dict(re.findall(r'<tr id="(t-\d+)"[^>]*\sdata-project="([^"]*)"', results_page))
    assert {row.upper() for row, listed in facets.items() if slug in listed.split()} == expected


def test_project_oracle_reuses_inputs_without_reloading_source_records(
    overview: overview_data.Overview,
    project_inputs: _ProjectInputs,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def unexpected_reload(*_args: object, **_kwargs: object) -> None:
        pytest.fail("project oracle must reuse its validated module inputs")

    monkeypatch.setattr(f"{__name__}.load_occurrences", unexpected_reload)
    monkeypatch.setattr(f"{__name__}.safe_load", unexpected_reload)
    attributed = {
        url: _attributed(overview, url, project_inputs)
        for url in overview_sections.project_urls()
    }
    assert any(attributed.values())


def _cards(page: str) -> list[tuple[str, str]]:
    """Project headings and their independent tally footers, in page order."""
    section = page.split(SECTION, 1)[1].split("<h2", 1)[0]
    cards = []
    for body in section.split('<div class="site-card site-card-footed"')[1:]:
        heading = re.search(r'<a class="site-card-link site-card-heading" href="([^"]+)"', body)
        assert heading is not None
        tally = re.search(r'<span class="site-project-tally">', body)
        foot = ""
        if tally is not None:
            depth = 1
            for span in re.finditer(r"</?span\b[^>]*>", body[tally.end() :]):
                depth += -1 if span[0].startswith("</") else 1
                if depth == 0:
                    foot = body[tally.end() : tally.end() + span.start()]
                    break
            assert depth == 0, "unterminated project tally"
        cards.append((heading[1], foot))
    return cards


def test_the_page_lists_the_projects_in_the_functions_order(
    page: str, overview: overview_data.Overview, project_inputs: _ProjectInputs
) -> None:
    """All resource kinds share the register's descending significance order.

    No catalogue prefix may interrupt the count vector, and resources with no
    registered result come last, by name.
    """
    ranked = overview_sections.ranked_projects(overview)
    assert [url for url, _ in _cards(page)] == [url for url, _ in ranked]
    assert [url for url, _ in overview_sections.listed_projects(overview)] == [
        url for url, _ in _cards(page)
    ]
    assert {url for url, _ in ranked} == set(overview_sections.project_urls())
    keys = []
    for url, _ in ranked:
        own = _attributed(overview, url, project_inputs)
        levels = [overview_sections.significance(result) for result in own]
        newest = max((result.dated[1] for result in own), default="")
        keys.append((tuple(levels.count(level) for level in LEVELS), newest))
    assert [counts for counts, _ in keys] == sorted(
        (counts for counts, _ in keys), reverse=True
    )
    for (counts, newest), (after, older) in itertools.pairwise(keys):
        if counts == after and sum(counts):
            assert newest >= older
    empty = [
        overview_sections.project_headline(url).lower()
        for (url, _), (counts, _) in zip(ranked, keys, strict=True)
        if not sum(counts)
    ]
    assert empty
    assert empty == sorted(empty)
    assert sum(keys[len(keys) - len(empty) - 1][0]) > 0
    assert overview_sections.significance_levels() == LEVELS


def test_each_card_ends_with_its_tally_linked_to_its_results(
    page: str, overview: overview_data.Overview, project_inputs: _ProjectInputs
) -> None:
    """One shared component counts distinct registered results and scoped reviewed credits."""
    with_tally = 0
    measures = {
        result.id: (overview_sections.significance(result), result.dated[1])
        for result in overview.results
    }
    for url, foot in _cards(page):
        own = _attributed(overview, url, project_inputs)
        levels = [overview_sections.significance(result) for result in own]
        slug = overview_sections.project_slug(url)
        total = f"{len(own)} result" + ("" if len(own) == 1 else "s")
        counts = [(level, levels.count(level)) for level in LEVELS if level in levels]
        authors = next(
            (record.profile_ids for record in project_inputs.resources if record.url == url),
            (),
        )
        associations = site_tallies.project_credit_associations(
            authors,
            overview_sections.project_source_keys()[url],
            project_inputs.occurrences,
            [result.record for result in overview.results],
        )
        expected = total
        if len(counts) == 1:
            expected += f" (at S{counts[0][0]})"
        elif counts:
            expected += f" ({', '.join(f'{n} at S{level}' for level, n in counts)})"
        records = record_presentation.record_tally(
            [result.id for result in own], measures, blank_zero=True
        )
        if records:
            expected = records + " · " + expected
        if associations:
            expected += " · " + site_tallies.render_tally(
                site_tallies.tally_credits(associations, measures, LEVELS), noun="credit"
            )
        assert re.sub(r"<[^>]+>", "", foot) == re.sub(r"<[^>]+>", "", expected), url
        links = re.findall(r'<a href="([^"]+)">([^<]+)</a>', foot)
        if own:
            with_tally += 1
            assert links[0] == (f"results.html?project={slug}", total)
            expected_levels = [
                (
                    f"results.html?project={slug}&amp;s={level}",
                    f"S{level}" if len(counts) == 1 else f"{n} at S{level}",
                )
                for level, n in counts
            ]
            assert links[1:] == expected_levels
        else:
            assert links == []
    assert with_tally >= 9
    assert render_overview.RESULTS_PAGE == "results.html"


def test_a_tally_link_selects_exactly_its_projects_rows(
    overview: overview_data.Overview, project_inputs: _ProjectInputs, results_page: str
) -> None:
    """A row carries the slugs of the listed projects it is attributed to, and the
    Project preset holds a row to one of them, so the rows a tally's link shows are the
    results it counts. The results page's defaults hide no row, so the link needs to
    clear nothing; and every slug is distinct and is a choice of the Project control."""
    results = results_page
    facets = dict(re.findall(r'<tr id="(t-\d+)"[^>]*\sdata-project="([^"]*)"', results))
    assert len(facets) == len(overview.results)
    slugs = [overview_sections.project_slug(url) for url in overview_sections.project_urls()]
    assert len(set(slugs)) == len(slugs)
    for url in overview_sections.project_urls():
        slug = overview_sections.project_slug(url)
        assert re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug), slug
        rows = sorted(row for row, listed in facets.items() if slug in listed.split())
        assert rows == sorted(
            result.id.lower() for result in _attributed(overview, url, project_inputs)
        ), url
        name = html.escape(overview_sections.project_name(url))
        assert f'<option value="{slug}">{name}</option>' in results
    assert overview_sections.FilterDefaults() == overview_sections.RESULTS_DEFAULTS
    assert not re.search(r"<tr id=\"t-\d+\"[^>]*\shidden", results)
    bar = results.split('<div class="site-table-tools site-result-filters">', 1)[1]
    bar = bar.split("</div>", 1)[0]
    assert bar.count("<label hidden>") == 4
    assert (
        '<label hidden>Project <select data-filter="project" data-bound="has" data-preset>'
        in bar
    )
    assert '<label hidden>At significance <select data-filter="s" data-preset>' in bar
    assert '<label hidden>Added on <select data-filter="added" data-preset>' in bar
    # The bar's own controls keep their order, and the preset-only ones follow them.
    order = re.findall(r'data-filter="([a-z]+)"', bar)
    own = ["s", "v", "c", "kind", "status", "current", "source", "n", "date", "added"]
    assert order == [*own, "project", "s", "added", "added"]


class _Nesting(HTMLParser):
    """Each link that opens inside another link, and each interactive element inside a
    link or a button, which HTML forbids."""

    def __init__(self) -> None:
        super().__init__()
        self.open: list[str] = []
        self.nested: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"a", "button"}:
            if self.open:
                self.nested.append(f"<{tag}> in <{self.open[-1]}>: {dict(attrs)}")
            self.open.append(tag)

    def handle_endtag(self, tag: str) -> None:
        if tag in {"a", "button"} and self.open and self.open[-1] == tag:
            self.open.pop()


def test_no_link_is_nested_in_a_link(page: str) -> None:
    """Project, profile and tally links are siblings within the card. The project
    opens in a new tab; the profile and tally links stay on the site."""
    section = page.split(SECTION, 1)[1].split("<h2", 1)[0]
    parser = _Nesting()
    parser.feed(section)
    assert parser.nested == []
    assert parser.open == []
    cards = section.split('<div class="site-card site-card-footed"')[1:]
    assert len(cards) == len(_cards(page))
    for card in cards:
        heading = card.index('class="site-card-value"')
        byline = card.index('class="site-card-byline"')
        note = card.index('class="site-card-note"')
        source = card.index('class="site-card-url"')
        assert heading < byline < source < note
        author = card.split('<p class="site-card-byline">', 1)[1].split("</p>", 1)[0]
        assert 'class="site-project-author"' in author
        assert "target=" not in author
        if foot := re.search(r'<p class="site-card-foot">(.*?)</p>', card):
            assert 'class="site-project-author"' not in foot[1]
            assert "target=" not in foot[1]
    css = render_overview.SITE_CSS.read_text(encoding="utf-8")
    assert "> a.site-card-main:is(:hover, :focus-visible)" in css
    assert ".site-card-heading, a.site-card-url" in css
    assert ".site-table-tools label[hidden] {\n  display: none;\n}" in css


@pytest.fixture(scope="module")
def browser() -> Iterator[Any]:
    sync_api = pytest.importorskip("playwright.sync_api")
    with sync_api.sync_playwright() as driver:
        try:
            launched = driver.chromium.launch(executable_path=os.environ.get(BROWSER_OVERRIDE))
        except sync_api.Error as error:
            pytest.skip(f"no Chromium to launch: {error.message.splitlines()[0]}")
        yield launched
        launched.close()


@pytest.fixture(scope="module")
def site(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """The project catalogue and results page, so a tally link between them works."""
    root = tmp_path_factory.mktemp("site")
    site_renders.write(root, "index.html", render_overview.RESULTS_PAGE)
    return root


def _follow(browser: Any, site: Path, overview: overview_data.Overview, link: str) -> Any:
    """The results page as a reader reaches it by pressing `link`, a tally's link on the
    project catalogue, on the register's reference date."""
    opened = browser.new_page(viewport={"width": 1280, "height": 900})
    noon = datetime.combine(overview_sections.reference_date(overview), time(12))
    opened.clock.set_fixed_time(noon)
    opened.goto((site / "index.html").as_uri(), wait_until="load")
    target = opened.locator(f'.site-card-foot a[href="{link}"]')
    assert target.count() == 1, link
    target.scroll_into_view_if_needed()
    target.click()
    # The results page's own load, not the navigation's: `expect_navigation` can return
    # while the new document is still parsing, and the page's programs are shared files
    # (`site_assets`) its parser waits on, so a read then finds the table unfiltered.
    opened.wait_for_url(f"**/{link}", wait_until="load")
    opened.wait_for_load_state("load")
    return opened


def test_following_a_cards_links_shows_the_rows_they_count(
    browser: Any, site: Path, overview: overview_data.Overview
) -> None:
    """In Chromium: the total of the first card that has two levels opens the results
    page on exactly that project's rows, with the count saying how many of the register
    they are and the Project control in the bar, naming the project; a level's count
    opens the same rows at that level alone, with At significance in the bar beside it.
    Setting Project back to All takes it out of the bar and shows the other projects'
    rows at that level again."""
    url, tally = next(
        (url, tally)
        for url, tally in overview_sections.ranked_projects(overview)
        if sum(bool(count) for _, count in tally.counts) > 1
    )
    slug = overview_sections.project_slug(url)
    own = sorted(result.lower() for result in tally.results)
    total = len(overview.results)
    opened = _follow(browser, site, overview, f"results.html?project={slug}")
    try:
        found = opened.evaluate(PRESETS)
    finally:
        opened.close()
    assert found["page"] == "results.html"
    assert found["search"] == f"?project={slug}"
    assert sorted(found["shown"]) == own
    assert found["total"] == total
    assert found["count"] == overview_sections.count_text(len(own), total)
    project, exact, added = found["presets"]
    assert added == {
        "filter": "added",
        "value": "",
        "choice": "All",
        "label": "Added on",
        "out": True,
    }
    assert project == {
        "filter": "project",
        "value": slug,
        "choice": overview_sections.project_name(url),
        "label": "Project",
        "out": False,
    }
    assert exact == {
        "filter": "s",
        "value": "",
        "choice": "All",
        "label": "At significance",
        "out": True,
    }

    level = next(level for level, count in tally.counts if count)
    at_level = sorted(
        result.id.lower()
        for result in overview.results
        if result.id in tally.results and overview_sections.significance(result) == level
    )
    assert 0 < len(at_level) < len(own)
    opened = _follow(browser, site, overview, f"results.html?project={slug}&s={level}")
    try:
        found = opened.evaluate(PRESETS)
        assert sorted(found["shown"]) == at_level
        assert found["count"] == overview_sections.count_text(len(at_level), total)
        assert [(preset["value"], preset["out"]) for preset in found["presets"]] == [
            (slug, False),
            (str(level), False),
            ("", True),
        ]
        assert found["presets"][1]["choice"] == f"S{level}"
        opened.select_option('select[data-filter="project"]', "")
        cleared = opened.evaluate(PRESETS)
    finally:
        opened.close()
    everyone = sorted(
        result.id.lower()
        for result in overview.results
        if overview_sections.significance(result) == level
    )
    assert sorted(cleared["shown"]) == everyone
    assert len(everyone) > len(at_level)
    assert [(preset["value"], preset["out"]) for preset in cleared["presets"]] == [
        ("", True),
        (str(level), False),
        ("", True),
    ]


def test_profile_resources_add_only_evidenced_websites_and_keep_exact_urls() -> None:
    metadata = {
        "alex": {
            "display_name": "Alex One",
            "links": [
                {"kind": "github", "url": "https://github.com/alex", "handle": "alex"},
                {"kind": "personal", "url": "https://alex.example/?one=1"},
                {"kind": "publication", "url": "https://journal.example/paper#page2"},
            ],
        }
    }
    records = site_resources.profile_resources("alex", (), metadata=metadata)
    assert [record.url for record in records] == [
        "https://alex.example/?one=1",
        "https://journal.example/paper#page2",
    ]
    assert all(record.profile_ids == ("alex",) for record in records)
    assert site_resources.profile_resources("alex", records, metadata=metadata) == records


def test_formalization_resource_names_mixed_contributors_without_claiming_authorship() -> None:
    resource = next(
        record
        for record in site_resources.resources()
        if record.url.endswith("/11SquaresFormalized")
    )
    assert resource.byline_label == "Contributors"
    assert len(resource.profile_ids) == 6
    for identifier in resource.profile_ids:
        assert resource in site_resources.resources_for_profile(identifier)
    rendered = overview_sections.resource_byline(resource, current_profile="ctjlewis")
    assert rendered.startswith("Contributors: ")
    assert "profiles/ctjlewis.html" not in rendered
    assert "profiles/julian-jj.html" in rendered
    assert (
        'profiles/manasseh-ahmed.html" data-profile-name="full">Manasseh Ahmed</a>' in rendered
    )
