import type { AtlasGrowthRule, AtlasLaw } from "../api/workbench-api.js";
import type { GeometryPose, GeometryReceipt, GeometrySnapshot } from "../core/geometry.js";
import { measurePackingGeometry } from "../core/geometry.ts";
import {
  admitBestPacking,
  assessPackingSnapshot,
  type BestPacking,
  type PackingAssessment,
  packingSnapshot,
  parseUint32Seed,
  seededRandom,
} from "../core/runtime-contracts.ts";
import { forceLawSubsteps } from "./force-law.ts";
import {
  advanceSimulation,
  createSimulationState,
  type SimulationState,
  type SimulationWork,
  setUniformSimulationSquareSize,
  simulationBuffers,
  simulationSnapshot,
  translateSimulation,
} from "./kernel.ts";

const QUARTER_TURN = Math.PI / 2;
// Best admission uses a fixed simulation cadence, independent of browser frame batches.
// Exact all-pairs checks on every physics step would dominate large Pack runs.
const BEST_OBSERVATION_INTERVAL = 10;

export interface PackPhysicsConfiguration {
  stepsPerSecond: number;
  omega: number;
  zeta: number;
  contactDamping: number;
  contactTorque: number;
  jiggle: number;
  jiggleTorque: number;
  jiggleHz: readonly [number, number];
  maxSpeed: number;
  maxSpin: number;
  cell: number;
}

export interface PackAnnealConfiguration {
  amplitude: number;
  decayPower: number;
  tau: number;
  floor: number;
}

export interface PackGrowthConfiguration {
  on: boolean;
  rate: number;
  rule: AtlasGrowthRule;
}

export interface PackContainerConfiguration {
  squeezeRate: number;
  relaxRate: number;
  squeezeTolerance: number;
  jamTolerance: number;
  minimumSide: number;
}

export interface PackStationarityConfiguration {
  linearSpeed: number;
  angularSpeed: number;
  /** Dimensionless annealing multiplier, including its floor. */
  forcingScale: number;
  window: number;
  stop: boolean;
}

export interface PackConfiguration {
  n: number;
  /** Seed requested by the caller, retained for provenance. */
  seed: number;
  /** Exact stream seed after caller-specific mixing. */
  effectiveSeed: number;
  startKind: PackStartKind;
  start: GeometrySnapshot;
  targets: readonly GeometryPose[] | null;
  reference: { pairIndex: number; recordSide: number } | null;
  pairLaw: AtlasLaw;
  wallLaw: AtlasLaw;
  relatedMask: Uint8Array | null;
  physics: PackPhysicsConfiguration;
  anneal: PackAnnealConfiguration;
  growth: PackGrowthConfiguration;
  container: PackContainerConfiguration;
  stationarity: PackStationarityConfiguration;
}

export type PackStartKind = "grid" | "random" | "given" | "record" | "previous";

export type PackTerminationReason = "work-limit" | "cancelled" | "stationary" | "nonfinite";

export interface PackWork extends SimulationWork {
  baseSteps: number;
}

export interface PackFeasibility {
  /** The contract's pair and wall clauses pass, independent of square size. */
  geometryValid: boolean;
  /** Every clause of `PACKING_VALIDITY` passes: unit squares with valid geometry. */
  valid: boolean;
  unitSquares: boolean;
  reason: string | null;
  geometry: GeometryReceipt;
}

export interface PackReceipt {
  snapshot: GeometrySnapshot;
  best: BestPacking | null;
  feasibility: PackFeasibility;
  configuration: {
    n: number;
    seed: number;
    effectiveSeed: number;
    startKind: PackStartKind;
    guided: boolean;
    reference: { pairIndex: number; recordSide: number } | null;
    pairLaw: AtlasLaw;
    wallLaw: AtlasLaw;
    physics: PackPhysicsConfiguration;
    anneal: PackAnnealConfiguration;
    growth: PackGrowthConfiguration;
    container: PackContainerConfiguration;
    stationarity: PackStationarityConfiguration;
  };
  arithmetic: "float64";
  timestep: number;
  work: PackWork;
  residual: { maxLinearSpeed: number; maxAngularSpeed: number };
  forcing: { active: boolean; scale: number };
  termination: {
    reason: PackTerminationReason;
    stationary: boolean;
    converged: boolean;
    stationarySteps: number;
  };
}

