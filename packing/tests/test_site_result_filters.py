"""The static homepage subset and the complete results page's browser filters.

The complete page retains pointer/keyboard, defaults, composition, counts and label
geometry checks. The homepage keeps only its declared recent rows with scripts on or
off; its ordinary link carries supported legacy filters and registered row fragments
into the complete table, where the named row must remain visible despite the filters.
The clock is fixed at the register's reference date for deterministic age checks.
"""

from __future__ import annotations

from collections.abc import Iterator
from datetime import datetime, time
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlsplit

import pytest

from devtools import (
    overview_data,
    overview_sections,
    render_recent_results,
    result_status,
    site_urls,
)
from sqpack.probes import probe
from tests import site_browser, site_renders

PROBES = Path(__file__).resolve().parent / "probes"
STATE = probe(PROBES, "site_result_filters/state")
HOME = probe(PROBES, "site_result_filters/home")
RETIRED = tuple(
    row
    for row in site_urls.load_registry()
    if row.status == "withdrawn" and row.kind == "result"
)

#: The complete table has controls; index.html has a static recent subset instead.
PAGES = {
    "all-results.html": overview_sections.RESULTS_DEFAULTS,
}
#: The widths the design is shot at: a desktop, a tablet and a phone.
WIDTHS = (1280, 768, 390)
LABEL = "Hide superseded"
STATUS = '.site-result-filters select[data-filter="status"]'
KIND = '.site-result-filters select[data-filter="kind"]'


@pytest.fixture(scope="module")
def overview() -> overview_data.Overview:
    return site_renders.overview()


@pytest.fixture(scope="module")
def browser() -> Iterator[Any]:
    with site_browser.api().sync_playwright() as driver:
        launched = site_browser.launch(driver)
        yield launched
        launched.close()


@pytest.fixture(scope="module")
def pages(tmp_path_factory: pytest.TempPathFactory) -> dict[str, Path]:
    root = tmp_path_factory.mktemp("site")
    written = site_renders.write(root, "index.html", *PAGES)
    crawl, _ = site_urls.crawl_files()
    for row in RETIRED:
        target = root / row.path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(crawl[row.path], encoding="utf-8")
        written[row.path] = target
    size = sum(path.stat().st_size for path in root.rglob("*") if path.is_file())
    assert size < 30 * 1024 * 1024, f"bounded browser fixture wrote {size} bytes"
    return written


def opened(
    browser: Any, path: Path, overview: overview_data.Overview, width: int = 1280
) -> Any:
    """The page at `path`, loaded on the register's reference date."""
    page = browser.new_page(viewport={"width": width, "height": 900})
    noon = datetime.combine(overview_sections.reference_date(overview), time(12))
    page.clock.set_fixed_time(noon)
    page.goto(path.as_uri(), wait_until="load")
    return page


def state(page: Any) -> dict[str, Any]:
    found = page.evaluate(STATE)
    assert found is not None, "the page has no results table under a filter bar"
    return found


def rows(
    overview: overview_data.Overview, defaults: overview_sections.FilterDefaults
) -> list[str]:
    """The ids of the rows a bar at `defaults` shows on the reference date, sorted."""
    reference = overview_sections.reference_date(overview)
    return sorted(
        result.id.lower()
        for result in overview.results
        if overview_sections.shown_by_default(result, defaults, reference)
    )


def count(shown: int, overview: overview_data.Overview) -> str:
    return overview_sections.count_text(shown, len(overview.results))


