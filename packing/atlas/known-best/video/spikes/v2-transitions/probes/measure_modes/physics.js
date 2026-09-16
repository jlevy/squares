// Run (or fetch from the cache) one pair's trajectory under a style and a simulation mode, and
// what it missed the record by. Takes {index, style, mode}.
//
// `mode` is the tool's first command-line word, handed on unchecked as it always has been, so it
// arrives as a string and is typed as the mode the page declares at the one call that takes it.
/** @param {{index: number, style: import("../../../../../../../../packages/workbench/src/api/workbench-api.js").AtlasStyle, mode: string}} o */
(o) => {
  const r = window.atlasTransitions.physics(
    o.index,
    o.style,
    /** @type {import("../../../../../../../../packages/workbench/src/api/workbench-api.js").AtlasSimMode} */ (
      o.mode
    ),
  );
  return {
    miss: r.miss,
    ms: r.ms,
    bodies: r.bodies,
    pen: r.maxPenetration,
    penLate: r.maxPenetrationLate,
  };
};
