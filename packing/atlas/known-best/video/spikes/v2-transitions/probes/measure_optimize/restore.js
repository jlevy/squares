// Put the speed back to 1 and the start back to `previous`.
() => {
  window.atlasTransitions.setSpeed(1);
  return window.atlasTransitions.setInitial("previous");
};
