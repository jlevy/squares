import type { PackingSnapshot } from "../core/runtime-contracts.ts";
import type { ResolveTerminationReason } from "../simulation/resolve.ts";

export const SEARCH_PLAN_CONTRACT = "packing.squares:SearchPlan/v1";
export const SEARCH_OUTCOMES_CONTRACT = "packing.squares:SearchOutcomes/v1";

export type SearchPartition = "tuning" | "held-out" | "exploratory";
export type SearchTerminalStatus = "completed" | "failed" | "timed-out" | "cancelled";
export type SearchSlotStatus = SearchTerminalStatus | "not-started";
export type SearchCancellationReason = "timed-out" | "cancelled";

export type JsonValue =
  | null
  | boolean
  | number
  | string
  | JsonValue[]
  | { [key: string]: JsonValue };
export type JsonObject = { [key: string]: JsonValue };

export interface SearchSource {
  commit: string;
  dirty: boolean;
  runtime: string;
  engine: string;
}

export interface SearchConfigurationEntry {
  id: string;
  configuration: JsonObject;
}

export interface SearchWorkBudget {
  proposalAttempts: number;
  physicsSteps: number;
  repairIterations: number;
}

export interface SearchWorkReceipt extends SearchWorkBudget {
  pairCandidates: number;
  pairForces: number;
  wallForces: number;
  repairPairTests: number;
  repairPairTranslations: number;
  repairFitTranslations: number;
}

export interface SearchCohort {
  id: string;
  configurationId: string;
  partition: SearchPartition;
  n: number;
  seeds: readonly number[];
  blockSize: number;
  workBudget: SearchWorkBudget;
  timeoutMs: number | null;
}

export interface SearchSlot {
  id: string;
  index: number;
  cohortId: string;
  configurationId: string;
  partition: SearchPartition;
  n: number;
  seed: number;
  block: number;
  positionInBlock: number;
  workBudget: SearchWorkBudget;
  timeoutMs: number | null;
}

export interface SearchPlan {
  contract: typeof SEARCH_PLAN_CONTRACT;
  id: string;
  source: SearchSource;
  configurations: readonly SearchConfigurationEntry[];
  cohorts: readonly SearchCohort[];
  slots: readonly SearchSlot[];
}

export interface SearchPackingState {
  snapshot: PackingSnapshot;
  valid: boolean;
  validityReason: string | null;
  absoluteSide: number | null;
}

export type SearchSelectedState = "raw" | "repaired" | "best-observed";

/** How a slot's repair ended: Resolve's own termination, or `not-requested` when none was asked for. */
export type SearchRepairTermination = ResolveTerminationReason | "not-requested";

export interface SearchStationarityReceipt {
  stationary: boolean;
  stationarySteps: number;
  window: number;
  residual: { maxLinearSpeed: number; maxAngularSpeed: number };
  forcingScale: number;
  thresholds: { linearSpeed: number; angularSpeed: number; forcingScale: number };
}

export interface SearchTrialValue {
  /** Exact terminal state returned by Pack. */
  raw: SearchPackingState;
  /** Independently checked repair of the terminal state, when requested. */
  repaired: SearchPackingState | null;
  /** Smallest independently admitted state observed by Pack during this slot. */
  bestObserved: SearchPackingState | null;
  selectedState: SearchSelectedState;
  stationarity: SearchStationarityReceipt;
  repair: {
    termination: SearchRepairTermination;
    resolved: boolean;
    exhausted: boolean;
    tolerance: number | null;
    iterationLimit: number;
  };
  objective: number | null;
  work: SearchWorkReceipt;
  configuration: JsonObject;
}

export function selectedSearchState(result: SearchTrialValue): SearchPackingState | null {
  if (result.selectedState === "raw") {
    return result.raw;
  }
  if (result.selectedState === "repaired") {
    return result.repaired;
  }
  return result.bestObserved;
}

interface SearchOutcomeBase {
  slot: SearchSlot;
  elapsedMs: number;
}

export interface SearchCompletedOutcome extends SearchOutcomeBase {
  status: "completed";
  result: SearchTrialValue;
}

export interface SearchFailedOutcome extends SearchOutcomeBase {
  status: "failed";
  error: string;
  partial: SearchTrialValue | null;
}

export interface SearchInterruptedOutcome extends SearchOutcomeBase {
  status: "timed-out" | "cancelled";
  error: string;
  partial: SearchTrialValue | null;
}

export interface SearchNotStartedOutcome {
  slot: SearchSlot;
  status: "not-started";
  elapsedMs: 0;
  reason: string;
}

export type SearchOutcome =
  | SearchCompletedOutcome
  | SearchFailedOutcome
  | SearchInterruptedOutcome
  | SearchNotStartedOutcome;

export interface SearchOutcomes {
  contract: typeof SEARCH_OUTCOMES_CONTRACT;
  planId: string;
  /** Complete immutable declaration binds resume to configurations and source provenance. */
  plan: SearchPlan;
  outcomes: readonly SearchOutcome[];
}

export interface SearchTrialControl {
  cancellationReason(): SearchCancellationReason | null;
}

export type SearchTrialRunner = (
  slot: SearchSlot,
  configuration: JsonObject,
  control: SearchTrialControl,
) => SearchTrialValue | Promise<SearchTrialValue>;
