// Write a mark on one identity's element, so a later read says whether it survived.
// Takes {identity, mark}.
(o) => {
  /** @type {SVGGElement} */ (
    document.querySelector(`#squares g[data-identity="${o.identity}"]`)
  ).dataset.probe = o.mark;
};
