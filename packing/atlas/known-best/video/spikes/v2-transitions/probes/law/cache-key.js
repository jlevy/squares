// The free run each of four laws draws, in order, with the shipped law set between them:
// the cache is keyed rather than cleared, so coming back to a law gives what it gave before.
// o.n is the size, o.presets the laws to walk.
(o) => {
  const api = window.atlasTransitions;
  api.setStepN(o.n);
  const i = api.state().pair;
  const out = {};
  for (const key of Object.keys(o.presets)) {
    api.setLawPreset(o.presets[key]);
    out[key] = JSON.stringify(api.physics(i, "bodies", "free").miss);
  }
  api.setLawPreset("default");
  return out;
};
