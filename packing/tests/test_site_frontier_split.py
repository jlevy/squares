"""The survey and graphic Atlas retain distinct canonical reader destinations."""

from devtools import overview_sections, render_overview, site_navigation, site_urls


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


def test_full_atlas_arrives_expanded_and_homepage_preview_stays_short() -> None:
    complete = overview_sections.atlas_grid()
    preview = overview_sections.atlas_preview()
    for markup in (complete, preview):
        assert markup.count('class="site-atlas-cell"') == 324
    assert "data-atlas-rest>" in complete
    assert 'data-atlas-toggle aria-expanded="true"' in complete
    assert "data-atlas-rest hidden>" in preview
    assert 'data-homepage-atlas-toggle aria-expanded="false"' in preview


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
