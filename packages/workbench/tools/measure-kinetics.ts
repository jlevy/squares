import { resolve } from "node:path";
import { performance } from "node:perf_hooks";
import { illustrationFrame, type MotionTrack } from "../src/animation/illustration.ts";
import { pairSchedule, type TimelineConfiguration } from "../src/animation/timeline.ts";
import type { AtlasLaw, AtlasPhase, AtlasSimMode, AtlasTiming } from "../src/api/workbench-api.ts";
import { mixUint32Seed } from "../src/core/runtime-contracts.ts";
import { type Corpus, type CorpusPair, decodeCorpus, frameAt, pairAt } from "../src/data/corpus.ts";
import {
  ANNEAL_SETTINGS,
  ARRIVAL_DELAY_BOUNDS,
  annealConfiguration,
  BLIND_TRAJECTORY_SETTINGS,
  DEFAULT_ANIMATE_STYLE,
  DEFAULT_ARRIVAL_DELAY_FRACTION,
  DEFAULT_MOTION_RESPONSE,
  DEFAULT_STEP_TIMING,
  DEFAULT_WALL_LAW,
  LAW_PARAMETER_DEFINITIONS,
  MOTION_RESPONSE_BOUNDS,
  type MotionLaw,
  type MotionLawKey,
  type MotionStyle,
  NEW_FRACTION,
  PAIR_LAW_BOUNDS,
  PAIR_LAW_PRESETS,
  PHYSICS_SETTINGS,
  type PhysicalPresentationSchedule,
  pairLawPreset,
  physicalPresentationNeedsTrajectory,
  physicalPresentationState,
  ROLL_MAX,
  STEPS_PER_SECOND,
  TRAJECTORY_PHYSICS_SETTINGS,
  trajectoryPhysicsConfiguration,
  WALL_LAW_BOUNDS,
} from "../src/motion-settings.ts";
import { MAX_FORCE_LAW_SUBSTEPS } from "../src/simulation/force-law.ts";
import {
  buildTrajectory,
  sampleTrajectoryPose,
  sampleTrajectorySide,
  type Trajectory,
  type TrajectoryPhysicsConfiguration,
} from "../src/simulation/trajectory.ts";
import { readCorpus } from "./check-candidate-corpus.ts";
import {
  analyzeMotionTrace,
  identicalMotionFrames,
  type MotionFrame,
  type MotionPose,
  stableNumber,
} from "./kinetics-metrics.ts";

export const KINETICS_SCHEMA = "squares.workbench.kinetics/v1";
/** Hard ceiling for one physical solver cache, including its initial state. */
export const MAX_KINETICS_STORED_FRAMES = 10_000;
/** Hard ceiling for one uniformly sampled wall-time presentation trace. */
export const MAX_KINETICS_PRESENTATION_FRAMES = 10_000;
/** Maximum retained pose objects across the presented, stored, and raw stored traces. */
export const MAX_KINETICS_POSE_SAMPLES = 250_000;

interface KineticsOptions {
  corpusPath: string;
  solver: MotionStyle;
  mode: AtlasSimMode;
  phase: AtlasPhase;
  lawName: string;
  wallLawName: string;
  pairLawOverrides: Partial<MotionLaw>;
  wallLawOverrides: Partial<MotionLaw>;
  annealLevel: number;
  timing: string;
  instance: number;
  seed: number;
  stepsPerSecond: number;
  sampleRate: number;
  arrivalDelay: number;
  integrationSubsteps: "adaptive" | number;
  motionResponse: { speedLimit: number; contactDamping: number };
  jiggleHz: readonly [number, number];
  includeFrames: boolean;
}

const PHYSICAL_OVERRIDE_FLAGS = {
  "contact-damping": "contactDamping",
  "speed-limit": "speedLimit",
  "max-speed": "speedLimit",
} as const;

const PHASES: readonly AtlasPhase[] = [
  "add-then-move",
  "move-then-add",
  "simultaneous",
  "rotate-first",
  "slide-first",
];

const MODES: readonly AtlasSimMode[] = ["snap", "free", "blind"];

function numberArgument(value: string | undefined, label: string): number {
  const parsed = Number(value);
  if (!Number.isFinite(parsed)) {
    throw new RangeError(`${label} must be a finite number`);
  }
  return parsed;
}

function integerArgument(value: string | undefined, label: string, minimum: number): number {
  const parsed = numberArgument(value, label);
  if (!Number.isSafeInteger(parsed) || parsed < minimum) {
    throw new RangeError(`${label} must be an integer >= ${minimum}`);
  }
  return parsed;
}

function frameSteps(
  rate: number,
  duration: number,
  maximumFrames: number,
  label: "stored" | "presentation",
): number {
  if (!Number.isFinite(duration) || duration <= 0) {
    throw new RangeError(`${label} frame duration must be finite and positive`);
  }
  const unroundedSteps = rate * duration;
  if (!Number.isFinite(unroundedSteps) || !Number.isSafeInteger(Math.round(unroundedSteps))) {
    throw new RangeError(`${label} frame count is not a safe finite integer`);
  }
  const steps = Math.max(1, Math.round(unroundedSteps));
  const frames = steps + 1;
  if (frames > maximumFrames) {
    throw new RangeError(
      `${label} frame budget exceeded: ${frames} requested, maximum ${maximumFrames}`,
    );
  }
  return steps;
}

