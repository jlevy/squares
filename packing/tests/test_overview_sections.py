"""The homepage previews bound their actual content while keeping complete records linked."""

from __future__ import annotations

import re
from dataclasses import replace
from datetime import timedelta

import pytest

from devtools import overview_data, overview_sections
from sqpack import release


def test_results_table_omits_the_superseded_bottom_legend() -> None:
    overview = overview_data.load()
    table = overview_sections.results_table(overview)
    assert "site-rung-legend" not in table
    assert "What each rung means" not in table
    # The full Results documentation still defines every rung and remains linkable.
    ladders = overview_sections.verification_block()
    for label in overview_sections.rung_meanings():
        assert label in ladders
    assert overview_sections.LADDERS_SECTION == "verification-ladders"


def test_canonical_atlas_targets_keep_every_tile_addressable_without_scripts() -> None:
    grid = overview_sections.atlas_grid()
    assert overview_sections.ATLAS_DEFAULT == "triangle"
    assert 'data-atlas-view="triangle" data-atlas-size="small"' in grid
    assert 'data-atlas-drawing="regularized" data-atlas-grid>' in grid
    tabs = overview_sections.atlas_view_tabs()
    selected = re.findall(r'<button[^>]*aria-selected="true"[^>]*>', tabs)
    assert len(selected) == 1
    assert 'data-atlas-tab="triangle"' in selected[0]
    assert re.findall(r'id="atlas-n-(\d+)"', grid) == [str(n) for n in range(1, 325)]
    assert 'id="atlas-n-324" href="cases/324.html" data-case="324"' in grid
    # Every tile is visible in the static markup, so no-script readers need no style
    # of their own to see them (think-rk91): only the link to the survey remains.
    fallback = grid.split("<noscript>", 1)[1].split("</noscript>", 1)[0]
    assert "<style" not in fallback
    tiles = grid.split('class="site-atlas-cells"', 1)[1].split("<noscript>")[0]
    assert not re.search(r"\shidden(?=[\s>=])", tiles)
    assert 'href="frontier.html"' in fallback
    assert 'href="frontier.html"' in overview_sections.page_cards()
    assert 'href="atlas.html#the-frontier-survey"' not in fallback


def test_recent_preview_contains_only_the_twelve_newest_eligible_rows() -> None:
    overview = overview_data.load()
    reference = overview_sections.reference_date(overview)
    cutoff = (reference - timedelta(days=180)).isoformat()
    assert (
        overview_sections.FilterDefaults(significance=4, max_age=180, hide_superseded=True)
        == overview_sections.RECENT_DEFAULTS
    )
    # The record currently has six eligible major results. Promote current S3
    # results in this fixture so the twelve-row DOM cap is exercised.
    extras = [
        result
        for result in overview.results
        if result.record["significance"]["score"] == 3
        and not overview_sections.is_superseded(result)
        and overview_sections.first_day(result.dated[1]) >= cutoff
    ][:12]
    promoted = {
        extra.id: replace(
            extra,
            record={
                **extra.record,
                "significance": {**extra.record["significance"], "score": 4},
            },
        )
        for extra in extras
    }
    overview = replace(
        overview,
        results=[promoted.get(result.id, result) for result in overview.results],
    )
    eligible = [
        result
        for result in overview_sections.recent_results(overview)
        if result.record["significance"]["score"] >= 4
        and not overview_sections.is_superseded(result)
        and overview_sections.first_day(result.dated[1]) >= cutoff
    ]
    assert len(eligible) > 12
    preview = overview_sections.recent_table(overview)
    rows = re.findall(r'<tr data-result="([^"]+)"([^>]*)>', preview)
    assert [result_id for result_id, _ in rows] == [
        result.id.lower() for result in eligible[:12]
    ]
    assert all(" hidden" not in attributes for _, attributes in rows)
    for _, attributes in rows:
        significance = re.search(r'data-s="(\d+)"', attributes)
        dated = re.search(r'data-date="([^"]+)"', attributes)
        assert significance is not None
        assert int(significance[1]) >= 4
        assert dated is not None
        assert dated[1] >= cutoff
        assert 'data-current="true"' in attributes
    assert preview.count('class="site-popover site-row-pop"') == len(rows)
    for result in eligible[:12]:
        assert f'href="result/{result.id.lower()}.html"' in preview
    assert "site-recent-scope" not in preview
    assert "Showing 12 of" not in preview
    assert "from the last 180 days" not in preview
    attributes = overview_sections.all_results_link_attributes(overview)
    assert attributes.startswith("data-all-results ")
    assert f'data-result-ids="{" ".join(r.id.lower() for r in overview.results)}"' in (
        attributes
    )
    assert "data-retired-results=" in attributes


