// The run's state, read and then stopped where it stands.
() => {
  const api = window.atlasTransitions;
  const state = api.optimizeState();
  api.pause();
  return state;
};
