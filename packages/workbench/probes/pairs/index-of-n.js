// Which pair steps into this size, by index, or -1 if the page carries none. o.n is the size.
/** @param {{n: number}} o */ (o) =>
  window.atlasTransitions.pairs().findIndex((p) => p.n + 1 === o.n);
