// Where each pair-moving call leaves the stage against the range. o.calls is a list of
// [method, ...arguments]; after each, the range, the n the stage is on, and the run state.
/** @param {{calls: [keyof import("../../src/api/workbench-api.js").AtlasTransitions, ...unknown[]][]}} o */
(o) => {
  const api = window.atlasTransitions;
  return o.calls.map((call) => {
    const method = api[call[0]];
    if (typeof method !== "function") {
      throw new Error(`unknown workbench API method: ${call[0]}`);
    }
    Reflect.apply(method, api, call.slice(1));
    const range = api.range();
    const s = api.state();
    return {
      call: call[0],
      from: range.from,
      to: range.to,
      inside: range.inside,
      n: s.n + 1,
      aspect: s.aspect,
      playing: s.playing,
      optimizing: s.optimizing,
      continuous: api.continuous().on,
    };
  });
};
