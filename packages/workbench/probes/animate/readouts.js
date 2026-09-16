// Every Animate readout that could call an arrangement a packing, after the calls in o.calls
// ([method, ...arguments]) and a gap-bar refresh: the bar's validity, hit, excess, side, reason,
// tolerance and precision with its hand's drawn opacity, the growth and the open-ended run's own
// packing flags and excess, and the growth readout's text.
/** @param {{calls: [keyof import("../../src/api/workbench-api.js").AtlasTransitions, ...unknown[]][]}} o */
(o) => {
  const api = window.atlasTransitions;
  for (const call of o.calls) {
    const method = api[call[0]];
    if (typeof method !== "function") {
      throw new Error(`unknown workbench API method: ${call[0]}`);
    }
    Reflect.apply(method, api, call.slice(1));
  }
  api.refreshGap();
  const bar = api.gapBar();
  const growth = api.growth();
  const run = api.optimizeState();
  const hand = /** @type {Element} */ (document.getElementById("gapbar-hand"));
  return {
    valid: bar.valid,
    met: bar.met,
    excess: bar.excess,
    side: bar.side,
    reason: bar.reason,
    tolerance: bar.tolerance,
    precision: bar.precision,
    hand: Number(getComputedStyle(hand).opacity),
    growthPacking: growth.packing,
    growthExcess: growth.excess,
    runPacking: run.packing ?? null,
    runExcess: run.excess ?? null,
    growInfo: document.getElementById("grow-info")?.textContent ?? "",
  };
};
