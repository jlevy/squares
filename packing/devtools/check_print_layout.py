#!/usr/bin/env python3
"""Measure the explainer's print layout in the browser, and refuse what reads wrong.

Every other check this repository runs looks at the page on screen. The PDF is drawn
from the same document under `media: print`, and that block changes the inputs the rest
of the stylesheet computes from -- the base font size, the page margin -- and adds rules
that override the screen ones. So a print-only defect is invisible to every check we
have, and the three we shipped were all found by a human reading the finished PDF:

  * a colophon that came out left-aligned, because the print block's
    `.kpress p { text-align: left !important }` (0,2,0) beats the restatement meant to
    exempt it, `.colophon { text-align: center !important }` (0,1,0);
  * a list bullet sitting at the baseline, because its `top` is a multiple of
    `--kpress-font-size-base`, which the print block redefines;
  * a footnote reference wrapping onto a line of its own.

None of the three is a divergence between Chromium and CSS. Chromium applied exactly the
cascade we wrote; we had just never looked at what that cascade computes under `print`.
This looks.

The waiting is the PDF exporter's, deliberately: a check that measures a differently
settled page than the one that gets drawn is measuring a document nobody reads.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import TypedDict

from playwright.sync_api import ViewportSize

from devtools.render_explainer_pdf import BROWSER_OVERRIDE, PAGE, READY


class Centred(TypedDict):
    """One element's alignment, in one medium. `index` and `parent` line the two up."""

    index: int
    parent: int
    path: str
    align: str
    declared: bool
    shown: bool


class Marker(TypedDict):
    """A list marker's box against the line box it belongs to."""

    path: str
    markerCentre: float
    lineCentre: float
    fontSize: float
    lineHeight: float


class Footnote(TypedDict):
    """How much of a footnote reference's own line lies in front of it."""

    path: str
    text: str
    leadIn: float
    fontSize: float


class Boxed(TypedDict):
    """Text against the box drawn around it, for a control that is a box and a label."""

    path: str
    text: str
    offset: float


class Overflow(TypedDict):
    """A block reaching past the measure, where the paper will clip rather than wrap."""

    path: str
    over: float
    text: str


class Probe(TypedDict):
    """Everything one pass measures, plus the column it measured at."""

    centred: list[Centred]
    markers: list[Marker]
    footnotes: list[Footnote]
    boxed: list[Boxed]
    overflow: list[Overflow]
    #: How far the document's layout reaches past the page, and the run that reaches
    #: farthest. Not clipped: Chromium scales the whole document to fit it.
    pageOverflow: float
    widest: Overflow | None
    measure: float
    viewport: float


class Measured(TypedDict):
    """The two passes, taken from one browser and one load of the page."""

    screen: Probe
    print: Probe


#: One CSS pixel, which at the print body size is six percent of an em: well under what
#: reads as misaligned, well over the rounding in a font's own metrics. The bullet defect
#: was 1.9px, so this catches it with room to spare. Not tighter, because the two sides of
#: the comparison are built differently -- a marker box against a line box -- and half a
#: pixel is finer than that construction is self-consistent to.
TOLERANCE_PX = 1.0

#: Half of that, for a label against the box drawn around it. Tighter because the
#: measurement is tighter: both sides are rects from one layout, with none of the
#: marker check's mismatch between a marker box and a line box. It has to be tighter to
#: be worth having -- the chips shipped 0.65px off and a reader saw it, which a
#: one-pixel tolerance would have called clean.
BOXED_TOLERANCE_PX = 0.5

#: The measure the PDF actually has, in CSS pixels. `emulate_media` switches which media
#: queries match; it does not paginate and it does not apply the `@page` box. So the
#: default 1280px viewport leaves the column at whatever `--kpress-measure` caps it to --
#: 720px here -- and every horizontal question is asked of a page 25% wider than the one
#: that gets printed. Letter is 816 x 1056px at 96dpi; the stylesheet's margin is 1.25in,
#: so the column is 816 - 2 * 120.
PRINT_VIEWPORT: ViewportSize = {"width": 816 - 2 * 120, "height": 1056 - 2 * 120}

