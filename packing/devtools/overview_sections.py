"""The overview page's generated blocks, as HTML, from `devtools.overview_data`.

The page's prose lives in `templates/overview-article.md`; every block that states a
fact is built here and substituted into it, so a bound or a count never appears in the
template as a literal. Values are set as `$…$` inline math for KaTeX, and every table
works without scripts: rows are all present, a row's detail opens in its popover from
the native trigger in the row (`row_detail`), and `overview/table.js` adds sorting and
filters on top while `overview/row-popover.js` makes the whole row the control.
"""

from __future__ import annotations

import base64
import html
import itertools
import math
import re
import textwrap
from collections.abc import Iterable, Sequence
from datetime import date, timedelta
from functools import cache
from html.parser import HTMLParser
from pathlib import Path
from typing import Literal, NamedTuple, get_args
from urllib.parse import urlsplit

from devtools import repo_links
from devtools.check_results import KINDS, kind_label
from devtools.overview_data import (
    APOSTROPHE,
    EN_DASH,
    FRONTIER,
    REPO,
    Overview,
    Result,
    compress,
    prose_html,
    tex_bounds,
)
from devtools.render_overview import (
    DOCUMENT_PAGES,
    N11_LOWER_BOUNDS_EXPLAINER,
    N11_OPTIMALITY_REVIEW,
    RESULTS_PAGE,
    SITE_PAGES,
    paper_path,
)
from devtools.render_recent_results import SUPERSEDED, superseded
from devtools.repo_links import branch_file
from devtools.result_status import CONFIRMED, STATUSES
from sqpack.yamlio import safe_load


def _esc(text: object) -> str:
    return html.escape(str(text), quote=True)


def _fill(rung: str) -> str:
    """The attributes `site.css` colours a rung by: its scale, `V`, `C` or `S`, and its
    level, which darkens the fill. Badges, bar segments and legend swatches share them."""
    return f'data-rung="{_esc(rung[0])}" data-level="{_esc(rung[1:])}"'


def _rung(label: str) -> str:
    """A rung chip as a table prints it. The rung's full meaning is the title of the
    diagram's chip (`_ladder_cell`), where the rubric is explained once."""
    return f'<span class="site-chip site-rung-fill" {_fill(label)}>{_esc(label)}</span>'


def standing_key(standing: str) -> str:
    """A standing as a row attribute and a filter value: `current best, reported`
    is `current-best-reported`. A result that has no standing, one that claims no
    bound, has the empty key."""
    return re.sub(r"[^a-z]+", "-", standing).strip("-")


def is_superseded(result: Result) -> bool:
    """Whether a result is no longer the best: it is a bound, and no case bound rests on
    it now (`render_recent_results.superseded`). The standing is derived from the case
    records, and `devtools.check_standing` holds it to the numbers. A result that still
    holds a bound, a second proof of a value another result holds, and a result that is
    no bound are all current. A row says so as `data-current`, which the bar's "Hide
    superseded" reads (`result_filters`), and draws the `superseded` chip
    (`status_marks`)."""
    return superseded(result.record, result.standing)


def standing_chip(standing: str) -> str:
    """A result's standing as a chip, the plain gray one. A table draws one, `superseded`
    (`status_marks`); it is the kind's and the status's own chip and differs from them
    only in its word."""
    return (
        f'<span class="site-chip" data-standing="{_esc(standing_key(standing))}">'
        f"{_esc(standing)}</span>"
    )


def kind_chip(result: Result) -> str:
    """What a result is, as a chip: its `kind` in the rubric's words, `lower bound` or
    `case exclusion` (epistemics.md, Result Kinds). The plain gray chip, the standing
    chips' own, and every result has one."""
    kind = str(result.record["kind"])
    return f'<span class="site-chip" data-kind="{_esc(kind)}">{_esc(kind_label(kind))}</span>'


def status_chip(status: str) -> str:
    """A result's status as its chip: `recorded`, `reviewed`, `confirmed` or
    `incomplete` (`devtools.result_status`), the one word for how far this project's
    workflow has taken the result. The plain gray chip, like the kind's."""
    return f'<span class="site-chip" data-status="{_esc(status)}">{_esc(status)}</span>'


def case_status_chip(status: str) -> str:
    """A case's status as its chip, `proved` or `open`, the one chip for it on every page
    that draws it, the frontier table, a case record and a result's list of cases: its
    fill is the status's own, green for `proved` and yellow for `open` (`site.css`,
    `think-c19o`)."""
    return f'<span class="site-chip" data-case-status="{_esc(status)}">{_esc(status)}</span>'


def activity_chip(result: Result) -> str:
    """Who has the next move on a result, where the register records it: `in analysis`
    for work under way here, `waiting on source` for a request with another party
    (`Result.activity`). Its title is what the register says is in hand and since when.
    Nothing where the register records none."""
    activity = result.record.get("activity")
    if not activity:
        return ""
    title = f"{' '.join(str(activity['what']).split())} Since {activity['since']}."
    return (
        f'<span class="site-chip" data-activity="{_esc(activity["state"])}" '
        f'title="{_esc(title)}">{_esc(result.activity)}</span>'
    )


def result_url(result_id: str) -> str:
    """A result's row in the results table, on its own page."""
    return f"{RESULTS_PAGE}#{result_id.lower()}"


def card_kind(href: str) -> str:
    """Where a card's popover leads, which its icons show: a row on this page, another
    site, or another page of this one."""
    if href.startswith("#"):
        return "scroll"
    if href.startswith("https://"):
        return "external"
    return "page"


def is_site_page(href: str) -> bool:
    """Whether `href` is a full page this site serves, the one rule for which cards
    navigate in the same tab (`link_card`, `new_tab=False`): an entry of
    `render_overview.SITE_PAGES`, the papers under `papers/` among them
    (`papers/n11-optimality-review.html`), or a directory the site serves by
    its `index.html`, as `workbench/` is. A query or fragment on it does not matter. A
    file beside the page, such as a poster's PDF, an address off the site and a place
    on this page are not pages."""
    page = href.partition("#")[0].partition("?")[0]
    return page in SITE_PAGES or (page.endswith("/") and f"{page}index.html" in SITE_PAGES)


def embed_url(href: str) -> str:
    """A site page's address framed in a popover: `view=embed`, which its `embed.js`
    reads to drop the site chrome, added before any fragment."""
    base, hash_mark, fragment = href.partition("#")
    joined = f"{base}{'&' if '?' in base else '?'}view=embed"
    return joined + hash_mark + fragment


def card_hero(src: str) -> str:
    """A card's optional hero: a small picture at its head, in a fixed 16:9 box the
    picture covers from its top edge. It is decorative (`alt=""`), since the card's own
    label and value say what it shows, and loads lazily. `src` is a file served beside
    the page, never an address off the site."""
    if "://" in src or src.startswith("//"):
        raise SystemExit(f"{src}: a card's hero is served beside the page, never fetched")
    return (
        '<span class="site-card-hero">'
        f'<img src="{_esc(src)}" alt="" loading="lazy" decoding="async"></span>'
    )


#: A card's size, narrowest first. A card says which it is in `data-card-size`, and
#: `site.css` gives each its width: a column of the grid of that size's minimum column
#: the card section's frame fits (`paper-design.md`, Cards).
CardSize = Literal["small", "medium", "large"]
CARD_SIZES: tuple[CardSize, ...] = get_args(CardSize)

#: The default size's two thresholds, in characters of a card's own text, its headline
#: and its note together: fewer than the first is a small card, the second or more a
#: large one, and anything between a medium one.
CARD_SMALL_BELOW = 80
CARD_LARGE_FROM = 160

#: Each card section's size, declared here so its cards are one width and its lines one
#: grid, in the order the sections stand on the page. Each is the size its typical
#: card's text asks for by `card_size` (a test holds the two together): the documents'
#: one-line notes are small; the rest carry a sentence and are medium.
SECTION_CARD_SIZES: dict[str, CardSize] = {
    "pages": "medium",
    "atlas": "medium",
    "projects": "medium",
    "documents": "small",
}

#: A section set in lines of its own, as counts of its cards in order, where one
#: wrapping row would not set them as they are meant to read: the five page cards stand
#: one, two and two, the Frontier page alone at the top, then the two papers, then the
#: tutorial and the workbench (the owner, 2026-10-02, `think-ns3d`; they stood two over
#: three from `think-ec5k` the same day, the Frontier page's card last). Each line is a
#: row of its own, and none sets more cards to a line than the longest line holds, so the
#: lines share one column width, half the frame's. The stylesheet holds each longest line
#: here to a rule.
SECTION_CARD_LINES: dict[str, tuple[int, ...]] = {"pages": (1, 2, 2)}


#: Elements with no end tag, which open nothing a parser must later close.
_VOID_TAGS = frozenset({"br", "hr", "img", "input", "wbr"})


class _ReadingText(HTMLParser):
    """An HTML fragment's text as a reader sees it: a formula is its MathML's text, not
    also the TeX kpress carries beside it for KaTeX to set. `outside` is the text that
    is in no formula, and `formulas` counts them."""

    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self.outside: list[str] = []
        self.formulas = 0
        self._skipping = 0
        self._in_math = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in _VOID_TAGS:
            return
        classes = (dict(attrs).get("class") or "").split()
        if self._in_math:
            self._in_math += 1
        elif "kpress-math" in classes:
            self._in_math = 1
            self.formulas += 1
        if self._skipping:
            self._skipping += 1
        elif "kpress-math-render" in classes:
            self._skipping = 1

    def handle_endtag(self, tag: str) -> None:
        if tag in _VOID_TAGS:
            return
        if self._skipping:
            self._skipping -= 1
        if self._in_math:
            self._in_math -= 1

    def handle_data(self, data: str) -> None:
        if not self._skipping:
            self.parts.append(data)
        if not self._in_math:
            self.outside.append(data)


def _read(fragment: str) -> _ReadingText:
    reader = _ReadingText()
    reader.feed(fragment)
    reader.close()
    return reader


def reading_text(fragment: str) -> str:
    """`fragment`'s text as it reads, with runs of white space as one space."""
    return " ".join("".join(_read(fragment).parts).split())


def formulas(fragment: str) -> int:
    """How many formulas `fragment` holds."""
    return _read(fragment).formulas


def words(fragment: str) -> str:
    """`fragment`'s text that is in no formula, with runs of white space as one space."""
    return " ".join("".join(_read(fragment).outside).split())


def is_all_math(fragment: str) -> bool:
    """Whether `fragment` is mathematics standing alone: at least one formula, and no
    word, digit or mark outside one. `$n = 11$` is; "Earlier $n = 11$ lower bounds" is
    not."""
    return formulas(fragment) > 0 and not words(fragment)


#: The mark that sets a block's mathematics in the serif face whatever the words around
#: it are set in; the host adapter's sans test (`host_math_init.js`) honours it.
SERIF_MATH = 'data-math-face="serif"'


def headline_math_face(headline: str) -> str:
    """The attribute, with its leading space, for a headline's element: `SERIF_MATH`
    when the headline is mathematics standing alone, such as `$n = 11$`, and nothing
    when it has words, whose math then follows them into the sans face."""
    return f" {SERIF_MATH}" if is_all_math(headline) else ""


def size_for_length(length: float) -> CardSize:
    """The size a card whose text runs to `length` characters takes by default: under
    `CARD_SMALL_BELOW` is small, `CARD_LARGE_FROM` or more is large, and between them
    medium."""
    if length < CARD_SMALL_BELOW:
        return "small"
    return "large" if length >= CARD_LARGE_FROM else "medium"


def card_size(*text: str) -> CardSize:
    """The size a card takes when its spec declares none, from how much text it carries:
    its headline and its note (and a direct card's address), as HTML, counted as they
    read (`reading_text`) and sized by `size_for_length`."""
    return size_for_length(sum(len(reading_text(part)) for part in text))


def _size_attribute(size: CardSize | None, *text: str) -> str:
    """A card's `data-card-size`: the size its spec declares, or `card_size`'s default."""
    chosen = size or card_size(*text)
    if chosen not in CARD_SIZES:
        raise SystemExit(f"{chosen!r} is not a card size: {', '.join(CARD_SIZES)}")
    return f'data-card-size="{chosen}"'