/** Refuse a trace set too large for ordinary Node heaps before any frame arrays are built. */
export function assertKineticsPoseSampleBudget(
  squareCount: number,
  presentationFrames: number,
  storedFrames: number | null,
): void {
  if (!Number.isSafeInteger(squareCount) || squareCount < 1) {
    throw new RangeError("kinetics pose-sample square count must be a positive safe integer");
  }
  if (!Number.isSafeInteger(presentationFrames) || presentationFrames < 2) {
    throw new RangeError("kinetics presentation frame count must be a safe integer of at least 2");
  }
  if (storedFrames !== null && (!Number.isSafeInteger(storedFrames) || storedFrames < 2)) {
    throw new RangeError("kinetics stored frame count must be a safe integer of at least 2");
  }
  const traceFrames = presentationFrames + (storedFrames === null ? 0 : 2 * storedFrames);
  const poseSamples = squareCount * traceFrames;
  if (!Number.isSafeInteger(poseSamples) || poseSamples > MAX_KINETICS_POSE_SAMPLES) {
    throw new RangeError(
      `kinetics pose-sample budget exceeded: ${poseSamples} requested, maximum ${MAX_KINETICS_POSE_SAMPLES}`,
    );
  }
}

function nextArgument(arguments_: readonly string[], index: number, flag: string): string {
  const value = arguments_[index + 1];
  if (value === undefined || value.startsWith("--")) {
    throw new RangeError(`${flag} requires a value`);
  }
  return value;
}

export function parseKineticsArguments(arguments_: readonly string[]): KineticsOptions {
  const options: KineticsOptions = {
    corpusPath: "",
    solver: DEFAULT_ANIMATE_STYLE,
    mode: "snap",
    phase: "add-then-move",
    lawName: "balanced",
    wallLawName: "default",
    pairLawOverrides: {},
    wallLawOverrides: {},
    annealLevel: ANNEAL_SETTINGS.defaultLevel,
    timing: "corpus",
    instance: 17,
    seed: 0,
    stepsPerSecond: STEPS_PER_SECOND,
    sampleRate: 60,
    arrivalDelay: DEFAULT_ARRIVAL_DELAY_FRACTION,
    integrationSubsteps: "adaptive",
    motionResponse: { ...DEFAULT_MOTION_RESPONSE },
    jiggleHz: TRAJECTORY_PHYSICS_SETTINGS.jiggleHz,
    includeFrames: false,
  };
  for (let index = 0; index < arguments_.length; index += 1) {
    const flag = arguments_[index];
    if (flag === "--frames") {
      options.includeFrames = true;
      continue;
    }
    if (flag === "--help") {
      throw new Error("help");
    }
    const value = nextArgument(arguments_, index, flag ?? "argument");
    index += 1;
    if (flag === "--corpus") {
      options.corpusPath = value;
    } else if (flag === "--solver") {
      if (value !== "tween" && value !== "physics" && value !== "bodies") {
        throw new RangeError("solver must be tween, physics, or bodies");
      }
      options.solver = value;
    } else if (flag === "--mode") {
      if (!MODES.some((mode) => mode === value)) {
        throw new RangeError("mode must be snap, free, or blind");
      }
      options.mode = value as AtlasSimMode;
    } else if (flag === "--phase") {
      if (!PHASES.some((phase) => phase === value)) {
        throw new RangeError(`phase must be one of ${PHASES.join(", ")}`);
      }
      options.phase = value as AtlasPhase;
    } else if (flag === "--law") {
      options.lawName = value;
    } else if (flag === "--wall-law") {
      options.wallLawName = value;
    } else if (flag === "--anneal") {
      options.annealLevel = integerArgument(value, "anneal", ANNEAL_SETTINGS.min);
      if (options.annealLevel > ANNEAL_SETTINGS.max) {
        throw new RangeError(`anneal must not exceed ${ANNEAL_SETTINGS.max}`);
      }
    } else if (flag === "--timing") {
      options.timing = value;
    } else if (flag === "--instance") {
      options.instance = integerArgument(value, "instance", 2);
    } else if (flag === "--seed") {
      options.seed = integerArgument(value, "seed", 0);
    } else if (flag === "--steps-per-second") {
      options.stepsPerSecond = numberArgument(value, "steps per second");
      if (options.stepsPerSecond <= 0) {
        throw new RangeError("steps per second must be positive");
      }
    } else if (flag === "--sample-rate") {
      options.sampleRate = numberArgument(value, "sample rate");
      if (options.sampleRate <= 0) {
        throw new RangeError("sample rate must be positive");
      }
    } else if (flag === "--arrival-delay") {
      options.arrivalDelay = numberArgument(value, "arrival delay");
      if (
        options.arrivalDelay < ARRIVAL_DELAY_BOUNDS[0] ||
        options.arrivalDelay > ARRIVAL_DELAY_BOUNDS[1]
      ) {
        throw new RangeError(
          `arrival delay must be between ${ARRIVAL_DELAY_BOUNDS[0]} and ${ARRIVAL_DELAY_BOUNDS[1]}`,
        );
      }
    } else if (flag === "--substeps") {
      options.integrationSubsteps =
        value === "adaptive" ? "adaptive" : integerArgument(value, "substeps", 1);
      if (
        options.integrationSubsteps !== "adaptive" &&
        options.integrationSubsteps > MAX_FORCE_LAW_SUBSTEPS
      ) {
        throw new RangeError(`substeps must not exceed ${MAX_FORCE_LAW_SUBSTEPS}`);
      }
    } else if (flag === "--jiggle-hz") {
      const values = value.split(",").map(Number);
      const low = values[0];
      const high = values[1];
      if (
        values.length !== 2 ||
        low === undefined ||
        high === undefined ||
        !Number.isFinite(low) ||
        !Number.isFinite(high) ||
        low <= 0 ||
        high < low
      ) {
        throw new RangeError("jiggle Hz must be two positive ascending numbers: low,high");
      }
      options.jiggleHz = [low, high];
    } else if (flag?.startsWith("--wall-")) {
      const key = flag.slice("--wall-".length) as MotionLawKey;
      if (!LAW_PARAMETER_DEFINITIONS.some((definition) => definition.key === key)) {
        throw new RangeError(`unknown argument: ${flag}`);
      }
      options.wallLawOverrides[key] = numberArgument(value, flag);
    } else if (flag?.startsWith("--")) {
      const key = flag.slice(2);
      if (LAW_PARAMETER_DEFINITIONS.some((definition) => definition.key === key)) {
        options.pairLawOverrides[key as MotionLawKey] = numberArgument(value, flag);
      } else if (key in PHYSICAL_OVERRIDE_FLAGS) {
        const property = PHYSICAL_OVERRIDE_FLAGS[key as keyof typeof PHYSICAL_OVERRIDE_FLAGS];
        options.motionResponse[property] = numberArgument(value, flag);
      } else {
        throw new RangeError(`unknown argument: ${flag}`);
      }
    } else {
      throw new RangeError(`unexpected positional argument: ${flag}`);
    }
  }
  if (options.corpusPath.length === 0) {
    throw new RangeError("--corpus is required (raw corpus JSON or a generated workbench page)");
  }
  for (const [key, bounds] of Object.entries(MOTION_RESPONSE_BOUNDS)) {
    const value = options.motionResponse[key as keyof typeof options.motionResponse];
    if (value < bounds[0] || value > bounds[1]) {
      throw new RangeError(`${key} must be between ${bounds[0]} and ${bounds[1]}`);
    }
  }
  return options;
}

