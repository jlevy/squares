"""The shared hierarchy agrees across navigation, visible trails and structured data."""

from __future__ import annotations

import html
import re
from html.parser import HTMLParser
from pathlib import Path
from typing import TYPE_CHECKING, override

import pytest

from devtools.site_navigation import (
    NAVIGATION,
    breadcrumb_data,
    breadcrumbs_html,
    navigation_links,
    navigation_title,
)

if TYPE_CHECKING:
    from playwright.sync_api import FloatRect


class Tags(HTMLParser):
    def __init__(self, source: str) -> None:
        super().__init__()
        self.tags: list[tuple[str, dict[str, str | None]]] = []
        self.feed(source)

    @override
    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.tags.append((tag, dict(attrs)))


def test_navigation_marks_ancestors_without_claiming_the_parent_page() -> None:
    nav = navigation_links("cases/11.html", root="../")
    tags = Tags(nav).tags
    links = [attrs for tag, attrs in tags if tag == "a"]
    assert [
        link["data-page"]
        for tag, link in tags
        if tag in {"a", "button"}
        and link.get("class") != "site-nav-fallback"
        and link.get("data-page") in {"overview", "news", "results", "learn", "about"}
    ] == ["overview", "news", "results", "learn", "about"]
    assert any(
        link.get("data-page") == "results" and link.get("aria-current") == "true"
        for _, link in tags
    )
    assert any(
        link.get("href") == "../atlas.html" and link.get("aria-current") == "true"
        for link in links
    )
    assert not any(link.get("aria-current") == "page" for link in links)
    assert sum(attrs.get("class") == "site-nav-disclosure" for _, attrs in tags) == 3
    assert not any(
        attrs.get("role") == "menu" and attrs.get("class") == "site-nav-submenu"
        for _, attrs in tags
    )


def test_visible_and_structured_ancestry_share_paths_and_escape_titles() -> None:
    families = {
        "cases/11.html": ["Results", "Visual Atlas", "Current <title>"],
        "result/t-060.html": ["Results", "All Results", "Current <title>"],
        "results.html": ["Results", "Current <title>"],
        "profiles/person.html": ["About", navigation_title("profiles/"), "Current <title>"],
        "about.html": ["About", "Current <title>"],
        "synopsis/problem.html": ["About", "Research Synopsis", "Current <title>"],
        "epistemics.html": [
            "Results",
            navigation_title("verification.html"),
            "Current <title>",
        ],
        "papers/proof.html": ["Learn", "Papers", "Current <title>"],
        "tutorial.html": ["Learn", "Tutorials", "Current <title>"],
        "tutorial-advanced.html": ["Learn", "Tutorials", "Current <title>"],
        "papers.html": ["Learn", "Current <title>"],
        "tutorials.html": ["Learn", "Current <title>"],
        "posters.html": ["Learn", "Current <title>"],
        "resources.html": ["Learn", "Current <title>"],
        "workbench/index.html": ["Learn", "Current <title>"],
    }
    for path, expected in families.items():
        expected[-1] = navigation_title(path, expected[-1])
        trail = breadcrumbs_html(path, "Current <title>", root="../")
        labels = [
            html.unescape(re.sub(r"<[^>]+>", "", item))
            for item in re.findall(r"<li>(.*?)</li>", trail)
        ]
        assert labels == expected
        assert any(
            tag == "span" and attrs.get("aria-current") == "page"
            for tag, attrs in Tags(trail).tags
        )
        assert not any(tag == "title" for tag, _ in Tags(trail).tags)
        data = breadcrumb_data(path, "Current <title>", "https://squaremath.org/")
        assert data
        items = data["itemListElement"]
        assert [item["name"] for item in items] == expected
        canonical = path.removesuffix("index.html") if path.endswith("/index.html") else path
        assert items[-1]["item"] == f"https://squaremath.org/{canonical}"
        if expected[0] in {"Learn", "Results", "About"}:
            assert "item" not in items[0]
            assert f"<li><span>{expected[0]}</span></li>" in trail
            if expected[0] == "Learn" and len(expected) > 2:
                catalogue = "papers.html" if expected[1] == "Papers" else "tutorials.html"
                assert f'href="../{catalogue}"' in trail
    for path in ("index.html", "./", "news.html"):
        assert not breadcrumbs_html(path, "Standalone page")
        assert breadcrumb_data(path, "Standalone page", "https://squaremath.org/") is None


def test_legacy_navigation_keys_keep_the_correct_group() -> None:
    for key, group in {
        "atlas": "results",
        "papers": "learn",
        "explanations": "learn",
        "visualize": "learn",
        "github": "about",
    }.items():
        links = [attrs for _, attrs in Tags(navigation_links(key)).tags]
        assert any(
            link.get("data-page") == group and link.get("aria-current") for link in links
        )


def _browser_document() -> str:
    from devtools import render_overview  # noqa: PLC0415
    from devtools.render_n11_lower_bounds_explainer import (  # noqa: PLC0415
        kpress_css,
        kpress_static,
    )

    templates = render_overview.TEMPLATES
    css = kpress_css(kpress_static()) + "\n".join(
        (templates / name).read_text()
        for name in (
            "paper-type.css",
            "site-nav.css",
            "site.css",
            "site-contributor.css",
            "site-result.css",
        )
    )
    scripts = "\n".join(
        (render_overview.BROWSER / name).read_text()
        for name in ("navigation.js", "headroom.js")
    )
    return (
        '<!doctype html><html><head><meta charset="utf-8"><style>'
        + css
        + '</style></head><body class="kpress"><div class="kpress-site-header">'
        + navigation_links("cases/11.html")
        + "</div><main><h1>Navigation fixture</h1>"
        + '<a href="#outside" id="outside">Outside action</a>'
        + '<button popovertarget="profile">Profile</button>'
        + '<button popovertarget="result">Result</button>'
        + '<button popovertarget="case">Case</button>'
        + '<div style="height:2400px"></div>'
        + '<div class="site-popover site-contributor-popover" id="profile" popover>'
        + "<p>Profile article</p></div>"
        + '<div class="site-popover site-row-pop" id="result" popover>'
        + '<div class="site-result">Result article</div></div>'
        + '<div class="site-popover site-case-pop" id="case" popover>'
        + "<p>Wide case visualization</p></div>"
        + "</main><script>"
        + scripts
        + "</script></body></html>"
    )


