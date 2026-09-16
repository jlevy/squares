// The law's force at each signed gap. o.gaps is the list of gaps; positive is apart.
/** @param {{gaps: number[]}} o */ (o) =>
  o.gaps.map(/** @param {number} d */ (d) => window.atlasTransitions.lawForce(d));
