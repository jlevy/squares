// What a stray key or click could have disturbed: one square's pose, the run's progress,
// the start the run came from, playback, and where keyboard focus sits.
// o.index is the square to report.
/** @param {{index: number}} o */
(o) => {
  /** @typedef {import("../../src/api/pack-api.js").PackWorkbenchApi} PackWorkbenchApi */
  const api = /** @type {Window & {packWorkbench?: PackWorkbenchApi}} */ (window).packWorkbench;
  if (api === undefined) {
    throw new Error("probe requires window.packWorkbench");
  }
  const state = api.state();
  const pose = state.snapshot.poses[o.index];
  const start = document.getElementById("pack-start");
  const active = document.activeElement;
  return {
    x: pose.x,
    y: pose.y,
    angle: pose.angle,
    latest: state.latest !== null,
    steps: state.latest?.work.baseSteps ?? 0,
    startKind: state.configuration.startKind,
    startControl: start instanceof HTMLSelectElement ? start.value : null,
    playing: api.playing(),
    focus: active?.getAttribute("data-pack-index") ?? active?.id ?? null,
  };
};