def test_disclosures_work_with_keyboard_outside_click_and_mobile_menu() -> None:
    from pathlib import Path  # noqa: PLC0415

    from sqpack.probes import probe  # noqa: PLC0415
    from tests import site_browser  # noqa: PLC0415

    with site_browser.api().sync_playwright() as driver:
        browser = site_browser.launch(driver)
        page = browser.new_page(viewport={"width": 1280, "height": 800})
        page.set_content(_browser_document())
        results = page.get_by_role("button", name="Results", exact=True)
        learn = page.get_by_role("button", name="Learn", exact=True)
        results.focus()
        page.keyboard.press("Enter")
        assert results.get_attribute("aria-expanded") == "true"
        for fallback in page.locator(".site-nav-fallback").all():
            assert not fallback.is_visible()
        results.locator("svg").click()
        assert results.get_attribute("aria-expanded") == "false"
        results.click()
        assert results.get_attribute("aria-expanded") == "true"
        page.keyboard.press("Tab")
        site_browser.api().expect(
            page.get_by_role("link", name="Visual Atlas", exact=True)
        ).to_be_focused()
        page.keyboard.press("Escape")
        assert results.get_attribute("aria-expanded") == "false"
        site_browser.api().expect(results).to_be_focused()
        results.click()
        learn.click()
        assert results.get_attribute("aria-expanded") == "false"
        assert learn.get_attribute("aria-expanded") == "true"
        page.get_by_role("link", name="Outside action").click()
        assert learn.get_attribute("aria-expanded") == "false"
        assert page.url.endswith("#outside")
        page.set_viewport_size({"width": 390, "height": 800})
        menu = page.get_by_role("button", name="Menu", exact=True)
        assert menu.is_visible()
        site_browser.api().expect(results).to_be_hidden()
        menu.click()
        results.click()
        assert page.get_by_role("link", name="All Results", exact=True).is_visible()
        page.keyboard.press("Escape")
        assert results.get_attribute("aria-expanded") == "false"
        page.keyboard.press("Escape")
        assert menu.get_attribute("aria-expanded") == "false"
        site_browser.api().expect(menu).to_be_focused()
        layout = probe(Path(__file__).with_name("probes"), "site_navigation/layout")
        assert not page.evaluate(layout)["overflow"]
        browser.close()


def test_navigation_remains_reachable_without_script() -> None:
    from tests import site_browser  # noqa: PLC0415

    with site_browser.api().sync_playwright() as driver:
        browser = site_browser.launch(driver)
        page = browser.new_page(
            java_script_enabled=False, viewport={"width": 390, "height": 800}
        )
        page.set_content(_browser_document())
        for label in (
            "Overview",
            "News",
            "All Results",
            "Visual Atlas",
            "Frontier Survey",
            "Tutorials",
            "Resources",
            "Project Documentation",
        ):
            assert page.get_by_role("link", name=label, exact=True).is_visible()
        assert not page.get_by_role("button", name="Menu", exact=True).is_visible()
        browser.close()


def test_shared_popover_widths_fit_the_viewport_and_keep_the_case_stage() -> None:
    from pathlib import Path  # noqa: PLC0415

    from sqpack.probes import probe  # noqa: PLC0415
    from tests import site_browser  # noqa: PLC0415

    layout = probe(Path(__file__).with_name("probes"), "site_navigation/layout")
    with site_browser.api().sync_playwright() as driver:
        browser = site_browser.launch(driver)
        for width in (1280, 390, 320):
            page = browser.new_page(viewport={"width": width, "height": 800})
            page.set_content(_browser_document())
            sizes = {}
            for label in ("Profile", "Result", "Case"):
                page.get_by_role("button", name=label, exact=True).click()
                panel = next(
                    panel for panel in page.evaluate(layout)["panels"] if panel["width"] > 0
                )
                assert panel["left"] >= 7
                assert panel["right"] <= width - 7
                assert not panel["overflow"]
                sizes[label] = panel["width"]
                page.keyboard.press("Escape")
            assert abs(sizes["Profile"] - sizes["Result"]) < 1
            if width == 1280:
                assert sizes["Profile"] > 36 * 16
                assert sizes["Case"] > sizes["Profile"]
            page.close()
        browser.close()


def test_expand_controls_use_the_same_diagonal_glyph_and_destination_in_both_modes() -> None:
    from devtools.site_popovers import popover_controls  # noqa: PLC0415

    for sprite in (False, True):
        controls = popover_controls(
            "panel", destination=("result/t-060.html", "Open full page"), sprite=sprite
        )
        tags = Tags(controls).tags
        expand = next(attrs for tag, attrs in tags if tag == "a")
        assert expand["href"] == "result/t-060.html"
        assert expand["aria-label"] == "Open full page"
        paths = [attrs["d"] for tag, attrs in tags if tag == "path"]
        assert paths[:4] == ["M15 3h6v6", "m21 3-7 7", "M3 15v6h6", "m3 21 7-7"]
        assert not any(
            tag == "use" and attrs.get("href") == "#kpress-icon-maximize-2"
            for tag, attrs in tags
        )


