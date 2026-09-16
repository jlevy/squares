import { parseUint32Seed } from "../core/runtime-contracts.ts";
import {
  type JsonObject,
  type JsonValue,
  SEARCH_PLAN_CONTRACT,
  type SearchCohort,
  type SearchConfigurationEntry,
  type SearchPartition,
  type SearchPlan,
  type SearchSlot,
  type SearchSource,
  type SearchWorkBudget,
} from "./contracts.ts";

type UnknownRow = Record<string, unknown>;

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

function list(value: unknown, label: string): unknown[] {
  if (!Array.isArray(value)) {
    throw new TypeError(`${label} must be an array`);
  }
  return value;
}

function text(value: unknown, label: string): string {
  if (typeof value !== "string" || value.length === 0) {
    throw new TypeError(`${label} must be a nonempty string`);
  }
  return value;
}

function boolean(value: unknown, label: string): boolean {
  if (typeof value !== "boolean") {
    throw new TypeError(`${label} must be a boolean`);
  }
  return value;
}

function integer(value: unknown, label: string, minimum = 0): number {
  if (!Number.isSafeInteger(value) || (value as number) < minimum) {
    throw new RangeError(`${label} must be a safe integer >= ${minimum}`);
  }
  return value as number;
}

function positive(value: unknown, label: string): number {
  if (typeof value !== "number" || !Number.isFinite(value) || value <= 0) {
    throw new RangeError(`${label} must be finite and positive`);
  }
  return value;
}

function jsonValue(value: unknown, label: string, depth = 0): JsonValue {
  if (depth > 32) {
    throw new RangeError(`${label} nesting exceeds 32 levels`);
  }
  if (value === null) {
    return null;
  }
  if (typeof value === "boolean" || typeof value === "string") {
    return value;
  }
  if (typeof value === "number") {
    if (!Number.isFinite(value)) {
      throw new RangeError(`${label} numbers must be finite`);
    }
    return value;
  }
  if (Array.isArray(value)) {
    return value.map((item) => jsonValue(item, label, depth + 1));
  }
  if (typeof value !== "object") {
    throw new TypeError(`${label} must contain only JSON values`);
  }
  return Object.fromEntries(
    Object.entries(value).map(([key, field]) => [key, jsonValue(field, label, depth + 1)]),
  );
}

function jsonObject(value: unknown, label: string): JsonObject {
  const checked = jsonValue(value, label);
  if (checked === null || typeof checked !== "object" || Array.isArray(checked)) {
    throw new TypeError(`${label} must be a JSON object`);
  }
  return checked;
}

function source(value: unknown): SearchSource {
  const sourceRow = row(value, ["commit", "dirty", "runtime", "engine"], "search source");
  return {
    commit: text(sourceRow.commit, "source commit"),
    dirty: boolean(sourceRow.dirty, "source dirty flag"),
    runtime: text(sourceRow.runtime, "source runtime"),
    engine: text(sourceRow.engine, "source engine"),
  };
}

function partition(value: unknown): SearchPartition {
  if (value === "tuning" || value === "held-out" || value === "exploratory") {
    return value;
  }
  throw new TypeError("cohort partition must be tuning, held-out or exploratory");
}

function workBudget(value: unknown): SearchWorkBudget {
  const budget = row(
    value,
    ["proposal_attempts", "physics_steps", "repair_iterations"],
    "work budget",
  );
  return {
    proposalAttempts: integer(budget.proposal_attempts, "proposal attempts"),
    physicsSteps: integer(budget.physics_steps, "physics steps", 1),
    repairIterations: integer(budget.repair_iterations, "repair iterations"),
  };
}

function configuration(value: unknown): SearchConfigurationEntry {
  const entry = row(value, ["id", "configuration"], "search configuration");
  return {
    id: text(entry.id, "configuration id"),
    configuration: jsonObject(entry.configuration, "search configuration"),
  };
}

function cohort(value: unknown): SearchCohort {
  const entry = row(
    value,
    [
      "id",
      "configuration_id",
      "partition",
      "n",
      "seeds",
      "block_size",
      "work_budget",
      "timeout_ms",
    ],
    "search cohort",
  );
  const seeds = list(entry.seeds, "cohort seeds").map((seed) => {
    const checked = parseUint32Seed(seed);
    if (checked === null) {
      throw new RangeError("cohort seeds must be unsigned 32-bit integers");
    }
    return checked;
  });
  if (seeds.length === 0 || new Set(seeds).size !== seeds.length) {
    throw new RangeError("each cohort needs unique seed slots");
  }
  return {
    id: text(entry.id, "cohort id"),
    configurationId: text(entry.configuration_id, "cohort configuration id"),
    partition: partition(entry.partition),
    n: integer(entry.n, "cohort n", 1),
    seeds,
    blockSize: integer(entry.block_size, "cohort block size", 1),
    workBudget: workBudget(entry.work_budget),
    timeoutMs: entry.timeout_ms === undefined ? null : positive(entry.timeout_ms, "cohort timeout"),
  };
}

function uniqueIds(values: readonly { id: string }[], label: string): void {
  if (new Set(values.map(({ id }) => id)).size !== values.length) {
    throw new RangeError(`${label} ids must be unique`);
  }
}

function slots(cohorts: readonly SearchCohort[]): SearchSlot[] {
  const result: SearchSlot[] = [];
  for (const cohort of cohorts) {
    cohort.seeds.forEach((seed, position) => {
      result.push({
        id: `${cohort.id}:${position}`,
        index: result.length,
        cohortId: cohort.id,
        configurationId: cohort.configurationId,
        partition: cohort.partition,
        n: cohort.n,
        seed,
        block: Math.floor(position / cohort.blockSize),
        positionInBlock: position % cohort.blockSize,
        workBudget: { ...cohort.workBudget },
        timeoutMs: cohort.timeoutMs,
      });
    });
  }
  return result;
}

/** Decode a complete, versioned registry and derive its deterministic trial slots. */
export function decodeSearchPlan(value: unknown): SearchPlan {
  const plan = row(value, ["contract", "id", "source", "configurations", "cohorts"], "search plan");
  if (plan.contract !== SEARCH_PLAN_CONTRACT) {
    throw new TypeError(`unsupported search plan contract ${String(plan.contract)}`);
  }
  const configurations = list(plan.configurations, "configurations").map(configuration);
  const cohorts = list(plan.cohorts, "cohorts").map(cohort);
  if (configurations.length === 0 || cohorts.length === 0) {
    throw new RangeError("search plan needs configurations and cohorts");
  }
  uniqueIds(configurations, "configuration");
  uniqueIds(cohorts, "cohort");
  const configurationIds = new Set(configurations.map(({ id }) => id));
  for (const declared of cohorts) {
    if (!configurationIds.has(declared.configurationId)) {
      throw new RangeError(
        `cohort ${declared.id} names unknown configuration ${declared.configurationId}`,
      );
    }
  }
  return {
    contract: SEARCH_PLAN_CONTRACT,
    id: text(plan.id, "search plan id"),
    source: source(plan.source),
    configurations,
    cohorts,
    slots: slots(cohorts),
  };
}

export function configurationFor(plan: SearchPlan, id: string): JsonObject {
  const entry = plan.configurations.find((candidate) => candidate.id === id);
  if (entry === undefined) {
    throw new RangeError(`search plan has no configuration ${id}`);
  }
  return entry.configuration;
}
