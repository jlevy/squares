// Self-test: the bold run draws `D`, and KPress's 650 table holds exactly the advance it
// measures. `fontAdvance` is `font_advance.js`'s measurement.
/** @param {{ fontAdvance: (element: Element) => number }} o */
({ fontAdvance }) => {
  const bold = /** @type {HTMLElement} */ (document.querySelector(".mathbf"));
  bold.textContent = "D";
  // Reproduce Linux's small-glyph rounding without depending on the
  // host rasterizer. Measuring the original run again must not pass.
  const bounding = bold.getBoundingClientRect.bind(bold);
  bold.getBoundingClientRect = () => {
    const rect = bounding();
    return new DOMRect(rect.x, rect.y, Math.round(rect.width), rect.height);
  };
  const advance = fontAdvance(bold);
  globalThis.kpressKatexTextMetrics = {
    sans: { "Main-Bold": { 68: [0, 0, 0, 0, advance] } },
  };
};