def card(
    target: str,
    label: str,
    value: str,
    note: str,
    *,
    href: str,
    action: str,
    preview: str = "",
    also: tuple[str, str] | None = None,
    hero: str = "",
    size: CardSize | None = None,
) -> str:
    """A card and the popover it opens. The card is a caps label, the summary and a line
    under it; pressing it opens a popover that repeats the label and summary, shows
    where the card leads, and ends in a button that goes there.

    What the popover shows depends on the target. Another page of the site, a document
    among them, is rendered in the popover itself: framed narrow, without its site
    chrome, and the button expands it to the full page. A place on this page is
    previewed from `preview`, and the button scrolls there; so is a row on another page,
    such as a result's in the results table, and the button goes to that page. `also`
    adds a second, quiet link, such as the document on GitHub. `hero` heads the card
    with a picture (`card_hero`). `size` is the card's width, small, medium or large;
    left out, `card_size` chooses it from the length of the value and note.

    The popover is native (`popover`), so it opens, closes on Escape or a click outside,
    and follows its button with no script. It is set in sans, so its math is sans too,
    with one exception the card shares: a headline that is mathematics standing alone
    (`headline_math_face`) is set in the serif. The label and action are escaped here;
    the value, note and preview are HTML, so they may carry math.
    """
    face = headline_math_face(value)
    kind = card_kind(href)
    if kind == "page" and not preview:
        body = (
            f'<iframe class="site-popover-frame" src="{_esc(embed_url(href))}" '
            f'loading="lazy" title="{_esc(label)}"></iframe>'
        )
    else:
        body = f'<div class="site-popover-preview">{preview}</div>'
    second = (
        f' <a class="site-popover-also" href="{_esc(also[0])}">{_esc(also[1])}</a>'
        if also
        else ""
    )
    return (
        f'<button type="button" class="site-card" popovertarget="{_esc(target)}" '
        f'data-go="{kind}" {_size_attribute(size, value, note)}>'
        f"{card_hero(hero) if hero else ''}"
        f'<span class="site-card-label">{_esc(label)}</span>'
        f'<span class="site-card-value"{face}>{value}</span>'
        f'<span class="site-card-note">{note}</span></button>'
        f'<div class="site-popover" id="{_esc(target)}" popover '
        f'data-go="{kind}">'
        f'<button type="button" class="site-popover-close" popovertarget="{_esc(target)}" '
        'popovertargetaction="hide" aria-label="Close">\u00d7</button>'
        f'<span class="site-card-label">{_esc(label)}</span>'
        f'<p class="site-popover-value"{face}>{value}</p>{body}'
        f'<p class="site-popover-actions"><a class="site-popover-action" href="{_esc(href)}" '
        f'data-go="{kind}">{_esc(action)}</a>{second}</p>'
        "</div>"
    )


def _cards(cards: list[str], section: str = "") -> str:
    """A card section's frame and its cards: one wrapping row, or for a section of
    `SECTION_CARD_LINES` a row per line, each no wider than its longest line."""
    lines = SECTION_CARD_LINES.get(section, (len(cards),))
    if sum(lines) != len(cards):
        raise SystemExit(f"{section}: {len(cards)} cards in lines of {lines}")
    most = f' data-cards-most="{max(lines)}"' if section in SECTION_CARD_LINES else ""
    rows = "".join(
        f'<div class="site-cards"{most}>{"".join(cards[end - count : end])}</div>'
        for count, end in zip(lines, itertools.accumulate(lines), strict=True)
    )
    return f'<div class="site-cards-frame site-wide">{rows}</div>'


# ---------- Row popovers: the one way a table row shows its detail ----------


class RowDetail(NamedTuple):
    """The three pieces that make a table row the unit (paper-design.md, Row popovers).

    The caller writes `attributes` into the row's `<tr>`, `trigger` into one of its
    cells, and `popover` after the table, outside every cell, so no cell expands and the
    panel takes no style from the table. The row finds its popover by id, so sorting and
    filtering, which move and hide rows, never part a row from its popover.
    """

    attributes: str
    """For the `<tr>`: `data-row-popover`, the id of the row's popover, and `aria-label`,
    the row's accessible name. It carries no `tabindex`: `overview/row-popover.js` makes
    the row focusable, so a row is never a stop that does nothing."""
    trigger: str
    """The row's one native trigger, a `<button popovertarget>` around the row's own key:
    without scripts it is what opens the popover; with them the whole row does, and the
    button leaves the tab order so each row is one stop."""
    popover: str
    """The panel: a card's popover in every way (`.site-popover`: the close cross, the caps
    label, the headline, Escape and a click outside), with the row's body and an optional
    action at its foot."""


def row_detail(
    target: str,
    *,
    name: str,
    trigger: str,
    label: str,
    title: str,
    body: str,
    action: tuple[str, str] | None = None,
    deferred: bool = False,
    fallback: str = "",
    source: str = "",
) -> RowDetail:
    """A table row's popover and the markup that ties its row to it.

    `target` is the popover's id, unique on the page; `name` the row's accessible name,
    plain text; `trigger` the HTML the native trigger wraps, the row's own key such as its
    id. The popover repeats `label` as its caps label and `title` as its headline, set as
    every headline is (`headline_math_face`: serif when it is mathematics standing alone,
    sans with its words otherwise), then `body`, the row's detail, and, when
    `action` is `(href, words)`, the one button that goes there. `name`, `label` and the
    action's words are escaped here; `trigger`, `title` and `body` are HTML.

    A `deferred` body is held in a `<template>`, which the browser parses but neither
    lays out nor typesets, and `overview/row-popover.js` places it the first time the
    popover opens: for a body too heavy to render once per row at load. It costs the
    same bytes. Without scripts a template stays inert, so `fallback`, HTML in a
    `<noscript>` beside it, is what such a reader's popover shows.

    `source` is for a body too heavy to carry in the page at all: the address, beside
    the page, of a fuller body that the script fetches when the popover is first opened
    and puts in place of `body`, which is then the short form the page itself holds and
    what a reader without scripts, or off the network, keeps. The page gains only the
    address.
    """
    if deferred and source:
        raise SystemExit(f"{target}: a row body waits in a template or is fetched, not both")
    if deferred:
        body = f"<template data-row-pop-body>{body}</template>" + (
            f"<noscript>{fallback}</noscript>" if fallback else ""
        )
    fetched = f' data-row-pop-src="{_esc(source)}"' if source else ""
    target = _esc(target)
    attributes = f'data-row-popover="{target}" aria-label="{_esc(name)}"'
    button = (
        f'<button type="button" class="site-row-open" popovertarget="{target}">'
        f"{trigger}</button>"
    )
    foot = ""
    if action:
        href, words = action
        kind = card_kind(href)
        foot = (
            f'<p class="site-popover-actions"><a class="site-popover-action" '
            f'href="{_esc(href)}" data-go="{kind}">{_esc(words)}</a></p>'
        )
    popover = (
        f'<div class="site-popover site-row-pop" id="{target}" popover role="dialog" '
        f'aria-labelledby="{target}-title">'
        f'<button type="button" class="site-popover-close" popovertarget="{target}" '
        'popovertargetaction="hide" aria-label="Close">\u00d7</button>'
        f'<span class="site-card-label">{_esc(label)}</span>'
        f'<p class="site-popover-value"{headline_math_face(title)} id="{target}-title">'
        f"{title}</p>"
        f'<div class="site-row-pop-body"{fetched}>{body}</div>{foot}</div>'
    )
    return RowDetail(attributes, button, popover)


def plain_text(register: str) -> str:
    """Register prose as an accessible name: its code marks dropped, its spaces one."""
    return " ".join(register.replace("`", "").split())


def _dl(rows: list[tuple[str, str]]) -> str:
    body = "".join(f"<dt>{label}</dt><dd>{value}</dd>" for label, value in rows)
    return f'<dl class="site-detail">{body}</dl>'


def _detail(result: Result) -> str:
    """A result's claim, composition, next rung, why it matters and novelty label: the
    short form of what its row opens to, which the page itself carries (`result_row`)."""
    record = result.record
    rows = [("Claim", prose_html(record["claim"]))]
    for key, label in (("composition", "Composition"), ("next_rung", "Next rung")):
        if record.get(key):
            rows.append((label, prose_html(record[key])))
    rows.append(("Significance", prose_html(record["significance"]["rationale"])))
    meaning = novelty_labels().get(result.novelty, "")
    rows.append(
        (
            "Novelty",
            (
                f'<span class="site-chip" data-novelty="{_esc(result.novelty)}">'
                f"{_esc(result.novelty)}</span> {_esc(meaning)}"
            ),
        )
    )
    body = "".join(f"<dt>{label}</dt><dd>{value}</dd>" for label, value in rows)
    return f'<dl class="site-detail">{body}</dl>'


def _records(result: Result) -> str:
    """A result's records, its case link, the register, its evidence, source and reviews,
    as its Details cell sets them: one link to a line on a wide screen, and on a phone a
    line under the claim, a dot drawn between two links (`site.css`)."""
    return "".join(
        f'<a href="{_esc(link.url)}"'
        + (f' title="{_esc(link.title)}"' if link.title else "")
        + f">{_esc(link.label)}</a>"
        for link in result.records
    )


def result_row_popover_body(result: Result, overview: Overview) -> str:
    """The body of a result row's popover, the one source of it for every table that
    lists results: the recent table on the overview and the results page's table. It is
    the result's whole overview (`result_overview.result_popover_html`): its case drawn,
    the chain of results on that case, and every link.

    The overviews run to 2.8 MB between them, and two pages list the results, so no page
    carries one. Each is written once, beside the pages (`result_fragment`,
    `render_overview.result_fragments`), and a row's popover fetches its own when it
    first opens (`result_row`).
    """
    # `result_overview` reads this module for the chips and the film's facts.
    from devtools import result_overview  # noqa: PLC0415

    return result_overview.result_popover_html(result, overview)


#: Where the result overviews are served, under the site's root: a directory of
#: fragments, one a result, which are not pages. Not `results/`: `results.html` is still
#: served, as the forwarder where `RESULTS.md` was a page, and a host may serve either
#: at `/results`.
RESULT_FRAGMENTS = "result"


def result_fragment(result_id: str) -> str:
    """The address of a result's overview, from a page at the site's root. Its links
    are written from the root too, so only a page there may place it."""
    return f"{RESULT_FRAGMENTS}/{result_id.lower()}.html"


#: The site's one star, the mark of a recent lower bound (paper-design.md), as an escape.
STAR = "\u2605"

#: What a starred result is called, as the film and a case's visual summary call a starred
#: case.
NEW_RESULT = "new result"


def new_result_label(result: Result, overview: Overview) -> str:
    """What a result's star says, or nothing where the result has no star: that it is a
    new result, and the cases whose verified lower bound it holds now.

    The rule is the atlas's (`overview_data.starred_results`): the result is the one a
    case's verified lower bound rests on, and that bound is recent, proved or published
    since `RECENT_SINCE`. It is the star and the "new result" of the film and of a case's
    visual summary, asked of the result instead of the case.
    """
    cases = overview.starred.get(result.id)
    if not cases:
        return ""
    return (
        f"{NEW_RESULT.capitalize()}: holds the verified lower bound for n = "
        f"{compress(list(cases))}"
    )


def new_result_star(result: Result, overview: Overview) -> str:
    """The red star straight after a new result's text in a table of results, or nothing
    (`new_result_label`). The glyph is an image whose name and tooltip are the label, so
    it is read and not only seen, and the row's own name says "new result" too
    (`result_row`). No space joins it to the text: a browser may break a line between a
    formula and a space that does not break, which left the star on a line of its own.
    `site.css` hangs it after the last character instead, with a gap, in room the cell
    keeps for it."""
    label = new_result_label(result, overview)
    if not label:
        return ""
    return (
        f'<span class="site-star" role="img" aria-label="{_esc(label)}" '
        f'title="{_esc(label)}">{STAR}</span>'
    )


def star_legend() -> str:
    """The sentence that says what the star in a table of results marks, with the star
    itself, for the prose above each table (`{{STAR_LEGEND}}` in the two articles)."""
    return (
        f'A star (<span class="site-star" aria-hidden="true">{STAR}</span>) marks a '
        f"{NEW_RESULT}, as the atlas does: the verified lower bound of a case rests on it "
        f"now, and it was proved or published on or after {_since()}."
    )