@pytest.mark.parametrize("name", PAGES)
def test_the_checkbox_starts_at_its_pages_default_and_the_table_with_it(
    browser: Any, pages: dict[str, Path], overview: overview_data.Overview, name: str
) -> None:
    """On load the complete page's checkbox is clear as its HTML has it; every row
    shows and the count is theirs. The rows that carry the flag are every result
    that is not superseded: the current bests, the second certificates, the better
    bounds the case records have not taken in yet (T-128, pending adoption) and the
    results that claim no bound, which have no standing, but for one the register
    declares a later result implies whole (T-031, superseded by T-060)."""
    defaults = PAGES[name]
    page = opened(browser, pages[name], overview)
    try:
        found = state(page)
    finally:
        page.close()
    assert found["type"] == "checkbox"
    assert found["label"] == LABEL
    assert found["checked"] is found["starts_checked"] is defaults.hide_superseded
    assert defaults.hide_superseded is False
    expected = rows(overview, defaults)
    assert sorted(found["shown"]) == expected
    assert found["total"] == len(overview.results)
    assert found["count"] == count(len(expected), overview)
    current = sorted(
        result.id.lower()
        for result in overview.results
        if not overview_sections.is_superseded(result)
    )
    assert sorted(found["current"]) == current
    # What stays: every standing but superseded, and a result that is no bound whatever
    # its evidence makes its standing, the limit of a method among them (T-003), unless
    # a later result is declared to imply all of it: T-031 goes, and T-036, superseded
    # only in part, stays. No result has stood as a reported second certificate since
    # 2 October 2026, when T-055's replay made it a verified one. A bound pending adoption
    # stays too: nothing has replaced it (think-h0d1).
    kept = [result for result in overview.results if result.id.lower() in current]
    assert {result.standing for result in kept} == {
        render_recent_results.HOLDS,
        render_recent_results.HOLDS_REPORTED,
        render_recent_results.SECOND_CERTIFICATE,
        render_recent_results.PENDING_ADOPTION,
        render_recent_results.NO_STANDING,
        render_recent_results.SUPERSEDED,
    }
    assert [result.id for result in kept if result.standing == "superseded"] == ["T-003"]
    pending = render_recent_results.PENDING_ADOPTION
    assert "T-128" in [result.id for result in kept if result.standing == pending]
    assert "t-031" not in current
    assert "t-036" in current
    assert set(found["current"]) < set(found["shown"])


@pytest.mark.parametrize("name", PAGES)
def test_toggling_it_hides_and_shows_the_superseded_rows(
    browser: Any, pages: dict[str, Path], overview: overview_data.Overview, name: str
) -> None:
    """A click on the label toggles the checkbox, and so does the space bar with the
    checkbox focused, reached by Tab from Standing. Checked, the table shows the rows
    the page's other defaults keep that are not superseded; clear, all the rows those
    defaults keep. The count follows each time, and the rows hidden stay in the page."""
    defaults = PAGES[name]
    checked = rows(overview, defaults._replace(hide_superseded=True))
    clear = rows(overview, defaults._replace(hide_superseded=False))
    assert set(checked) < set(clear)
    page = opened(browser, pages[name], overview)
    try:
        expected = {True: checked, False: clear}
        now = defaults.hide_superseded
        # The label is the control: a click on its words toggles the checkbox.
        for _ in range(2):
            page.get_by_text(LABEL, exact=True).click()
            now = not now
            found = state(page)
            assert found["checked"] is now
            assert sorted(found["shown"]) == expected[now]
            assert found["count"] == count(len(expected[now]), overview)
            assert found["total"] == len(overview.results)
        # The keyboard: Tab from Status lands on it, and the space bar toggles it.
        page.locator(STATUS).focus()
        page.keyboard.press("Tab")
        found = state(page)
        assert found["focused"]
        for _ in range(2):
            page.keyboard.press("Space")
            now = not now
            found = state(page)
            assert found["checked"] is now
            assert sorted(found["shown"]) == expected[now]
            assert found["count"] == count(len(expected[now]), overview)
        assert now is defaults.hide_superseded
        assert found["starts_checked"] is defaults.hide_superseded
    finally:
        page.close()


@pytest.mark.parametrize("name", PAGES)
def test_a_fresh_load_returns_to_the_pages_own_default(
    browser: Any, pages: dict[str, Path], overview: overview_data.Overview, name: str
) -> None:
    """The bar has no reset control. What a reader changed is undone by loading the page
    again, which starts from the HTML: the checkbox as that page's defaults have it, and
    the rows and the count with it."""
    defaults = PAGES[name]
    page = opened(browser, pages[name], overview)
    try:
        page.get_by_label(LABEL).set_checked(not defaults.hide_superseded)
        changed = state(page)
        assert changed["checked"] is not defaults.hide_superseded
        assert changed["starts_checked"] is defaults.hide_superseded
        assert sorted(changed["shown"]) != rows(overview, defaults)
        page.goto(pages[name].as_uri(), wait_until="load")
        found = state(page)
    finally:
        page.close()
    assert found["checked"] is defaults.hide_superseded
    assert sorted(found["shown"]) == rows(overview, defaults)
    assert found["count"] == count(len(rows(overview, defaults)), overview)


