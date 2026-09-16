// What the page asks for, taken from the page rather than read out of the stylesheet.
// A run is counted when the first family in its computed stack is one of the two sans
// names the probe is handed: the print family kpress declares its instances under, and
// `SCREEN_SANS`. Runs the print stylesheet hides are skipped -- a `display: none` block
// still reports a computed weight, and counting it would declare an instance for text
// no reader ever sees.
//
// Two passes, because a tree walk sees only half the type. Text nodes are the first;
// generated content is the second, and it is not hypothetical here -- kpress numbers
// footnote items with `li.kpress-footnote-item::before`, a real sans run in no text
// node on the page.
//
// Takes `[families, pseudos, sig]`: the two sans names, the pseudo-elements that can carry
// type (`PSEUDO_ELEMENTS`), and `element_path`'s function.
/** @param {[string[], string[], (el: Element) => string]} argument */
([families, pseudos, sig]) => {
  const sans = new Set(families);
  /** @type {Map<string, { weight: number, style: string, path: string }>} */
  const found = new Map();
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  for (let node = walker.nextNode(); node; node = walker.nextNode()) {
    if (!node.nodeValue?.trim()) {
      continue;
    }
    const el = node.parentElement;
    if (!el?.getClientRects().length) {
      continue;
    }
    record(getComputedStyle(el), sig(el));
  }
  for (const el of document.body.querySelectorAll("*")) {
    if (!el.getClientRects().length) {
      continue;
    }
    for (const pseudo of pseudos) {
      const style = getComputedStyle(el, pseudo);
      if (!draws(style.content)) {
        continue;
      }
      record(style, sig(el) + pseudo);
    }
  }
  return [...found.values()].sort((a, b) => a.weight - b.weight || a.style.localeCompare(b.style));

  /* Whether a computed `content` puts glyphs on the page. `none` is no pseudo-element
     at all and `normal` is the default -- which for `::marker` is a bullet drawn in the
     list item's own font, already counted through its text. An empty string is a box
     with no type in it: a rule, a spacer, a clearfix. None of the four asks for a face. */
  /** @param {string} content */
  function draws(content) {
    return Boolean(content) && !["none", "normal", '""', "''"].includes(content);
  }

  /* One request, recorded once per weight and style. The first element to ask for a
     pair is the one a failure names, and the text pass runs first, so a run a reader
     can point at is preferred over generated content that says the same thing. */
  /**
   * @param {CSSStyleDeclaration} style
   * @param {string} path
   */
  function record(style, path) {
    const family = /** @type {string} */ (style.fontFamily.split(",")[0])
      .trim()
      .replace(/^["']|["']$/g, "");
    if (!sans.has(family)) {
      return;
    }
    const weight = parseInt(style.fontWeight, 10);
    const key = `${weight}/${style.fontStyle}`;
    if (!found.has(key)) {
      found.set(key, { weight, style: style.fontStyle, path });
    }
  }
};
