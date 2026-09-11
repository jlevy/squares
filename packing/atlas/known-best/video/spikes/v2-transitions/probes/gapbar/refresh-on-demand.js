// The bar before a seek, after it, and when asked to redraw. A seek marks the bar dirty on
// purpose, so the frame clock is driven rather than the seek relied on.
// o.before and o.after are the two instants to seek to.
(o) => {
  const api = window.atlasTransitions;
  api.pause();
  api.seek(o.before);
  const before = api.gapBar().x;
  api.seek(o.after);
  return { before, after: api.gapBar().x, demand: api.refreshGap().x };
};
