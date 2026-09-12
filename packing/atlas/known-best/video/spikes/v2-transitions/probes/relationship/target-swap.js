// A target graph given from outside, and back to the record's. o.graph is what to give it.
(o) => {
  const api = window.atlasTransitions;
  const before = api.targetGraph();
  const from = api.relationship().target;
  api.setTargetGraph(o.graph);
  const given = {
    graph: api.targetGraph(),
    target: api.relationship().target,
    edges: api.relationship().edges,
  };
  api.setTargetGraph(null);
  return { before, from, given, after: api.targetGraph(), target: api.relationship().target };
};
