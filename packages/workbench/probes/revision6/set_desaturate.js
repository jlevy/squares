// The drain that empties the fills while the pair moves. Takes {on}.
/** @param {{on: boolean}} o */ (o) => {
  window.atlasTransitions.setDesaturate(o.on);
};
