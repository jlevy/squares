// Watch every formula not yet submitted for `observationMs` of animation frames, and report
// any whose active formula becomes exposed. With `broken`, the queued markers that should
// protect those formulas are removed first, as the negative control. `math` is
// `math/library.js`'s helpers.
/** @param {{ broken: boolean, math: SquaresMathProbes, observationMs: number }} o */
async (o) => {
  // The real head watchdog has expired while initial work and font
  // transfers remain held. Its fallback must not expose queued math.
  if (o.broken) {
    for (const node of /** @type {NodeListOf<HTMLElement>} */ (
      document.querySelectorAll("[data-squares-math-queued]")
    )) {
      delete node.dataset.squaresMathQueued;
    }
  }
  const { activeVariant: active, exposed } = o.math;
  const waiting = [
    .../** @type {NodeListOf<HTMLElement>} */ (
      document.querySelectorAll(".tex, .tex-d, .kpress-math")
    ),
  ].filter((node) => {
    const box = node.classList.contains("kpress-math")
      ? /** @type {HTMLElement | null} */ (node.querySelector(".kpress-math-render"))
      : node;
    return (
      box &&
      !box.dataset.done &&
      node.getClientRects().length &&
      !box.matches("[data-kpress-math-pending]") &&
      !box.querySelector("[data-kpress-math-pending]")
    );
  });
  globalThis.__squaresQueuedControlNodes = waiting;
  /** @type {Set<HTMLElement>} */
  const visible = new Set();
  const end = performance.now() + o.observationMs;
  let frames = 0;
  do {
    await new Promise((done) => requestAnimationFrame(done));
    frames++;
    for (const node of waiting) {
      const formulas = [...node.querySelectorAll(".katex,.kpress-math-semantic")].filter(active);
      if (formulas.some(exposed)) {
        visible.add(node);
      }
    }
  } while (performance.now() < end);
  return {
    delayed_batches: /** @type {SquaresQueueControl} */ (__squaresQueueControl).count,
    root_pending: document.documentElement.hasAttribute("data-kpress-math-pending"),
    unsubmitted_formulas: waiting.length,
    observed_ms: performance.now(),
    frames,
    target_classes: Object.fromEntries(
      ["tex", "tex-d", "kpress-math"].map((name) => [
        name,
        waiting.filter((node) => node.classList.contains(name)).length,
      ]),
    ),
    exposed: [...visible].map(
      (node) =>
        node.dataset.kpressMathSource ||
        /** @type {HTMLElement | null} */ (node.querySelector(".kpress-math-render"))?.dataset
          .kpressMathSource ||
        /** @type {string} */ (node.textContent).trim().slice(0, 100),
    ),
  };
};
