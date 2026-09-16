// One blind trial through the benchmark bundle; the options are the probe's one argument.
/** @param {import("../bench-annealing.js").TrialOptions} options */
(options) => {
  /** @type {typeof import("../bench-annealing.js")} */
  const bench = Reflect.get(window, "SquaresWorkbenchBench");
  return bench.runTrial(options);
};
