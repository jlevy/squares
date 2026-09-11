// A shifted drag turns the held square about its own centre. o.n is the size, o.at where
// the square is, o.grab where the cursor takes hold, o.first and o.second where it goes.
(o) => {
  const api = window.atlasTransitions;
  api.setStepN(o.n);
  api.setInitial('grid');
  const j = api.pickAt(o.at[0], o.at[1]);
  api.grab(j, o.grab[0], o.grab[1]);
  const a = api.dragTo(o.first[0], o.first[1], true);
  const b = api.dragTo(o.second[0], o.second[1], true);
  api.release();
  return {a, b};
}
