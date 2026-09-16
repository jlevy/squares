import { type GeometryPose, type GeometrySnapshot, packingBounds } from "../core/geometry.ts";
import {
  assessPackingSnapshot,
  PACKING_VALIDITY,
  type PackingAssessment,
  withinCoordinateLimit,
} from "../core/runtime-contracts.ts";

export interface ResolveConfiguration {
  expectedCount: number;
  iterationLimit: number;
  /** Maximum permitted pair or wall overlap. Must not exceed `PACKING_VALIDITY.penetrationTolerance`. */
  tolerance: number;
}

export interface ResolveWork {
  iterations: number;
  pairTests: number;
  pairTranslations: number;
  fitTranslations: number;
}

/** Every way a Resolve can end, in the order a receipt's reader should expect to meet them. */
export const RESOLVE_TERMINATION_REASONS = Object.freeze([
  "already-valid",
  "resolved",
  "budget-exhausted",
  "cancelled",
  "stalled",
  "refused-count",
  "refused-dimensions",
  "refused-nonfinite",
  "refused-magnitude",
  "refused-unit-size",
] as const);

export type ResolveTerminationReason = (typeof RESOLVE_TERMINATION_REASONS)[number];

/** The reasons whose receipt carries a checked, valid repaired state. */
export const RESOLVED_TERMINATION_REASONS: readonly ResolveTerminationReason[] = Object.freeze([
  "already-valid",
  "resolved",
]);

export interface ResolveReceipt {
  /** Immutable copy of the input and its pre-repair assessment. */
  raw: PackingAssessment;
  /** Post-repair copy and assessment, absent when input admission was refused. */
  repaired: PackingAssessment | null;
  configuration: ResolveConfiguration;
  work: ResolveWork;
  termination: {
    reason: ResolveTerminationReason;
    resolved: boolean;
    exhausted: boolean;
  };
  normalization: "lower-left-square";
}

export interface ResolveOptions {
  shouldCancel?: () => boolean;
}

interface Translation {
  firstX: number;
  firstY: number;
  secondX: number;
  secondY: number;
}

function copySnapshot(snapshot: GeometrySnapshot): GeometrySnapshot {
  return {
    squareSide: snapshot.squareSide,
    container: { ...snapshot.container },
    poses: snapshot.poses.map((pose) => ({ ...pose })),
  };
}

function validateConfiguration(configuration: ResolveConfiguration): void {
  if (!Number.isSafeInteger(configuration.expectedCount) || configuration.expectedCount < 1) {
    throw new RangeError("Resolve expected count must be a positive integer");
  }
  if (!Number.isSafeInteger(configuration.iterationLimit) || configuration.iterationLimit < 1) {
    throw new RangeError("Resolve iteration limit must be a positive integer");
  }
  if (
    !Number.isFinite(configuration.tolerance) ||
    configuration.tolerance < 0 ||
    configuration.tolerance > PACKING_VALIDITY.penetrationTolerance
  ) {
    throw new RangeError(
      `Resolve tolerance must be between zero and the contract's ${PACKING_VALIDITY.penetrationTolerance}`,
    );
  }
}

function poseAt(poses: readonly GeometryPose[], index: number): GeometryPose {
  const pose = poses[index];
  if (pose === undefined) {
    throw new RangeError(`Resolve has no pose at index ${index}`);
  }
  return pose;
}

function radiusOnAxis(
  axisX: number,
  axisY: number,
  cosine: number,
  sine: number,
  halfSide: number,
): number {
  return (
    halfSide * (Math.abs(axisX * cosine + axisY * sine) + Math.abs(-axisX * sine + axisY * cosine))
  );
}

function pairTranslation(
  first: GeometryPose,
  second: GeometryPose,
  squareSide: number,
  tolerance: number,
): Translation | null {
  const firstCosine = Math.cos(first.angle);
  const firstSine = Math.sin(first.angle);
  const secondCosine = Math.cos(second.angle);
  const secondSine = Math.sin(second.angle);
  const axes: readonly (readonly [number, number])[] = [
    [firstCosine, firstSine],
    [-firstSine, firstCosine],
    [secondCosine, secondSine],
    [-secondSine, secondCosine],
  ];
  const dx = second.x - first.x;
  const dy = second.y - first.y;
  const halfSide = squareSide / 2;
  let penetration = Infinity;
  let normalX = 0;
  let normalY = 0;
  for (const [axisX, axisY] of axes) {
    const projected = dx * axisX + dy * axisY;
    const overlap =
      radiusOnAxis(axisX, axisY, firstCosine, firstSine, halfSide) +
      radiusOnAxis(axisX, axisY, secondCosine, secondSine, halfSide) -
      Math.abs(projected);
    if (overlap <= tolerance) {
      return null;
    }
    if (overlap < penetration) {
      penetration = overlap;
      const sign = projected < 0 ? -1 : 1;
      normalX = axisX * sign;
      normalY = axisY * sign;
    }
  }
  const push = (penetration + tolerance) / 2;
  return {
    firstX: -normalX * push,
    firstY: -normalY * push,
    secondX: normalX * push,
    secondY: normalY * push,
  };
}

function fitLowerLeft(snapshot: GeometrySnapshot): GeometrySnapshot {
  const bounds = packingBounds(snapshot.poses, snapshot.squareSide);
  const side = Math.max(bounds.maxX - bounds.minX, bounds.maxY - bounds.minY);
  return {
    squareSide: snapshot.squareSide,
    container: { originX: 0, originY: 0, side },
    poses: snapshot.poses.map((pose) => ({
      x: pose.x - bounds.minX,
      y: pose.y - bounds.minY,
      angle: pose.angle,
    })),
  };
}

