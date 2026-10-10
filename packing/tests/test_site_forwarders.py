"""A page that moved or was withdrawn still arrives, in a browser.

`render_overview.forwarder_pages` writes a forwarder at each address a page used to
have (`MOVED_PAGES`): three repository documents that left the site, and the two papers,
which moved to `papers/<slug>.html` on 2026-10-01 (think-cmz6). Links to the papers' old
addresses are in dated records, in other people's pages and in readers' bookmarks, most
of them with a fragment: a section, a footnote, the explainer's certificate picker.

`tests/node/overview_forward` runs the script against a stand-in document. Whether a
forwarder forwards is the browser's to say: a script that replaces the location, a
refresh inside `<noscript>`, and a relative address resolved from a directory. So this
opens the forwarders themselves, as they are written, and reads where the browser ends
up: with scripts, at the target with the query string and the fragment the reader came
with; without scripts, at the target by the refresh. It does that from files and a
local HTTP address for every forwarder, where the real overview and case index are
served beside stand-in papers and `check_published_site` is asked the same of the site,
which is the check a deploy is held to. A target off the site, the defect log on GitHub,
is answered by a stand-in, so no test reaches the network.

Skipped where no Chromium can be launched; `SQPACK_CHROMIUM` names one the environment
supplies, as the other browser tools read it.
"""

from __future__ import annotations

import contextlib
import os
import socket
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest

from devtools import check_published_site, render_case_pages, render_overview
from devtools.overview_sections import LOWER_BOUNDS_PAPER, OPTIMALITY_PAPER
from devtools.preview_site import serve
from devtools.repo_links import REPO_URL
from tests import site_browser, site_renders

#: What stands at each target: a page with nothing to run and nothing to fetch.
STAND_IN = "<!doctype html><title>target</title><p>target</p>"
DEFECTS = f"{REPO_URL}/blob/main/defects.md"
#: Real fragments and a real query string an old link to a paper carries: a section of
#: each paper, a footnote, the explainer's certificate picker and its review switch.
EXPLAINER_LINKS = ("#proof-of-the-new-lower-bound", "#fn-3", "?review=fonts#381-100")
REVIEW_LINKS = ("#the-result", "#fn-1", "?view=embed#fn-3")


@pytest.fixture(scope="module")
def browser() -> Iterator[Any]:
    sync_api = site_browser.api()
    with sync_api.sync_playwright() as driver:
        launched = site_browser.launch(driver)
        yield launched
        launched.close()


def _stand_ins(root: Path) -> None:
    """A stand-in page at each address of the site a forwarder sends a reader to."""
    for _, new in render_overview.MOVED_PAGES:
        if not new.startswith("https://") and new != "atlas.html":
            (root / new).parent.mkdir(parents=True, exist_ok=True)
            (root / new).write_text(STAND_IN, encoding="utf-8")
    # A registered individual-case target exercises selector forwarding separately
    # from the real generated index, which must never be a directory listing.
    (root / render_case_pages.case_url(17)).write_text(STAND_IN, encoding="utf-8")


