// Whether a square can be joined to itself. o.index is the square.
/** @param {{index: number}} o */ (o) => {
  const api = window.atlasTransitions;
  return api.linkStart(o.index) >= 0 && api.linkEnd(o.index).added;
};
