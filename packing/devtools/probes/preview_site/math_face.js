// Every typeset formula set in the wrong face (paper-design.md, Math). Math takes the
// face of the text around it, serif in serif prose and sans in sans text, with one
// exception: a headline that is mathematics standing alone, such as `n = 11`, is serif
// though the headline's own face is sans. kpress picks the face from a fixed list of
// sans contexts, and the host adapter from the text's computed face and the
// `data-math-face="serif"` mark, so a site style that sets a block in the other face, a
// headline of math left unmarked and a mark on a headline with words in it all show
// here. Formulas kpress leaves in the stock KaTeX face are not reported. Native frontier
// cells are checked against the actual surrounding font, through their visible token.
() => {
  /** @param {string} family */
  const first = (family) => (family.split(",")[0] ?? "").trim().replace(/^["']|["']$/g, "");
  const sans = first(
    getComputedStyle(document.documentElement).getPropertyValue("--kpress-font-sans"),
  );
  /** @type {Record<string, boolean>} */
  const faces = { "KPress Math Text": false, "KPress Math Text Sans": true };
  const headlines = "h1, h2, h3, h4, h5, h6, .site-card-value, .site-popover-value";
  /**
   * Whether `block` holds formulas and nothing else.
   * @param {Element} block
   */
  const allMath = (block) => {
    let formulas = 0;
    for (const node of block.childNodes) {
      if (node instanceof Element && node.matches(".kpress-math")) {
        formulas += 1;
      } else if ((node.textContent ?? "").trim()) {
        return false;
      }
    }
    return formulas > 0;
  };
  const found = [];
  for (const math of document.querySelectorAll(
    '.kpress-math[data-kpress-math-rendered], .kpress-math[data-site-native-math="frontier"]',
  )) {
    const host = math.parentElement;
    if (math.getAttribute("data-site-native-math") === "frontier") {
      const roots = [...math.children].filter(
        (node) =>
          node.namespaceURI === "http://www.w3.org/1998/Math/MathML" && node.localName === "math",
      );
      const root = roots[0];
      const token = [...(root?.querySelectorAll("mi, mn, mtext, ms") ?? [])].find((node) => {
        const box = node.getBoundingClientRect();
        return (
          (node.textContent ?? "").trim() &&
          box.width > 0 &&
          box.height > 0 &&
          getComputedStyle(node).visibility !== "hidden"
        );
      });
      if (!host || !math.closest(".site-frontier td") || roots.length !== 1 || !token) {
        found.push("native frontier math has no visible mathematical token");
      } else if (
        first(getComputedStyle(token).fontFamily) !== first(getComputedStyle(host).fontFamily)
      ) {
        found.push(
          `native frontier math differs from surrounding text in #${math.closest("[id]")?.id ?? ""}`,
        );
      }
      continue;
    }
    const katex = math.querySelector(".katex");
    if (!(host && katex)) {
      continue;
    }
    const mathSans = faces[first(getComputedStyle(katex).fontFamily)];
    if (mathSans === undefined) {
      continue;
    }
    const textSans = first(getComputedStyle(host).fontFamily) === sans;
    const alone = host.matches(headlines) && allMath(host);
    if (mathSans !== (textSans && !alone)) {
      const where = host.closest("[id]")?.id ?? "";
      const tag = `${host.tagName.toLowerCase()}.${host.className || "-"}`;
      const tex =
        math.querySelector("annotation")?.textContent ??
        math.querySelector("math")?.textContent ??
        "";
      const around = alone ? "a headline that is all math" : `${textSans ? "sans" : "serif"} text`;
      found.push(
        `${mathSans ? "sans" : "serif"} math in ${around}: ${tag} in #${where}: ${tex.slice(0, 40)}`,
      );
    }
  }
  return found;
};
