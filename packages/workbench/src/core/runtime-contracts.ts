const UINT32_MAX = 0xffff_ffff;
const SEED_STRIDE = 0x9e37_79b1;
const GEOMETRY_TOLERANCE = 1e-9;

export interface SquarePose {
  x: number;
  y: number;
  angle: number;
}

export interface PackingContainer {
  originX: number;
  originY: number;
  side: number;
}

export interface PackingSnapshot {
  squareSide: number;
  container: PackingContainer;
  poses: readonly SquarePose[];
}

export interface PackingBounds {
  minX: number;
  maxX: number;
  minY: number;
  maxY: number;
}

export interface PackingAssessment {
  snapshot: PackingSnapshot;
  valid: boolean;
  reason: string | null;
  requiredSide: number;
  bounds: PackingBounds;
  maxPairOverlap: number;
  maxWallOverlap: number;
}

export interface BestPacking extends PackingSnapshot {
  squareSide: 1;
  at: number;
  requiredSide: number;
  maxPairOverlap: number;
  maxWallOverlap: number;
}

/** Return an exact unsigned 32-bit seed, or refuse the value without coercion. */
export function parseUint32Seed(value: unknown): number | null {
  return typeof value === "number" && Number.isInteger(value) && value >= 0 && value <= UINT32_MAX
    ? value
    : null;
}

/** Fold an exact run seed into a generator base without losing low integer bits. */
export function mixUint32Seed(base: number, seed: number): number {
  const checkedBase = parseUint32Seed(base);
  const checkedSeed = parseUint32Seed(seed);
  if (checkedBase === null || checkedSeed === null) {
    throw new RangeError("seed mixing requires unsigned 32-bit integers");
  }
  return (checkedBase + Math.imul(checkedSeed, SEED_STRIDE)) >>> 0;
}

/** Create the workbench's deterministic linear congruential random stream. */
export function seededRandom(seedValue: number): () => number {
  const checkedSeed = parseUint32Seed(seedValue);
  if (checkedSeed === null) {
    throw new RangeError("the random generator requires an unsigned 32-bit seed");
  }
  let seed = (Math.imul(checkedSeed, 2_654_435_761) + 0x9e37_79b9) >>> 0;
  return () => {
    seed = (Math.imul(seed, 1_664_525) + 1_013_904_223) >>> 0;
    return seed / 4_294_967_296;
  };
}

function valueAt(values: ArrayLike<number>, index: number): number {
  const value = values[index];
  if (value === undefined) {
    throw new RangeError(`pose buffer has no value at index ${index}`);
  }
  return value;
}

function poseAt(poses: readonly SquarePose[], index: number): SquarePose {
  const pose = poses[index];
  if (pose === undefined) {
    throw new RangeError(`pose list has no value at index ${index}`);
  }
  return pose;
}

function poseBounds(poses: readonly SquarePose[], squareSide: number): PackingBounds {
  let minX = Infinity;
  let maxX = -Infinity;
  let minY = Infinity;
  let maxY = -Infinity;
  const half = squareSide / 2;
  for (const pose of poses) {
    const radius = half * (Math.abs(Math.cos(pose.angle)) + Math.abs(Math.sin(pose.angle)));
    minX = Math.min(minX, pose.x - radius);
    maxX = Math.max(maxX, pose.x + radius);
    minY = Math.min(minY, pose.y - radius);
    maxY = Math.max(maxY, pose.y + radius);
  }
  return { minX, maxX, minY, maxY };
}

/** Copy live numeric buffers into a snapshot with an explicit or tight container. */
export function packingSnapshot(
  x: ArrayLike<number>,
  y: ArrayLike<number>,
  angle: ArrayLike<number>,
  squareSide: number,
  container: PackingContainer | null,
): PackingSnapshot {
  if (x.length !== y.length || x.length !== angle.length) {
    throw new RangeError("pose buffers must have the same length");
  }
  const poses: SquarePose[] = [];
  for (let index = 0; index < x.length; index += 1) {
    poses.push({
      x: valueAt(x, index),
      y: valueAt(y, index),
      angle: valueAt(angle, index),
    });
  }
  if (container !== null) {
    return {
      squareSide,
      container: {
        originX: container.originX,
        originY: container.originY,
        side: container.side,
      },
      poses,
    };
  }
  const bounds = poseBounds(poses, squareSide);
  return {
    squareSide,
    container: {
      originX: bounds.minX,
      originY: bounds.minY,
      side: Math.max(bounds.maxX - bounds.minX, bounds.maxY - bounds.minY),
    },
    poses,
  };
}

/** Copy poses into their smallest axis-aligned square container. */
export function tightPackingSnapshot(
  x: ArrayLike<number>,
  y: ArrayLike<number>,
  angle: ArrayLike<number>,
  squareSide: number,
): PackingSnapshot {
  return packingSnapshot(x, y, angle, squareSide, null);
}

