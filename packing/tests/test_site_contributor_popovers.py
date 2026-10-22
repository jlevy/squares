"""Canonical article loading, contributor transitions and native link fallbacks."""

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
NATIVE_CLICK = probe(PROBES, "contributor_popovers/native_click")
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
        "contributor-popover.js",
    )
    for name in scripts:
        (root / name).write_text((render_overview.BROWSER / name).read_text())
    (root / "site.css").write_text(render_overview.SITE_CSS.read_text())
    contributor = (
        '<div id="pop-contributor" class="site-popover site-contributor-popover" '
        'popover="auto" data-contributor-popover role="dialog" '
        'aria-label="Profile">'
        '<button class="site-popover-close" popovertarget="pop-contributor" '
        'popovertargetaction="hide">Close</button><div data-contributor-body></div>'
        '<a data-contributor-open href="profiles/walter-stromquist.html">'
        "Open profile</a></div>"
    )
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
        + contributor
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
def test_profile_content_scoped_links_and_focus(
    browser: Any, served: str, width: int, theme: str
) -> None:
    with _page(browser, viewport={"width": width, "height": 900}, color_scheme=theme) as page:
        requests: list[str] = []
        page.on("request", lambda request: requests.append(request.url))
        page.goto(served)
        link = page.locator("#profile-link")
        # The script names each link it enhances as opening a dialog; the HTML does not.
        site_browser.api().expect(link).to_have_attribute("aria-haspopup", "dialog")
        link.focus()
        page.keyboard.press("Enter")
        panel = page.locator("#pop-contributor")
        article = panel.locator("article.site-contributor")
        article.wait_for(state="visible")
        canonical = page.context.new_page()
        canonical.goto(f"{served}profiles/walter-stromquist.html")
        assert (
            article.inner_text() == canonical.locator("article.site-contributor").inner_text()
        )
        canonical.close()
        heading_id = article.locator("h1").get_attribute("id")
        assert heading_id != "title"
        assert article.get_attribute("aria-labelledby") == heading_id
        assert panel.get_attribute("aria-labelledby") == heading_id
        site_browser.api().expect(panel).to_have_accessible_name("Walter Stromquist")
        assert (
            article.locator('[data-case="11"]').get_attribute("href")
            == f"{served}cases/11.html"
        )
        assert (
            panel.locator("[data-contributor-open]").get_attribute("href")
            == f"{served}profiles/walter-stromquist.html"
        )
        article.locator('a:has-text("Biography")').click()
        assert panel.is_visible()
        # The scoped target is this load's alone, so the address keeps no fragment for it.
        assert page.url == served
        layout = page.evaluate(LAYOUT)
        assert layout["duplicateIds"] == []
        assert layout["left"] >= 0
        assert layout["right"] <= width
        assert layout["pageWidth"] <= width
        page.keyboard.press("Escape")
        site_browser.api().expect(link).to_be_focused()
        link.click()
        article.wait_for(state="visible")
        assert article.locator("h1").get_attribute("id") != heading_id
        assert requests.count(f"{served}profiles/walter-stromquist.html") == 1


@pytest.mark.parametrize("width", [1280, 390])
@pytest.mark.parametrize("theme", ["light", "dark"])
@pytest.mark.parametrize("overlay", [False, True], ids=["standalone", "popover"])
def test_generated_profile_uses_shared_roles_without_overflow(
    browser: Any,
    design_generated: str,
    tmp_path: Path,
    width: int,
    theme: str,
    *,
    overlay: bool,
) -> None:
    with _page(browser, viewport={"width": width, "height": 900}, color_scheme=theme) as page:
        if overlay:
            page.goto(f"{design_generated}title-reference.html", wait_until="load")
            page.locator('main a[href$="profiles/evan-daniel.html"]').click()
            selector = "#pop-contributor article.site-contributor"
        else:
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
        if overlay:
            assert styles["title"]["size"] == pytest.approx(styles["headline"]["size"])
            assert styles["title"]["weight"] == styles["medium"]
            assert styles["title"]["leading"] == pytest.approx(styles["headline"]["leading"])
            assert styles["title"]["family"] == styles["note"]["family"]
            assert styles["title"]["transform"] == "none"
            assert styles["body"]["family"] == styles["note"]["family"]
            assert styles["body"]["weight"] == styles["note"]["weight"]
            assert styles["left"] == pytest.approx(styles["right"], abs=1)
            assert styles["bodyClearance"] == "0px"
            assert styles["titleClearance"] == "0px"
            assert styles["panelWidth"] <= min(36 * 16, width - 32) + 1
        else:
            assert styles["body"]["family"] != styles["note"]["family"]
        assert styles["overflow"] == []
        for bounds in styles["wideBounds"]:
            assert bounds["left"] >= 0
            assert bounds["right"] <= width
        assert styles["pageWidth"] <= width
        shots = Path(os.environ.get("SQPACK_CONTRIBUTOR_DESIGN_SHOTS", str(tmp_path)))
        shots.mkdir(parents=True, exist_ok=True)
        mode = "popover" if overlay else "standalone"
        article.locator(".site-contributor-breadcrumb").scroll_into_view_if_needed()
        page.screenshot(path=str(shots / f"profile-{mode}-{width}-{theme}.png"))


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


