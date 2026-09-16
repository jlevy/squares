// Drive the page's own API as api/apply does, and report a refusal rather than raise it: what the
// calls throw, as a string, or null when every call is accepted.
// o.calls is a list of [method, ...arguments].
/** @param {{calls: [keyof import("../../src/api/workbench-api.js").AtlasTransitions, ...unknown[]][]}} o */
(o) => {
  try {
    const api = window.atlasTransitions;
    for (const call of o.calls) {
      const method = api[call[0]];
      if (typeof method !== "function") {
        throw new Error(`unknown workbench API method: ${call[0]}`);
      }
      Reflect.apply(method, api, call.slice(1));
    }
    return null;
  } catch (error) {
    return String(error);
  }
};
