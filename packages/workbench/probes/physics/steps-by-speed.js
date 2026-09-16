// What each pair plays and what it simulates, with the simple-transition speed-up on and then
// off: its duration on the clock and the physics steps `physics()` runs, which is what the
// annealing benchmark calls. Takes {indices, style, mode}; puts the setting back as it was.
/** @param {{indices: number[], style: import("../../src/api/workbench-api.js").AtlasStyle, mode: import("../../src/api/workbench-api.js").AtlasSimMode}} o */
(o) => {
  const api = window.atlasTransitions;
  const found = api.continuous().fastSimple;
  const rows = [];
  for (const fastSimple of [true, false]) {
    api.setContinuous({ fastSimple });
    for (const index of o.indices) {
      rows.push({
        index,
        fastSimple,
        duration: api.duration(index),
        steps: api.physics(index, o.style, o.mode).steps,
      });
    }
  }
  api.setContinuous({ fastSimple: found });
  return rows;
};
