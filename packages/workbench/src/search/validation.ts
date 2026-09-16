import {
  assessPackingSnapshot,
  mixUint32Seed,
  PACKING_VALIDITY,
} from "../core/runtime-contracts.ts";
import {
  RESOLVE_TERMINATION_REASONS,
  RESOLVED_TERMINATION_REASONS,
} from "../simulation/resolve.ts";
import {
  type JsonObject,
  type SearchSlot,
  type SearchTrialValue,
  selectedSearchState,
} from "./contracts.ts";
import {
  decodePackSearchConfiguration,
  PACK_SEARCH_CONFIGURATION_CONTRACT,
} from "./pack-runner.ts";

export interface SearchAdmissionOptions {
  /** Trusted corpus lookup supplied by the caller, never read from an imported receipt. */
  referenceSide?: (slot: SearchSlot) => number;
}

function canonical(value: unknown): string {
  if (value === null || typeof value !== "object") {
    return JSON.stringify(value);
  }
  if (Array.isArray(value)) {
    return `[${value.map(canonical).join(",")}]`;
  }
  return `{${Object.entries(value)
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([key, item]) => `${JSON.stringify(key)}:${canonical(item)}`)
    .join(",")}}`;
}

function admitPolicy(
  result: SearchTrialValue,
  slot: SearchSlot,
  configuration: JsonObject,
  options: SearchAdmissionOptions,
): void {
  const pack =
    configuration.contract === PACK_SEARCH_CONFIGURATION_CONTRACT
      ? decodePackSearchConfiguration(configuration)
      : null;
  const expected =
    pack === null
      ? configuration
      : {
          ...configuration,
          requested_seed: slot.seed,
          effective_seed: mixUint32Seed(pack.seedBase, slot.seed),
        };
  if (canonical(result.configuration) !== canonical(expected)) {
    throw new RangeError("trial effective configuration or seed disagrees with plan");
  }
  const policy = configuration.objective;
  if (
    policy === null ||
    typeof policy !== "object" ||
    Array.isArray(policy) ||
    (policy.kind !== "absolute-side" && policy.kind !== "relative-excess") ||
    typeof policy.require_stationary !== "boolean" ||
    policy.state !== result.selectedState
  ) {
    throw new RangeError("trial objective policy disagrees with plan");
  }
  if (pack !== null) {
    const stationarity = result.stationarity;
    if (
      stationarity.window !== pack.stationarity.window ||
      stationarity.thresholds.linearSpeed !== pack.stationarity.linearSpeed ||
      stationarity.thresholds.angularSpeed !== pack.stationarity.angularSpeed ||
      stationarity.thresholds.forcingScale !== pack.stationarity.forcingScale ||
      result.repair.tolerance !== (pack.repair.kind === "resolve" ? pack.repair.tolerance : null)
    ) {
      throw new RangeError("trial stationarity or repair policy disagrees with plan");
    }
  }
  const selected = selectedSearchState(result);
  let objective: number | null = null;
  if (
    selected?.valid === true &&
    selected.absoluteSide !== null &&
    (!policy.require_stationary || result.stationarity.stationary)
  ) {
    objective = selected.absoluteSide;
    if (policy.kind === "relative-excess") {
      const reference = options.referenceSide?.(structuredClone(slot));
      if (reference === undefined || !Number.isFinite(reference) || reference <= 0) {
        throw new RangeError("relative objective requires a trusted corpus reference side");
      }
      objective = (objective - reference) / reference;
    }
  }
  if (result.objective !== objective) {
    throw new RangeError("trial objective disagrees with checked geometry and plan policy");
  }
  result.objective = objective;
}

type Shape =
  | "number"
  | "boolean"
  | "string"
  | "json"
  | ["nullable" | "array", Shape]
  | { readonly [key: string]: Shape };
