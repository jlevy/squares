import type { AtlasGrowthRule, AtlasLaw } from "../api/workbench-api.ts";
import type { GeometryPose, GeometrySnapshot } from "../core/geometry.ts";
import {
  assessPackingSnapshot,
  mixUint32Seed,
  PACKING_VALIDITY,
  type PackingAssessment,
  parseUint32Seed,
} from "../core/runtime-contracts.ts";
import { type Corpus, type CorpusFrame, frameAt } from "../data/corpus.ts";
import {
  advancePackRun,
  createGridPackStart,
  createPackRun,
  createRandomPackStart,
  type PackAnnealConfiguration,
  type PackConfiguration,
  type PackContainerConfiguration,
  type PackGrowthConfiguration,
  type PackPhysicsConfiguration,
  type PackReceipt,
  type PackStationarityConfiguration,
} from "../simulation/pack.ts";
import { resolvePacking } from "../simulation/resolve.ts";
import {
  appendPackStartCandidateCount,
  createAppendPackStart,
} from "../simulation/start-proposals.ts";
import {
  type JsonObject,
  type SearchPackingState,
  type SearchPlan,
  type SearchSelectedState,
  type SearchSlot,
  type SearchTrialControl,
  type SearchTrialRunner,
  type SearchTrialValue,
  selectedSearchState,
} from "./contracts.ts";

export const PACK_SEARCH_CONFIGURATION_CONTRACT = "packing.squares:PackSearchConfiguration/v1";

type UnknownRow = Record<string, unknown>;

export type PackSearchProposal =
  | { kind: "grid" }
  | { kind: "random"; containerSide: number }
  | { kind: "record-append"; inflate: number; gridStep: number };

export type PackSearchRepair = { kind: "none" } | { kind: "resolve"; tolerance: number };

export interface PackSearchObjective {
  kind: "absolute-side" | "relative-excess";
  state: SearchSelectedState;
  requireStationary: boolean;
}

export interface PackSearchConfiguration {
  contract: typeof PACK_SEARCH_CONFIGURATION_CONTRACT;
  seedBase: number;
  proposal: PackSearchProposal;
  reference: "none" | "corpus";
  targets: "none" | "record";
  pairLaw: AtlasLaw;
  wallLaw: AtlasLaw;
  relatedMask: readonly number[] | null;
  physics: PackPhysicsConfiguration;
  anneal: PackAnnealConfiguration;
  growth: PackGrowthConfiguration;
  container: PackContainerConfiguration;
  stationarity: PackStationarityConfiguration;
  repair: PackSearchRepair;
  objective: PackSearchObjective;
}

export interface PackSearchContext {
  corpus?: Corpus;
  /** Maximum base steps before returning to the host event loop. */
  batchSteps?: number;
  yieldControl?: () => Promise<void>;
}

function row(value: unknown, fields: readonly string[], label: string): UnknownRow {
  if (value === null || typeof value !== "object" || Array.isArray(value)) {
    throw new TypeError(`${label} must be an object`);
  }
  const result: UnknownRow = {};
  for (const [key, field] of Object.entries(value)) {
    if (!fields.includes(key)) {
      throw new TypeError(`${label} has unsupported field ${key}`);
    }
    result[key] = field;
  }
  return result;
}

function finite(value: unknown, label: string): number {
  if (typeof value !== "number" || !Number.isFinite(value)) {
    throw new TypeError(`${label} must be finite`);
  }
  return value;
}

function positive(value: unknown, label: string): number {
  const number = finite(value, label);
  if (number <= 0) {
    throw new RangeError(`${label} must be positive`);
  }
  return number;
}

function nonnegative(value: unknown, label: string): number {
  const number = finite(value, label);
  if (number < 0) {
    throw new RangeError(`${label} must be nonnegative`);
  }
  return number;
}

function positiveInteger(value: unknown, label: string): number {
  if (!Number.isSafeInteger(value) || (value as number) < 1) {
    throw new RangeError(`${label} must be a positive safe integer`);
  }
  return value as number;
}

function boolean(value: unknown, label: string): boolean {
  if (typeof value !== "boolean") {
    throw new TypeError(`${label} must be a boolean`);
  }
  return value;
}