/** Mutable continuation state for interactive Pack. Search consumes only its receipts. */
export interface PackRun {
  readonly configuration: PackConfiguration;
  readonly simulation: SimulationState;
  readonly X: Float64Array;
  readonly Y: Float64Array;
  readonly TH: Float64Array;
  readonly VX: Float64Array;
  readonly VY: Float64Array;
  readonly W: Float64Array;
  readonly seed: number;
  readonly effectiveSeed: number;
  readonly n: number;
  readonly kind: PackStartKind;
  readonly pair: number | null;
  readonly springs: boolean;
  readonly record: number | null;
  side: number;
  size: number;
  time: number;
  steps: number;
  sub: number;
  pen: number;
  near: number;
  stalled: boolean;
  grew: number;
  required: number;
  bx0: number;
  bx1: number;
  by0: number;
  by1: number;
  exactPen: number;
  wallPen: number;
  packingValid: boolean;
  invalidReason: string | null;
  bestPacking: BestPacking | null;
  best: number;
  bestAt: number;
  bestPen: number;
  bestWallPen: number;
  held: number;
  heldX: number;
  heldY: number;
  heldTH: number;
  edited: boolean;
  msPerStep: number;
  stationarySteps: number;
  residual: { maxLinearSpeed: number; maxAngularSpeed: number };
  forcingScale: number;
  work: PackWork;
}

export interface PackAdvanceOptions {
  shouldCancel?: () => boolean;
}

export interface PackRunUpdate {
  pairLaw: AtlasLaw;
  wallLaw: AtlasLaw;
  relatedMask: Uint8Array | null;
  physics: Pick<PackPhysicsConfiguration, "jiggle" | "jiggleTorque">;
  anneal: Pick<PackAnnealConfiguration, "amplitude" | "decayPower">;
  growth: PackGrowthConfiguration;
}

function finite(value: number, label: string): void {
  if (!Number.isFinite(value)) {
    throw new RangeError(`${label} must be finite`);
  }
}

function nonnegative(value: number, label: string): void {
  finite(value, label);
  if (value < 0) {
    throw new RangeError(`${label} must be nonnegative`);
  }
}

function positive(value: number, label: string): void {
  finite(value, label);
  if (value <= 0) {
    throw new RangeError(`${label} must be positive`);
  }
}

function integer(value: number, label: string): void {
  if (!Number.isSafeInteger(value) || value < 1) {
    throw new RangeError(`${label} must be a positive integer`);
  }
}

function validateLaw(law: AtlasLaw, label: string): void {
  positive(law.rigidity, `${label} rigidity`);
  nonnegative(law.repulsion, `${label} repulsion`);
  nonnegative(law.attraction, `${label} attraction`);
  nonnegative(law.range, `${label} range`);
}

function validatePose(pose: GeometryPose, label: string): void {
  finite(pose.x, `${label} x`);
  finite(pose.y, `${label} y`);
  finite(pose.angle, `${label} angle`);
}

function cloneConfiguration(configuration: PackConfiguration): PackConfiguration {
  return {
    n: configuration.n,
    seed: configuration.seed,
    effectiveSeed: configuration.effectiveSeed,
    startKind: configuration.startKind,
    start: {
      squareSide: configuration.start.squareSide,
      container: { ...configuration.start.container },
      poses: configuration.start.poses.map((pose) => ({ ...pose })),
    },
    targets: configuration.targets?.map((pose) => ({ ...pose })) ?? null,
    reference: configuration.reference === null ? null : { ...configuration.reference },
    pairLaw: { ...configuration.pairLaw },
    wallLaw: { ...configuration.wallLaw },
    relatedMask: configuration.relatedMask?.slice() ?? null,
    physics: { ...configuration.physics, jiggleHz: [...configuration.physics.jiggleHz] },
    anneal: { ...configuration.anneal },
    growth: { ...configuration.growth },
    container: { ...configuration.container },
    stationarity: { ...configuration.stationarity },
  };
}

