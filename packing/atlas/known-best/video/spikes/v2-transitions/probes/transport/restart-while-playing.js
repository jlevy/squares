// Restart a run that is playing: it goes back to the top and keeps rolling.
() => {
  const api = window.atlasTransitions;
  const was = api.state().playing;
  api.restart();
  return {was, playing: api.state().playing, steps: api.optimizeState().steps};
}
