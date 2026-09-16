// Start a real playing run at double speed, from one kind of start. Takes {n, kind}.
/** @param {{n: number, kind: import("../../../../../../../../packages/workbench/src/api/workbench-api.js").AtlasInitial}} o */
(o) => {
  const A = window.atlasTransitions;
  A.setStepN(o.n);
  A.setSpeed(2);
  A.setInitial(o.kind);
  A.optimize(true);
};
