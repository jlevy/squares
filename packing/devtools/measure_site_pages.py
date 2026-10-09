#!/usr/bin/env python3
"""Measure a built site's pages against the explainer: load and math timing, text, faces,
the card sections' layout, the rating ladders' rows, the face of every formula, the
space around tables and headings, the columns of the data tables, the chips, where each
page's header stands, the baselines its labels stand on, the size of what a press
opens, how every run of text and every formula is drawn, and where each figure's
drawing stands and what is lettered into it.

Fifteen measurements, each over pages of a directory `preview_site` has built:

- `load` serves the directory on a local port and opens each page in a fresh Chromium
  context, cold cache, at a desktop or phone width. An init script (a probe) records
  long tasks and, on every animation frame, how many displayed formulas are typeset
  and showing. It reports DOMContentLoaded, load, first contentful paint, the first
  frame at which every formula in the first viewport is readable and the first at which
  every displayed formula is, the long tasks and their blocking time over 50 ms, and the
  document's bytes, with the bytes the load moved over the network and its requests,
  every file and the files the cache did not answer. Times are milliseconds from
  navigation start; `--runs` repeats each load and reports the median. A directory is
  served as GitHub Pages serves it, gzipped and fresh for ten minutes
  (`preview_site.serve`), so the bytes are the deployed site's. `--network` throttles
  each load to a named network (`NETWORKS`), and `--after PAGE` opens that page first in
  the same browser, so the load measured is a reader's second page. An animation frame
  is an opportunity to paint, not a presented frame, and the per-frame scan is observer
  overhead every page pays alike.
- `type` reports the reading column's resolved typography, role by role (paragraph,
  h1 to h4, list item, table cell, code, inline math), and every `--kpress-*`,
  `--site-*`, `--paper-*` and `--cert-*` token the root and the column resolve.
- `faces` needs no browser: it lists every `@font-face` block each page carries, inline
  or in a shared stylesheet it links, by family, and whether the block is
  byte-identical to the explainer's.
- `cards` reports every card section as laid out: its cards in rows, each row's card
  widths and sizes and the slack at its start and end (equal when the row is centred),
  and each card's headline face, weight and size. `--markdown` prints one line a row, and
  `--media print` lays the page out as it prints.
- `ladders` reports the rating-ladder diagram (`.site-ladders`) as laid out: how many
  columns its rungs stand in, every rung's height, the rules under its heads and between
  its rows, and each description's box, the lines its words take and how far they run
  past the box. `--markdown` prints one line a width, with the distinct rung heights (one
  value when every row is the same height), the narrowest description box and the most
  lines any description takes. `--shots DIR` also shoots each diagram there at each
  width, light and dark, under its heading.
- `math` reports the face of every typeset formula beside the face of the text it sits
  in, counted by surface (a card's headline, a chip, a table, a popover, a caption, the
  prose), once the page has typeset all its math. `--press SELECTOR` presses an element
  first, a card or an atlas cell, so the math of what it opens is counted too.
- `space` reports the white space above and below every table and every heading as laid
  out, in CSS pixels between border boxes, and each heading's size, line height and
  leading (line height over size). A table is the component a reader sees, its filter
  bar included, and has its side gutters too: how far it and its bar sit from the
  window's edges, or from the popover's that holds it. The page's first block is
  reported with the space from the bar's rule down to it. A heading is every `h1` to
  `h4` and every headline set in a heading's face (a card's, a popover's, a case
  record's), with how many lines it takes and how much of its content its box cannot
  show. `--press SELECTOR` presses an element once
  the page is measured and reports what it opened, a popover or a disclosure, as rows
  whose `state` is the selector. `--markdown` prints one line a table and one line a
  heading role, with the least and most space found. This is the tool the design
  system's spacing tokens are measured with (`templates/paper-design.md`, Spacing).
- `columns` reports every shared data table (`.site-table`) as laid out, once its math
  is typeset: the table's width, how far it runs past what scrolls it sideways, how many
  rows show, and each column's width, the most lines a cell of it takes, the words a
  line break splits, and the tallest row whose height that column's cell sets. So a
  column too narrow for what it holds shows as the one making rows tall. With them it
  reports what a column's lines may not do: the values of a list of cases cut across
  lines, the widest piece of typeset math, which is the least a cell of formulas can be,
  the formulas a line ends inside anywhere but after a relation or a binary operator,
  and the punctuation that begins a line. On a phone,
  where a row is a card, it reports the tallest card and each cell's lines. A page's
  address may carry the query that presets its filters: `index.html?s-min=&age=` is the
  overview's recent table with every row showing. `--markdown` prints one line a
  column. `--shots DIR` also shoots each table there at each width, its filter bar and
  its first rows.
- `chips` reports every chip a page shows (`.site-chip`), once its math is typeset: its
  kind (a rung, a result's kind, a standing, a novelty label or another), its words, the
  surface it sits on, its font size, line height and box, and the lines its words take,
  which is 1 for a chip that does not wrap. `--press SELECTOR` presses an element once
  the page is measured and reports the chips of what it opened. `--markdown` prints one
  line for each kind on each surface, with the distinct sizes found and the chips that
  wrap.
- `header` reports where each page's header stands at each width, as tops and bottoms in
  CSS pixels from the top of the document: the navigation bar, the rule under it and the
  element that draws it, the section tabs with the current tab's name (on a page of the
  Visualize section), and the first block of the page's content. With them it reports
  the header's type: the computed font size of the body's prose, the site's name (and
  whether its text is shown), a link in the bar and a section tab, and how many lines the
  bar's links take. `--markdown` prints one line a page and width.
- `baselines` reports the text baselines of the header's labels, measured and not read
  from a box's edge: the site's name (where its text is shown), the links of each line
  of the bar, the section tabs, how far the name stands off the links, and how far the
  current link's and the current tab's baseline stand over the rule and the foot of the
  tab strip. `--markdown` prints one line a page and width.
- `popover` presses each `--press SELECTOR` in a window of each `--width` and `--height`
  and reports the popover it opened: its box, the margin the window keeps above, below
  and beside it, the height of what it holds, the share of that it shows without
  scrolling (its frame's share, where it frames a page), and every word in it broken
  across lines inside the word (`preview_site.split_problem`). `--shots DIR` also shoots
  the window with each popover open. This is the tool the popovers' height limits are
  measured with (`templates/paper-design.md`, Site Components, Cards).
- `glyphs` reports how each page's glyphs are drawn, once its math is typeset, at each
  `--width` and in each `--scheme`: for every role of text (prose, a heading, a caption,
  a table cell, a footnote, a chip, a link of the bar, and as `other` every run no role
  names) and for the formulas of every surface, inline and display apart, each distinct
  setting with how many elements it stands for. A setting is everything that decides
  what a reader sees: the face asked for and the platform face the browser drew
  (`CSS.getPlatformFontsForNode`, with a variable face's drawn weight), weight, size,
  line height, colour, opacity, and the properties that change how a face is
  rasterised, `text-rendering` among them; for a formula also how it is typeset, its
  size over its text's, whether it takes its text's colour, and `ink`, the area its
  glyphs paint in square em of its own size, measured on a shot at twice its size. Ink
  is the one number that says a formula is drawn thinner when no computed size, weight
  or face differs. With it come the faces the page declares and whether each is
  inlined or shared and loaded, the KaTeX the page runs, what it stamps on its root,
  and what the shared text tokens come to. `--tex SOURCE` reports that formula as a
  row of its own, so one formula can be compared between pages; `--style CSS` adds a
  stylesheet before
  measuring, to see what one declaration changes; `--platform NAME` tells the page it
  is on that platform. `--view` prints one table: `formulas`, a row a formula sampled;
  `differences`, every property a page sets differently from the first page;
  `summary`, each role's distinct settings with the pages that set it so, where a role
  with one row is set one way everywhere; `problems`, where a page departs from what
  the shared layers set (`glyph_problems`), which fails the run when there is any.
  `--shots DIR` saves each formula's shot. This is the tool the optimality paper's
  thinner mathematics was found and measured with (`templates/paper-design.md`, Math).

- `figures` reports every figure a page shows, once its math is typeset, at each
  `--width`: how wide its drawing is and how far the drawing's centre, and the centre of
  what an SVG paints in it, stand from the centre of the reading column; whether it
  scrolls sideways there or shares its row with controls; how many text elements its
  SVGs hold, the widest of them with its share of the drawing, and any that reads as a
  sentence; and its caption. Each row carries its `problems` (`figure_problems`): a
  drawing off the column's centre, what it paints off that centre (a packing at the
  left of a wide canvas), a title or a sentence lettered into the drawing, and a figure
  with no caption. `--media print` lays the page out as it prints, and `--shots DIR`
  shoots each figure with its caption. This is the tool the optimality paper's figures
  were brought to the first paper's treatment with (`templates/paper-design.md`,
  Figures).
- `credits` reports the front of each page, once its math is typeset, at each `--width`,
  one row an item: each chip of the formats row with its size and weight, then each line
  of the credits, the series strip's lines last, with what the line is (its class), the
  weight it is set at, the weights of the names and the links in it, the space above it
  in line heights, the lines its words take and its width as a share of the column's.
  This is the tool the papers' fronts are held together with in the browser
  (`templates/paper-design.md`, The Papers' Front).

Every mode but `faces` also takes, in place of the directory, the address a site is
served at, and measures the published pages as they are.

Usage, from `packing/`:
    uv run --frozen --all-extras --group dev python -m devtools.measure_site_pages load SITE
    uv run --frozen --all-extras --group dev python -m devtools.measure_site_pages type SITE
    uv run --frozen --all-extras --group dev python -m devtools.measure_site_pages faces SITE
    uv run --frozen --all-extras --group dev python -m devtools.measure_site_pages cards SITE \
        --page index.html --width 1280 --width 390 --markdown
    uv run --frozen --all-extras --group dev python -m devtools.measure_site_pages \
        ladders SITE --page index.html --width 1280 --width 768 --width 390 --markdown
    uv run --frozen --all-extras --group dev python -m devtools.measure_site_pages math SITE \
        --page index.html --press '[data-atlas-n="11"]' --markdown
    uv run --frozen --all-extras --group dev python -m devtools.measure_site_pages space SITE \
        --page index.html --page all-results.html --width 1280 --width 390 --markdown
    uv run --frozen --all-extras --group dev python -m devtools.measure_site_pages \
        columns SITE --page index.html --page all-results.html \
        --width 1280 --width 1024 --width 768 --markdown
    uv run --frozen --all-extras --group dev python -m devtools.measure_site_pages header SITE \
        --page visualize.html --page workbench/index.html --width 1280 --width 390 --markdown
    uv run --frozen --all-extras --group dev python -m devtools.measure_site_pages baselines \
        SITE --page frontier.html --page visualize.html --width 1280 --width 768 --width 390 \
        --markdown
    uv run --frozen --all-extras --group dev python -m devtools.measure_site_pages \
        popover SITE --page frontier.html --press 'a[data-case="79"]' \
        --width 1280 --height 900 --height 1200 --height 1440 --markdown
    uv run --frozen --all-extras --group dev python -m devtools.measure_site_pages glyphs \
        SITE --page papers/n11-lower-bounds-explainer.html \
        --page papers/n11-threshold-bound-review.html \
        --page papers/n11-optimality-review.html \
        --width 1280 --width 390 --scheme light --scheme dark --view differences --markdown
    uv run --frozen --all-extras --group dev python -m devtools.measure_site_pages glyphs \
        https://jlevy.github.io/squares --page papers/n11-lower-bounds-explainer.html \
        --view problems --markdown
    uv run --frozen --all-extras --group dev python -m devtools.measure_site_pages figures \
        SITE --page papers/n11-lower-bounds-explainer.html \
        --page papers/n11-threshold-bound-review.html \
        --page papers/n11-optimality-review.html \
        --width 1280 --width 390 --shots DIR --markdown
    uv run --frozen --all-extras --group dev python -m devtools.measure_site_pages credits \
        SITE --page papers/n11-lower-bounds-explainer.html \
        --page papers/n11-threshold-bound-review.html \
        --page papers/n11-optimality-review.html --width 1280 --width 390 --markdown

`SITE` is a directory holding the whole site, as `devtools.preview_site` builds it: the
kpress pages and the papers under `papers/`. Set
`SQPACK_CHROMIUM` to use a browser the environment supplies, as the other tools do.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import itertools
import json
import re
import statistics
import sys
from collections.abc import Iterable, Sequence
from pathlib import Path
from typing import TYPE_CHECKING, Any

from devtools import render_overview
from devtools.preview_site import (
    BASELINES,
    HEADER,
    launch_chromium,
    motion_for,
    press,
    serve,
    settle_math,
    shot_stem,
    split_words,
)
from devtools.render_n11_lower_bounds_explainer import MATH_WRAPPERS
from sqpack.probes import applied, probe

if TYPE_CHECKING:
    from playwright.sync_api import Page

PROBES = Path(__file__).resolve().parent / "probes"
_INSTRUMENT = applied(probe(PROBES, "measure_site_pages/instrument"))
_DONE = probe(PROBES, "measure_site_pages/done")
_REPORT = probe(PROBES, "measure_site_pages/report")
TYPOGRAPHY = probe(PROBES, "measure_site_pages/typography")
CARDS = probe(PROBES, "measure_site_pages/cards")
LADDERS = probe(PROBES, "measure_site_pages/ladders")
MATH_FACES = probe(PROBES, "measure_site_pages/math_faces")
SPACING = probe(PROBES, "measure_site_pages/spacing")
COLUMNS = probe(PROBES, "measure_site_pages/columns")
_COLUMNS_SCROLL = probe(PROBES, "measure_site_pages/columns_scroll")
CHIPS = probe(PROBES, "measure_site_pages/chips")
POPOVER = probe(PROBES, "measure_site_pages/popover")
GLYPHS = probe(PROBES, "measure_site_pages/glyphs")
PLATFORM = probe(PROBES, "measure_site_pages/platform")
FIGURES = probe(PROBES, "measure_site_pages/figures")
CREDITS = probe(PROBES, "measure_site_pages/credits")
#: What a press opens, which `space` then reports alone: an open popover or disclosure.
OPENED = ":popover-open, details[open]"

#: The pages compared by default: the explainer, the long reports, two short ones, the
#: homepage and one case record.
DEFAULT_PAGES = (
    render_overview.paper_path(render_overview.N11_LOWER_BOUNDS_EXPLAINER),
    "tutorial.html",
    "synopsis.html",
    "epistemics.html",
    "readme.html",
    "index.html",
    "cases/index.html#n-11",
)
#: The pages a mode that compares papers takes by default (`credits`, `figures`): every
#: paper of the site, in reading order (`render_overview.PAPERS`).
PAPER_PAGES = tuple(render_overview.paper_path(paper.slug) for paper in render_overview.PAPERS)
#: The modes that compare the papers' own parts, and so take `PAPER_PAGES` by default.
PAPER_MODES = frozenset({"credits", "figures"})
#: A face fetched from the site's shared assets (`site_assets`), which a page ships.
_SHARED_FACE = re.compile(r"/assets/fonts/[^/]+\.[0-9a-f]{16}\.woff2$")
#: How long a load may take to finish its math before it is reported as it stands.
WAIT_MS = 35_000
FONT_FACE = re.compile(r"@font-face\s*\{[^}]*\}")
FAMILY = re.compile(r"font-family:\s*(\"[^\"]+\"|[^;]+);")


def _launch(driver: Any) -> Any:
    return launch_chromium(driver)


#: The networks a load can be measured over, as Chromium's emulation takes them: download
#: and upload throughput in bytes a second, and the latency added to every request in
#: milliseconds. Named for what they stand for, not for any browser's presets, whose
#: numbers have changed between releases; these are written here so a reading says what
#: it was taken over.
NETWORKS: dict[str, dict[str, float]] = {
    "slow-4g": {"downloadThroughput": 1.6e6 / 8, "uploadThroughput": 750e3 / 8, "latency": 150},
    "fast-4g": {"downloadThroughput": 9e6 / 8, "uploadThroughput": 1.5e6 / 8, "latency": 60},
    "cable": {"downloadThroughput": 50e6 / 8, "uploadThroughput": 10e6 / 8, "latency": 20},
}


def measure_load(
    base: str,
    pages: Sequence[str],
    *,
    widths: Sequence[int],
    runs: int,
    network: str | None = None,
    after: str | None = None,
) -> list[dict[str, Any]]:
    """Each page's load report at each width, the median of `runs` loads.

    Each load is in a fresh browser context, so its cache starts empty. `after` opens that
    page first in the same context and waits for it to finish, so the page measured is a
    reader's second page, with whatever the first left in the cache. `network` throttles
    the context to one of `NETWORKS` before anything is fetched.
    """
    from playwright.sync_api import sync_playwright  # noqa: PLC0415

    results: list[dict[str, Any]] = []
    with sync_playwright() as driver:
        browser = _launch(driver)
        for width in widths:
            for name in pages:
                samples: list[dict[str, Any]] = []
                for _ in range(runs):
                    context = browser.new_context(viewport={"width": width, "height": 900})
                    context.add_init_script(_INSTRUMENT)
                    page = context.new_page()
                    if network is not None:
                        session = context.new_cdp_session(page)
                        session.send("Network.enable")
                        session.send(
                            "Network.emulateNetworkConditions",
                            {"offline": False, **NETWORKS[network]},
                        )
                    if after is not None:
                        page.goto(f"{base}/{after}", wait_until="load")
                        page.wait_for_function(_DONE, timeout=WAIT_MS)
                    page.goto(f"{base}/{name}", wait_until="load")
                    page.wait_for_function(_DONE, timeout=WAIT_MS)
                    samples.append(page.evaluate(_REPORT))
                    context.close()
                results.append(
                    {"page": name, "width": width, "network": network, "after": after}
                    | _median(samples)
                )
        browser.close()
    return results


def _median(samples: list[dict[str, Any]]) -> dict[str, Any]:
    merged: dict[str, Any] = {}
    for key, first in samples[0].items():
        values = [sample[key] for sample in samples]
        if isinstance(first, (int, float)) and not isinstance(first, bool):
            present = [value for value in values if value is not None]
            merged[key] = round(statistics.median(present), 1) if present else None
        else:
            merged[key] = values[-1]
    return merged


def measure_type(
    base: str, pages: Sequence[str], *, widths: Sequence[int]
) -> list[dict[str, Any]]:
    """Each page's reading typography and resolved tokens at each width."""
    return [
        {"page": name, "width": width, **found}
        for name, width, found in _evaluate(base, pages, widths=widths, script=TYPOGRAPHY)
    ]


