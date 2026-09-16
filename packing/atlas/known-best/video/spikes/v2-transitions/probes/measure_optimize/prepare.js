// Set up the same start paused, to be driven by exact step counts. Takes {n, kind}.
/** @param {{n: number, kind: import("../../../../../../../../packages/workbench/src/api/workbench-api.js").AtlasInitial}} o */
(o) => {
  const A = window.atlasTransitions;
  A.setStepN(o.n);
  A.setInitial(o.kind);
  A.optimize(true);
  A.pause();
};
