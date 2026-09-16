import assert from "node:assert/strict";
import { test } from "node:test";
import type { GeometrySnapshot } from "../src/core/geometry.ts";
import { PACKING_VALIDITY } from "../src/core/runtime-contracts.ts";
import { resolvePacking } from "../src/simulation/resolve.ts";

const configuration = {
  expectedCount: 2,
  iterationLimit: 40,
  tolerance: PACKING_VALIDITY.penetrationTolerance,
} as const;

function snapshot(poses: GeometrySnapshot["poses"], side = 3): GeometrySnapshot {
  return {
    squareSide: 1,
    container: { originX: 0, originY: 0, side },
    poses,
  };
}

test("a valid input is retained as distinct checked raw and repaired copies", () => {
  const input = snapshot([
    { x: 0.5, y: 0.5, angle: 0 },
    { x: 1.5, y: 0.5, angle: 0 },
  ]);
  const result = resolvePacking(input, configuration);
  assert.equal(result.termination.reason, "already-valid");
  assert.equal(result.termination.resolved, true);
  assert.equal(result.work.iterations, 0);
  assert.notEqual(result.raw.snapshot, input);
  assert.notEqual(result.repaired?.snapshot, result.raw.snapshot);
  assert.deepEqual(result.raw.snapshot, input);
  assert.deepEqual(result.repaired?.snapshot.poses, input.poses);
  assert.equal(result.repaired?.snapshot.container.side, 2);
});

test("overlapping rotated squares are translated and post-validated", () => {
  const input = snapshot([
    { x: 1.2, y: 1.5, angle: Math.PI / 12 },
    { x: 1.7, y: 1.5, angle: -Math.PI / 9 },
  ]);
  const result = resolvePacking(input, configuration);
  assert.equal(result.raw.reason, "pair-overlap");
  assert.equal(result.termination.reason, "resolved");
  assert.equal(result.termination.resolved, true);
  assert.equal(result.repaired?.valid, true);
  assert.equal(result.repaired?.snapshot.poses[0]?.angle, input.poses[0]?.angle);
  assert.equal(result.repaired?.snapshot.poses[1]?.angle, input.poses[1]?.angle);
  assert(result.work.pairTests > 0);
  assert(result.work.pairTranslations > 0);
  assert.equal(result.raw.maxPairOverlap > configuration.tolerance, true);
  assert.equal((result.repaired?.maxPairOverlap ?? Infinity) <= configuration.tolerance, true);
});

test("wall overlap is repaired by fitting a lower-left square container", () => {
  const input = snapshot([
    { x: 0.1, y: 0.5, angle: 0 },
    { x: 2.5, y: 2.9, angle: 0 },
  ]);
  const result = resolvePacking(input, configuration);
  assert.equal(result.raw.reason, "wall-overlap");
  assert.equal(result.termination.reason, "resolved");
  assert.equal(result.repaired?.maxWallOverlap, 0);
  assert.equal(result.normalization, "lower-left-square");
  assert(result.work.fitTranslations > 0);
});

test("a tiny input container does not constrain the repaired lower-left fit", () => {
  const result = resolvePacking(
    snapshot(
      [
        { x: 0.5, y: 0.5, angle: 0 },
        { x: 0.5, y: 0.5, angle: 0 },
      ],
      0.75,
    ),
    configuration,
  );
  assert.equal(result.termination.resolved, true);
  assert.equal(result.repaired?.valid, true);
  assert((result.repaired?.snapshot.container.side ?? 0) >= 2);
});

test("iteration exhaustion returns the checked partial repair without a success claim", () => {
  const poses = Array.from({ length: 4 }, () => ({ x: 1, y: 1, angle: 0 }));
  const result = resolvePacking(snapshot(poses), {
    expectedCount: 4,
    iterationLimit: 1,
    tolerance: PACKING_VALIDITY.penetrationTolerance,
  });
  assert.equal(result.termination.reason, "budget-exhausted");
  assert.equal(result.termination.resolved, false);
  assert.equal(result.termination.exhausted, true);
  assert.equal(result.work.iterations, 1);
  assert.equal(result.work.pairTests, 6);
  assert.equal(result.repaired?.reason, "pair-overlap");
});

