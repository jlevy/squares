// The original font-line-strut bug, put back into the prepared baseline fixture: every base
// given a 1.2 line height and the `.strut` style KaTeX first drew, from
// `baselineOriginalStruts`.
/** @param {Element} caption */
(caption) => {
  const targets = [...caption.querySelectorAll(".tex")];
  for (const [index, target] of targets.entries()) {
    const bases = [.../** @type {NodeListOf<HTMLElement>} */ (target.querySelectorAll(".base"))];
    for (const [part, base] of bases.entries()) {
      base.style.setProperty("line-height", "1.2", "important");
      const strut = /** @type {Element} */ (base.querySelector(":scope > .strut"));
      const original = /** @type {(string | null)[][]} */ (baselineOriginalStruts)[index];
      strut.setAttribute("style", /** @type {string} */ (/** @type {string[]} */ (original)[part]));
    }
  }
};
