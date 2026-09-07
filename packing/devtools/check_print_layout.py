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
The same browser also exercises Figure 5 after those measurements, including its
certificate controls, feedback, field cache, and layout at desktop and phone widths.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections.abc import Sequence
from fractions import Fraction
from pathlib import Path
from typing import NotRequired, TypedDict

from playwright.sync_api import CDPSession, Locator, Page, ViewportSize

from devtools.render_explainer import WALKTHROUGH
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
    measure: float
    viewport: float


class Measured(TypedDict):
    """The two passes, taken from one browser and one load of the page."""

    screen: Probe
    print: Probe
    controls: NotRequired[list[str]]


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

  /* The block's first line box: every rect a Range over its whole contents puts on the
     topmost line, unioned. Taken this way rather than as one text node's rect, which is
     that run's inline box and is shorter than the line whenever anything taller -- a
     KaTeX span, a larger inline -- shares the line with it. Comparing a marker box
     against an inline box that is not the line box is comparing two different things,
     and the difference was 3px.

     The mass-condition bullets have inline tops at -1, 0, 2 and 3px. A one-pixel band
     kept only the highest math run and falsely reported a 2.2px marker offset. Group
     runs starting in the topmost rect's upper half; the next line starts below it.

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


#: Geometry and computed type sizes, rather than a match on the stylesheet that
#: intended them. The active certificate is checked at each screen width.
_PROVER_LAYOUT = r"""() => {
  const found = [];
  for (const figure of document.querySelectorAll('figure[data-figure="5"]')) {
    if (!figure.getClientRects().length) continue;
    const panel = figure.querySelector('.panel');
    const stage = figure.querySelector('.stage');
    if (panel.getBoundingClientRect().top < stage.getBoundingClientRect().bottom - 1)
      found.push('control panel is beside the graphic');
    const {left, right} = panel.getBoundingClientRect();
    for (const item of figure.querySelectorAll('.math-item')) {
      if (getComputedStyle(item).whiteSpace !== 'nowrap')
        found.push('a direction item permits an internal line break');
      const ink = item.querySelector('.katex-html') || item;
      const box = ink.getBoundingClientRect();
      if (box.left < left - 1 || box.right > right + 1)
        found.push('a direction item overflows the control panel');
      const math = item.querySelector('.katex');
      if (math && math.querySelector('.mfrac')) fraction(math, 'half-tangent');
    }
    if (!figure.querySelector('.math-item')) found.push('direction items are missing');
    fraction(figure.querySelector('.mass-val .katex'), 'mass');
    for (const hidden of figure.querySelectorAll('[hidden]')) {
      if (hidden.getClientRects().length)
        found.push('a hidden status or verdict still occupies a visible box');
    }
  }
  return found;

  function fraction(mass, label) {
    const digits = [...mass.querySelectorAll('.katex-html .mfrac .mord')]
      .filter(el => !el.children.length && /[0-9]/.test(el.textContent));
    const size = parseFloat(getComputedStyle(mass).fontSize);
    if (!digits.length || digits.some(
        el => parseFloat(getComputedStyle(el).fontSize) < size * .95))
      found.push(`the ${label} fraction has reduced-size numerator or denominator`);
  }
}"""


def prover_findings(page: Page) -> list[str]:
    """Exercise Figure 5 through its public controls in the already open browser.

    A bitmap comparison follows two paths to the same state: restore a field after
    changing direction while it was hidden, then rebuild it at that direction. A
    stale cache differs. Neither path reads the page's private geometric variables.
    These checks run after the print measurements, so their interaction cannot change
    the state whose print layout is being inspected.
    """
    page.emulate_media(media="screen", reduced_motion="reduce")
    page.set_viewport_size({"width": 1280, "height": 900})
    page.evaluate(_SETTLED)
    slugs: list[str] = page.locator(".cert-figure").evaluate_all(
        "els => [...new Set(els.map(el => el.dataset.cert))]"
    )
    if not slugs:
        return ["Figure 5: no certificate figures were found"]
    records = (json.loads(path.read_text("utf-8")) for path in WALKTHROUGH)
    known_minima = {
        record["outer_side"].replace("/", "-"): Fraction(record["least_cell_mass"])
        for record in records
    }
    found: list[str] = []
    for slug in slugs:
        prefix = f"Figure 5 ({slug}): "
        page.locator(
            f'figure[data-figure="5"] .cert-toggle button[data-cert="{slug}"]:visible'
        ).click()
        selection: bool = page.evaluate(
            """slug => [...document.querySelectorAll('.cert-figure')].every(
              el => el.hidden === (el.dataset.cert !== slug)) &&
              [...document.querySelectorAll('.cert-toggle button')].every(
              el => el.getAttribute('aria-pressed') === String(el.dataset.cert === slug))
              && location.hash === '#' + slug""",
            slug,
        )
        if not selection:
            found.append(prefix + "certificate visibility, selection, and URL disagree")
        focused: bool = page.evaluate(
            """slug => document.activeElement.matches('.cert-toggle button') &&
              document.activeElement.dataset.cert === slug &&
              document.activeElement.getClientRects().length > 0""",
            slug,
        )
        if not focused:
            found.append(prefix + "certificate switching leaves focus on a hidden control")
        figure = page.locator(f'.cert-figure[data-cert="{slug}"] figure[data-figure="5"]')
        if figure.count() != 1 or not figure.is_visible():
            found.append(prefix + "the selected certificate has no visible prover")
            continue
        reset = figure.locator(f"#btn-tight-{slug}")
        scan = figure.locator(f"#btn-scan-{slug}")
        field = figure.locator(f"#btn-heat-{slug}")
        slider = figure.locator(f"#kslider-{slug}")
        status = figure.locator(f"#status-{slug}")
        hint = figure.locator(f"#hint-{slug}")
        canvas = figure.locator("canvas")
        verdict = figure.locator(f"#vd-{slug}")
        instruction = hint.inner_text()
        initial_bitmap: str = canvas.evaluate("el => el.toDataURL()")
        if slider.input_value() == "0" or _control_angle(slider, prover=True) == 0:
            found.append(prefix + "the opening pose is axis-aligned")
        if verdict.is_visible() or "off the net" in (
            slider.get_attribute("aria-valuetext") or ""
        ):
            found.append(prefix + "the opening pose is not an admissible net placement")
        reset.click()
        if not status.is_visible() or not status.inner_text().strip():
            found.append(prefix + "reset gives no status feedback")
        if slider.input_value() != "0":
            found.append(prefix + "reset does not restore direction zero")
        if verdict.is_visible():
            found.append(prefix + "the ordinary on-net minimum shows a stale verdict")
        if canvas.evaluate("el => el.toDataURL()") == initial_bitmap:
            found.append(prefix + "the minimum button does not change the opening pose")
        terms = figure.locator(f"#mv-{slug} .katex-mathml mfrac mn").all_text_contents()
        minimum_mass = Fraction(int(terms[0]), int(terms[1])) if len(terms) == 2 else None
        if slug in known_minima and minimum_mass != known_minima[slug]:
            found.append(prefix + "the minimum button disagrees with the retained certificate")
        minimum = figure.locator(f"#mv-{slug}").inner_text()
        canvas.click(position={"x": 20, "y": 20})
        if status.is_visible() and status.inner_text().strip():
            found.append(prefix + "moving the square leaves reset feedback visible")
        if not verdict.is_visible():
            found.append(prefix + "an outside-domain placement has no verdict")
        reset.click()
        if figure.locator(f"#mv-{slug}").inner_text() != minimum:
            found.append(prefix + "reset does not restore the certificate's minimum mass")
        scan.click()
        if not status.is_visible() or not status.inner_text().strip():
            found.append(prefix + "the raster scan gives no status feedback")
        slider.evaluate("(el, value) => { el.value = value; }", slider.get_attribute("max"))
        slider.dispatch_event("input")
        if status.is_visible() and status.inner_text().strip():
            found.append(prefix + "changing direction leaves scan feedback visible")
        field.check()
        visible_bitmap: str = canvas.evaluate("el => el.toDataURL()")
        field.uncheck()
        if canvas.evaluate("el => el.toDataURL()") == visible_bitmap:
            found.append(prefix + "unchecking mass shading leaves the field unchanged")
        slider.evaluate("el => { el.value = '0'; }")
        slider.dispatch_event("input")
        field.check()
        replays: bool = figure.evaluate(
            """figure => {
              const canvas = figure.querySelector('canvas');
              const restored = canvas.toDataURL();
              figure.querySelector('input[type=range]').dispatchEvent(
                new Event('input', {bubbles: true}));
              return canvas.toDataURL() === restored;
            }"""
        )
        if not replays:
            found.append(prefix + "restoring the field uses a stale direction bitmap")
        if hint.inner_text() != instruction:
            found.append(prefix + "an action overwrites the permanent instructions")
        # This is the reported long half-tangent, 12219313/45000000, rather than
        # only the much shorter zero readout which cannot expose the wrap defect.
        slider.evaluate("el => { el.value = String(Math.min(118, Number(el.max))); }")
        slider.dispatch_event("input")
        if slider.get_attribute("max") == "180":
            direction = figure.locator(f"#kval-{slug}").inner_text()
            if not all(value in direction for value in ("12219313", "45000000", "30.3836")):
                found.append(prefix + "direction 118 has the wrong half-tangent or angle")
        for width in (1280, 375):
            page.set_viewport_size({"width": width, "height": 900})
            page.evaluate(_SETTLED)
            layout: list[str] = page.evaluate(_PROVER_LAYOUT)
            found.extend(prefix + f"{width}px: {failure}" for failure in layout)
        page.set_viewport_size({"width": 1280, "height": 900})
        slider.evaluate("el => { el.value = '0'; }")
        slider.dispatch_event("input")
        box = canvas.bounding_box()
        if box is not None:
            # Center the square, then drag the visible top handle into the reflected
            # angle range. These are pointer locations in the displayed instrument;
            # they do not call or expose its private geometry functions.
            canvas.click(position={"x": box["width"] / 2, "y": box["height"] / 2})
            box = canvas.bounding_box()
            assert box is not None
            handle = figure.locator(f"#prove-rotate-{slug}")
            target = handle.bounding_box() if handle.count() else None
            if target is None:
                found.append(prefix + "the rotation handle is missing")
                continue
            page.mouse.move(
                target["x"] + target["width"] / 2, target["y"] + target["height"] / 2
            )
            page.mouse.down()
            page.mouse.move(box["x"] + box["width"] * 0.3, box["y"] + box["height"] * 0.4)
            page.mouse.up()
            if "off the net" not in (slider.get_attribute("aria-valuetext") or ""):
                found.append(prefix + "free rotation does not report an off-net direction")
            for width in (1280, 375):
                page.set_viewport_size({"width": width, "height": 900})
                page.evaluate(_SETTLED)
                layout = page.evaluate(_PROVER_LAYOUT)
                found.extend(prefix + f"off-net {width}px: {failure}" for failure in layout)
        page.set_viewport_size({"width": 1280, "height": 900})
    return found


_ROTATION_TARGET = """handle => {
  const found = [], box = handle.getBoundingClientRect();
  if (box.width < 44 || box.height < 44) found.push('rotation target is smaller than 44px');
  if (handle.tagName !== 'BUTTON' || !handle.getAttribute('aria-label'))
    found.push('rotation target is not a named native button');
  const hit = document.elementFromPoint(box.x + box.width / 2, box.y + box.height / 2);
  if (!handle.contains(hit)) found.push('rotation target is covered by another element');
  if (getComputedStyle(handle).touchAction !== 'none')
    found.push('rotation target allows the browser to cancel its touch drag');
  const canvas = handle.closest('.stage').querySelector('canvas');
  if (getComputedStyle(canvas).touchAction !== 'pan-y')
    found.push('the canvas no longer permits vertical touch scrolling');
  return found;
}"""


def _touch_gesture(
    page: Page,
    session: CDPSession,
    start: tuple[float, float],
    end: tuple[float, float] | None = None,
) -> None:
    """Send real browser touch input, paced by animation frames rather than sleeps."""
    session.send(
        "Input.dispatchTouchEvent",
        {"type": "touchStart", "touchPoints": [{"x": start[0], "y": start[1], "id": 1}]},
    )
    if end is not None:
        for step in range(1, 7):
            x = start[0] + (end[0] - start[0]) * step / 6
            y = start[1] + (end[1] - start[1]) * step / 6
            session.send(
                "Input.dispatchTouchEvent",
                {"type": "touchMove", "touchPoints": [{"x": x, "y": y, "id": 1}]},
            )
            page.evaluate(_SETTLED)
    session.send("Input.dispatchTouchEvent", {"type": "touchEnd", "touchPoints": []})
    page.evaluate(_SETTLED)


def _control_angle(control: Locator, *, prover: bool) -> float:
    if not prover:
        return float(control.input_value()) / 10
    text = control.get_attribute("aria-valuetext") or ""
    match = re.search(r"([0-9]+(?:\.[0-9]+)?) degrees", text)
    if match is None:
        raise ValueError(f"net direction control has no readable angle: {text!r}")
    return float(match.group(1))


def touch_findings(page: Page) -> list[str]:
    """Tap, drag, keyboard, and ordinary swipes on both figures and certificates."""
    session = page.context.new_cdp_session(page)
    slugs: list[str] = page.locator(".cert-figure").evaluate_all(
        "els => [...new Set(els.map(el => el.dataset.cert))]"
    )
    found: list[str] = []
    try:
        for slug in slugs:
            page.locator(f'.cert-toggle button[data-cert="{slug}"]:visible').first.tap()
            for number, name, control_name in ((5, "prove", "kslider"), (6, "shrink", "phi")):
                prefix = f"Figure {number} touch ({slug}): "
                canvas = page.locator(f"#{name}-{slug}")
                handle = page.locator(f"#{name}-rotate-{slug}")
                if not handle.count() or not handle.is_visible():
                    found.append(prefix + "no visible rotation button before the first touch")
                    continue
                canvas.evaluate("el => el.scrollIntoView({block: 'center'})")
                page.evaluate(_SETTLED)
                control = page.locator(f"#{control_name}-{slug}")
                if number == 5:
                    control.evaluate("el => { el.value = '0'; }")
                    control.dispatch_event("input")
                    box = canvas.bounding_box()
                    assert box is not None
                    _touch_gesture(
                        page,
                        session,
                        (box["x"] + box["width"] / 2, box["y"] + box["height"] / 2),
                    )
                target_findings: list[str] = handle.evaluate(_ROTATION_TARGET)
                found.extend(prefix + failure for failure in target_findings)
                before = _control_angle(control, prover=number == 5)
                target = handle.bounding_box()
                assert target is not None
                _touch_gesture(
                    page,
                    session,
                    (target["x"] + target["width"] / 2, target["y"] + target["height"] / 2),
                )
                if _control_angle(control, prover=number == 5) == before:
                    found.append(
                        prefix + "tapping the rotation button does not turn the square"
                    )
                before = _control_angle(control, prover=number == 5)
                target, box = handle.bounding_box(), canvas.bounding_box()
                assert target is not None
                assert box is not None
                _touch_gesture(
                    page,
                    session,
                    (target["x"] + target["width"] / 2, target["y"] + target["height"] / 2),
                    (box["x"] + box["width"] * 0.3, box["y"] + box["height"] * 0.4),
                )
                if abs(_control_angle(control, prover=number == 5) - before) < 0.5:
                    found.append(
                        prefix + "touch dragging the handle does not rotate the square"
                    )
                before = _control_angle(control, prover=number == 5)
                handle.press("ArrowRight")
                if _control_angle(control, prover=number == 5) == before:
                    found.append(prefix + "the rotation button does not support arrow keys")
                canvas.evaluate("el => el.scrollIntoView({block: 'center'})")
                page.evaluate(_SETTLED)
                box = canvas.bounding_box()
                assert box is not None
                scroll = """() => (document.querySelector('[data-kpress-viewport]')
                  || document.scrollingElement).scrollTop"""
                prior_scroll: float = page.evaluate(scroll)
                _touch_gesture(
                    page,
                    session,
                    (box["x"] + box["width"] * 0.8, box["y"] + box["height"] * 0.8),
                    (box["x"] + box["width"] * 0.8, box["y"] + box["height"] * 0.2),
                )
                if page.evaluate(scroll) - prior_scroll < 20:
                    found.append(prefix + "an ordinary canvas swipe does not scroll the page")
    finally:
        session.detach()
    return found


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
            controls = prover_findings(page)
            mobile = browser.new_page(
                viewport={"width": 375, "height": 812},
                is_mobile=True,
                has_touch=True,
                reduced_motion="reduce",
            )
            mobile.goto(page_url, wait_until="load")
            mobile.wait_for_selector(READY, timeout=60_000)
            mobile.evaluate("document.fonts.ready")
            controls.extend(touch_findings(mobile))
            return {"screen": screen, "print": printed, "controls": controls}
        finally:
            browser.close()


def findings(measured: Measured, *, every: bool = False) -> list[str]:
    """Everything the two passes say is wrong, as lines a reader can act on."""
    screen = measured["screen"]
    printed = measured["print"]
    found: list[str] = list(measured.get("controls", []))

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