function timingArgument(value: string, corpus: Corpus): AtlasTiming {
  if (value === "corpus") {
    return { ...corpus.timing };
  }
  if (value === "default") {
    return { ...DEFAULT_STEP_TIMING };
  }
  const fields = value.split(",").map(Number);
  if (fields.length !== 4 || fields.some((field) => !Number.isFinite(field) || field < 0)) {
    throw new RangeError("timing must be corpus, default, or dwell,move,correct,settle in seconds");
  }
  const [dwell, move, correct, settle] = fields;
  if (dwell === undefined || move === undefined || correct === undefined || settle === undefined) {
    throw new RangeError("timing is incomplete");
  }
  return { dwell, move, correct, settle };
}

function boundedLaw(
  name: string,
  overrides: Partial<MotionLaw>,
  wall: boolean,
): { name: string; law: AtlasLaw } {
  const aliases: Record<string, string> = { default: wall ? "default" : "balanced" };
  const effectiveName = aliases[name] ?? name;
  const preset =
    wall && effectiveName === "default" ? DEFAULT_WALL_LAW : pairLawPreset(effectiveName);
  if (preset === null) {
    const names = wall
      ? ["default", ...Object.keys(PAIR_LAW_PRESETS)]
      : ["default", ...Object.keys(PAIR_LAW_PRESETS)];
    throw new RangeError(`unknown ${wall ? "wall " : ""}law ${name}; choose ${names.join(", ")}`);
  }
  const law: MotionLaw = { ...preset, ...overrides };
  const bounds = wall ? WALL_LAW_BOUNDS : PAIR_LAW_BOUNDS;
  for (const definition of LAW_PARAMETER_DEFINITIONS) {
    const [minimum, maximum] = bounds[definition.key];
    const value = law[definition.key];
    if (!Number.isFinite(value) || value < minimum || value > maximum) {
      throw new RangeError(
        `${wall ? "wall " : ""}${definition.key} must be between ${minimum} and ${maximum}`,
      );
    }
  }
  return { name: name === "default" && !wall ? "default" : effectiveName, law };
}

async function loadCorpus(path: string): Promise<Corpus> {
  return decodeCorpus(await readCorpus(path));
}

function transition(corpus: Corpus, instance: number): { pairIndex: number; pair: CorpusPair } {
  const pairIndex = corpus.pairs.findIndex((candidate) => candidate.n + 1 === instance);
  if (pairIndex < 0) {
    throw new RangeError(`corpus has no transition into n=${instance}`);
  }
  return { pairIndex, pair: pairAt(corpus, pairIndex) };
}

function targetPoses(corpus: Corpus, pair: CorpusPair): MotionPose[] {
  const target = frameAt(corpus, pair.n + 1);
  const poses: MotionPose[] = [];
  for (const mapped of pair.map) {
    const pose = target.squares[mapped];
    if (pose === undefined) {
      throw new RangeError("corpus target correspondence is incomplete");
    }
    poses.push({ x: pose[0], y: pose[1], angleRadians: (pose[2] * Math.PI) / 180 });
  }
  const arriving = target.squares[pair.new];
  if (arriving === undefined) {
    throw new RangeError("corpus arriving square is missing");
  }
  poses.push({ x: arriving[0], y: arriving[1], angleRadians: (arriving[2] * Math.PI) / 180 });
  return poses;
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
  const positive = blockTurn + difference;
  const negative = blockTurn + difference - 90;
  return Math.abs(positive) <= Math.abs(negative) + 1e-9 ? positive : negative;
}