const nullable = (shape: Shape): Shape => ["nullable", shape];
const packingShape: Shape = {
  snapshot: {
    squareSide: "number",
    container: { originX: "number", originY: "number", side: "number" },
    poses: ["array", { x: "number", y: "number", angle: "number" }],
  },
  valid: "boolean",
  validityReason: nullable("string"),
  absoluteSide: nullable("number"),
};
const trialShape: Shape = {
  raw: packingShape,
  repaired: nullable(packingShape),
  bestObserved: nullable(packingShape),
  selectedState: "string",
  stationarity: {
    stationary: "boolean",
    stationarySteps: "number",
    window: "number",
    residual: { maxLinearSpeed: "number", maxAngularSpeed: "number" },
    forcingScale: "number",
    thresholds: { linearSpeed: "number", angularSpeed: "number", forcingScale: "number" },
  },
  repair: {
    termination: "string",
    resolved: "boolean",
    exhausted: "boolean",
    tolerance: nullable("number"),
    iterationLimit: "number",
  },
  objective: nullable("number"),
  work: {
    proposalAttempts: "number",
    physicsSteps: "number",
    repairIterations: "number",
    pairCandidates: "number",
    pairForces: "number",
    wallForces: "number",
    repairPairTests: "number",
    repairPairTranslations: "number",
    repairFitTranslations: "number",
  },
  configuration: "json",
};

function checkShape(value: unknown, shape: Shape, path: string, depth = 0): void {
  if (depth > 64) {
    throw new TypeError(`${path} exceeds the nesting limit`);
  }
  if (shape === "json") {
    if (value === null || typeof value === "string" || typeof value === "boolean") {
      return;
    }
    if (typeof value === "number" && Number.isFinite(value)) {
      return;
    }
    if (typeof value !== "object" || value === null) {
      throw new TypeError(`${path} must be finite JSON`);
    }
    for (const field of Object.values(value)) {
      checkShape(field, "json", path, depth + 1);
    }
    return;
  }
  if (typeof shape === "string") {
    if (typeof value !== shape || (typeof value === "number" && !Number.isFinite(value))) {
      throw new TypeError(`${path} must be a finite ${shape}`);
    }
    return;
  }
  if (Array.isArray(shape)) {
    const member = shape[1];
    if (member === undefined) {
      throw new TypeError("missing internal shape");
    }
    if (shape[0] === "nullable") {
      if (value !== null) {
        checkShape(value, member, path, depth + 1);
      }
    } else {
      if (!Array.isArray(value)) {
        throw new TypeError(`${path} must be an array`);
      }
      value.forEach((field, index) => {
        checkShape(field, member, `${path}[${index}]`, depth + 1);
      });
    }
    return;
  }
  if (value === null || typeof value !== "object" || Array.isArray(value)) {
    throw new TypeError(`${path} must be an object`);
  }
  const fields = Object.fromEntries(Object.entries(value));
  const keys = Object.keys(shape);
  if (Object.keys(fields).some((key) => !keys.includes(key))) {
    throw new TypeError(`${path} has unsupported fields`);
  }
  for (const [key, fieldShape] of Object.entries(shape)) {
    checkShape(fields[key], fieldShape, `${path}.${key}`, depth + 1);
  }
}

function integer(value: number, label: string, minimum = 0): void {
  if (!Number.isSafeInteger(value) || value < minimum) {
    throw new RangeError(`${label} must be a safe integer >= ${minimum}`);
  }
}

