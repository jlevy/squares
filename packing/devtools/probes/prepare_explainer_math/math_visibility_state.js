// A diagnostic of the after-state: the root's data attributes, the queued and pending
// markers, how many active formulas are still hidden, every declared face, and the ancestor
// chain of up to three hidden formulas. `math` is `math/library.js`'s helpers.
/** @param {{ math: SquaresMathProbes }} o */
(o) => {
  const { activeVariant: active } = o.math;
  const maths = [...document.querySelectorAll(".katex,.squares-math-box")]
    .filter(active)
    .filter((node) => node.getClientRects().length);
  const hidden = maths.filter((node) => getComputedStyle(node).visibility === "hidden");
  return {
    at_ms: performance.now(),
    root: { ...document.documentElement.dataset },
    queued: document.querySelectorAll("[data-squares-math-queued]").length,
    pending: document.querySelectorAll("[data-kpress-math-pending]").length,
    hidden: hidden.length,
    fonts: [...document.fonts].map((face) => ({
      family: face.family,
      weight: face.weight,
      style: face.style,
      status: face.status,
    })),
    samples: hidden.slice(0, 3).map((math) => {
      const chain = [];
      for (
        let node = /** @type {HTMLElement | null} */ (math);
        node && node !== document.body;
        node = node.parentElement
      ) {
        const style = getComputedStyle(node);
        chain.push({
          classes: node.className,
          style: node.getAttribute("style"),
          data: { ...node.dataset },
          visibility: style.visibility,
          family: style.fontFamily,
        });
      }
      return { text: /** @type {string} */ (math.textContent).slice(0, 100), chain };
    }),
  };
};
