// One combination of pair, style, run mode, annealing level and instant.
// Takes {index, style, mode, level, at}; mode is 'snap', 'free' or 'blind'.
(o) => {
  const A = window.atlasTransitions;
  A.select(o.index);
  A.setStyle(o.style);
  A.setSnap(o.mode !== "free");
  A.setBlind(o.mode === "blind");
  A.setAnneal(o.level);
  A.seek(o.at);
};
