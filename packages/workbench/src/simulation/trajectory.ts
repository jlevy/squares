import type { AtlasLaw, AtlasMiss, AtlasSimMode } from "../api/workbench-api.js";
import type { GeometryReceipt, GeometrySnapshot } from "../core/geometry.js";
import { measurePackingGeometry } from "../core/geometry.ts";
import { assessPackingSnapshot } from "../core/runtime-contracts.ts";
import type { CorpusFrame, CorpusPair } from "../data/corpus.js";
import {
  advanceSimulation,
  createSimulationState,
  type SimulationBodyDefinition,
  type SimulationPose,
  type SimulationTarget,
  type SimulationWork,
  setSimulationSquareSize,
  simulationSnapshot,
  translateSimulation,
} from "./kernel.ts";

const DEGREES_TO_RADIANS = Math.PI / 180;

export type PhysicalStyle = "physics" | "bodies";

export interface AnnealConfiguration {
  level: number;
  amplitude: number;
  decayPower: number;
  span: number;
}

export interface TrajectoryPhysicsConfiguration {
  omega: number;
  zeta: number;
  springRamp: number;
  contactDamping: number;
  contactTorque: number;
  lockIn: number;
  open: number;
  openBy: number;
  shutFrom: number;
  tighten: number;
  tightenFrom: number;
  grow: number;
  jiggle: number;
  jiggleTorque: number;
  bodiesJiggle: number;
  bodiesJiggleTorque: number;
  jiggleHz: readonly [number, number];
  drop: number;
  appear: number;
  inflateFrom: number;
  blend: number;
  maxSpeed: number;
  maxSpin: number;
  cell: number;
}

export interface BlindTrajectoryConfiguration {
  inflate: number;
  hold: number;
  close: number;
  overlapTolerance: number;
  gridStep: number;
}

export interface TrajectoryRequest {
  pairIndex: number;
  pair: CorpusPair;
  source: CorpusFrame;
  target: CorpusFrame;
  steps: number;
  style: PhysicalStyle;
  mode: AtlasSimMode;
  effectiveSeed: number;
  pairLaw: AtlasLaw;
  wallLaw: AtlasLaw;
  relatedMask: Uint8Array | null;
  anneal: AnnealConfiguration;
  physics: TrajectoryPhysicsConfiguration;
  blind: BlindTrajectoryConfiguration;
}

export interface TrajectoryFeasibility {
  valid: boolean;
  reason: string | null;
  geometry: GeometryReceipt;
}

export interface TrajectoryReceipt {
  snapshot: GeometrySnapshot;
  feasibility: TrajectoryFeasibility;
  configuration: {
    pairIndex: number;
    style: PhysicalStyle;
    mode: AtlasSimMode;
    guided: boolean;
    effectiveSeed: number;
    anneal: AnnealConfiguration;
  };
  arithmetic: "float64";
  timestep: number;
  work: SimulationWork;
  residual: { maxLinearSpeed: number; maxAngularSpeed: number };
  forcing: { active: boolean; finalScale: number };
  termination: { reason: "step-limit"; converged: false; stationary: false };
}

export interface Trajectory {
  pair: number;
  n: number;
  steps: number;
  style: PhysicalStyle;
  mode: AtlasSimMode;
  bodies: number;
  states: Float64Array;
  sides: Float64Array;
  pens: Float32Array;
  nears: Float32Array;
  maxPenetration: number;
  maxPenetrationLate: number;
  squeeze: number;
  squeezeDone: boolean;
  side0: number;
  miss: AtlasMiss;
  receipt: TrajectoryReceipt;
}

function finite(value: number, label: string): void {
  if (!Number.isFinite(value)) {
    throw new RangeError(`${label} must be finite`);
  }
}

function positive(value: number, label: string): void {
  finite(value, label);
  if (value <= 0) {
    throw new RangeError(`${label} must be positive`);
  }
}

function nonNegative(value: number, label: string): void {
  finite(value, label);
  if (value < 0) {
    throw new RangeError(`${label} must not be negative`);
  }
}

function fraction(value: number, label: string): void {
  finite(value, label);
  if (value < 0 || value > 1) {
    throw new RangeError(`${label} must be between zero and one`);
  }
}

function numberAt(values: ArrayLike<number>, index: number, label: string): number {
  const value = values[index];
  if (value === undefined) {
    throw new RangeError(`${label} has no item at index ${index}`);
  }
  return value;
}