function fitTranslationCount(before: GeometrySnapshot, after: GeometrySnapshot): number {
  return after.poses.reduce((count, pose, index) => {
    const source = poseAt(before.poses, index);
    return count + (pose.x !== source.x || pose.y !== source.y ? 1 : 0);
  }, 0);
}

function isResolved(assessment: PackingAssessment, tolerance: number): boolean {
  return (
    assessment.valid &&
    assessment.maxPairOverlap <= tolerance &&
    assessment.maxWallOverlap <= tolerance
  );
}

function refusedReason(assessment: PackingAssessment): ResolveTerminationReason | null {
  if (assessment.reason === "count") {
    return "refused-count";
  }
  if (assessment.reason === "nonfinite") {
    return "refused-nonfinite";
  }
  if (assessment.reason === "dimensions") {
    return "refused-dimensions";
  }
  if (!withinCoordinateLimit(assessment.snapshot)) {
    // Fitting to the origin cannot restore digits float64 already lost at this magnitude.
    return "refused-magnitude";
  }
  if (assessment.snapshot.squareSide !== PACKING_VALIDITY.squareSide) {
    // Translation cannot change a square's size, so no repair of this input is a packing.
    return "refused-unit-size";
  }
  return null;
}

/**
 * Attempt a deterministic, translation-only overlap repair and lower-left square fit.
 * The bounded operation reports its checked raw and repaired snapshots separately.
 */
export function resolvePacking(
  input: GeometrySnapshot,
  configuration: ResolveConfiguration,
  options: ResolveOptions = {},
): ResolveReceipt {
  validateConfiguration(configuration);
  const raw = assessPackingSnapshot(copySnapshot(input), configuration.expectedCount);
  const work: ResolveWork = {
    iterations: 0,
    pairTests: 0,
    pairTranslations: 0,
    fitTranslations: 0,
  };
  const refused = refusedReason(raw);
  if (refused !== null) {
    return {
      raw,
      repaired: null,
      configuration: { ...configuration },
      work,
      termination: { reason: refused, resolved: false, exhausted: false },
      normalization: "lower-left-square",
    };
  }
  if (options.shouldCancel?.()) {
    return {
      raw,
      repaired: raw,
      configuration: { ...configuration },
      work,
      termination: { reason: "cancelled", resolved: false, exhausted: false },
      normalization: "lower-left-square",
    };
  }
  if (raw.maxPairOverlap <= configuration.tolerance) {
    const fittedRaw = fitLowerLeft(raw.snapshot);
    work.fitTranslations += fitTranslationCount(raw.snapshot, fittedRaw);
    const fittedAssessment = assessPackingSnapshot(fittedRaw, configuration.expectedCount);
    const resolved = isResolved(fittedAssessment, configuration.tolerance);
    return {
      raw,
      repaired: fittedAssessment,
      configuration: { ...configuration },
      work,
      termination: {
        reason: resolved
          ? isResolved(raw, configuration.tolerance)
            ? "already-valid"
            : "resolved"
          : "stalled",
        resolved,
        exhausted: false,
      },
      normalization: "lower-left-square",
    };
  }

  const mutable: GeometrySnapshot = copySnapshot(raw.snapshot);
  const poses = mutable.poses as GeometryPose[];
  let repaired = raw;
  let stalled = false;
  for (let iteration = 0; iteration < configuration.iterationLimit; iteration += 1) {
    if (options.shouldCancel?.()) {
      return {
        raw,
        repaired,
        configuration: { ...configuration },
        work,
        termination: { reason: "cancelled", resolved: false, exhausted: false },
        normalization: "lower-left-square",
      };
    }
    let distanceMoved = 0;
    for (let firstIndex = 0; firstIndex < poses.length; firstIndex += 1) {
      for (let secondIndex = firstIndex + 1; secondIndex < poses.length; secondIndex += 1) {
        work.pairTests += 1;
        const first = poseAt(poses, firstIndex);
        const second = poseAt(poses, secondIndex);
        const translation = pairTranslation(
          first,
          second,
          mutable.squareSide,
          configuration.tolerance,
        );
        if (translation === null) {
          continue;
        }
        first.x += translation.firstX;
        first.y += translation.firstY;
        second.x += translation.secondX;
        second.y += translation.secondY;
        work.pairTranslations += 1;
        distanceMoved +=
          Math.hypot(translation.firstX, translation.firstY) +
          Math.hypot(translation.secondX, translation.secondY);
      }
    }
    work.iterations += 1;
    const fitted = fitLowerLeft(mutable);
    work.fitTranslations += fitTranslationCount(mutable, fitted);
    repaired = assessPackingSnapshot(fitted, configuration.expectedCount);
    if (isResolved(repaired, configuration.tolerance)) {
      return {
        raw,
        repaired,
        configuration: { ...configuration },
        work,
        termination: { reason: "resolved", resolved: true, exhausted: false },
        normalization: "lower-left-square",
      };
    }
    if (repaired.reason === "nonfinite") {
      return {
        raw,
        repaired,
        configuration: { ...configuration },
        work,
        termination: { reason: "refused-nonfinite", resolved: false, exhausted: false },
        normalization: "lower-left-square",
      };
    }
    if (distanceMoved <= Number.EPSILON) {
      stalled = true;
      break;
    }
  }
  return {
    raw,
    repaired,
    configuration: { ...configuration },
    work,
    termination: {
      reason: stalled ? "stalled" : "budget-exhausted",
      resolved: false,
      exhausted: !stalled,
    },
    normalization: "lower-left-square",
  };
}

export const packingResolver = Object.freeze({ resolvePacking });

export type PackingResolverModule = typeof packingResolver;