def test_open_navigation_protects_the_sticky_header_without_keyboard_focus() -> None:
    from pathlib import Path  # noqa: PLC0415

    from sqpack.probes import probe  # noqa: PLC0415
    from tests import site_browser  # noqa: PLC0415

    probes = Path(__file__).with_name("probes")
    scroll = probe(probes, "site_headroom/scroll")
    blur = probe(probes, "site_navigation/blur")
    layout = probe(probes, "site_navigation/layout")
    with site_browser.api().sync_playwright() as driver:
        browser = site_browser.launch(driver)
        page = browser.new_page(
            viewport={"width": 1280, "height": 800}, reduced_motion="reduce"
        )
        page.set_content(_browser_document())
        page.locator(".site-headroom").wait_for(state="attached")
        page.get_by_role("button", name="Results", exact=True).click()
        page.evaluate(blur)
        page.evaluate(scroll, 700)
        assert page.evaluate(layout)["headerTop"] >= 0
        assert page.get_by_role("link", name="All Results", exact=True).is_visible()
        page.get_by_role("button", name="Results", exact=True).click()
        page.evaluate(blur)
        page.evaluate(scroll, 900)
        assert "site-headroom-hidden" in (
            page.locator(".site-headroom").get_attribute("class") or ""
        )
        browser.close()


def test_paper_formats_fit_between_breadcrumb_and_title_without_a_second_opening_gap() -> None:
    from devtools import render_overview  # noqa: PLC0415
    from tests import site_browser  # noqa: PLC0415

    path = "papers/example.html"
    head = _browser_document().split("</head>", 1)[0]
    publication = (render_overview.TEMPLATES / "paper-publication.css").read_text()
    document = (
        head
        + "<style>"
        + publication
        + "</style></head><body>"
        + '<main class="kpress-page-main">'
        + navigation_links(path)
        + breadcrumbs_html(path, "Paper title")
        + '<article class="kpress kpress-doc kpress-prose cert-page">'
        + '<div class="doc-links"><a class="chip" href="paper.pdf">PDF</a>'
        + '<a class="chip" href="paper.md">Markdown</a></div>'
        + '<header class="hero"><h1>Paper title</h1></header></article></main></body></html>'
    )
    with site_browser.api().sync_playwright() as driver:
        browser = site_browser.launch(driver)
        for width in (1280, 390):
            page = browser.new_page(viewport={"width": width, "height": 900})
            page.set_content(document)
            trail = page.locator(".site-breadcrumbs").bounding_box()
            title = page.get_by_role("heading", name="Paper title").bounding_box()
            formats = page.locator(".doc-links").bounding_box()
            assert trail is not None
            assert title is not None
            assert formats is not None
            assert formats["y"] >= trail["y"] + trail["height"]
            gap = title["y"] - trail["y"] - trail["height"]
            assert 24 <= gap <= 56
            page.emulate_media(media="print")
            assert not page.locator(".site-breadcrumbs").is_visible()
            page.close()
        browser.close()


def test_served_navigation_has_no_shift_when_its_controller_arrives_after_first_paint(
    tmp_path: Path,
) -> None:
    from typing import Any, Literal  # noqa: PLC0415

    from devtools import check_site_rendering, preview_site, render_overview  # noqa: PLC0415
    from devtools.render_n11_lower_bounds_explainer import (  # noqa: PLC0415
        kpress_css,
        kpress_static,
    )
    from sqpack.probes import probe  # noqa: PLC0415
    from tests import site_browser  # noqa: PLC0415

    template = (render_overview.TEMPLATES / "n11-lower-bounds-explainer-shell.html").read_text()
    template = template.replace(
        "<script>{{SITE_NAVIGATION}}</script>", '<script src="navigation.js"></script>'
    )
    values = {
        "KPRESS_CSS": kpress_css(kpress_static()),
        "PAPER_TYPE_CSS": render_overview.PAPER_TYPE_CSS.read_text(),
        "SITE_NAV_CSS": render_overview.SITE_NAV_CSS.read_text(),
        "PUBLICATION_CSS": (render_overview.TEMPLATES / "paper-publication.css").read_text(),
        "SITE_EMBED": render_overview.EMBED_SCRIPT.read_text(),
        "SITE_NAV": navigation_links("papers/n11-lower-bounds-explainer.html"),
        "BODY_HTML": "<h1>Navigation layout</h1><p>Reading content.</p>"
        '<div style="height:1800px"></div>',
        "SITE_HEADROOM": render_overview.HEADROOM_SCRIPT.read_text(),
    }
    document = re.sub(r"\{\{([A-Z_]+)\}\}", lambda match: values.get(match[1], ""), template)
    (tmp_path / "paper.html").write_text(document)
    (tmp_path / "navigation.js").write_text(render_overview.NAVIGATION_SCRIPT.read_text())
    scroll = probe(Path(__file__).with_name("probes"), "site_headroom/scroll")
    server = preview_site.serve(tmp_path, 0)
    try:
        with site_browser.api().sync_playwright() as driver:
            browser = site_browser.launch(driver)
            pending: list[Any] = []

            def hold_navigation(route: Any) -> None:
                pending.append(route)

            variants: tuple[tuple[int, Literal["light", "dark"]], ...] = (
                (1280, "light"),
                (1280, "dark"),
                (390, "light"),
                (390, "dark"),
            )
            for width, theme in variants:
                context = browser.new_context(
                    viewport={"width": width, "height": 900}, color_scheme=theme
                )
                check_site_rendering.install_observer(context)
                page = context.new_page()
                page.route("**/navigation.js", hold_navigation)
                page.goto(
                    f"http://127.0.0.1:{server.server_port}/paper.html", wait_until="commit"
                )
                heading = page.get_by_role("heading", name="Navigation layout")
                heading.wait_for(state="visible")
                check_site_rendering.wait_for_fonts(page)
                page.evaluate(scroll, 0)
                before = heading.bounding_box()
                assert before is not None
                assert len(pending) == 1
                pending.pop().continue_()
                page.wait_for_load_state("load")
                page.evaluate(scroll, 0)
                after = heading.bounding_box()
                assert after is not None
                assert abs(after["y"] - before["y"]) < 0.5
                report = check_site_rendering.read_report(page)
                assert report["cls"] <= check_site_rendering.CLS_LIMIT, report
                context.close()
            browser.close()
    finally:
        server.shutdown()
        server.server_close()