def result_row(result: Result, *, trigger: str, starred: bool = False) -> RowDetail:
    """A result's row popover, the same on both tables of results: its id as the caps
    label, its summary as the headline, then the result's short detail (`_detail`),
    which the script replaces with the whole overview, fetched from `result_fragment`
    when the popover first opens. It has no button: the row pressed is the result's
    row, in either table, and a button from one table to the same row of the other
    leads nowhere new. A `starred` row's name ends ", new result", what its star says
    (`new_result_star`)."""
    name = f"{result.id}: {plain_text(result.summary)}"
    return row_detail(
        f"pop-result-{result.id.lower()}",
        name=f"{name}, {NEW_RESULT}" if starred else name,
        trigger=trigger,
        label=result.id,
        title=tex_bounds(result.summary),
        body=_detail(result),
        source=result_fragment(result.id),
    )


# ---------- Result filters: one tools bar for every table of results ----------


class FilterDefaults(NamedTuple):
    """Where a table's bar starts, which is all that differs between the two tables of
    results: the lowest significance shown and the greatest age in days, each `None`
    for no limit, and whether "Hide superseded" starts checked. Every other control
    starts at all on both."""

    significance: int | None = None
    max_age: int | None = None
    hide_superseded: bool = False


#: The overview's Recent Results: what matters most, from the last half year, and of
#: that only what nothing has superseded.
RECENT_DEFAULTS = FilterDefaults(significance=4, max_age=180, hide_superseded=True)

#: The results page: every result, of any significance, any age and any standing.
RESULTS_DEFAULTS = FilterDefaults()

#: The rung filters, in the bar's order: the scale, which names the row's attribute
#: (`data-s`), and the select's label.
RUNG_FILTERS: tuple[tuple[str, str], ...] = (
    ("S", "Significance"),
    ("V", "Verification"),
    ("C", "Confirmation"),
)

#: What every select of the bar offers first: no filter on that facet.
ALL = "All"


def result_cases(result: Result) -> str:
    """A result's cases as its row's `data-n`, which the Case filter reads: each count,
    and a run of counts as a range, `18-21 26`."""
    return result.scope.replace(EN_DASH, "-").replace(",", "")


def result_facets(result: Result) -> str:
    """A result row's facets as attributes, the same on every table of results, each one
    a filter of `result_filters`: whose result it is, its V, C and S rungs as numbers,
    its kind, the listed projects it is attributed to, as their slugs a space apart
    (`result_projects`; empty for most rows), its status, whether it is current, which
    is to say not superseded (`is_superseded`), its cases and the date the table shows."""
    record = result.record
    return (
        f'data-source="{"ours" if result.ours else "others"}" '
        f'data-v="{_esc(record["verification"][1:])}" '
        f'data-c="{_esc(record["confirmation"][1:])}" '
        f'data-s="{significance(result)}" '
        f'data-kind="{_esc(record["kind"])}" '
        f'data-project="{_esc(" ".join(result_projects(result)))}" '
        f'data-status="{_esc(result.status)}" '
        f'data-current="{"false" if is_superseded(result) else "true"}" '
        f'data-n="{_esc(result_cases(result))}" '
        f'data-date="{_esc(first_day(result.dated[1]))}"'
    )


def reference_date(overview: Overview) -> date:
    """The day a render measures a result's age from: the newest `registered` date in
    the register. It is the register's own and never the clock's, so two renders of one
    tree are the same bytes. It decides only what the HTML starts with: on the page,
    `overview/table.js` measures every age again from the reader's own day."""
    return max(date.fromisoformat(str(r.record["registered"])) for r in overview.results)


def age_cutoff(reference: date, days: int) -> str:
    """The first day a row may be dated to be no older than `days` on `reference`, as
    `overview/table.js` reckons it (`ageCutoff`): 180 days on 2026-09-30 is 2026-04-03."""
    return (reference - timedelta(days=days)).isoformat()


def shown_by_default(result: Result, defaults: FilterDefaults, reference: date) -> bool:
    """Whether a result's row shows before the reader touches the filters, a table's
    `defaults`, with its age measured from `reference`."""
    if defaults.significance is not None and significance(result) < defaults.significance:
        return False
    if defaults.hide_superseded and is_superseded(result):
        return False
    return defaults.max_age is None or first_day(result.dated[1]) >= age_cutoff(
        reference, defaults.max_age
    )


def rung_options(scale: str) -> list[tuple[str, str]]:
    """A rung filter's choices: all, then each level above the scale's lowest as a
    floor, `S4 and up`, the top one bare. The levels are the rubric's own."""
    levels = sorted(level for level, _ in rubric_levels()[scale])
    return [
        ("", ALL),
        *(
            (str(level), f"{scale}{level}" + ("" if level == levels[-1] else " and up"))
            for level in levels[1:]
        ),
    ]


def _options(options: Iterable[tuple[str, str]], selected: str = "") -> str:
    return "".join(
        f'<option value="{_esc(value)}"{" selected" if value == selected else ""}>'
        f"{_esc(label)}</option>"
        for value, label in options
    )


def first_day(dated: str) -> str:
    """A date the register gives only to its year or its month, as the first day of it,
    so every row's `data-date` is a whole date and orders as text: `1979` is
    `1979-01-01`, and `2005-03` is `2005-03-01`."""
    missing = "-01-01"[max(len(dated) - 4, 0) :]
    return dated + missing if len(dated) < len("2026-01-01") else dated


def count_text(shown: int, total: int, noun: str = "results") -> str:
    """A tools bar's count, as `overview/table.js` writes it (`countText`)."""
    return f"{total} {noun}" if shown == total else f"{shown} of {total} {noun}"


def result_filters(
    overview: Overview, listed: Sequence[Result], defaults: FilterDefaults
) -> str:
    """The one tools bar every table of results carries: the overview's recent table and
    the results page's table. `overview/table.js` drives it.

    One control per facet a row carries (`result_facets`), and they compose: Significance,
    Verification and Confirmation as floors (`data-bound="min"`), Kind, Status and
    Source as equalities, "Hide superseded" as a flag the row must carry
    (`data-current`), Case as a number the row's cases must hold (`covers`), and Max age
    as the most days the row's date may lie behind the reader's day (`age`), empty for no
    limit.

    Kind offers the kinds the register holds, in the rubric's order. Status offers the
    workflow statuses some result has (`result_status`): recorded, reviewed, confirmed
    and incomplete. "Hide superseded" stands straight after it and is a different
    question, the result's place on the frontier: checked, it hides exactly the
    superseded rows (`is_superseded`), whatever their status.

    Two more controls are preset-only (`data-preset`): Project, which holds a row to one
    of the listed projects it is attributed to (`has`, against the row's `data-project`),
    and At significance, which holds it to one S rung exactly. Each is `hidden` in the
    HTML and starts at all. A link sets them, `all-results.html?project=…&s=4`, as the
    tallies on the other projects' cards do (`project_tally`), and the script shows a
    preset control while it filters, so the reader sees what narrows the table and can
    set it back to All.

    A table's `defaults` are where Significance, Max age and "Hide superseded" start;
    every other control starts at all. The tables write the rows outside those defaults
    `hidden` and the bar writes the count of the rows left, so the first paint is the
    filtered table. An age is measured there from `reference_date`, and by the script
    from the reader's day.
    Without scripts nothing stays filtered: `site.css` shows every row and drops the bar.

    The choices come from the whole register, never from `listed`, the rows of the table
    the bar sits over, so the bar is the same on both pages but for where it starts and
    its count.
    """
    present = {result.status for result in overview.results}
    held = {str(result.record["kind"]) for result in overview.results}
    last = f' max="{max(overview.cases)}"' if overview.cases else ""
    floor = "" if defaults.significance is None else str(defaults.significance)
    age = "" if defaults.max_age is None else f' value="{defaults.max_age}"'
    hide = " checked" if defaults.hide_superseded else ""
    reference = reference_date(overview)
    rungs = "".join(
        f'<label>{label} <select data-filter="{scale.lower()}" data-bound="min">'
        f"{_options(rung_options(scale), floor if scale == 'S' else '')}"
        "</select></label>"
        for scale, label in RUNG_FILTERS
    )
    kinds = [("", ALL), *((kind, kind_label(kind)) for kind in KINDS if kind in held)]
    statuses = [("", ALL), *((status, status) for status in STATUSES if status in present)]
    sources = [("", ALL), ("ours", "This project"), ("others", "Others")]
    projects = [("", ALL), *((project_slug(url), project_name(url)) for url in project_urls())]
    exact = [("", ALL), *((str(level), f"S{level}") for level in significance_levels())]
    shown = sum(shown_by_default(result, defaults, reference) for result in listed)
    return (
        '<div class="site-table-tools site-result-filters">'
        f"{rungs}"
        f'<label>Kind <select data-filter="kind">{_options(kinds)}</select></label>'
        f'<label>Status <select data-filter="status">{_options(statuses)}</select></label>'
        f'<label><input type="checkbox" data-filter="current"{hide}> Hide superseded</label>'
        f'<label>Source <select data-filter="source">{_options(sources)}</select></label>'
        '<label>Case <var>n</var> <input type="number" data-filter="n" data-bound="covers" '
        f'min="1"{last} placeholder="any"></label>'
        '<label>Max age <input type="number" data-filter="date" data-bound="age" '
        f'min="0" placeholder="any"{age}> days</label>'
        '<label hidden>Project <select data-filter="project" data-bound="has" data-preset>'
        f"{_options(projects)}</select></label>"
        '<label hidden>At significance <select data-filter="s" data-preset>'
        f"{_options(exact)}</select></label>"
        '<span class="site-count" data-count data-noun="results" aria-live="polite">'
        f"{count_text(shown, len(listed))}</span></div>"
    )


def result_head() -> str:
    """The header row of a table of results: the one set of columns both tables carry,
    in one order. The date; the result; the cases; the credit; the rungs, with the kind
    under them; the status; the details, the result's records a link to a line; and the
    id, which is the row's trigger. The owner set this order on 2026-10-02: the id led
    and the date closed the row until then (`think-t090`); the status stood under the
    kind, in the rungs' cell, though it is where the result stands and no rung
    (`think-ybt5`); and the records stood on a line under the summary, where the result's
    cell holds the claim alone now (`think-e4o3`). A column sorts where an order means
    something, on either page."""
    return (
        "<thead><tr>"
        '<th data-sort="text" title="Published, for a result by others; established, for '
        f'this project{APOSTROPHE}s">Date</th>'
        '<th class="site-col-result">Result</th>'
        '<th data-sort="num" class="num site-col-n">n</th>'
        '<th data-sort="text">Credit</th>'
        '<th data-sort="text" title="Significance, verification and confirmation, then '
        'what the result is">Rungs</th>'
        '<th data-sort="text" class="site-col-status" title="How far the work on it here '
        "has gone: recorded, reviewed, confirmed or incomplete; then who has the next "
        'move, and superseded where it is">Status</th>'
        '<th class="site-col-details">Details</th>'
        '<th data-sort="text" class="site-col-id">ID</th>'
        "</tr></thead>"
    )


def id_cell(result: Result, detail: RowDetail) -> str:
    """A result's id cell, the last of its row in both tables of results: the id in a
    column of its own (`.site-col-id`), as the row's native trigger, which opens the
    row's popover without scripts (`row_detail`)."""
    return f'<td class="site-col-id" data-value="{_esc(result.id)}">{detail.trigger}</td>'


#: The most characters a result's list of cases may have and stay on one line, half the
#: `--site-cases-measure` of `site.css`: a cell wraps from five values, and also when a
#: shorter list is longer than this, since on one line it would hold the column wider
#: than the floor it narrows to before the table scrolls. T-075's four values, two counts
#: and two ranges, are 20 characters, and on one line ran the table of results 26 pixels
#: past its frame at 1024 with six columns, and 47 past its floors with eight.
CASES_ONE_LINE = 12


def case_cell_class(result: Result) -> str:
    """The n cell's classes: `site-n-wraps` where its list wraps in the measure."""
    long = len(result.scope.split(", ")) >= 5 or len(result.scope) > CASES_ONE_LINE
    return "num site-col-n site-n-wraps" if long else "num site-col-n"