function squareAt(frame: CorpusFrame, index: number, label: string) {
  const square = frame.squares[index];
  if (square === undefined) {
    throw new RangeError(`${label} has no square at index ${index}`);
  }
  return square;
}

function clamp01(value: number): number {
  return value < 0 ? 0 : value > 1 ? 1 : value;
}

function lerp(first: number, second: number, progress: number): number {
  return first + (second - first) * progress;
}

function smoothstep(value: number): number {
  return value <= 0 ? 0 : value >= 1 ? 1 : value * value * (3 - 2 * value);
}

function smootherstep(value: number): number {
  return value <= 0 ? 0 : value >= 1 ? 1 : value * value * value * (value * (value * 6 - 15) + 10);
}

function easeOut(value: number): number {
  return 1 - (1 - value) ** 3;
}

function angleDelta(firstDegrees: number, secondDegrees: number): number {
  let difference = (((secondDegrees - firstDegrees) % 90) + 90) % 90;
  if (difference > 45 + 1e-9) {
    difference -= 90;
  }
  return difference;
}

function memberTurn(blockTurn: number, sourceDegrees: number, targetDegrees: number): number {
  const difference = (((targetDegrees - sourceDegrees - blockTurn) % 90) + 90) % 90;
  const positiveTurn = blockTurn + difference;
  const negativeTurn = blockTurn + difference - 90;
  return Math.abs(positiveTurn) <= Math.abs(negativeTurn) + 1e-9 ? positiveTurn : negativeTurn;
}

function validateFrame(frame: CorpusFrame, count: number, label: string): void {
  positive(frame.side, `${label} side`);
  if (frame.squares.length !== count || frame.ident.length !== count) {
    throw new RangeError(`${label} frame must contain ${count} squares and identities`);
  }
  for (let index = 0; index < count; index++) {
    const square = squareAt(frame, index, label);
    finite(square[0], `${label} square x`);
    finite(square[1], `${label} square y`);
    finite(square[2], `${label} square angle`);
  }
}

function validateConfiguration(request: TrajectoryRequest): void {
  if (!Number.isSafeInteger(request.steps) || request.steps < 1) {
    throw new RangeError("trajectory step budget must be a positive integer");
  }
  const { pair, physics, blind, anneal } = request;
  validateFrame(request.source, pair.n, "source");
  validateFrame(request.target, pair.n + 1, "target");
  if (
    pair.map.length !== pair.n ||
    pair.block_of.length !== pair.n ||
    !Number.isSafeInteger(pair.new) ||
    pair.new < 0 ||
    pair.new > pair.n
  ) {
    throw new RangeError("pair correspondence does not match its declared count");
  }
  for (const mapped of pair.map) {
    if (!Number.isSafeInteger(mapped) || mapped < 0 || mapped > pair.n || mapped === pair.new) {
      throw new RangeError("pair correspondence contains an invalid target index");
    }
  }
  for (const [label, value] of Object.entries({
    omega: physics.omega,
    zeta: physics.zeta,
    springRamp: physics.springRamp,
    contactDamping: physics.contactDamping,
    contactTorque: physics.contactTorque,
    open: physics.open,
    tighten: physics.tighten,
    jiggle: physics.jiggle,
    jiggleTorque: physics.jiggleTorque,
    bodiesJiggle: physics.bodiesJiggle,
    bodiesJiggleTorque: physics.bodiesJiggleTorque,
    maxSpeed: physics.maxSpeed,
    maxSpin: physics.maxSpin,
    cell: physics.cell,
    blindInflate: blind.inflate,
    blindTolerance: blind.overlapTolerance,
    blindGridStep: blind.gridStep,
    annealDecayPower: anneal.decayPower,
    annealSpan: anneal.span,
  })) {
    positive(value, label);
  }
  // Level zero on the annealing dial is amplitude zero: an unforced run, reported as such.
  nonNegative(anneal.amplitude, "annealAmplitude");
  for (const [label, value] of Object.entries({
    lockIn: physics.lockIn,
    openBy: physics.openBy,
    shutFrom: physics.shutFrom,
    tightenFrom: physics.tightenFrom,
    grow: physics.grow,
    appear: physics.appear,
    inflateFrom: physics.inflateFrom,
    blend: physics.blend,
    blindHold: blind.hold,
    blindClose: blind.close,
  })) {
    fraction(value, label);
  }
  if (blind.close <= blind.hold) {
    throw new RangeError("blind close must follow its hold");
  }
  if (request.relatedMask !== null && request.relatedMask.length !== (pair.n + 1) ** 2) {
    throw new RangeError("trajectory relationship mask must be n by n");
  }
}

