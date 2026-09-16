import {
  type GeometryBounds,
  type GeometryContainer,
  type GeometryPose,
  type GeometrySnapshot,
  measurePackingGeometry,
  packingBounds,
} from "./geometry.ts";

const UINT32_MAX = 0xffff_ffff;
const SEED_STRIDE = 0x9e37_79b1;

/**
 * The one validity contract for a packing of unit squares.
 *
 * Pack, Resolve, Search and the benchmark probe take validity from here, and so does anything on
 * the page that calls an arrangement a packing. `tools/workbench_tools/packing_contracts.py`
 * applies the same clauses with the same values. `tests/fixtures/packing-validity.json` holds
 * arrangements just inside and just outside each clause, and both `node --test` and pytest must
 * reach its verdicts.
 *
 * An assessment reports the first clause that fails, in `clauses` order. The pair and wall clauses
 * measure separating-axis penetration: how far one square must move to stop overlapping its
 * neighbour, or to lie inside the container. A penetration of at most `penetrationTolerance` counts
 * as contact, because a tight packing touches along whole sides and float64 cannot hold that at zero.
 */
export const PACKING_VALIDITY = Object.freeze({
  contract: "packing.squares:PackingValidity/v1",
  /** The side of every square in a packing the workbench ranks or reports. */
  squareSide: 1,
  /** The largest pair or wall penetration, in the poses' length unit, that still counts as contact. */
  penetrationTolerance: 1e-9,
  /**
   * The largest centre, container origin, container side or square side the float64 measure is
   * trusted at. Float64 spacing at 2^17, where an origin plus a side can reach, is 2.9e-11, and the
   * pair, wall and side measures each take a few subtractions of such values, so rounding stays
   * under 1.2e-10, a tenth of `penetrationTolerance`. Near 2^52 a centre +- half a side rounds
   * away entirely and overlapping squares read as touching.
   */
  coordinateLimit: 2 ** 16,
  /**
   * The order an assessment reports the first failure in. The two precision clauses follow the
   * geometric ones because they only matter for an arrangement that would otherwise pass.
   * `area-bound`: n squares of side a whose pairs penetrate by at most t still fit, shrunk to side
   * a - 2t, without overlap, so their tight side is at least sqrt(n)(a - 2t); a measured side below
   * that, less one more t for rounding, can only come from arithmetic that lost the geometry.
   */
  clauses: Object.freeze([
    "count",
    "nonfinite",
    "dimensions",
    "pair-overlap",
    "wall-overlap",
    "area-bound",
    "magnitude",
    "unit-size",
  ] as const),
});

/** The smallest side a tolerance-qualified packing of `count` squares can measure (`area-bound`). */
export function areaBound(count: number, squareSide: number, tolerance: number): number {
  return Math.sqrt(count) * (squareSide - 2 * tolerance) - tolerance;
}

/** Whether every length in the snapshot is inside `PACKING_VALIDITY.coordinateLimit` (`magnitude`). */
export function withinCoordinateLimit(snapshot: GeometrySnapshot): boolean {
  const limit = PACKING_VALIDITY.coordinateLimit;
  if (
    Math.abs(snapshot.squareSide) > limit ||
    Math.abs(snapshot.container.originX) > limit ||
    Math.abs(snapshot.container.originY) > limit ||
    Math.abs(snapshot.container.side) > limit
  ) {
    return false;
  }
  return snapshot.poses.every((pose) => Math.abs(pose.x) <= limit && Math.abs(pose.y) <= limit);
}

/**
 * The one declared exception to the contract tolerance: frames at the catalogue's stored precision.
 *
 * The page builder rounds each witness centre to 1e-6 and each angle to 1e-4 degrees
 * (`build_candidate.compact_frame`). Rounding a centre moves a pair's projected distance by at most
 * 1.42e-6; rounding both angles moves it by at most 1.23e-6 through the axis and 1.23e-6 through the
 * other square's projected radius. So a record re-measured at stored precision can read up to 3.9e-6
 * of pair penetration, and 1.2e-6 at a wall, without overlapping; 147 of the 324 stored frames fail
 * the 1e-9 contract for that reason alone (`tests/test_catalogue_precision.py` re-measures both).
 * Only `assessCataloguePrecisionFrame` applies this value, and its assessment records it; nothing
 * that ranks or admits a result may use it.
 */
export const CATALOGUE_PRECISION = Object.freeze({
  contract: "packing.squares:CataloguePrecisionTolerance/v1",
  positionDecimals: 6,
  angleDecimalsDegrees: 4,
  penetrationTolerance: 4e-6,
});

