// The mark left on one identity's element, if its element is the same one. Takes {identity}.
/** @param {{identity: number}} o */ (o) =>
  /** @type {SVGGElement} */ (document.querySelector(`#squares g[data-identity="${o.identity}"]`))
    .dataset.probe;