def test_it_composes_with_status_and_neither_sets_the_other(
    browser: Any, pages: dict[str, Path], overview: overview_data.Overview
) -> None:
    """Checked, with Status at All, the results page shows every result but the
    superseded ones. Status then chooses among them by a different question, how far the
    work here has gone: each status shows its rows that are not superseded, and clearing
    the box brings its superseded rows back. Superseded is no status, so no choice of
    Status leaves the box nothing to hide by itself. Neither control changes the other."""
    by_status: dict[str, list[str]] = {}
    superseded = set()
    for result in overview.results:
        by_status.setdefault(result.status, []).append(result.id.lower())
        if overview_sections.is_superseded(result):
            superseded.add(result.id.lower())
    # No result was incomplete from 2 October 2026, when the replays of T-058 and T-059
    # confirmed the last two, until the same day's finding that Nagamochi's Lemma 1 is
    # false (T-085) left T-007 at V0 with its C1 read, merged here on 3 October 2026; it is
    # the one incomplete result since. Status offers only the statuses some result has.
    assert set(by_status) == set(result_status.STATUSES)
    assert by_status[result_status.INCOMPLETE] == ["t-007"]
    offered = [status for status in result_status.STATUSES if status in by_status]
    # Some confirmed results are superseded and some are not, so the two controls differ.
    assert set(by_status["confirmed"]) & superseded
    assert set(by_status["confirmed"]) - superseded
    page = opened(browser, pages["all-results.html"], overview)
    try:
        box = page.get_by_label(LABEL)
        box.check()
        found = state(page)
        assert len(found["shown"]) == len(overview.results) - len(superseded)
        assert not set(found["shown"]) & superseded
        for status in offered:
            page.locator(STATUS).select_option(status)
            found = state(page)
            held = by_status[status]
            assert sorted(found["shown"]) == sorted(set(held) - superseded), status
            assert found["count"] == count(len(found["shown"]), overview)
            assert found["checked"]
            box.uncheck()
            found = state(page)
            assert sorted(found["shown"]) == sorted(held), status
            assert page.locator(STATUS).input_value() == status
            box.check()
    finally:
        page.close()


def test_kind_shows_the_results_of_one_kind(
    browser: Any, pages: dict[str, Path], overview: overview_data.Overview
) -> None:
    """Kind is the bar's select for what a result is. Each kind the register holds shows
    exactly its results and the count follows; All shows every row again; it composes
    with Status, so a kind with no recorded result leaves no row; and a link can preset
    it, `?kind=optimality`."""
    by_kind: dict[str, list[str]] = {}
    for result in overview.results:
        by_kind.setdefault(str(result.record["kind"]), []).append(result.id.lower())
    assert {"lower-bound", "upper-bound", "optimality", "rigidity"} <= set(by_kind)
    page = opened(browser, pages["all-results.html"], overview)
    try:
        for kind, ids in by_kind.items():
            page.locator(KIND).select_option(kind)
            found = state(page)
            assert sorted(found["shown"]) == sorted(ids), kind
            assert found["count"] == count(len(ids), overview), kind
        page.locator(KIND).select_option("rigidity")
        page.locator(STATUS).select_option("recorded")
        assert state(page)["shown"] == []
        page.locator(STATUS).select_option("")
        page.locator(KIND).select_option("")
        assert len(state(page)["shown"]) == len(overview.results)
        page.goto(pages["all-results.html"].as_uri() + "?kind=optimality", wait_until="load")
        assert page.locator(KIND).input_value() == "optimality"
        assert sorted(state(page)["shown"]) == sorted(by_kind["optimality"])
    finally:
        page.close()


def test_a_link_can_set_it_or_clear_it(
    browser: Any, pages: dict[str, Path], overview: overview_data.Overview
) -> None:
    """Both current presets apply on the complete page and leave its HTML default clear."""
    name = "all-results.html"
    for checked in (True, False):
        query = f"?current={str(checked).lower()}"
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        noon = datetime.combine(overview_sections.reference_date(overview), time(12))
        page.clock.set_fixed_time(noon)
        try:
            page.goto(pages[name].as_uri() + query, wait_until="load")
            found = state(page)
        finally:
            page.close()
        assert found["checked"] is checked, name
        assert found["starts_checked"] is PAGES[name].hide_superseded, name
        expected = rows(overview, PAGES[name]._replace(hide_superseded=checked))
        assert sorted(found["shown"]) == expected, name
        assert found["count"] == count(len(expected), overview), name


