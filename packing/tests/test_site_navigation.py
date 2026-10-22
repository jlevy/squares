"""The shared hierarchy agrees across navigation, visible trails and structured data."""

from __future__ import annotations

import html
import re
from html.parser import HTMLParser
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
        for link in links
        if link.get("data-page") in {"overview", "news", "results", "learn", "about"}
    ] == ["overview", "news", "results", "learn", "about"]
    assert any(
        link.get("data-page") == "results" and link.get("aria-current") == "true"
        for link in links
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
    for path in ("index.html", "./", "news.html", "results.html", "papers.html", "about.html"):
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
        links = [attrs for tag, attrs in Tags(navigation_links(key)).tags if tag == "a"]
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
        results = page.get_by_role("button", name="Results links")
        learn = page.get_by_role("button", name="Learn links")
        results.focus()
        page.keyboard.press("Enter")
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
        page.get_by_role("button", name="Results links").click()
        page.evaluate(blur)
        page.evaluate(scroll, 700)
        assert page.evaluate(layout)["headerTop"] >= 0
        assert page.get_by_role("link", name="All Results", exact=True).is_visible()
        page.get_by_role("button", name="Results links").click()
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