function motionTracks(corpus: Corpus, pair: CorpusPair): MotionTrack[] {
  const source = frameAt(corpus, pair.n);
  const target = frameAt(corpus, pair.n + 1);
  return pair.map.map((mapped, index) => {
    const from = source.squares[index];
    const to = target.squares[mapped];
    if (from === undefined || to === undefined) {
      throw new RangeError("corpus tween correspondence is incomplete");
    }
    const blockIndex = pair.block_of[index];
    const block = blockIndex === undefined || blockIndex < 0 ? undefined : pair.blocks[blockIndex];
    if (block === undefined) {
      return {
        ident: source.ident[index] ?? index + 1,
        a: from,
        b: to,
        turn: angleDelta(from[2], to[2]),
        block: null,
        dx: 0,
        dy: 0,
        rx: 0,
        ry: 0,
      };
    }
    const cosine = Math.cos((block.turn * Math.PI) / 180);
    const sine = Math.sin((block.turn * Math.PI) / 180);
    const dx = from[0] - block.from[0];
    const dy = from[1] - block.from[1];
    return {
      ident: source.ident[index] ?? index + 1,
      a: from,
      b: to,
      turn: memberTurn(block.turn, from[2], to[2]),
      block,
      dx,
      dy,
      rx: to[0] - (block.to[0] + cosine * dx - sine * dy),
      ry: to[1] - (block.to[1] + sine * dx + cosine * dy),
    };
  });
}

function tweenFrames(
  corpus: Corpus,
  pairIndex: number,
  timing: AtlasTiming,
  phase: AtlasPhase,
  steps: number,
  arrivalDelay: number,
): MotionFrame[] {
  const pair = pairAt(corpus, pairIndex);
  const source = frameAt(corpus, pair.n);
  const target = frameAt(corpus, pair.n + 1);
  const configuration: TimelineConfiguration = {
    pairs: corpus.pairs,
    timing,
    continuous: { on: false, fullBeat: false, beat: timing, staticBeat: timing },
    anneal: 0,
    phase,
    arrivalFraction: corpus.arrival_fraction,
    newFraction: NEW_FRACTION,
    rollMax: ROLL_MAX,
    arrivalDelay,
  };
  const schedule = pairSchedule(configuration, pairIndex, "tween");
  const tracks = motionTracks(corpus, pair);
  const arriving = target.squares[pair.new];
  if (arriving === undefined) {
    throw new RangeError("corpus arriving square is missing");
  }
  const duration = Math.max(schedule.moveEnd, schedule.containerEnd) - schedule.moveStart;
  return Array.from({ length: steps + 1 }, (_, storedStep) => {
    const elapsed = (duration * storedStep) / steps;
    const scene = illustrationFrame({
      pairIndex,
      n: pair.n + (storedStep === steps ? 1 : 0),
      fromSide: source.side,
      toSide: target.side,
      tracks,
      arriving: { identity: pair.n + 1, pose: arriving },
      previousIndex: null,
      phase,
      schedule,
      seconds: schedule.moveStart + elapsed,
      moveSeconds: timing.move,
      padding: 0,
      drain: 0,
      resting: 0,
      homeward: 0,
      links: false,
      tint: 0,
      mark: { wide: 0, thin: 0, fade: 0 },
    });
    return {
      timeSeconds: elapsed,
      containerSide: scene.containerSide,
      poses: scene.squares.map((square) => ({
        x: square.x,
        y: square.y,
        angleRadians: (square.angleDegrees * Math.PI) / 180,
        size: square.scale,
        active: square.opacity > 0,
      })),
    };
  });
}

function trajectoryFrames(
  trajectory: Trajectory,
  duration: number,
  states: Float64Array,
  includeSimulatorDiagnostics: boolean,
): MotionFrame[] {
  const squareCount = trajectory.n + 1;
  return Array.from({ length: trajectory.steps + 1 }, (_, storedStep) => {
    const newSize = trajectory.newSizes[storedStep] ?? TRAJECTORY_PHYSICS_SETTINGS.inflateFrom;
    return {
      timeSeconds: (duration * storedStep) / trajectory.steps,
      containerSide: trajectory.sides[storedStep] ?? trajectory.side0,
      trajectoryProgress: storedStep / trajectory.steps,
      appearanceProgress: clampUnit(
        (newSize - TRAJECTORY_PHYSICS_SETTINGS.inflateFrom) /
          (1 - TRAJECTORY_PHYSICS_SETTINGS.inflateFrom),
      ),
      ...(includeSimulatorDiagnostics
        ? {
            simulatorPairPenetration: trajectory.allPens[storedStep] ?? 0,
            nearPairs: trajectory.nears[storedStep] ?? 0,
          }
        : {}),
      poses: Array.from({ length: squareCount }, (_, square) => {
        const offset = (storedStep * squareCount + square) * 3;
        const x = states[offset];
        const y = states[offset + 1];
        const angleRadians = states[offset + 2];
        if (x === undefined || y === undefined || angleRadians === undefined) {
          throw new RangeError("trajectory state is incomplete");
        }
        return { x, y, angleRadians, size: square === trajectory.n ? newSize : 1 };
      }),
    };
  });
}

function clampUnit(value: number): number {
  return Math.max(0, Math.min(1, value));
}

function interpolate(first: number, second: number, progress: number): number {
  return first + (second - first) * progress;
}

function easeInOut(progress: number): number {
  return progress < 0.5 ? 4 * progress * progress * progress : 1 - (-2 * progress + 2) ** 3 / 2;
}

function smootherstep(progress: number): number {
  const value = clampUnit(progress);
  return value * value * value * (value * (value * 6 - 15) + 10);
}

function presentedContainerSide(
  sourceSide: number,
  targetSide: number,
  progress: number,
  physics: TrajectoryPhysicsConfiguration,
): number {
  const growth = 1 - (1 - clampUnit(progress / physics.grow)) ** 3;
  const shutSpan = Math.max(1e-6, 1 - physics.blend - physics.shutFrom);
  const open = smootherstep(progress / physics.openBy);
  const shut = smootherstep((progress - physics.shutFrom) / shutSpan);
  return interpolate(sourceSide, targetSide, growth) + physics.open * open * (1 - shut);
}