#: What each media's probe returns. Written as one script so the two passes cannot drift
#: apart: the whole point is comparing like with like across `emulateMedia`.
_PROBE = r"""() => {
  const out = {
    centred: [], markers: [], footnotes: [], boxed: [], overflow: [],
    pageOverflow: 0, widest: null,
    /* Named so a viewport that did not take is visible in the output rather than
       silently making every horizontal answer wrong. */
    measure: document.querySelector('.kpress')?.getBoundingClientRect().width ?? 0,
    viewport: document.documentElement.clientWidth,
  };

  /* Centring. `.centred` is the page's declaration that a block is centred in every
     medium, so it is also the thing to hold it to; nothing else here needs a list of
     intents. Everything with text of its own is recorded as well, for `--all`: that
     sweep is how the colophon was found, before there was a class to check.

     `text-align` inherits, so each row names its parent's row. Without that a single
     lost centring is reported once for the block and once more for every span, link
     and KaTeX node beneath it, and the cause is buried in its own consequences. */
  const seen = new Map();
  for (const el of document.querySelectorAll('.kpress, .kpress *')) {
    if (!el.textContent.trim()) continue;
    seen.set(el, out.centred.length);
    out.centred.push({
      index: out.centred.length,
      parent: seen.has(el.parentElement) ? seen.get(el.parentElement) : -1,
      path: sig(el),
      align: getComputedStyle(el).textAlign,
      declared: el.classList.contains('centred'),
      /* Whether the element is laid out at all in this medium. `screen-only` blocks are
         `display: none` under print and still report an inherited `text-align`, so
         without this every one of them is a finding about a box nobody prints. */
      shown: el.getClientRects().length > 0,
    });
  }

  /* Markers. The list bullet is not a `::marker`: kpress sets `list-style-type: none`
     and draws an absolutely positioned `::before`, so there is no marker box to
     measure. Its top edge is the `li`'s content-box top plus the pseudo-element's own
     `top`, and its height is its line box, which is what `lineHeight` computes to. The
     line it should sit on is the `li`'s first line box, taken as a Range over the first
     text node rather than as the `li`'s own box, which spans every line. */
  for (const li of document.querySelectorAll('.kpress li')) {
    const before = getComputedStyle(li, '::before');
    const own = getComputedStyle(li);
    /* `top` is measured from the containing block's padding edge, and the containing
       block is the `li` only while it is positioned. If kpress ever drops that, the
       offset is against something else and this arithmetic would quietly measure the
       wrong box, so the case is skipped rather than guessed at. */
    if (before.content === 'none' || before.position !== 'absolute') continue;
    if (own.position === 'static') continue;
    const line = firstLineBox(li);
    if (!line) continue;
    const box = li.getBoundingClientRect();
    const edge = parseFloat(own.borderTopWidth) || 0;
    const top = box.top + edge + (parseFloat(before.top) || 0);
    const height =
      parseFloat(before.height) || parseFloat(before.lineHeight) ||
      parseFloat(before.fontSize) || 0;
    out.markers.push({
      path: sig(li),
      markerCentre: round(top + height / 2),
      lineCentre: round((line.top + line.bottom) / 2),
      fontSize: round(parseFloat(before.fontSize)),
      lineHeight: round(height),
    });
  }

  /* Footnote references. A reference that opens a line has been cut off from the
     sentence it marks, which is what a reader reported: a line ending in the formula and
     a bare "3" on the next.

     Measured as how much of the reference's own line lies before it. Two earlier
     definitions were wrong and both read clean on a document that was not: comparing the
     reference's top against the preceding text's top misses the case where the wrap falls
     before a full stop, because the stop then travels down with the reference and the two
     agree; and a Range's `getClientRects` returns one rect per box rather than per line,
     so its last rect is the single character before the reference and is always narrow.
     The line's extent is the union of every rect that vertically overlaps that last one.
     Verified on a reproduction: the corrected form fires at 20 of 310 column widths where
     both earlier ones fired at none. */
  for (const sup of document.querySelectorAll('sup.kpress-footnote-ref')) {
    const block = sup.closest('p, li, dd, figcaption, td, th');
    if (!block) continue;
    const before = document.createRange();
    before.setStart(block, 0);
    before.setEndBefore(sup);
    const rects = [...before.getClientRects()].filter((r) => r.width && r.height);
    if (!rects.length) continue;
    const tail = rects[rects.length - 1];
    const line = rects.filter((r) => r.bottom > tail.top + 0.5 && r.top < tail.bottom - 0.5);
    const ahead = line.length
      ? Math.max(...line.map((r) => r.right)) - Math.min(...line.map((r) => r.left))
      : 0;
    out.footnotes.push({
      path: sig(sup),
      text: block.textContent.trim().slice(0, 60),
      /* The width of its own line that precedes it. Near zero and it opens the line. */
      leadIn: round(ahead),
      fontSize: round(parseFloat(getComputedStyle(block).fontSize)),
    });
  }

  /* Boxed labels: a control whose whole design is a word inside a border, where the
     word being off the border's centre is the defect. Measured against the box rather
     than against a line, because there is only one line and the box is what a reader
     sees it against.

     The chips shipped 0.65px high, from `line-height: 1` on a font whose content area is
     taller than one em: the half-leading goes negative and negative leading is not shared
     the way positive leading is. Nothing here computes a marker or a line, so none of the
     checks above could have seen it. */
  for (const chip of document.querySelectorAll('.doc-links .chip')) {
    const box = chip.getBoundingClientRect();
    const text = [...chip.childNodes].find((n) => n.nodeType === 3 && n.textContent.trim());
    if (!text || !box.height) continue;
    const range = document.createRange();
    range.selectNodeContents(text);
    const ink = range.getBoundingClientRect();
    if (!ink.height) continue;
    out.boxed.push({
      path: sig(chip),
      text: text.textContent.trim().slice(0, 20),
      /* Positive when the label sits below the centre of the box drawn around it. */
      offset: round((ink.top + ink.bottom) / 2 - (box.top + box.bottom) / 2),
    });
  }

  /* Overflow. The measure is set by the `@page` margin, so a block reaching past the
     body's content box is wrapped wrongly or cut. Figures are allowed their own scroll
     on screen and are excluded by the same class the stylesheet uses to let them. */
  const page = document.querySelector('.kpress');
  if (page) {
    const room = page.getBoundingClientRect();
    for (const el of page.querySelectorAll('p, li, h1, h2, h3, h4, figcaption, blockquote')) {
      const box = el.getBoundingClientRect();
      if (!box.width) continue;
      const over = round(Math.max(room.left - box.left, box.right - room.right));
      if (over > 1) {
        out.overflow.push({path: sig(el), over, text: el.textContent.trim().slice(0, 60)});
      }
    }
  }

  /* The whole page. An unclipped run past the page box is not cut at the paper's edge:
     Chromium scales the entire document down until it fits, and every size on every
     page shrinks with it, silently. One display equation 42px too wide printed a 12pt
     document at 11.2pt and nothing here saw it, because the blocks above are column
     boxes and the run that overflowed was inline content inside one. The document's own
     scroll width is what Chromium fits, so that is what is measured, with the widest
     unclipped run named so the finding says what to shrink. */
  const root = document.documentElement;
  out.pageOverflow = round(root.scrollWidth - root.clientWidth);
  if (out.pageOverflow > 1) out.widest = widestRun(root);

  return out;

  function round(v) { return Math.round((v || 0) * 100) / 100; }

  /* The run that reaches farthest past the page, among the runs that can put it there.
     Among: a box whose ink an ancestor clips away has nothing past that ancestor's edge
     and cannot widen the document, so naming it sends the author to shrink something
     that was never the cause.

     KaTeX writes a full MathML transcription of every formula into a `.katex-mathml`
     span that is 1px square with `overflow: hidden` and `clip: rect(1px, 1px, 1px,
     1px)`, and the boxes inside it keep their natural width. On this page, printed at
     576px, the tau* equation's `mrow` reports a 236.77px overhang while the document's
     own scroll width equals the page's: nothing overflows, and the first form of this
     scan named that mrow anyway, the moment anything else made the page overflow.

     So cut each candidate's right edge back to what its clipping ancestors leave
     visible. General rather than a class name, because the same thing is true of a
     figure given its own scroll -- it does not widen the page either, and if it did the
     scrolling box would be the culprit, not its contents. SVG internals stay excluded
     outright: their user units are not the page's pixels. */
  function widestRun(root) {
    let widest = null;
    for (const el of document.querySelectorAll('.kpress *')) {
      if (el.closest('svg')) continue;
      const box = el.getBoundingClientRect();
      /* Ink never reaches past the box, so the ancestor walk is only worth its cost
         where the box itself is past the edge. */
      if (!box.width || box.right - root.clientWidth <= 1) continue;
      const over = round(inkRight(el) - root.clientWidth);
      if (over > 1 && (!widest || over > widest.over)) {
        widest = {path: sig(el), over, text: el.textContent.trim().slice(0, 60)};
      }
    }
    return widest;
  }

  /* How far right an element's ink actually reaches: its own right edge, cut back by
     every ancestor that clips it. The clip is taken as the ancestor's border box, which
     is exact for the `overflow` cases and an over-estimate for `clip` and `clip-path` --
     the wrong way for a false name to survive, and the KaTeX wrapper's rect clip is its
     border box to within a pixel anyway.

     Out-of-flow boxes are not cut by boxes they are not laid out inside: an absolutely
     positioned one escapes until its containing block, a fixed one escapes the lot.
     `.katex-mathml` is itself absolute inside a relative `.katex`, so getting this wrong
     in the other direction would exclude everything under a positioned ancestor. */
  function inkRight(el) {
    let right = el.getBoundingClientRect().right;
    let position = getComputedStyle(el).position;
    for (let node = el.parentElement; node; node = node.parentElement) {
      const style = getComputedStyle(node);
      const containing = style.position !== 'static';
      if (position === 'fixed' || (position === 'absolute' && !containing)) continue;
      if (style.overflowX !== 'visible' || style.clip !== 'auto' || style.clipPath !== 'none') {
        right = Math.min(right, node.getBoundingClientRect().right);
      }
      position = style.position;
    }
    return right;
  }

  /* A name for an element that is stable across the two passes and readable in a
     failure: the tag, its classes, and its index among its siblings. */
  function sig(el) {
    const steps = [];
    for (let node = el, depth = 0; node && depth < 3; node = node.parentElement, depth++) {
      const parent = node.parentElement;
      const nth = parent ? [...parent.children].indexOf(node) : 0;
      const cls = [...node.classList].join('.');
      steps.unshift(`${node.tagName.toLowerCase()}${cls ? '.' + cls : ''}[${nth}]`);
      if (node.classList.contains('kpress')) break;
    }
    return steps.join(' > ');
  }

  /* The block's first line box: every rect a Range over its whole contents puts on the
     topmost line, unioned. Taken this way rather than as one text node's rect, which is
     that run's inline box and is shorter than the line whenever anything taller -- a
     KaTeX span, a larger inline -- shares the line with it. Comparing a marker box
     against an inline box that is not the line box is comparing two different things,
     and the difference was 3px.

     The mass-condition bullets have inline tops at -1, 0, 2 and 3px, because each
     run's box is its own font's ascent above the shared baseline: PT Serif's is 1.04em
     and KaTeX_Main's 0.90em. A one-pixel band kept only the highest math run and
     falsely reported a 2.2px marker offset. Group runs starting in the topmost rect's
     upper half; the next line starts a full line height below it.

     A zero-line-height footnote is raised without enlarging that line, but its ink
     still appears in Range rects. Remove its owned rectangles before grouping, not
     other inline boxes that really can enlarge the line. Count duplicate rectangles
     so an unrelated box with the same geometry is not removed along with the ref. */
  function firstLineBox(el) {
    const range = document.createRange();
    range.selectNodeContents(el);
    const excluded = new Map();
    const key = (r) => [r.top, r.right, r.bottom, r.left].join(',');
    for (const ref of el.querySelectorAll('sup.kpress-footnote-ref')) {
      if (parseFloat(getComputedStyle(ref).lineHeight) !== 0) continue;
      const reference = document.createRange();
      reference.selectNode(ref);
      for (const rect of reference.getClientRects()) {
        if (!rect.width || !rect.height) continue;
        const id = key(rect);
        excluded.set(id, (excluded.get(id) || 0) + 1);
      }
    }
    const rects = [...range.getClientRects()].filter((r) => {
      if (!r.width || !r.height) return false;
      const id = key(r);
      const count = excluded.get(id) || 0;
      if (!count) return true;
      excluded.set(id, count - 1);
      return false;
    });
    if (!rects.length) return null;
    const topmost = rects.reduce((a, r) => (r.top < a.top ? r : a));
    const band = rects.filter((r) => r.top < topmost.top + topmost.height / 2);
    return {
      top: Math.min(...band.map((r) => r.top)),
      bottom: Math.max(...band.map((r) => r.bottom)),
    };
  }
}"""