def case_list(result: Result) -> str:
    """A result's cases as its n cell sets them: the register's counts and ranges
    (`Result.scope`: `68, 102`, then `130` to `132` as a range with an en dash), each
    with the comma after it in a box of its own (`.site-n-value`), a space between two
    boxes. The cell reads as it did, to a reader and to a screen reader, and a line ends
    between two values and never inside one: without the box a browser ends a line after
    a range's dash. A cell of five values or more wraps in a column of its own measure,
    and a shorter one stays on one line (`site.css`, `--site-cases-measure`). The column
    sorts on the cell's `data-value`, the first case, and the Case filter reads the row's
    `data-n` (`result_cases`)."""
    *before, last = result.scope.split(", ")
    values = (*(f"{value}," for value in before), last)
    return " ".join(f'<span class="site-n-value">{_esc(value)}</span>' for value in values)


def result_text(result: Result) -> str:
    """A result's summary as its Result cell sets it, in both tables of results: the
    register's headline, its math typeset. It links nowhere: the row is the result's
    own in either table, and opens its popover."""
    return tex_bounds(result.summary)


def credit_cell(credit: str) -> str:
    """A credit as its cell sets it, whatever the register's credit line says: the
    finder first, and "after …", the work it builds on, quiet after it, in full. So a
    row says whose the result is and what it rests on without a heading over it."""
    finder, _, after = credit.partition(" after ")
    if not after:
        return _esc(finder)
    return f'{_esc(finder)} <span class="site-cell-quiet">after {_esc(after)}</span>'


def date_cell(result: Result) -> str:
    """What a result's date cell holds, in both tables of results: the date first, then
    what it dates, `published` or `established`, quiet (`.site-date-kind`). The cell
    sorts and filters on the date alone, its `data-value` and the row's `data-date`.
    A result's overview sets its date, and each date of its chain, with this too
    (`result_overview.head`, `step`), so the order has one definition."""
    kind, dated = result.dated
    return f'{_esc(dated)} <span class="site-date-kind">{_esc(kind)}</span>'


def result_cells(result: Result, overview: Overview, detail: RowDetail) -> str:
    """A result's cells, one for each column of `result_head`, the same on both tables:
    its date (`date_cell`), its summary with the star a new result earns (`result_text`,
    `new_result_star`), its cases (`case_list`), its credit (`credit_cell`), its rung
    chips with its kind on a line under them (`kind_chip`), its status line
    (`status_marks`), its records a link to a line (`_records`), and its id
    (`id_cell`). The status cell sorts on the status word alone."""
    record = result.record
    standing = f'<span class="site-standing">{status_marks(result)}</span>'
    return (
        f'<td class="site-col-date" data-value="{_esc(result.dated[1])}">'
        f"{date_cell(result)}</td>"
        f'<td class="site-col-result">{result_text(result)}'
        f"{new_result_star(result, overview)}</td>"
        f'<td class="{case_cell_class(result)}" data-value="{result.first_n}">'
        f"{case_list(result)}</td>"
        f'<td class="site-col-credit" data-value="{_esc(result.credit)}">'
        f"{credit_cell(result.credit)}</td>"
        f'<td class="site-rungs" '
        f'data-value="{_esc(record["confirmation"] + record["verification"])}">'
        f'{rung_chips(result)}<span class="site-kind">{kind_chip(result)}</span></td>'
        f'<td class="site-col-status" data-value="{_esc(result.status)}">{standing}</td>'
        '<td class="site-col-details">'
        f'<div class="site-records">{_records(result)}</div></td>'
        f"{id_cell(result, detail)}"
    )


def result_table_row(
    result: Result, overview: Overview, *, here: bool, shown: bool
) -> tuple[str, str]:
    """One result's row in a table of results, and the popover the row opens: the one
    row both tables write, the same cells and the same popover. On the results page
    (`here`) the row is the result's own address, `id="t-018"`; anywhere else it names
    the result as `data-result`, since that address is the results page's. A row that is
    not `shown`, one outside its table's defaults, is `hidden` in the HTML. Those two
    attributes are all a row differs in between the tables."""
    starred = bool(new_result_label(result, overview))
    detail = result_row(result, trigger=_esc(result.id), starred=starred)
    key = "id" if here else "data-result"
    row = (
        f'<tr {key}="{_esc(result.id.lower())}" {result_facets(result)} '
        f"{detail.attributes}{'' if shown else ' hidden'}>"
        f"{result_cells(result, overview, detail)}</tr>"
    )
    return row, detail.popover


def table_of_results(overview: Overview, defaults: FilterDefaults, *, here: bool) -> str:
    """A table of results as a page carries it: the tools bar (`result_filters`), every
    result as one flat table under `result_head`, newest first (`recent_results`),
    sortable and filterable (`overview/table.js`), and the rows' popovers after it.

    Both pages' tables are this one, and they are two filters of it. They differ in
    `defaults`, where the bar starts, with a row outside them `hidden` in the HTML, so
    the first paint is already filtered; and in `here`, which is the results page, where
    each row is the result's own address (`result_table_row`). Every row shows its
    records and opens its popover in both, and no row of one links to the other.

    No heading divides the rows. Whose a result is, and what it builds on, is read from
    its credit (`credit_cell`), and the Source filter narrows the table to this
    project's results or to others'.
    """
    results = recent_results(overview)
    reference = reference_date(overview)
    body = []
    popovers = []
    for result in results:
        row, popover = result_table_row(
            result, overview, here=here, shown=shown_by_default(result, defaults, reference)
        )
        body.append(row)
        popovers.append(popover)
    return (
        f'<div class="site-wide">{result_filters(overview, results, defaults)}'
        '<div class="site-table-wrap">'
        '<table class="kpress-table site-table site-results" data-site-table>'
        f"{result_head()}"
        f"<tbody>{''.join(body)}</tbody></table></div>{''.join(popovers)}</div>"
    )


def results_table(overview: Overview, defaults: FilterDefaults = RESULTS_DEFAULTS) -> str:
    """The results page's table: every registered result (`table_of_results`), each row
    the result's own address, under a bar that starts by hiding nothing."""
    return table_of_results(overview, defaults, here=True)


#: The rubric's three scored dimensions, in the site's order, significance first: the
#: scale, its name, the `epistemics.md` section that defines it, and the question it
#: answers, each a short plain question in the same form (the owner's wording,
#: 2026-10-01). In the axis table's terms `V` is what the result's own source certifies
#: and `C` how far that has been independently confirmed; the rungs under each head say
#: so in full.
DIMENSIONS: tuple[tuple[str, str, str, str], ...] = (
    ("S", "Significance", "significance-and-novelty", "How significant is the result?"),
    ("V", "Verification", "verification", "How was it originally verified?"),
    ("C", "Confirmation", "confirmation", "How has it been confirmed?"),
)

_LEVEL_ROW = re.compile(r"^\| `([VCS])(\d)` \| ([^|]+?) \|", re.MULTILINE)


def rubric_levels() -> dict[str, list[tuple[int, str]]]:
    """Each dimension's levels and their one-line meanings, read from the tables in
    `epistemics.md`, so the ladder diagram cannot drift from the rubric it summarizes."""
    text = (REPO / repo_links.EPISTEMICS).read_text(encoding="utf-8")
    levels: dict[str, list[tuple[int, str]]] = {}
    for scale, level, meaning in _LEVEL_ROW.findall(text):
        levels.setdefault(scale, []).append((int(level), meaning.strip()))
    for scale, *_ in DIMENSIONS:
        if not levels.get(scale):
            raise SystemExit(f"epistemics.md defines no {scale} levels")
    return levels


_NOVELTY_ROW = re.compile(r"^\| `([a-z]+(?:-[a-z]+)+)` \| ([^|]+?) \|$", re.MULTILINE)


def novelty_labels() -> dict[str, str]:
    """Each novelty label and its one-line meaning, read from the table in
    `epistemics.md` as `rubric_levels` reads the scored dimensions."""
    text = (REPO / repo_links.EPISTEMICS).read_text(encoding="utf-8")
    section = text.split("Novelty uses four labels", 1)[-1]
    labels = {label: meaning.strip() for label, meaning in _NOVELTY_ROW.findall(section)}
    for label in ("apparently-novel", "confirmed-novel", "previously-published"):
        if label not in labels:
            raise SystemExit(f"epistemics.md defines no novelty label {label}")
    return labels


#: The short form the ladder diagram prints for an `S` rung whose anchor in
#: `epistemics.md` does not fit a cell's two lines. The `V` and `C` rungs carry their
#: short form in the `Short` column of their tables in `epistemics.md`, the one place a
#: short form is written for them (`_SHORT_ROW`); a rung named in neither prints its
#: meaning whole. The chip's `title` carries the full meaning either way.
RUNG_SHORT_MEANINGS: dict[str, str] = {
    "S4": "Reusable technique, bound family, or settled value",
    "S5": "Moves a central open case, or broad adoption",
}

#: A `V` or `C` row of the rubric with its `Short` column: the label, the meaning, then
#: the short form the diagram prints.
_SHORT_ROW = re.compile(r"^\| `([VC])(\d)` \| [^|]+? \| ([^|]+?) \|", re.MULTILINE)


def rubric_short_forms() -> dict[str, str]:
    """The `Short` column of the `V` and `C` tables in `epistemics.md`, by rung label;
    every `V` and `C` rung has one, or the page does not build."""
    text = (REPO / repo_links.EPISTEMICS).read_text(encoding="utf-8")
    short = {f"{scale}{level}": form.strip() for scale, level, form in _SHORT_ROW.findall(text)}
    missing = sorted(
        label for label in rung_meanings() if label[0] in "VC" and label not in short
    )
    if missing:
        raise SystemExit(f"epistemics.md gives no Short form to {', '.join(missing)}")
    return short


#: How many characters one line of a ladder cell's description holds where the cell is
#: narrowest, 13.5rem or 216px (`--site-ladders-meaning-min` in `site.css`): the note
#: size sets a line of prose at 7.3 to 8.4px a character, so 25 characters are at most
#: 210px. A description fits its two lines when it wraps to two lines of this many
#: characters; `tests/test_site_ladders.py` measures the same in a browser, in pixels.
SHORT_MEANING_LINE = 25


@cache
def rung_meanings() -> dict[str, str]:
    """Every rung chip's label (`V3`, `C5`, `S2`) and its one-line meaning, from the
    tables in `epistemics.md`, so a chip's `title` says what the rubric says."""
    return {
        f"{scale}{level}": meaning
        for scale, levels in rubric_levels().items()
        for level, meaning in levels
    }


@cache
def rung_short_meanings() -> dict[str, str]:
    """Every rung's description in a ladder cell: its short form in `RUNG_SHORT_MEANINGS`,
    or the rubric's own meaning where that fits. One that does not fit two lines of the
    narrowest cell fails the build, since the fix is a shorter text, never a clipped one."""
    meanings = rung_meanings()
    unknown = sorted(set(RUNG_SHORT_MEANINGS) - set(meanings))
    if unknown:
        raise SystemExit(f"a short form names no rung of epistemics.md: {', '.join(unknown)}")
    written = {**rubric_short_forms(), **RUNG_SHORT_MEANINGS}
    short = {label: written.get(label, meaning) for label, meaning in meanings.items()}
    for label, text in short.items():
        if len(textwrap.wrap(text, SHORT_MEANING_LINE)) > 2:
            raise SystemExit(
                f"{label}'s description, {text!r}, does not fit two lines of "
                f"{SHORT_MEANING_LINE} characters: give it a short form in RUNG_SHORT_MEANINGS"
            )
    return short


def _ladder_cell(scale: str, level: int) -> str:
    """One rung of the ladder diagram: the chip the tables use, titled with the rubric's
    full meaning, and the two-line description."""
    label = f"{scale}{level}"
    return (
        f'<div class="site-ladders-cell" role="cell" data-ladder="{scale}">'
        '<div class="site-ladders-rung">'
        f'<span class="site-chip site-rung-fill" title="{_esc(rung_meanings()[label])}" '
        f"{_fill(label)}>{label}</span>"
        f'<span class="site-ladders-meaning">{_esc(rung_short_meanings()[label])}</span>'
        "</div></div>"
    )


