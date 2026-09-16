import assert from "node:assert/strict";
import { test } from "node:test";
import type { AtlasLaw } from "../src/api/workbench-api.ts";
import {
  advanceSimulation,
  broadPhaseGrid,
  createSimulationState,
  MAX_BROAD_PHASE_DIMENSION,
  simulationSnapshot,
} from "../src/simulation/kernel.ts";

const repulsion: AtlasLaw = { rigidity: 0.15, repulsion: 2_500, attraction: 0, range: 0 };
const noForce: AtlasLaw = { rigidity: 0.15, repulsion: 0, attraction: 0, range: 0 };

function stepConfiguration(overrides: Record<string, unknown> = {}) {
  return {
    timestep: 0.01,
    container: { originX: 0, originY: 0, side: 3 },
    pairLaw: repulsion,
    wallLaw: noForce,
    baseCell: 1.5,
    contactDamping: 0,
    contactScale: 1,
    spring: { stiffness: 0, damping: 0, quarterTurn: false },
    forcing: { linear: 0, angular: 0, time: 0 },
    maxSpeed: 40,
    maxSpin: 20,
    ...overrides,
  };
}

test("one shared step separates a pair symmetrically and reports exact work", () => {
  const state = createSimulationState({
    squares: [
      { x: 0.7, y: 1.5, angle: 0, size: 1 },
      { x: 1.5, y: 1.5, angle: 0, size: 1 },
    ],
    bodies: [
      { members: [0], angle: 0, target: { x: 0.7, y: 1.5, angle: 0 }, torqueFactor: 0.15 },
      { members: [1], angle: 0, target: { x: 1.5, y: 1.5, angle: 0 }, torqueFactor: 0.15 },
    ],
    container: { originX: 0, originY: 0, side: 3 },
    seed: 0,
    frequencyRange: [2.5, 4],
  });

  const receipt = advanceSimulation(state, stepConfiguration());
  const snapshot = simulationSnapshot(state);

  assert.equal(receipt.work.steps, 1);
  assert.equal(receipt.work.pairCandidates, 1);
  assert.equal(receipt.work.pairForces, 1);
  assert(Math.abs(receipt.deepestPairPenetration - 0.2) < 1e-12);
  assert.deepEqual(
    snapshot.poses.map(({ x, y, angle }) => [x, y, angle]),
    [
      [0.6625, 1.5, 0.016875],
      [1.5375, 1.5, -0.016875],
    ],
  );
  assert.equal(snapshot.container.side, 3);
});

test("the same kernel handles wall forces, pins, and rigid members", () => {
  const wallState = createSimulationState({
    squares: [{ x: -0.1, y: 1.5, angle: 0, size: 1 }],
    bodies: [{ members: [0], angle: 0, target: { x: -0.1, y: 1.5, angle: 0 }, torqueFactor: 0.15 }],
    container: { originX: 0, originY: 0, side: 3 },
    seed: 1,
    frequencyRange: [2.5, 4],
  });
  const wallReceipt = advanceSimulation(
    wallState,
    stepConfiguration({ pairLaw: noForce, wallLaw: repulsion }),
  );
  assert.equal(wallReceipt.work.wallForces, 2);
  assert(Math.abs((simulationSnapshot(wallState).poses[0]?.x ?? 0) + 0.025) < 1e-12);

  const rigid = createSimulationState({
    squares: [
      { x: 1, y: 1.5, angle: 0, size: 1 },
      { x: 2, y: 1.5, angle: 0, size: 1 },
    ],
    bodies: [{ members: [0, 1], angle: 0, target: { x: 1.5, y: 1.5, angle: 0 }, torqueFactor: 1 }],
    container: { originX: 0, originY: 0, side: 3 },
    seed: 2,
    frequencyRange: [2.5, 4],
  });
  const rigidReceipt = advanceSimulation(
    rigid,
    stepConfiguration({
      pinned: { body: 0, x: 1.5, y: 2, angle: Math.PI / 2 },
    }),
  );
  const rigidPoses = simulationSnapshot(rigid).poses;
  assert.equal(rigidReceipt.work.pairCandidates, 0);
  assert(Math.abs((rigidPoses[0]?.x ?? 0) - 1.5) < 1e-12);
  assert(Math.abs((rigidPoses[0]?.y ?? 0) - 1.5) < 1e-12);
  assert(Math.abs((rigidPoses[1]?.x ?? 0) - 1.5) < 1e-12);
  assert(Math.abs((rigidPoses[1]?.y ?? 0) - 2.5) < 1e-12);
});