#: Two frames, so the media switch and the viewport change have both been laid out
#: before anything is measured. `evaluate` alone does not guarantee a flush after
#: `emulate_media`, and a rect read from the previous layout is the classic flake here.
_SETTLED = """() => new Promise(
  (done) => requestAnimationFrame(() => requestAnimationFrame(done)),
)"""

#: What `--self-check` puts in front of the gate, and what it holds the gate to naming.
#: 42px is the overflow the display equation shipped with, and the number the reviewer
#: reproduced this defect at: in a 576px print column it is a 618px block, and Chromium
#: would print the whole document at 93.2%.
SELF_CHECK_PX = 42.0
SELF_CHECK_CLASS = "print-layout-self-check"

#: A block the print column cannot contain, appended to the page. Given its margins and
#: its width outright, because the column centres its blocks and caps their measure: a
#: block merely handed a width comes back centred at half the overhang, which is how the
#: first draft of this control quietly measured nothing.
_OVERSHOOT = r"""(spec) => {
  const root = document.documentElement;
  const page = document.querySelector('.kpress');
  if (!page) throw new Error('no .kpress column to overflow');
  const el = document.createElement('div');
  el.className = spec.name;
  el.textContent = 'print layout self-check';
  el.style.setProperty('margin', '0', 'important');
  el.style.setProperty('max-width', 'none', 'important');
  page.appendChild(el);
  /* Measured after insertion rather than assumed: the width that overhangs the page by
     `over` is the one that reaches `over` past it from wherever the column starts. */
  const start = el.getBoundingClientRect().left;
  el.style.setProperty('width', `${root.clientWidth + spec.over - start}px`, 'important');
}"""