function emptiestSpot(
  poses: readonly SimulationPose[],
  count: number,
  side: number,
  gridStep: number,
): readonly [number, number] {
  const low = 0.5;
  const high = side - 0.5;
  const cells = Math.max(1, Math.round((high - low) / gridStep));
  let resultX = low;
  let resultY = low;
  let best = -1;
  for (let xIndex = 0; xIndex <= cells; xIndex++) {
    const x = lerp(low, high, xIndex / cells);
    for (let yIndex = 0; yIndex <= cells; yIndex++) {
      const y = lerp(low, high, yIndex / cells);
      let nearest = Infinity;
      for (let index = 0; index < count; index++) {
        const pose = poses[index];
        if (pose === undefined) {
          throw new RangeError("blind source pose is missing");
        }
        nearest = Math.min(nearest, (pose.x - x) ** 2 + (pose.y - y) ** 2);
      }
      if (nearest > best) {
        best = nearest;
        resultX = x;
        resultY = y;
      }
    }
  }
  return [resultX, resultY];
}

interface PreparedTrajectory {
  poses: SimulationPose[];
  targets: SimulationTarget[];
  bodies: SimulationBodyDefinition[];
  side0: number;
  newSquare: number;
}

function prepareTrajectory(request: TrajectoryRequest): PreparedTrajectory {
  const { pair, source, target, physics } = request;
  const count = pair.n + 1;
  const poses: SimulationPose[] = [];
  const targets: SimulationTarget[] = [];
  for (let index = 0; index < pair.n; index++) {
    const from = squareAt(source, index, "source");
    const mapped = pair.map[index];
    if (mapped === undefined) {
      throw new RangeError("pair target index is missing");
    }
    const to = squareAt(target, mapped, "target");
    const blockIndex = pair.block_of[index];
    const block = blockIndex === undefined || blockIndex < 0 ? undefined : pair.blocks[blockIndex];
    const turn =
      request.style === "bodies" && block !== undefined
        ? memberTurn(block.turn, from[2], to[2])
        : angleDelta(from[2], to[2]);
    poses.push({ x: from[0], y: from[1], angle: from[2] * DEGREES_TO_RADIANS, size: 1 });
    targets.push({
      x: to[0],
      y: to[1],
      angle: (from[2] + turn) * DEGREES_TO_RADIANS,
    });
  }
  const arriving = squareAt(target, pair.new, "target");
  poses.push({
    x: arriving[0],
    y: arriving[1] + physics.drop,
    angle: arriving[2] * DEGREES_TO_RADIANS,
    size: physics.inflateFrom,
  });
  targets.push({
    x: arriving[0],
    y: arriving[1],
    angle: arriving[2] * DEGREES_TO_RADIANS,
  });

  const blind = request.mode === "blind";
  const side0 = blind ? target.side * request.blind.inflate : source.side;
  if (blind) {
    const shift = (side0 - source.side) / 2;
    for (let index = 0; index < pair.n; index++) {
      const pose = poses[index];
      if (pose === undefined) {
        throw new RangeError("blind source pose is missing");
      }
      pose.x += shift;
      pose.y += shift;
    }
    const [x, y] = emptiestSpot(poses, pair.n, side0, request.blind.gridStep);
    const newPose = poses[pair.n];
    if (newPose === undefined) {
      throw new RangeError("arriving pose is missing");
    }
    newPose.x = x;
    newPose.y = y;
    newPose.angle = 0;
  }

  const bodies: SimulationBodyDefinition[] = [];
  const assigned = new Uint8Array(count);
  if (request.style === "bodies") {
    for (const block of pair.blocks) {
      if (block.members.length === 0) {
        continue;
      }
      let targetX = 0;
      let targetY = 0;
      for (const index of block.members) {
        const targetPose = targets[index];
        if (targetPose === undefined || index < 0 || index >= pair.n || assigned[index] !== 0) {
          throw new RangeError("rigid block membership is invalid");
        }
        assigned[index] = 1;
        targetX += targetPose.x;
        targetY += targetPose.y;
      }
      bodies.push({
        members: block.members.slice(),
        angle: 0,
        target: {
          x: targetX / block.members.length,
          y: targetY / block.members.length,
          angle: block.turn * DEGREES_TO_RADIANS,
        },
        torqueFactor: 1,
      });
    }
  }
  for (let index = 0; index < count; index++) {
    if (assigned[index] !== 0) {
      continue;
    }
    const pose = poses[index];
    const targetPose = targets[index];
    if (pose === undefined || targetPose === undefined) {
      throw new RangeError("trajectory singleton body is missing");
    }
    bodies.push({
      members: [index],
      angle: 0,
      target: { x: targetPose.x, y: targetPose.y, angle: targetPose.angle - pose.angle },
      torqueFactor: physics.contactTorque,
    });
  }
  return { poses, targets, bodies, side0, newSquare: pair.n };
}