function pairOverlap(a: SquarePose, b: SquarePose, squareSide: number): number {
  const dx = b.x - a.x;
  const dy = b.y - a.y;
  const ac = Math.cos(a.angle);
  const as = Math.sin(a.angle);
  const bc = Math.cos(b.angle);
  const bs = Math.sin(b.angle);
  const axes: readonly (readonly [number, number])[] = [
    [ac, as],
    [-as, ac],
    [bc, bs],
    [-bs, bc],
  ];
  let penetration = Infinity;
  for (const [axisX, axisY] of axes) {
    const radiusA =
      (squareSide * (Math.abs(axisX * ac + axisY * as) + Math.abs(-axisX * as + axisY * ac))) / 2;
    const radiusB =
      (squareSide * (Math.abs(axisX * bc + axisY * bs) + Math.abs(-axisX * bs + axisY * bc))) / 2;
    const overlap = radiusA + radiusB - Math.abs(dx * axisX + dy * axisY);
    if (overlap <= GEOMETRY_TOLERANCE) {
      return Math.max(0, overlap);
    }
    penetration = Math.min(penetration, overlap);
  }
  return penetration;
}

/** Recompute every packing-admission fact from the copied snapshot. */
export function assessPackingSnapshot(
  snapshot: PackingSnapshot,
  expectedCount: number,
): PackingAssessment {
  const bounds = poseBounds(snapshot.poses, snapshot.squareSide);
  const requiredSide = Math.max(bounds.maxX - bounds.minX, bounds.maxY - bounds.minY);
  const base = {
    snapshot,
    requiredSide,
    bounds,
    maxPairOverlap: 0,
    maxWallOverlap: 0,
  };
  if (
    !Number.isInteger(expectedCount) ||
    expectedCount < 1 ||
    snapshot.poses.length !== expectedCount
  ) {
    return { ...base, valid: false, reason: "count" };
  }
  const numbers = [
    snapshot.squareSide,
    snapshot.container.originX,
    snapshot.container.originY,
    snapshot.container.side,
    requiredSide,
  ];
  for (const pose of snapshot.poses) {
    numbers.push(pose.x, pose.y, pose.angle);
  }
  if (!numbers.every(Number.isFinite)) {
    return { ...base, valid: false, reason: "nonfinite" };
  }
  if (!(snapshot.squareSide > 0) || !(snapshot.container.side > 0)) {
    return { ...base, valid: false, reason: "dimensions" };
  }

  const wallMaxX = snapshot.container.originX + snapshot.container.side;
  const wallMaxY = snapshot.container.originY + snapshot.container.side;
  const half = snapshot.squareSide / 2;
  let maxWallOverlap = 0;
  for (const pose of snapshot.poses) {
    const radius = half * (Math.abs(Math.cos(pose.angle)) + Math.abs(Math.sin(pose.angle)));
    maxWallOverlap = Math.max(
      maxWallOverlap,
      snapshot.container.originX - (pose.x - radius),
      pose.x + radius - wallMaxX,
      snapshot.container.originY - (pose.y - radius),
      pose.y + radius - wallMaxY,
    );
  }

  let maxPairOverlap = 0;
  for (let left = 0; left < snapshot.poses.length; left += 1) {
    for (let right = left + 1; right < snapshot.poses.length; right += 1) {
      maxPairOverlap = Math.max(
        maxPairOverlap,
        pairOverlap(
          poseAt(snapshot.poses, left),
          poseAt(snapshot.poses, right),
          snapshot.squareSide,
        ),
      );
    }
  }
  const measured = { ...base, maxPairOverlap, maxWallOverlap };
  if (maxPairOverlap > GEOMETRY_TOLERANCE) {
    return { ...measured, valid: false, reason: "pair-overlap" };
  }
  if (maxWallOverlap > GEOMETRY_TOLERANCE) {
    return { ...measured, valid: false, reason: "wall-overlap" };
  }
  return { ...measured, valid: true, reason: null };
}

/** Admit and deep-copy a smaller valid unit-square packing snapshot. */
export function admitBestPacking(
  current: BestPacking | null,
  candidate: PackingAssessment,
  at: number,
): BestPacking | null {
  if (
    !candidate.valid ||
    candidate.snapshot.squareSide !== 1 ||
    !Number.isFinite(at) ||
    (current !== null && candidate.requiredSide >= current.requiredSide)
  ) {
    return current;
  }
  return {
    squareSide: 1,
    container: { ...candidate.snapshot.container },
    poses: candidate.snapshot.poses.map((pose) => ({ ...pose })),
    at,
    requiredSide: candidate.requiredSide,
    maxPairOverlap: candidate.maxPairOverlap,
    maxWallOverlap: candidate.maxWallOverlap,
  };
}

export const workbenchCore = Object.freeze({
  parseUint32Seed,
  mixUint32Seed,
  seededRandom,
  packingSnapshot,
  tightPackingSnapshot,
  assessPackingSnapshot,
  admitBestPacking,
});

export type WorkbenchCore = typeof workbenchCore;
