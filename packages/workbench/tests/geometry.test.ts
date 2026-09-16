import assert from "node:assert/strict";
import { test } from "node:test";
import {
  degreesToRadians,
  type GeometrySnapshot,
  measureFrameGeometry,
  measurePackingGeometry,
  pairPenetration,
} from "../src/core/geometry.ts";

const CONTACT_OPTIONS = {
  gap: 0.01,
  angleToleranceRadians: degreesToRadians(0.5),
};

function snapshot(
  poses: GeometrySnapshot["poses"],
  side: number,
  squareSide = 1,
): GeometrySnapshot {
  return {
    squareSide,
    container: { originX: 0, originY: 0, side },
    poses,
  };
}

test("geometry measures pair, wall, and full-side contact facts from one pose", () => {
  const touching = measurePackingGeometry(
    snapshot(
      [
        { x: 0.5, y: 0.5, angle: 0 },
        { x: 1.5, y: 0.5, angle: 0 },
      ],
      2,
    ),
    CONTACT_OPTIONS,
  );
  assert.deepEqual(touching.contacts, [3, 3]);
  assert.deepEqual(touching.contactEdges, [0, 1]);
  assert.equal(touching.totalOverlap, 0);
  assert.equal(touching.deepestOverlap, 0);
  assert.equal(touching.overlapPairs, 0);
  assert.equal(touching.maxWallOverlap, 0);

  const overlap = measurePackingGeometry(
    snapshot(
      [
        { x: 0.5, y: 0.5, angle: 0 },
        { x: 1.49, y: 0.5, angle: 0 },
      ],
      2,
    ),
    CONTACT_OPTIONS,
  );
  assert(Math.abs(overlap.totalOverlap - 0.01) < 1e-12);
  assert(Math.abs(overlap.deepestOverlap - 0.01) < 1e-12);
  assert.equal(overlap.overlapPairs, 1);

  const turned = measurePackingGeometry(
    snapshot([{ x: 0.5, y: 0.5, angle: Math.PI / 4 }], 1),
    CONTACT_OPTIONS,
  );
  assert(Math.abs(turned.maxWallOverlap - (Math.SQRT1_2 - 0.5)) < 1e-12);
  assert.equal(turned.wallOverlapTotal, turned.maxWallOverlap);
  assert.deepEqual(turned.contacts, [0]);
});

test("legacy degree buffers adapt to the normalized radian geometry contract", () => {
  const fromDegrees = measureFrameGeometry(
    new Float64Array([0.5, 1.49]),
    new Float64Array([0.5, 0.5]),
    new Float64Array([0, 0]),
    2,
    1,
    { gap: 0.01, angleToleranceDegrees: 0.5 },
  );
  const normalized = measurePackingGeometry(
    snapshot(
      [
        { x: 0.5, y: 0.5, angle: 0 },
        { x: 1.49, y: 0.5, angle: 0 },
      ],
      2,
    ),
    CONTACT_OPTIONS,
  );
  assert.deepEqual(fromDegrees, normalized);
});

test("pair penetration is symmetric, rotation-aware, and zero at separation", () => {
  const left = { x: 0.5, y: 0.5, angle: 0 };
  const right = { x: 1.5, y: 0.5, angle: 0 };
  assert.equal(pairPenetration(left, right, 1), 0);
  assert.equal(pairPenetration(right, left, 1), 0);

  const rotated = { x: 1.55, y: 0.5, angle: Math.PI / 4 };
  assert(pairPenetration(left, rotated, 1) > 0);
  assert.equal(pairPenetration(left, rotated, 1), pairPenetration(rotated, left, 1));

  assert.throws(() => pairPenetration(left, { x: Number.NaN, y: 0, angle: 0 }, 1), /finite/);
});