def test_group_controls_include_label_and_chevron_and_start_with_substantive_content() -> None:
    nav = navigation_links("tutorials.html")
    controls = re.findall(r'<button[^>]+class="site-nav-disclosure"[^>]*>(.*?)</button>', nav)
    assert [html.unescape(re.sub(r"<[^>]+>", "", content)) for content in controls] == [
        "Results",
        "Learn",
        "About",
    ]
    assert all(any(tag == "svg" for tag, _ in Tags(content).tags) for content in controls)
    for group, target in {
        "results": "atlas.html",
        "learn": "tutorials.html",
        "about": "about.html",
    }.items():
        menu = re.search(rf'<ul id="site-nav-{group}"[^>]*>(.*?)</ul>', nav)
        assert menu is not None
        links = [attrs for tag, attrs in Tags(menu[1]).tags if tag == "a"]
        assert links[0]["href"] == target
        assert all("#" not in (link["href"] or "") for link in links)
    assert any(
        attrs.get("data-page") == "learn" and tag == "span" and "href" not in attrs
        for tag, attrs in Tags(nav).tags
    )
    for label in ("The Squares Project", "Contributor Profiles"):
        assert label in nav


def test_legacy_catalogue_fragments_keep_queries_and_reach_substantive_pages(
    tmp_path: Path,
) -> None:
    from devtools import preview_site  # noqa: PLC0415
    from tests import site_browser  # noqa: PLC0415

    for source in ("papers.html", "about.html", "results.html", "posters.html"):
        document = _browser_document()
        if source == "results.html":
            document = document.replace(
                "<main>",
                '<main><h1>Complete destination</h1><section id="all-results"></section>',
                1,
            )
        (tmp_path / source).write_text(document)
    for destination in (
        "tutorials.html",
        "posters.html",
        "papers.html",
        "visualize.html",
        "resources.html",
        "documentation.html",
        "report.html",
    ):
        body = (
            '<h1>Complete destination</h1><section id="tutorial"></section>'
            '<section id="pdfs"></section>'
        )
        if destination in {"papers.html", "posters.html"}:
            body = _browser_document().replace("<main>", "<main>" + body, 1)
        (tmp_path / destination).write_text(body)
    variants = {
        "papers.html#tutorial": "tutorials.html#tutorial",
        "papers.html#pdfs": "posters.html#pdfs",
        "posters.html#paper-editions": "papers.html",
        "papers.html#visuals": "visualize.html",
        "papers.html#resources": "resources.html",
        "about.html#squares-project-documentation": "documentation.html",
        "about.html#report-your-results": "report.html",
        "about.html#contribute-your-results": "report.html",
        "results.html#recent-arrivals": "results.html#all-results",
        "results.html#added-in-the-last-seven-days": ("results.html#all-results"),
        "results.html#earlier-results-by-week-published": ("results.html#all-results"),
    }
    server = preview_site.serve(tmp_path, 0)
    try:
        with site_browser.api().sync_playwright() as driver:
            browser = site_browser.launch(driver)
            page = browser.new_page()
            base = f"http://127.0.0.1:{server.server_port}/"
            for source, destination in variants.items():
                source_path, fragment = source.split("#", 1)
                target_path, _, target_fragment = destination.partition("#")
                query = "?keep=1&filter=complete"
                expected = (
                    base
                    + target_path
                    + query
                    + ("#" + target_fragment if target_fragment else "")
                )
                for loaded_source in (False, True):
                    if loaded_source:
                        page.goto(base + source_path + query)
                    page.goto(base + source_path + query + "#" + fragment)
                    page.wait_for_url(expected)
                    assert page.get_by_role("heading", name="Complete destination").is_visible()
            browser.close()
    finally:
        server.shutdown()
        server.server_close()


