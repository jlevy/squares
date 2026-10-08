"""The published workbench carries the site's navigation bar, the one every page carries.

No real build runs here. `build` is given a stand-in for its two child processes -- the
candidate generator and the Node corpus check -- that writes the page template where the
generator would, so what is tested is what `build` does to a page, in milliseconds. That
the bar then sits in the same box as on every other page is measured in Chromium by the
site preview, not here.
"""

from __future__ import annotations

import re
import subprocess
from collections.abc import Sequence
from pathlib import Path

import pytest

from devtools import check_published_site, render_overview
from devtools.site_assets import read_inline_page
from workbench_tools import build_site

TEMPLATE = build_site.WORKBENCH_PACKAGE / "assets" / "template.html"


def fake_run(args: Sequence[str], **_: object) -> subprocess.CompletedProcess[str]:
    """Write the template as the candidate `build_candidate --out DIR` would, and pass."""
    argv = [str(arg) for arg in args]
    if "--out" in argv:
        out = Path(argv[argv.index("--out") + 1])
        (out / "workbench.html").write_text(
            TEMPLATE.read_text(encoding="utf-8").replace("__DATA__", "{}"), encoding="utf-8"
        )
    return subprocess.CompletedProcess(argv, 0, "", "")


@pytest.fixture(scope="module")
def page(tmp_path_factory: pytest.TempPathFactory) -> str:
    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(build_site.subprocess, "run", fake_run)
        patch.setattr(build_site, "published_script", lambda: "loader")
        out = tmp_path_factory.mktemp("workbench")
        build_site.build(out, revision="0" * 40, dirty=False)
        return read_inline_page(out / "index.html")


def test_the_page_carries_the_shared_nav_with_visualize_current(page: str) -> None:
    nav = render_overview.nav_html("visualize", root="../")
    assert page.count(nav) == 1
    assert page.count('class="site-nav"') == 1
    current = re.findall(r'<a data-page="(\w+)"[^>]* aria-current="page"', page)
    assert current == ["visualize"]
    visualize = '<a data-page="visualize" aria-current="page" href="../visualize.html">'
    assert f"{visualize}Visualize</a>" in page


def test_the_page_carries_the_sites_head_at_the_address_it_is_served_at(page: str) -> None:
    """The published workbench had a title and nothing else, so a shared link to it
    previewed as a bare line. Its head is the site's one set (`render_overview.head_tags`)
    in place of the template's title: the workbench's own name and sentence, the address
    it is served at, and the site's card. None of it is a load, so the page stays
    self-contained, and the policy still opens the head."""
    url = render_overview.canonical_url(build_site.PAGE.path)
    assert url == render_overview.SITE_URL + "workbench/"
    assert check_published_site.head_problems(page, url) == []
    head = check_published_site.read_head(page)
    assert head.titles == ("Workbench · The Squares Project",)
    assert head.meta("og:title") == ["Workbench"]
    assert head.meta("og:type") == ["website"]
    assert head.meta("description") == [build_site.PAGE.description]
    template = TEMPLATE.read_text(encoding="utf-8")
    assert template.count("<title>Square packing workbench</title>") == 1
    assert "<title>Square packing workbench</title>" not in page
    assert page.count("<title>") == 1
    assert 'data-src="data/corpus.' in page
    assert page.index(build_site.POLICY_META) < page.index("<title>")
    with pytest.raises(ValueError, match="the page has no title"):
        build_site.with_head("<html><head></head><body></body></html>")


def test_the_bar_has_one_papers_entry_reaching_the_site_root(page: str) -> None:
    """The bar is the site's partial, so the workbench carries its Papers entry, which
    stands for the explainer and the tutorial, and no entry for either of them."""
    entries = re.findall(r'<a data-page="(\w+)"[^>]* href="([^"]+)">([^<]+)</a>', page)
    assert [key for key, _, _ in entries] == [
        "overview",
        "results",
        "papers",
        "frontier",
        "visualize",
        "github",
    ]
    assert ("papers", "../papers.html", "Papers") in entries


def test_the_page_is_the_workbench_tab_of_the_visualize_section(page: str) -> None:
    """The workbench carries the Visualize section's tabs under the bar with its own tab
    current, so an existing `workbench/` link lands on the Workbench tab beside the Film."""
    tabs = render_overview.visualize_tabs("workbench", root="../")
    assert page.count(tabs) == 1
    assert page.count('class="site-tabs"') == 1
    current = re.findall(r'<a data-tab="(\w+)" aria-current="page" href="([^"]+)"', page)
    assert current == [("workbench", "../workbench/")]
    assert '<a data-tab="film" href="../visualize.html">Film</a>' in page
    # In the header after the bar, where a kpress page of the section also puts it.
    body = page.split("<body>", 1)[1]
    bar_end = body.index("</nav>", body.index('class="site-nav"'))
    assert bar_end < body.index(tabs) < body.index("</header>") < body.index('id="viewport"')
    # The bar's stylesheet, which the page carries, draws the rule under the bar and over
    # the tabs, and keeps the tabs' own space between them and the application.
    head = page.split("</head>", 1)[0]
    for rule in (
        ".kpress-site-header:has(> .site-tabs) {\n  border-block-end: 0;\n}",
        ".kpress-site-header > .site-nav:has(+ .site-tabs) {\n  border-block-end: 1px solid",
        ".site-app-shell .site-tabs {\n  margin-block-end: var(--site-tabs-space);\n}",
    ):
        assert rule in head, rule


def test_every_site_link_reaches_the_site_root(page: str) -> None:
    nav = page.split('<nav class="site-nav"', 1)[1].split("</nav>", 1)[0]
    for href in re.findall(r'href="([^"]+)"', nav):
        assert href.startswith(("../", "https://")), href


def test_the_bar_opens_the_body_above_the_workbench(page: str) -> None:
    body = page.split("<body>", 1)[1]
    assert body.lstrip().startswith('<div class="site-app-shell">')
    assert body.index('class="site-nav"') < body.index('id="viewport"')


def test_the_theme_is_applied_before_paint_and_the_gear_is_wired(page: str) -> None:
    head = page.split("</head>", 1)[0]
    # kpress's bootstrap reads the stored choice before anything is drawn, after the policy
    # that governs it and before the workbench's own stylesheet.
    assert 'stored("kpress.theme")' in head
    assert head.index(build_site.POLICY_META) < head.index('stored("kpress.theme")')
    assert head.index(render_overview.SITE_NAV_CSS.read_text(encoding="utf-8")) < head.index(
        "__WORKBENCH_CSS__"
    )
    script = render_overview.THEME_SCRIPT.read_text(encoding="utf-8")
    assert page.count(script) == 1
    assert page.index(script) > page.index('id="viewport"')


def test_the_bar_is_set_in_its_own_face_and_fetches_nothing(page: str) -> None:
    assert 'font-family: "Source Sans 3 Variable"' in page
    assert 'url("../fonts/' not in page
    assert 'data-src="data/corpus.' in page
