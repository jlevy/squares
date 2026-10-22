"""The shared hierarchy agrees across navigation, visible trails and structured data."""

from __future__ import annotations

import html
import re
from html.parser import HTMLParser
from pathlib import Path
from typing import override

from devtools.site_navigation import breadcrumb_data, breadcrumbs_html, navigation_links


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
        "cases/11.html": ["Results", "Atlas", "Current <title>"],
        "result/t-060.html": ["Results", "Current <title>"],
        "profiles/person.html": ["About", "Profiles", "Current <title>"],
        "synopsis/problem.html": ["About", "Research Synopsis", "Current <title>"],
        "epistemics.html": ["Results", "Current <title>"],
        "papers/proof.html": ["Learn", "Current <title>"],
        "papers.html": ["Learn", "Current <title>"],
        "tutorials.html": ["Learn", "Current <title>"],
        "downloads.html": ["Learn", "Current <title>"],
        "resources.html": ["Learn", "Current <title>"],
        "workbench/index.html": ["Learn", "Current <title>"],
    }
    for path, expected in families.items():
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
        if expected[0] == "Learn":
            assert "item" not in items[0]
            assert "<li><span>Learn</span></li>" in trail
    for path in ("index.html", "./", "news.html", "results.html", "about.html"):
        assert not breadcrumbs_html(path, "Root page")
        assert breadcrumb_data(path, "Root page", "https://squaremath.org/") is None


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
            page.get_by_role("link", name="All Results", exact=True)
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
        assert not results.is_visible()
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
            "Atlas",
            "Tutorials",
            "Resources",
            "Documentation",
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
        "results": "results.html",
        "learn": "papers.html",
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

    for source in ("papers.html", "about.html"):
        (tmp_path / source).write_text(_browser_document())
    for destination in (
        "tutorials.html",
        "downloads.html",
        "visualize.html",
        "resources.html",
        "documentation.html",
        "report.html",
    ):
        (tmp_path / destination).write_text(
            '<h1>Complete destination</h1><section id="tutorial"></section>'
            '<section id="pdfs"></section>'
        )
    variants = {
        "papers.html#tutorial": "tutorials.html#tutorial",
        "papers.html#pdfs": "downloads.html#pdfs",
        "papers.html#visuals": "visualize.html",
        "papers.html#resources": "resources.html",
        "about.html#squares-project-documentation": "documentation.html",
        "about.html#report-your-results": "report.html",
        "about.html#contribute-your-results": "report.html",
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
