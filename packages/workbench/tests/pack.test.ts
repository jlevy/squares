import assert from "node:assert/strict";
import { test } from "node:test";
import type { AtlasLaw } from "../src/api/workbench-api.ts";
import {
  advancePackRun,
  createGridPackStart,
  createPackRun,
  createRandomPackStart,
  type PackConfiguration,
  runPack,
} from "../src/simulation/pack.ts";

const law: AtlasLaw = { rigidity: 0.15, repulsion: 2_500, attraction: 0, range: 0 };

function configuration(overrides: Partial<PackConfiguration> = {}): PackConfiguration {
  return {
    n: 5,
    seed: 17,
    effectiveSeed: 17,
    startKind: "grid",
    start: createGridPackStart(5),
    targets: null,
    reference: null,
    pairLaw: law,
    wallLaw: law,
    relatedMask: null,
    physics: {
      stepsPerSecond: 120,
      omega: 10,
      zeta: 0.85,
      contactDamping: 20,
      contactTorque: 0.15,
      jiggle: 20,
      jiggleTorque: 12,
      jiggleHz: [2.5, 4],
      maxSpeed: 40,
      maxSpin: 20,
      cell: 1.5,
    },
    anneal: { amplitude: 1, decayPower: 1.5, tau: 2, floor: 0.15 },
    growth: { on: false, rate: 0.05, rule: "constant" },
    container: {
      squeezeRate: 0.03,
      relaxRate: 0.03,
      squeezeTolerance: 0.004,
      jamTolerance: 0.06,
      minimumSide: 0.5,
    },
    stationarity: {
      linearSpeed: 1e-6,
      angularSpeed: 1e-6,
      forcingScale: 1e-6,
      window: 8,
      stop: false,
    },
    ...overrides,
  };
}

test("Pack accepts arbitrary n without an atlas pair and reports the exact returned geometry", () => {
  const start = createGridPackStart(5);
  const receipt = runPack(
    configuration({
      start,
      targets: start.poses,
      anneal: { amplitude: 0, decayPower: 1.5, tau: 2, floor: 0 },
    }),
    12,
  );
  assert.equal(receipt.snapshot.poses.length, 5);
  assert.equal(receipt.configuration.n, 5);
  assert.equal(receipt.configuration.effectiveSeed, 17);
  assert.equal(receipt.configuration.reference, null);
  assert.equal(receipt.work.baseSteps, 12);
  assert.equal(receipt.termination.reason, "work-limit");
  assert.equal(receipt.termination.converged, false);
  assert.equal(receipt.feasibility.valid, true);
  assert.equal(receipt.feasibility.geometry.maxPairOverlap, 0);
});

test("fixed work can be continued without changing the deterministic result", () => {
  const config = configuration({
    n: 7,
    start: createRandomPackStart(7, 4, 99),
    effectiveSeed: 99,
    seed: 99,
    startKind: "random",
  });
  const once = runPack(config, 20);
  const continued = createPackRun(config);
  advancePackRun(continued, 7);
  const twice = advancePackRun(continued, 13);
  assert.deepEqual(twice.snapshot, once.snapshot);
  assert.deepEqual(twice.best, once.best);
  assert.deepEqual(twice.work, once.work);
  assert.deepEqual(twice.residual, once.residual);
});

test("best packing is independent of how the same fixed work is batched", () => {
  const config = configuration({
    n: 2,
    seed: 0,
    effectiveSeed: 0,
    startKind: "random",
    start: createRandomPackStart(2, 4, 0),
  });
  const uninterrupted = runPack(config, 300);
  const continued = createPackRun(config);
  let batched = advancePackRun(continued, 10);
  for (let batch = 1; batch < 30; batch += 1) {
    batched = advancePackRun(continued, 10);
  }
  assert.deepEqual(batched.snapshot, uninterrupted.snapshot);
  assert.deepEqual(batched.best, uninterrupted.best);
  assert((batched.best?.requiredSide ?? Infinity) < 2.5);
});

test("cancellation and stationarity are explicit and separate from feasibility", () => {
  const run = createPackRun(configuration());
  let checks = 0;
  const cancelled = advancePackRun(run, 50, {
    shouldCancel: () => ++checks > 3,
  });
  assert.equal(cancelled.termination.reason, "cancelled");
  assert.equal(cancelled.work.baseSteps, 3);
  assert.equal(cancelled.termination.converged, false);
  assert.equal(typeof cancelled.feasibility.valid, "boolean");

  const stationary = runPack(
    configuration({
      n: 1,
      start: createGridPackStart(1),
      pairLaw: { ...law, repulsion: 0 },
      wallLaw: { ...law, repulsion: 0 },
      anneal: { amplitude: 0, decayPower: 1.5, tau: 2, floor: 0 },
      stationarity: {
        linearSpeed: 0,
        angularSpeed: 0,
        forcingScale: 0,
        window: 2,
        stop: true,
      },
      container: { ...configuration().container, squeezeRate: 0, relaxRate: 0 },
    }),
    20,
  );
  assert.equal(stationary.termination.reason, "stationary");
  assert.equal(stationary.termination.stationary, true);
  assert.equal(stationary.termination.converged, true);
  assert.equal(stationary.work.baseSteps, 2);
});

test("changing container or square size cannot be declared stationary", () => {
  const base = configuration({
    n: 1,
    start: {
      squareSide: 1,
      container: { originX: 0, originY: 0, side: 10 },
      poses: [{ x: 5, y: 5, angle: 0 }],
    },
    pairLaw: { ...law, repulsion: 0 },
    wallLaw: { ...law, repulsion: 0 },
    anneal: { amplitude: 0, decayPower: 1.5, tau: 2, floor: 0 },
    stationarity: {
      linearSpeed: 0,
      angularSpeed: 0,
      forcingScale: 0,
      window: 1,
      stop: true,
    },
  });
  const shrinking = runPack(base, 1);
  assert(shrinking.snapshot.container.side < 10);
  assert.equal(shrinking.termination.reason, "work-limit");
  assert.equal(shrinking.termination.stationarySteps, 0);

  const growing = runPack(
    {
      ...base,
      start: { ...base.start, squareSide: 0.5 },
      growth: { on: true, rate: 0.1, rule: "constant" },
    },
    1,
  );
  assert(growing.snapshot.squareSide > 0.5);
  assert.equal(growing.termination.reason, "work-limit");
  assert.equal(growing.termination.stationarySteps, 0);
});

test("sub-unit growth is disclosed and cannot produce a retained unit packing", () => {
  const start = createGridPackStart(2, 0.5);
  const receipt = runPack(
    configuration({
      n: 2,
      start,
      growth: { on: true, rate: 0.01, rule: "clean" },
    }),
    1,
  );
  assert(receipt.snapshot.squareSide > 0.5 && receipt.snapshot.squareSide < 1);
  assert.equal(receipt.best, null);
  assert.equal(receipt.feasibility.unitSquares, false);
});

test("bad counts, masks, budgets and nonfinite configuration fail before a run", () => {
  assert.throws(() => createPackRun(configuration({ n: 4 })), /declared count/);
  assert.throws(
    () => createPackRun(configuration({ relatedMask: new Uint8Array(3) })),
    /relationship mask/,
  );
  assert.throws(() => runPack(configuration(), 0), /work budget/);
  assert.throws(
    () => createPackRun(configuration({ reference: { pairIndex: 0, recordSide: Number.NaN } })),
    /record side/,
  );
});
