// Walk a range's scope by hand: the run must not carry past the range's last pair.
// o.lo and o.hi are the range's two ends, o.step the step to walk to.
(o) => {
  const api = window.atlasTransitions;
  api.setRange(o.lo, o.hi);
  api.playRange();
  api.pause();
  api.goTo(o.step);
  api.seek(api.duration() - 0.001);
  return {n: api.state().n, last: api.range().to};
}
