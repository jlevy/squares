import type {
  AtlasSimMode,
  AtlasStyle,
  AtlasTransitions,
  WorkbenchApiHost,
} from "../src/api/workbench-api.ts";

type Axis = readonly [number, number];
type Point = readonly [number, number];
type Pose = [number, number, number];

export interface TrialOptions {
  n: number;
  seed: number;
  style: AtlasStyle;
  inflate: number | null;
  anneal: number | null;
}

export interface TrialResult {
  configuration: {
    style: AtlasStyle;
    mode: AtlasSimMode;
    seed: number;
    inflate: number;
    anneal: number;
  };
  excess: number;
  side: number;
  record: number;
  centre: number;
  angle: number;
  overlap: number;
  poses: Pose[];
  resolvedPoses: Pose[];
  resolvedSide: number;
  resolvedOverlap: number;
  repairSweeps: number;
  repairSweepLimit: number;
  repairConverged: boolean;
  steps: number;
  physicsMs: number;
  repairMs: number;
  ms: number;
}

export type TrialResponse = TrialResult | { error: string };

export type GuardResult = { ok: false; why: string } | { ok: true; pairs: number; seed: number };

const REPAIR_SWEEP_LIMIT = 400;

function browserHost(): WorkbenchApiHost {
  return window as unknown as WorkbenchApiHost;
}

function axesOf(angle: number): readonly [Axis, Axis] {
  const radians = (angle * Math.PI) / 180;
  return [
    [Math.cos(radians), Math.sin(radians)],
    [-Math.sin(radians), Math.cos(radians)],
  ];
}

function cornersOf(pose: Pose): Point[] {
  const radians = (pose[2] * Math.PI) / 180;
  const cosine = Math.cos(radians) / 2;
  const sine = Math.sin(radians) / 2;
  return [
    [pose[0] + cosine - sine, pose[1] + sine + cosine],
    [pose[0] - cosine - sine, pose[1] - sine + cosine],
    [pose[0] - cosine + sine, pose[1] - sine - cosine],
    [pose[0] + cosine + sine, pose[1] + sine - cosine],
  ];
}

function spanOn(points: readonly Point[], axis: Axis): Axis {
  let low = Number.POSITIVE_INFINITY;
  let high = Number.NEGATIVE_INFINITY;
  for (const point of points) {
    const value = point[0] * axis[0] + point[1] * axis[1];
    low = Math.min(low, value);
    high = Math.max(high, value);
  }
  return [low, high];
}

function pairDepth(
  first: Pose,
  second: Pose,
  firstCorners: Point[],
  secondCorners: Point[],
): number {
  let depth = Number.POSITIVE_INFINITY;
  for (const axis of [...axesOf(first[2]), ...axesOf(second[2])]) {
    const [firstLow, firstHigh] = spanOn(firstCorners, axis);
    const [secondLow, secondHigh] = spanOn(secondCorners, axis);
    const overlap = Math.min(firstHigh, secondHigh) - Math.max(firstLow, secondLow);
    if (overlap <= 0) {
      return 0;
    }
    depth = Math.min(depth, overlap);
  }
  return depth;
}

function deepestOverlap(poses: Pose[]): number {
  const corners = poses.map(cornersOf);
  let deepest = 0;
  for (let first = 0; first < poses.length; first += 1) {
    for (let second = first + 1; second < poses.length; second += 1) {
      const firstPose = poses[first];
      const secondPose = poses[second];
      const firstCorners = corners[first];
      const secondCorners = corners[second];
      if (
        firstPose === undefined ||
        secondPose === undefined ||
        firstCorners === undefined ||
        secondCorners === undefined
      ) {
        throw new Error("pose inventory changed while measuring overlap");
      }
      if (Math.hypot(firstPose[0] - secondPose[0], firstPose[1] - secondPose[1]) > 1.4143) {
        continue;
      }
      deepest = Math.max(deepest, pairDepth(firstPose, secondPose, firstCorners, secondCorners));
    }
  }
  return deepest;
}

