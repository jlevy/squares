// What the bar reads at the dwell, at rest under the snap, and at rest on a free run.
// Takes {index, style}; leaves the snap back on.
(o) => {
  const A = window.atlasTransitions;
  A.stopAll();
  A.select(o.index);
  A.setStyle(o.style);
  A.setSnap(true);
  A.setBlind(false);
  A.setAnneal(3);
  const read = () => {
    const g = A.gapBar();
    return { side: g.side, record: g.record, met: g.met };
  };
  const out = {};
  A.seek(0);
  out.dwell = read();
  A.seek(A.duration());
  out.rest = read();
  A.setSnap(false);
  A.seek(A.duration());
  out.free = read();
  A.setSnap(true);
  return out;
};
