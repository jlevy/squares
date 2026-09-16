// Whether the visible mathematics is completely prepared. Every visible math target needs a
// formula and every base of a visible formula its own reserved box; CSS must display exactly
// one variant, the reader's, of each variant set; and no ID may repeat.
() => {
  const root = document.documentElement.dataset;
  const preference =
    (root.kpressFontSet === "system" ? "system" : "custom") +
    "-" +
    (root.kpressProseFont === "sans" ? "sans" : "serif");
  const parents = new Set(
    [...document.querySelectorAll(".squares-math-variant")].map(
      (node) => /** @type {HTMLElement} */ (node.parentElement),
    ),
  );
  /** @type {string[]} */
  const variant_errors = [];
  for (const parent of parents) {
    const displayed = [
      .../** @type {NodeListOf<HTMLElement>} */ (
        parent.querySelectorAll(":scope > .squares-math-variant")
      ),
    ].filter((node) => getComputedStyle(node).display !== "none");
    if (
      displayed.length !== 1 ||
      !displayed[0]?.dataset.squaresMathContexts?.split(/\s+/).includes(preference)
    ) {
      variant_errors.push(parent.dataset.kpressMathSource || parent.id);
    }
  }
  /** @type {Set<string>} */
  const ids = new Set();
  /** @type {string[]} */
  const duplicate_ids = [];
  for (const node of document.querySelectorAll("[id]")) {
    if (ids.has(node.id)) {
      duplicate_ids.push(node.id);
    }
    ids.add(node.id);
  }
  const targets = [
    .../** @type {NodeListOf<HTMLElement>} */ (
      document.querySelectorAll("[data-kpress-math-source]")
    ),
  ].filter((node) => node.getClientRects().length);
  const formulas = [
    ...new Set(
      targets.flatMap((node) =>
        [...node.querySelectorAll(".katex-html")].filter(
          (formula) => formula.getClientRects().length,
        ),
      ),
    ),
  ];
  /** @type {(string | null | undefined)[]} */
  const missing = targets
    .filter((node) => !formulas.some((formula) => node.contains(formula)))
    .map((node) => node.dataset.kpressMathSource);
  /** @type {(string | null | undefined)[]} */
  const unreserved = [];
  let bases = 0;
  for (const formula of formulas) {
    const parts = [...formula.querySelectorAll(".base")];
    if (!parts.length) {
      missing.push(formula.textContent);
    }
    for (const base of parts) {
      bases++;
      const box = /** @type {HTMLElement} */ (base.parentElement);
      if (!box.classList.contains("squares-math-box") || box.parentElement !== formula) {
        unreserved.push(
          /** @type {HTMLElement | null} */ (formula.closest("[data-kpress-math-source]"))?.dataset
            .kpressMathSource || formula.textContent,
        );
      }
    }
  }
  return {
    targets: targets.length,
    formulas: formulas.length,
    bases,
    missing,
    unreserved,
    variant_errors,
    duplicate_ids,
  };
};
