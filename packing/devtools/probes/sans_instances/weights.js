// Every distinct family, weight and style the page draws text in, with a run count and
// the first few elements that ask for it, each stamped with a marker the matched-rule
// walk finds it by. Not scoped to the sans: the question the listing answers is whether
// one bold and one medium serve the whole design system, and the serif's own bold is
// part of that answer. Hidden runs are skipped for the reason `requests` skips them -- a
// weight nobody sees is not a weight the design has to reconcile.
//
// Several elements per combination, not one, because one is the wrong number for the
// question. `.doc-links .chip` and the caption's label are both the sans at 550, and a
// listing that reported the first would say the medium had one source when it had two.
// The markers are cleared first: the same page is probed under both media, and a marker
// the screen pass left behind would be found instead of the element the print pass just
// stamped, since `DOM.querySelector` answers with the first match in document order.
//
// `sig` is `element_path`'s function.
/** @param {{ attribute: string, samples: number, sig: (el: Element) => string }} argument */
({ attribute, samples, sig }) => {
  for (const stale of document.querySelectorAll(`[${attribute}]`)) {
    stale.removeAttribute(attribute);
  }
  /** @typedef {{ family: string, weight: number, style: string, runs: number, seen: { marker: number, path: string }[] }} SansWeightRow */
  /** @type {Map<string, SansWeightRow>} */
  const found = new Map();
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  let next = 0;
  for (let node = walker.nextNode(); node; node = walker.nextNode()) {
    if (!node.nodeValue?.trim()) {
      continue;
    }
    const el = node.parentElement;
    if (!el?.getClientRects().length) {
      continue;
    }
    const style = getComputedStyle(el);
    const family = /** @type {string} */ (style.fontFamily.split(",")[0])
      .trim()
      .replace(/^["']|["']$/g, "");
    const weight = parseInt(style.fontWeight, 10);
    const key = `${family}/${weight}/${style.fontStyle}`;
    if (!found.has(key)) {
      found.set(key, { family, weight, style: style.fontStyle, runs: 0, seen: [] });
    }
    const row = /** @type {SansWeightRow} */ (found.get(key));
    row.runs++;
    if (row.seen.length < samples && !el.hasAttribute(attribute)) {
      el.setAttribute(attribute, String(next));
      row.seen.push({ marker: next, path: sig(el) });
      next++;
    }
  }
  return [...found.values()].sort(
    (a, b) =>
      a.family.localeCompare(b.family) || a.weight - b.weight || a.style.localeCompare(b.style),
  );
};
