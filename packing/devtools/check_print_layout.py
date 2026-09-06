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
    overflow: list[Overflow]
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
    centred: [], markers: [], footnotes: [], overflow: [],
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

  /* Overflow. The measure is set by the `@page` margin, so anything reaching past the
     body's content box will be clipped at the paper's edge rather than wrapped. Figures
     are allowed their own scroll on screen and are excluded by the same class the
     stylesheet uses to let them. */
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

  return out;

  function round(v) { return Math.round((v || 0) * 100) / 100; }

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

  /* The block's first line box: every rect a Range over its whole contents puts in the
     topmost band, unioned. Taken this way rather than as one text node's rect, which is
     that run's inline box and is shorter than the line whenever anything taller -- a
     KaTeX span, a larger inline -- shares the line with it. Comparing a marker box
     against an inline box that is not the line box is comparing two different things,
     and the difference was 3px. */
  function firstLineBox(el) {
    const range = document.createRange();
    range.selectNodeContents(el);
    const rects = [...range.getClientRects()].filter((r) => r.width && r.height);
    if (!rects.length) return null;
    const first = Math.min(...rects.map((r) => r.top));
    const band = rects.filter((r) => Math.abs(r.top - first) < 1);
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


def measure(page_url: str) -> Measured:
    """The probe's answer under each medium, from one browser and one load."""
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
            f"{medium}: {row['path']} runs {row['over']:.2f}px past the measure "
            f"({row['text']!r})"
            for row in probe["overflow"]
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


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--page", type=Path, default=PAGE, help="the rendered page to measure")
    parser.add_argument("--json", action="store_true", help="print the raw measurements")
    parser.add_argument(
        "--all",
        action="store_true",
        help="also report every block centred on screen and not in print",
    )
    args = parser.parse_args(argv)

    if not args.page.is_file():
        raise SystemExit(f"{args.page}: no rendered page; run `render_explainer` first")

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
        f"{len(counts['markers'])} list markers and {len(counts['footnotes'])} footnote "
        f"references in each medium; print column "
        f"{counts['measure']:.0f}px in a {counts['viewport']:.0f}px page"
    )
    if found:
        print(f"{len(found)} print-layout findings")
        return 1
    print("print layout clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())
