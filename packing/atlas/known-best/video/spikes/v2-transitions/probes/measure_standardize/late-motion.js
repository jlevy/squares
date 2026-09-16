// How much an open-ended run is still moving late on. After 3,600 fixed steps it samples every
// visible square's transform, then 12 steps later (a tenth of a simulated second) and 108 after
// that (out to a whole one), and reports the greatest and mean square speed over the tenth and
// the greatest turn over the whole second. Takes {n, kind, level}.
/** @param {{n: number, kind: import("../../../../../../../../packages/workbench/src/api/workbench-api.js").AtlasInitial, level: number}} o */
(o) => {
  const A = window.atlasTransitions;
  A.setStepN(o.n);
  A.setAnneal(o.level);
  A.setInitial(o.kind);
  A.optimizeStep(3600);
  const before = A.optimizeState();
  const poseOf = () =>
    Array.from(/** @type {NodeListOf<SVGGElement>} */ (document.querySelectorAll("#squares g")))
      .filter((g) => g.style.display !== "none")
      .map((g) => g.getAttribute("transform"));
  const a = poseOf();
  A.optimizeStep(12); // a tenth of a simulated second
  const b = poseOf();
  A.optimizeStep(108); // out to a whole one
  const c = poseOf();
  // The transform is read as it stands, as the tool always has: a square without one is a
  // TypeError here, not a skipped square. The casts say so to the type checker.
  /** @param {string} s */
  const num = (s) => (s.match(/-?\d+\.?\d*(e-?\d+)?/g) || []).map(Number);
  let max = 0,
    sum = 0,
    count = 0,
    turn = 0;
  for (let i = 0; i < a.length; i++) {
    const p = num(/** @type {string} */ (a[i])),
      q = num(/** @type {string} */ (b[i])),
      r = num(/** @type {string} */ (c[i]));
    if (p.length < 2 || q.length < 2) {
      continue;
    }
    // The length checks above are what make these components present.
    const d =
      Math.hypot(
        /** @type {number} */ (q[0]) - /** @type {number} */ (p[0]),
        /** @type {number} */ (q[1]) - /** @type {number} */ (p[1]),
      ) * 10;
    if (d > max) {
      max = d;
    }
    sum += d;
    count++;
    if (p.length >= 3 && r.length >= 3) {
      const g = Math.abs(/** @type {number} */ (r[2]) - /** @type {number} */ (p[2])) % 90;
      const f = Math.min(g, 90 - g);
      if (f > turn) {
        turn = f;
      }
    }
  }
  return { steps: before.steps, max, mean: count ? sum / count : 0, turn };
};