@pytest.mark.parametrize("width", WIDTHS)
@pytest.mark.parametrize("javascript", [True, False])
def test_home_includes_only_its_visible_recent_subset_and_ordinary_links(
    browser: Any,
    pages: dict[str, Path],
    overview: overview_data.Overview,
    width: int,
    *,
    javascript: bool,
) -> None:
    expected = rows(overview, overview_sections.RECENT_DEFAULTS)
    assert 0 < len(expected) < len(overview.results)
    page = browser.new_page(
        viewport={"width": width, "height": 900}, java_script_enabled=javascript
    )
    try:
        page.goto(pages["index.html"].as_uri(), wait_until="load")
        assert page.evaluate(STATE) is None, "home must not offer a filter over incomplete data"
        found = page.evaluate(HOME)
    finally:
        page.close()
    assert found is not None
    assert found["bar_count"] == found["controls"] == 0
    assert sorted(found["included"]) == sorted(found["visible"]) == expected
    assert found["hidden"] == [], "omitted results must not be duplicated as hidden rows"
    assert not found["scope_present"]
    assert sorted(found["registered"]) == sorted(r.id.lower() for r in overview.results)
    assert found["retired"] == {Path(row.path).stem: row.path for row in RETIRED}
    assert {row["result"]: row["href"] for row in found["links"]} == {
        result: f"result/{result}.html" for result in expected
    }
    assert urlsplit(found["destination"]).path.endswith("/all-results.html")
    assert found["overflow"] <= 0


@pytest.mark.parametrize("width", [1280, 390])
def test_legacy_home_query_and_registered_fragment_reach_the_complete_filtered_table(
    browser: Any,
    pages: dict[str, Path],
    overview: overview_data.Overview,
    width: int,
) -> None:
    target = "t-031"
    defaults = overview_sections.RECENT_DEFAULTS
    expected = sorted(
        result.id.lower()
        for result in overview.results
        if result.record["kind"] == "rigidity"
        and overview_sections.shown_by_default(
            result,
            defaults._replace(significance=3),
            overview_sections.reference_date(overview),
        )
    )
    assert target not in expected
    assert target not in rows(overview, defaults)
    query = "?kind=rigidity&current=true&s-min=3&age=180&utm_source=omitted"
    page = opened(browser, pages["index.html"], overview, width)
    try:
        page.goto(pages["index.html"].as_uri() + query, wait_until="load")
        # Editing the fragment in the address is a same-document reader action.
        # Initial legacy result addresses have their separate automatic-forward test.
        page.goto(pages["index.html"].as_uri() + query + f"#{target}", wait_until="load")
        home = page.evaluate(HOME)
        assert home is not None
        assert sorted(home["included"]) == rows(overview, defaults)
        assert home["bar_count"] == 0
        destination = urlsplit(home["destination"])
        assert destination.fragment == target
        assert parse_qs(destination.query) == {
            "kind": ["rigidity"],
            "current": ["true"],
            "s-min": ["3"],
            "age": ["180"],
        }
        with page.expect_navigation(wait_until="load"):
            page.get_by_role("link", name="View all results", exact=True).click()
        landed = urlsplit(page.url)
        assert landed.path.endswith("/all-results.html")
        assert landed.query == destination.query
        assert landed.fragment == target
        assert page.locator(KIND).input_value() == "rigidity"
        assert page.get_by_label(LABEL).is_checked()
        assert page.locator('[data-filter="s"][data-bound="min"]').input_value() == "3"
        assert page.locator('[data-filter="date"][data-bound="age"]').input_value() == "180"
        found = state(page)
        assert sorted(found["shown"]) == sorted([*expected, target])
        assert found["total"] == len(overview.results)
        assert found["count"] == count(len(expected) + 1, overview)
        assert page.locator(f"tr#{target}").is_visible()
    finally:
        page.close()


