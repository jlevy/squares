// Which steps play sped up, observed rather than asked for: every pair's duration with the
// simple-transition speed-up off and then on, and whether it halves. Puts the setting back.
() => {
  const api = window.atlasTransitions;
  const found = api.continuous().fastSimple;
  const pairs = api.pairs();
  api.setContinuous({ fastSimple: false });
  const full = pairs.map((_, index) => api.duration(index));
  api.setContinuous({ fastSimple: true });
  const rows = pairs.map((pair, index) => {
    const long = full[index] ?? Number.NaN;
    return {
      n: pair.n,
      kind: pair.kind,
      sped: long > 0 && Math.abs(2 * api.duration(index) - long) < 1e-9,
    };
  });
  api.setContinuous({ fastSimple: found });
  return rows;
};
