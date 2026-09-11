// A grab made while a run is playing must leave it playing. o.n is the size, o.x and o.y
// where the square is reached for.
(o) => {
  const api = window.atlasTransitions;
  api.setInitial('previous');
  api.setStepN(o.n);
  api.seek(0);
  api.play();
  const m = api.pickAt(o.x, o.y);
  api.grab(m, o.x, o.y);
  const out = {held: api.hand().held, playing: api.state().playing, optimizing: api.state().optimizing};
  api.release();
  api.pause();
  return out;
}
