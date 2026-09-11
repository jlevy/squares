// The cache key and the free run under each of a walk of target graphs: the record's own,
// then each drawn graph in turn. o.walk is a list of [name, edges or null for the record].
(o) => {
  const api = window.atlasTransitions;
  const i = api.state().pair;
  const out = {};
  const one = () => ({key: api.relationship().key,
                      miss: JSON.stringify(api.physics(i, 'bodies', 'free').miss)});
  for (const step of o.walk) {
    if (step[1] === null) api.setTargetSource('record');
    else api.setEdges(step[1]);
    out[step[0]] = one();
  }
  return out;
}
