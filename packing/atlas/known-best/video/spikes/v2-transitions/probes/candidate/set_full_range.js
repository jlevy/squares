// Open the range back to everything the page carries, which progress is measured over.
() => {
  const A = window.atlasTransitions;
  A.setRange(A.range().min, A.range().max);
}
