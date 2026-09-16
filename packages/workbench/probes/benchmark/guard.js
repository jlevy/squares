// The benchmark bundle's guard: whether the page exposes a nonempty, seeded workbench API.
() => {
  /** @type {typeof import("../bench-annealing.js")} */
  const bench = Reflect.get(window, "SquaresWorkbenchBench");
  return bench.guard();
};
