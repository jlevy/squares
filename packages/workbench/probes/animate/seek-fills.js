// The fills of one instant reached three ways: seeking straight to it from the dwell, walking to
// it from the start of the step in o.walk seeks, and seeking to it again after scrubbing past it
// and back. A frame is a function of its instant, so all three must agree. o.n is the step's n,
// o.at the instant as a fraction of the step.
/** @param {{n: number, at: number, walk: number}} o */
(o) => {
  const api = window.atlasTransitions;
  api.pause();
  api.setStepN(o.n);
  const t = api.duration() * o.at;
  api.seek(t);
  const direct = api.colour().fills;
  api.seek(0);
  for (let k = 1; k <= o.walk; k++) {
    api.seek((t * k) / o.walk);
  }
  const walked = api.colour().fills;
  api.seek(api.duration() * 0.95);
  api.seek(api.duration() * 0.3);
  api.seek(t);
  const again = api.colour().fills;
  return { direct, walked, again };
};
