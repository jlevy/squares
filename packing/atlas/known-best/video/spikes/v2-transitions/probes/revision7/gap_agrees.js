// The side the bar reads at the end of a free run, beside the side the trajectory says it
// reached. Takes {index}; leaves the snap back on.
(o) => {
  const A = window.atlasTransitions;
  A.select(o.index);
  A.setStyle("bodies");
  A.setSnap(false);
  A.seek(A.duration());
  const g = A.gapBar();
  const m = A.physics(o.index, "bodies", "free").miss;
  A.setSnap(true);
  return [g.side, m.side];
};
