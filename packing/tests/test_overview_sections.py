"""The homepage previews bound their actual content while keeping complete records linked."""

from __future__ import annotations

import base64
import gzip
import html
import re
import xml.etree.ElementTree as ET
from dataclasses import replace
from datetime import timedelta

from devtools import overview_data, overview_sections


def test_homepage_legend_keeps_original_rungs_in_four_icon_and_label_rows() -> None:
    home = overview_sections.rung_legend(here=False, heading="Legend")
    complete = overview_sections.rung_legend(here=True)
    assert '<h2 class="site-rung-legend-heading">Legend</h2>' in home
    assert 'href="all-results.html#verification-ladders"' in home
    assert home.count('<span class="site-rung-legend-icons">') == 4
    assert re.findall(r'<span class="site-rung-legend-name">([^<]+)</span>', home) == [
        "Significance",
        "Verification",
        "Confirmation",
        "new result",
    ]
    assert "What each rung means" not in home
    meanings = overview_sections.rung_meanings()
    for scale, levels in overview_sections.rubric_levels().items():
        for level, _ in levels:
            label = f"{scale}{level}"
            assert f'title="{html.escape(meanings[label], quote=True)}"' in home
            if scale == "S":
                mark = overview_sections.significance_mark(level, meanings[label])
                assert mark in home
                assert mark in complete
    chips = re.findall(r'<span class="site-chip site-rung-fill"[^>]*>[^<]+</span>', home)
    assert len(chips) == 12
    assert all(chip in complete for chip in chips)
    assert 'class="site-star"' in home
    assert '<a href="#verification-ladders">What each rung means</a>' in complete
    assert complete.count("<p>") == 3
    assert "site-rung-legend-icons" not in complete


def test_canonical_atlas_targets_keep_every_tile_addressable_without_scripts() -> None:
    grid = overview_sections.atlas_grid()
    assert overview_sections.ATLAS_DEFAULT == "triangle"
    assert 'data-atlas-view="triangle" data-atlas-size="medium"' in grid
    assert 'data-atlas-first="100" data-atlas-grid' in grid
    tabs = overview_sections.atlas_view_tabs()
    selected = re.findall(r'<button[^>]*aria-selected="true"[^>]*>', tabs)
    assert len(selected) == 1
    assert 'data-atlas-tab="triangle"' in selected[0]
    assert re.findall(r'id="atlas-n-(\d+)"', grid) == [str(n) for n in range(1, 325)]
    assert 'id="atlas-n-324" href="cases/324.html" data-case="324"' in grid
    fallback = grid.split("<noscript>", 1)[1].split("</noscript>", 1)[0]
    assert ".site-atlas-grid .site-atlas-rest[hidden]{display:contents}" in fallback
    assert ".site-atlas-grid .site-atlas-toggle-row{display:none}" in fallback
    assert 'href="atlas.html#the-frontier-survey"' in fallback
    assert 'href="atlas.html#the-frontier-survey"' in overview_sections.page_cards()
    assert 'href="frontier.html"' not in fallback


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


def test_atlas_preview_keeps_six_rows_and_prepares_web_labels_without_changing_print() -> None:
    preview = overview_sections.atlas_preview()
    source = overview_sections.ATLAS_COMPOSITE.read_text(encoding="utf-8")
    payload = preview.split("<template data-homepage-atlas-gzip>", 1)[1].split(
        "</template>", 1
    )[0]
    assert re.fullmatch(r"[A-Za-z0-9+/=]+", payload)
    web = gzip.decompress(base64.b64decode(payload)).decode("utf-8")
    originals = ET.fromstring(source).findall('.//*[@data-feature="packing-card"]')
    cards = ET.fromstring(web).findall('.//*[@data-feature="packing-card"]')
    assert len(originals) == len(cards) == 324
    for n, (original, card) in enumerate(zip(originals, cards, strict=True), 1):
        assert card.attrib == original.attrib
        texts = card.findall(".//{*}text")
        assert [(text.get("data-feature"), "".join(text.itertext())) for text in texts] == [
            ("packing-label", str(n))
        ]
        assert card.findall('.//*[@data-feature="evidence-badge"]') == []
        assert len(original.findall(".//{*}text")) > 1
        assert original.findall('.//*[@data-feature="evidence-badge"]')
        for feature in ("container-outline", "square-fills", "legend-star"):
            original_nodes = original.findall(f'.//*[@data-feature="{feature}"]')
            web_nodes = card.findall(f'.//*[@data-feature="{feature}"]')
            assert [
                [(child.tag, child.attrib, (child.text or "").strip()) for child in node.iter()]
                for node in web_nodes
            ] == [
                [(child.tag, child.attrib, (child.text or "").strip()) for child in node.iter()]
                for node in original_nodes
            ], (n, feature)
    starts = list(
        re.finditer(r'^  <g data-feature="packing-card" data-n="(\d+)"', web, re.MULTILINE)
    )
    links = re.findall(r'<a class="site-atlas-cell"[^>]*>', preview)
    assert len(links) == 36
    assert overview_sections.ATLAS_PREVIEW_ROWS == 6
    assert 'data-atlas-view="triangle"' in preview
    assert 'data-atlas-count="36"' in preview
    assert 'style="--site-atlas-widest:11"' in preview
    assert re.findall(r'data-feature="packing-card" data-n="(\d+)"', preview) == [
        str(n) for n in range(1, 37)
    ]
    for index, start in enumerate(starts[:36]):
        assert web[start.start() : starts[index + 1].start()] in preview
        assert re.search(r"\n[ \t]*\n", web[start.start() : starts[index + 1].start()]) is None
        n = index + 1
        k = int((n - 1) ** 0.5) + 1
        assert f'style="--r:{k};--c:{k * k - n};--o:' in links[index]
    assert 'viewBox="60 174 216 252"' in preview
    assert 'viewBox="1428 426 216 252"' in preview
    assert len(preview.encode("utf-8")) < 1_200_000
    assert '<div class="site-atlas-rest" data-atlas-rest hidden></div>' in preview
    assert "data-atlas-preview" in preview
    for absent in (
        "data-atlas-toggle",
        'role="tab"',
    ):
        assert absent not in preview
    for link in links:
        n = re.search(r'data-atlas-n="(\d+)"', link)
        assert n is not None
        assert f'href="cases/{n[1]}.html" data-case="{n[1]}"' in link
        assert f'aria-label="Case {n[1]}: packing and bounds"' in link
