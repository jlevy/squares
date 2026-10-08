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
import json
import math
import re
import textwrap
from collections.abc import Collection, Iterable, Mapping, Sequence
from datetime import date, timedelta
from functools import cache
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Literal, NamedTuple, get_args
from urllib.parse import urlsplit

from devtools import repo_links
from devtools.check_results import KINDS, kind_label
from devtools.overview_data import (
    APOSTROPHE,
    BIBLIOGRAPHY,
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
    N11_THRESHOLD_BOUND_REVIEW,
    PACKING_METHODS,
    RESULTS_PAGE,
    SITE_PAGES,
    paper_path,
    paper_record,
)
from devtools.render_overview import PAPERS as PAPER_RECORDS
from devtools.render_recent_results import REPORTED_MARK, SUPERSEDED, listed, superseded
from devtools.repo_links import branch_file
from devtools.result_status import CONFIRMED, STATUSES
from sqpack.yamlio import safe_load


def _esc(text: object) -> str:
    return html.escape(str(text), quote=True)


def _fill(rung: str) -> str:
    """The attributes `site.css` colours a rung chip by: its scale, `V` or `C`, and its
    level, which darkens the fill. Significance is no chip (`significance_mark`)."""
    return f'data-rung="{_esc(rung[0])}" data-level="{_esc(rung[1:])}"'


def _rung(label: str) -> str:
    """A rung chip as a table prints it. The rung's full meaning is the title of the
    diagram's chip (`_ladder_cell`), where the rubric is explained once."""
    return f'<span class="site-chip site-rung-fill" {_fill(label)}>{_esc(label)}</span>'


#: The significance ladder's top rung, the most bars its mark draws.
SIGNIFICANCE_TOP = 5


def significance_mark(level: int, meaning: str = "") -> str:
    """A significance rung as the site draws it wherever it shows one: its letter and
    level, `S4`, in the significance teal (`--site-significance`), and that many small
    bars after it in the same ink, one to five. It is no chip: significance asks how
    much a result matters, a different question from what the verification and
    confirmation chips answer, so it looks different from them (the owner, 2026-10-03,
    `think-m3m4`). It is one image to a screen reader, named by its level, and titled
    with the rubric's `meaning` where one is given."""
    bars = '<span class="site-significance-bar"></span>' * level
    title = f' title="{_esc(meaning)}"' if meaning else ""
    return (
        f'<span class="site-significance" data-level="{level}" role="img" '
        f'aria-label="Significance S{level} of {SIGNIFICANCE_TOP}"{title}>'
        f'<span class="site-significance-label" aria-hidden="true">S{level}</span>'
        f'<span class="site-significance-bars" aria-hidden="true">{bars}</span></span>'
    )


def standing_key(standing: str) -> str:
    """A standing as a row attribute and a filter value: `current best, reported`
    is `current-best-reported`. A result that has no standing, one that claims no
    bound, has the empty key."""
    return re.sub(r"[^a-z]+", "-", standing).strip("-")


def is_superseded(result: Result) -> bool:
    """Whether a result is no longer the best (`render_recent_results.superseded`): it
    is a bound, no case bound rests on it now and its cases hold one at least as good,
    which is derived from the case records and held to the numbers by
    `devtools.check_standing`; or it is a result of another kind whose register entry
    declares a later result that implies the whole of it (`superseded_by`). A result that
    still holds a bound, a better bound pending adoption, a second proof of a value
    another result holds, a result that is no bound, and one superseded only in part are
    all current. A row says so as `data-current`, which the bar's "Hide superseded"
    reads (`result_filters`), and draws the `superseded` chip (`supersession_marks`)."""
    return superseded(result.record, result.standing)


