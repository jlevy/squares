// The n of the first pair and of the last, which is what goTo has to clamp to.
() => {
  const pairs = window.atlasTransitions.pairs();
  const first = pairs[0];
  const last = pairs.at(-1);
  if (first === undefined || last === undefined) {
    throw new Error("probe requires at least one pair");
  }
  return [first.n, last.n];
};
