// Click the quick-pick chip for this size, and say what range it set. o.n is the size.
/** @param {{n: number}} o */ (o) => {
  /** @type {HTMLButtonElement} */ (
    document.querySelector(`#step-chips button[data-n="${o.n}"]`)
  ).click();
  return window.atlasTransitions.range();
};
