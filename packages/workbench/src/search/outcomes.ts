import {
  SEARCH_OUTCOMES_CONTRACT,
  type SearchOutcome,
  type SearchOutcomes,
  type SearchPlan,
} from "./contracts.ts";
import { configurationFor } from "./registry.ts";
import { decodeSearchTrialValue, type SearchAdmissionOptions } from "./validation.ts";

function strictJson(_key: string, value: unknown): unknown {
  if (typeof value === "number" && !Number.isFinite(value)) {
    throw new RangeError("search outcome contains a nonfinite number");
  }
  return value;
}

/** Serialize a complete slot ledger without JSON's nonfinite-to-null coercion. */
export function encodeSearchOutcomes(
  outcomes: SearchOutcomes,
  options: SearchAdmissionOptions = {},
): string {
  if (outcomes.contract !== SEARCH_OUTCOMES_CONTRACT) {
    throw new TypeError(`unsupported search outcomes contract ${outcomes.contract}`);
  }
  return `${JSON.stringify(decodeSearchOutcomes(outcomes, outcomes.plan, options), strictJson, 2)}\n`;
}

export interface SearchStatusCounts {
  completed: number;
  failed: number;
  timedOut: number;
  cancelled: number;
  notStarted: number;
}

/** Count operational outcomes independently from packing validity. */
export function statusCounts(outcomes: readonly SearchOutcome[]): SearchStatusCounts {
  const counts: SearchStatusCounts = {
    completed: 0,
    failed: 0,
    timedOut: 0,
    cancelled: 0,
    notStarted: 0,
  };
  for (const outcome of outcomes) {
    switch (outcome.status) {
      case "completed":
        counts.completed += 1;
        break;
      case "failed":
        counts.failed += 1;
        break;
      case "timed-out":
        counts.timedOut += 1;
        break;
      case "cancelled":
        counts.cancelled += 1;
        break;
      case "not-started":
        counts.notStarted += 1;
        break;
    }
  }
  return counts;
}

function object(value: unknown, fields: readonly string[], label: string): Record<string, unknown> {
  if (value === null || typeof value !== "object" || Array.isArray(value)) {
    throw new TypeError(`${label} must be an object`);
  }
  const result = Object.fromEntries(Object.entries(value));
  if (Object.keys(result).some((key) => !fields.includes(key))) {
    throw new TypeError(`${label} has unsupported fields`);
  }
  return result;
}

function canonical(value: unknown): string {
  const normalize = (item: unknown): unknown => {
    if (item === null || typeof item !== "object") {
      return strictJson("", item);
    }
    if (Array.isArray(item)) {
      return item.map(normalize);
    }
    return Object.fromEntries(
      Object.entries(item)
        .sort(([left], [right]) => left.localeCompare(right))
        .map(([key, field]) => [key, normalize(field)]),
    );
  };
  return JSON.stringify(normalize(value));
}

/** Decode a complete ledger, rejecting changed plans, forged geometry and missing slots. */
export function decodeSearchOutcomes(
  value: unknown,
  plan: SearchPlan,
  options: SearchAdmissionOptions = {},
): SearchOutcomes {
  const envelope = object(value, ["contract", "planId", "plan", "outcomes"], "search outcomes");
  if (
    envelope.contract !== SEARCH_OUTCOMES_CONTRACT ||
    envelope.planId !== plan.id ||
    canonical(envelope.plan) !== canonical(plan)
  ) {
    throw new TypeError("search outcomes do not belong to this exact plan");
  }
  if (!Array.isArray(envelope.outcomes) || envelope.outcomes.length !== plan.slots.length) {
    throw new RangeError("search outcomes must account for every planned slot");
  }
  const seen = new Set<string>();
  const outcomes = envelope.outcomes.map((value): SearchOutcome => {
    const outcome = object(
      value,
      ["slot", "status", "elapsedMs", "result", "partial", "error", "reason"],
      "search outcome",
    );
    const slotRow = object(outcome.slot, Object.keys(plan.slots[0] ?? {}), "outcome slot");
    const slot = plan.slots.find((candidate) => candidate.id === slotRow.id);
    if (slot === undefined || canonical(slotRow) !== canonical(slot) || seen.has(slot.id)) {
      throw new RangeError("search outcome contains duplicate or mismatched slot");
    }
    seen.add(slot.id);
    if (
      typeof outcome.elapsedMs !== "number" ||
      !Number.isFinite(outcome.elapsedMs) ||
      outcome.elapsedMs < 0
    ) {
      throw new RangeError("outcome elapsed time must be finite and nonnegative");
    }
    if (outcome.status === "not-started") {
      object(value, ["slot", "status", "elapsedMs", "reason"], "not-started outcome");
      if (outcome.elapsedMs !== 0 || typeof outcome.reason !== "string") {
        throw new TypeError("not-started outcome needs zero elapsed time and a reason");
      }
      return {
        slot: structuredClone(slot),
        status: "not-started",
        elapsedMs: 0,
        reason: outcome.reason,
      };
    }
    if (outcome.status === "completed") {
      object(value, ["slot", "status", "elapsedMs", "result"], "completed outcome");
      return {
        slot: structuredClone(slot),
        status: "completed",
        elapsedMs: outcome.elapsedMs,
        result: decodeSearchTrialValue(
          outcome.result,
          slot,
          true,
          configurationFor(plan, slot.configurationId),
          options,
        ),
      };
    }
    if (
      outcome.status !== "failed" &&
      outcome.status !== "timed-out" &&
      outcome.status !== "cancelled"
    ) {
      throw new TypeError("unsupported search outcome status");
    }
    object(value, ["slot", "status", "elapsedMs", "partial", "error"], "interrupted outcome");
    if (typeof outcome.error !== "string") {
      throw new TypeError("unsuccessful outcome needs an error");
    }
    return {
      slot: structuredClone(slot),
      status: outcome.status,
      elapsedMs: outcome.elapsedMs,
      error: outcome.error,
      partial:
        outcome.partial === null
          ? null
          : decodeSearchTrialValue(
              outcome.partial,
              slot,
              false,
              configurationFor(plan, slot.configurationId),
              options,
            ),
    };
  });
  outcomes.sort((left, right) => left.slot.index - right.slot.index);
  return {
    contract: SEARCH_OUTCOMES_CONTRACT,
    planId: plan.id,
    plan: structuredClone(plan),
    outcomes,
  };
}
