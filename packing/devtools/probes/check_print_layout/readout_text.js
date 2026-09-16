// A typeset readout's text, read from its text nodes rather than from Chromium's
// rendered-text collection (`_readout_text` says why). Glyph and raw fallback text come
// from the active font profile only: dormant prepared variants and the clipped MathML
// annotation cannot supply an expected value when the displayed formula is wrong.
//
// Takes the readout, then `math`, the math library (`math/library.js`), through a handle.
/**
 * @param {Element} el
 * @param {{ math: SquaresMathProbes }} o
 */
(el, o) => {
  const { activeVariant } = o.math;
  const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
  let text = "";
  for (let node = walker.nextNode(); node; node = walker.nextNode()) {
    const parent = node.parentElement;
    if (parent && activeVariant(parent) && !parent.closest(".katex-mathml")) {
      text += node.textContent;
    }
  }
  return text;
};
