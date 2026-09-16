// The free run each graph draws, in the order asked, gathered per graph so one graph
// reached twice can be compared with itself. o.n is the size, o.kinds the walk.
/** @param {{n: number, kinds: import("../../src/api/workbench-api.js").AtlasRelationshipKind[]}} o */
(o) => {
  const api = window.atlasTransitions;
  api.setStepN(o.n);
  const i = api.state().pair;
  /** @type {Partial<Record<import("../../src/api/workbench-api.js").AtlasRelationshipKind, string[]>>} */
  const out = {};
  for (const k of o.kinds) {
    api.setRelationship(k);
    out[k] ??= [];
    out[k]?.push(JSON.stringify(api.physics(i, "bodies", "free").miss));
  }
  api.setRelationship("general");
  api.setLawPreset("default");
  return out;
};