@pytest.mark.parametrize("fragment", ["t-999", "atlas", "%E0%A4"])
def test_unknown_home_fragments_and_unrelated_query_keys_do_not_change_the_subset(
    browser: Any,
    pages: dict[str, Path],
    overview: overview_data.Overview,
    fragment: str,
) -> None:
    page = opened(browser, pages["index.html"], overview)
    try:
        page.goto(
            pages["index.html"].as_uri() + "?current=false&unrelated=omitted#" + fragment,
            wait_until="load",
        )
        found = page.evaluate(HOME)
        assert found is not None
        assert sorted(found["included"]) == rows(overview, overview_sections.RECENT_DEFAULTS)
        assert found["hidden"] == []
        assert found["controls"] == 0
        destination = urlsplit(found["destination"])
        assert destination.fragment == ""
        assert parse_qs(destination.query) == {"current": ["false"]}
        assert urlsplit(page.url).path.endswith("/index.html"), "unknown anchors must stay put"
    finally:
        page.close()


@pytest.mark.parametrize("fragment", ["t-031", "%74-031"])
def test_initial_registered_home_result_fragment_retains_automatic_forwarding(
    browser: Any,
    pages: dict[str, Path],
    overview: overview_data.Overview,
    fragment: str,
) -> None:
    query = "?kind=rigidity&current=true&s-min=3&age=180"
    target = "t-031"
    expected = {
        result.id.lower()
        for result in overview.results
        if result.record["kind"] == "rigidity"
        and overview_sections.shown_by_default(
            result,
            overview_sections.RECENT_DEFAULTS._replace(significance=3),
            overview_sections.reference_date(overview),
        )
    }
    assert target not in expected
    page = opened(browser, pages["all-results.html"], overview)
    try:
        page.goto(pages["index.html"].as_uri() + query + "#" + fragment, wait_until="load")
        landed = urlsplit(page.url)
        assert landed.path.endswith("/all-results.html")
        assert landed.query == query.removeprefix("?")
        assert landed.fragment == fragment
        assert page.locator(KIND).input_value() == "rigidity"
        assert page.get_by_label(LABEL).is_checked()
        found = state(page)
        assert set(found["shown"]) == expected | {target}
        assert found["count"] == count(len(expected) + 1, overview)
        assert page.locator(f"tr#{target}").is_visible()
    finally:
        page.close()


def assert_tombstone(page: Any, row: site_urls.SiteURL, fragment: str, query: str) -> None:
    """The actual retained page explains the withdrawal at its registered address."""
    landed = urlsplit(page.url)
    assert landed.path.endswith("/" + row.path)
    assert landed.fragment == fragment
    assert parse_qs(landed.query) == parse_qs(query)
    assert page.get_by_role("heading", name="Withdrawn Address", exact=True).is_visible()
    assert row.tombstone in " ".join(page.locator("main").inner_text().split())
    assert page.locator('link[rel="canonical"]').get_attribute("href") == (
        site_urls.site_url() + row.canonical
    )
    assert page.get_by_role("link", name=row.target, exact=True).get_attribute("href") == (
        site_urls.site_url() + row.target
    )


@pytest.mark.parametrize("row", RETIRED, ids=lambda row: Path(row.path).stem)
@pytest.mark.parametrize("encoded", [False, True])
def test_initial_retired_home_fragments_reach_the_registered_explanation(
    browser: Any,
    pages: dict[str, Path],
    overview: overview_data.Overview,
    row: site_urls.SiteURL,
    *,
    encoded: bool,
) -> None:
    name = Path(row.path).stem
    fragment = name.replace("t", "%74", 1) if encoded else name
    query = "current=true&kind=rigidity&review=legacy"
    page = opened(browser, pages["all-results.html"], overview, 390)
    try:
        page.goto(
            pages["index.html"].as_uri() + "?" + query + "#" + fragment, wait_until="load"
        )
        assert_tombstone(page, row, fragment, query)
    finally:
        page.close()