@pytest.mark.parametrize("opener", ["case", "result"])
def test_overlay_replacement_retains_page_focus(browser: Any, served: str, opener: str) -> None:
    with _page(browser) as page:
        page.goto(served)
        origin = page.locator("#case-link" if opener == "case" else "#result-row")
        origin.click()
        source = page.locator("#pop-case" if opener == "case" else "#pop-result")
        name = source.locator('a[href$="/profiles/walter-stromquist.html"]')
        name.wait_for()
        # A name in an article cloned after start-up is announced as a dialog opener too.
        site_browser.api().expect(name).to_have_attribute("aria-haspopup", "dialog")
        name.click()
        profile = page.locator("#pop-contributor")
        profile.locator("article.site-contributor").wait_for(state="visible")
        assert not source.is_visible()
        assert page.url == served
        profile.locator('a[data-case="11"]').click()
        page.locator("#pop-case article.site-case").wait_for(state="visible")
        assert not profile.is_visible()
        page.keyboard.press("Escape")
        site_browser.api().expect(origin).to_be_focused()


def test_pressing_a_name_in_a_row_fetches_only_the_profile(browser: Any, served: str) -> None:
    """A name in a row is the name's link, not the row: pressing it opens the profile
    and starts no fetch of the row's whole result page beside it."""
    with _page(browser) as page:
        requests: list[str] = []
        page.on("request", lambda request: requests.append(request.url))
        page.goto(served)
        page.locator("#row-name").click()
        page.locator("#pop-contributor article.site-contributor").wait_for(state="visible")
        assert f"{served}profiles/evan-daniel.html" in requests
        assert f"{served}result/test.html" not in requests
        assert not page.locator("#pop-named").is_visible()
        page.keyboard.press("Escape")
        page.locator("#named-row td").first.click()
        page.locator("#pop-named article.site-result").wait_for(state="visible")
        assert requests.count(f"{served}result/test.html") == 1


def test_native_navigation_and_modified_clicks(browser: Any, served: str) -> None:
    with _page(browser, java_script_enabled=False) as page:
        page.goto(served)
        assert page.locator("#profile-link").get_attribute("aria-haspopup") is None
        page.locator("#profile-link").click()
        page.wait_for_url(f"{served}profiles/walter-stromquist.html")
        assert (
            page.locator("article.site-contributor")
            .inner_text()
            .startswith("Walter Stromquist")
        )
    with _page(browser) as page:
        page.goto(served)
        for modifier in ("ctrlKey", "metaKey", "shiftKey", "altKey"):
            assert page.evaluate(NATIVE_CLICK, modifier) is False
            assert not page.locator("#pop-contributor").is_visible()


def test_failed_fetch_follows_the_canonical_link(browser: Any, served: str) -> None:
    with _page(browser) as page:
        page.route(
            "**/profiles/walter-stromquist.html",
            lambda route: (
                route.abort() if route.request.resource_type == "fetch" else route.continue_()
            ),
        )
        page.goto(served)
        page.locator("#profile-link").click()
        page.wait_for_url(f"{served}profiles/walter-stromquist.html")
        assert page.locator("article.site-contributor h1").inner_text() == "Walter Stromquist"


