// The gap bar through one step's dwell, where the arriving square is not drawn yet: at each
// sampled instant before `schedule().arrive`, what the bar says about which n it measures, the
// record it compares against, the side it read and whether it calls the arrangement a packing.
// o.n is the step's n (the step n - 1 -> n).
/** @param {{n: number}} o */
(o) => {
  const api = window.atlasTransitions;
  api.pause();
  api.setStepN(o.n);
  const arrive = api.schedule().arrive;
  return [0, arrive / 2, Math.max(0, arrive - 1e-3)].map((t) => {
    api.seek(t);
    const g = api.gapBar();
    return { t, n: g.n, record: g.record, side: g.side, valid: g.valid };
  });
};
