// Self-test: mark both paragraphs' formulas sans, which is wrong for the serif one.
() => {
  /** @type {HTMLElement} */ (document.querySelector("#a")).dataset.kpressMathFace = "sans";
  /** @type {HTMLElement} */ (document.querySelector("#b")).dataset.kpressMathFace = "sans";
};