@pytest.fixture(scope="module")
def site(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """The forwarders as the site writes them, beside a stand-in for each target page."""
    root = tmp_path_factory.mktemp("forwarders")
    render_overview.write_site(
        root,
        [*render_overview.forwarder_pages(), site_renders.page("atlas.html")],
    )
    _stand_ins(root)
    return root


def _free_port() -> int:
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        return int(probe.getsockname()[1])


@pytest.fixture(scope="module")
def served(tmp_path_factory: pytest.TempPathFactory) -> Iterator[str]:
    """The forwarders and the overview as they are rendered, beside the stand-ins, served
    on a local address as a deployed site is on its own; the address, with its closing
    slash. SQPACK_SITE_PREVIEW_URL reuses an existing local build without copying it.
    A directory's address and the overview's fragment forwarding need a server."""
    if live := os.environ.get("SQPACK_SITE_PREVIEW_URL"):
        yield live.rstrip("/") + "/"
        return
    container = tmp_path_factory.mktemp("served")
    root = container / "squares"
    root.mkdir()
    files = [
        *render_overview.forwarder_pages(),
        site_renders.page("index.html"),
        site_renders.page("atlas.html"),
    ]
    render_overview.write_site(root, files)
    _stand_ins(root)
    server = serve(container, _free_port(), as_pages=True)
    try:
        yield f"http://127.0.0.1:{server.server_port}/squares/"
    finally:
        server.shutdown()
        server.server_close()


def _arrives(
    browser: Any, address: str, expected: str, *, scripts: bool, atlas: bool = False
) -> str:
    """Where a reader who opens `address` ends up, with or without scripts, once the
    browser has had the chance to reach `expected`."""
    sync_api = pytest.importorskip("playwright.sync_api")
    context = browser.new_context(java_script_enabled=scripts)
    try:
        context.route(
            f"{REPO_URL}/**",
            lambda route: route.fulfill(status=200, content_type="text/html", body=STAND_IN),
        )
        page = context.new_page()
        page.goto(address, wait_until="load")
        # A page that never arrives is left where it is, and the caller compares.
        with contextlib.suppress(sync_api.TimeoutError):
            page.wait_for_url(expected, timeout=5000)
        if atlas:
            assert page.locator("h1#the-atlas-of-square-packings").text_content() == (
                "The Atlas of Square Packings"
            )
            assert page.locator('tr#n-17 a[data-case="17"]').first.get_attribute("href") == (
                "cases/17.html"
            )
            assert page.locator('link[rel="canonical"]').get_attribute("href") == (
                render_overview.canonical_url("atlas.html")
            )
            fragment = page.url.rsplit("#", 1)[-1]
            if fragment.startswith("n-") and fragment[2:].isdigit():
                row = page.locator(f"tr#{fragment}")
                if row.count():
                    assert row.is_visible()
        return page.url
    finally:
        context.close()


def _arrivals(root: str) -> dict[str, str]:
    """Where each old address should arrive, for a site whose root is `root`."""
    return {
        "results.html": f"{root}/all-results.html",
        "status.html": f"{root}/atlas.html",
        "frontier.html": f"{root}/atlas.html",
        "defects.html": DEFECTS,
        "explainer.html": f"{root}/{LOWER_BOUNDS_PAPER}",
        "n11-optimality/t-060-explainer.html": f"{root}/{OPTIMALITY_PAPER}",
        "n11-optimality/index.html": f"{root}/{OPTIMALITY_PAPER}",
        "cases.html": f"{root}/atlas.html",
        "cases/index.html": f"{root}/atlas.html",
    }


def test_each_old_address_arrives_with_its_query_and_fragment(browser: Any, site: Path) -> None:
    moved = dict(render_overview.MOVED_PAGES)
    assert moved["results.html"] == "all-results.html"
    assert moved["status.html"] == "atlas.html"
    assert moved["frontier.html"] == "atlas.html"
    assert moved["defects.html"] == DEFECTS
    assert moved["explainer.html"] == LOWER_BOUNDS_PAPER
    root = site.as_uri()
    arrivals = _arrivals(root)
    assert set(arrivals) == set(moved)
    for old, target in arrivals.items():
        assert (
            _arrives(
                browser,
                f"{root}/{old}",
                target,
                scripts=True,
                atlas=old in {"cases.html", "cases/index.html"},
            )
            == target
        ), old
        kept = f"{target}?view=embed#retained-forwarder-fragment"
        came = f"{root}/{old}?view=embed#retained-forwarder-fragment"
        assert (
            _arrives(
                browser,
                came,
                kept,
                scripts=True,
                atlas=old in {"cases.html", "cases/index.html"},
            )
            == kept
        ), old


@pytest.mark.parametrize(
    "suffix",
    [
        "#n-291",
        "?recent=true#n-291",
        "#the-frontier-survey",
        "#the-survey",
        "?view=embed#frontier-table",
    ],
)
def test_legacy_frontier_row_section_and_query_links_arrive_on_atlas(
    browser: Any, served: str, suffix: str
) -> None:
    arrival = f"{served}atlas.html{suffix}"
    assert _arrives(browser, f"{served}frontier.html{suffix}", arrival, scripts=True) == arrival


def test_without_scripts_the_refresh_still_arrives(browser: Any, site: Path) -> None:
    """A reader without scripts is sent on by the refresh, which cannot keep a fragment."""
    root = site.as_uri()
    for old, target in _arrivals(root).items():
        assert (
            _arrives(
                browser,
                f"{root}/{old}",
                target,
                scripts=False,
                atlas=old in {"cases.html", "cases/index.html"},
            )
            == target
        ), old
        assert (
            _arrives(
                browser,
                f"{root}/{old}#fn-3",
                target,
                scripts=False,
                atlas=old in {"cases.html", "cases/index.html"},
            )
            == target
        ), old


@pytest.mark.parametrize("suffix", EXPLAINER_LINKS)
def test_the_explainers_old_address_arrives_at_the_paper(
    served: str, browser: Any, suffix: str
) -> None:
    """`explainer.html`, with the fragment and the query string an old link carried."""
    arrival = served + LOWER_BOUNDS_PAPER + suffix
    assert (
        _arrives(browser, f"{served}explainer.html{suffix}", arrival, scripts=True) == arrival
    )


@pytest.mark.parametrize("old", ["n11-optimality/t-060-explainer.html", "n11-optimality/"])
@pytest.mark.parametrize("suffix", REVIEW_LINKS)
def test_the_optimality_papers_old_addresses_arrive_at_the_paper(
    served: str, browser: Any, old: str, suffix: str
) -> None:
    """Its page and the directory it was linked by, which the forwarder a level down
    has to climb out of."""
    arrival = served + OPTIMALITY_PAPER + suffix
    assert _arrives(browser, f"{served}{old}{suffix}", arrival, scripts=True) == arrival


def test_the_optimality_papers_directory_arrives_without_scripts(
    served: str, browser: Any
) -> None:
    """The refresh of a directory's index is resolved from the directory."""
    arrival = served + OPTIMALITY_PAPER
    assert _arrives(browser, f"{served}n11-optimality/#fn-1", arrival, scripts=False) == arrival


def test_the_overview_sends_an_old_explainer_fragment_to_the_paper(
    served: str, browser: Any
) -> None:
    """The explainer was once the site's root, so a fragment the overview lacks goes to
    the paper where it is served now, in one step and not through `explainer.html`; a
    result's row goes to the results table; The Frontier Survey's goes to the Frontier
    page; and a fragment the overview has stays."""
    arrival = f"{served}{LOWER_BOUNDS_PAPER}?review=fonts#fn-3"
    assert _arrives(browser, f"{served}?review=fonts#fn-3", arrival, scripts=True) == arrival
    arrival = f"{served}{render_overview.RESULTS_PAGE}#t-018"
    assert _arrives(browser, f"{served}index.html#t-018", arrival, scripts=True) == arrival
    # Verification Ladders is the results page's since 2026-10-02: both its fragments
    # go there, and one the overview has stays.
    for ladders in ("verification-ladders", "verification-at-a-glance"):
        arrival = f"{served}{render_overview.RESULTS_PAGE}#{ladders}"
        assert _arrives(browser, f"{served}#{ladders}", arrival, scripts=True) == arrival
    # The Frontier Survey left the overview the same day: both its fragments go to the
    # Frontier page, whose title carries the first.
    for survey in ("the-frontier-survey", "the-survey"):
        arrival = f"{served}atlas.html#{survey}"
        assert _arrives(browser, f"{served}#{survey}", arrival, scripts=True) == arrival
    stays = f"{served}#recent-results"
    assert _arrives(browser, stays, stays, scripts=True) == stays


def test_the_deployed_site_check_follows_the_same_forwarders(
    served: str, browser: Any, monkeypatch: pytest.MonkeyPatch
) -> None:
    """`check_published_site` visits each old address the way a deploy is checked, and
    accepts a site this machine serves; it fails when a forwarder leads nowhere."""
    context = browser.new_context()
    context.route(
        f"{REPO_URL}/**",
        lambda route: route.fulfill(status=200, content_type="text/html", body=STAND_IN),
    )
    try:
        followed = check_published_site.forwarder_arrivals(context, served, timeout=10)
        assert [passed for passed, _ in followed] == [True] * len(render_overview.MOVED_PAGES)
        lines = dict(
            zip((old for old, _ in render_overview.MOVED_PAGES), followed, strict=True)
        )
        suffix = check_published_site.FORWARDED_SUFFIX
        paper = f"{served}{LOWER_BOUNDS_PAPER}{suffix}"
        line = lines["explainer.html"][1]
        assert f"visiting {served}explainer.html{suffix} arrives at {paper!r}" in line
        assert (
            f"visiting {served}n11-optimality/{suffix} "
            in lines["n11-optimality/index.html"][1]
        )
        assert f"arrives at {DEFECTS + suffix!r}" in lines["defects.html"][1]
        assert check_published_site.fetch_once(f"{served}explainer.html")[0] == 200

        monkeypatch.setattr(
            render_overview,
            "MOVED_PAGES",
            (("explainer.html", "papers/not-a-paper.html"),),
        )
        ((passed, line),) = check_published_site.forwarder_arrivals(context, served, timeout=2)
        assert not passed
        assert "papers/not-a-paper.html" in line
    finally:
        context.close()


@pytest.mark.parametrize("scripts", [True, False])
def test_published_forwarders_reach_canonical_content(
    served: str, browser: Any, *, scripts: bool
) -> None:
    """HTTP uses canonical script targets and the physical no-script fallback.

    Both retired case directories reach Atlas with the same canonical identity.
    """
    for old, target in _arrivals(served.rstrip("/")).items():
        suffix = "?view=embed#retained-forwarder-fragment"
        expected = target + suffix if scripts else target
        assert (
            _arrives(
                browser,
                served + old + suffix,
                expected,
                scripts=scripts,
                atlas=old in {"cases.html", "cases/index.html"},
            )
            == expected
        ), old


@pytest.mark.parametrize("transport", ["site", "served"])
@pytest.mark.parametrize("old", ["cases.html", "cases/index.html"])
@pytest.mark.parametrize(
    ("suffix", "target"),
    [
        ("#n-17", "atlas.html#n-17"),
        ("?recent=true#n-291", "atlas.html?recent=true#n-291"),
        ("?n=17&view=embed", "atlas.html?view=embed#n-17"),
        ("?n=17&view=embed#bounds", "cases/17.html?view=embed#bounds"),
        ("#n-999", "atlas.html#n-999"),
        ("?n=999&view=embed#bounds", "atlas.html?n=999&view=embed#bounds"),
        ("?n=invalid#unknown", "atlas.html?n=invalid#unknown"),
    ],
)
def test_case_selectors_preserve_state_and_only_use_registered_destinations(
    request: pytest.FixtureRequest,
    browser: Any,
    transport: str,
    *,
    old: str,
    suffix: str,
    target: str,
) -> None:
    fixture = request.getfixturevalue(transport)
    root = fixture.as_uri() + "/" if isinstance(fixture, Path) else fixture
    expected = root + target
    assert (
        _arrives(
            browser,
            root + old + suffix,
            expected,
            scripts=True,
            atlas=target.startswith("atlas.html"),
        )
        == expected
    )


def test_case_directory_address_arrives_on_its_atlas_row(browser: Any, served: str) -> None:
    expected = served + "atlas.html#n-291"
    assert (
        _arrives(browser, served + "cases/#n-291", expected, scripts=True, atlas=True)
        == expected
    )
