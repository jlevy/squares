"""The other projects' order, their tallies of results, and the links the tallies carry.

The overview's Other Square Packing Projects section leads with the catalogues of the
record packings (the owner, 2026-10-05) and then lists each project, on GitHub or off
it, by the significance of the results the register cites from it (the owner,
2026-10-01). A card with registered results ends with a tally, `6 results (3 at S4, 3 at
S3)`, whose total opens the results table on that project's results and whose counts
open it at one significance level.

The order is one small function over the register, tested here on a synthetic register
with a tie at each step, and the rendered page is held to it. The tallies are held to the
same counts, their links to the rows they name, and their markup to valid HTML: a card
with a tally is a box holding the card's link and then the tally, since a link cannot
hold a link. The last tests follow a card's links in Chromium and read the table they
open. Skipped where no Chromium can be launched; `SQPACK_CHROMIUM` names one the
environment supplies.
"""

from __future__ import annotations

import html
import itertools
import os
import re
from collections.abc import Iterator
from datetime import datetime, time
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

import pytest

from devtools import overview_data, overview_sections, render_overview
from devtools.overview_sections import Cited, ProjectTally, project_order, project_tallies
from devtools.render_n11_lower_bounds_explainer_pdf import BROWSER_OVERRIDE
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


@pytest.fixture(scope="module")
def overview() -> overview_data.Overview:
    return site_renders.overview()


@pytest.fixture(scope="module")
def page() -> str:
    return site_renders.html("index.html")


def _attributed(overview: overview_data.Overview, url: str) -> list[overview_data.Result]:
    """A project's results, read from the register here and not through the mapping the
    page uses: those whose attribution names a key the coverage register gives a source
    at the project's address, a key `PROJECT_EXTRA_KEYS` adds, or a key the bibliography
    files under the project's venue in `SOURCE_VENUES`."""
    coverage = safe_load(overview_sections.SOURCE_COVERAGE.read_text(encoding="utf-8"))
    bibliography = safe_load(overview_data.BIBLIOGRAPHY.read_text(encoding="utf-8"))
    venue = overview_sections.SOURCE_VENUES.get(url)
    keys = (
        {
            source["source_key"]
            for source in coverage["sources"]
            if re.sub(r"/tree/.*", "", source["url"]).rstrip("/") == url.rstrip("/")
        }
        | set(overview_sections.PROJECT_EXTRA_KEYS.get(url, ()))
        | {
            entry["key"]
            for entry in bibliography["sources"]
            if venue and entry.get("venue") == venue
        }
    )
    return [
        result
        for result in overview.results
        if keys & set((result.record.get("attribution") or {}).get("source_keys") or ())
    ]


def _cards(page: str) -> list[tuple[str, str]]:
    """The section's cards in page order: each project's address and its tally's markup,
    empty for a card with none."""
    section = page.split(SECTION, 1)[1].split("<h2", 1)[0]
    found = re.findall(
        r'<a class="site-card[^"]*" href="([^"]+)"[^>]*>.*?</a>'
        r'(?:<p class="site-card-foot">(.*?)</p>)?',
        section,
        re.DOTALL,
    )
    return [(url, foot) for url, foot in found if url.startswith("https://")]


def test_the_page_lists_the_projects_in_the_functions_order(
    page: str, overview: overview_data.Overview
) -> None:
    """The rendered order is the catalogues as `CATALOGUE_SITES` writes them, then
    `ranked_projects`, computed from the register; the lists in the source keep no
    order of their own. Checked against the register directly: after the catalogues the
    tuple of counts never rises down the page, and the projects with no registered
    result come last, by name."""
    ranked = overview_sections.ranked_projects(overview)
    catalogues = [url for url, _, _, _ in overview_sections.CATALOGUE_SITES]
    assert [url for url, _ in _cards(page)] == [*catalogues, *(url for url, _ in ranked)]
    assert [url for url, _ in overview_sections.listed_projects(overview)] == [
        url for url, _ in _cards(page)
    ]
    assert {*catalogues, *(url for url, _ in ranked)} == set(overview_sections.project_urls())
    keys = []
    for url, _ in ranked:
        own = _attributed(overview, url)
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
    page: str, overview: overview_data.Overview
) -> None:
    """A project with registered results ends its card `N results (a at S5, b at S4)`:
    the total, singular for one, then each level that has a result, the highest first.
    The total links to the results page filtered to the project and each count to the
    same filter at that level. A project with no registered result has no tally."""
    with_tally = 0
    for url, foot in _cards(page):
        own = _attributed(overview, url)
        if not own:
            assert foot == "", url
            continue
        with_tally += 1
        levels = [overview_sections.significance(result) for result in own]
        slug = overview_sections.project_slug(url)
        total = f"{len(own)} result" + ("" if len(own) == 1 else "s")
        counts = [(level, levels.count(level)) for level in LEVELS if level in levels]
        text = re.sub(r"<[^>]+>", "", foot)
        assert text == f"{total} ({', '.join(f'{n} at S{level}' for level, n in counts)})", url
        links = re.findall(r'<a href="([^"]+)">([^<]+)</a>', foot)
        assert links == [
            (f"all-results.html?project={slug}", total),
            *(
                (f"all-results.html?project={slug}&amp;s={level}", f"{n} at S{level}")
                for level, n in counts
            ),
        ], url
    assert with_tally >= 9
    assert render_overview.RESULTS_PAGE == "all-results.html"