def verification_block() -> str:
    """The rating ladders as one diagram: a column per dimension of the rubric,
    Significance, Verification, Confirmation, headed by its name and the question it
    answers, and a row per level, the highest at the top, so the rungs of the three
    ladders line up. A cell is the rung's chip and its description on two lines; a ladder
    with no rung at a level leaves its cell empty, as Significance does at level 0.

    It is a grid marked with table roles, not a `<table>`: kpress wraps every table on a
    page in its own scroller and restyles it as `.kpress-table`, which this diagram is
    not. Each name links to that section of `epistemics.md`.
    """
    heads = {
        scale: (
            f'<a class="site-ladders-name" href="epistemics.html#{section}">{_esc(name)}</a> '
            f'<span class="site-ladders-question">{_esc(question)}</span>'
        )
        for scale, name, section, question in DIMENSIONS
    }
    names = ", ".join(name.lower() for _, name, _, _ in DIMENSIONS)
    return _ladder_grid(heads, f"Verification ladders by level: {names}", "site-ladders-frame")


def rung_key() -> str:
    """The overview's key to the three ratings on a row of its table: the rating ladders'
    grid (`verification_block`) with each column headed by its rating and its letter
    alone, no question and no link, each rung its chip and its short meaning. It stands
    under Recent Results' account of the ratings (the owner, 2026-10-02, `think-tgjv`);
    the ladders themselves, with what each rating asks, are the Results page's."""
    heads = {
        scale: f'<span class="site-ladders-name">{_esc(name)} ({scale})</span>'
        for scale, name, _, _ in DIMENSIONS
    }
    names = ", ".join(name.lower() for _, name, _, _ in DIMENSIONS)
    return _ladder_grid(
        heads, f"The ratings' rungs by level: {names}", "site-ladders-frame site-ladders-key"
    )


def _ladder_grid(heads: dict[str, str], label: str, frame: str) -> str:
    """The ladders' grid under `heads`, each column's head by its letter: a header row,
    then a row per level, the highest at the top, each cell a rung (`_ladder_cell`) or
    empty where a ladder has no rung at that level, in a frame of class `frame` in the
    wide track."""
    levels = {scale: {level for level, _ in rungs} for scale, rungs in rubric_levels().items()}
    columns = "".join(
        f'<div class="site-ladders-head" role="columnheader" data-ladder="{scale}">'
        f"{heads[scale]}</div>"
        for scale, *_ in DIMENSIONS
    )
    rows = [
        (
            '<div class="site-ladders-row" role="row">'
            f'<span class="site-ladders-level" role="columnheader">Level</span>{columns}</div>'
        )
    ]
    every = sorted({level for scale, *_ in DIMENSIONS for level in levels[scale]}, reverse=True)
    for level in every:
        cells = "".join(
            _ladder_cell(scale, level)
            if level in levels[scale]
            else f'<div class="site-ladders-cell site-ladders-empty" role="cell" '
            f'data-ladder="{scale}"></div>'
            for scale, *_ in DIMENSIONS
        )
        rows.append(
            f'<div class="site-ladders-row" role="row" data-level="{level}">'
            f'<span class="site-ladders-level" role="rowheader">Level {level}</span>'
            f"{cells}</div>"
        )
    return (
        f'<div class="{frame} site-wide">'
        f'<div class="site-ladders" role="table" aria-label="{label}">'
        f"{''.join(rows)}</div></div>"
    )


def recent_results(overview: Overview) -> list[Result]:
    """Every result, newest first: by the date the table shows, then by id. It is the
    order of both tables of results. What makes the overview's table recent is its
    bar's defaults (`RECENT_DEFAULTS`), which a reader can change, and never a cut the
    page makes for them."""
    return sorted(overview.results, key=lambda r: (first_day(r.dated[1]), r.id), reverse=True)


def significance(result: Result) -> int:
    """A result's S rung, the level its S chip shows."""
    return int(result.record["significance"]["score"])


def result_rungs(result: Result) -> tuple[str, str, str]:
    """A result's three rungs in the order the site lists them wherever it shows them:
    significance first, then verification and confirmation (`S4`, `V4`, `C3`). The
    register's own documents keep theirs, verification first."""
    record = result.record
    return (f"S{significance(result)}", record["verification"], record["confirmation"])


def rung_chips(result: Result) -> str:
    """A result's rung chips, S, V and C, a space apart: the one place their order is
    set, for a table's row, a popover, a result's overview and a case record."""
    return " ".join(_rung(rung) for rung in result_rungs(result))


def status_marks(result: Result) -> str:
    """A result's status line: its status chip, always; who has the next move, where
    the register records it (`activity_chip`); and `superseded`, where it is a bound
    that no case bound rests on now (`is_superseded`)."""
    mark = standing_chip(SUPERSEDED) if is_superseded(result) else ""
    return " ".join(filter(None, (status_chip(result.status), activity_chip(result), mark)))


def kind_and_status(result: Result) -> str:
    """What a result is and where it stands, as chips a space apart: its kind chip, then
    its status line (`status_marks`). A popover's head and a chain's step set them on
    one line; a table's row sets each on a line of its own."""
    return f"{kind_chip(result)} {status_marks(result)}"


def status_chips(result: Result) -> str:
    """A result's rung chips, S, V and C, then its kind chip and its status line, side
    by side."""
    return f"{rung_chips(result)} {kind_and_status(result)}"


def recent_table(overview: Overview, defaults: FilterDefaults = RECENT_DEFAULTS) -> str:
    """The overview's Recent Results: the results page's table (`table_of_results`), its
    bar starting at the recent defaults. The line under it, "See all results", is the
    one link from this table to the other."""
    return table_of_results(overview, defaults, here=False)


def status_counts(overview: Overview) -> str:
    """One Markdown sentence on the results this project has not confirmed, counted from
    the register, for the results page's prose where the statuses are defined: how many
    are confirmed, and how many are recorded, reviewed or incomplete, each count the
    link to those rows of the table. A result reported and not yet replayed is a row
    like any other, and its status is a value of the table's filter."""
    held = [result.status for result in overview.results]
    confirmed = held.count(CONFIRMED)
    links = [
        f"[{held.count(status)} {status}]({RESULTS_PAGE}?status={status})"
        for status in STATUSES
        if status != CONFIRMED and status in held
    ]
    if not links:
        return f"All {len(held)} results are confirmed."
    listed = links[0] if len(links) == 1 else ", ".join(links[:-1]) + " and " + links[-1]
    return f"Of the {len(held)} results, {confirmed} are confirmed; the rest are {listed}."


def _since() -> str:
    """`RECENT_SINCE` as prose, 22 August 2026, written by the Frontier page's own
    helper so every page writes the date one way."""
    from devtools.render_frontier_page import since_prose  # noqa: PLC0415

    return since_prose()


#: The repository's reader documents, as the overview's cards show them: the file, a
#: label, and one line on what a reader finds there, in the order of
#: `render_overview.DOCUMENT_PAGES`. README and `epistemics.md` lead, as the two a reader
#: needs most: what the project is, and how each result is graded. The synopsis, the
#: full technical record, follows, then the two reference documents, for the record's
#: formats and for the code. The results register, the status table and the defect log
#: are not here: the results table and the Frontier page show the first two from the
#: same record, and the defect log is internal to the repository (think-bk2e).
DOCUMENTS: tuple[tuple[str, str, str], ...] = (
    (
        repo_links.README,
        "The Squares Project",
        "What the project is, how it works, and where to start.",
    ),
    (repo_links.EPISTEMICS, "Epistemics", "How each result is verified, confirmed and scored."),
    (
        repo_links.SYNOPSIS,
        "The synopsis",
        "The full research record: methods, claims and status.",
    ),
    (repo_links.CONVENTIONS, "Conventions", "Record formats, identifiers and naming."),
    (repo_links.DEVELOPMENT, "Development", "Building, testing and validating the code."),
)


def document_cards() -> str:
    """One card per reader document; its popover renders the document, served as a page
    of the site, and expands to it, with its latest version on GitHub beside."""
    return _cards(
        [
            card(
                f"pop-doc-{page.removesuffix('.html')}",
                path.rsplit("/", 1)[-1],
                _esc(label),
                _esc(note),
                href=page,
                action=f"Expand {path.rsplit('/', 1)[-1]}",
                also=(branch_file(path), "On GitHub"),
                size=SECTION_CARD_SIZES["documents"],
            )
            for (path, label, note), page in zip(DOCUMENTS, DOCUMENT_PAGES, strict=True)
        ]
    )


#: When the explainer's proofs are from, as its cards say it: T-018 was established on
#: 4 September 2026 and T-025 and T-026 on 9 September (`results.yaml`), first published
#: on 5 and 13 September (`sqpack.release.PUBLICATION_HISTORY`). A test holds this phrase
#: to those dates.
EXPLAINER_AS_OF = "early September"


class Paper(NamedTuple):
    """One of the site's papers, as its card says what it is: where it is served, a caps
    label naming its kind, its title, one or two sentences on what it is, and the size
    of its card on the Papers page. The title and description are register prose, so
    `n = 11` in either is set as math. The card is the link to the paper and holds no
    other, so what a description names (T-060, the optimality paper) is linked from
    the Papers page's introduction (`templates/papers-article.md`)."""

    href: str
    label: str
    title: str
    description: str
    size: CardSize = "large"


#: Where the two papers are served, under `papers/` by their slugs
#: (`render_overview.paper_path`): the optimality review, which
#: `render_n11_optimality_review` builds, and the lower-bounds explainer, which
#: `render_n11_lower_bounds_explainer` builds. Each renderer's `SITE_PATH` is the same
#: path from the same slug.
OPTIMALITY_PAPER = paper_path(N11_OPTIMALITY_REVIEW)
LOWER_BOUNDS_PAPER = paper_path(N11_LOWER_BOUNDS_EXPLAINER)

#: The site's papers, in the order the Papers page shows them, one large card each
#: (`paper_cards`). A new paper is one entry here. The optimality paper is first: it
#: explains the result that stands, T-060, where the explainer proves the lower bounds
#: T-060 superseded and the tutorial is the background to both. Its title is its
#: renderer's (`render_n11_optimality_review.TITLE`) in sentence case, and its
#: description says what T-060's rungs allow, `V3/C3`: an accepted proof, machine-checked
#: here with its review record pending. The explainer's title is the owner's
#: (2026-09-30), as `render_n11_lower_bounds_explainer.TITLE` has it in title case; the
#: tutorial's description is `TUTORIAL.md`'s own opening, its audience and what it owns.
PAPERS: tuple[Paper, ...] = (
    Paper(
        href=OPTIMALITY_PAPER,
        label="Optimality paper",
        title="A review of the optimality proof of the Trump packing of 11 squares",
        description=(
            "Explains the accepted proof that Trump\u2019s 1979 packing of eleven squares "
            "is optimal, s(11) = 3.8770835\u2026 (T-060): the exact construction, the "
            "exhaustive case exclusions, the geometric capture and the local-isolation "
            "argument, with figures drawn from or checked against the retained proof data."
        ),
    ),
    Paper(
        href=LOWER_BOUNDS_PAPER,
        label="Explainer",
        title="New lower bounds for square packing for n = 11",
        description=(
            "An explainer and proof of certain lower bounds for n = 11. It explains the "
            f"earlier, simpler proofs as of {EXPLAINER_AS_OF}; newer optimality proofs now "
            "exist (T-060)."
        ),
    ),
    Paper(
        href="tutorial.html",
        label="Tutorial",
        title="Square packing from first principles",
        description=(
            "An introduction for anyone new to the problem: what the objects are, why the "
            "approach is shaped the way it is, and what the research has and has not "
            "established. Each outside idea it uses, from linear programming to algebraic "
            "number fields, is introduced where it is first needed."
        ),
    ),
)
#: The explainer, whose card reads the same on the overview as on the Papers page.
EXPLAINER = next(paper for paper in PAPERS if paper.href == LOWER_BOUNDS_PAPER)
#: The optimality paper, whose card on the overview carries its label and its title.
OPTIMALITY = next(paper for paper in PAPERS if paper.href == OPTIMALITY_PAPER)


def paper_cards() -> str:
    """One card per paper. Each card is the link itself and goes to its paper in the same
    tab, as the overview's page cards do (`page_cards`): a paper is a full page the site
    serves, so no popover previews it (`link_card`, `new_tab=False`). A link holds no
    other link, so the Papers page's introduction links what a description names."""
    return _cards(
        [
            link_card(
                paper.href,
                paper.label,
                tex_bounds(paper.title),
                tex_bounds(paper.description),
                size=paper.size,
                new_tab=False,
            )
            for paper in PAPERS
        ]
    )


