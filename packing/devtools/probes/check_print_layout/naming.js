// How every row of the layout probe names an element, and the precision it reports at.
// `sig` is a name that is stable across the two passes and readable in a failure: the tag,
// its classes, and its index among its siblings, up to the page wrapper. `round` keeps two
// decimal places, and counts a measurement that is not a number as zero.
//
// A reference probe, handed to `layout.js` and `layout_helpers.js` through a handle rather
// than written into each, so the two name one element the same way and the Node tests can
// run the helpers with a stand-in `sig`.
/** @returns {PrintLayoutNaming} */
() => {
  return { sig, round };

  /** @param {number} v */
  function round(v) {
    return Math.round((v || 0) * 100) / 100;
  }

  /** @param {Element} el */
  function sig(el) {
    const steps = [];
    for (
      let node = /** @type {Element | null} */ (el), depth = 0;
      node && depth < 3;
      node = node.parentElement, depth++
    ) {
      const parent = node.parentElement;
      const nth = parent ? [...parent.children].indexOf(node) : 0;
      const cls = [...node.classList].join(".");
      steps.unshift(`${node.tagName.toLowerCase()}${cls ? `.${cls}` : ""}[${nth}]`);
      if (node.classList.contains("kpress")) {
        break;
      }
    }
    return steps.join(" > ");
  }
};
