// Start small and grow under one rule for 7,200 fixed steps, and what the arrangement reached.
// The returned object's key order is the order of the tool's table and JSON. Takes {n, rule}.
/** @param {{n: number, rule: import("../../../../../../../../packages/workbench/src/api/workbench-api.js").AtlasGrowthRule}} o */
(o) => {
  const api = window.atlasTransitions;
  api.reset();
  api.setStepN(o.n);
  api.setBlind(true);
  api.setGrowth({ size: 0.3, rate: 0.05, rule: o.rule, on: true });
  api.setInitial("grid");
  api.optimize(true);
  api.pause();
  api.optimizeStep(7200);
  const g = api.growth();
  const run = api.optimizeState();
  return {
    n: o.n,
    rule: o.rule,
    size: g.size,
    growing: g.growing,
    stalled: g.stalled,
    tight: g.sideAtSize,
    unitSide: g.unitSide,
    record: g.record,
    pen: g.penetration,
    packing: g.packing,
    suspect: g.suspect,
    excess: g.excess,
    steps: run.steps,
  };
};
