// How many steps the same run takes at the default level. Takes {index, mode}.
(o) => {
  const A = window.atlasTransitions;
  A.setAnneal(3);
  return A.physics(o.index, "physics", o.mode).steps;
};
