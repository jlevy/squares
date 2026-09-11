// Setting the graph must change the graph and nothing else. o.kind is the graph to set.
(o) => {
  const api = window.atlasTransitions;
  const before = api.law().key;
  api.setRelationship(o.kind);
  return {before, after: api.law().key, kind: api.relationship().kind};
}
