// Reset, which is the other control: it puts the parameters back and leaves the picture.
// o.n is the size, o.steps how far the run is taken first.
(o) => {
  const api = window.atlasTransitions;
  api.setMode('pack');
  api.setStepN(o.n);
  api.setInitial('grid');
  api.setLawPreset('sticky');
  api.optimizeStep(o.steps);
  const before = {steps: api.optimizeState().steps, pull: api.law().attraction};
  api.reset();
  return {before, reset: {steps: api.optimizeState().steps, pull: api.law().attraction,
                          playing: api.state().playing}};
}
