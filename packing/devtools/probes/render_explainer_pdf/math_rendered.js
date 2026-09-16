// A completed render can be a recovered failure: the host replaces a failed `.tex`
// formula with its source and marks it ready. Repeated PDFs then agree on raw TeX.
// Inspect the final print DOM as well as waiting for it. Native KPress formulas may
// retain readable semantic MathML, provided their source box remains hidden.
// Successful KaTeX keeps TeX in accessibility annotations, so source-text regexes
// would reject valid formulas. Geometry and clipping distinguish the painted output
// from hidden variants and the clipped semantic copy beside successful KaTeX.
//
// `math` is `math/library.js`, whose `exposed` is the geometry and clipping check.
/** @param {{ math: SquaresMathProbes }} o */
({ math }) => {
  const { exposed } = math;
  const selector = ".tex,.tex-d,.kpress-math,[data-squares-math-ready]";
  const failures = [];
  for (const [index, host] of [
    .../** @type {NodeListOf<HTMLElement>} */ (document.querySelectorAll(selector)),
  ].entries()) {
    // The outer host owns its active prepared variant and native source box. A
    // display:none print alternative has no layout; pending visibility:hidden
    // formulas still have layout and must pass the output checks below.
    if (host.parentElement?.closest(selector) || !host.getClientRects().length) {
      continue;
    }
    /** @param {string} query */
    const hasVisible = (query) => [...host.querySelectorAll(query)].some(exposed);
    const native = host.matches(".kpress-math");
    const raw = /** @type {HTMLElement | null} */ (host.querySelector(".kpress-math-render"));
    const semantic = hasVisible("math.kpress-math-semantic, .kpress-math-semantic math");
    const pending =
      host.closest("[data-squares-math-queued]") ||
      host.querySelector("[data-squares-math-queued]");
    const error = hasVisible(".katex-error, merror");
    const readable =
      native && host.dataset.kpressMathRendered !== "true"
        ? semantic && (!raw || !exposed(raw))
        : hasVisible(".katex-html") && (!native || !semantic);
    if (!pending && !error && readable) {
      continue;
    }
    const source =
      host.dataset.kpressMathSource || raw?.dataset.kpressMathSource || host.textContent || "";
    failures.push(
      `${index} (${host.className || host.tagName}): ${source.replace(/\s+/g, " ").slice(0, 160)}`,
    );
  }
  if (failures.length) {
    throw new Error(
      `unrendered math in ${failures.length} printed formulas: ${failures.slice(0, 8).join("; ")}`,
    );
  }
};