#: The site's reading and working pages, as the overview's cards under The Squares
#: Project show them: the page, a label, its title, and one line on what a reader finds
#: there. Both are register prose, so a bound in either is written in ASCII
#: (`s(11) >= 3.8264…`) and set as math. The explainer's card takes its paper's words;
#: the optimality paper's and the tutorial's keep a shorter line here. The optimality
#: paper leads the papers, as on the Papers page: it explains the result that stands. Every
#: address is a full page the site serves, the paper's a directory below the root, so
#: its card links straight to it. The Frontier page's card is first, on a line of its
#: own (`SECTION_CARD_LINES`, `think-ns3d`): it stood in The Frontier Survey section,
#: beside a card to the recent cases, until the owner dropped that section on 2026-10-02
#: and moved the card to every case up here (`think-ec5k`), last of the five at first.
#: The Results page is reached from Recent Results, whose pointer is its own.
PAGES: tuple[tuple[str, str, str, str], ...] = (
    (
        "frontier.html",
        "Frontier survey",
        "Every case from n = 1 to 324",
        "Reported and verified bounds side by side, with their sources.",
    ),
    (
        OPTIMALITY.href,
        OPTIMALITY.label,
        OPTIMALITY.title,
        (
            "Explains the accepted proof that Trump\u2019s packing of eleven squares is "
            "optimal, s(11) = 3.8770835\u2026 (T-060)."
        ),
    ),
    (EXPLAINER.href, EXPLAINER.label, EXPLAINER.title, EXPLAINER.description),
    (
        "tutorial.html",
        "Tutorial",
        "Square packing from first principles",
        "The problem, its configuration space, exact algebra and the search.",
    ),
    (
        "workbench/",
        "Workbench",
        "Pack squares by hand",
        "Move squares yourself and watch the known packings.",
    ),
)


def page_cards() -> str:
    """One card per page of `PAGES`, at the section's declared size. Each card is the
    link itself and goes to its page in the same tab: the target is a full page the site
    serves, so no popover previews it (`link_card`, `new_tab=False`)."""
    return _cards(
        [
            link_card(
                href,
                label,
                tex_bounds(title),
                tex_bounds(note),
                size=SECTION_CARD_SIZES["pages"],
                new_tab=False,
            )
            for href, label, title, note in PAGES
        ],
        "pages",
    )


#: The case drawn large under the homepage's title.
HERO_CASE = 53


def hero() -> str:
    """The homepage's picture: one known-best packing, drawn from its atlas rendering
    and linked to its row in the frontier atlas."""
    from devtools.render_frontier_page import packing_svg  # noqa: PLC0415

    n = HERO_CASE
    return (
        f'<figure class="site-hero-figure"><a href="frontier.html#n-{n}" '
        f'aria-label="The best packing known for {n} squares, in the frontier survey">'
        f"{packing_svg(n, units=1000)}</a>"
        f"<figcaption>The best packing known for {n} squares</figcaption></figure>"
    )


#: The other public square-packing projects on GitHub that the research frontier cites:
#: each repository's home, its author as the record credits them (the GitHub handle
#: where the record names no one), and what it holds. A test holds this list to cover
#: every source repository in the source-coverage register.
OTHER_PROJECTS: tuple[tuple[str, str, str], ...] = (
    (
        "https://github.com/evand/square-packing",
        "Evan Daniel",
        "Exact weighted certificates and zero-margin closed covers, closing n = 21, 32 and 45.",
    ),
    (
        "https://github.com/squarepacker/s12-lower-bound",
        "Ryu Sungjoon",
        "Evan Daniel's s(12) certificate rescaled by 7902/7901, a bound for twelve squares.",
    ),
    (
        "https://github.com/wand125/square-packing-bounds",
        "wand125",
        "Weighted point and rectangle-density lower-bound certificates across many n.",
    ),
    (
        "https://github.com/wand125/valid7-independent-check",
        "wand125",
        "A second, independent exact checker of Valid7, the finite step of s(k² \u2212 3) = k.",
    ),
    (
        "https://github.com/tokoharu/square-packing-density-bounds",
        "Tokoharu",
        "Rectangle-density lower-bound certificates.",
    ),
    (
        "https://github.com/franciscouzo/square-packing",
        "Francisco Couzo",
        "Improved packings for 49 counts from n = 68 to 307.",
    ),
    (
        "https://github.com/griffcass/square-packing",
        "Griffin Casson",
        "Improved packings for n = 103, 105 and other cases.",
    ),
    (
        "https://github.com/JoostdeWinter/square-packing-211",
        "Joost de Winter",
        "A packing of 211 squares in a square of side under 15.",
    ),
    (
        "https://github.com/Queuingtheorydotcom/11SquaresOptimal",
        "Queuingtheorydotcom",
        "A computer-assisted proof that Trump's packing of eleven squares is optimal.",
    ),
    (
        "https://github.com/Kleddamag/11-squares-certified-bound",
        "Kleddamag",
        "A certified lower bound for eleven squares.",
    ),
    (
        "https://github.com/Kleddamag/17-squares-certified-bound",
        "Kleddamag",
        "Certified lower bounds for seventeen squares.",
    ),
    (
        "https://github.com/Guzhou0806/n17-square-packing",
        "Guzhou0806",
        "Strict lower bounds for seventeen squares.",
    ),
    (
        "https://github.com/DRMacIver/square-packing-research",
        "David R. MacIver",
        "A lower bound for seventeen squares, with its paper and a Lean check.",
    ),
    (
        "https://github.com/ahyangyi/17squares",
        "ahyangyi",
        "A lower-bound proof for seventeen squares.",
    ),
    (
        "https://github.com/anabologyco-maker/square17-lower-bound",
        "anabologyco-maker",
        "A weighted fractional lower bound for seventeen squares.",
    ),
    (
        "https://github.com/BalthasarStrauss/Squares-packing_S-29-_New-Record",
        "Thomas Schadt",
        "A record packing of 29 squares.",
    ),
)


#: Favicons for other projects hosted off GitHub, saved here by host name
#: (`example.org.png`, `.svg` or `.ico`) and inlined, so the page fetches nothing.
PROJECT_FAVICONS = Path(__file__).resolve().parent / "overview" / "favicons"

#: GitHub's mark (Octicons `mark-github`, 16 units), drawn in the text colour.
GITHUB_MARK = (
    '<svg class="site-link-icon" viewBox="0 0 16 16" aria-hidden="true" focusable="false">'
    '<path fill="currentColor" d="M8 0c4.42 0 8 3.58 8 8a8.013 8.013 0 0 1-5.45 7.59c-.4.08'
    "-.55-.17-.55-.38 0-.27.01-1.13.01-2.2 0-.75-.25-1.23-.54-1.48 1.78-.2 3.65-.88 3.65-3.95 "
    "0-.88-.31-1.59-.82-2.15.08-.2.36-1.02-.08-2.12 0 0-.67-.22-2.2.82-.64-.18-1.32-.27-2-.27"
    "-.68 0-1.36.09-2 .27-1.53-1.03-2.2-.82-2.2-.82-.44 1.1-.16 1.92-.08 2.12-.51.56-.82 1.28"
    "-.82 2.15 0 3.06 1.86 3.75 3.64 3.95-.23.2-.44.55-.51 1.07-.46.21-1.61.55-2.33-.66-.15"
    "-.24-.6-.83-1.23-.82-.67.01-.27.38.01.53.34.19.73.9.82 1.13.16.45.68 1.31 2.69.94 0 .67"
    '.01 1.3.01 1.49 0 .21-.15.45-.55.38A7.995 7.995 0 0 1 0 8c0-4.42 3.58-8 8-8Z"/></svg>'
)

_FAVICON_TYPES = {".png": "image/png", ".svg": "image/svg+xml", ".ico": "image/x-icon"}


def link_icon(url: str) -> str:
    """The mark beside a project's address: GitHub's for a GitHub URL, otherwise the
    site's own favicon from `PROJECT_FAVICONS`, which a build without one refuses."""
    host = (urlsplit(url).hostname or "").removeprefix("www.")
    if host == "github.com":
        return GITHUB_MARK
    for suffix, mime in _FAVICON_TYPES.items():
        path = PROJECT_FAVICONS / f"{host}{suffix}"
        if path.is_file():
            data = base64.b64encode(path.read_bytes()).decode("ascii")
            return (
                f'<img class="site-link-icon" src="data:{mime};base64,{data}" alt="" '
                'width="16" height="16">'
            )
    raise SystemExit(
        f"{url}: save {host}'s favicon as {PROJECT_FAVICONS.name}/{host}.png (or .svg, .ico)"
    )


def _breakable(address: str) -> str:
    """An address that may wrap after each slash rather than inside a name."""
    return "/<wbr>".join(_esc(part) for part in address.split("/"))


def link_card(
    url: str,
    label: str,
    value: str,
    note: str,
    *,
    hero: str = "",
    size: CardSize | None = None,
    new_tab: bool = True,
    foot: str = "",
) -> str:
    """A card that is itself the link, with no popover: for a place whose address, or
    whose picture, is the whole of what a preview would say, and for a full page of this
    site, which needs no preview. It carries the label, the value and note, and `hero`
    heads it with a picture (`card_hero`). `size` is its width, as `card` takes it; left
    out, `card_size` chooses it from the value, the note and the address shown.

    A direct card opens its target in a new tab unless `new_tab` is false, so the page
    the reader chose it from stays where they left it: a poster's PDF, the film, a place
    off the site. A card for one of the site's own pages passes `new_tab=False` and
    navigates in the same tab, as the navigation bar does, and only a page the site
    serves may (`is_site_page`). Its corner icon is `data-go`'s (`card_kind`): the right
    arrow for a page or file of this site, the external arrow for a place off it. An
    address off the site is shown under the note beside the host's mark; a PDF is typed
    as one, so the browser opens it in place.

    `foot` is a closing line that holds links of its own, such as a project's tally of
    results. A link cannot hold a link, so a card with a foot is a box, `div.site-card`,
    holding the card's link (`site-card-main`, everything above the foot) and then the
    foot (`site-card-foot`), inside the one border. It sizes, washes and shows its
    corner icon as every card does (`site.css`).
    """
    kind = card_kind(url)
    if not new_tab and not is_site_page(url):
        raise SystemExit(f"{url}: only a page of this site opens in the same tab")
    tab = ' target="_blank" rel="noopener noreferrer"' if new_tab else ""
    typed = ' type="application/pdf"' if url.endswith(".pdf") else ""
    address = ""
    if kind == "external":
        shown = url.removeprefix("https://").rstrip("/")
        address = (
            f'<span class="site-card-url">{link_icon(url)}'
            f"<span>{_breakable(shown)}</span></span>"
        )
    body = (
        f"{card_hero(hero) if hero else ''}"
        f'<span class="site-card-label">{_esc(label)}</span>'
        f'<span class="site-card-value"{headline_math_face(value)}>{value}</span>'
        f'<span class="site-card-note">{note}</span>'
        f"{address}"
    )
    sized = _size_attribute(size, value, note, address)
    if foot:
        return (
            f'<div class="site-card site-card-footed" data-go="{kind}" {sized}>'
            f'<a class="site-card-link site-card-main" href="{_esc(url)}"{typed}{tab}>'
            f'{body}</a><p class="site-card-foot">{foot}</p></div>'
        )
    return (
        f'<a class="site-card site-card-link" href="{_esc(url)}"{typed} data-go="{kind}" '
        f"{sized}{tab}>{body}</a>"
    )


#: Where a listed project's results are attributed under a bibliography key that the
#: source-coverage register ties to no repository of its own. The September 20 packet
#: of weighted certificates is two repositories under one key, Guzhou0806's R012 and
#: Mira's measure; Guzhou0806's is listed here, so the result registered from the packet
#: counts for it.
PROJECT_EXTRA_KEYS: dict[str, tuple[str, ...]] = {
    "https://github.com/Guzhou0806/n17-square-packing": (
        "[n17 weighted certificates 2026-09-20]",
    ),
}

#: The source-coverage register: each source repository the record reviews, with the
#: bibliography key its results are attributed under.
SOURCE_COVERAGE = FRONTIER / "source-coverage.yaml"


def project_urls() -> tuple[str, ...]:
    """The listed projects' repositories, in the order `OTHER_PROJECTS` writes them,
    which is not the order the page shows them in (`project_order`)."""
    return tuple(url for url, _, _ in OTHER_PROJECTS)