function validateConfiguration(configuration: PackConfiguration): void {
  integer(configuration.n, "declared count");
  if (parseUint32Seed(configuration.seed) === null) {
    throw new RangeError("seed must be an unsigned 32-bit integer");
  }
  if (parseUint32Seed(configuration.effectiveSeed) === null) {
    throw new RangeError("effective seed must be an unsigned 32-bit integer");
  }
  if (configuration.start.poses.length !== configuration.n) {
    throw new RangeError("start pose count does not match the declared count");
  }
  if (configuration.targets !== null && configuration.targets.length !== configuration.n) {
    throw new RangeError("target pose count does not match the declared count");
  }
  positive(configuration.start.squareSide, "start square side");
  finite(configuration.start.container.originX, "start container origin x");
  finite(configuration.start.container.originY, "start container origin y");
  positive(configuration.start.container.side, "start container side");
  if (configuration.reference !== null) {
    if (
      !Number.isSafeInteger(configuration.reference.pairIndex) ||
      configuration.reference.pairIndex < 0
    ) {
      throw new RangeError("reference pair index must be a nonnegative integer");
    }
    positive(configuration.reference.recordSide, "record side");
  }
  for (const [index, pose] of configuration.start.poses.entries()) {
    validatePose(pose, `start pose ${index}`);
  }
  configuration.targets?.forEach((pose, index) => {
    validatePose(pose, `target pose ${index}`);
  });
  if (
    configuration.relatedMask !== null &&
    configuration.relatedMask.length !== configuration.n ** 2
  ) {
    throw new RangeError("Pack relationship mask must be n by n");
  }
  validateLaw(configuration.pairLaw, "pair law");
  validateLaw(configuration.wallLaw, "wall law");
  const { physics, anneal, growth, container, stationarity } = configuration;
  positive(physics.stepsPerSecond, "steps per second");
  positive(physics.omega, "omega");
  positive(physics.zeta, "zeta");
  nonnegative(physics.contactDamping, "contact damping");
  nonnegative(physics.contactTorque, "contact torque");
  nonnegative(physics.jiggle, "linear jiggle");
  nonnegative(physics.jiggleTorque, "angular jiggle");
  positive(physics.jiggleHz[0], "minimum jiggle frequency");
  positive(physics.jiggleHz[1], "maximum jiggle frequency");
  if (physics.jiggleHz[1] < physics.jiggleHz[0]) {
    throw new RangeError("jiggle frequency range is reversed");
  }
  positive(physics.maxSpeed, "maximum speed");
  positive(physics.maxSpin, "maximum spin");
  positive(physics.cell, "broad phase cell");
  nonnegative(anneal.amplitude, "annealing amplitude");
  positive(anneal.decayPower, "annealing decay power");
  positive(anneal.tau, "annealing time constant");
  if (anneal.floor < 0 || anneal.floor > 1) {
    throw new RangeError("annealing floor must be between zero and one");
  }
  nonnegative(growth.rate, "growth rate");
  if (growth.rule !== "constant" && growth.rule !== "clean") {
    throw new RangeError("unknown growth rule");
  }
  nonnegative(container.squeezeRate, "container squeeze rate");
  nonnegative(container.relaxRate, "container relax rate");
  nonnegative(container.squeezeTolerance, "container squeeze tolerance");
  nonnegative(container.jamTolerance, "container jam tolerance");
  positive(container.minimumSide, "minimum container side");
  nonnegative(stationarity.linearSpeed, "stationary linear speed");
  nonnegative(stationarity.angularSpeed, "stationary angular speed");
  nonnegative(stationarity.forcingScale, "stationary forcing scale");
  integer(stationarity.window, "stationarity window");
}

export function createGridPackStart(n: number, squareSide = 1): GeometrySnapshot {
  integer(n, "grid count");
  positive(squareSide, "grid square side");
  const columns = Math.ceil(Math.sqrt(n));
  const rows = Math.ceil(n / columns);
  return {
    squareSide,
    container: { originX: 0, originY: 0, side: Math.max(columns, rows) * squareSide },
    poses: Array.from({ length: n }, (_, index) => ({
      x: ((index % columns) + 0.5) * squareSide,
      y: (Math.floor(index / columns) + 0.5) * squareSide,
      angle: 0,
    })),
  };
}

export function createRandomPackStart(
  n: number,
  containerSide: number,
  effectiveSeed: number,
  squareSide = 1,
): GeometrySnapshot {
  integer(n, "random count");
  positive(containerSide, "random container side");
  positive(squareSide, "random square side");
  const seed = parseUint32Seed(effectiveSeed);
  if (seed === null) {
    throw new RangeError("random seed must be an unsigned 32-bit integer");
  }
  const random = seededRandom(seed);
  const low = Math.SQRT1_2 * squareSide;
  const high = Math.max(low, containerSide - low);
  return {
    squareSide,
    container: { originX: 0, originY: 0, side: containerSide },
    poses: Array.from({ length: n }, () => ({
      x: low + (high - low) * random(),
      y: low + (high - low) * random(),
      angle: random() * QUARTER_TURN,
    })),
  };
}