function containerOpen(progress: number, physics: TrajectoryPhysicsConfiguration): number {
  const shutSpan = Math.max(1e-6, 1 - physics.blend - physics.shutFrom);
  const open = smootherstep(clamp01(progress / physics.openBy));
  const shut = smootherstep(clamp01((progress - physics.shutFrom) / shutSpan));
  return physics.open * open * (1 - shut);
}

function containerSide(
  source: number,
  target: number,
  progress: number,
  physics: TrajectoryPhysicsConfiguration,
): number {
  const growth = easeOut(clamp01(progress / physics.grow));
  return lerp(source, target, growth) + containerOpen(progress, physics);
}

function tightenScale(progress: number, physics: TrajectoryPhysicsConfiguration): number {
  const span = Math.max(1e-6, 1 - physics.blend - physics.tightenFrom);
  return 1 + (physics.tighten - 1) * smootherstep(clamp01((progress - physics.tightenFrom) / span));
}

function storeState(
  states: Float64Array,
  storedStep: number,
  squareCount: number,
  snapshot: GeometrySnapshot,
): void {
  let offset = storedStep * squareCount * 3;
  for (const pose of snapshot.poses) {
    states[offset++] = pose.x;
    states[offset++] = pose.y;
    states[offset++] = pose.angle;
  }
}

function finalSnapshot(
  states: Float64Array,
  steps: number,
  squareCount: number,
  side: number,
): GeometrySnapshot {
  const offset = steps * squareCount * 3;
  return {
    squareSide: 1,
    container: { originX: 0, originY: 0, side },
    poses: Array.from({ length: squareCount }, (_, index) => ({
      x: numberAt(states, offset + index * 3, "trajectory state"),
      y: numberAt(states, offset + index * 3 + 1, "trajectory state"),
      angle: numberAt(states, offset + index * 3 + 2, "trajectory state"),
    })),
  };
}

function measureMiss(
  snapshot: GeometrySnapshot,
  targets: readonly SimulationTarget[],
  recordSide: number,
  align: boolean,
): AtlasMiss {
  const geometry = measurePackingGeometry(snapshot);
  const originX = align ? geometry.bounds.minX : 0;
  const originY = align ? geometry.bounds.minY : 0;
  let centre = 0;
  let angle = 0;
  for (let index = 0; index < snapshot.poses.length; index++) {
    const pose = snapshot.poses[index];
    const target = targets[index];
    if (pose === undefined || target === undefined) {
      throw new RangeError("trajectory miss input is incomplete");
    }
    centre = Math.max(centre, Math.hypot(pose.x - originX - target.x, pose.y - originY - target.y));
    angle = Math.max(
      angle,
      Math.abs(angleDelta(target.angle / DEGREES_TO_RADIANS, pose.angle / DEGREES_TO_RADIANS)),
    );
  }
  const side = Math.max(
    geometry.bounds.maxX - geometry.bounds.minX,
    geometry.bounds.maxY - geometry.bounds.minY,
  );
  return { centre, angle, side, record: recordSide, excess: (side / recordSide - 1) * 100 };
}

function addWork(total: SimulationWork, step: SimulationWork): void {
  total.steps += step.steps;
  total.pairCandidates += step.pairCandidates;
  total.pairForces += step.pairForces;
  total.wallForces += step.wallForces;
}