function law(value: unknown, label: string): AtlasLaw {
  const declared = row(value, ["rigidity", "repulsion", "attraction", "range"], label);
  return {
    rigidity: positive(declared.rigidity, `${label} rigidity`),
    repulsion: nonnegative(declared.repulsion, `${label} repulsion`),
    attraction: nonnegative(declared.attraction, `${label} attraction`),
    range: nonnegative(declared.range, `${label} range`),
  };
}

function proposal(value: unknown): PackSearchProposal {
  const base = row(value, ["kind", "container_side", "inflate", "grid_step"], "proposal");
  if (base.kind === "grid") {
    row(value, ["kind"], "grid proposal");
    return { kind: "grid" };
  }
  if (base.kind === "random") {
    row(value, ["kind", "container_side"], "random proposal");
    return {
      kind: "random",
      containerSide: positive(base.container_side, "random proposal container side"),
    };
  }
  if (base.kind === "record-append") {
    row(value, ["kind", "inflate", "grid_step"], "record append proposal");
    return {
      kind: "record-append",
      inflate: positive(base.inflate, "record append inflation"),
      gridStep: positive(base.grid_step, "record append grid step"),
    };
  }
  throw new TypeError("proposal kind must be grid, random or record-append");
}

function reference(value: unknown): "none" | "corpus" {
  if (value === "none" || value === "corpus") {
    return value;
  }
  throw new TypeError("reference must be none or corpus");
}

function targets(value: unknown): "none" | "record" {
  if (value === "none" || value === "record") {
    return value;
  }
  throw new TypeError("targets must be none or record");
}

function relatedMask(value: unknown): readonly number[] | null {
  if (value === null) {
    return null;
  }
  if (!Array.isArray(value) || value.some((item) => item !== 0 && item !== 1)) {
    throw new TypeError("related mask must be null or an array of zeros and ones");
  }
  return value as number[];
}

function physics(value: unknown): PackPhysicsConfiguration {
  const declared = row(
    value,
    [
      "steps_per_second",
      "omega",
      "zeta",
      "contact_damping",
      "contact_torque",
      "jiggle",
      "jiggle_torque",
      "jiggle_hz",
      "max_speed",
      "max_spin",
      "cell",
    ],
    "physics configuration",
  );
  if (!Array.isArray(declared.jiggle_hz) || declared.jiggle_hz.length !== 2) {
    throw new TypeError("physics jiggle_hz must contain exactly two frequencies");
  }
  const jiggleHz: readonly [number, number] = [
    positive(declared.jiggle_hz[0], "minimum jiggle frequency"),
    positive(declared.jiggle_hz[1], "maximum jiggle frequency"),
  ];
  if (jiggleHz[1] < jiggleHz[0]) {
    throw new RangeError("physics jiggle frequency range is reversed");
  }
  return {
    stepsPerSecond: positive(declared.steps_per_second, "physics steps per second"),
    omega: positive(declared.omega, "physics omega"),
    zeta: positive(declared.zeta, "physics zeta"),
    contactDamping: nonnegative(declared.contact_damping, "physics contact damping"),
    contactTorque: nonnegative(declared.contact_torque, "physics contact torque"),
    jiggle: nonnegative(declared.jiggle, "physics jiggle"),
    jiggleTorque: nonnegative(declared.jiggle_torque, "physics jiggle torque"),
    jiggleHz,
    maxSpeed: positive(declared.max_speed, "physics maximum speed"),
    maxSpin: positive(declared.max_spin, "physics maximum spin"),
    cell: positive(declared.cell, "physics cell"),
  };
}

function anneal(value: unknown): PackAnnealConfiguration {
  const declared = row(value, ["amplitude", "decay_power", "tau", "floor"], "annealing");
  const floor = nonnegative(declared.floor, "annealing floor");
  if (floor > 1) {
    throw new RangeError("annealing floor must not exceed one");
  }
  return {
    amplitude: nonnegative(declared.amplitude, "annealing amplitude"),
    decayPower: positive(declared.decay_power, "annealing decay power"),
    tau: positive(declared.tau, "annealing time constant"),
    floor,
  };
}

