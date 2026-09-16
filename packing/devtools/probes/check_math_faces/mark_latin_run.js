// One letter or digit of a formula, marked so CDP can find it: gives the first childless
// `.mord` run of letters, digits or points in a visible, active formula under `scope` the id
// `mark`, and returns its text, or null. The composite claims the Latin ranges and the digits
// and nothing else, so a run of operators or Greek would answer with a KaTeX face whichever
// composite is in force and prove nothing. `math` is `math/library.js`'s helpers.
/** @param {{ scope: string, mark: string, math: SquaresMathProbes }} o */
({ scope, mark, math }) => {
  const { activeVariant } = math;
  for (const node of document.querySelectorAll(scope)) {
    if (!activeVariant(node)) {
      continue;
    }
    if (!node.checkVisibility({ visibilityProperty: true })) {
      continue;
    }
    for (const run of node.querySelectorAll(".mord")) {
      const text = /** @type {string} */ (run.textContent);
      if (run.children.length === 0 && /^[0-9A-Za-z.]+$/.test(text.trim())) {
        run.id = mark;
        return text.trim();
      }
    }
  }
  return null;
};