def test_a_tally_link_selects_exactly_its_projects_rows(
    overview: overview_data.Overview,
) -> None:
    """A row carries the slugs of the listed projects it is attributed to, and the
    Project preset holds a row to one of them, so the rows a tally's link shows are the
    results it counts. The results page's defaults hide no row, so the link needs to
    clear nothing; and every slug is distinct and is a choice of the Project control."""
    results = site_renders.html(render_overview.RESULTS_PAGE)
    facets = dict(re.findall(r'<tr id="(t-\d+)"[^>]*\sdata-project="([^"]*)"', results))
    assert len(facets) == len(overview.results)
    slugs = [overview_sections.project_slug(url) for url in overview_sections.project_urls()]
    assert len(set(slugs)) == len(slugs)
    for url in overview_sections.project_urls():
        slug = overview_sections.project_slug(url)
        assert re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug), slug
        rows = sorted(row for row, listed in facets.items() if slug in listed.split())
        assert rows == sorted(result.id.lower() for result in _attributed(overview, url)), url
        name = html.escape(overview_sections.project_name(url))
        assert f'<option value="{slug}">{name}</option>' in results
    assert overview_sections.FilterDefaults() == overview_sections.RESULTS_DEFAULTS
    assert not re.search(r"<tr id=\"t-\d+\"[^>]*\shidden", results)
    bar = results.split('<div class="site-table-tools site-result-filters">', 1)[1]
    bar = bar.split("</div>", 1)[0]
    assert bar.count("<label hidden>") == 2
    assert (
        '<label hidden>Project <select data-filter="project" data-bound="has" data-preset>'
        in bar
    )
    assert '<label hidden>At significance <select data-filter="s" data-preset>' in bar
    # The bar's own controls keep their order, and the preset-only ones follow them.
    order = re.findall(r'data-filter="([a-z]+)"', bar)
    own = ["s", "v", "c", "kind", "status", "current", "source", "n", "date"]
    assert order == [*own, "project", "s"]


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
    """A card with a tally is a box, not a link: its link and its tally's links are
    siblings inside it, so no link holds a link anywhere in the section. The card's own
    link still opens the project in a new tab, and the tally's links stay on the site."""
    section = page.split(SECTION, 1)[1].split("<h2", 1)[0]
    parser = _Nesting()
    parser.feed(section)
    assert parser.nested == []
    assert parser.open == []
    footed = re.findall(
        r'<div class="site-card site-card-footed" data-go="external" '
        r'data-card-size="medium"><a class="site-card-link site-card-main" '
        r'href="(https://[^"]+)" target="_blank" rel="noopener noreferrer">.*?</a>'
        r'<p class="site-card-foot">(.*?)</p></div>',
        section,
        re.DOTALL,
    )
    assert len(footed) == sum(bool(foot) for _, foot in _cards(page))
    for _, foot in footed:
        assert "target=" not in foot
    css = render_overview.SITE_CSS.read_text(encoding="utf-8")
    assert (
        ".kpress .site-card-footed:has(> .site-card-main:is(:hover, :focus-visible)) {" in css
    )
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
    opened = _follow(browser, site, overview, f"all-results.html?project={slug}")
    try:
        found = opened.evaluate(PRESETS)
    finally:
        opened.close()
    assert found["page"] == "all-results.html"
    assert found["search"] == f"?project={slug}"
    assert sorted(found["shown"]) == own
    assert found["total"] == total
    assert found["count"] == overview_sections.count_text(len(own), total)
    project, exact = found["presets"]
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
    opened = _follow(browser, site, overview, f"all-results.html?project={slug}&s={level}")
    try:
        found = opened.evaluate(PRESETS)
        assert sorted(found["shown"]) == at_level
        assert found["count"] == overview_sections.count_text(len(at_level), total)
        assert [(preset["value"], preset["out"]) for preset in found["presets"]] == [
            (slug, False),
            (str(level), False),
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
    ]