function resolveOverlaps(poses: Pose[]): { poses: Pose[]; sweeps: number } {
  const resolved = poses.map((pose): Pose => [...pose]);
  let unresolved = true;
  let sweeps = 0;
  for (; sweeps < REPAIR_SWEEP_LIMIT && unresolved; sweeps += 1) {
    unresolved = false;
    const corners = resolved.map(cornersOf);
    for (let first = 0; first < resolved.length; first += 1) {
      for (let second = first + 1; second < resolved.length; second += 1) {
        const firstPose = resolved[first];
        const secondPose = resolved[second];
        if (firstPose === undefined || secondPose === undefined) {
          throw new Error("pose inventory changed while resolving overlap");
        }
        if (Math.hypot(firstPose[0] - secondPose[0], firstPose[1] - secondPose[1]) > 1.4143) {
          continue;
        }
        let depth = Number.POSITIVE_INFINITY;
        let best: Axis | null = null;
        let sign = 1;
        for (const axis of [...axesOf(firstPose[2]), ...axesOf(secondPose[2])]) {
          const firstCorners = corners[first];
          const secondCorners = corners[second];
          if (firstCorners === undefined || secondCorners === undefined) {
            throw new Error("corner inventory changed while resolving overlap");
          }
          const [firstLow, firstHigh] = spanOn(firstCorners, axis);
          const [secondLow, secondHigh] = spanOn(secondCorners, axis);
          const overlap = Math.min(firstHigh, secondHigh) - Math.max(firstLow, secondLow);
          if (overlap <= 0) {
            depth = 0;
            break;
          }
          if (overlap < depth) {
            depth = overlap;
            best = axis;
            sign = firstHigh - secondHigh > 0 ? 1 : -1;
          }
        }
        if (depth > 1e-9 && best !== null) {
          unresolved = true;
          const push = (depth / 2 + 1e-9) * sign;
          firstPose[0] += best[0] * push;
          firstPose[1] += best[1] * push;
          secondPose[0] -= best[0] * push;
          secondPose[1] -= best[1] * push;
          corners[first] = cornersOf(firstPose);
          corners[second] = cornersOf(secondPose);
        }
      }
    }
  }
  return { poses: resolved, sweeps };
}

function fittedPoses(poses: Pose[]): { poses: Pose[]; side: number } {
  let lowX = Number.POSITIVE_INFINITY;
  let highX = Number.NEGATIVE_INFINITY;
  let lowY = Number.POSITIVE_INFINITY;
  let highY = Number.NEGATIVE_INFINITY;
  for (const pose of poses) {
    for (const corner of cornersOf(pose)) {
      lowX = Math.min(lowX, corner[0]);
      highX = Math.max(highX, corner[0]);
      lowY = Math.min(lowY, corner[1]);
      highY = Math.max(highY, corner[1]);
    }
  }
  return {
    poses: poses.map((pose): Pose => [pose[0] - lowX, pose[1] - lowY, (pose[2] * Math.PI) / 180]),
    side: Math.max(highX - lowX, highY - lowY),
  };
}

function requiredApi(host: WorkbenchApiHost): AtlasTransitions {
  const api = host.atlasTransitions;
  if (api === undefined) {
    throw new Error("the page has no workbench API");
  }
  return api;
}

/** Verify that a loaded page exposes a nonempty, seeded workbench API. */
export function guard(host: WorkbenchApiHost = browserHost()): GuardResult {
  const api = host.atlasTransitions;
  if (api === undefined || typeof api.physics !== "function") {
    return { ok: false, why: "no page API" };
  }
  if (typeof api.setSeed !== "function") {
    return { ok: false, why: "the page has no seed" };
  }
  const pairs = api.pairs();
  if (pairs.length === 0) {
    return { ok: false, why: "the page carries no pairs" };
  }
  return { ok: true, pairs: pairs.length, seed: api.seed() };
}

/** Run one blind trial and independently measure and resolve its final overlap. */
export function runTrial(
  options: TrialOptions,
  host: WorkbenchApiHost = browserHost(),
): TrialResponse {
  const api = requiredApi(host);
  api.setSeed(options.seed);
  if (options.inflate !== null) {
    api.setBlindInflate(options.inflate);
  }
  if (options.anneal !== null) {
    api.setAnneal(options.anneal);
  }
  const index = api.pairs().findIndex((pair) => pair.n + 1 === options.n);
  if (index < 0) {
    return { error: `the page carries no pair into n = ${options.n}` };
  }

  const started = performance.now();
  const result = api.physics(index, options.style, "blind");
  const poses = result.final.map((pose): Pose => [...pose]);
  const overlap = deepestOverlap(poses);
  const raw = fittedPoses(poses);
  const repairStarted = performance.now();
  const resolved = resolveOverlaps(poses);
  const fitted = fittedPoses(resolved.poses);
  const resolvedOverlap = deepestOverlap(resolved.poses);
  const repairMs = performance.now() - repairStarted;

  return {
    configuration: {
      style: result.style,
      mode: result.mode,
      seed: api.seed(),
      inflate: api.state().blindInflate,
      anneal: result.anneal,
    },
    excess: result.miss.excess,
    side: raw.side,
    record: result.miss.record,
    centre: result.miss.centre,
    angle: result.miss.angle,
    overlap,
    poses: raw.poses,
    resolvedPoses: fitted.poses,
    resolvedSide: fitted.side,
    resolvedOverlap,
    repairSweeps: resolved.sweeps,
    repairSweepLimit: REPAIR_SWEEP_LIMIT,
    repairConverged: resolvedOverlap <= 1e-9,
    steps: result.steps,
    physicsMs: result.ms,
    repairMs,
    ms: performance.now() - started,
  };
}
