"""The survey and graphic Atlas retain distinct canonical reader destinations."""

from devtools import overview_sections, render_overview, site_navigation, site_urls


def test_frontier_is_a_results_destination_and_not_an_atlas_forwarder() -> None:
    assert "frontier.html" in render_overview.PAGES
    assert "frontier.html" not in dict(render_overview.MOVED_PAGES)
    links = site_navigation.navigation_links("frontier.html")
    assert 'href="frontier.html" aria-current="page">The Frontier Survey</a>' in links
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
