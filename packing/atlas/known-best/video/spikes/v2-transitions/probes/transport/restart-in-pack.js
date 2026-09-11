// Restart in Pack: the run goes back to its start and every setting stays. o.n is the size,
// o.steps how far the run is taken first, o.anneal the dial to leave it on.
(o) => {
  const api = window.atlasTransitions;
  api.setMode('pack');
  api.setStepN(o.n);
  api.setInitial('grid');
  api.setLawPreset('sticky');
  api.setAnneal(o.anneal);
  api.optimizeStep(o.steps);
  const before = {steps: api.optimizeState().steps, pull: api.law().attraction, anneal: api.anneal().level};
  const said = api.restart();
  return {before, said, after: {steps: api.optimizeState().steps, on: api.optimizeState().on,
                                pull: api.law().attraction, anneal: api.anneal().level,
                                playing: api.state().playing}};
}