def measure_cards(
    base: str, pages: Sequence[str], *, widths: Sequence[int], media: str = "screen"
) -> list[dict[str, Any]]:
    """Each page's card sections as laid out at each width, one entry a section."""
    return [
        {"page": name, "width": width, **section}
        for name, width, found in _evaluate(
            base, pages, widths=widths, script=CARDS, media=media
        )
        for section in found
    ]


#: How much of the page a ladder shot shows above and below the diagram, in CSS pixels:
#: the section heading over it and the first lines under it, so its spacing is in view.
LADDER_SHOT_MARGIN = (130, 90)


def measure_ladders(
    base: str, pages: Sequence[str], *, widths: Sequence[int], shots: Path | None = None
) -> list[dict[str, Any]]:
    """Each page's rating-ladder diagrams as laid out at each width, one entry a diagram.
    With `shots`, each diagram is also shot there at each width, light and dark, with the
    heading above it: `ladders-<page>-<width>-<scheme>.png`."""
    from playwright.sync_api import sync_playwright  # noqa: PLC0415

    results: list[dict[str, Any]] = []
    above, below = LADDER_SHOT_MARGIN
    schemes = ("light", "dark") if shots is not None else ("light",)
    if shots is not None:
        shots.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as driver:
        browser = _launch(driver)
        for width in widths:
            for name in pages:
                for scheme in schemes:
                    page = browser.new_page(
                        viewport={"width": width, "height": 900}, color_scheme=scheme
                    )
                    page.goto(f"{base}/{name}", wait_until="load")
                    page.wait_for_timeout(300)
                    found: list[dict[str, Any]] = page.evaluate(LADDERS)
                    if scheme == "light":
                        results.extend(
                            {"page": name, "width": width, **diagram} for diagram in found
                        )
                    stem = Path(name.split("#", 1)[0]).stem
                    for index, diagram in enumerate(found):
                        if shots is None:
                            break
                        which = f"{stem}-{index}" if index else stem
                        top = max(0, diagram["top"] - above)
                        page.screenshot(
                            path=str(shots / f"ladders-{which}-{width}-{scheme}.png"),
                            full_page=True,
                            clip={
                                "x": 0,
                                "y": top,
                                "width": width,
                                "height": diagram["top"] + diagram["height"] + below - top,
                            },
                        )
                    page.close()
        browser.close()
    return results


