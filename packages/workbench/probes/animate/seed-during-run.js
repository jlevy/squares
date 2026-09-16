// A new seed while the hand's open-ended run is playing: the run belongs to the old seed, so the
// page must stop it rather than leave the clock running with no run behind it. o.n is the step.
/** @param {{n: number}} o */
(o) => {
  const api = window.atlasTransitions;
  api.pause();
  api.setStepN(o.n);
  api.seek(api.duration());
  api.grab(0);
  api.release();
  api.play();
  const read = () => {
    const s = api.state();
    return { playing: s.playing, optimizing: s.optimizing, seed: s.seed };
  };
  const before = read();
  api.setSeed(3);
  const after = read();
  api.pause();
  api.setSeed(0);
  return { before, after };
};
