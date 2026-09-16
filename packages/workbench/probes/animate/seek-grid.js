// Seek every instant of a regular grid over each listed step, under each style and annealing
// level, and report every call the page threw at. The grid includes both ends of the step,
// where a smoothed ramp that overshoots one by a rounding error used to reach the painter.
// o.ns are the steps, o.styles the styles, o.levels the annealing levels, o.k the grid size.
/** @param {{ns: number[], styles: import("../../src/api/workbench-api.js").AtlasStyle[], levels: number[], k: number}} o */
(o) => {
  const api = window.atlasTransitions;
  /** @type {string[]} */
  const failures = [];
  let seeks = 0;
  const attempt = (/** @type {string} */ label, /** @type {() => unknown} */ call) => {
    try {
      call();
    } catch (error) {
      failures.push(`${label}: ${error}`);
    }
  };
  api.pause();
  api.seek(0);
  const level = api.anneal().level;
  const style = api.state().style;
  for (const s of o.styles) {
    attempt(`setStyle ${s}`, () => api.setStyle(s));
    for (const a of o.levels) {
      attempt(`setAnneal ${a}`, () => api.setAnneal(a));
      for (const n of o.ns) {
        attempt(`setStepN ${n}`, () => api.setStepN(n));
        for (let j = 0; j <= o.k; j++) {
          const t = (api.duration() * j) / o.k;
          seeks += 1;
          attempt(`${s} anneal ${a} step into ${n} at ${t}`, () => api.seek(t));
        }
        attempt("seek 0", () => api.seek(0));
      }
    }
  }
  attempt("restore", () => {
    api.setAnneal(level);
    api.setStyle(style);
    api.seek(0);
  });
  return { seeks, failures };
};
