// An open-ended run at one n from one of the three starts. Takes {n, initial}.
(o) => {
  const A = window.atlasTransitions;
  A.setStepN(o.n);
  A.setInitial(o.initial);
  if (o.initial === "previous") {
    A.optimize(true);
    A.pause();
  }
  A.optimizeStep(1200);
};
