// The motion style: 'tween', 'physics' or 'bodies'. Takes {style}.
/** @param {{style: Parameters<import("../../src/api/workbench-api.js").AtlasTransitions["physics"]>[1]}} o */ (
  o,
) => {
  window.atlasTransitions.setStyle(o.style);
};