function physicalPresentedFrames(
  corpus: Corpus,
  pair: CorpusPair,
  trajectory: Trajectory,
  timing: AtlasTiming,
  duration: number,
  steps: number,
  physics: TrajectoryPhysicsConfiguration,
  presentationSchedule: PhysicalPresentationSchedule,
): MotionFrame[] {
  const source = frameAt(corpus, pair.n);
  const target = frameAt(corpus, pair.n + 1);
  const targets = targetPoses(corpus, pair);
  const blind = trajectory.mode === "blind";
  return Array.from({ length: steps + 1 }, (_, frameIndex) => {
    const elapsed = (duration * frameIndex) / steps;
    const presentation = physicalPresentationState(elapsed, duration, timing, presentationSchedule);
    const progress = presentation.trajectoryProgress;
    const containerProgress = presentation.containerProgress;
    const needsTrajectory = physicalPresentationNeedsTrajectory(
      presentation,
      trajectory.mode === "snap",
    );
    const opening = blind ? easeInOut(clampUnit(progress / BLIND_TRAJECTORY_SETTINGS.open)) : 1;
    const containerOpening = blind
      ? easeInOut(clampUnit(containerProgress / BLIND_TRAJECTORY_SETTINGS.open))
      : 1;
    const simulationProgress = blind
      ? clampUnit(
          (progress - BLIND_TRAJECTORY_SETTINGS.open) / (1 - BLIND_TRAJECTORY_SETTINGS.open),
        )
      : Math.min(progress, 1);
    const containerSimulationProgress = blind
      ? clampUnit(
          (containerProgress - BLIND_TRAJECTORY_SETTINGS.open) /
            (1 - BLIND_TRAJECTORY_SETTINGS.open),
        )
      : Math.min(containerProgress, 1);
    const side =
      blind && needsTrajectory
        ? containerOpening < 1
          ? interpolate(source.side, trajectory.side0, containerOpening)
          : sampleTrajectorySide(trajectory, containerSimulationProgress)
        : containerProgress >= 1
          ? target.side
          : presentedContainerSide(source.side, target.side, containerProgress, physics);
    const poses: MotionPose[] = [];
    for (let square = 0; square < pair.n; square += 1) {
      const from = source.squares[square];
      const expected = targets[square];
      if (from === undefined || expected === undefined) {
        throw new RangeError("presentation correspondence is incomplete");
      }
      if (progress <= 0) {
        poses.push({ x: from[0], y: from[1], angleRadians: (from[2] * Math.PI) / 180 });
      } else if (!needsTrajectory) {
        poses.push({ ...expected });
      } else {
        const sampled = sampleTrajectoryPose(
          trajectory,
          square,
          opening < 1 ? 0 : simulationProgress,
        );
        const sampledPose = {
          x: sampled[0],
          y: sampled[1],
          angleRadians: (sampled[2] * Math.PI) / 180,
        };
        poses.push(
          blind && opening < 1
            ? {
                x: interpolate(from[0], sampledPose.x, opening),
                y: interpolate(from[1], sampledPose.y, opening),
                angleRadians: interpolate(
                  (from[2] * Math.PI) / 180,
                  sampledPose.angleRadians,
                  opening,
                ),
              }
            : sampledPose,
        );
      }
    }
    const expectedNew = targets[pair.n];
    if (expectedNew === undefined) {
      throw new RangeError("presentation arriving square is missing");
    }
    const appearance = presentation.appearanceProgress;
    if (appearance > 0 && needsTrajectory) {
      const sampled = sampleTrajectoryPose(trajectory, pair.n, simulationProgress);
      poses.push({
        x: sampled[0],
        y: sampled[1],
        angleRadians: (sampled[2] * Math.PI) / 180,
      });
    } else {
      poses.push({ ...expectedNew, active: appearance > 0 });
    }
    return {
      timeSeconds: elapsed,
      containerSide: side,
      trajectoryProgress: progress,
      containerProgress,
      appearanceProgress: appearance,
      poses,
    };
  });
}

function sameTrajectory(left: Trajectory, right: Trajectory): boolean {
  return (
    left.states.length === right.states.length &&
    left.states.every((value, index) => value === right.states[index]) &&
    left.rawStates.every((value, index) => value === right.rawStates[index]) &&
    left.sides.every((value, index) => value === right.sides[index]) &&
    left.pens.every((value, index) => value === right.pens[index]) &&
    left.allPens.every((value, index) => value === right.allPens[index]) &&
    left.newSizes.every((value, index) => value === right.newSizes[index]) &&
    left.nears.every((value, index) => value === right.nears[index])
  );
}

function presentedGeometryEpochs(frames: readonly MotionFrame[]) {
  const fullSizeIndex = frames.findIndex((frame) => (frame.appearanceProgress ?? 1) >= 1);
  if (fullSizeIndex < 2 || frames.length - fullSizeIndex < 2) {
    return null;
  }
  const growthFrames = frames.slice(0, fullSizeIndex);
  const fullSizeFrames = frames.slice(fullSizeIndex);
  return {
    growth: {
      frames: growthFrames.length,
      endTimeSeconds: growthFrames.at(-1)?.timeSeconds,
      geometry: analyzeMotionTrace({ frames: growthFrames }).presentedGeometry,
    },
    fullSize: {
      frames: fullSizeFrames.length,
      startTimeSeconds: fullSizeFrames[0]?.timeSeconds,
      geometry: analyzeMotionTrace({ frames: fullSizeFrames }).presentedGeometry,
    },
  };
}

