// The record's own graph, and the same graph drawn by hand: the physics is told nothing
// about where the edges came from, so the two must drive the same run. o.graph is the
// record's graph, as a flat list of pairs.
(o) => {
  const api = window.atlasTransitions;
  const i = api.state().pair;
  api.setTargetSource('record');
  const fromRecord = JSON.stringify(api.physics(i, 'bodies', 'free').miss);
  api.setEdges(o.graph);
  const fromHand = JSON.stringify(api.physics(i, 'bodies', 'free').miss);
  return {fromRecord, fromHand};
}
