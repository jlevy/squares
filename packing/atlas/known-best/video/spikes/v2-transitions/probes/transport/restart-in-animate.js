// Restart in Animate: the beginning is the first step of the range, not this step's own
// zero. o.lo and o.hi are the range, o.at the step to go to, o.t how far into it.
(o) => {
  const api = window.atlasTransitions;
  api.setMode('animate');
  api.setRange(o.lo, o.hi);
  api.goTo(o.at);
  api.seek(o.t);
  const before = {n: api.stepN(), t: api.state().t};
  api.restart();
  return {before, after: {n: api.stepN(), t: api.state().t}, first: api.range().first, pair: api.state().pair};
}
