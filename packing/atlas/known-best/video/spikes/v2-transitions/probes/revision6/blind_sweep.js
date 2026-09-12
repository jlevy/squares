// A blind run of every pair under style C, with what each one misses by.
() => {
  const A = window.atlasTransitions;
  A.setStyle("bodies");
  A.setSnap(true);
  const out = [];
  for (const q of A.pairs()) {
    // `squeezeDone` and `side0` below are the blind contraction's own numbers. The simulator
    // carries them, but `physics()` does not copy them into the report it returns, so both read
    // `undefined` here. Left exactly as they are -- dropping them would change what this probe
    // hands back -- and declared optional so the read is honest about what it finds.
    const t = /** @type {AtlasPhysics & Partial<{ squeezeDone: boolean; side0: number }>} */ (
      A.physics(q.index, "bodies", "blind")
    );
    out.push({ n: q.n, kind: q.kind, miss: t.miss, squeezeDone: t.squeezeDone, side0: t.side0 });
  }
  return out;
};
