// Drive the page's own API in one turn, so no frame can fall between the calls.
// o.calls is a list of [method, ...arguments]; the last call's answer comes back.
/** @param {{calls: [keyof import("../../src/api/workbench-api.js").AtlasTransitions, ...unknown[]][]}} o */
(o) => {
  const api = window.atlasTransitions;
  /** @type {unknown} */
  let answer;
  for (const call of o.calls) {
    const method = api[call[0]];
    if (typeof method !== "function") {
      throw new Error(`unknown workbench API method: ${call[0]}`);
    }
    answer = Reflect.apply(method, api, call.slice(1));
  }
  return answer;
};