/** Admit runner and persisted results through the same shape, geometry and work checks. */
export function decodeSearchTrialValue(
  value: unknown,
  slot: SearchSlot,
  completed: boolean,
  configuration: JsonObject,
  options: SearchAdmissionOptions = {},
): SearchTrialValue {
  checkShape(value, trialShape, "trial");
  // Every field above has been checked before crossing the unknown boundary.
  const result = structuredClone(value) as SearchTrialValue;
  if (
    result.selectedState !== "raw" &&
    result.selectedState !== "repaired" &&
    result.selectedState !== "best-observed"
  ) {
    throw new TypeError("unsupported selected trial state");
  }
  for (const state of [result.raw, result.repaired, result.bestObserved]) {
    if (state === null) {
      continue;
    }
    const assessment = assessPackingSnapshot(state.snapshot, slot.n);
    if (state.valid !== assessment.valid || state.valid !== (state.validityReason === null)) {
      throw new RangeError("trial validity disagrees with snapshot geometry");
    }
    if (state.absoluteSide !== assessment.requiredSide) {
      throw new RangeError("trial absolute side disagrees with snapshot geometry");
    }
  }
  const selected = selectedSearchState(result);
  if ((selected === null || !selected.valid) && result.objective !== null) {
    throw new RangeError("an unavailable or invalid trial cannot carry a ranking objective");
  }
  for (const [label, count] of Object.entries(result.work)) {
    integer(count, `trial work ${label}`);
  }
  for (const key of ["proposalAttempts", "physicsSteps", "repairIterations"] as const) {
    if (result.work[key] > slot.workBudget[key]) {
      throw new RangeError(`trial ${key} exceeded its declared work budget`);
    }
  }
  if (completed && result.work.physicsSteps !== slot.workBudget.physicsSteps) {
    throw new RangeError("trial did not complete its fixed physics work");
  }
  const stationarity = result.stationarity;
  integer(stationarity.stationarySteps, "stationary steps");
  integer(stationarity.window, "stationarity window", 1);
  if (
    stationarity.stationarySteps > result.work.physicsSteps ||
    stationarity.stationary !== stationarity.stationarySteps >= stationarity.window
  ) {
    throw new RangeError("trial stationarity accounting disagrees");
  }
  for (const count of [
    ...Object.values(stationarity.residual),
    ...Object.values(stationarity.thresholds),
    stationarity.forcingScale,
  ]) {
    if (count < 0) {
      throw new RangeError("stationarity measurements must be nonnegative");
    }
  }
  if (
    stationarity.stationary &&
    (stationarity.residual.maxLinearSpeed > stationarity.thresholds.linearSpeed ||
      stationarity.residual.maxAngularSpeed > stationarity.thresholds.angularSpeed ||
      stationarity.forcingScale > stationarity.thresholds.forcingScale)
  ) {
    throw new RangeError("stationary trial exceeds its declared thresholds");
  }
  if (result.bestObserved !== null && !result.bestObserved.valid) {
    throw new RangeError("best observed state must be valid");
  }
  if (
    result.repair.tolerance !== null &&
    (result.repair.tolerance < 0 || result.repair.tolerance > PACKING_VALIDITY.penetrationTolerance)
  ) {
    throw new RangeError("invalid repair tolerance");
  }
  // The termination is Resolve's own reason or `not-requested`, and every flag beside it follows
  // from it the way `resolvePacking` sets them.
  const termination: string = result.repair.termination;
  const resolveReason = RESOLVE_TERMINATION_REASONS.find((reason) => reason === termination);
  if (resolveReason === undefined && termination !== "not-requested") {
    throw new TypeError("unsupported repair termination");
  }
  if ((resolveReason === undefined) !== (result.repair.tolerance === null)) {
    throw new RangeError("repair tolerance must be null exactly when no repair was requested");
  }
  if (
    result.repair.resolved !==
    (resolveReason !== undefined && RESOLVED_TERMINATION_REASONS.includes(resolveReason))
  ) {
    throw new RangeError("repair resolved flag disagrees with its termination");
  }
  if (result.repair.exhausted !== (resolveReason === "budget-exhausted")) {
    throw new RangeError("repair exhausted flag disagrees with its termination");
  }
  if (
    result.repair.resolved &&
    (result.repaired === null || !result.repaired.valid || result.repair.exhausted)
  ) {
    throw new RangeError("resolved repair must carry a valid state without exhaustion");
  }
  integer(result.repair.iterationLimit, "repair iteration limit");
  if (result.repair.iterationLimit !== slot.workBudget.repairIterations) {
    throw new RangeError("repair limit disagrees with slot budget");
  }
  if (
    result.configuration === null ||
    typeof result.configuration !== "object" ||
    Array.isArray(result.configuration)
  ) {
    throw new TypeError("trial configuration must be an object");
  }
  admitPolicy(result, slot, configuration, options);
  return result;
}