export type PackingValidityClause = (typeof PACKING_VALIDITY.clauses)[number];

export type SquarePose = GeometryPose;
export type PackingContainer = GeometryContainer;
export type PackingSnapshot = GeometrySnapshot;
export type PackingBounds = GeometryBounds;

export interface PackingAssessment {
  snapshot: PackingSnapshot;
  /** Every clause of `PACKING_VALIDITY` holds at `tolerance`. */
  valid: boolean;
  /** Every clause but `unit-size` holds at `tolerance`: sound geometry, whatever the square size. */
  geometryValid: boolean;
  /** The first clause that failed, in `PACKING_VALIDITY.clauses` order. */
  reason: PackingValidityClause | null;
  /** The penetration tolerance this assessment applied. */
  tolerance: number;
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
  const bounds = packingBounds(poses, squareSide);
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

function assessAtTolerance(
  snapshot: PackingSnapshot,
  expectedCount: number,
  tolerance: number,
): PackingAssessment {
  const unavailable = {
    snapshot,
    geometryValid: false,
    tolerance,
    requiredSide: Infinity,
    bounds: { minX: Infinity, maxX: -Infinity, minY: Infinity, maxY: -Infinity },
    maxPairOverlap: 0,
    maxWallOverlap: 0,
  };
  if (
    !Number.isInteger(expectedCount) ||
    expectedCount < 1 ||
    snapshot.poses.length !== expectedCount
  ) {
    return { ...unavailable, valid: false, reason: "count" };
  }
  const numbers = [
    snapshot.squareSide,
    snapshot.container.originX,
    snapshot.container.originY,
    snapshot.container.side,
  ];
  for (const pose of snapshot.poses) {
    numbers.push(pose.x, pose.y, pose.angle);
  }
  if (!numbers.every(Number.isFinite)) {
    return { ...unavailable, valid: false, reason: "nonfinite" };
  }
  if (!(snapshot.squareSide > 0) || !(snapshot.container.side > 0)) {
    return { ...unavailable, valid: false, reason: "dimensions" };
  }
  const geometry = measurePackingGeometry(snapshot);
  const failed: readonly [boolean, PackingValidityClause][] = [
    [geometry.maxPairOverlap > tolerance, "pair-overlap"],
    [geometry.maxWallOverlap > tolerance, "wall-overlap"],
    [
      geometry.requiredSide < areaBound(expectedCount, snapshot.squareSide, tolerance),
      "area-bound",
    ],
    [!withinCoordinateLimit(snapshot), "magnitude"],
    [snapshot.squareSide !== PACKING_VALIDITY.squareSide, "unit-size"],
  ];
  const reason = failed.find(([fails]) => fails)?.[1] ?? null;
  return {
    snapshot,
    valid: reason === null,
    geometryValid: reason === null || reason === "unit-size",
    reason,
    tolerance,
    requiredSide: geometry.requiredSide,
    bounds: geometry.bounds,
    maxPairOverlap: geometry.maxPairOverlap,
    maxWallOverlap: geometry.maxWallOverlap,
  };
}

/** Recompute every clause of the validity contract from the copied snapshot. */
export function assessPackingSnapshot(
  snapshot: PackingSnapshot,
  expectedCount: number,
): PackingAssessment {
  return assessAtTolerance(snapshot, expectedCount, PACKING_VALIDITY.penetrationTolerance);
}

/**
 * Assess a retained catalogue frame at its stored precision, under the declared
 * `CATALOGUE_PRECISION` tolerance. For display of records only; never for admission or ranking.
 */
export function assessCataloguePrecisionFrame(
  snapshot: PackingSnapshot,
  expectedCount: number,
): PackingAssessment {
  return assessAtTolerance(snapshot, expectedCount, CATALOGUE_PRECISION.penetrationTolerance);
}

/** Admit and deep-copy a smaller valid unit-square packing snapshot. */
export function admitBestPacking(
  current: BestPacking | null,
  candidate: PackingAssessment,
  at: number,
): BestPacking | null {
  if (
    !candidate.valid ||
    candidate.tolerance !== PACKING_VALIDITY.penetrationTolerance ||
    candidate.snapshot.squareSide !== PACKING_VALIDITY.squareSide ||
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
  PACKING_VALIDITY,
  CATALOGUE_PRECISION,
  areaBound,
  withinCoordinateLimit,
  parseUint32Seed,
  mixUint32Seed,
  seededRandom,
  packingSnapshot,
  tightPackingSnapshot,
  assessPackingSnapshot,
  assessCataloguePrecisionFrame,
  admitBestPacking,
});

export type WorkbenchCore = typeof workbenchCore;