def test_every_shell_aligns_the_trail_with_header_text_and_preserves_35em_prose() -> None:
    from devtools import render_overview  # noqa: PLC0415
    from devtools.measure_site_pages import TYPOGRAPHY  # noqa: PLC0415
    from tests import site_browser  # noqa: PLC0415

    prose = '<p id="reading">A reading paragraph with the shared body measure.</p>'
    wide = (
        '<div class="site-wide"><div class="site-table-wrap"><table>'
        "<tr><td>Wide data</td></tr></table></div></div>"
    )
    ordinary = render_overview.kpress_page(
        "# Tutorials\n\n" + prose + wide,
        name="tutorials.html",
        current="learn",
        title="Tutorials",
        description="Reading-width fixture.",
        toc=False,
        prepare_math=False,
    ).html
    profile = render_overview.static_content_page(
        '<article class="site-contributor"><h1>Contributor profile</h1>' + prose + "</article>",
        meta=render_overview.PageMeta(
            "Contributor profile", "A profile.", "profiles/person.html"
        ),
        current="profiles",
    ).html
    directory = render_overview.static_content_page(
        '<section class="site-contributor-directory"><h1>Contributor Profiles</h1>'
        + prose
        + wide
        + "</section>",
        meta=render_overview.PageMeta("Contributor Profiles", "Profiles.", "profiles/"),
        current="profiles",
    ).html
    css = _browser_document().split("<style>", 1)[1].split("</style>", 1)[0]
    publication = (render_overview.TEMPLATES / "paper-publication.css").read_text()
    paper = (
        "<!doctype html><html><head></head><body>"
        '<main class="kpress-page-main kpress-viewport">'
        + navigation_links("papers/example.html")
        + breadcrumbs_html("papers/example.html", "Paper")
        + '<div class="kpress kpress-doc kpress-prose cert-page"><h1>Paper</h1>'
        + prose
        + "</div></main></body></html>"
    )
    with site_browser.api().sync_playwright() as driver:
        browser = site_browser.launch(driver)
        for width in (1440, 1256, 768, 390, 320):
            page = browser.new_page(viewport={"width": width, "height": 900})
            for name, source in (
                ("ordinary", ordinary),
                ("profile", profile),
                ("directory", directory),
                ("paper", paper),
            ):
                document = source.replace(
                    "</head>", "<style>" + css + publication + "</style></head>"
                )
                page.set_content(document)
                found = page.evaluate(TYPOGRAPHY)
                trail = found["breadcrumb"]
                text = page.locator("#reading").bounding_box()
                brand = page.locator(".site-name-text:visible").bounding_box()
                assert trail is not None, (name, width, found)
                assert text is not None, (name, width, found)
                assert brand is not None, (name, width, found)
                first = page.locator(".site-breadcrumbs li").first.bounding_box()
                assert first is not None
                assert abs(first["x"] - brand["x"]) < 0.5, (name, width, found)
                assert text["width"] <= 35 * 18 + 0.5, (name, width, found)
                if width >= 768:
                    assert abs(text["width"] - 35 * 18) < 0.5, (name, width, found)
                assert text["x"] >= 8, (name, width, found)
                assert text["x"] + text["width"] <= width - 8, (name, width, found)
                if name in {"ordinary", "directory"} and width >= 1256:
                    frame = page.locator(".site-wide").bounding_box()
                    assert frame is not None
                    assert frame["width"] > text["width"]
            page.close()
        browser.close()


def test_disclosure_and_chevron_motion_share_timing_and_respect_reduced_motion() -> None:
    from sqpack.probes import probe  # noqa: PLC0415
    from tests import site_browser  # noqa: PLC0415

    motion = probe(Path(__file__).with_name("probes"), "site_navigation/motion")
    with site_browser.api().sync_playwright() as driver:
        browser = site_browser.launch(driver)
        for width in (1280, 390):
            for reduced in ("no-preference", "reduce"):
                page = browser.new_page(
                    viewport={"width": width, "height": 900}, reduced_motion=reduced
                )
                page.set_content(_browser_document())
                if width < 768:
                    page.get_by_role("button", name="Menu", exact=True).click()
                for label in ("Results", "Learn", "About"):
                    trigger = page.get_by_role("button", name=label, exact=True)
                    trigger.click()
                    state = page.evaluate(motion)
                    expected = 0 if reduced == "reduce" else 0.14
                    assert state["chevron"]["duration"] == [expected]
                    assert state["panel"]["duration"] == [expected] * 3
                    assert state["panel"]["properties"] == ["opacity", "transform", "display"]
                    if width < 768:
                        assert state["mobile"]["duration"] == [expected] * 3
                    if reduced == "reduce":
                        assert state["panel"]["opacity"] == 1
                        assert state["panel"]["animations"] == 0
                        assert state["chevron"]["animations"] == 0
                    panel = page.locator("#" + (trigger.get_attribute("aria-controls") or ""))
                    trigger.click()
                    site_browser.api().expect(panel).to_be_hidden()
                    assert panel.get_attribute("inert") is not None
                page.close()
        browser.close()


def test_results_container_names_and_marks_each_substantive_destination() -> None:
    group = next(item for item in NAVIGATION if item.key == "results")
    destinations = tuple((item.path, item.label) for item in group.children)
    for path, label in destinations:
        nav = navigation_links(path)
        menu = re.search(r'<ul id="site-nav-results"[^>]*>(.*?)</ul>', nav)
        assert menu is not None
        assert [html.unescape(text) for text in re.findall(r"<a[^>]*>(.*?)</a>", menu[1])] == [
            name for _, name in destinations
        ]
        links = [attrs for tag, attrs in Tags(menu[1]).tags if tag == "a"]
        assert [link["href"] for link in links] == [target for target, _ in destinations]
        assert [link["href"] for link in links if link.get("aria-current") == "page"] == [path]
        controls = [
            (tag, attrs) for tag, attrs in Tags(nav).tags if attrs.get("data-page") == "results"
        ]
        assert {tag for tag, _ in controls} == {"span", "button"}
        assert all(attrs.get("aria-current") == "true" for _, attrs in controls)
        trail = breadcrumbs_html(path, label)
        assert "<li><span>Results</span></li>" in trail
        assert not any(tag == "a" for tag, _ in Tags(trail).tags)
        assert f'<span aria-current="page">{label}</span>' in trail


