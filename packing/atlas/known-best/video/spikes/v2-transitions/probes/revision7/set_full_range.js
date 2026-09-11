// Open the range back to everything the page carries, which is what progress is measured over.
() => {
  const A = window.atlasTransitions;
  A.setRange(A.range().min, A.range().max);
}
