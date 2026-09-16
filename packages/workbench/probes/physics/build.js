// Build one pair's trajectory and report what it cost. o.index is the pair, o.style the solver.
/** @param {{index: number, style: Parameters<import("../../src/api/workbench-api.js").AtlasTransitions["physics"]>[1]}} o */ (
  o,
) => window.atlasTransitions.physics(o.index, o.style);
