// The injected fault's formula as the exporter left it, read just before its browser closes.
() => {
  const target = /** @type {HTMLElement | null} */ (
    document.querySelector("[data-pdf-math-fault]")
  );
  const semantic = target?.querySelector(".kpress-math-semantic math");
  const render = /** @type {HTMLElement | null | undefined} */ (
    target?.querySelector(".kpress-math-render")
  );
  /** @param {Element | null | undefined} node */
  const visible = (node) =>
    !!node &&
    node.checkVisibility({ opacityProperty: true, visibilityProperty: true }) &&
    !!node.getClientRects().length;
  return {
    target_found: !!target,
    source: globalThis.pdfMathFaultSource,
    math_ready: document.documentElement.classList.contains("math-ready"),
    host_ready: (render || target)?.dataset.squaresMathReady,
    visible: visible(target),
    semantic_visible: visible(semantic),
    raw_box_visible: visible(render),
    visible_text: target?.innerText,
    raw_text: target?.textContent,
    katex_count: target?.querySelectorAll(".katex").length,
    waits: (globalThis.kpressMathFaceWait || [])
      .filter((entry) => entry.request.includes("PDF Math Fault Control"))
      .map((entry) => entry.outcome),
  };
};
