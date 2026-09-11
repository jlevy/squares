// Click the quick-pick chip for this size, and say what range it set. o.n is the size.
(o) => {
  document.querySelector('#step-chips button[data-n="' + o.n + '"]').click();
  return window.atlasTransitions.range();
}