def test_menu_destinations_supply_canonical_titles_and_categories_have_no_urls() -> None:
    for group in NAVIGATION:
        if group.children:
            assert not group.path
        for item in (group, *group.children):
            if not item.path:
                continue
            if item.path == "./":
                # The homepage keeps the name its renderer gives it, the project's
                # (the owner, 2026-10-23), and is Overview only when it is given none.
                assert navigation_title(item.path, "The Squares Project") == (
                    "The Squares Project"
                )
                assert navigation_title(item.path) == item.label == "Overview"
            else:
                assert navigation_title(item.path, "Stale page title") == item.label
            trail = breadcrumbs_html(item.path, "Stale page title")
            data = breadcrumb_data(item.path, "Stale page title", "https://squaremath.org/")
            if not group.children:
                assert not trail
                assert data is None
                continue
            assert f'<span aria-current="page">{html.escape(item.label)}</span>' in trail
            assert data
            assert data["itemListElement"][-1]["name"] == item.label
            if group.children:
                assert f"<li><span>{group.label}</span></li>" in trail
                assert "item" not in data["itemListElement"][0]
    assert navigation_title("papers/specific-proof.html", "Specific proof") == "Specific proof"
    assert navigation_title("visualize") == navigation_title("visualize.html")
    assert navigation_title("profiles/index.html") == navigation_title("profiles/")
    about = breadcrumbs_html("about.html", "Stale project title")
    assert not any(tag == "a" for tag, _ in Tags(about).tags)


def test_short_card_groups_align_their_outer_edges_with_prose_for_every_size() -> None:
    from tests import site_browser  # noqa: PLC0415

    groups = []
    for size in ("small", "medium", "large"):
        for count in (1, 2):
            most = ' data-cards-most="3"' if count == 1 else ""
            card_markup = "".join(
                f'<a class="site-card" data-card-size="{size}" href="#reading">Card {n}</a>'
                for n in range(count)
            )
            groups.append(
                f'<div class="site-cards-frame site-wide" id="{size}-{count}">'
                f'<div class="site-cards"{most}>{card_markup}</div></div>'
            )
    head = _browser_document().split("</head>", 1)[0]
    document = (
        head + '</head><body><main class="kpress-page-main kpress-viewport">'
        '<article class="kpress kpress-doc"><div class="kpress-doc-layout">'
        '<div class="kpress-prose kpress-long-text site-page">'
        '<p id="reading">Shared prose column.</p>'
        + "".join(groups)
        + "</div></div></article></main></body></html>"
    )
    with site_browser.api().sync_playwright() as driver:
        browser = site_browser.launch(driver)
        for width in (1280, 768, 390, 320):
            page = browser.new_page(viewport={"width": width, "height": 900})
            page.set_content(document)
            prose = page.locator("#reading").bounding_box()
            assert prose is not None
            for size in ("small", "medium", "large"):
                for count in (1, 2):
                    frame = page.locator(f"#{size}-{count}")
                    box = frame.bounding_box()
                    cards: list[FloatRect] = []
                    for card in frame.locator(".site-card").all():
                        card_box = card.bounding_box()
                        assert card_box is not None
                        cards.append(card_box)
                    assert box is not None
                    assert abs(box["x"] - prose["x"]) < 0.5
                    assert abs(box["width"] - prose["width"]) < 0.5
                    assert abs(min(card["x"] for card in cards) - prose["x"]) < 0.5
                    right = max(card["x"] + card["width"] for card in cards)
                    assert abs(right - prose["x"] - prose["width"]) < 0.5
                    if count == 2 and width >= 768:
                        assert abs(cards[0]["y"] - cards[1]["y"]) < 0.5
                    if width < 768:
                        assert all(abs(card["width"] - prose["width"]) < 0.5 for card in cards)
            page.close()
        browser.close()


def test_menu_chevrons_keep_down_up_endpoints_and_reverse_their_travel() -> None:
    from sqpack.probes import probe  # noqa: PLC0415
    from tests import site_browser  # noqa: PLC0415

    motion = probe(Path(__file__).with_name("probes"), "site_navigation/motion")
    with site_browser.api().sync_playwright() as driver:
        browser = site_browser.launch(driver)
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        page.set_content(_browser_document())
        button = page.get_by_role("button", name="Results", exact=True)
        assert button.locator("path").get_attribute("d") == "m6 9 6 6 6-6"
        button.click()
        opened = page.evaluate(motion)["chevron"]
        assert opened["keyframes"][-1] == "rotate(-180deg)"
        page.wait_for_timeout(170)
        button.click()
        closed = page.evaluate(motion)["chevrons"]["results"]
        assert closed["keyframes"][-1] == "rotate(0deg)"
        browser.close()


def test_text_buttons_and_actions_share_the_same_small_tracking() -> None:
    import pytest  # noqa: PLC0415

    from sqpack.probes import probe  # noqa: PLC0415
    from tests import site_browser  # noqa: PLC0415

    motion = probe(Path(__file__).with_name("probes"), "site_navigation/motion")
    controls = (
        '<a class="site-action" href="#reading">Browse</a>'
        '<a class="site-popover-action" href="#reading">Open</a>'
        '<div class="site-news-filters"><div class="site-tabs">'
        '<button class="site-chip">Topic</button></div></div>'
    )
    document = _browser_document().replace("</main>", controls + "</main>")
    with site_browser.api().sync_playwright() as driver:
        browser = site_browser.launch(driver)
        for width in (1280, 390):
            page = browser.new_page(viewport={"width": width, "height": 900})
            page.set_content(document)
            labels = page.evaluate(motion)["labels"]
            assert {"Browse", "Open", "Topic"} <= {item["label"] for item in labels}
            assert all(item["tracking"] == pytest.approx(0.021, abs=0.00001) for item in labels)
            page.close()
        browser.close()


@pytest.fixture(scope="module")
def reading_width_pages() -> dict[str, str]:
    """Actual page producers, rendered in setup without building the publication tree."""
    from devtools import render_contributors, site_assets  # noqa: PLC0415
    from tests import site_renders  # noqa: PLC0415

    names = (
        "index.html",
        "news.html",
        "results.html",
        "verification.html",
        "about.html",
        "tutorials.html",
        "papers.html",
        "resources.html",
        "posters.html",
        "documentation.html",
        "report.html",
        "epistemics.html",
        "tutorial.html",
        "tutorial-advanced.html",
    )
    assets = site_assets.shared().assets
    documents = {name: assets.inlined(site_renders.html(name)) for name in names}
    documents.update(
        {
            page.name: assets.inlined(page.html)
            for page in render_contributors.contributor_pages()
            if page.name in {"profiles/index.html", "profiles/joshua-levy.html"}
        }
    )
    return documents


