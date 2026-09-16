// The record's own contact graph at one n, flat as a, b, a, b, for drawing it by hand as the
// control. Takes {n}.
/** @param {{n: number}} o */
(o) => {
  const A = window.atlasTransitions;
  A.setStepN(o.n);
  A.setTargetSource("record");
  return A.targetGraph();
};