function growthRule(value: unknown): AtlasGrowthRule {
  if (value === "constant" || value === "clean") {
    return value;
  }
  throw new TypeError("growth rule must be constant or clean");
}

function growth(value: unknown): PackGrowthConfiguration {
  const declared = row(value, ["on", "rate", "rule"], "growth configuration");
  return {
    on: boolean(declared.on, "growth on"),
    rate: nonnegative(declared.rate, "growth rate"),
    rule: growthRule(declared.rule),
  };
}

function container(value: unknown): PackContainerConfiguration {
  const declared = row(
    value,
    ["squeeze_rate", "relax_rate", "squeeze_tolerance", "jam_tolerance", "minimum_side"],
    "container configuration",
  );
  return {
    squeezeRate: nonnegative(declared.squeeze_rate, "container squeeze rate"),
    relaxRate: nonnegative(declared.relax_rate, "container relax rate"),
    squeezeTolerance: nonnegative(declared.squeeze_tolerance, "container squeeze tolerance"),
    jamTolerance: nonnegative(declared.jam_tolerance, "container jam tolerance"),
    minimumSide: positive(declared.minimum_side, "container minimum side"),
  };
}

function stationarity(value: unknown): PackStationarityConfiguration {
  const declared = row(
    value,
    ["linear_speed", "angular_speed", "forcing_scale", "window", "stop"],
    "stationarity configuration",
  );
  const stop = boolean(declared.stop, "stationarity stop");
  if (stop) {
    throw new RangeError("Search requires stationarity stop=false to preserve fixed physics work");
  }
  return {
    linearSpeed: nonnegative(declared.linear_speed, "stationarity linear speed"),
    angularSpeed: nonnegative(declared.angular_speed, "stationarity angular speed"),
    forcingScale: nonnegative(declared.forcing_scale, "stationarity forcing scale"),
    window: positiveInteger(declared.window, "stationarity window"),
    stop,
  };
}

function repair(value: unknown): PackSearchRepair {
  const declared = row(value, ["kind", "tolerance"], "repair configuration");
  if (declared.kind === "none") {
    row(value, ["kind"], "disabled repair configuration");
    return { kind: "none" };
  }
  if (declared.kind === "resolve") {
    row(value, ["kind", "tolerance"], "resolve configuration");
    const tolerance = nonnegative(declared.tolerance, "repair tolerance");
    if (tolerance > PACKING_VALIDITY.penetrationTolerance) {
      throw new RangeError(
        `repair tolerance must not exceed the shared ${PACKING_VALIDITY.penetrationTolerance} validity tolerance`,
      );
    }
    return { kind: "resolve", tolerance };
  }
  throw new TypeError("repair kind must be none or resolve");
}

function objective(value: unknown): PackSearchObjective {
  const declared = row(value, ["kind", "state", "require_stationary"], "objective configuration");
  if (declared.kind !== "absolute-side" && declared.kind !== "relative-excess") {
    throw new TypeError("objective kind must be absolute-side or relative-excess");
  }
  if (
    declared.state !== "raw" &&
    declared.state !== "repaired" &&
    declared.state !== "best-observed"
  ) {
    throw new TypeError("objective state must be raw, repaired or best-observed");
  }
  return {
    kind: declared.kind,
    state: declared.state,
    requireStationary: boolean(declared.require_stationary, "objective stationarity requirement"),
  };
}