test("count, dimensions, nonfinite, non-unit and out-of-limit input are refused unrepaired", () => {
  const count = resolvePacking(snapshot([{ x: 0.5, y: 0.5, angle: 0 }]), configuration);
  assert.equal(count.termination.reason, "refused-count");
  assert.equal(count.repaired, null);
  const dimensions = resolvePacking(
    {
      ...snapshot([
        { x: 0.5, y: 0.5, angle: 0 },
        { x: 1.5, y: 0.5, angle: 0 },
      ]),
      squareSide: 0,
    },
    configuration,
  );
  assert.equal(dimensions.termination.reason, "refused-dimensions");
  const nonfinite = resolvePacking(
    snapshot([
      { x: Number.NaN, y: 0.5, angle: 0 },
      { x: 1.5, y: 0.5, angle: 0 },
    ]),
    configuration,
  );
  assert.equal(nonfinite.termination.reason, "refused-nonfinite");
  const halfSize = resolvePacking(
    {
      squareSide: 0.5,
      container: { originX: 0, originY: 0, side: 1 },
      poses: [
        { x: 0.25, y: 0.25, angle: 0 },
        { x: 0.75, y: 0.25, angle: 0 },
      ],
    },
    configuration,
  );
  assert.equal(halfSize.termination.reason, "refused-unit-size");
  assert.equal(halfSize.termination.resolved, false);
  assert.equal(halfSize.repaired, null);
  // Overlapping squares beyond the coordinate limit: fitting them to the origin cannot recover
  // the digits float64 already lost, so Resolve must not report a repaired packing.
  const far = 2 ** 40;
  const beyondLimit = resolvePacking(
    {
      squareSide: 1,
      container: { originX: far, originY: 0, side: 2 },
      poses: [
        { x: far + 0.5, y: 0.5, angle: 0 },
        { x: far + 1.25, y: 0.5, angle: 0 },
      ],
    },
    configuration,
  );
  assert.equal(beyondLimit.termination.reason, "refused-magnitude");
  assert.equal(beyondLimit.repaired, null);
  assert.deepEqual(nonfinite.work, {
    iterations: 0,
    pairTests: 0,
    pairTranslations: 0,
    fitTranslations: 0,
  });
});

test("invalid bounds are rejected before repair", () => {
  const input = snapshot([
    { x: 0.5, y: 0.5, angle: 0 },
    { x: 1.5, y: 0.5, angle: 0 },
  ]);
  assert.throws(
    () => resolvePacking(input, { ...configuration, iterationLimit: 0 }),
    /iteration limit/,
  );
  assert.throws(
    () =>
      resolvePacking(input, {
        ...configuration,
        tolerance: 2 * PACKING_VALIDITY.penetrationTolerance,
      }),
    /tolerance/,
  );
});

test("cancellation returns the last checked repair state and exact work", () => {
  const input = snapshot([
    { x: 1.2, y: 1.5, angle: Math.PI / 12 },
    { x: 1.7, y: 1.5, angle: -Math.PI / 9 },
  ]);
  const result = resolvePacking(input, configuration, { shouldCancel: () => true });
  assert.equal(result.termination.reason, "cancelled");
  assert.equal(result.termination.resolved, false);
  assert.deepEqual(result.repaired, result.raw);
  assert.deepEqual(result.work, {
    iterations: 0,
    pairTests: 0,
    pairTranslations: 0,
    fitTranslations: 0,
  });
});

test("fitting at zero tolerance cannot claim success for a rounded wall overlap", () => {
  const result = resolvePacking(
    snapshot([{ x: 1.61, y: 0.45099999999999996, angle: 0.151 }], 100),
    { expectedCount: 1, iterationLimit: 1, tolerance: 0 },
  );
  assert((result.repaired?.maxWallOverlap ?? 0) > 0);
  assert.equal(result.termination.reason, "stalled");
  assert.equal(result.termination.resolved, false);
});

test("cancellation is observed before the fast fitting path", () => {
  const result = resolvePacking(
    snapshot([{ x: 0.5, y: 0.5, angle: 0 }]),
    { expectedCount: 1, iterationLimit: 1, tolerance: PACKING_VALIDITY.penetrationTolerance },
    { shouldCancel: () => true },
  );
  assert.equal(result.termination.reason, "cancelled");
  assert.equal(result.termination.resolved, false);
  assert.equal(result.work.fitTranslations, 0);
});
