// Apply any calls given and then seek to the last instant of whatever is on the stage, in
// one turn, because the duration has to be read after the calls have taken effect.
// o.calls is a list of [method, ...arguments], and may be empty.
/** @param {{calls: [keyof import("../../src/api/workbench-api.js").AtlasTransitions, ...unknown[]][]}} o */
(o) => {
  const api = window.atlasTransitions;
  for (const call of o.calls || []) {
    const method = api[call[0]];
    if (typeof method !== "function") {
      throw new Error(`unknown workbench API method: ${call[0]}`);
    }
    Reflect.apply(method, api, call.slice(1));
  }
  return api.seek(api.duration());
};