export async function measureKinetics(options: KineticsOptions): Promise<Record<string, unknown>> {
  const corpus = await loadCorpus(options.corpusPath);
  const { pairIndex, pair } = transition(corpus, options.instance);
  const timing = timingArgument(options.timing, corpus);
  const staticStep = pair.kind === "prefix" || pair.kind === "shared-picture";
  const effectiveSolver: MotionStyle = staticStep ? "tween" : options.solver;
  const anneal = annealConfiguration(options.annealLevel);
  const visibleSpan = effectiveSolver === "tween" ? 1 : anneal.span;
  const solverDuration = (timing.move + timing.correct) * visibleSpan;
  if (solverDuration <= 0) {
    throw new RangeError("kinetics measurement requires a positive move or correction duration");
  }
  const storedSteps =
    effectiveSolver === "tween"
      ? null
      : frameSteps(options.stepsPerSecond, solverDuration, MAX_KINETICS_STORED_FRAMES, "stored");
  const timelineConfiguration: TimelineConfiguration = {
    pairs: corpus.pairs,
    timing,
    continuous: { on: false, fullBeat: false, beat: timing, staticBeat: timing },
    anneal: options.annealLevel,
    phase: options.phase,
    arrivalFraction: corpus.arrival_fraction,
    newFraction: NEW_FRACTION,
    rollMax: ROLL_MAX,
    arrivalDelay: options.arrivalDelay,
  };
  const schedule = pairSchedule(timelineConfiguration, pairIndex, effectiveSolver);
  const presentationDuration =
    Math.max(schedule.moveEnd, schedule.containerEnd) - schedule.moveStart;
  const presentationSteps = frameSteps(
    options.sampleRate,
    presentationDuration,
    MAX_KINETICS_PRESENTATION_FRAMES,
    "presentation",
  );
  assertKineticsPoseSampleBudget(
    pair.n + 1,
    presentationSteps + 1,
    storedSteps === null ? null : storedSteps + 1,
  );
  const pairLaw = boundedLaw(options.lawName, options.pairLawOverrides, false);
  const wallLaw = boundedLaw(options.wallLawName, options.wallLawOverrides, true);
  const effectiveSeed = mixUint32Seed(pair.n, options.seed);
  const physics: TrajectoryPhysicsConfiguration = {
    ...trajectoryPhysicsConfiguration(options.motionResponse),
    jiggleHz: options.jiggleHz,
  };
  const source = frameAt(corpus, pair.n);
  const target = frameAt(corpus, pair.n + 1);

  let presentedFrames: MotionFrame[];
  let storedFrames: MotionFrame[] | null = null;
  let rawStoredFrames: MotionFrame[] | null = null;
  let deterministic: boolean;
  let work: Record<string, unknown>;
  let wallMilliseconds: number;
  let presentedLandingStart: number | undefined;
  let storedLandingStart: number | undefined;
  if (effectiveSolver === "tween") {
    const started = performance.now();
    presentedFrames = tweenFrames(
      corpus,
      pairIndex,
      timing,
      options.phase,
      presentationSteps,
      options.arrivalDelay,
    );
    wallMilliseconds = stableNumber(performance.now() - started);
    const replay = tweenFrames(
      corpus,
      pairIndex,
      timing,
      options.phase,
      presentationSteps,
      options.arrivalDelay,
    );
    deterministic = identicalMotionFrames(presentedFrames, replay);
    work = {
      applicable: false,
      reason: staticStep
        ? "static append uses the direct illustration for every selected solver"
        : "tween is a direct illustration and does not integrate a physical system",
      storedSteps: "not_applicable",
      presentationSteps,
      integrationSteps: 0,
      substepsPerStoredStep: "not_applicable",
    };
  } else {
    if (storedSteps === null) {
      throw new Error("physical kinetics measurement has no stored step count");
    }
    const request = {
      pairIndex,
      pair,
      source,
      target,
      steps: storedSteps,
      style: effectiveSolver,
      mode: options.mode,
      effectiveSeed,
      pairLaw: pairLaw.law,
      wallLaw: wallLaw.law,
      relatedMask: null,
      anneal,
      physics,
      blind: BLIND_TRAJECTORY_SETTINGS,
      integrationSubsteps: options.integrationSubsteps,
    } as const;
    const started = performance.now();
    const trajectory = buildTrajectory(request);
    wallMilliseconds = stableNumber(performance.now() - started);
    const replay = buildTrajectory(request);
    deterministic = sameTrajectory(trajectory, replay);
    storedFrames = trajectoryFrames(trajectory, solverDuration, trajectory.states, false);
    rawStoredFrames = trajectoryFrames(trajectory, solverDuration, trajectory.rawStates, true);
    const presentedTiming: AtlasTiming = {
      ...timing,
      move: timing.move * anneal.span,
      correct: timing.correct * anneal.span,
    };
    const motionStartFraction =
      presentationDuration <= 0
        ? 0
        : (schedule.blocksStart - schedule.moveStart) / presentationDuration;
    const presentationSchedule: PhysicalPresentationSchedule = {
      motionStartFraction,
      motionEndFraction:
        presentationDuration <= 0
          ? 1
          : (schedule.blocksEnd - schedule.moveStart) / presentationDuration,
      containerStartFraction:
        presentationDuration <= 0
          ? 0
          : (schedule.containerStart - schedule.moveStart) / presentationDuration,
      containerEndFraction:
        presentationDuration <= 0
          ? 1
          : (schedule.containerEnd - schedule.moveStart) / presentationDuration,
      arrivalStartFraction:
        presentationDuration <= 0
          ? 0
          : (schedule.arrive - schedule.moveStart) / presentationDuration,
      arrivalEndFraction:
        presentationDuration <= 0
          ? 0
          : (schedule.arrived - schedule.moveStart) / presentationDuration,
    };
    const landingProgress =
      trajectory.mode === "blind"
        ? BLIND_TRAJECTORY_SETTINGS.open +
          (1 - BLIND_TRAJECTORY_SETTINGS.open) * PHYSICS_SETTINGS.tightenFrom
        : PHYSICS_SETTINGS.tightenFrom;
    presentedFrames = physicalPresentedFrames(
      corpus,
      pair,
      trajectory,
      presentedTiming,
      presentationDuration,
      presentationSteps,
      physics,
      presentationSchedule,
    );
    presentedLandingStart = presentedFrames.find(
      (frame) => (frame.trajectoryProgress ?? 0) >= landingProgress,
    )?.timeSeconds;
    storedLandingStart = storedFrames.find(
      (frame) => (frame.trajectoryProgress ?? 0) >= PHYSICS_SETTINGS.tightenFrom,
    )?.timeSeconds;
    work = {
      applicable: true,
      storedSteps: trajectory.steps,
      presentationSteps,
      integrationSteps: trajectory.receipt.work.steps,
      substepsPerStoredStep: trajectory.receipt.configuration.integration.effective,
      integration: trajectory.receipt.configuration.integration,
      storedTimestepSimulationSeconds: stableNumber(trajectory.receipt.storedTimestep),
      kernelTimestepSimulationSeconds: stableNumber(trajectory.receipt.timestep),
      impliedMaximumStoredDisplacement: stableNumber(
        physics.maxSpeed * trajectory.receipt.storedTimestep,
      ),
      penetrationEpochs: trajectory.receipt.penetration,
      pairCandidates: trajectory.receipt.work.pairCandidates,
      pairForces: trajectory.receipt.work.pairForces,
      wallForces: trajectory.receipt.work.wallForces,
    };
  }
  const expected = targetPoses(corpus, pair);
  const summaryFor = (
    frames: readonly MotionFrame[],
    poses: readonly MotionPose[],
    landingStartTimeSeconds: number | undefined,
    motionStartTimeSeconds: number | undefined,
  ) =>
    analyzeMotionTrace({
      frames,
      target: poses,
      ...(landingStartTimeSeconds === undefined ? {} : { landingStartTimeSeconds }),
      ...(motionStartTimeSeconds === undefined ? {} : { motionStartTimeSeconds }),
    });
  const establishedFrames = (frames: readonly MotionFrame[]) =>
    frames.map((frame) => ({ ...frame, poses: frame.poses.slice(0, pair.n) }));
  const presentedMotionStart = presentedFrames.find(
    (frame) => (frame.trajectoryProgress ?? 0) > 0,
  )?.timeSeconds;
  const summary = summaryFor(
    presentedFrames,
    expected,
    presentedLandingStart,
    presentedMotionStart,
  );
  const establishedSummary = summaryFor(
    establishedFrames(presentedFrames),
    expected.slice(0, pair.n),
    presentedLandingStart,
    presentedMotionStart,
  );
  const storedSummary =
    storedFrames === null ? null : summaryFor(storedFrames, expected, storedLandingStart, 0);
  const establishedStoredSummary =
    storedFrames === null
      ? null
      : summaryFor(
          establishedFrames(storedFrames),
          expected.slice(0, pair.n),
          storedLandingStart,
          0,
        );
  const rawStoredSummary =
    rawStoredFrames === null ? null : summaryFor(rawStoredFrames, expected, storedLandingStart, 0);
  const establishedRawStoredSummary =
    rawStoredFrames === null
      ? null
      : summaryFor(
          establishedFrames(rawStoredFrames),
          expected.slice(0, pair.n),
          storedLandingStart,
          0,
        );
  const physical =
    effectiveSolver === "tween"
      ? {
          applicable: false,
          reason: staticStep
            ? "the selected transition is a static append"
            : "tween interpolates known poses; force law and annealing are not consulted",
          requested: {
            law: options.lawName,
            wallLaw: options.wallLawName,
            anneal: options.annealLevel,
          },
        }
      : {
          applicable: true,
          pairLaw: pairLaw.law,
          wallLaw: wallLaw.law,
          anneal,
          physics,
          blind: BLIND_TRAJECTORY_SETTINGS,
        };
  const report: Record<string, unknown> = {
    schema: KINETICS_SCHEMA,
    units: {
      position: "square-side",
      angle: "radian",
      time: "second",
      speed: "square-side/second",
      acceleration: "square-side/second^2",
      jerk: "square-side/second^3",
    },
    definitions: {
      presentationFrame:
        "the browser-presented pose sampled uniformly in wall time through the moving and correction span, using the shared square, container, and trajectory clocks",
      storedFrame:
        "one solver cache state at the configured storage cadence; snap correction is included",
      rawStoredFrame:
        "one pre-snap solver cache state with simulator-native diagnostics from the same interval",
      reversal:
        "successive center-displacement vectors with negative dot product; intervals below the reported minimum are excluded",
      landing:
        "preLanding and landing split the trace where stored physical progress reaches the shared tightening boundary; finalInterval isolates the last displayed frame transition",
      appearancePoseTransition:
        "reportedPoseDisplacement compares the last invisible pose with the first visible pose as a staging diagnostic; it is excluded from visible displacement kinetics",
      populations:
        "summary includes every visible square; establishedSquaresSummary excludes the arriving identity so historical motion targets remain comparable",
      nearestNeighborGap:
        "minimum signed separating-axis face-normal gap among square pairs; positive is separated and negative is penetration",
      penetration:
        effectiveSolver === "tween"
          ? "presented pair and wall overlap recomputed independently from each illustrated frame"
          : "presented pair and wall overlap recomputed from emitted poses; simulatorNative separately reports the kernel's pre-snap full-size pair diagnostic",
      endpoint: "error from the retained n+1 corpus frame in trajectory square order",
      runtime:
        "wall time for one trace generation; deterministic replay and metric analysis excluded",
    },
    configuration: {
      solver: effectiveSolver,
      requestedSolver: options.solver,
      mode: effectiveSolver === "tween" ? "not_applicable" : options.mode,
      phase: options.phase,
      law: effectiveSolver === "tween" ? "not_applicable" : pairLaw.name,
      wallLaw: effectiveSolver === "tween" ? "not_applicable" : wallLaw.name,
      anneal: effectiveSolver === "tween" ? "not_applicable" : anneal.level,
      timing,
      solverDurationSeconds: stableNumber(solverDuration),
      presentationDurationSeconds: stableNumber(presentationDuration),
      instance: options.instance,
      transition: { from: pair.n, to: pair.n + 1, pairIndex },
      seed: options.seed,
      effectiveSeed: effectiveSolver === "tween" ? "not_applicable" : effectiveSeed,
      stepsPerSecond: effectiveSolver === "tween" ? "not_applicable" : options.stepsPerSecond,
      presentationSampleRate: options.sampleRate,
      arrivalDelayFraction: options.arrivalDelay,
      integrationSubsteps:
        effectiveSolver === "tween" ? "not_applicable" : options.integrationSubsteps,
      steps: storedSteps ?? "not_applicable",
      presentationSteps,
    },
    physical,
    summary,
    kinetics: {
      presented: {
        cadenceHz: options.sampleRate,
        frames: presentedFrames.length,
        summary,
        establishedSquaresSummary: establishedSummary,
        geometryEpochs: presentedGeometryEpochs(presentedFrames),
      },
      stored:
        storedSummary === null
          ? { applicable: false, reason: "direct illustration has no solver cache" }
          : {
              applicable: true,
              cadenceHz:
                storedSteps === null
                  ? "not_applicable"
                  : stableNumber(storedSteps / solverDuration),
              frames: storedFrames?.length,
              summary: storedSummary,
              establishedSquaresSummary: establishedStoredSummary,
              geometryEpochs: presentedGeometryEpochs(storedFrames ?? []),
            },
      rawStored:
        rawStoredSummary === null
          ? { applicable: false, reason: "direct illustration has no raw solver state" }
          : {
              applicable: true,
              cadenceHz:
                storedSteps === null
                  ? "not_applicable"
                  : stableNumber(storedSteps / solverDuration),
              frames: rawStoredFrames?.length,
              summary: rawStoredSummary,
              establishedSquaresSummary: establishedRawStoredSummary,
              geometryEpochs: presentedGeometryEpochs(rawStoredFrames ?? []),
            },
    },
    determinism: {
      identical: deterministic,
      scope:
        effectiveSolver === "tween"
          ? "presented frame arrays"
          : "raw and corrected trajectory, side, size, penetration, and neighbor arrays",
      comparedFrames: effectiveSolver === "tween" ? presentedFrames.length : storedFrames?.length,
    },
    work,
    runtime: { wallMilliseconds },
  };
  if (options.includeFrames) {
    report.frames = presentedFrames;
    report.storedFrames = storedFrames;
    report.rawStoredFrames = rawStoredFrames;
  }
  return report;
}

