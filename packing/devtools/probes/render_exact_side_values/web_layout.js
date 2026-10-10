// Measure the settled web report; local table scrolling preserves full source content.
/** @param {{settle?: boolean}} [options] */
async (options = {}) => {
  if (options?.settle !== false) {
    await document.fonts.ready;
    await new Promise((resolve) => requestAnimationFrame(() => requestAnimationFrame(resolve)));
  }
  const root = document.documentElement;
  /** @param {number} value */
  const round = (value) => Math.round(value * 100) / 100;
  const tables = [...document.querySelectorAll(".kpress-table-wrap, .coefficient-table-wrap")].map(
    (wrapper) => {
      const table = wrapper.querySelector("table");
      const style = getComputedStyle(wrapper);
      return {
        columns: table?.querySelector("tr")?.children.length ?? 0,
        rows: table?.querySelectorAll("tbody tr").length ?? 0,
        width: round(wrapper.getBoundingClientRect().width),
        contentWidth: wrapper.scrollWidth,
        overflow: style.overflowX,
        keyboardReachable: wrapper.getAttribute("tabindex") === "0",
      };
    },
  );
  const fractions = [...document.querySelectorAll(".exact-rational")].map((fraction) => {
    const style = getComputedStyle(fraction);
    return {
      source: fraction.getAttribute("data-exact-source"),
      numerator: fraction.querySelector(".exact-numerator")?.textContent,
      denominator: fraction.querySelector(".exact-denominator")?.textContent,
      width: round(fraction.getBoundingClientRect().width),
      fontPx: parseFloat(style.fontSize),
      hidden:
        style.display === "none" || style.visibility !== "visible" || Number(style.opacity) === 0,
    };
  });
  // Only visual source values are checked: KaTeX's hidden accessibility duplicate
  // is excluded, and scrollable regions retain access to their offscreen content.
  const activeMath = [
    ...document.querySelectorAll(".kpress-math-render .katex-html, #entry-equation math"),
    ...[...document.querySelectorAll(".kpress-math-semantic math")].filter(
      (math) => !math.closest('[data-kpress-math-rendered="true"]'),
    ),
  ];
  const values = [
    ...document.querySelectorAll(".exact-numerator, .exact-denominator"),
    ...[...document.querySelectorAll("td code")].filter(
      (code) =>
        /^[+-]?\d+$/.test(code.textContent ?? "") &&
        !code.closest("#coefficient-content[hidden], #detail-content[hidden]"),
    ),
    ...activeMath.flatMap((math) => [
      math,
      ...[...math.querySelectorAll("mi, mn, mo, span")].filter(
        (leaf) => !leaf.children.length && leaf.textContent?.trim() && !leaf.closest("mphantom"),
      ),
    ]),
  ];
  const lostInk = [];
  for (const value of values) {
    if (!value.textContent?.trim()) {
      continue;
    }
    const range = document.createRange();
    range.selectNodeContents(value);
    const boxes = [...value.getClientRects(), ...range.getClientRects()].filter(
      (box) => box.width > 0 && box.height > 0,
    );
    const cell = value.closest("td, th");
    const boundary = cell?.getBoundingClientRect();
    let hidden = false;
    let clipped = false;
    let accessible = boxes.map((box) => ({
      left: box.left,
      right: box.right,
      top: box.top,
      bottom: box.bottom,
    }));
    /** @type {Element | null} */
    let node = value;
    for (; node; node = node.parentElement) {
      const style = getComputedStyle(node);
      hidden ||=
        style.display === "none" || style.visibility !== "visible" || Number(style.opacity) === 0;
      const box = node.getBoundingClientRect();
      for (const ink of accessible) {
        clipped ||=
          (["hidden", "clip"].includes(style.overflowX) &&
            (box.left - ink.left > 1 || ink.right - box.right > 1)) ||
          (["hidden", "clip"].includes(style.overflowY) &&
            (box.top - ink.top > 1 || ink.bottom - box.bottom > 1));
      }
      // A reader can scroll to ink beyond this port. Only the port itself can
      // be clipped by outer ancestors; hidden inner clips above still refuse.
      accessible = accessible.map((ink) => {
        const x = ["auto", "scroll"].includes(style.overflowX);
        const y = ["auto", "scroll"].includes(style.overflowY);
        const left = x ? Math.max(box.left, Math.min(box.right, ink.left)) : ink.left;
        const top = y ? Math.max(box.top, Math.min(box.bottom, ink.top)) : ink.top;
        return {
          left,
          top,
          right: x ? Math.max(left, Math.min(box.right, ink.right)) : ink.right,
          bottom: y ? Math.max(top, Math.min(box.bottom, ink.bottom)) : ink.bottom,
        };
      });
    }
    const cellOverlap =
      boundary &&
      boxes.some((box) => boundary.left - box.left > 1 || box.right - boundary.right > 1);
    if (hidden || clipped || cellOverlap) {
      lostInk.push({
        source: value.textContent.slice(0, 100),
        hidden,
        clipped,
        cellOverlap: Boolean(cellOverlap),
      });
    }
  }
  const mathScrollRegions = [...document.querySelectorAll(".kpress-math-display, .entry-equation")]
    .filter((el) => el.scrollWidth - el.clientWidth > 1)
    .map((el) => ({
      width: el.clientWidth,
      contentWidth: el.scrollWidth,
      overflow: getComputedStyle(el).overflowX,
      keyboardReachable: el.getAttribute("tabindex") === "0",
    }));
  const headings = [...document.querySelectorAll("h3")].map((heading) => heading.textContent ?? "");
  return {
    viewport: root.clientWidth,
    pageOverflow: root.scrollWidth - root.clientWidth,
    theme: root.getAttribute("data-kpress-resolved-theme"),
    bodyFontPx: parseFloat(getComputedStyle(document.body).fontSize),
    tables,
    mathScrollRegions,
    checkedInk: values.length,
    lostInkCount: lostInk.length,
    lostInk: lostInk.slice(0, 5),
    fractions,
    currentPolynomials: headings.filter((heading) => heading.startsWith("Current polynomial for"))
      .length,
    historicalPolynomials: headings.filter((heading) =>
      heading.startsWith("Historical polynomial for"),
    ).length,
    mathHosts: document.querySelectorAll(".kpress-math, #entry-equation math").length,
    nativeMath: document.querySelectorAll("math").length,
    mathErrors: document.querySelectorAll(".katex-error, math merror").length,
    coefficients: [...document.querySelectorAll("td code")].filter((code) =>
      /^[+-]?\d+$/.test(code.textContent ?? ""),
    ).length,
  };
};
