// How many steps the run has taken, read and then stopped where it stands.
() => {
  const api = window.atlasTransitions;
  const steps = api.optimizeState().steps;
  api.pause();
  return steps;
}
