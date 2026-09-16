// Pause the playing run and report where it got to.
() => {
  const A = window.atlasTransitions;
  A.pause();
  return A.optimizeState();
};
