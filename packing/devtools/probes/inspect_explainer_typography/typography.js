// The computed typography of every visible text run on the page, grouped by family, weight,
// style and colour, with the sizes and a few samples of each. An SVG run's effective size
// includes the transform it is drawn under.
//
// With `check`, the same pass holds supporting text to its role: caption and endnote text to
// the first visible caption's size, family and colour, other supporting text to the first
// visible figure label's (or the caption's, without one). Links, math, code, headings and
// the figures' emphasis are exempt. It also refuses a persistent link underline and
// intersecting label boxes inside an inline SVG figure.
//
// Takes `{selector, supporting, check}`: an optional scope, the selector list of supporting
// text (`SUPPORTING_SELECTOR`), and whether to check.
/** @param {{ selector: string | null, supporting: string, check: boolean }} o */
({ selector, supporting, check }) => {
  /** @type {Map<string, TypographyFontUse>} */
  const groups = new Map();
  /** @type {Set<string>} */
  const findings = new Set();
  let checked = 0;
  /** @param {Element} el */
  const visible = (el) =>
    getComputedStyle(el).visibility === "visible" &&
    el.getClientRects().length &&
    !el.closest("[hidden]");
  const caption = [...document.querySelectorAll(".kpress-figcaption")].find(visible);
  const figure = [...document.querySelectorAll(".mass-line")].find(visible);
  const noteStyle = caption ? getComputedStyle(caption) : null;
  const figureStyle = figure ? getComputedStyle(figure) : noteStyle;
  const exceptions =
    "a, .katex, math, .tex, .tex-d, code, pre, " +
    "h1, h2, h3, h4, h5, h6, .verdict, .hi, .mass-val, .tag";
  if (check && !noteStyle) {
    findings.add("no visible caption to establish supporting typography");
  }
  /** @param {number} x */
  const round = (x) => Math.round(x * 10000) / 10000;
  const walker = document.createTreeWalker(document.documentElement, NodeFilter.SHOW_TEXT);
  while (walker.nextNode()) {
    const node = walker.currentNode,
      el = /** @type {Element | null} */ (node.parentElement);
    const text = /** @type {string} */ (node.textContent).replace(/\s+/g, " ").trim();
    if (!text || !el) {
      continue;
    }
    if (selector && !el.closest(selector)) {
      continue;
    }
    if (el.closest("script, style, title, desc, .kpress-math-semantic")) {
      continue;
    }
    const css = getComputedStyle(el);
    if (!visible(el)) {
      continue;
    }
    const svgText = el.closest("svg text");
    const color = svgText ? css.fill : css.color;
    const size = Number.parseFloat(css.fontSize);
    // The transformed vertical em measures displayed letter size, even where
    // the SVG has a rotated or non-uniformly scaled coordinate system.
    const ctm = svgText ? /** @type {SVGGraphicsElement} */ (el).getScreenCTM() : null;
    const effective = round(size * (ctm ? Math.hypot(ctm.c, ctm.d) : 1));
    const key = [css.fontFamily, css.fontWeight, css.fontStyle, color].join("|");
    if (!groups.has(key)) {
      groups.set(key, {
        family: css.fontFamily,
        weight: css.fontWeight,
        style: css.fontStyle,
        color,
        sizes: [],
        effective_sizes: [],
        samples: [],
      });
    }
    const group = /** @type {TypographyFontUse} */ (groups.get(key));
    if (!group.sizes.includes(size)) {
      group.sizes.push(size);
    }
    if (!group.effective_sizes.includes(effective)) {
      group.effective_sizes.push(effective);
    }
    const sample = `${el.tagName.toLowerCase()}: ${text.slice(0, 100)}`;
    if (group.samples.length < 5 && !group.samples.includes(sample)) {
      group.samples.push(sample);
    }
    const expected = el.closest(".kpress-figcaption, .kpress-footnotes") ? noteStyle : figureStyle;
    if (check && expected && el.closest(supporting) && !el.closest(exceptions)) {
      checked++;
      const differences = [];
      if (Math.abs(effective - Number.parseFloat(expected.fontSize)) > 0.1) {
        differences.push(`size ${effective}px (expected ${expected.fontSize})`);
      }
      if (css.fontFamily !== expected.fontFamily) {
        differences.push(`family ${css.fontFamily} (expected ${expected.fontFamily})`);
      }
      if (color !== expected.color && !el.closest('button[aria-pressed="true"]')) {
        differences.push(`color ${color} (expected ${expected.color})`);
      }
      if (differences.length) {
        findings.add(`${sample}: ${differences.join("; ")}`);
      }
    }
  }
  if (check && noteStyle && !checked) {
    findings.add("no ordinary supporting text matched the requested selector");
  }
  if (check) {
    for (const link of document.querySelectorAll(".cert-page a")) {
      if (visible(link) && getComputedStyle(link).textDecorationLine !== "none") {
        findings.add(`persistent link decoration: ${link.textContent.trim().slice(0, 80)}`);
      }
    }
    for (const svg of document.querySelectorAll(".line-fig svg, .chart svg")) {
      if (!visible(svg) || (selector && !svg.closest(selector) && !svg.querySelector(selector))) {
        continue;
      }
      const labels = [...svg.querySelectorAll("text")].filter(visible);
      for (let i = 0; i < labels.length; i++) {
        const label = /** @type {SVGTextElement} */ (labels[i]);
        const a = label.getBoundingClientRect();
        for (let j = i + 1; j < labels.length; j++) {
          const other = /** @type {SVGTextElement} */ (labels[j]);
          const b = other.getBoundingClientRect();
          const width = Math.min(a.right, b.right) - Math.max(a.left, b.left);
          const height = Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top);
          if (width > 1 && height > 1) {
            findings.add(
              "SVG label boxes overlap: " +
                `${label.textContent.trim()} / ${other.textContent.trim()} ` +
                `(${round(width)} x ${round(height)}px)`,
            );
          }
        }
      }
    }
  }
  return {
    fonts: [...groups.values()]
      .map((g) => ({
        ...g,
        sizes: g.sizes.sort((a, b) => a - b),
        effective_sizes: g.effective_sizes.sort((a, b) => a - b),
      }))
      .sort(
        (a, b) =>
          a.family.localeCompare(b.family) ||
          Number(a.weight) - Number(b.weight) ||
          a.color.localeCompare(b.color),
      ),
    findings: [...findings],
  };
};