/** Decode the complete Pack configuration used by a Search registry entry. */
export function decodePackSearchConfiguration(value: unknown): PackSearchConfiguration {
  const declared = row(
    value,
    [
      "contract",
      "seed_base",
      "proposal",
      "reference",
      "targets",
      "pair_law",
      "wall_law",
      "related_mask",
      "physics",
      "anneal",
      "growth",
      "container",
      "stationarity",
      "repair",
      "objective",
    ],
    "Pack search configuration",
  );
  if (declared.contract !== PACK_SEARCH_CONFIGURATION_CONTRACT) {
    throw new TypeError(`unsupported Pack search configuration ${String(declared.contract)}`);
  }
  const seedBase = parseUint32Seed(declared.seed_base);
  if (seedBase === null) {
    throw new RangeError("Pack search seed_base must be an unsigned 32-bit integer");
  }
  const decoded: PackSearchConfiguration = {
    contract: PACK_SEARCH_CONFIGURATION_CONTRACT,
    seedBase,
    proposal: proposal(declared.proposal),
    reference: reference(declared.reference),
    targets: targets(declared.targets),
    pairLaw: law(declared.pair_law, "pair law"),
    wallLaw: law(declared.wall_law, "wall law"),
    relatedMask: relatedMask(declared.related_mask),
    physics: physics(declared.physics),
    anneal: anneal(declared.anneal),
    growth: growth(declared.growth),
    container: container(declared.container),
    stationarity: stationarity(declared.stationarity),
    repair: repair(declared.repair),
    objective: objective(declared.objective),
  };
  if (decoded.proposal.kind === "record-append" && decoded.reference !== "corpus") {
    throw new RangeError("record-append proposals require corpus reference provenance");
  }
  if (decoded.targets === "record" && decoded.proposal.kind !== "record-append") {
    throw new RangeError("record targets require a record-append proposal with stable identities");
  }
  if (decoded.objective.state === "repaired" && decoded.repair.kind !== "resolve") {
    throw new RangeError("a repaired objective requires the resolve repair capability");
  }
  if (decoded.objective.kind === "relative-excess" && decoded.reference !== "corpus") {
    throw new RangeError("a relative-excess objective requires a corpus reference");
  }
  return decoded;
}

function corpusTransition(corpus: Corpus, n: number): { index: number; frame: CorpusFrame } {
  const index = corpus.pairs.findIndex((candidate) => candidate.n + 1 === n);
  if (index < 0) {
    throw new RangeError(`corpus has no transition into n=${n}`);
  }
  return { index, frame: frameAt(corpus, n) };
}

function frameSnapshot(frame: CorpusFrame): GeometrySnapshot {
  return {
    squareSide: 1,
    container: { originX: 0, originY: 0, side: frame.side },
    poses: frame.squares.map(([x, y, degrees]) => ({
      x,
      y,
      angle: (degrees * Math.PI) / 180,
    })),
  };
}

function recordTargets(corpus: Corpus, pairIndex: number): GeometryPose[] {
  const pair = corpus.pairs[pairIndex];
  if (pair === undefined) {
    throw new RangeError(`corpus has no transition at index ${pairIndex}`);
  }
  const target = frameSnapshot(frameAt(corpus, pair.n + 1)).poses;
  const ordered: GeometryPose[] = [];
  for (let source = 0; source < pair.n; source += 1) {
    const targetIndex = pair.map[source];
    const pose = targetIndex === undefined ? undefined : target[targetIndex];
    if (pose === undefined) {
      throw new RangeError("corpus transition target mapping is incomplete");
    }
    ordered.push({ ...pose });
  }
  const arriving = target[pair.new];
  if (arriving === undefined) {
    throw new RangeError("corpus transition has no arriving-square target");
  }
  ordered.push({ ...arriving });
  return ordered;
}

interface PreparedTrial {
  configuration: PackConfiguration;
  proposalAttempts: number;
  recordSide: number | null;
}