def test_actual_page_families_share_the_prose_measure_and_card_outer_edges(
    reading_width_pages: dict[str, str],
) -> None:
    from sqpack.probes import probe  # noqa: PLC0415
    from tests import site_browser  # noqa: PLC0415

    measure = probe(Path(__file__).with_name("probes"), "site_navigation/reading-widths")
    with site_browser.api().sync_playwright() as driver:
        browser = site_browser.launch(driver)
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        # Layout uses the real inlined styles; missing pictures cannot change its tracks.
        page.route("**/*", lambda route: route.abort())
        for name, document in reading_width_pages.items():
            page.set_content(document, wait_until="load")
            for width in (1440, 1256, 768, 390, 320):
                page.set_viewport_size({"width": width, "height": 900})
                found = page.evaluate(measure)
                column = found["root"]
                assert column["width"] <= 630.5, (name, width, found)
                if width >= 768:
                    assert abs(column["width"] - 630) < 0.5, (name, width, found)
                assert column["left"] >= 8, (name, width, found)
                assert column["right"] <= width - 8, (name, width, found)
                for paragraph in found["paragraphs"]:
                    # Bordered callouts/News cards disclose their inset separately.
                    if paragraph["card"] is None:
                        assert abs(paragraph["width"] - column["width"]) < 0.5, (
                            name,
                            width,
                            paragraph,
                        )
                for frame in (*found["cards"], *found["news"]):
                    assert abs(frame["left"] - column["left"]) < 0.5, (name, width, frame)
                    assert abs(frame["width"] - column["width"]) < 0.5, (name, width, frame)
                trail, brand = found["firstTrail"], found["brand"]
                if name in {"index.html", "news.html"}:
                    assert trail is None, name
                else:
                    assert trail is not None, (name, width, found)
                    assert brand is not None, (name, width, found)
                    assert abs(trail["left"] - brand["left"]) < 0.5, (name, width, found)
        browser.close()


@pytest.mark.parametrize("width", [1280, 390])
def test_breadcrumb_links_underline_only_on_hover_and_keep_keyboard_focus(width: int) -> None:
    from tests import site_browser  # noqa: PLC0415

    document = _browser_document().replace(
        "<main>", "<main>" + breadcrumbs_html("tutorial.html", "Tutorial")
    )
    with site_browser.api().sync_playwright() as driver:
        browser = site_browser.launch(driver)
        page = browser.new_page(viewport={"width": width, "height": 900})
        page.set_content(document)
        link = page.locator('.site-breadcrumbs a[href="tutorials.html"]')
        site_browser.api().expect(link).to_have_css("text-decoration-line", "none")
        link.hover()
        site_browser.api().expect(link).to_have_css("text-decoration-line", "underline")
        page.mouse.move(0, 0)
        site_browser.api().expect(link).to_have_css("text-decoration-line", "none")
        link.focus()
        site_browser.api().expect(link).to_be_focused()
        site_browser.api().expect(link).not_to_have_css("outline-style", "none")
        site_browser.api().expect(link).not_to_have_css("outline-width", "0px")
        browser.close()


def test_theme_control_uses_the_shared_contrast_icon_size_and_keeps_its_name() -> None:
    from tests import site_browser  # noqa: PLC0415

    with site_browser.api().sync_playwright() as driver:
        browser = site_browser.launch(driver)
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        page.set_content(_browser_document())
        button = page.get_by_role("button", name="Color theme", exact=True)
        icon = button.locator("svg")
        assert icon.locator('circle[r="10"]').count() == 1
        assert icon.locator('path[fill="currentColor"]').count() == 1
        site_browser.api().expect(icon.locator("path")).not_to_have_css("fill", "none")
        box = icon.bounding_box()
        reference = page.locator(".site-nav-disclosure .site-nav-icon").first.bounding_box()
        assert box is not None
        assert reference is not None
        assert box["width"] == reference["width"]
        assert box["height"] == reference["height"]
        button.click()
        site_browser.api().expect(page.get_by_role("menu", name="Color theme")).to_be_visible()
        browser.close()


def test_current_category_keeps_the_shared_underline_on_descendant_pages() -> None:
    from tests import site_browser  # noqa: PLC0415

    destinations = {
        "result/t-037.html": "Results",
        "profiles/joshua-levy.html": "About",
        "papers/proof.html": "Learn",
        "tutorial.html": "Learn",
        "results.html": "Results",
        "about.html": "About",
        "index.html": "Overview",
        "news.html": "News",
    }
    with site_browser.api().sync_playwright() as driver:
        browser = site_browser.launch(driver)
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        for path, label in destinations.items():
            document = _browser_document().replace(
                navigation_links("cases/11.html"), navigation_links(path)
            )
            page.set_content(document)
            role = "button" if label in {"Results", "Learn", "About"} else "link"
            active = page.get_by_role(role, name=label, exact=True)
            site_browser.api().expect(active).to_have_css("text-decoration-line", "underline")
            site_browser.api().expect(active).to_have_css("text-decoration-thickness", "2px")
            active.hover()
            site_browser.api().expect(active).to_have_css("text-decoration-line", "underline")
            active.focus()
            site_browser.api().expect(active).not_to_have_css("outline-style", "none")
            for other in ("Results", "Learn", "About"):
                if other != label:
                    site_browser.api().expect(
                        page.get_by_role("button", name=other, exact=True)
                    ).to_have_css("text-decoration-line", "none")
        browser.close()