def project_name(url: str) -> str:
    """A project as its owner and repository, `evand/square-packing`: the name the
    Project filter shows, since three of the repositories are called `square-packing`."""
    return urlsplit(url).path.strip("/")


def project_slug(url: str) -> str:
    """A project as the slug its results' rows carry (`data-project`) and a link names
    (`?project=`): its owner and repository in lower case, joined by a hyphen."""
    return re.sub(r"[^a-z0-9]+", "-", project_name(url).lower()).strip("-")


def source_repository(url: str) -> str:
    """A source's address as its repository's: a revision or a directory under it,
    `/tree/…`, names the same project."""
    return re.sub(r"/tree/.*", "", url).rstrip("/")


@cache
def project_source_keys() -> dict[str, frozenset[str]]:
    """Each listed project's bibliography keys: those the source-coverage register gives
    the sources at its repository, and those `PROJECT_EXTRA_KEYS` adds. A result is a
    project's where its `attribution.source_keys` names one of them."""
    coverage = safe_load(SOURCE_COVERAGE.read_text(encoding="utf-8"))["sources"]
    keys: dict[str, set[str]] = {
        url: set(PROJECT_EXTRA_KEYS.get(url, ())) for url in project_urls()
    }
    for source in coverage:
        repository = source_repository(source["url"])
        if repository in keys and source.get("source_key"):
            keys[repository].add(source["source_key"])
    return {url: frozenset(found) for url, found in keys.items()}


def result_projects(result: Result) -> tuple[str, ...]:
    """The slugs of the listed projects a result is attributed to, in the list's order.
    A result attributed to sources of several projects is each one's; this project's
    results, and a result by others whose source no listed project holds, are none's."""
    cited = set((result.record.get("attribution") or {}).get("source_keys") or ())
    return tuple(
        project_slug(url) for url, keys in project_source_keys().items() if cited & keys
    )


def significance_levels() -> tuple[int, ...]:
    """The significance rubric's levels, the highest first: 5 down to 1."""
    return tuple(sorted((level for level, _ in rubric_levels()["S"]), reverse=True))


class Cited(NamedTuple):
    """One registered result as the projects' order reads it: its id, its S rung, the
    date its row shows, and the projects it is attributed to, by any hashable name."""

    id: str
    level: int
    dated: str
    projects: tuple[str, ...]


class ProjectTally(NamedTuple):
    """The results the register cites from one project: their ids in the order given,
    how many stand at each significance level, the highest level first and every level
    present, and the date of the newest, empty where there is none."""

    results: tuple[str, ...]
    counts: tuple[tuple[int, int], ...]
    latest: str


def project_tallies(
    projects: Sequence[str], results: Iterable[Cited], levels: Sequence[int]
) -> dict[str, ProjectTally]:
    """Each project's tally over `results`. A result attributed to several projects
    counts once for each of them."""
    cited = list(results)
    tallies = {}
    for project in projects:
        own = [result for result in cited if project in result.projects]
        tallies[project] = ProjectTally(
            tuple(result.id for result in own),
            tuple((level, sum(result.level == level for result in own)) for level in levels),
            max((result.dated for result in own), default=""),
        )
    return tallies


def project_order(tallies: dict[str, ProjectTally], names: dict[str, str]) -> list[str]:
    """The projects by the significance of the results the register cites from each (the
    owner, 2026-10-01): by how many stand at the highest level, then at the next, and so
    down the scale, more first at each, compared in that order, so any project with a
    result at a level stands before every project with none at it or above. Projects
    level on every count stand by their newest result, the most recent first, and then
    by name. A project with no registered result has every count at zero and no date, so
    it comes after all the others, by name."""

    def newest_first(dated: str) -> int:
        return -date.fromisoformat(dated).toordinal() if dated else 0

    return sorted(
        tallies,
        key=lambda project: (
            tuple(-count for _, count in tallies[project].counts),
            newest_first(tallies[project].latest),
            names[project].lower(),
            project,
        ),
    )


def cited_results(overview: Overview) -> list[Cited]:
    """The register's results as `project_tallies` reads them: each with its S rung, the
    date its row shows (`Result.dated`, to the day) and the slugs of its projects."""
    return [
        Cited(
            result.id, significance(result), first_day(result.dated[1]), result_projects(result)
        )
        for result in overview.results
    ]


def repository_name(url: str) -> str:
    """A project's repository by its name alone, a card's headline."""
    return urlsplit(url).path.rstrip("/").rsplit("/", 1)[-1]


def ranked_projects(overview: Overview) -> list[tuple[str, ProjectTally]]:
    """The listed projects in the order the page shows them, each with its tally: read
    from the register when the page is rendered, never kept by hand."""
    slugs = {project_slug(url): url for url in project_urls()}
    tallies = project_tallies(list(slugs), cited_results(overview), significance_levels())
    names = {slug: repository_name(url) for slug, url in slugs.items()}
    return [(slugs[slug], tallies[slug]) for slug in project_order(tallies, names)]


def results_filter_url(project: str, level: int | None = None) -> str:
    """The results page opened on one project's results, and on those at one S rung with
    `level`: the Project and At significance presets of the bar (`result_filters`). The
    page's own defaults hide no result, so the link clears nothing."""
    exact = "" if level is None else f"&s={level}"
    return f"{RESULTS_PAGE}?project={project}{exact}"


def project_tally(url: str, tally: ProjectTally) -> str:
    """A project card's closing line, its results in the register: the total, then in
    parentheses the count at each significance level that has one, the highest first,
    `6 results (3 at S4, 3 at S3)`. The total links to the results table filtered to the
    project, and each count to the same table at that level. A project with one level
    keeps the parentheses, so every tally reads the same way and names its level. A
    project with no registered result has no line."""
    total = len(tally.results)
    if not total:
        return ""
    slug = project_slug(url)
    counts = ", ".join(
        f'<a href="{_esc(results_filter_url(slug, level))}">{count} at S{level}</a>'
        for level, count in tally.counts
        if count
    )
    noun = "result" if total == 1 else "results"
    return f'<a href="{_esc(results_filter_url(slug))}">{total} {noun}</a> ({counts})'


def other_project_cards(overview: Overview) -> str:
    """One card per other project, in `project_order`: its repository's name, its author,
    what it holds and its address, and at its foot its tally of registered results
    (`project_tally`). Each card's link opens the project in a new tab. The note is prose
    like a page card's, so a case it names (`n = 21`) is set as math."""
    listed = {url: (author, note) for url, author, note in OTHER_PROJECTS}
    cards = []
    for url, tally in ranked_projects(overview):
        author, note = listed[url]
        cards.append(
            link_card(
                url,
                f"By {author}",
                _esc(repository_name(url)),
                tex_bounds(note),
                size=SECTION_CARD_SIZES["projects"],
                foot=project_tally(url, tally),
            )
        )
    return _cards(cards)


#: The page the atlas's film card opens: the film alone, at full size.
VISUALIZE_PAGE = "visualize.html"

#: The atlas's three direct cards, the overview's PDFs and Videos section: where each
#: goes, the picture heading it (a file served beside the page), its label, value and
#: note. A label says what the card is and the form it opens in, which are the section
#: heading's two words: a poster is a PDF, the film a video.
ATLAS_CARDS: tuple[tuple[str, str, str, str, str], ...] = (
    (
        "known-best-1-100.pdf",
        "known-best-1-100-card.png",
        "Poster \u00b7 PDF",
        "n = 1 to 100",
        (
            "The first hundred, each labelled with its best-known side and, where the case is "
            "open, its strongest verified lower bound."
        ),
    ),
    (
        "known-best-1-324.pdf",
        "known-best-1-324.png",
        "Poster \u00b7 PDF",
        "n = 1 to 324",
        (
            "Every tracked case as its best-known packing, on one sheet that prints at 44 by "
            "51 inches."
        ),
    ),
    (
        VISUALIZE_PAGE,
        "ascent-n1-324-poster.png",
        "Film \u00b7 Video",
        "The ascent to n = 324",
        (
            "The atlas built one square at a time, each step naming the bound it reaches and "
            "its source. 8\u00a0m\u00a014\u00a0s."
        ),
    ),
)


def atlas_cards() -> str:
    """The atlas's posters and film as three cards side by side, each headed by its
    picture and itself the link: a poster opens its PDF, the film its own page. They
    are the overview's PDFs and Videos section, under The Atlas."""
    return _cards(
        [
            link_card(
                href,
                label,
                tex_bounds(value),
                tex_bounds(note),
                hero=hero,
                size=SECTION_CARD_SIZES["atlas"],
            )
            for href, hero, label, value, note in ATLAS_CARDS
        ]
    )


#: The atlas grid's drawings, in units across the frame. One drawing serves the cell and
#: the popover, which shows it about four hundred pixels across: at 100 units the
#: rounding shows there as uneven gaps, and 400 costs about 26 kB more gzipped.
ATLAS_UNITS = 400

#: How many cases the atlas grid shows until the reader asks for the rest: the first
#: hundred, the cases of the smaller poster.
ATLAS_FIRST = 100

#: The film's panel labels, keyed by the composite record's badge (glyph, style): the
#: words `packages/workbench/src/view/facts.ts` draws under each badge (`BADGE_LABELS`).
FILM_BADGES: dict[tuple[str, str], str] = {
    ("O", "solid"): "optimal",
    ("=", "solid"): "exact",
    ("\u2248", "muted"): "numerical",
    ("R", "solid"): "rigid",
    ("R", "muted"): "rigid (catalogue)",
}

#: `side.display` and `lower.display` as the composite record writes them.
_FILM_DISPLAY = re.compile(r"^s\((\d+)\) ([=\u2264\u2265]) (.+)$")


def _film_value(display: str, n: int, relations: str) -> tuple[str, str]:
    match = _FILM_DISPLAY.match(display)
    if match is None or int(match[1]) != n or match[2] not in relations:
        raise SystemExit(f"n = {n}: the atlas figure's {display!r} is not s({n}) {relations}")
    return match[2], match[3]


def atlas_film_facts() -> list[dict[str, object]]:
    """What the ascent film's panel says about each case, n = 1 to 324, read as the film
    reads it (`packages/workbench/tools/workbench_tools/build_candidate.py`, `load_facts`
    and `load_citations`).

    From the atlas figure's record: the bound as one statement, its values as the record
    displays them, the badges, a star where the lower bound is a recent result, and what
    is open (rigidity never is, as in the film). From `bound-citations.json`: the frontier
    record and each bound's source with this project's note.
    """
    import json  # noqa: PLC0415

    from devtools.build_bound_citations import corrects_tag  # noqa: PLC0415
    from devtools.overview_data import CITATIONS, COMPOSITE  # noqa: PLC0415

    figure = json.loads(COMPOSITE.read_text(encoding="utf-8"))["figure"]["entries"]
    cited = {
        entry["n"]: entry
        for entry in json.loads(CITATIONS.read_text(encoding="utf-8"))["citations"]["entries"]
    }
    facts: list[dict[str, object]] = []
    for entry in figure:
        n = entry["n"]
        relation, upper = _film_value(entry["side"]["display"], n, "=\u2264")
        lower = (
            _film_value(entry["lower"]["display"], n, "\u2265")[1]
            if entry["lower"]["shown"]
            else None
        )
        badges: list[list[str]] = []
        for badge in entry["badges"]:
            key = (badge["glyph"], badge["style"])
            if key not in FILM_BADGES:
                raise SystemExit(f"n = {n}: badge {key} is not one the film draws")
            badges.append([badge["glyph"], badge["style"], FILM_BADGES[key]])
        open_items: list[str] = []
        if entry["optimality"]["status"] == "open":
            open_items.append("optimality")
        if entry["exactness"]["state"] not in ("closed-form", "minimal-polynomial"):
            open_items.append("exact value")
        record = cited[n]
        # A lower bound standing in for a published result found unsound names that work,
        # `corrects Nagamochi 2005`, between its reference and its note (the owner,
        # 2026-10-02); it names outside work, never a correction to this register.
        citations = {
            bound: None
            if record.get(bound) is None
            else {
                "text": record[bound]["text"],
                "corrects": corrects_tag(record[bound].get("corrects")),
                "note": record[bound]["note"],
            }
            for bound in ("lower", "upper")
        }
        facts.append(
            {
                "n": n,
                "exact": relation == "=",
                "upper": upper,
                "lower": lower,
                "star": bool(entry["lower"]["recent_result"]),
                "badges": badges,
                "open": open_items,
                "record": record["record"],
                "cite": citations,
            }
        )
    if [fact["n"] for fact in facts] != list(range(1, len(facts) + 1)):
        raise SystemExit("the atlas figure's entries are not n = 1, 2, 3 and on, in order")
    return facts


