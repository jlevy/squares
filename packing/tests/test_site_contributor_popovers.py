"""Native profile navigation, profile design, and retained case/result loading races."""

from __future__ import annotations

import contextlib
import json
import os
from collections.abc import Iterator
from dataclasses import replace
from pathlib import Path
from typing import Any

import pytest

from devtools import (
    preview_site,
    render_case_pages,
    render_contributors,
    render_overview,
    site_assets,
)
from sqpack.contributor_occurrences import load_occurrences
from sqpack.contributors import ContributorSource, load_contributors
from sqpack.probes import probe
from tests import site_browser

PROBES = Path(__file__).parent / "probes"
LAYOUT = probe(PROBES, "contributor_popovers/layout")
SETTLED = probe(PROBES, "contributor_popovers/settled")
DESIGN = probe(PROBES, "contributor_popovers/design")
HEADING = probe(PROBES, "contributor_popovers/heading")
PROFILE = (
    '<article class="site-contributor" aria-labelledby="title">'
    '<h1 id="title">Walter Stromquist</h1><p>A mathematical contributor.</p>'
    '<a href="../cases/11.html" data-case="11">Case 11</a>'
    '<a href="#bio">Biography</a><p id="bio">Published biographical evidence.</p>'
    '<a href="../profiles/evan-daniel.html">Evan Daniel</a>'
    '<a href="https://example.org/">Public website</a></article>'
)
SECOND = (
    '<article class="site-contributor"><h1>Evan Daniel</h1>'
    "<p>Another contributor.</p></article>"
)
CASE = (
    '<article class="site-case" data-case="11"><h1 id="title">Case 11</h1>'
    '<a href="../profiles/walter-stromquist.html">'
    'Walter Stromquist</a><a href="12.html" data-case-step="12" rel="next">Next</a></article>'
)
RESULT = (
    '<article class="site-result" data-result-overview="t-test"><h1 id="title">Result</h1>'
    '<a href="../profiles/walter-stromquist.html">'
    "Walter Stromquist</a></article>"
)


@pytest.fixture(scope="module")
def browser() -> Iterator[Any]:
    with site_browser.api().sync_playwright() as driver:
        launched = site_browser.launch(driver)
        yield launched
        launched.close()


@pytest.fixture(scope="module")
def served(tmp_path_factory: pytest.TempPathFactory) -> Iterator[str]:
    """Controlled articles exercise races using the retained production programs/CSS."""
    root = tmp_path_factory.mktemp("contributor-popovers")
    scripts = (
        "article-loader.js",
        "popover.js",
        "row-popover.js",
        "case-popover.js",
    )
    for name in scripts:
        (root / name).write_text((render_overview.BROWSER / name).read_text())
    (root / "site.css").write_text(render_overview.SITE_CSS.read_text())
    body = (
        '<h1 id="title">Host title</h1><main><a id="profile-link" '
        'href="profiles/walter-stromquist.html">Walter Stromquist</a>'
        '<a id="second-link" href="profiles/evan-daniel.html">Evan Daniel</a>'
        # A container that keeps its names plain links, as News does.
        '<p data-contributor-plain><a id="plain-link" href="profiles/walter-stromquist.html">'
        "Walter Stromquist</a></p>"
        '<a id="case-link" href="cases/11.html" data-case="11">Case 11</a><table><tbody>'
        '<tr id="result-row" data-row-popover="pop-result"><td>Result details</td></tr>'
        # A row naming a person, as a results table's credit cell does.
        '<tr id="named-row" data-row-popover="pop-named"><td>Named result</td><td>'
        '<a id="row-name" href="profiles/evan-daniel.html">'
        "Evan Daniel</a></td></tr>"
        '</tbody></table><button id="native-opener" popovertarget="pop-native">'
        'Open native panel</button><div id="pop-native" class="site-popover" '
        'popover="auto">Native panel content</div>'
        '<div id="pop-result" class="site-popover" popover="auto">'
        '<button class="site-popover-close" popovertarget="pop-result" '
        'popovertargetaction="hide">Close</button><div data-row-pop-src="result/test.html">'
        '<a href="result/test.html">Read result</a></div></div>'
        '<div id="pop-named" class="site-popover" popover="auto">'
        '<button class="site-popover-close" popovertarget="pop-named" '
        'popovertargetaction="hide">Close</button><div data-row-pop-src="result/test.html">'
        '<a href="result/test.html">Read result</a></div></div>'
        + render_case_pages.case_popover()
        + "</main>"
    )
    document = (
        '<!doctype html><html><head><meta name="viewport" content="width=device-width">'
        '<link rel="stylesheet" href="site.css"></head><body class="kpress">'
        + body
        + "".join(f'<script src="{name}"></script>' for name in scripts)
        + "</body></html>"
    )
    (root / "index.html").write_text(document)
    for name, article in {
        "profiles/walter-stromquist.html": PROFILE,
        "profiles/evan-daniel.html": SECOND,
        "cases/11.html": CASE,
        "cases/12.html": CASE.replace('data-case="11"', 'data-case="12"'),
        "result/test.html": RESULT,
    }.items():
        target = root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(f"<!doctype html><html><body>{article}</body></html>")
    server = preview_site.serve(root, 0)
    try:
        yield f"http://127.0.0.1:{server.server_port}/"
    finally:
        server.shutdown()
        server.server_close()


