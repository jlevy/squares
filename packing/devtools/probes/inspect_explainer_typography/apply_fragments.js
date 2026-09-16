// Puts the math preparation's fragments into their keyed slots, as the publication build
// does: each slot's contents replaced by the prepared HTML, its attributes set, and its key
// removed.
/** @param {TypographyMathFragment[]} fragments */
(fragments) => {
  for (const fragment of fragments) {
    const target = /** @type {Element} */ (
      document.querySelector(`[data-squares-math-key="${fragment.key}"]`)
    );
    target.innerHTML = fragment.html;
    for (const [name, value] of Object.entries(fragment.attributes)) {
      target.setAttribute(name, value);
    }
    target.removeAttribute("data-squares-math-key");
  }
};
