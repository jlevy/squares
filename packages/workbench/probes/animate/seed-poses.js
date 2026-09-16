// The drawn poses of one mid-move instant under each seed in turn, in the physical style. The
// shake is seeded, so one seed must replay exactly and another must differ. o.n is the step's
// n, o.at the instant as a fraction of the step, o.seeds the seeds in order.
/** @param {{n: number, at: number, seeds: number[]}} o */
(o) => {
  const api = window.atlasTransitions;
  api.pause();
  api.setStyle("physics");
  api.setStepN(o.n);
  const poses = o.seeds.map((seed) => {
    api.setSeed(seed);
    api.seek(api.duration() * o.at);
    const out = [];
    for (let i = 0; i < o.n; i++) {
      out.push(api.poseOf(i));
    }
    return { seed: api.seed(), poses: out };
  });
  api.setSeed(0);
  return poses;
};
