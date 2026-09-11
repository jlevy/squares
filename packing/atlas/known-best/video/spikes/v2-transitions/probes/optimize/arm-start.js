// Arm an open-ended run from one initial condition. o.kind is the start; the previous
// packing is the one start that needs a run begun and paused to have an arrangement.
(o) => {
  const api = window.atlasTransitions;
  api.setInitial(o.kind);
  if (o.kind === 'previous') { api.optimize(true); api.pause(); }
}