#: The directions of the site's one arrow (paper-design.md, Arrows): each is the one
#: drawing, `--site-arrow` in site.css, turned or mirrored by `data-arrow`.
#: The arrow's five directions, and the double chevron's two: `double-down` for a control
#: that shows more below, `double-up` for one that shows less.
ARROW_DIRECTIONS = ("right", "left", "down", "up", "external", "double-down", "double-up")


def arrow_icon(direction: str = "right") -> str:
    """The site's arrow pointing `direction`, as inline markup: an empty, hidden span that
    site.css paints with the one arrow drawing in the text colour. It is never a typed
    `→`: the site's text face has no arrow glyphs, and each browser fell back to a
    different font for them, so no two arrows matched."""
    if direction not in ARROW_DIRECTIONS:
        raise ValueError(f"unknown arrow direction {direction!r}")
    return f'<span class="site-icon-arrow" data-arrow="{direction}" aria-hidden="true"></span>'


#: The atlas's two views, in tab order: the key the block's `data-atlas-view` and the
#: address's `?atlas=` take, and the tab's label. The first is the default and the one
#: the page is rendered in; `overview/atlas-view.js` lays the other out.
ATLAS_VIEWS: tuple[tuple[str, str], ...] = (("grid", "Grid"), ("triangle", "Triangle"))

#: The id the script gives the box of tiles, which each view tab controls.
ATLAS_PANEL = "atlas-cells"

#: The atlas's two drawings of a case, in tab order: the key the block's
#: `data-atlas-layer` and the address's `?layer=` take, and the tab's label. The house
#: drawing is the record's own rendering; the regularized one is the derived view
#: `atlas/known-best/regularized/` keeps for some cases (X-049, Exact Regularization),
#: and its key is the word the layer's index says every drawing of it must carry. The
#: first is the default and the one the page is rendered in; `overview/atlas-layer.js`
#: swaps the other in, and a case with no regularized view keeps its house tile.
ATLAS_LAYERS: tuple[tuple[str, str], ...] = (("house", "House"), ("regularized", "Regularized"))


def atlas_layer_mark() -> str:
    """The regularized layer's badge: one dot in the accent, drawn by site.css and hidden
    from assistive technology, whose names say "regularized" in words. A regularized
    tile carries it after its number, and the Regularized tab carries it before its word,
    so the tab is the key to the tiles."""
    return '<span class="site-atlas-layer-mark" aria-hidden="true"></span>'


def atlas_regularized() -> tuple[int, ...]:
    """The cases with a regularized drawing, read from the layer's index: each record it
    lists as regularized, whose view `devtools.render_regularized_atlas` has drawn.

    The set is the index's, so a view the layer gains joins the atlas at the next
    render. A drawing the index does not ask for, or one it asks for that is not there,
    is a stale render, and the page is refused rather than drawn from it.
    """
    import json  # noqa: PLC0415

    from devtools import render_frontier_page as frontier  # noqa: PLC0415

    index = json.loads(frontier.REGULARIZED_INDEX.read_text(encoding="utf-8"))
    label = ATLAS_LAYERS[1][0]
    if index.get("label") != label:
        raise SystemExit(f"the regularized index labels its drawings {index.get('label')!r}")
    listed = tuple(sorted(e["n"] for e in index["entries"] if e["status"] == "regularized"))
    drawn = tuple(
        sorted(
            int(path.stem.removeprefix("n-"))
            for path in frontier.REGULARIZED_RENDERINGS.glob("n-*.svg")
        )
    )
    if drawn != listed:
        missing = sorted(set(listed) - set(drawn))
        extra = sorted(set(drawn) - set(listed))
        raise SystemExit(
            f"the regularized drawings are stale (missing {missing}, unexpected {extra}); "
            "run python -m devtools.render_regularized_atlas --update"
        )
    return listed


def atlas_layer_tabs() -> str:
    """The tabs that choose the atlas's drawing, House or Regularized: the same strip as
    the view tabs (`atlas_view_tabs`), beside them over the tiles, a tablist of two
    buttons that swap a case's tile for its other drawing in place. House is selected
    and is the only tab in the page's tab order; the Regularized tab carries the badge
    its tiles carry (`atlas_layer_mark`). It ships `hidden`, as the view tabs do."""
    default = ATLAS_LAYERS[0][0]
    tabs = "".join(
        f'<button type="button" role="tab" id="atlas-layer-{key}" data-atlas-layer-tab="{key}" '
        f'aria-selected="{"true" if key == default else "false"}" '
        f'aria-controls="{ATLAS_PANEL}"{"" if key == default else ' tabindex="-1"'}>'
        f"{'' if key == default else atlas_layer_mark()}{_esc(label)}</button>"
        for key, label in ATLAS_LAYERS
    )
    return (
        '<div class="site-tabs site-atlas-layers" role="tablist" aria-label="Atlas drawings" '
        f"data-atlas-layers hidden>{tabs}</div>"
    )


def _atlas_cell(n: int, status: str, *, regularized: bool = False) -> str:
    """One case's tile: its drawing, a link to its case record, and its number under it.

    A regularized tile is the same tile drawn from the regularized rendering, marked
    `data-atlas-layer="regularized"`, named as the regularized view, and badged after its
    number. It reduces its drawing by `packing_svg`, as a house tile does, so the two
    differ only where the view moved a square or changed a square's shade.
    """
    from devtools import render_frontier_page as frontier  # noqa: PLC0415
    from devtools.render_case_pages import case_url  # noqa: PLC0415

    square = " data-atlas-square" if math.isqrt(n) ** 2 == n else ""
    if regularized:
        layer = f' data-atlas-layer="{ATLAS_LAYERS[1][0]}"'
        name = f"n = {n}, {ATLAS_LAYERS[1][0]} view, {_esc(status)}"
        drawing = frontier.packing_svg(
            n, units=ATLAS_UNITS, root=frontier.REGULARIZED_RENDERINGS
        )
        badge = atlas_layer_mark()
    else:
        layer, name, badge = "", f"n = {n}, {_esc(status)}", ""
        drawing = frontier.packing_svg(n, units=ATLAS_UNITS)
    return (
        f'<a class="site-atlas-cell" href="{case_url(n)}" data-case="{n}" '
        f'data-atlas-n="{n}"{square}{layer} '
        f'data-status="{_esc(status)}" aria-label="{name}">'
        f'{drawing}<span class="site-atlas-n">{n}{badge}</span></a>'
    )


def atlas_view_tabs() -> str:
    """The tabs over the atlas's tiles that choose its view, Grid or Triangle: the
    section tabs' strip (`.site-tabs`), but a tablist of two buttons that rearrange the
    one set of tiles in place, where the Visualize section's are links to two pages.

    The first view is selected and is the only tab in the page's tab order; the arrow
    keys move between the two (`overview/atlas-view.js`). The strip ships `hidden`, as
    the expander's row does: without the script it would do nothing, and the script
    shows it once the tiles are placed.
    """
    default = ATLAS_VIEWS[0][0]
    tabs = "".join(
        f'<button type="button" role="tab" id="atlas-view-{key}" data-atlas-tab="{key}" '
        f'aria-selected="{"true" if key == default else "false"}" '
        f'aria-controls="{ATLAS_PANEL}"{"" if key == default else ' tabindex="-1"'}>'
        f"{_esc(label)}</button>"
        for key, label in ATLAS_VIEWS
    )
    return (
        '<div class="site-tabs site-atlas-views" role="tablist" aria-label="Atlas layout" '
        f'data-atlas-views data-atlas-panel="{ATLAS_PANEL}" hidden>{tabs}</div>'
    )


def atlas_grid() -> str:
    """Every tracked case's known-best packing, n = 1 to 324, as a grid of drawings,
    each a link to its case record. With scripts, a cell opens the page's one case
    popover instead (`overview/case-popover.js`), which shows the case's record as its
    own page does: the visual summary, the drawing large and the bounds' number line,
    then the record's further data (`render_case_pages`, think-t21m).

    The block is rendered in the grid view (`data-atlas-view`), under tabs that switch
    it to the triangle (`atlas_view_tabs`). Both views are one set of tiles: the triangle
    places each by properties the script writes, so a tile's markup is the same in both.
    A perfect square's tile is marked `data-atlas-square`: it ends its row of the
    triangle, on the right edge, and the triangle numbers it in the text's colour.

    The cells, about a megabyte of SVG, sit in two `<template>`s, which the browser
    parses but does not render. The script places the first `ATLAS_FIRST` when the grid
    nears the viewport, so the page opens as fast as it did without them, and the rest
    only when the reader presses the button under the grid, "Show More" with the double
    chevron down. The button then reads
    "Show Less" with the chevron up and collapses the grid again; its name for assistive
    technology says what each does and how many cases that is (`data-name-more`,
    `data-name-less`), it controls the box of tiles (`ATLAS_PANEL`), and it is the site's
    one action under a table or grid (`.site-action`, with "See all results"). Its row
    ships `hidden`, since without the script it would do nothing. The atlas popover,
    filled by the script from a JSON of the film's facts, stood after the block until
    2026-10-03; the case popover took its place.

    The block is rendered with the house drawings (`data-atlas-layer`), under tabs beside
    the view tabs that switch it to the regularized ones (`atlas_layer_tabs`). The cases
    with a regularized view (`atlas_regularized`) have a second tile each, in a third
    `<template>`, which `overview/atlas-layer.js` swaps for the house tile in place; every
    other case keeps its house tile in both. Where no case has a view, the block has no
    third template and no layer tabs. The two strips stand in one row over the tiles
    (`.site-atlas-controls`), which the script places the tiles after.
    """
    from devtools import render_frontier_page as frontier  # noqa: PLC0415
    from devtools.render_case_pages import case_popover  # noqa: PLC0415

    cases = frontier.frontier_cases()
    status = {case["n"]: case["status"] for case in cases}
    cells = [_atlas_cell(case["n"], case["status"]) for case in cases]
    regularized = atlas_regularized()
    if not set(regularized) <= set(status):
        untracked = sorted(set(regularized) - set(status))
        raise SystemExit(f"regularized views of untracked cases: {untracked}")
    layer_cells = "".join(_atlas_cell(n, status[n], regularized=True) for n in regularized)
    layers = (
        (atlas_layer_tabs(), f"<template data-atlas-regularized>{layer_cells}</template>")
        if regularized
        else ("", "")
    )
    more, less = "Show More", "Show Less"
    name_more = f"Show more: all {len(cases)} cases"
    name_less = f"Show less: the first {ATLAS_FIRST}"
    return (
        f'<div class="site-wide site-atlas-grid" data-atlas-view="{ATLAS_VIEWS[0][0]}" '
        f'data-atlas-layer="{ATLAS_LAYERS[0][0]}" data-atlas-grid>'
        '<div class="site-atlas-controls" data-atlas-controls>'
        f"{atlas_view_tabs()}{layers[0]}</div>"
        f"<template data-atlas-first>{''.join(cells[:ATLAS_FIRST])}</template>"
        f"<template data-atlas-rest>{''.join(cells[ATLAS_FIRST:])}</template>"
        f"{layers[1]}"
        # The triangle's one-line key ("Each row ends at a perfect square…") stood here
        # and the line under the expander ("Every case from n = 1 to 324 is also in the
        # frontier survey, and each has a case record.") after it, until 2026-10-02 (the
        # owner, think-l38m): each tile opens its case record, and the Frontier page is a
        # page card. The expander's row ends the block.
        '<p class="site-action-row site-atlas-toggle-row" hidden>'
        '<button type="button" class="site-action site-atlas-toggle" '
        f'data-atlas-toggle aria-expanded="false" aria-controls="{ATLAS_PANEL}" '
        f'aria-label="{name_more}" data-label-more="{more}" data-label-less="{less}" '
        f'data-name-more="{name_more}" data-name-less="{name_less}">'
        f"<span data-atlas-label>{more}</span>{arrow_icon('double-down')}</button></p>"
        f"</div>{case_popover()}"
    )
