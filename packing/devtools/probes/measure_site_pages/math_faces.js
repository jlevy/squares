// Every typeset formula's actual face beside its surrounding text, counted by surface.
// Native frontier cells inspect a visible MathML token; prepared KaTeX keeps its visual
// root. Backend labels describe the inspected output, without substituting desired faces.
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
  /** @type {Map<string, {surface: string, text: string, math: string, backend: string, count: number, alone: number, example: string}>} */
  const rows = new Map();
  for (const math of document.querySelectorAll(
    '.kpress-math[data-kpress-math-rendered], .kpress-math[data-site-native-math="frontier"]',
  )) {
    const host = math.parentElement;
    if (!host) {
      continue;
    }
    const native = math.getAttribute("data-site-native-math") === "frontier";
    const root = native ? math.querySelector(":scope > math") : null;
    const visual = native
      ? [...(root?.querySelectorAll("mi, mn, mtext, ms") ?? [])].find((node) => {
          const box = node.getBoundingClientRect();
          return (
            node.namespaceURI === "http://www.w3.org/1998/Math/MathML" &&
            (node.textContent ?? "").trim() &&
            box.width > 0 &&
            box.height > 0 &&
            getComputedStyle(node).visibility !== "hidden"
          );
        })
      : math.querySelector(".katex");
    if (!native && !visual) {
      continue;
    }
    const surface = surfaces.find(([selector]) => host.closest(selector))?.[1] ?? "prose";
    const text = first(getComputedStyle(host).fontFamily);
    const face = visual ? first(getComputedStyle(visual).fontFamily) : "missing native MathML";
    const backend = native ? "native-mathml" : "katex";
    const key = `${surface}|${text}|${face}|${backend}`;
    const row = rows.get(key) ?? {
      surface,
      text,
      math: face,
      backend,
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
