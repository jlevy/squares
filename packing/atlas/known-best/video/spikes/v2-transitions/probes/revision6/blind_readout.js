// What the bar reads at the end of a blind run, beside what the trajectory missed by.
// Takes {index}.
(o) => {
  const A = window.atlasTransitions;
  A.select(o.index);
  A.setStyle("bodies");
  A.setBlind(true);
  A.seek(A.duration());
  return { read: String(A.gapBar().side), miss: A.physics(o.index, "bodies", "blind").miss };
};