test("attraction follows the declared relationship mask and forcing is repeatable", () => {
  const definition = {
    squares: [
      { x: 0.7, y: 1.5, angle: 0, size: 1 },
      { x: 1.8, y: 1.5, angle: 0, size: 1 },
    ],
    bodies: [
      { members: [0], angle: 0, target: { x: 0.7, y: 1.5, angle: 0 }, torqueFactor: 0.15 },
      { members: [1], angle: 0, target: { x: 1.8, y: 1.5, angle: 0 }, torqueFactor: 0.15 },
    ],
    container: { originX: 0, originY: 0, side: 3 },
    seed: 17,
    frequencyRange: [2.5, 4] as const,
  };
  const sticky: AtlasLaw = { rigidity: 0.15, repulsion: 2_500, attraction: 120, range: 0.25 };
  const excluded = createSimulationState(definition);
  const included = createSimulationState(definition);
  const mask = new Uint8Array(4);
  advanceSimulation(
    excluded,
    stepConfiguration({
      pairLaw: sticky,
      relatedMask: mask,
      forcing: { linear: 3, angular: 2, time: 0.4 },
    }),
  );
  mask[1] = 1;
  const attracted = advanceSimulation(
    included,
    stepConfiguration({
      pairLaw: sticky,
      relatedMask: mask,
      forcing: { linear: 3, angular: 2, time: 0.4 },
    }),
  );
  assert.equal(attracted.nearPairs, 1);
  assert.notDeepEqual(simulationSnapshot(excluded).poses, simulationSnapshot(included).poses);

  const replay = createSimulationState(definition);
  advanceSimulation(
    replay,
    stepConfiguration({
      pairLaw: sticky,
      relatedMask: mask,
      forcing: { linear: 3, angular: 2, time: 0.4 },
    }),
  );
  assert.deepEqual(simulationSnapshot(replay).poses, simulationSnapshot(included).poses);
  assert.equal(replay.seed, 17);
});

test("invalid definitions and nonfinite step inputs fail before mutation", () => {
  assert.throws(
    () =>
      createSimulationState({
        squares: [{ x: 0, y: 0, angle: 0, size: 1 }],
        bodies: [],
        container: { originX: 0, originY: 0, side: 3 },
        seed: 0,
        frequencyRange: [2.5, 4],
      }),
    /requires squares and bodies/,
  );
  const state = createSimulationState({
    squares: [{ x: 1, y: 1, angle: 0, size: 1 }],
    bodies: [{ members: [0], angle: 0, target: { x: 1, y: 1, angle: 0 }, torqueFactor: 0.15 }],
    container: { originX: 0, originY: 0, side: 3 },
    seed: 0,
    frequencyRange: [2.5, 4],
  });
  const before = simulationSnapshot(state);
  assert.throws(
    () => advanceSimulation(state, stepConfiguration({ timestep: Number.NaN })),
    /timestep/,
  );
  assert.deepEqual(simulationSnapshot(state), before);
});

test("a huge container keeps the broad-phase grid bounded and still finds every contact", () => {
  // The same cap `core/geometry.ts` puts on its grid (#160 R15). Uncapped, side 2,000
  // needs a 1,337-cell-wide grid, and side 1e6 cannot be allocated at all.
  const maximumDimension = 512;
  assert.equal(MAX_BROAD_PHASE_DIMENSION, maximumDimension);
  for (const side of [2_000, 1e6]) {
    // One touching pair near the origin, one mid-container, one just outside the far wall,
    // where the clamped cell mapping puts squares that belong to no cell.
    for (const x of [0.7, side / 2, side + 1]) {
      const state = createSimulationState({
        squares: [
          { x, y: 1.5, angle: 0, size: 1 },
          { x: x + 0.8, y: 1.5, angle: 0, size: 1 },
        ],
        bodies: [
          { members: [0], angle: 0, target: { x, y: 1.5, angle: 0 }, torqueFactor: 0.15 },
          { members: [1], angle: 0, target: { x: x + 0.8, y: 1.5, angle: 0 }, torqueFactor: 0.15 },
        ],
        container: { originX: 0, originY: 0, side },
        seed: 0,
        frequencyRange: [2.5, 4],
      });
      const receipt = advanceSimulation(
        state,
        stepConfiguration({ container: { originX: 0, originY: 0, side } }),
      );
      assert.ok(
        state.gridDimension <= maximumDimension,
        `side ${side}: a ${state.gridDimension}-cell-wide grid`,
      );
      assert.equal(receipt.work.pairCandidates, 1, `side ${side}, x ${x}`);
      assert.equal(receipt.work.pairForces, 1, `side ${side}, x ${x}`);
      assert(Math.abs(receipt.deepestPairPenetration - 0.2) < 1e-9, `side ${side}, x ${x}`);
    }
  }
});

test("below the cap the broad-phase grid is exactly the one the kernel always built", () => {
  // The formula before the cap, kept here so a change to ordinary grids cannot pass unseen:
  // pair visits follow the grid, and force sums follow the visits, so the same grid is what
  // keeps an ordinary run bit-for-bit the same.
  const uncapped = (side: number, cell: number) => Math.max(2, Math.ceil((side + 4) / cell) + 1);
  let ordinary = 0;
  for (const side of [0.5, 1, 3, 4.675, 20, 84, 400, 760]) {
    for (const cell of [1.5, Math.SQRT2 + 1e-9, 2.25, 3]) {
      const dimension = uncapped(side, cell);
      if (dimension <= MAX_BROAD_PHASE_DIMENSION) {
        ordinary += 1;
        assert.deepEqual(broadPhaseGrid(side, cell), { dimension, cell }, `side ${side}`);
      }
    }
  }
  assert.equal(ordinary, 31);
  for (const side of [763, 2_000, 1e6, 1e300]) {
    const grid = broadPhaseGrid(side, 1.5);
    assert.equal(grid.dimension, MAX_BROAD_PHASE_DIMENSION, `side ${side}`);
    assert.ok(grid.cell >= 1.5 && grid.cell * (grid.dimension - 1) >= side + 4, `side ${side}`);
  }
});