@pytest.fixture(scope="module")
def generated(tmp_path_factory: pytest.TempPathFactory) -> Iterator[str]:
    """Real profiles and small record articles use production shells and script order."""
    root = tmp_path_factory.mktemp("generated-contributor-popovers")
    pages = render_contributors.contributor_pages()
    case = CASE.replace('data-case="11"', 'data-case="10"').replace("Case 11", "Case 10")
    for name, article in (("cases/10.html", case), ("result/test.html", RESULT)):
        pages.append(
            render_overview.static_content_page(
                article.replace("../profiles/", "profiles/"),
                meta=render_overview.PageMeta("Record", "A record for browser checks.", name),
                current="",
            )
        )
    for record in pages:
        target = root / record.name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(record.html)
    site_assets.write_assets(root, site_assets.shared().assets.files())
    server = preview_site.serve(root, 0)
    try:
        yield f"http://127.0.0.1:{server.server_port}/"
    finally:
        server.shutdown()
        server.server_close()


@pytest.fixture(scope="module")
def design_generated(tmp_path_factory: pytest.TempPathFactory) -> Iterator[str]:
    """Production articles and shells with long public source identifiers and URLs."""
    root = tmp_path_factory.mktemp("contributor-design")
    contributor = load_contributors().by_id["evan-daniel"]
    contributor = replace(
        contributor,
        sources=(
            *contributor.sources,
            ContributorSource(
                id="public-source-" + "archived-evidence-" * 16 + "record",
                locator="Public URL: https://example.org/" + "sourcepath" * 40,
                url="https://example.org/" + "sourcepath" * 40,
            ),
        ),
    )
    profile = render_overview.static_content_page(
        render_contributors.contributor_article(contributor, load_occurrences().occurrences),
        meta=render_overview.PageMeta(
            contributor.display_name, "Contributor design regression.", contributor.profile_path
        ),
        current="",
    )
    directory = render_contributors.contributor_pages()[0]
    reference = render_overview.static_content_page(
        '<article class="title-reference"><h1>Shared page title</h1>'
        '<a href="profiles/evan-daniel.html">'
        "Evan Daniel</a></article>",
        meta=render_overview.PageMeta(
            "Shared page title", "Standard page heading reference.", "title-reference.html"
        ),
        current="",
    )
    for record in (profile, directory, reference):
        target = root / record.name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(record.html)
    site_assets.write_assets(root, site_assets.shared().assets.files())
    server = preview_site.serve(root, 0)
    try:
        yield f"http://127.0.0.1:{server.server_port}/"
    finally:
        server.shutdown()
        server.server_close()


@contextlib.contextmanager
def _page(browser: Any, **options: Any) -> Iterator[Any]:
    context = browser.new_context(**options)
    try:
        yield context.new_page()
    finally:
        context.close()


