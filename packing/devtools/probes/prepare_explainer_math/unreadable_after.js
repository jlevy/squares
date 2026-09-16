// The formulas the queue-watchdog control held that are still unreadable once the fonts and
// batches are released: no exposed active formula, or, where there is no formula, no exposed
// text. `math` is `math/library.js`'s helpers.
/** @param {{ math: SquaresMathProbes }} o */
(o) => {
  const { exposed, activeVariant: active } = o.math;
  return /** @type {HTMLElement[]} */ (__squaresQueuedControlNodes)
    .filter((node) => {
      const formulas = [...node.querySelectorAll(".katex,.kpress-math-semantic")].filter(active);
      return formulas.length
        ? !formulas.some(exposed)
        : !(/** @type {string} */ (node.textContent).trim()) || !exposed(node);
    })
    .map(
      (node) =>
        node.dataset.kpressMathSource || /** @type {string} */ (node.textContent).slice(0, 80),
    );
};
