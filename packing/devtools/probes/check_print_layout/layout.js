// What each media's probe returns. One probe for both passes so the two cannot drift apart:
// the whole point is comparing like with like across `emulateMedia`.
//
// Takes `naming` (`naming.js`: `sig` and `round`) and `helpers` (`layout_helpers.js`: the
// bullet box, the first line box and the culprit scan), each through a handle.
/** @param {{ naming: PrintLayoutNaming, helpers: PrintLayoutHelpers }} argument */
({ naming, helpers }) => {
  const { sig, round } = naming;
  const { bulletBox, firstLineBox, widestRun } = helpers;
  /** @type {PrintLayoutProbe} */
  const out = {
    centred: [],
    markers: [],
    bullets: [],
    footnotes: [],
    boxed: [],
    overflow: [],
    pageOverflow: 0,
    widest: null,
    /* Named so a viewport that did not take is visible in the output rather than
       silently making every horizontal answer wrong. */
    measure: document.querySelector(".kpress")?.getBoundingClientRect().width ?? 0,
    viewport: document.documentElement.clientWidth,
  };

  /* Centring. `.centred` is the page's declaration that a block is centred in every
     medium, so it is also the thing to hold it to; nothing else here needs a list of
     intents. Everything with text of its own is recorded as well, for `--all`: that
     sweep is how the colophon was found, before there was a class to check.

     `text-align` inherits, so each row names its parent's row. Without that a single
     lost centring is reported once for the block and once more for every span, link
     and KaTeX node beneath it, and the cause is buried in its own consequences. */
  /** @type {Map<Element, number>} */
  const seen = new Map();
  for (const el of document.querySelectorAll(".kpress, .kpress *")) {
    if (!el.textContent.trim()) {
      continue;
    }
    seen.set(el, out.centred.length);
    const parent = /** @type {Element} */ (el.parentElement);
    out.centred.push({
      index: out.centred.length,
      parent: seen.has(parent) ? /** @type {number} */ (seen.get(parent)) : -1,
      path: sig(el),
      align: getComputedStyle(el).textAlign,
      declared: el.classList.contains("centred"),
      /* Whether the element is laid out at all in this medium. `screen-only` blocks are
         `display: none` under print and still report an inherited `text-align`, so
         without this every one of them is a finding about a box nobody prints. */
      shown: el.getClientRects().length > 0,
    });
  }

  /* Markers. The list bullet is not a `::marker`: kpress sets `list-style-type: none`
     and draws an absolutely positioned `::before`, so there is no marker box to
     measure. Its top edge is the `li`'s content-box top plus the pseudo-element's own
     `top`; its computed height measures the painted square or the numbered marker's
     box. A painted square must retain its own height, not the line box's height. The
     line it should sit on is the `li`'s first line box, taken as a Range over the first
     text node rather than as the `li`'s own box, which spans every line. */
  for (const li of document.querySelectorAll(".kpress li")) {
    const before = getComputedStyle(li, "::before");
    const own = getComputedStyle(li);
    const bullet = bulletBox(li, before);
    if (bullet) {
      out.bullets.push(bullet);
    }
    /* `top` is measured from the containing block's padding edge, and the containing
       block is the `li` only while it is positioned. If kpress ever drops that, the
       offset is against something else and this arithmetic would quietly measure the
       wrong box, so the case is skipped rather than guessed at. */
    if (before.content === "none" || before.position !== "absolute") {
      continue;
    }
    if (own.position === "static") {
      continue;
    }
    const line = firstLineBox(li);
    if (!line) {
      continue;
    }
    const box = li.getBoundingClientRect();
    const edge = parseFloat(own.borderTopWidth) || 0;
    const top = box.top + edge + (parseFloat(before.top) || 0);
    const height =
      parseFloat(before.height) ||
      parseFloat(before.lineHeight) ||
      parseFloat(before.fontSize) ||
      0;
    out.markers.push({
      path: sig(li),
      markerCentre: round(top + height / 2),
      lineCentre: round((line.top + line.bottom) / 2),
      fontSize: round(parseFloat(before.fontSize)),
      baseFontSize: round(
        parseFloat(getComputedStyle(/** @type {Element} */ (li.closest(".kpress"))).fontSize),
      ),
      lineHeight: round(line.bottom - line.top),
      width: round(parseFloat(before.width) || 0),
      height: round(height),
      painted: before.content === '""' && before.backgroundColor !== "rgba(0, 0, 0, 0)",
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
  for (const sup of document.querySelectorAll("sup.kpress-footnote-ref")) {
    const block = sup.closest("p, li, dd, figcaption, td, th");
    if (!block) {
      continue;
    }
    const before = document.createRange();
    before.setStart(block, 0);
    before.setEndBefore(sup);
    const rects = [...before.getClientRects()].filter((r) => r.width && r.height);
    if (!rects.length) {
      continue;
    }
    const tail = /** @type {DOMRect} */ (rects[rects.length - 1]);
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
  for (const chip of document.querySelectorAll(".doc-links .chip")) {
    const box = chip.getBoundingClientRect();
    const text = [...chip.childNodes].find(
      (n) => n.nodeType === 3 && /** @type {string} */ (n.textContent).trim(),
    );
    if (!text || !box.height) {
      continue;
    }
    const range = document.createRange();
    range.selectNodeContents(text);
    const ink = range.getBoundingClientRect();
    if (!ink.height) {
      continue;
    }
    out.boxed.push({
      path: sig(chip),
      text: /** @type {string} */ (text.textContent).trim().slice(0, 20),
      /* Positive when the label sits below the centre of the box drawn around it. */
      offset: round((ink.top + ink.bottom) / 2 - (box.top + box.bottom) / 2),
    });
  }

  /* Overflow. The measure is set by the `@page` margin, so a block reaching past the
     body's content box is wrapped wrongly or cut. Figures are allowed their own scroll
     on screen and are excluded by the same class the stylesheet uses to let them. */
  const page = document.querySelector(".kpress");
  if (page) {
    const room = page.getBoundingClientRect();
    for (const el of page.querySelectorAll("p, li, h1, h2, h3, h4, figcaption, blockquote")) {
      const box = el.getBoundingClientRect();
      if (!box.width) {
        continue;
      }
      const over = round(Math.max(room.left - box.left, box.right - room.right));
      if (over > 1) {
        out.overflow.push({
          path: sig(el),
          over,
          text: el.textContent.trim().slice(0, 60),
        });
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
  if (out.pageOverflow > 1) {
    out.widest = widestRun(root);
  }

  return out;
};
