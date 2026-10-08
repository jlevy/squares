// Every typeset formula's face beside the face of the text it sits in, counted by the
// surface it is on: a card's headline or note, a chip, a table, a popover, the nav, a
// caption, a case record's panels, a heading, a list, the prose. One row per surface,
// text face and math face, with how many formulas it stands for, how many of those are
// a headline that is math standing alone, and one formula's TeX as an example.
// `preview_site/math_face.js` holds the rule these are judged by.
() => {
  /** @param {string} family */
  const first = (family) => (family.split(",")[0] ?? "").trim().replace(/^["']|["']$/g, "");
  /** @type {[string, string][]} */
  const surfaces = [
    [".site-card-value", "card headline"],
    [".site-card-note", "card note"],
    [".site-popover-value", "popover headline"],
    [".site-atlas-pop", "visual summary"],
    [".site-popover", "popover"],
    [".site-chip", "chip"],
    [".site-nav", "nav"],
    ["figcaption, caption", "caption"],
    [".subtitle", "subtitle"],
    [".site-case-head", "case head"],
    [".site-case-bounds", "case bounds"],
    [".site-case-data", "case detail"],
    ["summary", "summary"],
    ["details", "details"],
    ["th", "table head"],
    ["td", "table cell"],
    ["h1, h2, h3, h4, h5, h6", "heading"],
    [".kpress-footnotes", "footnote"],
    ["li", "list item"],
  ];
  const headlines = "h1, h2, h3, h4, h5, h6, .site-card-value, .site-popover-value";
  /** @param {Element} block */
  const allMath = (block) =>
    [...block.childNodes].every(
      (node) =>
        (node instanceof Element && node.matches(".kpress-math")) ||
        !(node.textContent ?? "").trim(),
    );
  /** @type {Map<string, {surface: string, text: string, math: string, count: number, alone: number, example: string}>} */
  const rows = new Map();
  for (const math of document.querySelectorAll(".kpress-math[data-kpress-math-rendered]")) {
    const host = math.parentElement;
    const katex = math.querySelector(".katex");
    if (!(host && katex)) {
      continue;
    }
    const surface = surfaces.find(([selector]) => host.closest(selector))?.[1] ?? "prose";
    const text = first(getComputedStyle(host).fontFamily);
    const face = first(getComputedStyle(katex).fontFamily);
    const key = `${surface}|${text}|${face}`;
    const row = rows.get(key) ?? {
      surface,
      text,
      math: face,
      count: 0,
      alone: 0,
      example: (
        math.querySelector("annotation")?.textContent ??
        math.querySelector("math")?.textContent ??
        ""
      ).slice(0, 40),
    };
    row.count += 1;
    row.alone += host.matches(headlines) && allMath(host) ? 1 : 0;
    rows.set(key, row);
  }
  return [...rows.values()];
};
