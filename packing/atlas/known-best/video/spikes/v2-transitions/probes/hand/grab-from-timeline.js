// Grab a square from the timeline: what was picked, and whether the grab handed the
// picture to an open-ended run. o.x and o.y are where to reach for it.
(o) => {
  const api = window.atlasTransitions;
  const before = api.state().optimizing;
  const i = api.pickAt(o.x, o.y);
  const g = api.grab(i, o.x, o.y);
  return { before, i, g, optimizing: api.state().optimizing, edited: api.hand().edited };
};
