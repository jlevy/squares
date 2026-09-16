// The motion mode: which of the new square and the blocks moves first. Takes {phase}.
/** @param {{phase: Parameters<import("../../src/api/workbench-api.js").AtlasTransitions["setPhase"]>[0]}} o */ (
  o,
) => {
  window.atlasTransitions.setPhase(o.phase);
};