/** Build a deterministic cached Animate trajectory through the shared step kernel. */
export function buildTrajectory(request: TrajectoryRequest): Trajectory {
  validateConfiguration(request);
  const prepared = prepareTrajectory(request);
  const { pair, physics, anneal } = request;
  const squareCount = pair.n + 1;
  const simulation = createSimulationState({
    squares: prepared.poses,
    bodies: prepared.bodies,
    container: { originX: 0, originY: 0, side: prepared.side0 },
    seed: request.effectiveSeed,
    frequencyRange: physics.jiggleHz,
  });
  const states = new Float64Array((request.steps + 1) * squareCount * 3);
  const sides = new Float64Array(request.steps + 1);
  const pens = new Float32Array(request.steps + 1);
  const nears = new Float32Array(request.steps + 1);
  sides[0] = prepared.side0;
  storeState(states, 0, squareCount, simulationSnapshot(simulation));
  const stiffness = physics.omega ** 2;
  const damping = 2 * physics.zeta * physics.omega;
  const timestep = anneal.span / request.steps;
  const rigid = request.style === "bodies";
  const jiggle = (rigid ? physics.bodiesJiggle : physics.jiggle) * anneal.amplitude;
  const jiggleTorque =
    (rigid ? physics.bodiesJiggleTorque : physics.jiggleTorque) * anneal.amplitude;
  const work: SimulationWork = { steps: 0, pairCandidates: 0, pairForces: 0, wallForces: 0 };
  let maximumLinearSpeed = 0;
  let maximumAngularSpeed = 0;
  let maxPenetration = 0;
  let maxPenetrationLate = 0;
  let previousPenetration = 0;
  let squeeze = 0;
  let squeezeDone = false;
  const blind = request.mode === "blind";
  for (let storedStep = 1; storedStep <= request.steps; storedStep++) {
    const progress = (storedStep - 1) / request.steps;
    let side: number;
    if (blind) {
      if (
        progress >= request.blind.hold &&
        previousPenetration <= request.blind.overlapTolerance &&
        squeeze < 1
      ) {
        squeeze = Math.min(
          1,
          squeeze + 1 / request.steps / (request.blind.close - request.blind.hold),
        );
        squeezeDone ||= squeeze >= 1;
      }
      side = lerp(prepared.side0, request.target.side, smoothstep(squeeze));
      const previousSide = numberAt(sides, storedStep - 1, "trajectory side");
      const shift = (side - previousSide) / 2;
      if (shift !== 0) {
        translateSimulation(simulation, shift, shift);
      }
    } else {
      side = containerSide(request.source.side, request.target.side, progress, physics);
    }
    sides[storedStep] = side;
    const decay = (1 - progress) ** anneal.decayPower;
    const tight = blind ? 1 : tightenScale(progress, physics);
    const springStiffness = blind
      ? 0
      : stiffness * smoothstep(progress / physics.springRamp) * tight;
    const springDamping = damping * Math.sqrt(tight);
    const contactScale =
      request.mode === "snap"
        ? 1 - clamp01((progress - physics.lockIn) / (1 - physics.blend - physics.lockIn))
        : 1;
    const newSize = lerp(physics.inflateFrom, 1, clamp01(progress / physics.appear));
    setSimulationSquareSize(simulation, prepared.newSquare, newSize);
    const step = advanceSimulation(simulation, {
      timestep,
      container: { originX: 0, originY: 0, side },
      pairLaw: request.pairLaw,
      wallLaw: request.wallLaw,
      relatedMask: request.relatedMask,
      baseCell: physics.cell,
      contactDamping: physics.contactDamping,
      contactScale,
      spring: { stiffness: springStiffness, damping: springDamping, quarterTurn: false },
      forcing: {
        linear: jiggle * decay,
        angular: jiggleTorque * decay,
        time: progress * anneal.span,
      },
      maxSpeed: physics.maxSpeed,
      maxSpin: physics.maxSpin,
    });
    previousPenetration = step.deepestFullSizePairPenetration;
    pens[storedStep] = previousPenetration;
    nears[storedStep] = step.nearPairs;
    if (contactScale >= 1) {
      maxPenetration = Math.max(maxPenetration, previousPenetration);
    } else {
      maxPenetrationLate = Math.max(maxPenetrationLate, previousPenetration);
    }
    maximumLinearSpeed = step.maxLinearSpeed;
    maximumAngularSpeed = step.maxAngularSpeed;
    addWork(work, step.work);
    storeState(states, storedStep, squareCount, simulationSnapshot(simulation));
  }

  if (request.mode === "snap") {
    const blendStart = 1 - physics.blend;
    for (let storedStep = 0; storedStep <= request.steps; storedStep++) {
      const progress = storedStep / request.steps;
      if (progress <= blendStart) {
        continue;
      }
      const weight =
        storedStep === request.steps ? 1 : smoothstep((progress - blendStart) / physics.blend);
      for (let index = 0; index < squareCount; index++) {
        const offset = (storedStep * squareCount + index) * 3;
        const target = prepared.targets[index];
        if (target === undefined) {
          throw new RangeError("trajectory target is missing during correction");
        }
        states[offset] =
          weight >= 1 ? target.x : lerp(numberAt(states, offset, "state"), target.x, weight);
        states[offset + 1] =
          weight >= 1 ? target.y : lerp(numberAt(states, offset + 1, "state"), target.y, weight);
        states[offset + 2] =
          weight >= 1
            ? target.angle
            : lerp(numberAt(states, offset + 2, "state"), target.angle, weight);
      }
    }
  }

  const snapshot = finalSnapshot(
    states,
    request.steps,
    squareCount,
    numberAt(sides, request.steps, "trajectory side"),
  );
  const assessed = assessPackingSnapshot(snapshot, squareCount);
  const geometry = measurePackingGeometry(snapshot);
  const receipt: TrajectoryReceipt = {
    snapshot,
    feasibility: { valid: assessed.valid, reason: assessed.reason, geometry },
    configuration: {
      pairIndex: request.pairIndex,
      style: request.style,
      mode: request.mode,
      guided: !blind,
      effectiveSeed: request.effectiveSeed,
      anneal: { ...anneal },
    },
    arithmetic: "float64",
    timestep,
    work,
    residual: {
      maxLinearSpeed: maximumLinearSpeed,
      maxAngularSpeed: maximumAngularSpeed,
    },
    forcing: {
      active: anneal.amplitude > 0,
      finalScale: 0,
    },
    termination: { reason: "step-limit", converged: false, stationary: false },
  };
  return {
    pair: request.pairIndex,
    n: pair.n,
    steps: request.steps,
    style: request.style,
    mode: request.mode,
    bodies: simulation.bodyCount,
    states,
    sides,
    pens,
    nears,
    maxPenetration,
    maxPenetrationLate,
    squeeze,
    squeezeDone,
    side0: prepared.side0,
    miss: measureMiss(snapshot, prepared.targets, request.target.side, blind),
    receipt,
  };
}

