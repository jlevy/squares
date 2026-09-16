// The drawn poses at the end of one step, where the stage is at rest. o.n is the step's n.
/** @param {{n: number}} o */
(o) => {
  const api = window.atlasTransitions;
  api.pause();
  api.setStepN(o.n);
  api.seek(api.duration());
  const poses = [];
  for (let i = 0; i < o.n; i++) {
    poses.push(api.poseOf(i));
  }
  return poses;
};
