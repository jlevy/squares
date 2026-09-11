// The durations continuous play gives each kind of pair, under the short beat and the full one.
() => {
  const A = window.atlasTransitions;
  A.goTo(A.pairs()[0].n); A.playAll(); A.pause();
  const beats = {};
  for (const q of A.pairs()) { A.select(q.index); (beats[q.kind] = beats[q.kind] || new Set()).add(A.duration()); }
  const out = {};
  for (const k in beats) out[k] = Array.from(beats[k]);
  A.setContinuous({fullBeat: true});
  const full = {};
  for (const q of A.pairs()) { A.select(q.index); (full[q.kind] = full[q.kind] || new Set()).add(A.duration()); }
  const outFull = {};
  for (const k in full) outFull[k] = Array.from(full[k]);
  A.setContinuous({fullBeat: false}); A.stopAll();
  return {out, outFull};
}
