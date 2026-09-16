// Every parameter pushed past its bounds, set inside them, read back, and then given junk
// and nothing at all. o.low, o.high and o.middle are the three laws to try.
/** @param {{low: Parameters<import("../../src/api/workbench-api.js").AtlasTransitions["setLaw"]>[0], high: Parameters<import("../../src/api/workbench-api.js").AtlasTransitions["setLaw"]>[0], middle: Parameters<import("../../src/api/workbench-api.js").AtlasTransitions["setLaw"]>[0]}} o */ (
  o,
) => {
  const api = window.atlasTransitions;
  const pick = /** @param {import("../../src/api/workbench-api.js").AtlasLawState} l */ (l) => ({
    rigidity: l.rigidity,
    repulsion: l.repulsion,
    attraction: l.attraction,
    range: l.range,
  });
  const lo = pick(api.setLaw(o.low));
  const hi = pick(api.setLaw(o.high));
  const mid = pick(api.setLaw(o.middle));
  const back = pick(api.law());
  const junk = pick(api.setLaw({ rigidity: "nope", repulsion: NaN }));
  const none = pick(api.setLaw(null));
  const stray = api.setLawPreset("nonesuch").key;
  api.setLawPreset("default");
  return { lo, hi, mid, back, junk, none, stray };
};
