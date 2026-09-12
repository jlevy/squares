// The measured side before and after a drag. o.n is the size, o.at where the square is,
// o.to where it is dragged.
(o) => {
  const api = window.atlasTransitions;
  api.setStepN(o.n);
  api.setInitial("grid");
  const before = api.gapBar().side;
  const k = api.pickAt(o.at[0], o.at[1]);
  api.grab(k, o.at[0], o.at[1]);
  api.dragTo(o.to[0], o.to[1], false);
  const after = api.gapBar().side;
  api.release();
  return { before, after };
};