/** Recheck the run's exact current buffers and refresh its derived fields. */
export function measurePackRun(run: PackRun, admitBest = true): PackingAssessment {
  const snapshot = packingSnapshot(run.X, run.Y, run.TH, run.size, {
    originX: run.configuration.start.container.originX,
    originY: run.configuration.start.container.originY,
    side: run.side,
  });
  const assessment = assessPackingSnapshot(snapshot, run.n);
  run.required = assessment.requiredSide;
  run.bx0 = assessment.bounds.minX;
  run.bx1 = assessment.bounds.maxX;
  run.by0 = assessment.bounds.minY;
  run.by1 = assessment.bounds.maxY;
  run.exactPen = assessment.maxPairOverlap;
  run.wallPen = assessment.maxWallOverlap;
  run.packingValid = assessment.valid;
  run.invalidReason = assessment.reason;
  if (admitBest) {
    const admitted = admitBestPacking(run.bestPacking, assessment, run.time);
    if (admitted !== run.bestPacking) {
      run.bestPacking = admitted;
      if (admitted !== null) {
        run.best = admitted.requiredSide;
        run.bestAt = admitted.at;
        run.bestPen = admitted.maxPairOverlap;
        run.bestWallPen = admitted.maxWallOverlap;
      }
    }
  }
  return assessment;
}

export function createPackRun(input: PackConfiguration): PackRun {
  validateConfiguration(input);
  const configuration = cloneConfiguration(input);
  const bodies = configuration.start.poses.map((pose, index) => ({
    members: [index],
    angle: pose.angle,
    target: { ...(configuration.targets?.[index] ?? pose) },
    torqueFactor: configuration.physics.contactTorque,
  }));
  const simulation = createSimulationState({
    squares: configuration.start.poses.map((pose) => ({
      ...pose,
      size: configuration.start.squareSide,
    })),
    bodies,
    container: { ...configuration.start.container },
    seed: configuration.effectiveSeed,
    frequencyRange: configuration.physics.jiggleHz,
  });
  const buffers = simulationBuffers(simulation);
  const run: PackRun = {
    configuration,
    simulation,
    X: buffers.x,
    Y: buffers.y,
    TH: buffers.angle,
    VX: buffers.velocityX,
    VY: buffers.velocityY,
    W: buffers.angularVelocity,
    seed: configuration.seed,
    effectiveSeed: configuration.effectiveSeed,
    n: configuration.n,
    kind: configuration.startKind,
    pair: configuration.reference?.pairIndex ?? null,
    springs: configuration.targets !== null,
    record: configuration.reference?.recordSide ?? null,
    side: configuration.start.container.side,
    size: configuration.start.squareSide,
    time: 0,
    steps: 0,
    sub: 1,
    pen: Infinity,
    near: 0,
    stalled: false,
    grew: 0,
    required: Infinity,
    bx0: Infinity,
    bx1: -Infinity,
    by0: Infinity,
    by1: -Infinity,
    exactPen: Infinity,
    wallPen: Infinity,
    packingValid: false,
    invalidReason: "not-measured",
    bestPacking: null,
    best: Infinity,
    bestAt: 0,
    bestPen: 0,
    bestWallPen: 0,
    held: -1,
    heldX: 0,
    heldY: 0,
    heldTH: 0,
    edited: false,
    msPerStep: 0.02,
    stationarySteps: 0,
    residual: { maxLinearSpeed: 0, maxAngularSpeed: 0 },
    forcingScale: 1,
    work: { baseSteps: 0, steps: 0, pairCandidates: 0, pairForces: 0, wallForces: 0 },
  };
  measurePackRun(run);
  return run;
}

/** Apply live control values after validating the complete effective configuration. */
export function updatePackRun(run: PackRun, update: PackRunUpdate): void {
  const candidate = cloneConfiguration(run.configuration);
  candidate.pairLaw = { ...update.pairLaw };
  candidate.wallLaw = { ...update.wallLaw };
  candidate.relatedMask = update.relatedMask?.slice() ?? null;
  candidate.physics.jiggle = update.physics.jiggle;
  candidate.physics.jiggleTorque = update.physics.jiggleTorque;
  candidate.anneal.amplitude = update.anneal.amplitude;
  candidate.anneal.decayPower = update.anneal.decayPower;
  candidate.growth = { ...update.growth };
  validateConfiguration(candidate);
  run.configuration.pairLaw = candidate.pairLaw;
  run.configuration.wallLaw = candidate.wallLaw;
  run.configuration.relatedMask = candidate.relatedMask;
  run.configuration.physics.jiggle = candidate.physics.jiggle;
  run.configuration.physics.jiggleTorque = candidate.physics.jiggleTorque;
  run.configuration.anneal.amplitude = candidate.anneal.amplitude;
  run.configuration.anneal.decayPower = candidate.anneal.decayPower;
  run.configuration.growth = candidate.growth;
}