function prepareTrial(
  slot: SearchSlot,
  decoded: PackSearchConfiguration,
  context: PackSearchContext,
): PreparedTrial {
  const effectiveSeed = mixUint32Seed(decoded.seedBase, slot.seed);
  let pairIndex: number | null = null;
  let recordSide: number | null = null;
  if (decoded.reference === "corpus") {
    if (context.corpus === undefined) {
      throw new RangeError("Pack search configuration requires a decoded corpus");
    }
    const transition = corpusTransition(context.corpus, slot.n);
    pairIndex = transition.index;
    recordSide = transition.frame.side;
  }
  let start: GeometrySnapshot;
  let proposalAttempts: number;
  if (decoded.proposal.kind === "grid") {
    start = createGridPackStart(slot.n);
    proposalAttempts = 1;
  } else if (decoded.proposal.kind === "random") {
    start = createRandomPackStart(slot.n, decoded.proposal.containerSide, effectiveSeed);
    proposalAttempts = 1;
  } else {
    if (context.corpus === undefined || recordSide === null) {
      throw new RangeError("record-append proposal requires a decoded corpus reference");
    }
    const previous = frameSnapshot(frameAt(context.corpus, slot.n - 1));
    const containerSide = recordSide * decoded.proposal.inflate;
    proposalAttempts = appendPackStartCandidateCount(
      containerSide,
      previous.squareSide,
      decoded.proposal.gridStep,
    );
    if (proposalAttempts > slot.workBudget.proposalAttempts) {
      throw new RangeError(
        `proposal needs ${proposalAttempts} attempts but the slot permits ${slot.workBudget.proposalAttempts}`,
      );
    }
    start = createAppendPackStart(previous, containerSide, {
      gridStep: decoded.proposal.gridStep,
    });
  }
  if (proposalAttempts > slot.workBudget.proposalAttempts) {
    throw new RangeError(
      `proposal needs ${proposalAttempts} attempts but the slot permits ${slot.workBudget.proposalAttempts}`,
    );
  }
  if (decoded.relatedMask !== null && decoded.relatedMask.length !== slot.n ** 2) {
    throw new RangeError("related mask does not match the slot count");
  }
  if (decoded.repair.kind === "resolve" && slot.workBudget.repairIterations < 1) {
    throw new RangeError("resolve repair requires a positive repair iteration budget");
  }
  const targets =
    decoded.targets === "none"
      ? null
      : recordTargets(
          context.corpus ??
            (() => {
              throw new RangeError("record targets require a decoded corpus");
            })(),
          pairIndex ?? -1,
        );
  return {
    configuration: {
      n: slot.n,
      seed: slot.seed,
      effectiveSeed,
      startKind: decoded.proposal.kind === "record-append" ? "previous" : decoded.proposal.kind,
      start,
      targets,
      reference: pairIndex === null || recordSide === null ? null : { pairIndex, recordSide },
      pairLaw: { ...decoded.pairLaw },
      wallLaw: { ...decoded.wallLaw },
      relatedMask: decoded.relatedMask === null ? null : Uint8Array.from(decoded.relatedMask),
      physics: { ...decoded.physics, jiggleHz: [...decoded.physics.jiggleHz] },
      anneal: { ...decoded.anneal },
      growth: { ...decoded.growth },
      container: { ...decoded.container },
      stationarity: { ...decoded.stationarity },
    },
    proposalAttempts,
    recordSide,
  };
}

function packingState(assessment: PackingAssessment): SearchPackingState {
  return {
    snapshot: {
      squareSide: assessment.snapshot.squareSide,
      container: { ...assessment.snapshot.container },
      poses: assessment.snapshot.poses.map((pose) => ({ ...pose })),
    },
    valid: assessment.valid,
    validityReason: assessment.reason,
    absoluteSide: Number.isFinite(assessment.requiredSide) ? assessment.requiredSide : null,
  };
}

function effectiveConfiguration(
  declared: JsonObject,
  requestedSeed: number,
  effectiveSeed: number,
): JsonObject {
  return {
    ...structuredClone(declared),
    requested_seed: requestedSeed,
    effective_seed: effectiveSeed,
  };
}

function trialObjective(
  configuration: PackSearchConfiguration,
  trial: SearchTrialValue,
  recordSide: number | null,
): number | null {
  const selected = selectedSearchState(trial);
  if (
    selected === null ||
    !selected.valid ||
    selected.absoluteSide === null ||
    (configuration.objective.requireStationary && !trial.stationarity.stationary)
  ) {
    return null;
  }
  if (configuration.objective.kind === "absolute-side") {
    return selected.absoluteSide;
  }
  if (recordSide === null) {
    throw new RangeError("relative-excess objective has no record side");
  }
  return (selected.absoluteSide - recordSide) / recordSide;
}

/** Validate each plan/configuration/cohort join before claiming a trial slot. */
export function validatePackSearchPlan(plan: SearchPlan, context: PackSearchContext = {}): void {
  const decoded = new Map(
    plan.configurations.map((entry) => [
      entry.id,
      decodePackSearchConfiguration(entry.configuration),
    ]),
  );
  for (const slot of plan.slots) {
    const configuration = decoded.get(slot.configurationId);
    if (configuration === undefined) {
      throw new RangeError(`slot ${slot.id} has no Pack search configuration`);
    }
    prepareTrial(slot, configuration, context);
  }
}

