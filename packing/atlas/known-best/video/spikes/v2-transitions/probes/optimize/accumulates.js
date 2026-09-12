// An open-ended run from the grid start, read before, during and after two batches of
// steps. o.n is the size, o.steps the size of each batch.
(o) => {
  const api = window.atlasTransitions;
  api.setStepN(o.n);
  api.setInitial("grid");
  const a = api.optimizeState();
  api.optimizeStep(o.steps);
  const b = api.optimizeState();
  api.optimizeStep(o.steps);
  const c = api.optimizeState();
  return { a, b, c };
};