/** Replace the uniform square side without discarding the current poses or velocities. */
export function setPackSquareSide(run: PackRun, squareSide: number): PackingAssessment {
  positive(squareSide, "Pack square side");
  run.size = squareSide;
  setUniformSimulationSquareSize(run.simulation, squareSide);
  return measurePackRun(run);
}

function addWork(total: PackWork, step: SimulationWork): void {
  total.steps += step.steps;
  total.pairCandidates += step.pairCandidates;
  total.pairForces += step.pairForces;
  total.wallForces += step.wallForces;
}

function finiteSnapshot(snapshot: GeometrySnapshot): boolean {
  return (
    Number.isFinite(snapshot.squareSide) &&
    Number.isFinite(snapshot.container.side) &&
    Number.isFinite(snapshot.container.originX) &&
    Number.isFinite(snapshot.container.originY) &&
    snapshot.poses.every(
      (pose) => Number.isFinite(pose.x) && Number.isFinite(pose.y) && Number.isFinite(pose.angle),
    )
  );
}

function receipt(run: PackRun, reason: PackTerminationReason): PackReceipt {
  // A caller may request a receipt after any step. It cannot change which sampled
  // states compete for best; otherwise browser frame size changes Search results.
  const assessment = measurePackRun(run, false);
  const snapshot = assessment.snapshot;
  const unitSquares = snapshot.squareSide === 1;
  const geometry = finiteSnapshot(snapshot)
    ? measurePackingGeometry(snapshot)
    : {
        bounds: { minX: Infinity, maxX: -Infinity, minY: Infinity, maxY: -Infinity },
        requiredSide: Infinity,
        totalOverlap: Infinity,
        deepestOverlap: Infinity,
        overlapPairs: 0,
        wallOverlapTotal: Infinity,
        maxPairOverlap: Infinity,
        maxWallOverlap: Infinity,
        contacts: [],
        contactEdges: [],
      };
  const stationary = reason === "stationary";
  return {
    snapshot,
    best: run.bestPacking,
    feasibility: {
      geometryValid: assessment.geometryValid,
      valid: assessment.valid,
      unitSquares,
      reason: assessment.reason,
      geometry,
    },
    configuration: {
      n: run.configuration.n,
      seed: run.configuration.seed,
      effectiveSeed: run.configuration.effectiveSeed,
      startKind: run.configuration.startKind,
      guided: run.springs,
      reference: run.configuration.reference === null ? null : { ...run.configuration.reference },
      pairLaw: { ...run.configuration.pairLaw },
      wallLaw: { ...run.configuration.wallLaw },
      physics: {
        ...run.configuration.physics,
        jiggleHz: [...run.configuration.physics.jiggleHz],
      },
      anneal: { ...run.configuration.anneal },
      growth: { ...run.configuration.growth },
      container: { ...run.configuration.container },
      stationarity: { ...run.configuration.stationarity },
    },
    arithmetic: "float64",
    timestep: 1 / run.configuration.physics.stepsPerSecond,
    work: { ...run.work },
    residual: { ...run.residual },
    forcing: {
      active:
        run.forcingScale > 0 &&
        (run.configuration.physics.jiggle > 0 || run.configuration.physics.jiggleTorque > 0),
      scale: run.forcingScale,
    },
    termination: {
      reason,
      stationary,
      converged: stationary,
      stationarySteps: run.stationarySteps,
    },
  };
}