@pytest.mark.parametrize("width", [1280, 390])
@pytest.mark.parametrize("theme", ["light", "dark"])
def test_generated_profile_uses_shared_roles_without_overflow(
    browser: Any,
    design_generated: str,
    tmp_path: Path,
    width: int,
    theme: str,
) -> None:
    with _page(browser, viewport={"width": width, "height": 900}, color_scheme=theme) as page:
        page.goto(f"{design_generated}profiles/evan-daniel.html", wait_until="load")
        selector = "main article.site-contributor"
        article = page.locator(selector)
        article.wait_for(state="visible")
        assert page.locator("html").get_attribute("data-kpress-resolved-theme") == theme
        for disclosure in article.locator("details").all():
            if disclosure.get_attribute("open") is None:
                disclosure.locator(":scope > summary").click()
        styles = page.evaluate(DESIGN, selector)
        assert styles["body"]["size"] == pytest.approx(18)
        assert styles["notes"]
        for note in styles["notes"]:
            assert note["size"] == pytest.approx(styles["note"]["size"])
            assert note["family"] == styles["note"]["family"]
            assert note["weight"] == styles["note"]["weight"]
            expected_color = (
                styles["foreground"] if note["primary"] else styles["note"]["color"]
            )
            assert note["color"] == expected_color
            assert note["wrap"] != "anywhere"
        assert all(term["weight"] == styles["medium"] for term in styles["terms"])
        assert styles["headings"]
        for heading in styles["headings"]:
            assert heading["size"] == pytest.approx(styles["section"]["size"])
            assert heading["leading"] == pytest.approx(styles["section"]["leading"])
        assert styles["body"]["family"] != styles["note"]["family"]
        assert styles["breadcrumbGap"] == pytest.approx(2.5 * 16, abs=1)
        assert styles["overflow"] == []
        for bounds in styles["wideBounds"]:
            assert bounds["left"] >= 0
            assert bounds["right"] <= width
        assert styles["pageWidth"] <= width
        shots = Path(os.environ.get("SQPACK_CONTRIBUTOR_DESIGN_SHOTS", str(tmp_path)))
        shots.mkdir(parents=True, exist_ok=True)
        article.locator("h1").scroll_into_view_if_needed()
        page.screenshot(path=str(shots / f"profile-{width}-{theme}.png"))


@pytest.mark.parametrize("width", [1280, 390])
@pytest.mark.parametrize("theme", ["light", "dark"])
@pytest.mark.parametrize("record", ["profiles/index.html", "profiles/evan-daniel.html"])
def test_generated_contributor_page_titles_match_the_shared_page_role(
    browser: Any,
    design_generated: str,
    tmp_path: Path,
    width: int,
    *,
    theme: str,
    record: str,
) -> None:
    with _page(browser, viewport={"width": width, "height": 900}, color_scheme=theme) as page:
        page.goto(f"{design_generated}title-reference.html", wait_until="load")
        reference = page.evaluate(HEADING, "main .title-reference > h1")
        assert reference["family"] == reference["sans"]
        assert reference["transform"] == "uppercase"
        assert reference["fontStyle"] == "normal"
        page.goto(f"{design_generated}{record}", wait_until="load")
        heading = page.locator("main article > h1")
        site_browser.api().expect(heading).to_be_visible()
        styles = page.evaluate(HEADING, "main article > h1")
        assert styles == reference
        tmp_path.joinpath("heading.json").write_text(json.dumps(styles, indent=2))
        if (
            width == 1280
            and theme == "light"
            and (directory := os.environ.get("SQPACK_CONTRIBUTOR_DESIGN_SHOTS"))
        ):
            Path(directory).mkdir(parents=True, exist_ok=True)
            name = "directory" if record.endswith("index.html") else "profile"
            page.screenshot(path=str(Path(directory) / f"page-title-{name}.png"))


