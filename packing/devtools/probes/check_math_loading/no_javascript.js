// With JavaScript disabled: counts the intended formulas in readable surrounding content, and
// how many of them have no readable fallback. Native MathML, raw TeX, and prepared KaTeX are
// alternative readable fallbacks. `math` is `math/library.js`.
/** @param {{ math: SquaresMathProbes }} o */
({ math }) => {
  const { exposed, activeVariant } = math;
  /** @param {string} selector */
  const visible = (selector) =>
    [...document.querySelectorAll(selector)].filter(activeVariant).filter(exposed).length;
  const wrappers = '.kpress-math,.tex,.tex-d,[data-kpress-math-prepared="true"]';
  /** @param {Element} node */
  const raw = (node) =>
    node.matches(".tex,.tex-d") &&
    !node.querySelector(".katex") &&
    !!(/** @type {string} */ (node.textContent).trim()) &&
    exposed(node);
  /** @param {Element} node */
  const prepared = (node) =>
    [...node.querySelectorAll(".katex-html")]
      .filter(activeVariant)
      .some((html) => /** @type {string} */ (html.textContent).trim() && exposed(html));
  /** @param {Element} node */
  const native = (node) =>
    [...node.querySelectorAll(".kpress-math-semantic")].filter(activeVariant).some(exposed);
  const targets = [...document.querySelectorAll(wrappers)].filter(activeVariant).filter((node) => {
    // Judge every intended formula in readable surrounding content. Filtering on
    // the formula's own box would silently discard clipped or empty fallbacks.
    const parent = /** @type {Element} */ (node.parentElement);
    return !parent.closest(wrappers) && exposed(parent);
  });
  return {
    raw_tex: targets.filter(raw).length,
    native_math: visible(".kpress-math-semantic"),
    prepared_math: visible(".katex-html"),
    math_wrappers: targets.length,
    unreadable_math: targets.filter((node) => !raw(node) && !prepared(node) && !native(node))
      .length,
  };
};
