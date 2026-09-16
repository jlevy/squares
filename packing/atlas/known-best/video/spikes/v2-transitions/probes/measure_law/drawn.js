// What fraction of a hand-drawn contact graph an Optimize run realises after an exact number of
// steps. The returned object's key order is the order of the tool's table and JSON.
// Takes {n, kind, graph, steps}: `kind` names the graph and `graph` is its edges, as pairs.
/** @param {{n: number, kind: string, graph: number[][], steps: number}} o */
(o) => {
  const api = window.atlasTransitions;
  api.reset();
  api.setStepN(o.n);
  api.setBlind(true);
  api.setLawPreset("sticky");
  api.setEdges(o.graph);
  api.setRelationship("contact");
  api.setInitial("grid");
  api.optimize(true);
  api.pause();
  const before = api.relationship();
  api.optimizeStep(o.steps);
  const rel = api.relationship();
  const run = api.optimizeState();
  return {
    n: o.n,
    graph: o.kind,
    source: rel.target,
    edges: rel.edges,
    metAtStart: before.met,
    met: rel.met,
    fraction: rel.fraction,
    side: rel.side,
    record: rel.record,
    excess: run.excess,
    pen: run.penetration,
    steps: run.steps,
  };
};