def test_late_result_body_waits_for_next_opening(browser: Any, served: str) -> None:
    with _page(browser) as page:
        held: list[Any] = []

        def hold(route: Any) -> None:
            held.append(route)

        page.route("**/result/test.html", hold)
        page.goto(served)
        row = page.locator("#result-row")
        row.click()
        page.keyboard.press("Escape")
        assert len(held) == 1
        held.pop().fulfill(status=200, content_type="text/html", body=RESULT)
        page.evaluate(SETTLED)
        assert page.locator("#pop-result article").count() == 0
        row.click()
        page.locator("#pop-result article.site-result").wait_for(state="visible")
        assert held == []


def test_pending_case_can_be_reopened_after_escape(browser: Any, served: str) -> None:
    with _page(browser) as page:
        held: list[Any] = []

        def hold(route: Any) -> None:
            held.append(route)

        page.route("**/cases/11.html", hold)
        page.goto(served)
        link = page.locator("#case-link")
        link.click()
        page.keyboard.press("Escape")
        link.click()
        assert len(held) == 1
        held.pop().fulfill(status=200, content_type="text/html", body=CASE)
        page.locator("#pop-case article.site-case").wait_for(state="visible")
        page.keyboard.press("Escape")
        site_browser.api().expect(link).to_be_focused()


@pytest.mark.parametrize(
    "record", ["profiles/walter-stromquist.html", "cases/10.html", "result/test.html"]
)
def test_generated_standalone_pages_enhance_article_links(
    browser: Any, generated: str, record: str
) -> None:
    with _page(browser, viewport={"width": 390, "height": 900}, color_scheme="dark") as page:
        address = f"{generated}{record}"
        page.goto(address, wait_until="load")
        if record.startswith("profiles/"):
            if directory := os.environ.get("SQPACK_CONTRIBUTOR_DESIGN_SHOTS"):
                page.evaluate(DESIGN, "main article.site-contributor")
                target = Path(directory) / "real-profile-standalone-390-dark.png"
                target.parent.mkdir(parents=True, exist_ok=True)
                page.screenshot(path=str(target))
            link = page.locator('main article.site-contributor a[data-case="10"]').first
            reviewed_work = page.locator(
                'main article.site-contributor details:has(a[data-case="10"])'
            )
            if reviewed_work.count() and reviewed_work.get_attribute("open") is None:
                reviewed_work.locator(":scope > summary").click()
            panel = page.locator("#pop-case")
            article = "article.site-case"
        else:
            link = page.locator('main a[href$="profiles/walter-stromquist.html"]')
            assert link.get_attribute("aria-haspopup") is None
            link.click()
            site_browser.api().expect(page).to_have_url(
                f"{generated}profiles/walter-stromquist.html"
            )
            assert page.locator("[data-contributor-popover]").count() == 0
            return
        site_browser.api().expect(link).to_be_visible(timeout=2000)
        link.click()
        site_browser.api().expect(panel).to_be_visible(timeout=2000)
        assert panel.locator(article).is_visible()
        assert page.url == address
        page.keyboard.press("Escape")
        site_browser.api().expect(link).to_be_focused()


def test_generated_profile_keeps_its_own_anchors_and_breadcrumb_plain(
    browser: Any, generated: str
) -> None:
    """A profile's in-page anchors resolve to a profile address, the page's own, and its
    breadcrumb to the directory; neither opens the panel."""
    with _page(browser, viewport={"width": 1280, "height": 900}) as page:
        address = f"{generated}profiles/walter-stromquist.html"
        page.goto(address, wait_until="load")
        article = page.locator("main article.site-contributor")
        anchors = article.locator('a[href^="#"]')
        assert anchors.count() > 0
        for index in range(anchors.count()):
            assert anchors.nth(index).get_attribute("aria-haspopup") is None
        breadcrumb = page.get_by_role("navigation", name="Breadcrumb").get_by_role(
            "link", name="Contributor Profiles", exact=True
        )
        assert breadcrumb.get_attribute("aria-haspopup") is None
        for disclosure in article.locator("details").all():
            if disclosure.get_attribute("open") is None:
                disclosure.locator(":scope > summary").click()
        anchor = anchors.first
        target = anchor.get_attribute("href")
        anchor.click()
        assert page.url == f"{address}{target}"
        assert not page.locator("#pop-contributor").is_visible()