/** Create a fixed-work Search runner over the shared Pack and Resolve contracts. */
export function createPackSearchRunner(context: PackSearchContext = {}): SearchTrialRunner {
  const batchSteps = context.batchSteps ?? 32;
  positiveInteger(batchSteps, "Search batch steps");
  const yieldControl =
    context.yieldControl ??
    (() => new Promise<void>((resolve) => globalThis.setTimeout(resolve, 0)));
  return async (
    slot: SearchSlot,
    declared: JsonObject,
    control: SearchTrialControl,
  ): Promise<SearchTrialValue> => {
    const decoded = decodePackSearchConfiguration(declared);
    const prepared = prepareTrial(slot, decoded, context);
    const run = createPackRun(prepared.configuration);
    let receipt: PackReceipt;
    do {
      await yieldControl();
      receipt = advancePackRun(
        run,
        Math.min(batchSteps, slot.workBudget.physicsSteps - run.work.baseSteps),
        {
          shouldCancel: () => control.cancellationReason() !== null,
        },
      );
      if (receipt.termination.reason !== "work-limit") {
        break;
      }
    } while (receipt.work.baseSteps < slot.workBudget.physicsSteps);
    if (receipt.termination.reason === "nonfinite") {
      throw new RangeError("Pack produced a nonfinite state");
    }
    const rawAssessment = assessPackingSnapshot(receipt.snapshot, slot.n);
    const raw = packingState(rawAssessment);
    const bestObserved =
      receipt.best === null ? null : packingState(assessPackingSnapshot(receipt.best, slot.n));
    await yieldControl();
    // A requested repair always calls Resolve, which reports `cancelled` itself when the slot was
    // cancelled first, so the receipt never says repair was not requested when it was.
    const repairReceipt =
      decoded.repair.kind === "none"
        ? null
        : resolvePacking(
            raw.snapshot,
            {
              expectedCount: slot.n,
              iterationLimit: slot.workBudget.repairIterations,
              tolerance: decoded.repair.tolerance,
            },
            { shouldCancel: () => control.cancellationReason() !== null },
          );
    const trial: SearchTrialValue = {
      raw,
      repaired:
        repairReceipt?.repaired === null || repairReceipt?.repaired === undefined
          ? null
          : packingState(repairReceipt.repaired),
      bestObserved,
      selectedState: decoded.objective.state,
      stationarity: {
        stationary:
          receipt.termination.stationarySteps >= prepared.configuration.stationarity.window,
        stationarySteps: receipt.termination.stationarySteps,
        window: prepared.configuration.stationarity.window,
        residual: { ...receipt.residual },
        forcingScale: receipt.forcing.scale,
        thresholds: {
          linearSpeed: prepared.configuration.stationarity.linearSpeed,
          angularSpeed: prepared.configuration.stationarity.angularSpeed,
          forcingScale: prepared.configuration.stationarity.forcingScale,
        },
      },
      repair: {
        termination: repairReceipt?.termination.reason ?? "not-requested",
        resolved: repairReceipt?.termination.resolved ?? false,
        exhausted: repairReceipt?.termination.exhausted ?? false,
        tolerance: decoded.repair.kind === "resolve" ? decoded.repair.tolerance : null,
        iterationLimit: slot.workBudget.repairIterations,
      },
      objective: null,
      work: {
        proposalAttempts: prepared.proposalAttempts,
        physicsSteps: receipt.work.baseSteps,
        repairIterations: repairReceipt?.work.iterations ?? 0,
        pairCandidates: receipt.work.pairCandidates,
        pairForces: receipt.work.pairForces,
        wallForces: receipt.work.wallForces,
        repairPairTests: repairReceipt?.work.pairTests ?? 0,
        repairPairTranslations: repairReceipt?.work.pairTranslations ?? 0,
        repairFitTranslations: repairReceipt?.work.fitTranslations ?? 0,
      },
      configuration: effectiveConfiguration(
        declared,
        receipt.configuration.seed,
        receipt.configuration.effectiveSeed,
      ),
    };
    trial.objective = trialObjective(decoded, trial, prepared.recordSide);
    return trial;
  };
}
