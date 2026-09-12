// Hold a square and drag it: it must follow the cursor exactly and its neighbours must be
// pushed aside. o.n is the size, o.steps how far the run is taken first and o.settle how
// far after the drag; o.at is where the square is, o.to where it goes, o.neighbour where
// the square next door sits.
(o) => {
  const api = window.atlasTransitions;
  api.setStepN(o.n);
  api.setInitial("grid");
  api.optimizeStep(o.steps);
  const i = api.pickAt(o.at[0], o.at[1]);
  api.grab(i, o.at[0], o.at[1]);
  api.dragTo(o.to[0], o.to[1], false);
  const neighbour = api.pickAt(o.neighbour[0], o.neighbour[1]);
  api.optimizeStep(o.settle);
  const out = {
    i,
    held: api.hand().held,
    stillThere: api.pickAt(o.to[0], o.to[1]) === i,
    neighbourMoved: api.pickAt(o.neighbour[0], o.neighbour[1]) !== neighbour,
  };
  out.dropped = api.release();
  out.after = api.hand().held;
  return out;
};
