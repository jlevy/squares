// For the first three `.kpress-math` formulas, whether each shows its native semantic MathML
// readably, with no KaTeX render left in place.
() =>
  [...document.querySelectorAll(".kpress-math")].slice(0, 3).map((node) => {
    const semantic = node.querySelector(".kpress-math-semantic");
    if (!semantic) {
      return false;
    }
    const style = getComputedStyle(semantic);
    const box = semantic.getBoundingClientRect();
    return (
      !(/** @type {HTMLElement} */ (node).dataset.kpressMathRendered) &&
      !node.querySelector(".katex") &&
      style.clipPath === "none" &&
      style.visibility !== "hidden" &&
      box.width > 1 &&
      box.height > 1
    );
  });
