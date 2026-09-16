// One pair's trajectory at one annealing level, and what the level means: the shake's amplitude,
// its decay power and its span. Takes {index, style, mode, level}.
//
// `mode` is the tool's first command-line word, handed on unchecked as it always has been, so it
// arrives as a string and is typed as the mode the page declares at the one call that takes it.
/** @param {{index: number, style: import("../../../../../../../../packages/workbench/src/api/workbench-api.js").AtlasStyle, mode: string, level: number}} o */
(o) => {
  const A = window.atlasTransitions;
  A.setStyle(o.style);
  A.setAnneal(o.level);
  const r = A.physics(
    o.index,
    o.style,
    /** @type {import("../../../../../../../../packages/workbench/src/api/workbench-api.js").AtlasSimMode} */ (
      o.mode
    ),
  );
  const a = A.anneal();
  return {
    miss: r.miss,
    ms: r.ms,
    pen: Math.max(r.maxPenetration, r.maxPenetrationLate),
    steps: r.steps,
    amp: a.amplitude,
    dec: a.decayPower,
    span: a.span,
  };
};
