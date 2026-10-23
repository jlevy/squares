"""Canonical site collections, shared actions and retained destination routes."""

import re

import pytest

from devtools import overview_sections, render_overview, site_navigation, site_urls
from tests import site_renders


@pytest.fixture(scope="module")
def results_page() -> str:
    return site_renders.html("results.html")


@pytest.fixture(scope="module")
def homepage() -> str:
    return site_renders.html("index.html")


def test_frontier_is_a_results_destination_and_not_an_atlas_forwarder() -> None:
    assert "frontier.html" in render_overview.PAGES
    assert "frontier.html" not in dict(render_overview.MOVED_PAGES)
    links = site_navigation.navigation_links("frontier.html")
    assert 'href="frontier.html" aria-current="page">Frontier Survey</a>' in links
    assert 'href="atlas.html"' in links
    row = next(row for row in site_urls.load_registry() if row.path == "frontier.html")
    assert (row.kind, row.status, row.canonical, row.target) == (
        "page",
        "live",
        "frontier.html",
        "",
    )


def test_both_atlases_arrive_with_every_case_and_no_expander() -> None:
    complete = overview_sections.atlas_grid()
    preview = overview_sections.atlas_preview()
    for markup in (complete, preview):
        assert markup.count('class="site-atlas-cell"') == 324
        assert "data-atlas-rest" not in markup
        assert "data-atlas-toggle" not in markup


def test_all_results_is_the_only_complete_result_collection() -> None:
    assert "results.html" in render_overview.PAGES
    assert "recent-results.html" not in render_overview.PAGES
    assert "recent-results.html" not in render_overview.SITE_PAGES
    assert dict(render_overview.MOVED_PAGES)["recent-results.html"] == "results.html"
    group = next(item for item in site_navigation.NAVIGATION if item.key == "results")
    assert [(item.label, item.path) for item in group.children] == [
        ("Visual Atlas", "atlas.html"),
        ("Frontier Survey", "frontier.html"),
        ("All Results", "results.html"),
        ("Verification", "verification.html"),
        ("Report a Result", "report.html"),
    ]
    row = next(row for row in site_urls.load_registry() if row.path == "recent-results.html")
    assert (row.kind, row.status, row.canonical, row.target) == (
        "forwarder",
        "forwarded",
        "results.html",
        "results.html",
    )


def test_tutorials_leads_learn_and_ends_with_the_shared_read_papers_action() -> None:
    group = next(item for item in site_navigation.NAVIGATION if item.key == "learn")
    assert [(item.label, item.path) for item in group.children[:2]] == [
        ("Tutorials", "tutorials.html"),
        ("Papers", "papers.html"),
    ]
    page = render_overview.tutorials_page().html
    article = page[page.index('<h1 id="tutorial"') : page.index("</article>")]
    assert (
        '<a class="site-action" href="papers.html">Read Papers'
        + overview_sections.arrow_icon("right")
        + "</a>"
    ) in article
    assert article.index("Read Papers") > article.index("Square Packing, Search, and Proof")


def test_all_results_collection_actions_share_one_row_after_the_table(
    results_page: str,
) -> None:
    article = results_page.split('<h1 id="every-result"', 1)[1].split("</article>", 1)[0]
    end = article.index("</table>") + len("</table>")
    action = r'<a class="site-action" href="([^"]+)">([^<]+)'
    assert re.findall(action, article[:end]) == []
    assert re.findall(action, article[end:]) == [
        ("atlas.html", "Visual Atlas"),
        ("frontier.html", "Frontier Survey"),
        ("verification.html", "Verification"),
    ]
    assert article[end:].count('class="site-action-row site-more"') == 1


def test_homepage_learn_immediately_follows_results(homepage: str) -> None:
    article = homepage.split('<h1 id="the-problem"', 1)[1].split("</main>", 1)[0]
    headings = re.findall(r'<h[12]\b[^>]*\bid="([^"]+)"', article)
    result = headings.index("recent-results")
    assert headings[result + 1] == "papers"
    expected = [
        "the-atlas-of-square-packings",
        "news",
        "recent-results",
        "papers",
        "report-your-results",
        "visuals",
        "more-resources",
        "about-the-squares-project",
    ]
    assert [heading for heading in headings if heading in expected] == expected