def measure(page_url: str, *, inject: str | None = None, spec: object = None) -> Measured:
    """The probe's answer under each medium, from one browser and one load.

    `inject` runs in the print pass, after the media switch and the viewport change and
    before the probe, which is the only place a deliberate print-layout defect can be put
    where the print measurement will see it. Nothing but `--self-check` passes one.
    """
    import os  # noqa: PLC0415

    from playwright.sync_api import sync_playwright  # noqa: PLC0415

    with sync_playwright() as driver:
        browser = driver.chromium.launch(executable_path=os.environ.get(BROWSER_OVERRIDE))
        try:
            page = browser.new_page()
            page.emulate_media(media="screen", reduced_motion="reduce")
            page.goto(page_url, wait_until="load")
            page.wait_for_selector(READY, timeout=60_000)
            page.evaluate("document.fonts.ready")
            screen: Probe = page.evaluate(_PROBE)
            page.emulate_media(media="print", reduced_motion="reduce")
            page.set_viewport_size(PRINT_VIEWPORT)
            page.evaluate("document.fonts.ready")
            if inject is not None:
                page.evaluate(inject, spec)
            page.evaluate(_SETTLED)
            printed: Probe = page.evaluate(_PROBE)
            return {"screen": screen, "print": printed}
        finally:
            browser.close()


