// Put the stage on one size under one relationship with the sticky law, ready for an
// open-ended run from the grid start. o.n is the size, o.kind the graph.
(o) => {
  const api = window.atlasTransitions;
  api.setStyle("tween");
  api.setStepN(o.n);
  api.setLawPreset("sticky");
  api.setRelationship(o.kind);
  api.setInitial("grid");
};
