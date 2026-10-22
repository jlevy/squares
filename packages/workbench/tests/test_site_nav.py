"""The published workbench carries the site's navigation bar, the one every page carries.

No real build runs here. `build` is given a stand-in for its two child processes -- the
candidate generator and the Node corpus check -- that writes the page template where the
generator would, so what is tested is what `build` does to a page, in milliseconds. That
the bar then sits in the same box as on every other page is measured in Chromium by the
site preview, not here.
"""

from __future__ import annotations

import subprocess
from collections.abc import Sequence
from pathlib import Path

import pytest

from devtools import check_published_site, paper_structure, render_overview
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


def test_the_page_carries_the_shared_nav_with_learn_as_its_parent(page: str) -> None:
    nav = paper_structure.parse(page).find("nav", "site-nav")
    assert nav is not None
    assert nav.attrs.get("aria-label")
    active = [
        (link.text(), link.attrs.get("href"), link.attrs.get("aria-current"))
        for link in nav.walk()
        if link.tag in {"a", "button"} and link.attrs.get("aria-current")
    ]
    assert active == [
        ("Learn", None, "true"),
        ("Workbench", "../workbench/", "page"),
    ]


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


def test_the_bar_has_the_shared_five_destinations_and_direct_learning_links(page: str) -> None:
    nav = paper_structure.parse(page).find("nav", "site-nav")
    assert nav is not None
    menu = nav.find("ul", "site-nav-links")
    assert menu is not None
    entries = [
        child.find("button") or child.find("a")
        for child in menu.children
        if isinstance(child, paper_structure.Node)
    ]
    assert [(link.text(), link.attrs.get("href")) for link in entries if link] == [
        ("Overview", ".././"),
        ("News", "../news.html"),
        ("Results", None),
        ("Learn", None),
        ("About", None),
    ]
    links = {
        link.attrs.get("data-page"): link
        for link in nav.find_all("a")
        if "data-page" in link.attrs
    }
    for key, href in (
        ("atlas", "../atlas.html"),
        ("resources", "../resources.html"),
        ("film", "../visualize.html"),
        ("workbench", "../workbench/"),
    ):
        assert links[key].attrs.get("href") == href
    github = links["github"]
    assert github.attrs.get("aria-label") == "GitHub"
    assert github.attrs.get("href") == "https://github.com/jlevy/squares"
    icon = github.find("svg")
    assert icon is not None
    assert icon.attrs.get("aria-hidden") == "true"


def test_workbench_uses_shared_navigation_without_a_sibling_toggle(page: str) -> None:
    """Videos and Workbench are destinations in Learn, without a redundant switcher."""
    root = paper_structure.parse(page)
    assert not root.find_all("nav", "site-tabs")
    nav = root.find("nav", "site-nav")
    assert nav is not None
    video = next(link for link in nav.find_all("a") if link.attrs.get("data-page") == "film")
    assert video.attrs.get("href") == "../visualize.html"
    assert video.text() == "Videos"


def test_every_site_link_reaches_the_site_root(page: str) -> None:
    nav = paper_structure.parse(page).find("nav", "site-nav")
    assert nav is not None
    for link in nav.find_all("a"):
        assert link.attrs.get("href", "").startswith(("../", "https://")), link.attrs


def test_the_bar_opens_the_body_above_the_workbench(page: str) -> None:
    root = paper_structure.parse(page)
    body = root.find("body")
    assert body is not None
    first = next(child for child in body.children if isinstance(child, paper_structure.Node))
    assert "site-app-shell" in first.classes
    elements = list(body.walk())
    nav = first.find("nav", "site-nav")
    assert nav is not None
    viewport = next(node for node in elements if node.attrs.get("id") == "viewport")
    assert elements.index(nav) < elements.index(viewport)


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


def test_breadcrumbs_precede_the_application_and_match_its_learning_parent(page: str) -> None:
    root = paper_structure.parse(page)
    trail = root.find("nav", "site-breadcrumbs")
    assert trail is not None
    assert trail.find_all("a") == []
    assert trail.find_all("span")[0].text() == "Learn"
    assert trail.find_all("span")[0].attrs.get("href") is None
    current = [node for node in trail.walk() if node.attrs.get("aria-current") == "page"]
    assert len(current) == 1
    assert current[0].tag == "span"
    assert current[0].text() == "Workbench"
    elements = list(root.walk())
    viewport = next(node for node in elements if node.attrs.get("id") == "viewport")
    assert elements.index(trail) < elements.index(viewport)
    shell = root.find("div", "site-app-shell")
    assert shell is not None
    assert trail in shell.walk()
    header = shell.find("header", "kpress-site-header")
    assert header is not None
    assert trail not in header.walk()
    assert page.count(render_overview.NAVIGATION_SCRIPT.read_text(encoding="utf-8")) == 1
