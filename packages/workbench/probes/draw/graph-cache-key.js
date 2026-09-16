// The cache key and the free run under each of a walk of target graphs: the record's own,
// then each drawn graph in turn. o.walk is a list of [name, edges or null for the record].
/** @param {{walk: [string, import("../../src/api/workbench-api.js").AtlasEdgeInput | null][]}} o */
(o) => {
  const api = window.atlasTransitions;
  const i = api.state().pair;
  /** @type {Record<string, {key: string, miss: string}>} */
  const out = {};
  const one = () => ({
    key: api.relationship().key,
    miss: JSON.stringify(api.physics(i, "bodies", "free").miss),
  });
  for (const step of o.walk) {
    if (step[1] === null) {
      api.setTargetSource("record");
    } else {
      api.setEdges(step[1]);
    }
    out[step[0]] = one();
  }
  return out;
};
