// Drive the Pack panel's own API in one turn, so no frame can fall between the calls.
// o.calls is a list of [method, ...arguments]; the last call's answer comes back.
/** @param {{calls: [keyof import("../../src/api/pack-api.js").PackWorkbenchApi, ...unknown[]][]}} o */
(o) => {
  /** @typedef {import("../../src/api/pack-api.js").PackWorkbenchApi} PackWorkbenchApi */
  const api = /** @type {Window & {packWorkbench?: PackWorkbenchApi}} */ (window).packWorkbench;
  if (api === undefined) {
    throw new Error("probe requires window.packWorkbench");
  }
  /** @type {unknown} */
  let answer;
  for (const call of o.calls) {
    const method = api[call[0]];
    if (typeof method !== "function") {
      throw new Error(`unknown Pack API method: ${call[0]}`);
    }
    answer = Reflect.apply(method, api, call.slice(1));
  }
  return answer;
};
