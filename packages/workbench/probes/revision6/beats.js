// The durations continuous play gives each kind of pair, under the short beat and the full one.
() => {
  const A = window.atlasTransitions;
  const first = A.pairs()[0];
  if (first === undefined) {
    throw new Error("probe requires at least one pair");
  }
  A.goTo(first.n);
  A.playAll();
  A.pause();
  /** @type {Partial<Record<import("../../src/api/workbench-api.js").AtlasPairKind, Set<number>>>} */
  const beats = {};
  for (const q of A.pairs()) {
    A.select(q.index);
    beats[q.kind] ??= new Set();
    beats[q.kind]?.add(A.duration());
  }
  /** @type {Record<string, number[]>} */
  const out = {};
  for (const k in beats) {
    out[k] = Array.from(
      beats[/** @type {import("../../src/api/workbench-api.js").AtlasPairKind} */ (k)] ?? [],
    );
  }
  A.setContinuous({ fullBeat: true });
  /** @type {Partial<Record<import("../../src/api/workbench-api.js").AtlasPairKind, Set<number>>>} */
  const full = {};
  for (const q of A.pairs()) {
    A.select(q.index);
    full[q.kind] ??= new Set();
    full[q.kind]?.add(A.duration());
  }
  /** @type {Record<string, number[]>} */
  const outFull = {};
  for (const k in full) {
    outFull[k] = Array.from(
      full[/** @type {import("../../src/api/workbench-api.js").AtlasPairKind} */ (k)] ?? [],
    );
  }
  A.setContinuous({ fullBeat: false });
  A.stopAll();
  return { out, outFull };
};
