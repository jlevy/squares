import assert from "node:assert/strict";
import { test } from "node:test";
import type { AtlasLaw } from "../src/api/workbench-api.ts";
import type { CorpusFrame, CorpusPair } from "../src/data/corpus.ts";
import {
  buildTrajectory,
  sampleTrajectoryPose,
  sampleTrajectorySide,
  type TrajectoryRequest,
} from "../src/simulation/trajectory.ts";

const source: CorpusFrame = {
  side: 2,
  ident: [1, 2],
  squares: [
    [0.5, 0.5, 0, "#000000", 2],
    [1.5, 0.5, 0, "#000000", 2],
  ],
};
const target: CorpusFrame = {
  side: 2,
  ident: [1, 2, 3],
  squares: [
    [0.5, 0.5, 0, "#000000", 2],
    [1.5, 0.5, 0, "#000000", 2],
    [1, 1.5, 0, "#000000", 2],
  ],
};
const pair: CorpusPair = {
  n: 2,
  kind: "matched",
  map: [0, 1],
  new: 2,
  new_rule: "test",
  new_tied: 0,
  blocks: [
    {
      members: [0, 1],
      riders: [],
      cluster: 0,
      turn: 0,
      from: [1, 0.5],
      to: [1, 0.5],
      drift_max: 0,
    },
  ],
  block_of: [0, 0],
  prev_new: null,
  stats: {},
};
const law: AtlasLaw = { rigidity: 0.15, repulsion: 2_500, attraction: 0, range: 0 };

function request(overrides: Partial<TrajectoryRequest> = {}): TrajectoryRequest {
  return {
    pairIndex: 0,
    pair,
    source,
    target,
    steps: 24,
    style: "physics",
    mode: "snap",
    effectiveSeed: 17,
    pairLaw: law,
    wallLaw: law,
    relatedMask: null,
    anneal: { level: 3, amplitude: 1, decayPower: 1.5, span: 1 },
    physics: {
      omega: 10,
      zeta: 0.85,
      springRamp: 0.25,
      contactDamping: 20,
      contactTorque: 0.15,
      lockIn: 0.7,
      open: 0.3,
      openBy: 0.3,
      shutFrom: 0.62,
      tighten: 16,
      tightenFrom: 0.68,
      grow: 0.5,
      jiggle: 20,
      jiggleTorque: 12,
      bodiesJiggle: 40,
      bodiesJiggleTorque: 24,
      jiggleHz: [2.5, 4],
      drop: 0,
      appear: 0.15,
      inflateFrom: 0.3,
      blend: 0.12,
      maxSpeed: 40,
      maxSpin: 20,
      cell: 1.5,
    },
    blind: {
      inflate: 1.12,
      hold: 0.2,
      close: 0.9,
      overlapTolerance: 0.08,
      gridStep: 0.25,
    },
    ...overrides,
  };
}

test("snap trajectories are deterministic, exact at both ends, and openly step-limited", () => {
  const first = buildTrajectory(request());
  const replay = buildTrajectory(request());
  assert.deepEqual(first.states, replay.states);
  assert.deepEqual(first.receipt, replay.receipt);
  assert.deepEqual(sampleTrajectoryPose(first, 0, 0), [0.5, 0.5, 0]);
  assert.deepEqual(sampleTrajectoryPose(first, 2, 1), [1, 1.5, 0]);
  assert.equal(sampleTrajectorySide(first, 0), source.side);
  assert.equal(sampleTrajectorySide(first, 1), target.side);
  assert.equal(first.receipt.termination.reason, "step-limit");
  assert.equal(first.receipt.termination.converged, false);
  assert.equal(first.receipt.feasibility.valid, true);
  assert.equal(first.receipt.work.steps, 24);
});

test("body trajectories share rigid members while square trajectories keep separate bodies", () => {
  const squares = buildTrajectory(request({ style: "physics", mode: "free" }));
  const bodies = buildTrajectory(request({ style: "bodies", mode: "free" }));
  assert.equal(squares.bodies, 3);
  assert.equal(bodies.bodies, 2);
  assert.notDeepEqual(squares.states, bodies.states);
  for (const trajectory of [squares, bodies]) {
    assert(trajectory.receipt.residual.maxLinearSpeed >= 0);
    assert(trajectory.receipt.residual.maxAngularSpeed >= 0);
    assert.equal(trajectory.receipt.configuration.mode, "free");
  }
});

test("blind trajectories disclose the squeeze result and never claim guided convergence", () => {
  const trajectory = buildTrajectory(request({ mode: "blind", style: "physics" }));
  assert.equal(trajectory.receipt.configuration.guided, false);
  assert.equal(trajectory.receipt.termination.converged, false);
  assert(trajectory.squeeze >= 0 && trajectory.squeeze <= 1);
  assert.equal(trajectory.sides.length, trajectory.steps + 1);
  assert.equal(trajectory.pens.length, trajectory.steps + 1);
  assert.equal(trajectory.nears.length, trajectory.steps + 1);
});

test("bad counts, step budgets and nonfinite inputs are rejected", () => {
  assert.throws(() => buildTrajectory(request({ steps: 0 })), /step budget/);
  assert.throws(
    () => buildTrajectory(request({ source: { ...source, squares: source.squares.slice(0, 1) } })),
    /source frame/,
  );
  assert.throws(
    () => buildTrajectory(request({ physics: { ...request().physics, omega: Number.NaN } })),
    /omega/,
  );
});

test("annealing level zero is an unforced run, not an invalid request", () => {
  const unforced = buildTrajectory(
    request({ mode: "free", anneal: { level: 0, amplitude: 0, decayPower: 1.5, span: 1 } }),
  );
  assert.equal(unforced.receipt.forcing.active, false);
  assert.equal(unforced.receipt.work.steps, 24);
  assert.throws(
    () =>
      buildTrajectory(request({ anneal: { level: 0, amplitude: -0.1, decayPower: 1.5, span: 1 } })),
    /annealAmplitude/,
  );
});