def ladder_rows(report: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """A `ladders` report flattened to one row per page and width: the diagram's columns,
    its distinct rung heights, the narrowest description box, the most lines a
    description takes, and the rungs whose words run past their two lines."""
    return [
        {
            "page": entry["page"],
            "width": entry["width"],
            "block": entry["block_width"],
            "columns": entry["columns"],
            "rungs": len(entry["rungs"]),
            "rung_heights": " ".join(f"{height:g}" for height in entry["heights"]),
            "meaning_min": min(rung["meaning_width"] for rung in entry["rungs"]),
            "meaning_height": _span([rung["meaning_height"] for rung in entry["rungs"]]),
            "max_lines": max(rung["lines"] for rung in entry["rungs"]),
            "overflowing": " ".join(r["rung"] for r in entry["rungs"] if r["overflow"]) or "-",
        }
        for entry in report
    ]


def measure_math(
    base: str, pages: Sequence[str], *, widths: Sequence[int], presses: Sequence[str] = ()
) -> list[dict[str, Any]]:
    """Every formula's face and its text's on each page at each width, one entry per
    surface, text face and math face. Each page is scrolled through until all its math
    is typeset, and each selector in `presses` that matches is pressed first, so what
    it opens is typeset and counted."""
    from playwright.sync_api import sync_playwright  # noqa: PLC0415

    results: list[dict[str, Any]] = []
    with sync_playwright() as driver:
        browser = _launch(driver)
        for width in widths:
            for name in pages:
                print(f"measuring {name} at {width}", file=sys.stderr, flush=True)
                page = browser.new_page(viewport={"width": width, "height": 900})
                page.goto(f"{base}/{name}", wait_until="load")
                pending = settle_math(page)
                for selector in presses:
                    if page.locator(selector).count():
                        press(page, selector)
                        page.keyboard.press("Escape")
                results.extend(
                    {"page": name, "width": width, "untypeset": pending, **row}
                    for row in page.evaluate(MATH_FACES)
                )
                page.close()
        browser.close()
    return results


def measure_space(
    base: str, pages: Sequence[str], *, widths: Sequence[int], presses: Sequence[str] = ()
) -> list[dict[str, Any]]:
    """The space around every table and heading on each page at each width, once its
    math is typeset, as rows of `kind` `first` (the page's first block, with the space
    from the bar down to it), `table` or `heading`. Each selector in `presses`
    that matches is then pressed, and what it opened is reported with the selector as
    its `state`; the page as loaded is the state `page`."""
    from playwright.sync_api import sync_playwright  # noqa: PLC0415

    results: list[dict[str, Any]] = []

    def collect(name: str, width: int, state: str, found: dict[str, Any]) -> None:
        for kind, key in (("first", "first"), ("table", "tables"), ("heading", "headings")):
            results.extend(
                {"page": name, "width": width, "state": state, "kind": kind, **row}
                for row in found[key]
            )

    with sync_playwright() as driver:
        browser = _launch(driver)
        for width in widths:
            for name in pages:
                print(f"measuring {name} at {width}", file=sys.stderr, flush=True)
                page = browser.new_page(viewport={"width": width, "height": 900})
                page.goto(f"{base}/{name}", wait_until="load")
                settle_math(page)
                collect(name, width, "page", page.evaluate(SPACING))
                for selector in presses:
                    # A match that is not shown, a row inside a closed disclosure, cannot
                    # be pressed; an earlier press may be what opens it.
                    target = page.locator(selector)
                    if not target.count() or not target.first.is_visible():
                        continue
                    press(page, selector)
                    collect(name, width, selector, page.evaluate(SPACING, {"scope": OPENED}))
                    page.keyboard.press("Escape")
                page.close()
        browser.close()
    return results


def measure_header(
    base: str, pages: Sequence[str], *, widths: Sequence[int]
) -> list[dict[str, Any]]:
    """Where each page's header stands at each width (`preview_site/header`), one flat
    row a page and width: the top and bottom of the bar, of the rule under it, of the
    section tabs and of the first block, with the element the rule is drawn on, the
    current tab and the first block's name; then the header's type, the font size of the
    body's prose, the site's name, a link in the bar and a section tab, and the lines the
    bar's links take. A part a page lacks is left empty."""
    rows: list[dict[str, Any]] = []
    for name, width, found in _evaluate(base, pages, widths=widths, script=HEADER):
        row: dict[str, Any] = {"page": name, "width": width}
        for part in ("nav", "rule", "tabs", "first"):
            box = found[part] or {}
            row[f"{part}_top"] = box.get("top", "")
            row[f"{part}_bottom"] = box.get("bottom", "")
        row["rule_on"] = (found["rule"] or {}).get("on", "")
        row["current_tab"] = (found["tabs"] or {}).get("current") or ""
        row["first"] = (found["first"] or {}).get("block", "")
        sizes = found["type"]
        row["body"] = sizes["body"] or (sizes["scale"] or {}).get("prose", "")
        row["name"] = sizes["name"] or ""
        row["name_shown"] = "yes" if sizes["name_shown"] else "no"
        row["link"] = sizes["link"] or ""
        row["tab"] = sizes["tab"] or ""
        row["links_rows"] = sizes["links_rows"]
        row["overflow"] = sizes["overflow"]
        rows.append(row)
    return rows


def measure_baselines(
    base: str, pages: Sequence[str], *, widths: Sequence[int]
) -> list[dict[str, Any]]:
    """The baselines of each page's header labels at each width (`preview_site/baselines`),
    one flat row a page and width: the name's, the links' line by line, the tabs', how far
    the name stands off the links of the first line, and how far the current link and the
    current tab stand over the rule and the foot of the tab strip."""
    rows: list[dict[str, Any]] = []
    for name, width, found in _evaluate(base, pages, widths=widths, script=BASELINES):
        lines: dict[int, set[float]] = {}
        for link in found["links"]:
            lines.setdefault(link["top"], set()).add(link["baseline"])
        ordered = [sorted(lines[top]) for top in sorted(lines)]
        first = ordered[0][0] if ordered else None
        shown = found["name"] is not None and first is not None
        rows.append(
            {
                "page": name,
                "width": width,
                "name": "" if found["name"] is None else found["name"],
                "links": " / ".join(
                    " ".join(f"{value:g}" for value in line) for line in ordered
                ),
                "name_off_links": round(found["name"] - first, 2) if shown else "",
                "tabs": " ".join(
                    f"{value:g}" for value in sorted({t["baseline"] for t in found["tabs"]})
                ),
                "rule": "" if found["rule"] is None else found["rule"],
                "current_above_rule": found["current_above_rule"] or "",
                "current_tab_above_foot": found["current_tab_above_foot"] or "",
            }
        )
    return rows


def measure_popovers(
    base: str,
    pages: Sequence[str],
    *,
    widths: Sequence[int],
    heights: Sequence[int],
    presses: Sequence[str],
    shots: Path | None = None,
) -> list[dict[str, Any]]:
    """What each selector in `presses` opens on each page, in a window of each width and
    height: one row a popover, with its box, its margins, the share of its content it
    shows without scrolling and the words in it broken across lines. A page is scrolled
    through first only when a selector matches nothing as loaded, which is how the atlas
    grid's later cells are placed. With `shots`, the window is shot there with each
    popover open: `popover-<page>-<width>x<height>-press<n>.png`."""
    from playwright.sync_api import sync_playwright  # noqa: PLC0415

    results: list[dict[str, Any]] = []
    if shots is not None:
        shots.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as driver:
        browser = _launch(driver)
        for width in widths:
            for height in heights:
                for name in pages:
                    print(f"measuring {name} at {width}x{height}", file=sys.stderr, flush=True)
                    page = browser.new_page(viewport={"width": width, "height": height})
                    page.goto(f"{base}/{name}", wait_until="load")
                    page.wait_for_timeout(300)
                    if not all(page.locator(selector).count() for selector in presses):
                        settle_math(page)
                    for index, selector in enumerate(presses, start=1):
                        target = page.locator(selector)
                        if not target.count() or not target.first.is_visible():
                            continue
                        press(page, selector)
                        split = split_words(page)
                        results.extend(
                            {
                                "page": name,
                                "width": width,
                                "press": selector,
                                **row,
                                "split_words": len(split),
                                "split": split,
                            }
                            for row in page.evaluate(POPOVER)
                        )
                        if shots is not None:
                            stem = f"popover-{shot_stem(name)}-{width}x{height}-press{index}"
                            page.screenshot(path=str(shots / f"{stem}.png"))
                        page.keyboard.press("Escape")
                    page.close()
        browser.close()
    return results


#: How much of a table a `columns` shot shows, in CSS pixels from the top of its filter
#: bar: the header and enough rows to see how the columns share the width.
COLUMN_SHOT_HEIGHT = 1100


def measure_columns(
    base: str,
    pages: Sequence[str],
    *,
    widths: Sequence[int],
    shots: Path | None = None,
    scroll_check: bool = False,
) -> list[dict[str, Any]]:
    """Every shared data table's columns on each page at each width, once its math is
    typeset, one entry a table: its width, how far it runs past what scrolls it sideways,
    and each column with its width, the most lines a cell of it takes, the words a line
    break splits and the tallest row it sets. With `shots`, each table is also shot
    there at each width, from the top of its filter bar down `COLUMN_SHOT_HEIGHT`
    pixels: `columns-<page>-<n>-<width>.png`, `<n>` counting the page's tables from 0."""
    from playwright.sync_api import sync_playwright  # noqa: PLC0415

    results: list[dict[str, Any]] = []
    if shots is not None:
        shots.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as driver:
        browser = _launch(driver)
        for width in widths:
            for name in pages:
                print(f"measuring {name} at {width}", file=sys.stderr, flush=True)
                page = browser.new_page(viewport={"width": width, "height": 900})
                page.goto(f"{base}/{name}", wait_until="load")
                settle_math(page)
                found: list[dict[str, Any]] = page.evaluate(COLUMNS)
                if scroll_check:
                    # Report both scroll extremes and the restored geometry. The
                    # observer keeps changed widths visible rather than accepting them.
                    states = {"initial": [_column_geometry(table) for table in found]}
                    for state, position in (
                        ("vertical_end", "bottom"),
                        ("horizontal_end", "right"),
                        ("restored", "reset"),
                    ):
                        page.evaluate(_COLUMNS_SCROLL, {"position": position})
                        states[state] = [
                            _column_geometry(table) for table in page.evaluate(COLUMNS)
                        ]
                    if any(len(tables) != len(found) for tables in states.values()):
                        raise ValueError("the visible table set changed while scrolling")
                    for index, table in enumerate(found):
                        table["scroll_geometry"] = {
                            state: tables[index] for state, tables in states.items()
                        }
                results.extend({"page": name, "width": width, **table} for table in found)
                stem = re.sub(r"[^A-Za-z0-9]+", "-", name.removesuffix(".html")).strip("-")
                for index, table in enumerate(found):
                    if shots is None:
                        break
                    page.screenshot(
                        path=str(shots / f"columns-{stem}-{index}-{width}.png"),
                        full_page=True,
                        clip={
                            "x": 0,
                            "y": max(0, table["top"] - 16),
                            "width": width,
                            "height": min(table["height"] + 32, COLUMN_SHOT_HEIGHT),
                        },
                    )
                page.close()
        browser.close()
    return results


def _column_geometry(table: dict[str, Any]) -> dict[str, Any]:
    """Keep layout and scroll positions without duplicating each column's contents."""
    return {
        **{
            key: table[key]
            for key in (
                "table",
                "layout",
                "table_width",
                "frame_width",
                "scrolls",
                "page_scrolls",
                "window_scroll_x",
                "window_scroll_y",
                "frame_scroll_left",
                "shown_rows",
            )
        },
        "column_widths": {column["column"]: column["width"] for column in table["columns"]},
    }


def measure_chips(
    base: str, pages: Sequence[str], *, widths: Sequence[int], presses: Sequence[str] = ()
) -> list[dict[str, Any]]:
    """Every chip each page shows at each width, once its math is typeset, one entry a
    chip, with the page as loaded as its `state`. Each selector in `presses` that
    matches is then pressed, and the chips of what it opened are reported with the
    selector as their `state`."""
    from playwright.sync_api import sync_playwright  # noqa: PLC0415

    results: list[dict[str, Any]] = []
    with sync_playwright() as driver:
        browser = _launch(driver)
        for width in widths:
            for name in pages:
                print(f"measuring {name} at {width}", file=sys.stderr, flush=True)
                page = browser.new_page(viewport={"width": width, "height": 900})
                page.goto(f"{base}/{name}", wait_until="load")
                settle_math(page)
                results.extend(
                    {"page": name, "width": width, "state": "page", **chip}
                    for chip in page.evaluate(CHIPS)
                )
                for selector in presses:
                    target = page.locator(selector)
                    if not target.count() or not target.first.is_visible():
                        continue
                    press(page, selector)
                    results.extend(
                        {"page": name, "width": width, "state": selector, **chip}
                        for chip in page.evaluate(CHIPS, {"scope": OPENED})
                    )
                    page.keyboard.press("Escape")
                page.close()
        browser.close()
    return results


def measure_credits(
    base: str, pages: Sequence[str], *, widths: Sequence[int], shots: Path | None = None
) -> list[dict[str, Any]]:
    """The front of each page at each width, once its math is typeset, one row an item
    (`probes/measure_site_pages/credits.js`): each chip of the formats row, then each
    line of the credits, the series strip's last, with what it is, the weight it is set
    at, the weights of the names and the links in it, the space above it in line heights,
    the lines its words take and its width as a share of the column's. This is what
    `tests/test_site_glyphs.py` holds the papers' fronts together with, in the browser;
    `devtools.paper_structure` reads the same front from the markup. With `shots`, the
    page is measured in the light and the dark scheme, each row says which, and the
    front, from the top of the page to the foot of the credits, is shot there at each
    width in each: `front-<page>-<width>-<scheme>.png`."""
    from playwright.sync_api import sync_playwright  # noqa: PLC0415

    schemes = ("light", "dark") if shots is not None else ("light",)
    if shots is not None:
        shots.mkdir(parents=True, exist_ok=True)
    results: list[dict[str, Any]] = []
    with sync_playwright() as driver:
        browser = _launch(driver)
        for width, name, scheme in itertools.product(widths, pages, schemes):
            print(f"measuring {name} at {width}, {scheme}", file=sys.stderr, flush=True)
            page = browser.new_page(
                viewport={"width": width, "height": 900}, color_scheme=scheme
            )
            page.goto(f"{base}/{name}", wait_until="load")
            settle_math(page)
            results.extend(
                {"page": name, "width": width, "scheme": scheme, **row}
                for row in page.evaluate(CREDITS)
            )
            if shots is not None:
                box = page.locator(".credits").first.bounding_box()
                foot = box["y"] + box["height"] if box else 900
                page.screenshot(
                    path=str(shots / f"front-{shot_stem(name)}-{width}-{scheme}.png"),
                    clip={"x": 0, "y": 0, "width": width, "height": min(foot + 32, 900)},
                )
            page.close()
        browser.close()
    return results


#: The attribute `glyphs` marks its samples with, so the browser can be asked which
#: platform face drew each and each can be shot.
GLYPH_MARK = "data-glyph-sample"
#: The device pixels to a CSS pixel `glyphs` lays a page out and shoots it at.
GLYPH_SCALE = 2
#: How long `glyphs` waits for one formula to be shot before reporting it without ink.
SHOT_WAIT_MS = 3_000
#: What decides how a role's text is drawn, in the order `glyphs` reports it.
TEXT_PROPERTIES = (
    "family",
    "host_faces",
    "weight",
    "size",
    "line_height",
    "style",
    "color",
    "opacity",
    "text_rendering",
    "smoothing",
    "synthesis",
    "optical_sizing",
    "variation",
    "features",
    "letter_spacing",
    "transform",
)
#: The same for a formula. `scale` is its font size over its text's; `text_color` is
#: `same` where the formula takes the colour of the words around it.
MATH_PROPERTIES = (
    "typeset",
    "math",
    "host_faces",
    "weight",
    "scale",
    "text",
    "text_color",
    "opacity",
    "text_rendering",
    "smoothing",
    "synthesis",
    "face_mark",
)
_RGB = re.compile(r"rgb\((\d+) (\d+) (\d+)")
#: How a face that came off the reader's machine is marked in a `glyphs` report.
HOST = " (host)"
#: The weight of a variable face's instance, as Blink writes it into the instance's
#: PostScript name: sixteen-bit fixed point, in hexadecimal.
_VARIABLE_WEIGHT = re.compile(r"_wght([0-9A-F]+)0000$")


def ink(png: bytes, *, color: str, size: float, scale: float = GLYPH_SCALE) -> float:
    """How much ink a shot of one formula holds, in square em of its own font size.

    Each pixel counts for its coverage, how far it stands from the ground toward the
    text's colour, so the sum is the area the glyphs paint: the same formula at the same
    size, drawn thinner, holds less. The ground is the median of the shot's border, and
    the colour is the formula's own computed one, so a dark page reads as a light one
    does. A measure of weight as drawn, which no computed style reports.
    """
    import numpy as np  # noqa: PLC0415
    from PIL import Image  # noqa: PLC0415

    found = _RGB.match(color)
    if found is None:
        raise ValueError(f"not a colour the glyphs probe writes: {color}")
    with Image.open(io.BytesIO(png)) as image:
        pixels = np.asarray(image.convert("RGB"), dtype=np.float64)
    border = np.concatenate([pixels[0], pixels[-1], pixels[:, 0], pixels[:, -1]])
    ground = np.median(border, axis=0)
    span = np.array([float(part) for part in found.groups()]) - ground
    if not span.any():
        return 0.0
    coverage = np.clip((pixels - ground) @ span / float(span @ span), 0.0, 1.0)
    return round(float(coverage.sum()) / (size * scale) ** 2, 4)


#: A DOM text node's `nodeType`.
TEXT_NODE = 3


def _platform_faces(session: Any, root: int, mark: str) -> list[str]:
    """The platform faces Blink drew the marked element's own text with, by name; a face
    the page did not ship is named as the reader's own (`host`)."""
    node = session.send(
        "DOM.querySelector", {"nodeId": root, "selector": f'[{GLYPH_MARK}="{mark}"]'}
    )
    fonts = session.send("CSS.getPlatformFontsForNode", {"nodeId": node["nodeId"]})["fonts"]
    return sorted({_platform_face(font) for font in fonts})


def _own_text_faces(session: Any, root: int, mark: str) -> list[str]:
    """The platform faces Blink drew the marked element's own text nodes with, by name.

    Asked of the element, `CSS.getPlatformFontsForNode` also counts the glyphs of inline
    children laid out in its line boxes: a result cell with words of its own and a star
    after them reported the star's host face as the cell's (T-064's row, 2026-10-03),
    though the star is a run of its own, measured under its own role. A text row stands
    for the element's own text, so its faces are asked of each of its text nodes.
    """
    node = session.send(
        "DOM.querySelector", {"nodeId": root, "selector": f'[{GLYPH_MARK}="{mark}"]'}
    )
    described = session.send("DOM.describeNode", {"nodeId": node["nodeId"], "depth": 1})
    backend = [
        child["backendNodeId"]
        for child in described["node"].get("children", [])
        if child["nodeType"] == TEXT_NODE and child.get("nodeValue", "").strip()
    ]
    if not backend:
        return _platform_faces(session, root, mark)
    pushed = session.send("DOM.pushNodesByBackendIdsToFrontend", {"backendNodeIds": backend})
    fonts = [
        font
        for text in pushed["nodeIds"]
        for font in session.send("CSS.getPlatformFontsForNode", {"nodeId": text})["fonts"]
    ]
    return sorted({_platform_face(font) for font in fonts})


def _platform_face(font: dict[str, Any]) -> str:
    """One platform face by the name that says most: a face the page ships by its
    PostScript name, with a variable face's weight read out of the instance Blink names
    (`SourceSans3-Roman_wght19A0000` is the 410 the sans is set at), so the weight a run
    is drawn at is reported and not only the weight it asks for; a face off the reader's
    machine by its family, marked `HOST`."""
    if not font["isCustomFont"]:
        return str(font["familyName"]) + HOST
    name = str(font.get("postScriptName") or font["familyName"])
    instance = _VARIABLE_WEIGHT.search(name)
    if instance is None:
        return name
    return f"{name[: instance.start()]}@{int(instance.group(1), 16)}"


def _host_faces(faces: Iterable[str]) -> str:
    """The faces among `faces` that came off the reader's machine, which no page of the
    site may draw from: every run is set in a face the page ships."""
    return ", ".join(sorted({face for face in faces if face.endswith(HOST)}))


def read_glyphs(page: Page, *, tex: Sequence[str] = ()) -> dict[str, Any]:
    """Read the owned glyph probe on an already loaded page without extra measurement."""
    return page.evaluate(
        GLYPHS, {"wrappers": MATH_WRAPPERS, "mark": GLYPH_MARK, "tex": list(tex)}
    )


def measure_glyphs(
    base: str,
    pages: Sequence[str],
    *,
    widths: Sequence[int],
    schemes: Sequence[str] = ("light",),
    tex: Sequence[str] = (),
    style: str | None = None,
    platform: str | None = None,
    shots: Path | None = None,
    every_ink: bool = True,
) -> list[dict[str, Any]]:
    """How each page's glyphs are drawn at each width in each colour scheme, one entry a
    page: its text roles, its formulas by surface, the faces it declares and what it
    stamps on its root (`probes/measure_site_pages/glyphs.js`). Each sample also carries
    `drawn`, the platform face the browser drew it from, and each formula `ink`, the
    area its glyphs paint (`ink`). `style` is a stylesheet added to each page before it
    is measured, which is how one property is toggled to see what it changes.
    `platform` is what the page is told `navigator.platform` is, before its own scripts
    run, which is how the choice a page makes by platform is seen on another machine;
    the glyphs are still this machine's. With `shots`, every formula sampled is shot
    there at twice its size:
    `glyphs-<page>-<width>-<scheme>-<surface>-<layout>-<n>.png`. Without `every_ink`,
    only the formulas `tex` names are shot and given their ink, which is most of what a
    long page costs to measure."""
    from playwright.sync_api import Error as PlaywrightError  # noqa: PLC0415
    from playwright.sync_api import sync_playwright  # noqa: PLC0415

    results: list[dict[str, Any]] = []
    if shots is not None:
        shots.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as driver:
        browser = _launch(driver)
        for width, scheme, name in itertools.product(widths, schemes, pages):
            print(f"measuring {name} at {width}, {scheme}", file=sys.stderr, flush=True)
            page = browser.new_page(
                viewport={"width": width, "height": 900},
                device_scale_factor=GLYPH_SCALE,
                color_scheme="dark" if scheme == "dark" else "light",
                reduced_motion=motion_for(name),
            )
            if platform is not None:
                page.add_init_script(applied(PLATFORM, platform))
            fetched: list[str] = []
            failed: list[str] = []
            page.on(
                "request",
                lambda request, fetched=fetched: (
                    fetched.append(request.url) if request.resource_type == "font" else None
                ),
            )
            page.on(
                "requestfailed",
                lambda request, failed=failed: (
                    failed.append(request.url) if request.resource_type == "font" else None
                ),
            )
            page.goto(f"{base}/{name}", wait_until="load")
            untypeset = settle_math(page)
            if style:
                page.add_style_tag(content=style)
                page.wait_for_timeout(200)
            found = read_glyphs(page, tex=tex)
            session = page.context.new_cdp_session(page)
            session.send("DOM.enable")
            session.send("CSS.enable")
            root = session.send("DOM.getDocument", {"depth": 0})["root"]["nodeId"]
            for row in found["text"]:
                faces = _own_text_faces(session, root, row["mark"])
                row["drawn"], row["host_faces"] = ", ".join(faces), _host_faces(faces)
            stem = f"glyphs-{shot_stem(name)}-{width}-{scheme}"
            for index, row in enumerate(found["math"]):
                parts = {
                    part: _platform_faces(session, root, mark)
                    for part, mark in row.pop("parts").items()
                }
                row["drawn"] = "; ".join(
                    f"{part}: {', '.join(faces)}" for part, faces in parts.items()
                )
                row["host_faces"] = _host_faces(itertools.chain(*parts.values()))
                row["ink"] = ""
                if not (every_ink or row["compared"]):
                    continue
                # A formula a scroller clips, a table's far column on a phone, cannot be
                # shot; it is reported without its ink.
                target = page.locator(f'[{GLYPH_MARK}="{row["mark"]}"]')
                try:
                    png = target.screenshot(timeout=SHOT_WAIT_MS)
                except PlaywrightError:
                    continue
                row["ink"] = ink(png, color=row["color"], size=row["size"])
                if shots is not None:
                    where = re.sub(r"[^a-z]+", "-", f"{row['surface']}-{row['layout']}")
                    row["shot"] = f"{stem}-{where}-{index}.png"
                    (shots / row["shot"]).write_bytes(png)
            session.detach()
            results.append(
                {
                    "page": name,
                    "width": width,
                    "scheme": scheme,
                    "untypeset": untypeset,
                    "font_requests": [url for url in fetched if not url.startswith("data:")],
                    "failed_requests": failed,
                    **found,
                }
            )
            page.close()
        browser.close()
    return results


def _glyph_settings(
    entry: dict[str, Any],
) -> dict[tuple[str, str], dict[str, set[str]]]:
    """One `glyphs` entry as the distinct values of each property, by part and role: a
    text role by its name, a formula by its surface and layout."""
    settings: dict[tuple[str, str], dict[str, set[str]]] = {}
    for part, names, rows in (
        ("text", TEXT_PROPERTIES, entry["text"]),
        ("math", MATH_PROPERTIES, entry["math"]),
    ):
        for row in rows:
            role = row["role"] if part == "text" else f"{row['surface']}, {row['layout']}"
            values = settings.setdefault((part, role), {})
            for name in names:
                values.setdefault(name, set()).add(str(row[name]))
    page = settings.setdefault(("page", "document"), {})
    page["KaTeX"] = {entry["katex"]}
    page["untypeset formulas"] = {str(entry["untypeset"])}
    page["font requests"] = {str(len(entry["font_requests"]))}
    page["failed requests"] = {str(len(entry["failed_requests"]))}
    for name, value in (entry["root"] | entry["tokens"]).items():
        page[name] = {value}
    for face in entry["faces"]:
        named = f"face {face['family']} {face['weight']} {face['style']}"
        # A face no glyph asked for stays unloaded, which says nothing of how a page is
        # drawn; one that failed to load does.
        optional = face.get("optional_local", False)
        source = (
            "optional local"
            if optional
            else "inlined"
            if face["inlined"]
            else "shared"
            if face.get("shared")
            else "fetched"
        )
        failed = (
            (", unavailable" if optional else ", failed") if face["status"] == "error" else ""
        )
        page.setdefault(named, set()).add(f"{face['display']}, {source}{failed}")
    return settings


def _values(values: set[str] | None) -> str:
    return " / ".join(sorted(values)) if values else "-"


def glyph_differences(report: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Every property a page sets differently from the first page of a `glyphs` report,
    which is the explainer by default, at each width and scheme: one row a role and
    property, for each role both pages have, with the distinct values each page sets.
    A face one page declares and the other does not is a row too; a face that neither
    loaded is not a difference."""
    rows: list[dict[str, Any]] = []
    for width, scheme in dict.fromkeys((entry["width"], entry["scheme"]) for entry in report):
        at = [entry for entry in report if (entry["width"], entry["scheme"]) == (width, scheme)]
        reference = _glyph_settings(at[0])
        for entry in at[1:]:
            here = _glyph_settings(entry)
            for (part, role), values in here.items():
                against = reference.get((part, role))
                if against is None:
                    continue
                names = dict.fromkeys((*against, *values)) if part == "page" else values
                rows.extend(
                    {
                        "width": width,
                        "scheme": scheme,
                        "part": part,
                        "role": role,
                        "property": name,
                        at[0]["page"]: _values(against.get(name)),
                        entry["page"]: _values(values.get(name)),
                    }
                    for name in names
                    if against.get(name) != values.get(name)
                )
    return rows


def glyph_summary(report: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """A `glyphs` report as the distinct settings of each role across its pages, one row
    a setting with the pages that set the role that way: a text role's face, weight,
    size over line height and style, and a formula's face, weight, scale against its
    text and `text-rendering`, by surface. A role with one row is set one way on every
    page that has it."""
    seen: dict[tuple[Any, ...], list[str]] = {}
    for entry in report:
        where = f"{entry['page']} ({entry['width']})"
        for row in entry["text"]:
            setting = (
                f"{row['family']} {row['weight']}"
                f"{'' if row['style'] == 'normal' else ' ' + row['style']}, "
                f"{row['size']:g}/{row['line_height']}"
            )
            pages = seen.setdefault((entry["scheme"], "text", row["role"], setting), [])
            pages.extend([] if where in pages else [where])
        for row in entry["math"]:
            setting = (
                f"{row['math']} {row['weight']} at {row['scale']:g} of "
                f"{row['text']} {row['text_weight']}, {row['text_rendering']}"
            )
            role = f"{row['surface']}, {row['layout']}"
            pages = seen.setdefault((entry["scheme"], "math", role, setting), [])
            pages.extend([] if where in pages else [where])
    return [
        {
            "scheme": scheme,
            "part": part,
            "role": role,
            "setting": setting,
            "pages": ", ".join(pages),
        }
        for (scheme, part, role, setting), pages in sorted(seen.items())
    ]


#: How a formula is typeset on every page: KaTeX's HTML over the MathML a reader without
#: scripts, or a screen reader, is given.
TYPESET = "KaTeX HTML + MathML"
#: The root attribute the publication layer's head script stamps on macOS, which its
#: stylesheet's math rule reads (`render_n11_lower_bounds_explainer.publication_layer`).
NATIVE_METRICS = "data-squares-native-math-metrics"
#: The serif and sans math composites, as `glyphs` names a formula's face.
SERIF_MATH, SANS_MATH = "KPress Math Text", "KPress Math Text Sans"
#: The sans weights KPress sets by its own rules, outside the three the shared layer
#: names: a table's head and bold sans mathematics at 650, and an `h4` at 540
#: (`templates/paper-design.md`, Text).
KPRESS_SANS_WEIGHTS = (540, 650)
#: How far a size may stand from the token it is derived from, in CSS pixels.
SIZE_TOLERANCE = 0.02


def _role_rules(entry: dict[str, Any]) -> dict[str, tuple[float | None, float | None]]:
    """The size and weight the shared text layer sets each role at on this page, from
    the tokens the page itself resolves (`templates/paper-type.css`): a role's size as
    its scale of the prose or of the sans base, and its weight as one of the sans
    weights, with `None` where the layer leaves it to the role's place (a link is as
    heavy as its text). Only the roles one rule sets on every page are here."""
    tokens = entry["tokens"]
    base = tokens["--kpress-font-size-base"]
    sans = base * tokens["--paper-font-scale-sans"]
    regular = tokens["--kpress-font-weight-sans-regular"]
    medium = tokens["--paper-font-weight-sans-medium"]
    bold = tokens["--paper-font-weight-sans-bold"]
    note = sans * tokens["--paper-note-scale"]
    return {
        "prose": (base, 400),
        "list item": (base, 400),
        "h2": (tokens["--kpress-font-size-h2"], 400),
        "page title": (sans * tokens["--paper-title-scale"], medium),
        "caption": (note, regular),
        "caption lead": (note, bold),
        "footnote": (note, regular),
        "colophon": (sans * tokens["--paper-colophon-scale"], regular),
        "nav name": (sans, bold),
        "nav link": (note, medium),
        "section tab": (note, medium),
    }


def glyph_problems(entry: dict[str, Any], *, katex: str | None = None) -> list[str]:
    """Where one `glyphs` entry departs from what the shared layers set, as sentences;
    none on a page set as `templates/paper-design.md` describes.

    A page: every formula typeset, by the KaTeX `katex` names when one is given; every
    shipped face inlined or a file of the site's shared assets (`site_assets`), and
    loaded; the optional local-only prose and sans fallbacks may be absent. Nothing else
    fetched.
    A page of the publication layer: its
    platform flag set on macOS and nowhere else. A formula: KaTeX's HTML over MathML; at
    its text's own size and in its text's own colour; at the regular weight of the
    composite it is set in; every glyph from a face the page ships; and rasterised as
    the text around it is, except under the publication layer off macOS, where the
    layer's `geometricPrecision` stands. Text, on a page with a reading column: each
    role the shared layer sets on every page at the size and weight its tokens come to
    (`_role_rules`), where the role is in the face the layer sets it in; and every sans
    run at one of the layer's three sans weights or one of KPress's own two. A face off
    the reader's machine under any sampled run is reported too.
    """
    problems: list[str] = []
    if entry["untypeset"]:
        problems.append(f"{entry['untypeset']} formulas are left untypeset")
    runtime = entry.get("runtime_katex", entry["katex"])
    if (
        katex is not None
        and any(row.get("prepared") != "yes" for row in entry["math"])
        and runtime != katex
    ):
        problems.append(f"the page runs KaTeX {runtime or 'not at all'}, not {katex}")
    if katex is not None and any(row.get("prepared") == "yes" for row in entry["math"]):
        version = entry.get("prepared_katex", "")
        if version != katex:
            problems.append(
                f"the prepared math uses KaTeX {version or 'without provenance'}, not {katex}"
            )
    problems.extend(
        f"a face is fetched: {url}"
        for url in entry["font_requests"]
        if not _SHARED_FACE.search(url)
    )
    problems.extend(f"a face failed to arrive: {url}" for url in entry["failed_requests"])
    for face in entry["faces"]:
        named = f"{face['family']} {face['weight']} {face['style']}"
        if not face["inlined"] and not face.get("shared"):
            problems.append(f"the face {named} is neither inlined nor a shared asset")
        if face["status"] == "error" and not face.get("optional_local", False):
            problems.append(f"the face {named} failed to load")
    mac = entry["platform"].startswith("Mac")
    flagged = entry["root"].get(NATIVE_METRICS) == "true"
    if entry["publication"] and flagged != mac:
        problems.append(
            f"the publication layer's platform flag is {'set' if flagged else 'not set'} "
            f"on {entry['platform']}"
        )
    regular = entry["tokens"].get("--kpress-font-weight-sans-regular")
    for row in entry["math"]:
        where = f"{row['surface']}, {row['layout']} formula `{row['example']}`"
        rendering = (
            "geometricprecision"
            if entry["publication"] and not mac
            else row["text_text_rendering"]
        )
        weight = {SERIF_MATH: "400", SANS_MATH: f"{regular:g}" if regular else None}
        expected = {
            "typeset": TYPESET,
            "scale": 1,
            "text_color": "same",
            "host_faces": "",
            "text_rendering": rendering,
            "weight": weight.get(row["math"]) or row["weight"],
        }
        problems.extend(
            f"{where}: {name} is {row[name] or 'empty'}, not {wanted or 'empty'}"
            for name, wanted in expected.items()
            if row[name] != wanted
        )
    if not entry["reading"]:
        return problems
    rules = _role_rules(entry)
    faces = {"prose": entry["prose"], "list item": entry["prose"], "h2": entry["prose"]}
    tokens = entry["tokens"]
    weights = {
        regular,
        tokens["--paper-font-weight-sans-medium"],
        tokens["--paper-font-weight-sans-bold"],
        *KPRESS_SANS_WEIGHTS,
    }
    for row in entry["text"]:
        where = f"{row['role']} `{row['example']}`"
        if row["host_faces"]:
            problems.append(f"{where}: drawn from {row['host_faces']}")
        if row["family"] == entry["sans"] and float(row["weight"]) not in weights:
            problems.append(f"{where}: sans text at {row['weight']}, which no token names")
        size, weight = rules.get(row["role"], (None, None))
        if row["family"] != faces.get(row["role"], entry["sans"]):
            continue
        if size is not None and abs(row["size"] - size) > SIZE_TOLERANCE:
            problems.append(f"{where}: {row['size']:g}px, not the role's {size:g}px")
        if weight is not None and float(row["weight"]) != weight:
            problems.append(f"{where}: weight {row['weight']}, not the role's {weight:g}")
    return problems


def problem_rows(report: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """A `glyphs` report as its problems, one row each (`glyph_problems`), against the
    KaTeX this checkout's KPress ships."""
    return [
        {
            "page": entry["page"],
            "width": entry["width"],
            "scheme": entry["scheme"],
            "problem": problem,
        }
        for entry in report
        for problem in glyph_problems(entry, katex=shipped_katex())
    ]


def shipped_katex() -> str:
    """The version of KaTeX the vendored KPress ships, which every page inlines."""
    from devtools.render_n11_lower_bounds_explainer import kpress_static  # noqa: PLC0415

    return (kpress_static() / "katex" / "VERSION").read_text(encoding="utf-8").split()[-1]


def glyph_rows(report: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """A `glyphs` report flattened to one row a formula sampled: what it is set in, the
    face that drew it and the ink it holds."""
    return [
        {
            "page": entry["page"],
            "width": entry["width"],
            "scheme": entry["scheme"],
            "surface": row["surface"],
            "layout": row["layout"],
            "formulas": row["count"],
            "example": "`" + row["example"].replace("|", "\\|") + "`",
            **{name: row[name] for name in MATH_PROPERTIES},
            "glyphs": row["glyphs"],
            "drawn": row["drawn"],
            "size": row["size"],
            "ink": row["ink"],
        }
        for entry in report
        for row in entry["math"]
    ]


#: How far, in CSS pixels, a figure's drawing may stand off the centre of the column.
FIGURE_CENTRE_TOLERANCE = 1.0
#: How far what a drawing paints may stand off that centre, as a share of the drawing's
#: width. A tree or a flow chart is not symmetric, and the widest such lean on either
#: paper is 0.035; the optimality paper's first figure, a packing at the left of a canvas
#: nearly twice its width, stood 0.18 off.
INK_CENTRE_TOLERANCE = 0.06
#: The share of a drawing's width past which a run of its text is a caption or a title
#: lettered into it and not a label. The widest label on either paper is 0.56 of its
#: drawing; the titles that were lettered into the optimality paper's drawings before
#: they became captions ran from 0.62 to 0.97 of theirs.
LETTERED_SHARE = 0.6


def measure_figures(
    base: str,
    pages: Sequence[str],
    *,
    widths: Sequence[int],
    media: str = "screen",
    shots: Path | None = None,
) -> list[dict[str, Any]]:
    """Every figure of each page at each width, one row a figure, once the page's math
    is typeset (`probes/measure_site_pages/figures.js`): how wide its drawing is, how
    far its centre and the centre of what it paints stand from the centre of the reading
    column, whether it scrolls sideways or shares its row with controls, how many text
    elements its SVGs hold, the widest of them with its share of the drawing and any
    that reads as a sentence, and its caption. `media` lays the
    page out as it prints. With `shots`, each figure is shot there with its caption:
    `figures-<page>-<width>-<n>.png`."""
    from playwright.sync_api import sync_playwright  # noqa: PLC0415

    results: list[dict[str, Any]] = []
    if shots is not None:
        shots.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as driver:
        browser = _launch(driver)
        for width, name in itertools.product(widths, pages):
            print(f"measuring {name} at {width}", file=sys.stderr, flush=True)
            page = browser.new_page(
                viewport={"width": width, "height": 900},
                device_scale_factor=GLYPH_SCALE,
                reduced_motion=motion_for(name),
            )
            page.goto(f"{base}/{name}", wait_until="load")
            settle_math(page)
            page.emulate_media(media="print" if media == "print" else "screen")
            page.wait_for_timeout(300)
            found: list[dict[str, Any]] = page.evaluate(FIGURES, {"mark": GLYPH_MARK})
            for row in found:
                if shots is not None:
                    row["shot"] = f"figures-{shot_stem(name)}-{width}-{row['figure']}.png"
                    target = page.locator(f'figure:has([{GLYPH_MARK}="{row["mark"]}"])')
                    target.first.screenshot(path=str(shots / row["shot"]))
                results.append({"page": name, "width": width, **row})
            page.close()
        browser.close()
    return results


def figure_problems(row: dict[str, Any]) -> list[str]:
    """Where one figure departs from how a paper sets a figure (`templates/
    paper-design.md`, Figures): its drawing centred in the column, unless it scrolls
    sideways there or shares its row with controls, and what it paints centred with it;
    nothing lettered into the drawing but its labels, so no run most of the drawing
    wide and no sentence; and its caption under it, as a `figcaption`."""
    where = f"figure {row['figure']} ({row['named'] or row['drawing']})"
    problems: list[str] = []
    centred = row["scrolls"] or row["beside"]
    if not centred and abs(row["offset"]) > FIGURE_CENTRE_TOLERANCE:
        problems.append(f"{where}: its drawing stands {row['offset']:g}px off the centre")
    if not centred and abs(row["ink_offset"]) > INK_CENTRE_TOLERANCE:
        problems.append(
            f"{where}: what it draws stands {row['ink_offset']:.0%} of its width off the centre"
        )
    if row["sentences"]:
        problems.append(f"{where}: a sentence is lettered into the drawing: {row['sentences']}")
    if row["share"] > LETTERED_SHARE:
        problems.append(
            f"{where}: `{row['longest']}` is lettered across {row['share']:.0%} of the drawing"
        )
    if not row["caption"]:
        problems.append(f"{where}: no caption under it")
    return problems


def _distinct(values: Iterable[float]) -> str:
    """The distinct values among some measurements, least first, a space apart."""
    return " ".join(f"{value:g}" for value in sorted(set(values)))


def chip_rows(report: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """A `chips` report as a table: one row for each kind of chip on each surface of each
    page at each width and state, with how many there are, the distinct font sizes and
    block sizes found (one value each when every chip is one size), the most lines one
    takes, and the words of each chip that wraps."""
    groups: dict[tuple[Any, ...], list[dict[str, Any]]] = {}
    for chip in report:
        key = (chip["page"], chip["width"], chip["state"], chip["surface"], chip["chip"])
        groups.setdefault(key, []).append(chip)
    rows: list[dict[str, Any]] = []
    for (page, width, state, surface, kind), chips in groups.items():
        wrapped = sorted({chip["text"] for chip in chips if chip["lines"] != 1})
        rows.append(
            {
                "page": page,
                "width": width,
                "state": state,
                "surface": surface,
                "chip": kind,
                "count": len(chips),
                "font_size": _distinct(chip["font_size"] for chip in chips),
                "block_size": _distinct(chip["block_size"] for chip in chips),
                "max_lines": max(chip["lines"] for chip in chips),
                "wrapped": ", ".join(wrapped) or "-",
            }
        )
    return rows


def column_rows(report: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """A `columns` report as a table, one row a column: the table it belongs to and that
    table's width, the column's width and the share of the table it takes, the width of
    the widest content a cell of it holds (`held`) and the row whose cell holds it
    (`held_by`), how many of its cells show something past their own box (`overflows`),
    the most lines a cell of it takes,
    how many of its words a line break splits, and the tallest row
    whose height its cell sets, with that row's height and the lines the cell takes
    there; a dash where it sets no row's height. Then what its lines may not do, as
    counts: `split`, the values of a list of cases cut across lines; `wrapped`, the
    formulas set on more than one line, and `cuts`, the pieces of one a line ends after
    with no relation or binary operator to end it; and `stranded`, the punctuation that
    begins a line. `math_piece` is the width of the
    column's widest piece of typeset math, a dash where it holds none.
    `past_frame` is how far the table runs past what scrolls it sideways, 0 when it
    fits."""
    rows: list[dict[str, Any]] = []
    for entry in report:
        table = entry["table_width"]
        for column in entry["columns"]:
            tallest = column["tallest"]
            width = column["width"]
            piece = column.get("piece")
            rows.append(
                {
                    "page": entry["page"],
                    "width": entry["width"],
                    "section": entry["section"],
                    "layout": entry["layout"],
                    "shown": entry["shown_rows"],
                    "table": f"{table:g}",
                    "past_frame": f"{entry['scrolls']:g}",
                    "column": column["column"],
                    "col_width": "-" if width is None else f"{width:g}",
                    "share": "-" if width is None else f"{100 * width / table:.0f}%",
                    "held": f"{column['held']:g}" if "held" in column else "-",
                    "held_by": column.get("held_by") or "-",
                    "overflows": len(column.get("overflows", ())),
                    "max_lines": column["lines"],
                    "broken_words": len(column["broken"]),
                    "tallest_row": "-" if tallest is None else tallest["row"],
                    "row_height": "-" if tallest is None else f"{tallest['height']:g}",
                    "its_lines": "-" if tallest is None else tallest["lines"],
                    "split": len(column.get("split", ())),
                    "wrapped": column.get("wrapped", 0),
                    "cuts": len(column.get("cuts", ())),
                    "stranded": len(column.get("stranded", ())),
                    "math_piece": "-" if not piece else f"{piece['width']:g}",
                }
            )
    return rows


def _span(values: Sequence[Any]) -> str:
    """The least and the most of some measurements, or the one value they share; nothing
    for none, and a value that is not a number, such as a line height of `normal`, is
    passed over."""
    numbers = [value for value in values if isinstance(value, (int, float))]
    if not numbers:
        return ""
    low, high = min(numbers), max(numbers)
    return f"{low:g}" if low == high else f"{low:g} to {high:g}"


def space_rows(report: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """A `space` report as a table: one row for each page's first block, one a table and
    one a heading role.

    A page's first block comes with the space from the bar down to it, and each table
    with the space above and below it and what that space is measured to. Headings are
    grouped by page, width, state and role (`h2`, `span.site-card-value`): how many
    there are, their size, line height and leading, the most lines one takes, the most
    its box cannot show of its content, and the least and most space above and below.
    """
    rows: list[dict[str, Any]] = [
        {
            "page": row["page"],
            "width": row["width"],
            "state": row["state"],
            "what": (
                f"first block: {row['block']}"
                if row["kind"] == "first"
                else row["component"] + (" with bar" if row["bar"] else "")
            ),
            "where": row.get("section", ""),
            "count": 1,
            "size": "",
            "line_height": "",
            "leading": "",
            "lines": "",
            "overflow": "",
            "above": f"{row['above']:g}",
            "above_to": row["above_to"],
            "below": _span([row.get("below")]),
            "below_to": row.get("below_to", ""),
            "sides": _sides(row),
        }
        for row in report
        if row["kind"] in ("first", "table")
    ]
    groups: dict[tuple[str, int, str, str], list[dict[str, Any]]] = {}
    for row in report:
        if row["kind"] == "heading":
            key = (row["page"], row["width"], row["state"], row["role"])
            groups.setdefault(key, []).append(row)
    for (name, width, state, role), members in groups.items():
        rows.append(
            {
                "page": name,
                "width": width,
                "state": state,
                "what": role,
                "where": members[0]["text"],
                "count": len(members),
                "size": _span([member["size"] for member in members]),
                "line_height": _span([member["line_height"] for member in members]),
                "leading": _span([member["leading"] for member in members]),
                "lines": max((member["lines"] or 0) for member in members),
                "overflow": max(
                    member["overflow"] if member["clips"] else 0 for member in members
                ),
                "above": _span([member["above"] for member in members]),
                "above_to": members[0]["above_to"],
                "below": _span([member["below"] for member in members]),
                "below_to": members[0]["below_to"],
                "sides": "",
            }
        )
    return rows


def _sides(row: dict[str, Any]) -> str:
    """A table's side gutters as `left | right`, in pixels from the window's edges or
    its popover's, with its bar's where it has one and a note when the table scrolls
    sideways inside its wrap or spills out of it."""
    if "left" not in row:
        return ""
    text = f"{row['left']:g} / {row['right']:g} from the {row['sides_to']}"
    if row.get("bar_left") is not None:
        text += f"; bar {row['bar_left']:g} / {row['bar_right']:g}"
    if row.get("spills"):
        text += f"; spills {row['spills']:g}"
    return text + ("; scrolls" if row.get("scrolls") else "")


def _evaluate(
    base: str,
    pages: Sequence[str],
    *,
    widths: Sequence[int],
    script: str,
    media: str = "screen",
) -> list[tuple[str, int, Any]]:
    """`script` evaluated on each page at each width, once the page has loaded, in the
    given CSS media."""
    from playwright.sync_api import sync_playwright  # noqa: PLC0415

    results: list[tuple[str, int, Any]] = []
    with sync_playwright() as driver:
        browser = _launch(driver)
        for width in widths:
            for name in pages:
                # Reduced motion on the film's page, so its film stays at its poster.
                page = browser.new_page(
                    viewport={"width": width, "height": 900}, reduced_motion=motion_for(name)
                )
                page.emulate_media(media="print" if media == "print" else "screen")
                page.goto(f"{base}/{name}", wait_until="load")
                page.wait_for_timeout(300)
                results.append((name, width, page.evaluate(script)))
                page.close()
        browser.close()
    return results


def font_faces(site: Path, page: str) -> dict[str, str]:
    """Every `@font-face` block a page carries, inline or in a shared stylesheet it links
    (`site_assets.inlined_from`), keyed by its digest, valued by family."""
    from devtools import site_assets  # noqa: PLC0415

    faces: dict[str, str] = {}
    for block in FONT_FACE.findall(site_assets.inlined_from(site, page)):
        family = FAMILY.search(block)
        name = family.group(1).strip().strip('"') if family else "?"
        faces[hashlib.sha256(block.encode()).hexdigest()[:12]] = name
    return faces


def compare_faces(site: Path, pages: Sequence[str]) -> list[dict[str, Any]]:
    """Per page and family: blocks shared with the explainer, and blocks it lacks or adds."""
    explainer = render_overview.paper_path(render_overview.N11_LOWER_BOUNDS_EXPLAINER)
    reference = font_faces(site, explainer)
    rows: list[dict[str, Any]] = []
    for name in pages:
        faces = font_faces(site, name.split("#")[0])
        families = sorted(set(faces.values()) | set(reference.values()))
        for family in families:
            mine = {digest for digest, value in faces.items() if value == family}
            theirs = {digest for digest, value in reference.items() if value == family}
            rows.append(
                {
                    "page": name,
                    "family": family,
                    "shared": len(mine & theirs),
                    "only_here": len(mine - theirs),
                    "only_explainer": len(theirs - mine),
                }
            )
    return rows


def type_rows(report: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """A `type` report flattened to one row per page, width and role."""
    return [
        {"page": row["page"], "width": row["width"], "role": role, **values}
        for row in report
        for role, values in row["roles"].items()
        if values is not None
    ]


def token_rows(
    report: list[dict[str, Any]], *, scope: str = "root_tokens"
) -> list[dict[str, Any]]:
    """Every `--kpress-*` token whose value differs between pages at one width, by page.

    The first page of each width is the reference, which is the explainer by default. A
    token a page does not resolve at all is shown as `-`.
    """
    rows: list[dict[str, Any]] = []
    for width in dict.fromkeys(row["width"] for row in report):
        at = [row for row in report if row["width"] == width]
        names = sorted(
            {name for row in at for name in row[scope] if name.startswith("--kpress-")}
        )
        for name in names:
            values = [" ".join(row[scope].get(name, "-").split()) for row in at]
            if len(set(values)) > 1:
                rows.append(
                    {
                        "width": width,
                        "token": name,
                        **{row["page"]: value for row, value in zip(at, values, strict=True)},
                    }
                )
    return rows


def card_rows(report: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """A `cards` report flattened to one row per page, width, section and row of cards."""
    return [
        {
            "page": entry["page"],
            "width": entry["width"],
            "section": entry["section"],
            "block": entry["block_width"],
            "row": index + 1,
            "cards": row["cards"],
            "sizes": " ".join(size or "-" for size in row["sizes"]),
            "widths": " ".join(f"{width:g}" for width in row["widths"]),
            "start": row["start"],
            "end": row["end"],
        }
        for entry in report
        for index, row in enumerate(entry["rows"])
    ]


def markdown_table(report: list[dict[str, Any]]) -> str:
    """A report's flat columns as a Markdown table, for a design note or a pull request."""
    if not report:
        return "(no rows)"
    if "faces" in report[0] and "math" in report[0]:
        report = glyph_rows(report)
    if report and "roles" in report[0]:
        report = type_rows(report)
    if report and "rows" in report[0]:
        report = card_rows(report)
    if report and "rungs" in report[0]:
        report = ladder_rows(report)
    if report and "kind" in report[0]:
        report = space_rows(report)
    if report and "columns" in report[0] and "layout" in report[0]:
        report = column_rows(report)
    if report and "block_size" in report[0] and "surface" in report[0]:
        report = chip_rows(report)
    columns = [key for key, value in report[0].items() if not isinstance(value, (dict, list))]
    lines = ["| " + " | ".join(columns) + " |", "|" + " --- |" * len(columns)]
    lines.extend("| " + " | ".join(str(row[key]) for key in columns) + " |" for row in report)
    return "\n".join(lines)


#: The measurements, as `mode` names them.
MODES = (
    "load",
    "type",
    "faces",
    "cards",
    "ladders",
    "math",
    "space",
    "columns",
    "chips",
    "header",
    "baselines",
    "popover",
    "glyphs",
    "figures",
    "credits",
)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("mode", choices=MODES)
    parser.add_argument(
        "site",
        help="the built site's directory; or, for every mode but `faces`, the address a "
        "site is served at, to measure the published pages as they are",
    )
    parser.add_argument(
        "--page", action="append", help="a page, with any #fragment; repeatable"
    )
    parser.add_argument("--width", type=int, action="append", help="viewport width; repeatable")
    parser.add_argument(
        "--height",
        type=int,
        action="append",
        help="with `popover`: viewport height, 900 by default; repeatable",
    )
    parser.add_argument("--runs", type=int, default=3)
    parser.add_argument(
        "--network",
        choices=sorted(NETWORKS),
        help="with `load`: throttle each load to this network (`NETWORKS`)",
    )
    parser.add_argument(
        "--after",
        metavar="PAGE",
        help="with `load`: open this page first in the same browser, so each page is "
        "measured as a reader's second page, with the first one's files cached",
    )
    parser.add_argument(
        "--scroll-check",
        action="store_true",
        help="with columns: retain geometry before, during and after "
        "vertical and horizontal scrolling",
    )
    parser.add_argument("--port", type=int, default=18961)
    parser.add_argument("--json", type=Path, help="read a saved report rather than measuring")
    parser.add_argument("--markdown", action="store_true", help="print a table, not JSON")
    parser.add_argument(
        "--media",
        choices=("screen", "print"),
        default="screen",
        help="with `cards` and `figures`: the CSS media to lay the page out in",
    )
    parser.add_argument(
        "--press",
        action="append",
        default=[],
        metavar="SELECTOR",
        help="with `math`: press the first element this CSS selector matches, where a page "
        "has one, before counting; with `space` and `chips`: press it once the page is "
        "measured and report what it opened; with `popover`: press it and measure the "
        "popover it opens; repeatable",
    )
    parser.add_argument(
        "--shots",
        type=Path,
        metavar="DIR",
        help="with `ladders`: also shoot each diagram here at each width, light and dark; "
        "with `columns`: also shoot each table here at each width; "
        "with `glyphs`: also shoot each formula sampled here, at twice its size; "
        "with `figures`: also shoot each figure here, with its caption; "
        "with `credits`: also shoot each page's front here at each width, light and dark; "
        "with `popover`: also shoot the window here with each popover open",
    )
    parser.add_argument(
        "--tokens",
        choices=("root_tokens", "column_tokens"),
        help="with `type`: list only the `--kpress-*` tokens that differ between pages",
    )
    parser.add_argument(
        "--scheme",
        action="append",
        choices=("light", "dark"),
        help="with `glyphs`: the colour scheme to lay the page out in, light by default; "
        "repeatable",
    )
    parser.add_argument(
        "--tex",
        action="append",
        default=[],
        metavar="SOURCE",
        help="with `glyphs`: report every formula whose TeX is exactly this as a row of its "
        "own, so one formula can be compared between pages; repeatable",
    )
    parser.add_argument(
        "--style",
        metavar="CSS",
        help="with `glyphs`: a stylesheet added to each page before it is measured, to see "
        "what one declaration changes",
    )
    parser.add_argument(
        "--tex-ink-only",
        action="store_true",
        help="with `glyphs`: shoot only the formulas `--tex` names for their ink, which "
        "is most of what a long page costs to measure",
    )
    parser.add_argument(
        "--platform",
        metavar="NAME",
        help="with `glyphs`: what each page is told `navigator.platform` is (`MacIntel`, "
        "`Linux x86_64`), to see the choice it makes by platform on this machine",
    )
    parser.add_argument(
        "--view",
        choices=("formulas", "differences", "summary", "problems"),
        help="with `glyphs`: print the formulas sampled, one a row; every property a page "
        "sets differently from the first page; each role's distinct settings across the "
        "pages; or where a page departs from what the shared layers set, which fails "
        "the run when there is any",
    )
    args = parser.parse_args(argv)
    served = args.site.startswith(("http://", "https://"))
    site = Path(args.site).resolve()
    pages = tuple(args.page or (PAPER_PAGES if args.mode in PAPER_MODES else DEFAULT_PAGES))
    widths = tuple(args.width or (1280,))
    if args.json is not None:
        report: list[dict[str, Any]] = json.loads(args.json.read_text(encoding="utf-8"))
    elif args.mode == "faces":
        if served:
            parser.error("`faces` reads the built files: give the site's directory")
        report = compare_faces(site, pages)
    else:
        server = None if served else serve(site, args.port, as_pages=args.mode == "load")
        base = args.site.rstrip("/") if served else f"http://127.0.0.1:{args.port}"
        try:
            if args.mode == "type":
                report = measure_type(base, pages, widths=widths)
            elif args.mode == "cards":
                report = measure_cards(base, pages, widths=widths, media=args.media)
            elif args.mode == "ladders":
                report = measure_ladders(base, pages, widths=widths, shots=args.shots)
            elif args.mode == "math":
                report = measure_math(base, pages, widths=widths, presses=args.press)
            elif args.mode == "space":
                report = measure_space(base, pages, widths=widths, presses=args.press)
            elif args.mode == "columns":
                report = measure_columns(
                    base, pages, widths=widths, shots=args.shots, scroll_check=args.scroll_check
                )
            elif args.mode == "chips":
                report = measure_chips(base, pages, widths=widths, presses=args.press)
            elif args.mode == "credits":
                report = measure_credits(base, pages, widths=widths, shots=args.shots)
            elif args.mode == "header":
                report = measure_header(base, pages, widths=widths)
            elif args.mode == "baselines":
                report = measure_baselines(base, pages, widths=widths)
            elif args.mode == "glyphs":
                report = measure_glyphs(
                    base,
                    pages,
                    widths=widths,
                    schemes=tuple(args.scheme or ("light",)),
                    tex=args.tex,
                    style=args.style,
                    platform=args.platform,
                    shots=args.shots,
                    every_ink=not args.tex_ink_only,
                )
            elif args.mode == "figures":
                report = measure_figures(
                    base, pages, widths=widths, media=args.media, shots=args.shots
                )
                for row in report:
                    row["problems"] = "; ".join(figure_problems(row))
            elif args.mode == "popover":
                report = measure_popovers(
                    base,
                    pages,
                    widths=widths,
                    heights=tuple(args.height or (900,)),
                    presses=args.press,
                    shots=args.shots,
                )
            else:
                report = measure_load(
                    base,
                    pages,
                    widths=widths,
                    runs=args.runs,
                    network=args.network,
                    after=args.after,
                )
        finally:
            if server is not None:
                server.shutdown()
                server.server_close()
    if args.tokens:
        report = token_rows(report, scope=args.tokens)
    if args.view:
        views = {
            "formulas": glyph_rows,
            "differences": glyph_differences,
            "summary": glyph_summary,
            "problems": problem_rows,
        }
        report = views[args.view](report)
    if args.markdown:
        print(markdown_table(report))
    else:
        json.dump(report, sys.stdout, indent=2)
        print()
    return 1 if args.view == "problems" and report else 0


if __name__ == "__main__":
    raise SystemExit(main())