def test_homepage_atlas_reuses_canonical_split_rows_and_shows_every_case() -> None:
    preview = overview_sections.atlas_preview()
    complete = overview_sections.atlas_grid()
    tiles = re.findall(r'<a class="site-atlas-cell"[^>]*>.*?</a>', preview)
    assert len(tiles) == 324
    assert tiles == re.findall(r'<a class="site-atlas-cell"[^>]*>.*?</a>', complete)
    assert [int(n) for n in re.findall(r'data-atlas-n="(\d+)"', preview)] == list(range(1, 325))
    assert 'data-atlas-view="triangle" data-atlas-size="small"' in preview
    assert 'id="homepage-atlas-cells"' in preview
    # All eighteen rows stand in the one visible box of tiles, with no expander
    # (the owner, 2026-10-23, think-rk91).
    cells = preview.split('id="homepage-atlas-cells"', 1)[1].split(
        "data-homepage-atlas-status"
    )[0]
    assert re.findall(r'data-atlas-row="(\d+)"', cells) == list(map(str, range(1, 19)))
    assert not re.search(r"\shidden(?=[\s>=])", cells)
    for absent in ("data-atlas-rest", "data-atlas-first", "data-atlas-count"):
        assert absent not in cells, absent
    assert preview.count('data-atlas-segment="non-grid"') == 18
    assert preview.count('data-atlas-segment="grid"') == 18
    for n, tile in enumerate(tiles, 1):
        assert f'id="atlas-n-{n}" href="cases/{n}.html" data-case="{n}"' in tile
        assert "<img " in tile
        assert 'loading="lazy"' in tile
        assert 'class="site-star"' not in tile
        recent = overview_sections.recent_contributions_by_case()[n].any
        assert (", new result" in tile) == recent
        assert 'class="site-atlas-n"' in tile
        assert 'class="site-atlas-n is-new-result"' not in tile
        assert "evidence-badge" not in tile
    assert preview.count('id="pop-case"') == 1
    assert preview.count('role="tab"') == complete.count('role="tab"') == 10
    assert 'data-atlas-drawing="regularized"' in preview
    drawing_tabs = overview_sections.atlas_drawing_tabs("homepage-atlas-cells")
    assert preview.count(drawing_tabs) == 1
    assert drawing_tabs.count('role="tab"') == 2
    selected = re.findall(r'<button[^>]*aria-selected="true"[^>]*>', drawing_tabs)
    assert len(selected) == 1
    assert 'data-atlas-drawing-tab="regularized"' in selected[0]
    assert "data-atlas-toggle" not in preview
    assert preview.count("data-atlas-legend") == complete.count("data-atlas-legend")
    assert 'aria-controls="atlas-cells"' not in preview
    assert preview.count('aria-controls="homepage-atlas-cells"') == 10
    assert len(preview.encode("utf-8")) < 400_000
    for absent in (
        "data-homepage-atlas-gzip",
        "data-homepage-atlas-svg",
        "<noscript>",
    ):
        assert absent not in preview


def test_reading_cards_keep_original_dates_when_a_new_edition_is_added(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        release,
        "EXPLAINER_HISTORY",
        (
            release.PublicationHistoryEntry("v9.0.0", "January 1, 2030", "Later revision"),
            *release.EXPLAINER_HISTORY,
        ),
    )
    expected = {
        "papers/n11-lower-bounds-explainer.html": "2026-09-05",
        "papers/n11-threshold-bound-review.html": "2026-10-05",
        "papers/n11-optimality-review.html": "2026-09-30",
        "papers/square-packing-methods-survey.html": "2026-10-08",
        "tutorial.html": "2026-10-01",
        "tutorial-advanced.html": "2026-10-14",
    }
    cards = re.findall(
        r'<a class="site-card site-card-link" href="([^"]+)"[^>]*>(.*?)</a>',
        overview_sections.paper_cards(),
        re.DOTALL,
    )
    assert len(cards) == len(expected)
    for href, card in cards:
        assert f'<time datetime="{expected[href]}">' in card
        assert "2030" not in card
        assert 'target="_blank"' not in card
        assert card.index("site-card-label") < card.index("<h3>") < card.index("<time ")
        assert card.index("</header>") < card.index("site-card-note")


def test_homepage_learning_preview_uses_the_shared_starting_cards() -> None:
    preview = overview_sections.homepage_paper_cards()
    destinations = re.findall(r'<a class="site-card site-card-link" href="([^"]+)"', preview)
    assert destinations == [
        "tutorial.html",
        "tutorial-advanced.html",
        overview_sections.LOWER_BOUNDS_PAPER,
    ]
    complete = overview_sections.paper_cards()
    for card in re.findall(r'<a class="site-card site-card-link".*?</a>', preview, re.DOTALL):
        assert card in complete
