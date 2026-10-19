// Build one pair's trajectory from scratch, past the cache, and report what it cost: a repeat
// times the build again rather than reading the first build's cost back. o.index is the pair,
// o.style the solver.
/** @param {{index: number, style: Parameters<import("../../src/api/workbench-api.js").AtlasTransitions["measurePhysics"]>[1]}} o */ (
  o,
) => window.atlasTransitions.measurePhysics(o.index, o.style);