@pytest.mark.parametrize("javascript", [False, True], ids=["no-javascript", "javascript"])
def test_generated_directory_keeps_native_profile_navigation(
    browser: Any, generated: str, *, javascript: bool
) -> None:
    with _page(
        browser,
        java_script_enabled=javascript,
        viewport={"width": 390, "height": 900},
        color_scheme="dark",
    ) as page:
        page.goto(f"{generated}profiles/index.html", wait_until="load")
        directory = page.evaluate(LAYOUT)["directory"]
        assert directory["headers"] == [
            "Name",
            "Accounts",
            "Records",
            "Results",
            "Credits",
            "Years active",
            "Resources",
        ]
        name_keys = [row["keys"][0] for row in directory["rows"]]
        assert name_keys == sorted(name_keys)
        assert {item["column"] for item in directory["tallies"]} == {
            "site-profile-records",
            "site-profile-stats",
            "site-profile-credits",
        }
        for item in directory["tallies"]:
            assert item["levelsTop"] >= item["totalBottom"] - 1
            assert item["totalColor"] == item["tallyColor"]
            assert item["levelsColor"] != item["totalColor"]
            assert all(color == item["levelsColor"] for color in item["levelLinkColors"])
        if javascript:
            assert (
                page.get_by_role("columnheader", name="Name", exact=True).get_attribute(
                    "aria-sort"
                )
                == "ascending"
            )
            for column, label in ((2, "Records"), (3, "Results"), (4, "Credits")):
                heading = page.get_by_role("columnheader", name=label, exact=True)
                heading.focus()
                heading.press("Enter")
                rows = page.evaluate(LAYOUT)["directory"]["rows"]
                values = [int(row["keys"][column]) for row in rows]
                assert values == sorted(values), label
                assert heading.get_attribute("aria-sort") == "ascending"
                heading.press("Space")
                rows = page.evaluate(LAYOUT)["directory"]["rows"]
                values = [int(row["keys"][column]) for row in rows]
                assert values == sorted(values, reverse=True), label
                assert heading.get_attribute("aria-sort") == "descending"
            for label, column in (("Years active", 5), ("Resources", 6), ("Accounts", 1)):
                heading = page.get_by_role("columnheader", name=label, exact=True)
                for _ in range(2):
                    heading.click()
                    rows = page.evaluate(LAYOUT)["directory"]["rows"]
                    missing = [not row["keys"][column].strip() for row in rows]
                    assert missing == sorted(missing), label
        public = page.get_by_role("link", name="GitHub: evand (Evan Daniel)", exact=True)
        assert public.get_attribute("href") == "https://github.com/evand"
        page.route(
            "https://github.com/evand", lambda route: route.fulfill(body="Public account")
        )
        public.click()
        page.wait_for_url("https://github.com/evand")
        page.go_back(wait_until="load")
        link = page.get_by_role("link", name="Walter Stromquist", exact=True)
        if javascript:
            row = page.get_by_role("row").filter(has=link)
            row.dispatch_event("click", {"ctrlKey": True})
            assert page.url == f"{generated}profiles/index.html"
            row.dispatch_event("click")
        else:
            link.click()
        page.wait_for_url(f"{generated}profiles/walter-stromquist.html")
        assert (
            page.locator("main article.site-contributor h1").text_content()
            == "Walter Stromquist"
        )
        page.get_by_role("navigation", name="Breadcrumb").get_by_role(
            "link", name="Contributor Profiles", exact=True
        ).click()
        page.wait_for_url(f"{generated}profiles/")


@pytest.mark.parametrize("selector", ["#profile-link", "#row-name"])
@pytest.mark.parametrize("javascript", [False, True])
def test_person_links_navigate_instead_of_opening_panels(
    browser: Any, served: str, selector: str, *, javascript: bool
) -> None:
    with _page(browser, java_script_enabled=javascript) as page:
        page.goto(served)
        link = page.locator(selector)
        href = link.get_attribute("href")
        assert href
        assert href.startswith("profiles/")
        assert link.get_attribute("aria-haspopup") is None
        link.focus()
        page.keyboard.press("Enter")
        site_browser.api().expect(page).to_have_url(served + href)