@pytest.mark.parametrize("row", RETIRED, ids=lambda row: Path(row.path).stem)
@pytest.mark.parametrize("encoded", [False, True])
def test_retired_reader_fragment_updates_the_ordinary_home_link_and_reaches_its_tombstone(
    browser: Any,
    pages: dict[str, Path],
    overview: overview_data.Overview,
    row: site_urls.SiteURL,
    *,
    encoded: bool,
) -> None:
    name = Path(row.path).stem
    fragment = name.replace("t", "%74", 1) if encoded else name
    query = "current=true&kind=rigidity&unrelated=omitted"
    supported = "current=true&kind=rigidity"
    page = opened(browser, pages["index.html"], overview, 390)
    try:
        page.goto(pages["index.html"].as_uri() + "?" + query, wait_until="load")
        page.goto(
            pages["index.html"].as_uri() + "?" + query + "#" + fragment, wait_until="load"
        )
        home = page.evaluate(HOME)
        assert home is not None
        assert sorted(home["included"]) == rows(overview, overview_sections.RECENT_DEFAULTS)
        destination = urlsplit(home["destination"])
        assert destination.path.endswith("/" + row.path)
        assert destination.fragment == fragment
        assert parse_qs(destination.query) == parse_qs(supported)
        with page.expect_navigation(wait_until="load"):
            page.get_by_role("link", name="View all results", exact=True).click()
        assert_tombstone(page, row, fragment, supported)
    finally:
        page.close()


@pytest.mark.parametrize("row", RETIRED, ids=lambda row: Path(row.path).stem)
@pytest.mark.parametrize("javascript", [True, False])
def test_direct_retired_results_fragment_has_a_visible_static_notice_and_tombstone_link(
    browser: Any,
    pages: dict[str, Path],
    overview: overview_data.Overview,
    row: site_urls.SiteURL,
    *,
    javascript: bool,
) -> None:
    name = Path(row.path).stem
    page = browser.new_page(
        viewport={"width": 390, "height": 900}, java_script_enabled=javascript
    )
    try:
        page.goto(pages["all-results.html"].as_uri() + "#" + name, wait_until="load")
        notice = page.locator(f"p.site-withdrawn-result#{name}")
        assert notice.count() == 1, "the retained fragment needs an ordinary static notice"
        assert urlsplit(page.url).path.endswith("/all-results.html")
        assert urlsplit(page.url).fragment == name
        assert "withdrawn" in notice.inner_text()
        box = notice.bounding_box()
        assert box is not None
        # Fragment scrolling rounds the target offset to a device pixel.
        assert -0.5 <= box["y"] < box["y"] + box["height"] <= 900.5
        assert page.locator("p.site-withdrawn-result").count() == len(RETIRED)
        assert page.locator("#t-999").count() == 0, "unknown fragments must not gain anchors"
        assert page.locator("table.site-results tbody tr").count() == len(overview.results)
        found = state(page)
        assert found["total"] == len(overview.results)
        assert sorted(found["shown"]) == sorted(
            result.id.lower() for result in overview.results
        )
        assert found["count"] == count(len(overview.results), overview)
        link = notice.get_by_role(
            "link", name=f"{name.upper()} withdrawal explanation", exact=True
        )
        assert link.get_attribute("href") == row.path
        with page.expect_navigation(url=pages[row.path].as_uri(), wait_until="load"):
            link.click()
        assert_tombstone(page, row, "", "")
    finally:
        page.close()


@pytest.mark.parametrize("width", WIDTHS)
@pytest.mark.parametrize("name", PAGES)
def test_the_checkbox_and_its_label_sit_in_the_bar_at_every_width(
    browser: Any,
    pages: dict[str, Path],
    overview: overview_data.Overview,
    name: str,
    width: int,
) -> None:
    """At a desktop's, a tablet's and a phone's width the label's words are on one line
    and inside the bar, as every control's label is, and the bar has nothing running
    past it. The words are level with those of the labels on the same line, whose
    controls are taller. The checkbox takes the site's accent and is reached by Tab."""
    page = opened(browser, pages[name], overview, width)
    try:
        found = state(page)
    finally:
        page.close()
    assert found["reachable"]
    assert found["accent"] not in {"", "auto"}
    assert len(found["label_lines"]) == 1, found["label_lines"]
    assert found["label_before"] <= 0.5
    assert found["label_after"] <= 0.5
    assert found["bar_overflow"] <= 0
    (line,) = found["label_lines"]
    beside = 0
    for other in found["labels"]:
        assert other["after"] <= 0.5, other
        assert len(other["lines"]) >= 1, other
        first = other["lines"][0]
        if (
            other["filter"] != "current"
            and first["top"] < line["bottom"]
            and line["top"] < first["bottom"]
        ):
            assert first["bottom"] == pytest.approx(line["bottom"], abs=1), other
            beside += 1
    assert [other["filter"] for other in found["labels"]].count("current") == 1
    assert beside >= 1, "no label shares the checkbox's line"
