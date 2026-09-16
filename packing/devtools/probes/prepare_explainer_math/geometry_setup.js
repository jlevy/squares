// Number every reserved box by the formula it belongs to and by its own key, and keep the
// laid-out ones as `__squaresGeometryBoxes` for the snapshots to measure.
() => {
  let group = 0;
  for (const formula of document.querySelectorAll(".katex-html")) {
    for (const box of /** @type {NodeListOf<HTMLElement>} */ (
      formula.querySelectorAll(":scope > .squares-math-box")
    )) {
      box.dataset.squaresGeometryGroup = String(group);
    }
    group++;
  }
  globalThis.__squaresGeometryBoxes = [
    .../** @type {NodeListOf<HTMLElement>} */ (document.querySelectorAll(".squares-math-box")),
  ].filter((box) => box.getBoundingClientRect().width > 0);
  globalThis.__squaresGeometryBoxes.forEach((box, key) => {
    box.dataset.squaresGeometryKey = String(key);
  });
};