/** Advance an existing Pack run by an exact number of base steps. */
export function advancePackRun(
  run: PackRun,
  baseStepBudget: number,
  options: PackAdvanceOptions = {},
): PackReceipt {
  integer(baseStepBudget, "Pack work budget");
  const { configuration } = run;
  const { physics, anneal, growth, container, stationarity } = configuration;
  const baseTimestep = 1 / physics.stepsPerSecond;
  const substeps = forceLawSubsteps(configuration.pairLaw, baseTimestep);
  run.sub = substeps;
  const timestep = baseTimestep / substeps;
  const stiffness = run.springs ? physics.omega ** 2 : 0;
  const damping = 2 * physics.zeta * physics.omega;
  let reason: PackTerminationReason = "work-limit";
  for (let baseStep = 0; baseStep < baseStepBudget; baseStep++) {
    if (options.shouldCancel?.()) {
      reason = "cancelled";
      break;
    }
    let containerChanged = false;
    let squareSizeChanged = false;
    for (let substep = 0; substep < substeps; substep++) {
      const decay =
        anneal.floor + (1 - anneal.floor) * (1 / (1 + run.time / anneal.tau)) ** anneal.decayPower;
      run.forcingScale =
        physics.jiggle > 0 || physics.jiggleTorque > 0 ? anneal.amplitude * decay : 0;
      const step = advanceSimulation(run.simulation, {
        timestep,
        container: {
          originX: configuration.start.container.originX,
          originY: configuration.start.container.originY,
          side: run.side,
        },
        pairLaw: configuration.pairLaw,
        wallLaw: configuration.wallLaw,
        relatedMask: configuration.relatedMask,
        baseCell: physics.cell,
        contactDamping: physics.contactDamping,
        contactScale: 1,
        spring: { stiffness, damping, quarterTurn: true },
        forcing: {
          linear: physics.jiggle * run.forcingScale,
          angular: physics.jiggleTorque * run.forcingScale,
          time: run.time,
        },
        maxSpeed: physics.maxSpeed,
        maxSpin: physics.maxSpin,
        ...(run.held < 0
          ? {}
          : {
              pinned: {
                body: run.held,
                x: run.heldX,
                y: run.heldY,
                angle: run.heldTH,
              },
            }),
      });
      run.pen = step.deepestPairPenetration;
      run.near = step.nearPairs;
      run.residual = {
        maxLinearSpeed: step.maxLinearSpeed,
        maxAngularSpeed: step.maxAngularSpeed,
      };
      addWork(run.work, step.work);

      if (!run.springs && !(growth.on && run.size < 1)) {
        let nextSide = run.side;
        if (run.pen <= container.squeezeTolerance) {
          nextSide = Math.max(
            container.minimumSide,
            run.side * (1 - container.squeezeRate * timestep),
          );
        } else if (run.pen > container.jamTolerance) {
          nextSide = run.side * (1 + container.relaxRate * timestep);
        }
        if (nextSide !== run.side) {
          containerChanged = true;
          const shift = (nextSide - run.side) / 2;
          translateSimulation(run.simulation, shift, shift);
          if (run.held >= 0) {
            run.heldX += shift;
            run.heldY += shift;
          }
          run.side = nextSide;
        }
      }
      if (growth.on && run.size < 1) {
        const mayGrow = growth.rule === "clean" ? run.pen <= container.squeezeTolerance : true;
        run.stalled = !mayGrow;
        if (mayGrow) {
          const previousSize = run.size;
          run.size = Math.min(1, run.size + growth.rate * timestep);
          squareSizeChanged ||= run.size !== previousSize;
          run.grew += run.size - previousSize;
          setUniformSimulationSquareSize(run.simulation, run.size);
        }
      } else {
        run.stalled = false;
      }
      run.time += timestep;
      run.steps += 1 / substeps;
    }
    run.work.baseSteps++;
    const snapshot = simulationSnapshot(run.simulation);
    if (!finiteSnapshot(snapshot)) {
      reason = "nonfinite";
      break;
    }
    if (run.work.baseSteps % BEST_OBSERVATION_INTERVAL === 0) {
      measurePackRun(run);
    }
    const withinStationarity =
      run.residual.maxLinearSpeed <= stationarity.linearSpeed &&
      run.residual.maxAngularSpeed <= stationarity.angularSpeed &&
      run.forcingScale <= stationarity.forcingScale &&
      !containerChanged &&
      !squareSizeChanged &&
      run.held < 0;
    run.stationarySteps = withinStationarity ? run.stationarySteps + 1 : 0;
    if (stationarity.stop && run.stationarySteps >= stationarity.window) {
      reason = "stationary";
      break;
    }
  }
  return receipt(run, reason);
}

export function runPack(
  configuration: PackConfiguration,
  baseStepBudget: number,
  options: PackAdvanceOptions = {},
): PackReceipt {
  return advancePackRun(createPackRun(configuration), baseStepBudget, options);
}

export const packSimulation = Object.freeze({
  createGridPackStart,
  createRandomPackStart,
  createPackRun,
  updatePackRun,
  setPackSquareSide,
  measurePackRun,
  advancePackRun,
  runPack,
});

export type PackSimulationModule = typeof packSimulation;
