// A run at level 9 under style B, in one mode. Takes {index, mode}, mode being 'snap' or
// 'blind'; leaves the dial back at its default.
(o) => {
  const A = window.atlasTransitions;
  A.setAnneal(9);
  const r = A.physics(o.index, 'physics', o.mode);
  A.setAnneal(3);
  return {miss: r.miss, steps: r.steps};
}
