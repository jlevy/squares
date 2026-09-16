// Every connected reserved box: its outer geometry and baseline, the intrinsic width, text,
// size and rendering of the glyphs inside it, and whether it is hidden.
() =>
  /** @type {HTMLElement[]} */ (globalThis.__squaresGeometryBoxes)
    .filter((box) => box.isConnected)
    .map((box) => {
      const rect = box.getBoundingClientRect(),
        style = getComputedStyle(box);
      const base = /** @type {Element} */ (box.firstElementChild),
        baseStyle = getComputedStyle(base);
      return {
        key: Number(box.dataset.squaresGeometryKey),
        group: Number(box.dataset.squaresGeometryGroup),
        x: rect.x,
        y: rect.y,
        width: rect.width,
        height: rect.height,
        baseline: rect.bottom + parseFloat(style.verticalAlign),
        intrinsic_width: base.getBoundingClientRect().width,
        text: base.textContent,
        font_size: parseFloat(baseStyle.fontSize),
        text_rendering: baseStyle.textRendering,
        native_linear_metrics: document.documentElement.dataset.squaresNativeMathMetrics === "true",
        hidden: style.visibility === "hidden",
      };
    });
