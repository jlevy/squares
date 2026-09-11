// What four levels of the dial do to the shake and to the run, keyed by level.
// Takes {index}; leaves the dial back at its default.
(o) => {
  const A = window.atlasTransitions;
  A.setStyle("bodies");
  A.setSnap(false);
  A.setBlind(false);
  const out = {};
  for (const L of [0, 3, 6, 10]) {
    A.setAnneal(L);
    const a = A.anneal(),
      r = A.physics(o.index, "bodies", "free");
    out[L] = {
      amp: a.amplitude,
      decay: a.decayPower,
      span: a.span,
      steps: r.steps,
      move: a.move,
      miss: r.miss,
      first: r.final[0],
    };
  }
  A.setAnneal(3);
  return out;
};