def findings(measured: Measured, *, every: bool = False) -> list[str]:
    """Everything the two passes say is wrong, as lines a reader can act on."""
    screen = measured["screen"]
    printed = measured["print"]
    found: list[str] = []

    # `.centred` is the page's declaration that a block is centred in every medium, so
    # it is the thing to hold it to. Everything here runs in both media: a defect that is
    # wrong on screen too is still a defect, and two of these were.
    for medium, probe in (("screen", screen), ("print", printed)):
        found.extend(
            f"{medium}: `.centred` block is `{row['align']}`, not centred ({row['path']})"
            for row in probe["centred"]
            if row["declared"] and row["shown"] and row["align"] != "center"
        )
        found.extend(
            f"{medium}: list marker off the line's centre by "
            f"{row['markerCentre'] - row['lineCentre']:+.2f}px "
            f"({row['path']}, {row['fontSize']}px on a {row['lineHeight']}px line)"
            for row in probe["markers"]
            if abs(row["markerCentre"] - row["lineCentre"]) > TOLERANCE_PX
        )
        # Under one em there is no word in front of the reference, only stray punctuation
        # that wrapped down with it, and it reads as opening the line.
        found.extend(
            f"{medium}: footnote reference opens its line, with only "
            f"{row['leadIn']:.2f}px in front of it ({row['path']}: {row['text']!r})"
            for row in probe["footnotes"]
            if row["leadIn"] < row["fontSize"]
        )
        found.extend(
            f"{medium}: label sits {row['offset']:+.2f}px off the centre of its own box "
            f"({row['path']}: {row['text']!r})"
            for row in probe["boxed"]
            if abs(row["offset"]) > BOXED_TOLERANCE_PX
        )
        found.extend(
            f"{medium}: {row['path']} runs {row['over']:.2f}px past the measure "
            f"({row['text']!r})"
            for row in probe["overflow"]
        )

    # The page as a whole, in print only: on screen a wide run scrolls, on paper it
    # shrinks the document. Reported with the scale Chromium would apply, which is the
    # number a reader of the PDF would otherwise have to infer from the type size.
    if printed["pageOverflow"] > TOLERANCE_PX:
        scale = printed["viewport"] / (printed["viewport"] + printed["pageOverflow"])
        widest = printed["widest"]
        where = f"; the widest run is {widest['path']} ({widest['text']!r})" if widest else ""
        found.append(
            f"print: the document is {printed['pageOverflow']:.0f}px wider than the page, "
            f"so Chromium prints every page scaled to {scale:.1%}{where}"
        )

    if not every:
        return found

    # The sweep, for exploring, and not a failure: the print block left-aligns figure
    # captions on purpose, so every caption in the document answers to it. This is how
    # the colophon was found, before there was a class to check.
    was = {row["index"]: row["align"] for row in screen["centred"]}
    lost = {
        row["index"]
        for row in printed["centred"]
        if row["shown"] and was.get(row["index"]) == "center" and row["align"] != "center"
    }
    # Only where the change starts. An element under one that also lost centring
    # inherited the loss and is a symptom of the same rule, not a second finding.
    found.extend(
        f"centring lost in print: {row['path']} is `center` on screen "
        f"and `{row['align']}` in print"
        for row in printed["centred"]
        if row["index"] in lost and row["parent"] not in lost
    )

    return found


