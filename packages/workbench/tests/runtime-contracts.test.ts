import assert from "node:assert/strict";
import { test } from "node:test";
import {
  workbenchCore as core,
  type PackingSnapshot,
  type SquarePose,
} from "../src/core/runtime-contracts.ts";

function snapshot(poses: readonly SquarePose[], side: number, squareSide = 1): PackingSnapshot {
  return {
    squareSide,
    container: { originX: 0, originY: 0, side },
    poses,
  };
}

test("uint32 seeds preserve seed zero, distinguish the known alias, and reject bad input", () => {
  assert.equal(core.mixUint32Seed(17, 0), 17);
  assert.equal(core.mixUint32Seed(17, 1), 2_654_435_778);
  assert.equal(core.mixUint32Seed(17, 0xffff_ffff), 1_640_531_552);
  assert.equal(core.mixUint32Seed(17, 79_049_217), 3_151_104_962);
  assert.equal(core.mixUint32Seed(17, 29_207_060), 3_151_104_997);
  assert.notEqual(core.mixUint32Seed(17, 79_049_217), core.mixUint32Seed(17, 29_207_060));

  const defaultRandom = core.seededRandom(core.mixUint32Seed(17, 0));
  assert.deepEqual(
    Array.from({ length: 3 }, defaultRandom),
    [0.6321227292064577, 0.32190035190433264, 0.41932153212837875],
  );
  const replay = core.seededRandom(core.mixUint32Seed(17, 79_049_217));
  const replayAgain = core.seededRandom(core.mixUint32Seed(17, 79_049_217));
  const distinct = core.seededRandom(core.mixUint32Seed(17, 29_207_060));
  const replayValues = Array.from({ length: 4 }, replay);
  assert.deepEqual(replayValues, Array.from({ length: 4 }, replayAgain));
  assert.notDeepEqual(replayValues, Array.from({ length: 4 }, distinct));

  assert.equal(core.parseUint32Seed(0), 0);
  assert.equal(core.parseUint32Seed(0xffff_ffff), 0xffff_ffff);
  for (const bad of [-1, 0x1_0000_0000, 1.5, Number.NaN, Infinity, "17", null]) {
    assert.equal(core.parseUint32Seed(bad), null, `accepted ${String(bad)}`);
  }
});

test("snapshot validation fails closed on count, finite, pair, and wall violations", () => {
  const valid = core.assessPackingSnapshot(
    snapshot(
      [
        { x: 0.5, y: 0.5, angle: 0 },
        { x: 1.5, y: 0.5, angle: 0 },
      ],
      2,
    ),
    2,
  );
  assert.equal(valid.valid, true);
  assert.equal(valid.maxPairOverlap, 0);
  assert.equal(valid.maxWallOverlap, 0);

  const wrongCount = core.assessPackingSnapshot(snapshot(valid.snapshot.poses, 2), 3);
  assert.equal(wrongCount.valid, false);
  assert.equal(wrongCount.reason, "count");

  const nonfinite = core.assessPackingSnapshot(
    snapshot([{ x: 0.5, y: 0.5, angle: Number.NaN }], 1),
    1,
  );
  assert.equal(nonfinite.valid, false);
  assert.equal(nonfinite.reason, "nonfinite");

  const overlapping = core.assessPackingSnapshot(
    snapshot(
      [
        { x: 0.5, y: 0.5, angle: 0 },
        { x: 1.49, y: 0.5, angle: 0 },
      ],
      2,
    ),
    2,
  );
  assert.equal(overlapping.valid, false);
  assert.equal(overlapping.reason, "pair-overlap");
  assert(overlapping.maxPairOverlap > 0.009);

  const throughWall = core.assessPackingSnapshot(snapshot([{ x: 0.49, y: 0.5, angle: 0 }], 1), 1);
  assert.equal(throughWall.valid, false);
  assert.equal(throughWall.reason, "wall-overlap");
  assert(throughWall.maxWallOverlap > 0.009);
});

test("best admission uses the assessed pose, ignores stale dynamics, and stores a copy", () => {
  const x = new Float64Array([0.5, 1.5]);
  const y = new Float64Array([0.5, 0.5]);
  const angle = new Float64Array([0, 0]);
  const first = core.assessPackingSnapshot(core.tightPackingSnapshot(x, y, angle, 1), 2);
  const best = core.admitBestPacking(null, first, 0);
  assert(best !== null);
  assert.equal(best.container.side, 2);

  x[0] = 99;
  y[0] = 99;
  angle[0] = Math.PI;
  assert.equal(best.poses[0]?.x, 0.5);
  assert.equal(best.poses[0]?.y, 0.5);
  assert.equal(best.poses[0]?.angle, 0);
  assert(best.poses.every((pose) => [pose.x, pose.y, pose.angle].every(Number.isFinite)));
  const stored = core.assessPackingSnapshot(best, 2);
  assert.equal(stored.valid, true);
  assert.equal(stored.maxPairOverlap, 0);
  assert.equal(stored.maxWallOverlap, 0);

  // This pose is smaller than the standing best, so the old pre-integration penetration could
  // admit it after a feasible-to-overlapping step. Admission must use this pose's own assessment.
  const crossedIntoOverlap = core.assessPackingSnapshot(
    core.tightPackingSnapshot([0.5, 1.49], [0.5, 0.5], [0, 0], 1),
    2,
  );
  assert(crossedIntoOverlap.snapshot.container.side < best.container.side);
  assert.equal(crossedIntoOverlap.valid, false);
  assert.strictEqual(core.admitBestPacking(best, crossedIntoOverlap, 1), best);

  const beforeRotation = core.assessPackingSnapshot(
    core.tightPackingSnapshot([0.5, 1.55], [0.5, 0.5], [0, 0], 1),
    2,
  );
  const afterRotation = core.assessPackingSnapshot(
    core.tightPackingSnapshot([0.5, 1.55], [0.5, 0.5], [0, Math.PI / 4], 1),
    2,
  );
  assert.equal(beforeRotation.valid, true);
  assert.equal(afterRotation.reason, "pair-overlap");
  assert.strictEqual(core.admitBestPacking(best, afterRotation, 1), best);

  const beforeGrowth = core.assessPackingSnapshot(
    core.tightPackingSnapshot([0.25, 0.8], [0.25, 0.25], [0, 0], 0.5),
    2,
  );
  const afterGrowth = core.assessPackingSnapshot(
    core.tightPackingSnapshot([0.25, 0.8], [0.25, 0.25], [0, 0], 1),
    2,
  );
  assert.equal(beforeGrowth.valid, true);
  assert.equal(afterGrowth.reason, "pair-overlap");
  assert.strictEqual(core.admitBestPacking(best, afterGrowth, 1), best);

  // A valid instantaneous pose ranks on its own evidence; convergence is a separate claim.
  const tighterValid = core.assessPackingSnapshot(
    core.tightPackingSnapshot([0.5], [0.5], [0], 1),
    1,
  );
  const admitted = core.admitBestPacking(best, tighterValid, 2);
  assert(admitted !== null);
  assert.equal(admitted.container.side, 1);
  assert.equal(admitted.at, 2);
});

test("a geometrically valid sub-unit state cannot rank as a unit-square packing", () => {
  const growing = core.assessPackingSnapshot(
    core.tightPackingSnapshot([0.25, 0.75], [0.25, 0.25], [0, 0], 0.5),
    2,
  );
  assert.equal(growing.valid, true);
  assert.equal(growing.snapshot.squareSide, 0.5);
  assert.equal(core.admitBestPacking(null, growing, 0), null);
});