def standing_chip(standing: str, words: str | None = None) -> str:
    """A result's standing as a chip, the plain gray one, lettered with the standing or
    with `words`. A table draws one word, `superseded`, for both its marks: the
    `superseded in part` mark's chip says `superseded` and keeps its own standing in
    `data-standing` (`supersession_marks`). It is the kind's and the status's own chip
    and differs from them only in its word."""
    return (
        f'<span class="site-chip" data-standing="{_esc(standing_key(standing))}">'
        f"{_esc(standing if words is None else words)}</span>"
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
    from devtools.render_n11_lower_bounds_explainer import COMPOSITE_ASSETS  # noqa: PLC0415
    from devtools.render_overview import image_dimensions  # noqa: PLC0415

    if "://" in src or src.startswith("//"):
        raise SystemExit(f"{src}: a card's hero is served beside the page, never fetched")
    source = next((path for path in COMPOSITE_ASSETS if path.name == src), None)
    if source is None:
        raise SystemExit(f"{src}: a card's hero must be a published atlas image")
    width, height = image_dimensions(source)
    return (
        '<span class="site-card-hero">'
        f'<img src="{_esc(src)}" alt="" width="{width}" height="{height}" '
        'loading="lazy" decoding="async"></span>'
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
#: wrapping row would not set them as they are meant to read: the seven page cards stand
#: one, three and three, the Frontier page alone at the top, then the three parts of the
#: n = 11 series on one line, one card per paper in reading order (the series plan,
#: 2026-10-05), then the methods tutorial, the first-principles tutorial and the workbench.
#: They stood one, two and two while
#: the site had two papers (the owner, 2026-10-02, `think-ns3d`; two over three from
#: `think-ec5k` the same day, the Frontier page's card last). Each line is a row of its
#: own, and none sets more cards to a line than the longest line holds, so the lines
#: share one column width, a third of the frame's. The stylesheet holds each longest
#: line here to a rule.
SECTION_CARD_LINES: dict[str, tuple[int, ...]] = {"pages": (1, 3, 3)}


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
    """The claim, significance, novelty and record links carried by a result's row.

    This preview remains available without scripts or a network connection. The full
    result fragment retains composition and next-rung details (`result_overview.head`).
    """
    record = result.record
    rows = [("Claim", prose_html(record["claim"]))]
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
    rows.append(("Records", f'<div class="site-records">{_records(result)}</div>'))
    body = "".join(f"<dt>{label}</dt><dd>{value}</dd>" for label, value in rows)
    return f'<dl class="site-detail">{body}</dl>'


def _records(result: Result) -> str:
    """A result's records, its case link, the register, its evidence, source and reviews,
    as the short form of its row's popover ends with them (`_detail`): one line, a dot
    drawn between two links (`site.css`). The table carried them as a Details column
    until 2026-10-04 (`think-46fw`); the row opens to them, and the overview it fetches
    links each of them again (`result_overview.links_section`)."""
    return "".join(
        f'<a href="{_esc(link.url)}"'
        + (f' title="{_esc(link.title)}"' if link.title else "")
        + f">{_esc(link.label)}</a>"
        for link in result.records
    )


def result_row_popover_body(
    result: Result,
    overview: Overview,
    *,
    amendments: Sequence[Mapping[str, Any]] = (),
    registered_paths: Collection[str] = (),
) -> str:
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

    return result_overview.result_popover_html(
        result, overview, amendments=amendments, registered_paths=registered_paths
    )


#: Where complete result pages are served under the site's root. The historic
#: constant name remains for callers that also use their articles in popovers.
#: Not `results/`: `results.html` is still
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
    """The red star of a new result in a table of results, or nothing
    (`new_result_label`): in the significance cell, after the significance mark's bars
    (`significance_cell`), where it stood after the result's text until 2026-10-03
    (`think-m3m4`). The glyph is an image whose name and tooltip are the label, so it is
    read and not only seen, and the row's own name says "new result" too
    (`result_row`)."""
    label = new_result_label(result, overview)
    if not label:
        return ""
    return (
        f'<span class="site-star" role="img" aria-label="{_esc(label)}" '
        f'title="{_esc(label)}">{STAR}</span>'
    )


def star_legend() -> str:
    """The sentence that says what the star in a table of results marks, with the star
    itself, for the prose above the Results page's table (`{{STAR_LEGEND}}` in its
    article); the homepage's table keys the star in its legend alone (`rung_legend`)."""
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
    detail = row_detail(
        f"pop-result-{result.id.lower()}",
        name=f"{name}, {NEW_RESULT}" if starred else name,
        trigger=trigger,
        label=result.id,
        title=tex_bounds(result.summary),
        body=(
            f'<p><a href="{result_fragment(result.id)}">Read the complete result record</a></p>'
        ),
        source=result_fragment(result.id),
        action=(result_fragment(result.id), "Open Result Record"),
    )
    return RowDetail(
        detail.attributes,
        f'<a class="site-row-open" href="{result_fragment(result.id)}">{trigger}</a>',
        detail.popover,
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
RECENT_DEFAULTS = FilterDefaults(significance=3, max_age=180, hide_superseded=True)

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
    in one order. The date; the significance, with a new result's star; the result; the
    cases; the credit; the verification and confirmation rungs, with the kind under
    them; the status; and the id, which is the row's trigger. The owner set this order
    on 2026-10-02: the id led and the date closed the row until then (`think-t090`);
    the status stood under the kind, in the rungs' cell, though it is where the result
    stands and no rung (`think-ybt5`); and the records stood on a line under the
    summary, where the result's cell holds the claim alone now (`think-e4o3`).
    Significance left the rungs for a column of its own, the second, on 2026-10-03
    (`think-m3m4`). The records, a Details column from 2026-10-02, moved into the row's
    popover on 2026-10-04 (`think-46fw`), which reads more cleanly than a column of
    links. A column sorts where an order means something, on either page."""
    return (
        "<thead><tr>"
        '<th data-sort="text" title="Published, for a result by others; established, for '
        f'this project{APOSTROPHE}s">Date</th>'
        '<th data-sort="num" class="site-col-s" title="Significance, S1 to S5, and a star '
        'on a new result">S</th>'
        '<th class="site-col-result">Result</th>'
        '<th data-sort="num" class="num site-col-n">n</th>'
        '<th data-sort="text">Credit</th>'
        '<th data-sort="text" title="Verification and confirmation, then what the result '
        'is">Rungs</th>'
        '<th data-sort="text" class="site-col-status" title="How far the work on it here '
        "has gone: recorded, reviewed, confirmed or incomplete; then who has the next "
        'move, and superseded, wholly or in part, and by what, where it is">Status</th>'
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
    return f'<a href="{result_fragment(result.id)}">{tex_bounds(result.summary)}</a>'


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
    its date (`date_cell`), its significance with the star a new result earns
    (`significance_cell`), its summary (`result_text`), its cases (`case_list`), its
    credit (`credit_cell`), its verification and confirmation chips with its kind on a
    line under them (`ladder_chips`, `kind_chip`), its status line (`status_marks`), and
    its id (`id_cell`). Its records are in the popover the row opens (`_detail`). The
    status cell sorts on the status word alone."""
    record = result.record
    standing = f'<span class="site-standing">{status_marks(result)}</span>'
    return (
        f'<td class="site-col-date" data-value="{_esc(result.dated[1])}">'
        f"{date_cell(result)}</td>"
        f"{significance_cell(result, overview)}"
        f'<td class="site-col-result">{result_text(result)}</td>'
        f'<td class="{case_cell_class(result)}" data-value="{result.first_n}">'
        f"{case_list(result)}</td>"
        f'<td class="site-col-credit" data-value="{_esc(result.credit)}">'
        f"{credit_cell(result.credit)}</td>"
        f'<td class="site-rungs" '
        f'data-value="{_esc(record["confirmation"] + record["verification"])}">'
        f'{ladder_chips(result)}<span class="site-kind">{kind_chip(result)}</span></td>'
        f'<td class="site-col-status" data-value="{_esc(result.status)}">{standing}</td>'
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


def retired_result_aliases() -> dict[str, str]:
    """Exact withdrawn result addresses retained by the published URL register."""
    from devtools.site_urls import load_registry  # noqa: PLC0415

    return {
        Path(row.path).stem: row.path
        for row in load_registry()
        if row.status == "withdrawn"
        and row.kind == "result"
        and not row.pattern
        and re.fullmatch(r"result/t-\d+\.html", row.path)
    }


def table_of_results(overview: Overview, defaults: FilterDefaults, *, here: bool) -> str:
    """The complete results table or the overview's static recent selection.

    The complete page keeps every result and its filtering tools, with rows outside
    the defaults hidden at first paint. The overview emits only rows selected by its
    published reference date and RECENT_DEFAULTS, followed by an ordinary link to the
    complete table. Supported query state travels through that link.

    Both use the same cells and record popovers. Complete-table rows own their
    canonical fragment IDs; overview rows name the same result with data-result.
    """

    results = recent_results(overview)
    reference = reference_date(overview)
    if not here:
        results = [
            result for result in results if shown_by_default(result, defaults, reference)
        ]
    aliases = retired_result_aliases()
    retired = json.dumps(aliases, separators=(",", ":")) if not here else ""
    notices = (
        "".join(
            f'<p class="site-withdrawn-result" id="{_esc(name)}">'
            f'{_esc(name.upper())} was withdrawn. <a href="{_esc(path)}">'
            f"{_esc(name.upper())} withdrawal explanation</a>.</p>"
            for name, path in aliases.items()
        )
        if here
        else ""
    )
    body = []
    popovers = []
    for result in results:
        row, popover = result_table_row(
            result, overview, here=here, shown=shown_by_default(result, defaults, reference)
        )
        body.append(row)
        popovers.append(popover)
    return (
        '<div class="site-wide">'
        + (
            result_filters(overview, results, defaults)
            if here
            else f'<p class="site-recent-scope">{len(results)} recent results of significance '
            "S3 or higher, "
            "from the last 180 days, excluding superseded results. "
            '<a href="all-results.html" data-all-results '
            f'data-result-ids="{_esc(" ".join(r.id.lower() for r in overview.results))}" '
            f'data-retired-results="{_esc(retired)}">'
            "Browse and filter every "
            "result</a>.</p>"
        )
        + '<div class="site-table-wrap">'
        '<table class="kpress-table site-table site-results" data-site-table>'
        f"{result_head()}"
        f"<tbody>{''.join(body)}</tbody></table></div>"
        f"{rung_legend(here=here)}{notices}{''.join(popovers)}</div>"
    )


#: Where the rating ladders define every rung in full: the Results page's section.
LADDERS_SECTION = "verification-ladders"


def rung_legend(*, here: bool) -> str:
    """The legend under a table of results, boxed, three short lines: every significance
    mark, S1 to S5; every verification and confirmation chip, V0 to C5; and the star,
    with a link to where the ladders define each rung in full, on the results page
    (`here`) or from another page. Each mark and chip is titled with the rubric's
    meaning. It took the place, on 2026-10-03, of the whole ladder grid the overview
    set under its table (the owner, `think-42dx`), and stood between the table's bar and
    the table until 2026-10-04, when the owner moved it under the table in a box of its
    own, so it reads as a legend and not as more of the filters."""
    meanings = rung_meanings()
    levels = rubric_levels()

    def chips(scale: str) -> str:
        return " ".join(
            f'<span class="site-chip site-rung-fill" title="{_esc(meanings[label])}" '
            f"{_fill(label)}>{label}</span>"
            for label in (f"{scale}{level}" for level, _ in sorted(levels[scale]))
        )

    names = {scale: name for scale, name, _, _ in DIMENSIONS}
    marks = " ".join(
        significance_mark(level, meanings[f"S{level}"]) for level, _ in sorted(levels["S"])
    )
    href = f"#{LADDERS_SECTION}" if here else f"{RESULTS_PAGE}#{LADDERS_SECTION}"
    star = f'<span class="site-star" aria-hidden="true">{STAR}</span>'

    def group(scale: str, shown: str) -> str:
        return (
            '<span class="site-rung-legend-group">'
            f'<span class="site-rung-legend-name">{_esc(names[scale])}</span> {shown}</span>'
        )

    # The star's words are a span of their own: no shipped face carries the star, and a
    # run that held both would be drawn, and measured, as the star's host face.
    return (
        '<div class="site-rung-legend" role="note" aria-label="What a row\u2019s marks mean">'
        f"<p>{group('S', marks)}</p>"
        f"<p>{group('V', chips('V'))} {group('C', chips('C'))}</p>"
        f'<p><span class="site-rung-legend-group">{star} <span>{NEW_RESULT}</span></span> '
        f'<a href="{href}">What each rung means</a></p>'
        "</div>"
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
    """One rung of the ladder diagram: the chip the tables use, or for significance its
    mark (`significance_mark`), titled with the rubric's full meaning, and the two-line
    description."""
    label = f"{scale}{level}"
    meaning = rung_meanings()[label]
    rung = (
        significance_mark(level, meaning)
        if scale == "S"
        else f'<span class="site-chip site-rung-fill" title="{_esc(meaning)}" '
        f"{_fill(label)}>{label}</span>"
    )
    return (
        f'<div class="site-ladders-cell" role="cell" data-ladder="{scale}">'
        '<div class="site-ladders-rung">'
        f"{rung}"
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
    """Every result ordered by displayed date, then ID, newest first.

    The complete table uses this whole list. The overview selects its static recent
    subset from it with RECENT_DEFAULTS and the publication's reference date.
    """
    return sorted(overview.results, key=lambda r: (first_day(r.dated[1]), r.id), reverse=True)


def significance(result: Result) -> int:
    """A result's S rung, the level its significance mark shows."""
    return int(result.record["significance"]["score"])


def significance_cell(result: Result, overview: Overview) -> str:
    """A result's significance cell, the second of its row in both tables of results:
    its mark (`significance_mark`), titled with the rubric's meaning, then the star a
    new result earns (`new_result_star`). The column is narrow and sorts on the level."""
    level = significance(result)
    mark = significance_mark(level, rung_meanings()[f"S{level}"])
    return (
        f'<td class="site-col-s" data-value="{level}">'
        f"{mark}{new_result_star(result, overview)}</td>"
    )


def result_rungs(result: Result) -> tuple[str, str, str]:
    """A result's three rungs in the order the site lists them wherever it shows them:
    significance first, then verification and confirmation (`S4`, `V4`, `C3`). The
    register's own documents keep theirs, verification first."""
    record = result.record
    return (f"S{significance(result)}", record["verification"], record["confirmation"])


def ladder_chips(result: Result) -> str:
    """A result's verification and confirmation chips, V and C, a space apart, as a
    table's rungs cell sets them, its significance having a column of its own."""
    return " ".join(_rung(rung) for rung in result_rungs(result)[1:])


def rung_chips(result: Result) -> str:
    """A result's rungs, S, V and C, a space apart: its significance mark
    (`significance_mark`), then its verification and confirmation chips
    (`ladder_chips`). The one place their order is set, for a popover, a result's
    overview and a case record; a table's row sets the significance in a column of its
    own."""
    level = significance(result)
    return f"{significance_mark(level, rung_meanings()[f'S{level}'])} {ladder_chips(result)}"


def superseder_link(other: str, reported: Collection[str]) -> str:
    """A superseding result as a mark names it: a link to its row, followed where it is a
    report no replay has confirmed by `(reported)` (`Supersession.named`)."""
    link = f'<a href="{_esc(result_url(other))}">{_esc(other)}</a>'
    return f"{link} {REPORTED_MARK}" if other in reported else link


def supersession_marks(result: Result) -> str:
    """Whether a result is superseded, and by what, as its status line ends: `superseded`
    where it is (`is_superseded`), then `superseded in part` where a later result implies
    some of it, each followed by the results that supersede it as links to their rows
    (`Result.supersessions`): the results a superseded bound's cases rest on now, or
    those a result of another kind declares imply it. Each mark and its results are one
    element, and an id never breaks at its hyphen (`site.css`).

    The chip is the one word `superseded` for both marks, and `in part` leads the quiet
    text after it, so the line reads as the register's words do (`Supersession.words`):
    a chip never wraps, the status column is as wide as its widest chip, and the four
    words as one chip, 150 pixels, set the column 52 pixels wider than `superseded` does,
    which the n column paid for (`think-kmi4`). The partial mark's chip keeps its own
    standing, `data-standing="superseded-in-part"`, and its row stays current."""
    marks = []
    for mark in result.supersessions:
        links = [superseder_link(other, mark.reported) for other in mark.by]
        extent = _esc(mark.mark.removeprefix(SUPERSEDED).strip())
        after = " ".join(filter(None, (extent, f"by {listed(links)}" if links else "")))
        quiet = f' <span class="site-cell-quiet">{after}</span>' if after else ""
        chip = standing_chip(mark.mark, SUPERSEDED)
        marks.append(f'<span class="site-superseded">{chip}{quiet}</span>')
    return " ".join(marks)


def status_marks(result: Result) -> str:
    """A result's status line: its status chip, always; who has the next move, where
    the register records it (`activity_chip`); and whether it is superseded, with the
    results that supersede it (`supersession_marks`)."""
    marks = (status_chip(result.status), activity_chip(result), supersession_marks(result))
    return " ".join(filter(None, marks))


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
    bar starting at the recent defaults. The line under it, "See all results", links to
    the other table, as a status line's superseding results do, each to its row there
    (`supersession_marks`)."""
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


class Paper(NamedTuple):
    """One of the site's papers, as its card says what it is: where it is served, a caps
    label naming it, its title, one or two sentences on what it is, and the size of its
    card on the Papers page. The title and description are register prose, so `n = 11`
    and a bound in either are set as math. The card is the link to the paper and holds
    no other, so what a description names (T-060, the series) is linked from the Papers
    page's introduction (`templates/papers-article.md`)."""

    href: str
    label: str
    title: str
    description: str
    size: CardSize = "large"


#: What each part of the n = 11 series says of itself on its cards and in README, by
#: slug, in the words of the series plan (`docs/project/specs/active/
#: plan-2026-10-05-n11-explainer-series.md`, Series Presentation): each title is its
#: renderer's (`render_overview.PAPERS`) in sentence case, and each line names the result
#: the paper proves or explains. Part III's line says what T-060's rungs allow, `V3/C3`:
#: a proof, machine-checked here with its review record pending, never a formal one.
SERIES_CARDS: dict[str, tuple[str, str]] = {
    N11_LOWER_BOUNDS_EXPLAINER: (
        "New lower bounds for square packing for n = 11",
        (
            "How weighted points and 2-of-3 threshold atoms prove T-018, T-025 and T-026, "
            "s(11) >= 3.8264\u2026, with interactive figures."
        ),
    ),
    N11_THRESHOLD_BOUND_REVIEW: (
        "A review of the certified lower bound s(11) > 31/8 for 11 squares",
        (
            "Explains Kleddamag\u2019s proof that s(11) > 31/8 (T-037): five-site k-of-m "
            "charges, k-of-m charges on shrunken parents with strict cores, and a "
            "reoptimized certificate over 12,028 angle rows."
        ),
    ),
    N11_OPTIMALITY_REVIEW: (
        "A review of the optimality proof of the Trump packing of 11 squares",
        (
            "Explains Queuingtheorydotcom\u2019s proof that Trump\u2019s packing is optimal, "
            "s(11) = 3.8770835\u2026 (T-060): construction, case exclusions, capture and "
            "local isolation."
        ),
    ),
    "exact-side-values": (
        "Exact side values for packing unit squares",
        (
            "All retained current and superseded side polynomials through n = 324, "
            "with exact root and irreducibility checks, closed forms, and routes for "
            "the remaining numerical values."
        ),
    ),
}

#: Where each part of the series is served, under `papers/` by its slug
#: (`render_overview.paper_path`); each renderer's `SITE_PATH` is the same path from the
#: same slug.
LOWER_BOUNDS_PAPER = paper_path(N11_LOWER_BOUNDS_EXPLAINER)
THRESHOLD_BOUND_PAPER = paper_path(N11_THRESHOLD_BOUND_REVIEW)
OPTIMALITY_PAPER = paper_path(N11_OPTIMALITY_REVIEW)

#: The site's papers, in the order the Papers page shows them, one large card each
#: (`paper_cards`): the three parts of the n = 11 series in reading order, I, II, III,
#: each labelled by its part (`render_overview.PAPERS`, the one registry a new paper is
#: entered in), then the standalone methods tutorial and the first-principles tutorial,
#: the background to the series, whose description is
#: `TUTORIAL.md`'s own opening, its audience and what it owns.
PAPERS: tuple[Paper, ...] = (
    *(
        Paper(
            href=paper_path(record.slug),
            label=record.label,
            title=SERIES_CARDS[record.slug][0],
            description=SERIES_CARDS[record.slug][1],
        )
        for record in PAPER_RECORDS
        if record.part is not None
    ),
    Paper(
        href=paper_path(PACKING_METHODS),
        label=paper_record(PACKING_METHODS).label,
        title="How record square packings are found",
        description=(
            "How seeds, search, local refinement and exact checks produce record upper bounds."
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
#: Each part of the series, whose card reads the same on the overview as on the Papers
#: page.
EXPLAINER = next(paper for paper in PAPERS if paper.href == LOWER_BOUNDS_PAPER)
THRESHOLD_REVIEW = next(paper for paper in PAPERS if paper.href == THRESHOLD_BOUND_PAPER)
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
#: (`s(11) >= 3.8264…`) and set as math. The three parts of the n = 11 series stand
#: together, in reading order, each card in its paper's own words, as on the Papers page.
#: Every address is a full page the site serves, a paper's a directory below the root,
#: so its card links straight to it. The Frontier page's card is first, on a line of its
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
    *((paper.href, paper.label, paper.title, paper.description) for paper in PAPERS[:-1]),
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
        "https://github.com/SidG2k1/square-packing-refinements",
        "Siddharth Gupta",
        (
            "Seventeen rational refinements of Nate Chaoweeraprasit's SQUISH packings, "
            "using Evan Daniel's optimizer; fourteen finite upper-bound improvements selected "
            "here (T-127) and three withdrawn. Exact feasibility is confirmed with "
            "independently re-implemented code; optimality is not established."
        ),
    ),
    (
        "https://github.com/ry-xu/square_packing",
        "Ryan Xu",
        (
            "Complete rational packings and an undilated radical n = 51 construction; "
            "finite feasibility is confirmed here (T-125, T-126)."
        ),
    ),
    (
        "https://github.com/ry-xu/square_packing/blob/8dc415296f697f5140caea27c7a0193d52deb4e6/square_packing_records.json",
        "Ryan Xu",
        "The complete source report retained for the rational packing comparisons.",
    ),
    (
        "https://github.com/wand125/square-packing",
        "wand125",
        "Canonical certificate and checker repository; historical source pins remain valid.",
    ),
    (
        "https://github.com/lollipoll/couzo-five-exact-certificates",
        "Seth Rehwaldt",
        (
            "Rational refinements of Couzo's packings; complete finite certificates at "
            "n = 105 and 292 are replayed here (T-117)."
        ),
    ),
    (
        "https://github.com/lollipoll/certified-square-packing-68",
        "Seth Rehwaldt",
        (
            "An exact finite rational refinement of Couzo's n = 68 packing, replayed "
            "here (T-118). Its analytic root and dual programs remain outside that replay."
        ),
    ),
    (
        "https://github.com/evand/square-packing",
        "Evan Daniel",
        (
            "Exact covers settling n = 21, 32, 45 and 60, and s(k\u00b2 \u2212 3) = k for every"
            " k \u2265 6; s(k\u00b2 \u2212 4) = k awaits its replay here."
        ),
    ),
    (
        "https://github.com/squarepacker/s12-lower-bound",
        "Ryu Sungjoon",
        (
            "Evan Daniel's s(12) points rescaled and then re-weighted, the lower bound"
            " s(12) \u2265 7943/2000 for twelve squares."
        ),
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
        (
            "Improved packings for 49 counts from n = 68 to 307. "
            "Eight complete rational refinements in issue451 (T-128) and five follow-up "
            "certificates at 84, 86, 105, 175 and 270 (T-130) have retained "
            "finite-feasibility results; selected-case integration remains pending."
        ),
    ),
    (
        "https://github.com/itsnaka/squish-certs",
        "Nate Chaoweeraprasit",
        "Exact rational certificates for SQUISH upper-bound packings.",
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
        "https://github.com/Queuingtheorydotcom/11SquaresFormalized",
        "Queuingtheorydotcom et al.",
        "A Lean 4 formalization of that proof, trusting Lean's compiler for its certificates.",
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

#: David Ellsworth's Squares in Squares catalogue, the record's `[Kingbird]`.
KINGBIRD = "https://kingbird.myphotos.cc/packing/squares_in_squares.html"

#: The catalogues of the record packings, which lead the Other Square Packing
#: Projects section in this order, ahead of the ranked cards (the owner, 2026-10-05,
#: `think-lvhh`): each one's address, its name, its maintainer as the record credits
#: them, and what it holds. Ellsworth's catalogue is the baseline of every upper bound
#: (`kingbird-current` in the source-coverage register). Erich Friedman's original page
#: is the one the catalogue's header credits, at the archived address that header links
#: (`resources/web/kingbird-squares-in-squares.md`). Evan Daniel's atlas is the
#: bibliography's `[evand square packing atlas 2026-10-04]`.
CATALOGUE_SITES: tuple[tuple[str, str, str, str], ...] = (
    (
        KINGBIRD,
        "Squares in Squares",
        "David Ellsworth after Erich Friedman",
        (
            "The catalogue of record packings, with their exact sides and histories: the"
            " baseline of every upper bound here."
        ),
    ),
    (
        "https://web.archive.org/web/20230530194618/https://erich-friedman.github.io/packing/squinsqu/",
        "Erich\u2019s Packing Center",
        "Erich Friedman",
        (
            "The original Squares in Squares page, as archived on 30 May 2023, which"
            " Ellsworth\u2019s catalogue continues."
        ),
    ),
    (
        "https://evand.github.io/square-packing/",
        "Square Packing Atlas",
        "Evan Daniel",
        (
            "Every record packing drawn beside the proven floor beneath it, with a page of"
            " open problems."
        ),
    ),
)

#: Other cited result pages, including first-party GitHub issue reports, ranked with the
#: projects on GitHub: each one's address, its name (a post's is its title, as the post
#: gives it), its author as the record credits them, and what it holds. They are the
#: source-coverage register's two sources off GitHub that are not a catalogue,
#: UnitSquare's release and Wang and Li's Zenodo record, and the two posts behind
#: Burns's and Massaccesi's n = 17 bound, whose key the register credits with T-015 and
#: T-016 and the case records cite. A test holds every source the coverage register
#: reviews to a card, here or in `OTHER_PROJECTS`, and every address here and in
#: `CATALOGUE_SITES` to one the record cites.
OTHER_SITES: tuple[tuple[str, str, str, str], ...] = (
    (
        "https://github.com/jlevy/squares/issues/401#issuecomment-6031977107",
        "SQUISH packing of 153 squares",
        "Nate Chaoweeraprasit",
        "The supplemental rational certificate submitted with the SQUISH packings.",
    ),
    (
        "https://github.com/jlevy/squares/issues/401#issuecomment-6043191866",
        "SQUISH dated source follow-up",
        "Nate Chaoweeraprasit",
        (
            "Dated SQUISH update, including a pinned copy of the original rational "
            "n153 certificate."
        ),
    ),
    (
        "https://sam-burns.com/posts/proposing-better-lower-bound-for-n17-square-packing/",
        "Proposing a Better Lower Bound for n = 17 Square Packing",
        "Sam Burns",
        (
            "A weighted certificate for s(17) \u2265 4.4811, the method Massaccesi\u2019s"
            " bound builds on."
        ),
    ),
    (
        "https://gus-massa.blogspot.com/2026/08/another-better-lower-bound-for-n17.html",
        "Another Better Lower Bound for n = 17 Square Packing",
        "Gustavo Massaccesi",
        "s(17) \u2265 4.5058, by linear programming on Burns\u2019s certificate architecture.",
    ),
    (
        "https://doi.org/10.5281/zenodo.23038546",
        "Zenodo 23038546",
        "Ke Wang and Can Li",
        (
            "An exact lower bound for eleven squares, a reweighting of Kleddamag\u2019s"
            " certificate."
        ),
    ),
    (
        "https://hmbelvedere.com/",
        "UnitSquare",
        "the UnitSquare Project",
        (
            "Results Release 1, reported packings for six counts from n = 68 to 131, each"
            " since superseded."
        ),
    ),
)


def site_name(url: str) -> str | None:
    """A listed website's name, `None` for a repository on GitHub."""
    for address, name, _, _ in (*CATALOGUE_SITES, *OTHER_SITES):
        if address == url:
            return name
    return None


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

#: The mark for a website whose favicon is not saved in `PROJECT_FAVICONS`: a globe, a
#: circle crossed by one meridian and the equator, drawn in the text colour on GitHub's
#: mark's 16 units.
WEB_MARK = (
    '<svg class="site-link-icon" viewBox="0 0 16 16" aria-hidden="true" focusable="false">'
    '<g fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="8" cy="8" r="6.75"/>'
    '<ellipse cx="8" cy="8" rx="2.75" ry="6.75"/><path d="M1.25 8h13.5"/></g></svg>'
)

_FAVICON_TYPES = {".png": "image/png", ".svg": "image/svg+xml", ".ico": "image/x-icon"}


def link_icon(url: str) -> str:
    """The mark beside a project's address: GitHub's for a GitHub URL, otherwise the
    site's own favicon where one is saved in `PROJECT_FAVICONS`, and the globe,
    `WEB_MARK`, where none is. None is saved yet: the hosts the cards for websites name
    refused this project's sessions when the cards were added (2026-10-05), and a page
    fetches nothing, so a favicon arrives only as a saved file."""
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
    return WEB_MARK


def _breakable(address: str) -> str:
    """An address that may wrap after each slash rather than inside a name, and after
    the two slashes of an address it holds, an archived one's, not between them."""
    return "/<wbr>".join(_esc(part) for part in address.split("/")).replace(
        "/<wbr>/<wbr>", "//<wbr>"
    )


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
#: counts for it. The key of Burns's and Massaccesi's n = 17 bound names both authors
#: and both posts, so its results count for each.
PROJECT_EXTRA_KEYS: dict[str, tuple[str, ...]] = {
    "https://github.com/Guzhou0806/n17-square-packing": (
        "[n17 weighted certificates 2026-09-20]",
    ),
    "https://sam-burns.com/posts/proposing-better-lower-bound-for-n17-square-packing/": (
        "[Burns\u2013Massaccesi n17]",
    ),
    "https://gus-massa.blogspot.com/2026/08/another-better-lower-bound-for-n17.html": (
        "[Burns\u2013Massaccesi n17]",
    ),
}

#: Where a listed website's results are cited under a bibliography venue of their own:
#: every key with that `venue` counts for it, so a result a later intake of the
#: catalogue registers counts without an edit here. The catalogue's own key, `[Kingbird]`,
#: is the baseline and attributes no result; each registered packing it carries has a
#: key of its own whose venue is the catalogue (T-088 and T-089).
SOURCE_VENUES: dict[str, str] = {KINGBIRD: "Squares in Squares"}

#: The source-coverage register: each source repository the record reviews, with the
#: bibliography key its results are attributed under.
SOURCE_COVERAGE = FRONTIER / "source-coverage.yaml"


def project_urls() -> tuple[str, ...]:
    """Every listed project's address, the websites' first, in the order
    `CATALOGUE_SITES`, `OTHER_SITES` and `OTHER_PROJECTS` write them, which is not the
    order the page shows them in (`listed_projects`)."""
    return (
        *(url for url, _, _, _ in (*CATALOGUE_SITES, *OTHER_SITES)),
        *(url for url, _, _ in OTHER_PROJECTS),
    )


def project_name(url: str) -> str:
    """A project as the Project filter names it: a website by its name, and a repository
    as its owner and repository, `evand/square-packing`, since three of the repositories
    are called `square-packing`."""
    return site_name(url) or urlsplit(url).path.strip("/")


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
    the sources at its address, those `PROJECT_EXTRA_KEYS` adds, and every key whose
    venue is the project's in `SOURCE_VENUES`. A result is a project's where its
    `attribution.source_keys` names one of them."""
    coverage = safe_load(SOURCE_COVERAGE.read_text(encoding="utf-8"))["sources"]
    bibliography = safe_load(BIBLIOGRAPHY.read_text(encoding="utf-8"))["sources"]
    keys: dict[str, set[str]] = {
        url: set(PROJECT_EXTRA_KEYS.get(url, ())) for url in project_urls()
    }
    listed = {source_repository(url): url for url in keys}
    for source in coverage:
        url = listed.get(source_repository(source["url"]))
        if url is not None and source.get("source_key"):
            keys[url].add(source["source_key"])
    for url, venue in SOURCE_VENUES.items():
        keys[url] |= {entry["key"] for entry in bibliography if entry.get("venue") == venue}
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
    """A project's repository by its name alone."""
    return urlsplit(url).path.rstrip("/").rsplit("/", 1)[-1]


def project_headline(url: str) -> str:
    """A project card's headline: a website's name, or its repository's."""
    return site_name(url) or repository_name(url)


def headline_html(url: str) -> str:
    """`project_headline` as the card sets it: a website's name is prose, so a case it
    names (`n = 17`) is set as math; a repository's name is an identifier, set as it is."""
    name = site_name(url)
    return tex_bounds(name) if name else _esc(repository_name(url))


def _tallied(urls: Sequence[str], overview: Overview) -> dict[str, ProjectTally]:
    """Each of `urls`'s tally over the register, by its address."""
    slugs = {project_slug(url): url for url in urls}
    tallies = project_tallies(list(slugs), cited_results(overview), significance_levels())
    return {url: tallies[slug] for slug, url in slugs.items()}


def ranked_projects(overview: Overview) -> list[tuple[str, ProjectTally]]:
    """The projects the page ranks, every listed one but the catalogues, in the order it
    shows them (`project_order`), each with its tally: read from the register when the
    page is rendered, never kept by hand."""
    urls = [*(url for url, _, _, _ in OTHER_SITES), *(url for url, _, _ in OTHER_PROJECTS)]
    tallies = _tallied(urls, overview)
    slugs = {project_slug(url): url for url in urls}
    names = {slug: project_headline(url) for slug, url in slugs.items()}
    ordered = project_order({slug: tallies[url] for slug, url in slugs.items()}, names)
    return [(slugs[slug], tallies[slugs[slug]]) for slug in ordered]


def listed_projects(overview: Overview) -> list[tuple[str, ProjectTally]]:
    """Every card of the Other Square Packing Projects section in page order, each with
    its tally: the catalogues as `CATALOGUE_SITES` writes them, then `ranked_projects`."""
    catalogues = [url for url, _, _, _ in CATALOGUE_SITES]
    tallies = _tallied(catalogues, overview)
    return [(url, tallies[url]) for url in catalogues] + ranked_projects(overview)


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
    """One card per other project, website or repository, in `listed_projects`'s order:
    its name (`project_headline`), its author, what it holds and its address, and at its
    foot its tally of registered results (`project_tally`). Each card's link opens the
    project in a new tab. The note is prose like a page card's, so a case it names
    (`n = 21`) is set as math."""
    listed = {url: (author, note) for url, author, note in OTHER_PROJECTS} | {
        url: (author, note) for url, _, author, note in (*CATALOGUE_SITES, *OTHER_SITES)
    }
    cards = []
    for url, tally in listed_projects(overview):
        author, note = listed[url]
        cards.append(
            link_card(
                url,
                f"By {author}",
                headline_html(url),
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
    are the overview's PDFs and Videos section, after Recent Results."""
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

#: The atlas's three sizes of tile, in tab order: the key the block's `data-atlas-size`
#: and the address's `?size=` take, and the tab's label. Medium is the size the atlas had
#: before it offered a choice, the default and the one the page is rendered in; site.css
#: scales a tile by each (`--site-atlas-scale`), and `overview/atlas-view.js` rearranges
#: the tiles for it (think-ht8t).
ATLAS_SIZES: tuple[tuple[str, str], ...] = (
    ("small", "Small"),
    ("medium", "Medium"),
    ("large", "Large"),
)

#: The size the page is rendered in.
ATLAS_SIZE = "medium"

#: The id the script gives the box of tiles, which each view and size tab controls.
ATLAS_PANEL = "atlas-cells"

#: The word every regularized drawing carries: the label the layer's index says each of
#: its drawings must be shown with (`atlas_regularized`), which a regularized tile's name
#: and the atlas's key say in words. The regularized layer is the derived view
#: `atlas/known-best/regularized/` keeps for some cases (X-049, Exact Regularization).
ATLAS_REGULARIZED = "regularized"

#: Where a reader learns what a regularized view is: the atlas README's section on the
#: layer, which the atlas's key links.
ATLAS_REGULARIZED_README = REPO / "packing" / "atlas" / "known-best" / "README.md"


def atlas_layer_mark() -> str:
    """The regularized layer's badge: one dot in the accent, drawn by site.css and hidden
    from assistive technology, whose names say "regularized" in words. A regularized
    tile carries it before its number, and the atlas's key carries it before its words,
    so the key names the tiles' mark (`atlas_legend`)."""
    return '<span class="site-atlas-layer-mark" aria-hidden="true"></span>'


def atlas_star() -> str:
    """The new-result star on a tile: the site's one star (`STAR`, `.site-star`), as the
    frontier table's Recent column and the tables of results draw it, after the case's
    number. It is hidden from assistive technology because the tile's name ends with
    what it says, "new result" (`NEW_RESULT`), as a starred row's name does
    (`result_row`); the atlas's key says it in words (`atlas_legend`)."""
    return f'<span class="site-star" aria-hidden="true">{STAR}</span>'


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
    if index.get("label") != ATLAS_REGULARIZED:
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


def _atlas_cell(n: int, status: str, *, regularized: bool = False, new: bool = False) -> str:
    """One case's tile: its drawing, a link to its case record, and its number under it.

    A case with a regularized view is drawn from that view, the house renderer's picture
    of the record's frame straightened, reduced by `packing_svg` as a house drawing is;
    its tile says so in its name and carries the layer's badge before its number
    (`atlas_layer_mark`). The atlas showed the house drawing too, under a House tab,
    until 2026-10-04, when the owner dropped the choice (think-k8x9); the case record's
    own drawing is still the house one. A case whose verified lower bound is a new
    result, the frontier table's rule (`render_frontier_page.recent_lower_bounds`),
    carries the star after its number (`atlas_star`), and its name ends "new result"
    (think-wwtt).
    """
    from devtools import render_frontier_page as frontier  # noqa: PLC0415
    from devtools.render_case_pages import case_url  # noqa: PLC0415

    row = math.isqrt(n - 1) + 1
    square = " data-atlas-square" if row * row == n else ""
    position = (
        f' style="--r:{row};--c:{row * row - n};--o:{int(row > 1 and n == (row - 1) ** 2 + 1)}"'
    )
    drawing = frontier.drawing_img(n, regularized=regularized, size=ATLAS_UNITS)
    view = f", {ATLAS_REGULARIZED} view" if regularized else ""
    name = f"n = {n}{view}, {_esc(status)}{f', {NEW_RESULT}' if new else ''}"
    badge = atlas_layer_mark() if regularized else ""
    star = atlas_star() if new else ""
    return (
        f'<a class="site-atlas-cell" href="{case_url(n)}" data-case="{n}" '
        f'data-atlas-n="{n}"{square} '
        f'data-status="{_esc(status)}" aria-label="{name}"{position}>'
        f'{drawing}<span class="site-atlas-n">{badge}{n}{star}</span></a>'
    )


def _atlas_tablist(
    choices: Sequence[tuple[str, str]],
    *,
    default: str,
    ids: str,
    data: str,
    classes: str,
    name: str,
    extra: str = "",
) -> str:
    """One strip of the atlas's tabs: a tablist of buttons, `default` selected and the
    strip's one stop in the tab order, each controlling the static box of tiles."""
    tabs = "".join(
        f'<button type="button" role="tab" id="{ids}-{key}" {data}="{key}" '
        f'aria-selected="{"true" if key == default else "false"}" '
        f'aria-controls="{ATLAS_PANEL}"{"" if key == default else ' tabindex="-1"'}>'
        f"{_esc(label)}</button>"
        for key, label in choices
    )
    return (
        f'<div class="site-tabs {classes}" role="tablist" aria-label="{_esc(name)}" '
        f"{extra.rstrip()}>{tabs}</div>"
    )


def atlas_view_tabs() -> str:
    """The tabs over the atlas's tiles that choose its view, Grid or Triangle: the
    section tabs' strip (`.site-tabs`), but a tablist of two buttons that rearrange the
    one set of tiles in place, where the Visualize section's are links to two pages.

    The first view is selected and is the only tab in the page's tab order; the arrow
    keys move between the two (`overview/atlas-view.js`). The strip is present in the
    first response.
    """
    return _atlas_tablist(
        ATLAS_VIEWS,
        default=ATLAS_VIEWS[0][0],
        ids="atlas-view",
        data="data-atlas-tab",
        classes="site-atlas-views",
        name="Atlas layout",
        extra=f'data-atlas-views data-atlas-panel="{ATLAS_PANEL}" ',
    )


def atlas_size_tabs() -> str:
    """The tabs beside the view tabs that choose the size of the tiles, Small, Medium
    or Large (think-ht8t): the view tabs' strip, a tablist of three buttons that resize
    the one set of tiles in place, in either view. Medium is selected and is the strip's
    one stop in the tab order; the arrow keys move between the three
    (`overview/atlas-view.js`). The strip is present in the first response."""
    return _atlas_tablist(
        ATLAS_SIZES,
        default=ATLAS_SIZE,
        ids="atlas-size",
        data="data-atlas-size-tab",
        classes="site-atlas-sizes",
        name="Atlas tile size",
        extra="data-atlas-sizes ",
    )


def atlas_legend(*, regularized: bool) -> str:
    """The key to a tile's marks, under the atlas's tabs: the star, "new result", and,
    where some case is drawn from its regularized view, the layer's badge, "regularized
    view", linked to the atlas README's section on the layer. A star without a key reads
    as decoration, which is why each table of results keeps one (paper-design.md), and a
    regularized drawing is only ever shown labelled as one (the atlas README); the
    Regularized tab keyed the badge until the owner dropped the choice of drawing on
    2026-10-04 (think-k8x9). Each mark's words are a span of their own, as in the
    tables' legend (`rung_legend`): no shipped face carries the star. The key arrives
    with the static tiles and their controls."""
    star = (
        f'<span class="site-atlas-legend-item">{atlas_star()} <span>{NEW_RESULT}</span></span>'
    )
    view = (
        f' <span class="site-atlas-legend-item">{atlas_layer_mark()}'
        f'<a href="{branch_file(ATLAS_REGULARIZED_README, "#the-regularized-views")}">'
        f"{ATLAS_REGULARIZED} view</a></span>"
        if regularized
        else ""
    )
    return (
        '<p class="site-atlas-legend" role="note" '
        f'aria-label="What a tile{APOSTROPHE}s marks mean" data-atlas-legend>'
        f"{star}{view}</p>"
    )


def atlas_grid() -> str:
    """Every tracked case's known-best packing, n = 1 to 324, as a grid of drawings,
    each a link to its case record. With scripts, a cell opens the page's one case
    popover instead (`overview/case-popover.js`), which shows the case's record as its
    own page does: the visual summary, the drawing large and the bounds' number line,
    then the record's further data (`render_case_pages`, think-t21m).

    The block is rendered in the grid view (`data-atlas-view`), under tabs that switch
    it to the triangle (`atlas_view_tabs`). Both views are one set of tiles: the triangle
    uses positions supplied by the static markup and stylesheet, so a tile's markup is
    the same in both.
    A perfect square's tile is marked `data-atlas-square`: it ends its row of the
    triangle, on the right edge, and the triangle numbers it in the text's colour. The
    block is rendered at the medium size (`data-atlas-size`), under tabs beside the view
    tabs that make every tile smaller or larger (`atlas_size_tabs`), in either view.

    The first `ATLAS_FIRST` cells arrive as static markup with reserved, lazy-loaded
    SVG images; the rest are already present in a hidden container. The script shows
    them only when the reader presses the button under the grid, "Show More" with the
    double chevron down. The button then reads "Show Less" with the chevron up and
    collapses the grid again; its name for assistive
    technology says what each does and how many cases that is (`data-name-more`,
    `data-name-less`), it controls the box of tiles (`ATLAS_PANEL`), and it is the site's
    one action under a table or grid (`.site-action`, with "See all results"). Ordinary
    links give readers without scripting all case records and the frontier survey. The atlas
    popover, filled by the script from a JSON of the film's facts, stood after the block until
    2026-10-03; the case popover took its place.

    A case with a regularized view (`atlas_regularized`) is drawn from it, badged, and
    every other case from its house rendering: one tile a case. Until 2026-10-04 the
    house tiles were the default and a third `<template>` held a second tile for each
    regularized case, which House and Regularized tabs swapped in place; the owner
    dropped the choice for the regularized drawings alone (think-k8x9), and with it the
    second set. A case whose verified lower bound is a new result carries the star
    (think-wwtt). The two strips stand in one row over the tiles, the key to the marks
    under them (`atlas_legend`), all in one box (`.site-atlas-controls`), which the
    script places the tiles after.
    """
    from devtools import render_frontier_page as frontier  # noqa: PLC0415
    from devtools.render_case_pages import case_popover  # noqa: PLC0415

    cases = frontier.frontier_cases()
    tracked = {case["n"] for case in cases}
    regularized = atlas_regularized()
    if not set(regularized) <= tracked:
        untracked = sorted(set(regularized) - tracked)
        raise SystemExit(f"regularized views of untracked cases: {untracked}")
    new = frontier.recent_lower_bounds()
    cells = [
        _atlas_cell(
            case["n"],
            case["status"],
            regularized=case["n"] in regularized,
            new=new.get(case["n"], False),
        )
        for case in cases
    ]
    more, less = "Show More", "Show Less"
    name_more = f"Show more: all {len(cases)} cases"
    name_less = f"Show less: the first {ATLAS_FIRST}"
    return (
        f'<div class="site-wide site-atlas-grid" data-atlas-view="{ATLAS_VIEWS[0][0]}" '
        f'data-atlas-size="{ATLAS_SIZE}" data-atlas-grid>'
        '<div class="site-atlas-controls" data-atlas-controls>'
        f"{atlas_view_tabs()}{atlas_size_tabs()}"
        f"{atlas_legend(regularized=bool(regularized))}</div>"
        f'<div class="site-atlas-cells" id="{ATLAS_PANEL}">'
        f"{''.join(cells[:ATLAS_FIRST])}"
        '<div class="site-atlas-rest" data-atlas-rest hidden>'
        f"{''.join(cells[ATLAS_FIRST:])}</div></div>"
        '<noscript><p><a href="cases/">All case records</a> · '
        '<a href="frontier.html">Every packing and bound in the frontier '
        "survey</a></p></noscript>"
        # The triangle's one-line key ("Each row ends at a perfect square…") stood here
        # and the line under the expander ("Every case from n = 1 to 324 is also in the
        # frontier survey, and each has a case record.") after it, until 2026-10-02 (the
        # owner, think-l38m): each tile opens its case record, and the Frontier page is a
        # page card. The expander's row ends the block.
        '<p class="site-action-row site-atlas-toggle-row">'
        '<button type="button" class="site-action site-atlas-toggle" '
        f'data-atlas-toggle aria-expanded="false" aria-controls="{ATLAS_PANEL}" '
        f'aria-label="{name_more}" data-label-more="{more}" data-label-less="{less}" '
        f'data-name-more="{name_more}" data-name-less="{name_less}">'
        f"<span data-atlas-label>{more}</span>{arrow_icon('double-down')}</button></p>"
        f"</div>{case_popover()}"
    )