def self_check(page_url: str) -> int:
    """Put a known overflow in front of the gate, and hold the gate to naming it.

    A check that has only ever passed cannot tell itself apart from one that cannot fail,
    and this one has a second way to be useless: it can fail loudly at the right size and
    still name the wrong element, which sends the author to shrink a formula that is not
    the cause. That is what it shipped doing. So the control checks all three of what the
    finding says -- the overflow, the scale, and the culprit -- against an overflow this
    puts there itself.

    A browser is the only place this can be established: what makes the reported culprit
    wrong is real layout, a MathML subtree at its natural width inside a 1px clipping
    wrapper, and no retained measurement can be trusted to still be what the page does.
    The unit tests beside this run the scan over rectangles retained from here.
    """
    measured = measure(
        page_url,
        inject=_OVERSHOOT,
        spec={"over": SELF_CHECK_PX, "name": SELF_CHECK_CLASS},
    )
    printed = measured["print"]
    column = printed["viewport"]
    print(
        f"self-check: a {column + SELF_CHECK_PX:.0f}px block in a {column:.0f}px print column, "
        f"expected to overflow the page by {SELF_CHECK_PX:.0f}px"
    )
    found = findings(measured)
    for line in found:
        print(f"self-check: {line}")

    widest = printed["widest"]
    scale = f"{column / (column + SELF_CHECK_PX):.1%}"
    wrong: list[str] = []
    if abs(printed["pageOverflow"] - SELF_CHECK_PX) > TOLERANCE_PX:
        wrong.append(
            f"the page overflows by {printed['pageOverflow']:.2f}px, not {SELF_CHECK_PX:.0f}px"
        )
    if not any(line.startswith("print: the document is") for line in found):
        wrong.append("the gate did not report the document as wider than the page")
    if not any(f"scaled to {scale}" in line for line in found):
        wrong.append(f"the gate did not report the print scale as {scale}")
    if widest is None:
        wrong.append("the gate named no culprit at all")
    elif SELF_CHECK_CLASS not in widest["path"]:
        wrong.append(
            f"the gate named {widest['path']} ({widest['over']:.2f}px over) rather than the "
            f"block it was handed; a clipped subtree cannot widen the page"
        )
    elif abs(widest["over"] - SELF_CHECK_PX) > TOLERANCE_PX:
        wrong.append(
            f"the named culprit overhangs by {widest['over']:.2f}px, not {SELF_CHECK_PX}"
        )

    for line in wrong:
        print(f"self-check failed: {line}")
    if wrong:
        return 1
    print(
        f"self-check passed: the gate fails on a {SELF_CHECK_PX:.0f}px overflow, reports the "
        f"{scale} scale, and names the block that caused it"
    )
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--page", type=Path, default=PAGE, help="the rendered page to measure")
    parser.add_argument("--json", action="store_true", help="print the raw measurements")
    parser.add_argument(
        "--all",
        action="store_true",
        help="also report every block centred on screen and not in print",
    )
    parser.add_argument(
        "--self-check",
        action="store_true",
        help="overflow the print column on purpose, and check the gate fails and names it",
    )
    args = parser.parse_args(argv)

    if not args.page.is_file():
        raise SystemExit(f"{args.page}: no rendered page; run `render_explainer` first")

    if args.self_check:
        return self_check(args.page.resolve().as_uri())

    measured = measure(args.page.resolve().as_uri())
    if args.json:
        print(json.dumps(measured, indent=2, sort_keys=True))
        return 0

    found = findings(measured, every=args.all)
    for line in found:
        print(line)
    counts = measured["print"]
    declared = sum(1 for row in counts["centred"] if row["declared"])
    print(
        f"measured {len(counts['centred'])} blocks ({declared} declared `.centred`), "
        f"{len(counts['markers'])} list markers, {len(counts['footnotes'])} footnote "
        f"references and {len(measured['screen']['boxed'])} boxed labels in each medium; "
        f"print column {counts['measure']:.0f}px in a {counts['viewport']:.0f}px page"
    )
    if found:
        print(f"{len(found)} print-layout findings")
        return 1
    print("print layout clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())