def test_plain_profile_links_and_the_open_action_navigate(browser: Any, served: str) -> None:
    """A profile link is known by its address, so a container that keeps its names plain
    (News, the directory) says so once, and the panel's own **Open profile** action
    reaches the complete page rather than opening the panel again."""
    with _page(browser) as page:
        page.goto(served)
        # The script has run once the ordinary name beside the plain one is announced.
        site_browser.api().expect(page.locator("#profile-link")).to_have_attribute(
            "aria-haspopup", "dialog"
        )
        plain = page.locator("#plain-link")
        assert plain.get_attribute("aria-haspopup") is None
        plain.click()
        page.wait_for_url(f"{served}profiles/walter-stromquist.html")
    with _page(browser) as page:
        page.goto(served)
        page.locator("#profile-link").click()
        panel = page.locator("#pop-contributor")
        panel.locator("article.site-contributor").wait_for(state="visible")
        action = panel.locator("[data-contributor-open]")
        assert action.get_attribute("aria-haspopup") is None
        action.click()
        page.wait_for_url(f"{served}profiles/walter-stromquist.html")


def test_late_response_cannot_replace_newer_profile_or_reopen_after_escape(
    browser: Any, served: str
) -> None:
    with _page(browser) as page:
        held: list[Any] = []

        def hold(route: Any) -> None:
            # Playwright attaches metadata to callbacks; built-in list.append cannot hold it.
            held.append(route)

        page.route("**/profiles/walter-stromquist.html", hold)
        page.goto(served)
        page.locator("#profile-link").click()
        page.locator("#second-link").click()
        panel = page.locator("#pop-contributor")
        panel.locator('h1:has-text("Evan Daniel")').wait_for(state="visible")
        assert len(held) == 1
        held.pop().fulfill(status=200, content_type="text/html", body=PROFILE)
        page.evaluate(SETTLED)
        assert panel.locator("h1").inner_text() == "Evan Daniel"
        assert panel.get_attribute("aria-labelledby") == panel.locator("h1").get_attribute("id")
        site_browser.api().expect(panel).to_have_accessible_name("Evan Daniel")
        page.keyboard.press("Escape")
        page.locator("#profile-link").click()
        panel.locator('h1:has-text("Walter Stromquist")').wait_for(state="visible")
        site_browser.api().expect(panel).to_have_accessible_name("Walter Stromquist")
        page.keyboard.press("Escape")
        # A separate page gives the second request its own empty cache.
        page.goto(served)
        page.locator("#profile-link").click()
        page.keyboard.press("Escape")
        assert len(held) == 1
        with page.expect_response("**/profiles/walter-stromquist.html"):
            held.pop().fulfill(status=200, content_type="text/html", body=PROFILE)
        page.evaluate(SETTLED)
        assert not panel.is_visible()


@pytest.mark.parametrize("status", [200, 503], ids=["success", "failure"])
def test_native_panel_cancels_pending_profile_response(
    browser: Any, served: str, status: int
) -> None:
    with _page(browser) as page:
        held: list[Any] = []

        def hold(route: Any) -> None:
            if route.request.resource_type == "fetch":
                held.append(route)
            else:
                route.continue_()

        page.route("**/profiles/walter-stromquist.html", hold)
        page.goto(served)
        page.locator("#profile-link").click()
        page.locator("#native-opener").click()
        native = page.locator("#pop-native")
        site_browser.api().expect(native).to_be_visible()
        assert len(held) == 1
        with page.expect_response("**/profiles/walter-stromquist.html"):
            held.pop().fulfill(status=status, content_type="text/html", body=PROFILE)
        page.evaluate(SETTLED)
        assert page.url == served
        assert native.is_visible()
        assert not page.locator("#pop-contributor").is_visible()


def test_closing_source_cancels_pending_profile_failure(browser: Any, served: str) -> None:
    with _page(browser) as page:
        held: list[Any] = []

        def hold(route: Any) -> None:
            held.append(route)

        page.route("**/profiles/walter-stromquist.html", hold)
        page.goto(served)
        page.locator("#case-link").click()
        page.locator('#pop-case a[href*="/profiles/"]').click()
        page.keyboard.press("Escape")
        assert len(held) == 1
        held.pop().fulfill(status=503, content_type="text/html", body="Unavailable")
        page.evaluate(SETTLED)
        assert page.url == served
        assert not page.locator("#pop-contributor").is_visible()


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
            panel = page.locator("#pop-contributor")
            article = "article.site-contributor"
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
        breadcrumb = article.locator('.site-contributor-breadcrumb a[href="index.html"]')
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
            "Records",
            "Results",
            "Credits",
            "Years active",
            "Resources",
            "Accounts",
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
            for column, label in ((1, "Records"), (2, "Results"), (3, "Credits")):
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
            for label, column in (("Years active", 4), ("Resources", 5), ("Accounts", 6)):
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
        page.locator('nav[aria-label="Breadcrumb"] a[href="index.html"]').click()
        page.wait_for_url(f"{generated}profiles/index.html")