export function sampleTrajectoryPose(
  trajectory: Trajectory,
  index: number,
  progress: number,
): readonly [number, number, number] {
  if (!Number.isSafeInteger(index) || index < 0 || index > trajectory.n) {
    throw new RangeError("trajectory square index is out of range");
  }
  finite(progress, "trajectory progress");
  const bounded = clamp01(progress);
  const frame = bounded * trajectory.steps;
  const lower = Math.min(Math.floor(frame), trajectory.steps - 1);
  const weight = frame - lower;
  const squareCount = trajectory.n + 1;
  const lowerOffset = (lower * squareCount + index) * 3;
  const upperOffset = ((lower + 1) * squareCount + index) * 3;
  return [
    lerp(
      numberAt(trajectory.states, lowerOffset, "trajectory state"),
      numberAt(trajectory.states, upperOffset, "trajectory state"),
      weight,
    ),
    lerp(
      numberAt(trajectory.states, lowerOffset + 1, "trajectory state"),
      numberAt(trajectory.states, upperOffset + 1, "trajectory state"),
      weight,
    ),
    lerp(
      numberAt(trajectory.states, lowerOffset + 2, "trajectory state"),
      numberAt(trajectory.states, upperOffset + 2, "trajectory state"),
      weight,
    ) / DEGREES_TO_RADIANS,
  ];
}

export function sampleTrajectorySide(trajectory: Trajectory, progress: number): number {
  finite(progress, "trajectory progress");
  const frame = clamp01(progress) * trajectory.steps;
  const lower = Math.floor(frame);
  if (lower >= trajectory.steps) {
    return numberAt(trajectory.sides, trajectory.steps, "trajectory side");
  }
  return lerp(
    numberAt(trajectory.sides, lower, "trajectory side"),
    numberAt(trajectory.sides, lower + 1, "trajectory side"),
    frame - lower,
  );
}

export const trajectorySimulation = Object.freeze({
  buildTrajectory,
  sampleTrajectoryPose,
  sampleTrajectorySide,
});

export type TrajectorySimulationModule = typeof trajectorySimulation;
