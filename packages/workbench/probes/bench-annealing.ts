import type {
  AtlasLaw,
  AtlasSimMode,
  AtlasStyle,
  AtlasTiming,
  AtlasTransitions,
  WorkbenchApiHost,
} from "../src/api/workbench-api.ts";
import { type GeometryPose, packingBounds, pairSeparation } from "../src/core/geometry.ts";
import { assessPackingSnapshot, PACKING_VALIDITY } from "../src/core/runtime-contracts.ts";

/** A lower-left pose as the trial reports it: centre x, centre y, radians. */
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
    /** The pair law the trajectory ran under; trials before and after a law change differ here. */
    pairLaw: AtlasLaw;
    wallLaw: AtlasLaw;
    /** The page's beat, which sets how many physics steps a trajectory takes. */
    timing: AtlasTiming;
    /** The annealed moving span of this trajectory, in seconds. */
    annealSpan: number;
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
const TOLERANCE = PACKING_VALIDITY.penetrationTolerance;
const SQUARE = PACKING_VALIDITY.squareSide;

function browserHost(): WorkbenchApiHost {
  return window as unknown as WorkbenchApiHost;
}

function geometryPoses(poses: readonly Pose[]): GeometryPose[] {
  return poses.map(([x, y, angle]) => ({ x, y, angle }));
}

/** Translate radian poses into the smallest lower-left square container, as the contract fits it. */
function fitted(poses: readonly Pose[]): { poses: Pose[]; side: number } {
  const bounds = packingBounds(geometryPoses(poses), SQUARE);
  return {
    poses: poses.map(([x, y, angle]): Pose => [x - bounds.minX, y - bounds.minY, angle]),
    side: Math.max(bounds.maxX - bounds.minX, bounds.maxY - bounds.minY),
  };
}

/** The contract's assessment of a fitted arrangement: the deepest pair overlap and the verdict. */
function measured(arrangement: { poses: Pose[]; side: number }) {
  return assessPackingSnapshot(
    {
      squareSide: SQUARE,
      container: { originX: 0, originY: 0, side: arrangement.side },
      poses: geometryPoses(arrangement.poses),
    },
    arrangement.poses.length,
  );
}

/**
 * Push overlapping pairs apart along their shallowest face normal until no pair penetrates by more
 * than the contract tolerance, or the sweep limit is spent. Each push clears the pair by one
 * tolerance, so a converged arrangement is left with a small gap rather than at the boundary.
 */
function resolveOverlaps(poses: readonly Pose[]): { poses: Pose[]; sweeps: number } {
  const resolved = poses.map((pose): Pose => [...pose]);
  let unresolved = true;
  let sweeps = 0;
  for (; sweeps < REPAIR_SWEEP_LIMIT && unresolved; sweeps += 1) {
    unresolved = false;
    for (let first = 0; first < resolved.length; first += 1) {
      for (let second = first + 1; second < resolved.length; second += 1) {
        const firstPose = resolved[first];
        const secondPose = resolved[second];
        if (firstPose === undefined || secondPose === undefined) {
          throw new Error("pose inventory changed while resolving overlap");
        }
        const dx = secondPose[0] - firstPose[0];
        const dy = secondPose[1] - firstPose[1];
        if (dx * dx + dy * dy >= 2 * SQUARE * SQUARE) {
          continue;
        }
        const separation = pairSeparation(
          { x: firstPose[0], y: firstPose[1], angle: firstPose[2] },
          { x: secondPose[0], y: secondPose[1], angle: secondPose[2] },
          SQUARE,
        );
        if (separation.penetration > TOLERANCE) {
          unresolved = true;
          const push = separation.penetration / 2 + TOLERANCE;
          firstPose[0] -= separation.normalX * push;
          firstPose[1] -= separation.normalY * push;
          secondPose[0] += separation.normalX * push;
          secondPose[1] += separation.normalY * push;
        }
      }
    }
  }
  return { poses: resolved, sweeps };
}

/**
 * The catalogue API, with Animate owning the page. The page opens on Pack, and until Animate
 * owns it the catalogue API refuses every call but `setMode` and `mode`.
 */
function catalogueApi(host: WorkbenchApiHost): AtlasTransitions | undefined {
  const api = host.atlasTransitions;
  if (api !== undefined && typeof api.setMode === "function" && api.mode() !== "animate") {
    api.setMode("animate");
  }
  return api;
}

function requiredApi(host: WorkbenchApiHost): AtlasTransitions {
  const api = catalogueApi(host);
  if (api === undefined) {
    throw new Error("the page has no workbench API");
  }
  return api;
}

/** Verify that a loaded page exposes a nonempty, seeded workbench API. */
export function guard(host: WorkbenchApiHost = browserHost()): GuardResult {
  const api = catalogueApi(host);
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

/** Run one blind trial and measure and resolve its final overlap under the validity contract. */
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
  const raw = fitted(
    result.final.map(([x, y, degrees]): Pose => [x, y, (degrees * Math.PI) / 180]),
  );
  const rawAssessment = measured(raw);
  const repairStarted = performance.now();
  const resolved = resolveOverlaps(raw.poses);
  const repaired = fitted(resolved.poses);
  const repairedAssessment = measured(repaired);
  const repairMs = performance.now() - repairStarted;
  const state = api.state();
  const law = api.law();
  const wallLaw = api.wallLaw();

  return {
    configuration: {
      style: result.style,
      mode: result.mode,
      seed: api.seed(),
      inflate: state.blindInflate,
      anneal: result.anneal,
      pairLaw: {
        rigidity: law.rigidity,
        repulsion: law.repulsion,
        attraction: law.attraction,
        range: law.range,
      },
      wallLaw: {
        rigidity: wallLaw.rigidity,
        repulsion: wallLaw.repulsion,
        attraction: wallLaw.attraction,
        range: wallLaw.range,
      },
      timing: {
        dwell: state.timing.dwell,
        move: state.timing.move,
        correct: state.timing.correct,
        settle: state.timing.settle,
      },
      annealSpan: result.annealSpan,
    },
    excess: result.miss.excess,
    side: rawAssessment.requiredSide,
    record: result.miss.record,
    centre: result.miss.centre,
    angle: result.miss.angle,
    overlap: rawAssessment.maxPairOverlap,
    poses: raw.poses,
    resolvedPoses: repaired.poses,
    resolvedSide: repairedAssessment.requiredSide,
    resolvedOverlap: repairedAssessment.maxPairOverlap,
    repairSweeps: resolved.sweeps,
    repairSweepLimit: REPAIR_SWEEP_LIMIT,
    repairConverged: repairedAssessment.valid,
    steps: result.steps,
    physicsMs: result.ms,
    repairMs,
    ms: performance.now() - started,
  };
}
