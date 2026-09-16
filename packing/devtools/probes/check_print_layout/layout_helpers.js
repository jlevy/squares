// The parts of the layout probe that are tested on their own, in Node, against rectangles
// retained from the browser: the drawn bullet's box, the first line box a marker is held
// to, and the scan that names the run widening the page.
//
// A reference probe: it returns the helpers rather than being one. Takes `naming.js`'s
// `sig` and `round`, which `layout.js` hands it through a handle and a test replaces with
// stand-ins.
/**
 * @param {PrintLayoutNaming} naming
 * @returns {PrintLayoutHelpers}
 */
({ sig, round }) => {
  return { bulletBox, firstLineBox, widestRun, inkRight };

  /* A centered rectangle can still be a vertical bar. Record shape and paint before
     the centering probe skips missing pseudo-elements; ordered markers are text. */
  /**
   * @param {Element} li
   * @param {CSSStyleDeclaration} before
   */
  function bulletBox(li, before) {
    if (li.parentElement?.tagName !== "UL" || !li.getClientRects().length) {
      return null;
    }
    return {
      path: sig(li),
      width: round(parseFloat(before.width)),
      height: round(parseFloat(before.height)),
      painted:
        before.content === '""' &&
        before.display !== "none" &&
        before.visibility === "visible" &&
        Number(before.opacity) > 0 &&
        !["transparent", "rgba(0, 0, 0, 0)"].includes(before.backgroundColor),
    };
  }

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
  /** @param {Element} root */
  function widestRun(root) {
    /** @type {PrintLayoutOverflow | null} */
    let widest = null;
    for (const el of document.querySelectorAll(".kpress *")) {
      if (el.closest("svg")) {
        continue;
      }
      const box = el.getBoundingClientRect();
      /* Ink never reaches past the box, so the ancestor walk is only worth its cost
         where the box itself is past the edge. */
      if (!box.width || box.right - root.clientWidth <= 1) {
        continue;
      }
      const over = round(inkRight(el) - root.clientWidth);
      if (over > 1 && (!widest || over > widest.over)) {
        widest = {
          path: sig(el),
          over,
          text: el.textContent.trim().slice(0, 60),
        };
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
  /** @param {Element} el */
  function inkRight(el) {
    let right = el.getBoundingClientRect().right;
    let position = getComputedStyle(el).position;
    for (let node = el.parentElement; node; node = node.parentElement) {
      const style = getComputedStyle(node);
      const containing = style.position !== "static";
      if (position === "fixed" || (position === "absolute" && !containing)) {
        continue;
      }
      if (style.overflowX !== "visible" || style.clip !== "auto" || style.clipPath !== "none") {
        right = Math.min(right, node.getBoundingClientRect().right);
      }
      position = style.position;
    }
    return right;
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

     A zero-line-height footnote and clipped accessibility MathML can have Range
     rectangles outside the line without enlarging it. Remove only those owned
     rectangles before grouping. Visible MathML fallback and ordinary inline boxes
     still contribute. Count duplicates so an unrelated box with the same geometry
     is not removed along with an overlay. */
  /** @param {Element} el */
  function firstLineBox(el) {
    const range = document.createRange();
    range.selectNodeContents(el);
    /** @type {Map<string, number>} */
    const excluded = new Map();
    /** @param {DOMRect} r */
    const key = (r) => [r.top, r.right, r.bottom, r.left].join(",");
    const overlays = [...el.querySelectorAll("sup.kpress-footnote-ref")].filter(
      (ref) => parseFloat(getComputedStyle(ref).lineHeight) === 0,
    );
    for (const ref of el.querySelectorAll(".katex-mathml, .kpress-math-semantic")) {
      const style = getComputedStyle(ref);
      if (style.position === "absolute" && (style.clip !== "auto" || style.clipPath !== "none")) {
        overlays.push(ref);
      }
    }
    for (const ref of overlays) {
      const reference = document.createRange();
      reference.selectNode(ref);
      for (const rect of reference.getClientRects()) {
        if (!rect.width || !rect.height) {
          continue;
        }
        const id = key(rect);
        excluded.set(id, (excluded.get(id) || 0) + 1);
      }
    }
    const rects = [...range.getClientRects()].filter((r) => {
      if (!r.width || !r.height) {
        return false;
      }
      const id = key(r);
      const count = excluded.get(id) || 0;
      if (!count) {
        return true;
      }
      excluded.set(id, count - 1);
      return false;
    });
    if (!rects.length) {
      return null;
    }
    const topmost = rects.reduce((a, r) => (r.top < a.top ? r : a));
    const band = rects.filter((r) => r.top < topmost.top + topmost.height / 2);
    return {
      top: Math.min(...band.map((r) => r.top)),
      bottom: Math.max(...band.map((r) => r.bottom)),
    };
  }
};