const HELP = `usage: node tools/measure-kinetics.ts --corpus PAGE_OR_JSON [options]

required:
  --corpus PATH                 generated workbench HTML or raw corpus JSON

experiment inputs:
  --solver tween|physics|bodies (default: ${DEFAULT_ANIMATE_STYLE})
  --mode snap|free|blind        physical solver target mode (default: snap)
  --phase NAME                  illustrated tween phase (default: add-then-move)
  --law NAME                    default|balanced|rigid|soft|sticky
  --wall-law NAME               default or any pair-law shape
  --anneal 0..20                annealing level (default: ${ANNEAL_SETTINGS.defaultLevel})
  --timing VALUE                corpus|default|dwell,move,correct,settle
  --instance N                  transition into N (default: 17)
  --seed N                      nonnegative integer (default: 0)
  --steps-per-second N          stored trajectory sampling rate (default: ${STEPS_PER_SECOND})
  --sample-rate N               presented wall-time sampling rate (default: 60)
  --arrival-delay 0..0.6      moving-span delay from container resize to the new square fading in (default: ${DEFAULT_ARRIVAL_DELAY_FRACTION})
  --substeps adaptive|1..${MAX_FORCE_LAW_SUBSTEPS}     integrator substeps (default: adaptive)

law overrides:
  --rigidity N --repulsion N --attraction N --range N
  --wall-rigidity N --wall-repulsion N --wall-attraction N --wall-range N

kinetic overrides:
  --contact-damping N --speed-limit N
  --jiggle-hz LOW,HIGH          forcing-frequency range in cycles per simulated second

output:
  --frames                       include every stored pose, not only summary metrics
`;

const invokedPath = process.argv[1];
if (invokedPath !== undefined && import.meta.filename === resolve(invokedPath)) {
  try {
    const options = parseKineticsArguments(process.argv.slice(2));
    process.stdout.write(`${JSON.stringify(await measureKinetics(options), null, 2)}\n`);
  } catch (error) {
    if (error instanceof Error && error.message === "help") {
      process.stdout.write(HELP);
      process.exitCode = 0;
    } else {
      process.stderr.write(`${error instanceof Error ? error.message : String(error)}\n\n${HELP}`);
      process.exitCode = 2;
    }
  }
}