def test_profile_sections_keep_navigation_roles_and_tallies_precede_resources() -> None:
    from devtools import render_contributors  # noqa: PLC0415
    from sqpack.contributor_occurrences import load_occurrences  # noqa: PLC0415
    from sqpack.contributors import load_contributors  # noqa: PLC0415
    from sqpack.probes import probe  # noqa: PLC0415
    from tests import site_browser  # noqa: PLC0415

    person = load_contributors().by_id["oscar-fitzharding"]
    article = render_contributors.contributor_article(person, load_occurrences().occurrences)
    head = _browser_document().split("</head>", 1)[0]
    document = (
        head
        + '</head><body class="kpress"><main class="site-page kpress-prose">'
        + article
        + '<section><h2 id="exposition">A Mathematical Argument</h2></section>'
        + "</main></body></html>"
    )
    measure = probe(Path(__file__).with_name("probes"), "site_navigation/presentation")
    with site_browser.api().sync_playwright() as driver:
        browser = site_browser.launch(driver)
        for width in (1280, 390):
            page = browser.new_page(viewport={"width": width, "height": 900})
            page.set_content(document)
            found = page.evaluate(measure)
            assert found["profileHeadings"]
            for heading in found["profileHeadings"]:
                assert "Source Sans" in heading["family"]
                assert heading["style"] == "normal"
                assert heading["weight"] == "550"
            assert "PT Serif" in found["exposition"]["family"]
            assert found["exposition"]["style"] == "italic"
            assert len(found["tallies"]) == 3
            assert all(
                current["bottom"] <= following["top"]
                for current, following in zip(
                    found["tallies"], found["tallies"][1:], strict=False
                )
            )
            assert found["tallies"][-1]["bottom"] < found["resourcesTop"]
            assert not found["overflow"]
            page.close()
        browser.close()


def test_tallies_widen_their_dots_and_stand_one_shared_space_clear() -> None:
    """The two tally tokens, measured in Chromium (the owner, 2026-10-23): every dot in a
    tally, the directory's summary and a profile's resource cards alike, is the shared
    separator, each word space beside it 0.15em wider; and a tally set as a line of its
    own, the directory's summary and a profile's stacked counts, has 1.25rem (20px)
    above and below, or a neighbour's larger margin where one meets it."""
    from devtools import render_contributors  # noqa: PLC0415
    from sqpack.contributor_occurrences import load_occurrences  # noqa: PLC0415
    from sqpack.contributors import load_contributors  # noqa: PLC0415
    from sqpack.probes import probe  # noqa: PLC0415
    from tests import site_browser  # noqa: PLC0415

    occurrences = load_occurrences().occurrences
    person = load_contributors().by_id["oscar-fitzharding"]
    directory = (
        '<article class="site-contributor-directory"><h1>Contributor Profiles</h1>'
        "<p>People whose work the record cites.</p>"
        + render_contributors.profile_summary([person], occurrences)
        + '<div class="site-table-wrap site-wide"><table class="site-table"><tbody>'
        "<tr><td>Row</td></tr></tbody></table></div></article>"
    )
    head = _browser_document().split("</head>", 1)[0]
    document = (
        head
        + '</head><body class="kpress"><main class="site-page kpress-prose">'
        + directory
        + render_contributors.contributor_article(person, occurrences)
        + "</main></body></html>"
    )
    measure = probe(Path(__file__).with_name("probes"), "site_tallies/spacing")
    with site_browser.api().sync_playwright() as driver:
        browser = site_browser.launch(driver)
        for width in (1280, 390):
            page = browser.new_page(viewport={"width": width, "height": 900})
            page.set_content(document)
            found = page.evaluate(measure)
            assert sorted(line["kind"] for line in found["lines"]) == ["profile", "summary"]
            for line in found["lines"]:
                assert line["marginTop"] == line["marginBottom"] == 20, line
                assert line["above"] >= 19.5, line
                assert line["below"] >= 19.5, line
            # The summary's four dots, and at least one on a resource card's tally.
            assert len(found["dots"]) > 4
            for dot in found["dots"]:
                assert dot["shared"], dot
                assert abs(dot["wordSpacing"] - 0.15 * dot["fontSize"]) < 0.01, dot
                if dot["before"] is not None:
                    assert dot["before"] > dot["wordSpacing"], dot
                    assert abs(dot["before"] - dot["after"]) < 0.5, dot
            assert not found["overflow"]
            page.close()
        browser.close()


def test_case_property_badges_use_the_same_text_and_height_as_tags() -> None:
    from devtools.overview_sections import case_status_chip  # noqa: PLC0415
    from devtools.result_overview import case_badges  # noqa: PLC0415
    from sqpack.probes import probe  # noqa: PLC0415
    from tests import site_browser  # noqa: PLC0415

    head = _browser_document().split("</head>", 1)[0]
    document = (
        head + '</head><body class="kpress"><main class="site-page">'
        '<table class="site-table site-frontier"><tbody><tr><td>'
        + case_status_chip("proved")
        + case_badges(11)
        + "</td></tr></tbody></table></main></body></html>"
    )
    measure = probe(Path(__file__).with_name("probes"), "site_navigation/presentation")
    with site_browser.api().sync_playwright() as driver:
        browser = site_browser.launch(driver)
        for width in (1280, 390):
            page = browser.new_page(viewport={"width": width, "height": 900})
            page.set_content(document)
            found = page.evaluate(measure)
            assert found["badges"]
            for badge in found["badges"]:
                assert badge["size"] == found["tag"]["size"]
                assert abs(badge["height"] - found["tag"]["height"]) < 0.5
                assert badge["label"]
                assert badge["width"] == badge["height"]
            page.close()
        browser.close()
