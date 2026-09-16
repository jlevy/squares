// One open-ended settle, advanced by an exact number of fixed steps with no clock in it, and what
// it reached. The returned object's key order is the order of the tool's table and JSON.
// Takes {n, law, start, relationship, steps}.
/** @param {{n: number, law: string, start: import("../../../../../../../../packages/workbench/src/api/workbench-api.js").AtlasInitial, relationship: import("../../../../../../../../packages/workbench/src/api/workbench-api.js").AtlasRelationshipKind, steps: number}} o */
(o) => {
  const api = window.atlasTransitions;
  api.reset();
  api.setStepN(o.n);
  api.setBlind(true);
  api.setLawPreset(o.law);
  api.setRelationship(o.relationship);
  api.setInitial(o.start);
  api.optimize(true);
  api.pause();
  api.optimizeStep(o.steps);
  const run = api.optimizeState();
  const rel = api.relationship();
  return {
    n: o.n,
    law: o.law,
    start: o.start,
    graph: o.relationship,
    side: run.side,
    required: run.required,
    best: run.best,
    bestPen: run.bestPenetration,
    pen: run.penetration,
    record: run.record,
    excess: run.excess,
    steps: run.steps,
    near: run.near === undefined ? null : run.near,
    edges: rel.edges,
    met: rel.met,
    fraction: rel.fraction,
  };
};
