// A name for an element that is readable in a failure: the tag, its classes, and its
// index among its siblings, up to the page wrapper. The same shape `check_print_layout`
// reports its findings with, so two print findings about one element read alike.
//
// A reference probe, handed to both of this tool's page probes as `sig` rather than written
// into each, so a path in the listing and a path in a `--check` failure name the same
// element the same way.
/** @returns {(el: Element) => string} */
() =>
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
  };
