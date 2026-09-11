// A blind run of every pair under style C, with what each one misses by.
() => {
  const A = window.atlasTransitions;
  A.setStyle("bodies");
  A.setSnap(true);
  const out = [];
  for (const q of A.pairs()) {
    const t = A.physics(q.index, "bodies", "blind");
    out.push({ n: q.n, kind: q.kind, miss: t.miss, squeezeDone: t.squeezeDone, side0: t.side0 });
  }
  return out;
};
