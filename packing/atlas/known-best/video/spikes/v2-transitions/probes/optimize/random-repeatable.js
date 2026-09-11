// Ask for the random start twice over, through another start, and report what it needs.
() => {
  const api = window.atlasTransitions;
  api.setInitial('previous');
  api.setInitial('random');
  return api.optimizeState().required;
}
