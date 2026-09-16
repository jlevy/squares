// Figure 5's layout at one screen width: geometry and computed type sizes, rather than a
// match on the stylesheet that intended them. The active certificate is checked at each
// width. Returns one line per defect found.
//
// Takes `math`, the math library (`math/library.js`), through a handle.
/** @param {{ math: SquaresMathProbes }} o */
(o) => {
  /** @type {string[]} */
  const found = [];
  const { activeVariant } = o.math;
  for (const figure of document.querySelectorAll('figure[data-figure="5"]')) {
    if (!figure.getClientRects().length) {
      continue;
    }
    const panel = /** @type {Element} */ (figure.querySelector(".panel"));
    const stage = /** @type {Element} */ (figure.querySelector(".stage"));
    if (panel.getBoundingClientRect().top < stage.getBoundingClientRect().bottom - 1) {
      found.push("control panel is beside the graphic");
    }
    const { left, right } = panel.getBoundingClientRect();
    for (const item of figure.querySelectorAll(".math-item")) {
      if (getComputedStyle(item).whiteSpace !== "nowrap") {
        found.push("a direction item permits an internal line break");
      }
      const ink = activeMath(item, ".katex-html") || item;
      const box = ink.getBoundingClientRect();
      if (box.left < left - 1 || box.right > right + 1) {
        found.push("a direction item overflows the control panel");
      }
      const math = activeMath(item, ".katex");
      if (math?.querySelector(".mfrac")) {
        fraction(math, "half-tangent");
      }
    }
    if (!figure.querySelector(".math-item")) {
      found.push("direction items are missing");
    }
    fraction(activeMath(figure, ".mass-val .katex"), "mass");
    for (const hidden of figure.querySelectorAll("[hidden]")) {
      if (hidden.getClientRects().length) {
        found.push("a hidden status or verdict still occupies a visible box");
      }
    }
  }
  return found;

  /**
   * @param {Element} root
   * @param {string} selector
   */
  function activeMath(root, selector) {
    return [...root.querySelectorAll(selector)].find(activeVariant);
  }

  /**
   * @param {Element | undefined} mass
   * @param {string} label
   */
  function fraction(mass, label) {
    if (!mass) {
      found.push(`the ${label} math is missing`);
      return;
    }
    const digits = [...mass.querySelectorAll(".katex-html .mfrac .mord")].filter(
      (el) => !el.children.length && /[0-9]/.test(el.textContent),
    );
    const size = parseFloat(getComputedStyle(mass).fontSize);
    if (
      !digits.length ||
      digits.some((el) => parseFloat(getComputedStyle(el).fontSize) < size * 0.95)
    ) {
      found.push(`the ${label} fraction has reduced-size numerator or denominator`);
    }
  }
};
