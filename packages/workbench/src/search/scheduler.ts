import {
  SEARCH_OUTCOMES_CONTRACT,
  type SearchCancellationReason,
  type SearchInterruptedOutcome,
  type SearchNotStartedOutcome,
  type SearchOutcome,
  type SearchOutcomes,
  type SearchPlan,
  type SearchSlot,
  type SearchTrialControl,
  type SearchTrialRunner,
  type SearchTrialValue,
} from "./contracts.ts";
import { decodeSearchOutcomes } from "./outcomes.ts";
import { configurationFor } from "./registry.ts";
import { decodeSearchTrialValue, type SearchAdmissionOptions } from "./validation.ts";

export interface SearchSchedulerOptions extends SearchAdmissionOptions {
  concurrency?: number;
  /**
   * Continue a saved ledger for the same plan. Completed and failed slots are kept as they are;
   * cancelled, timed-out and not-started slots are claimed and run again, so a resumed plan can
   * reach a completion rate of 1.
   */
  resume?: SearchOutcomes;
  signal?: AbortSignal;
  now?: () => number;
  yieldControl?: () => Promise<void>;
  onOutcome?: (outcome: SearchOutcome) => void | Promise<void>;
}

function elapsed(now: () => number, began: number): number {
  return Math.max(0, now() - began);
}

function errorText(error: unknown): string {
  return error instanceof Error ? error.message : String(error);
}

/**
 * The `onOutcome` observer threw, so the run stopped early.
 *
 * `outcomes` is still a complete ledger for the plan: every outcome recorded before the run
 * stopped, including the one the observer failed on, and `not-started` for every other slot. It
 * can be exported and resumed like any other ledger.
 */
export class SearchObserverError extends Error {
  readonly outcomes: SearchOutcomes;

  constructor(cause: unknown, outcomes: SearchOutcomes) {
    super(errorText(cause), { cause });
    this.name = "SearchObserverError";
    this.outcomes = outcomes;
  }
}

function notStarted(slot: SearchSlot, reason: string): SearchNotStartedOutcome {
  return { slot, status: "not-started", elapsedMs: 0, reason };
}

function interrupted(
  slot: SearchSlot,
  reason: SearchCancellationReason,
  elapsedMs: number,
  partial: SearchTrialValue | null,
): SearchInterruptedOutcome {
  return {
    slot,
    status: reason,
    elapsedMs,
    error: reason === "cancelled" ? "search cancelled during trial" : "trial deadline elapsed",
    partial,
  };
}

/**
 * Run a deterministic slot plan with bounded concurrency.
 *
 * Trial runners must poll `cancellationReason()` while doing work. This avoids a
 * Promise-race timeout leaving an unobserved simulation alive after its slot was
 * reported terminal. Pending slots remain explicit `not-started` outcomes.
 *
 * If `onOutcome` throws, no further slot is claimed, active runners are told to cancel and are
 * waited for, and the run rejects with a `SearchObserverError` carrying the ledger so far.
 */
export async function runSearchPlan(
  declaredPlan: SearchPlan,
  runner: SearchTrialRunner,
  options: SearchSchedulerOptions = {},
): Promise<SearchOutcomes> {
  const plan = structuredClone(declaredPlan);
  const concurrency = options.concurrency ?? 1;
  if (!Number.isSafeInteger(concurrency) || concurrency < 1 || concurrency > 64) {
    throw new RangeError("search concurrency must be an integer from 1 to 64");
  }
  const now = options.now ?? performance.now.bind(performance);
  const yieldControl =
    options.yieldControl ??
    (() => new Promise<void>((resolve) => globalThis.setTimeout(resolve, 0)));
  const outcomes: Array<SearchOutcome | undefined> = Array.from({ length: plan.slots.length });
  if (options.resume !== undefined) {
    const previous = decodeSearchOutcomes(options.resume, plan, options);
    for (const outcome of previous.outcomes) {
      if (outcome.status === "completed" || outcome.status === "failed") {
        outcomes[outcome.slot.index] = outcome;
      }
    }
  }
  let nextIndex = 0;
  let observerFailed = false;
  let observerError: unknown = null;

  const record = async (outcome: SearchOutcome): Promise<void> => {
    outcomes[outcome.slot.index] = outcome;
    try {
      await options.onOutcome?.(structuredClone(outcome));
    } catch (error: unknown) {
      if (!observerFailed) {
        observerFailed = true;
        observerError = error;
      }
      throw error;
    }
  };

  /** The ledger as it stands, with every slot not yet recorded marked not-started. */
  const envelope = (missing: string): SearchOutcomes => ({
    contract: SEARCH_OUTCOMES_CONTRACT,
    planId: plan.id,
    plan: structuredClone(plan),
    outcomes: plan.slots.map((slot) => outcomes[slot.index] ?? notStarted(slot, missing)),
  });
  const observerStopped = (): SearchObserverError =>
    new SearchObserverError(
      observerError,
      envelope("search stopped when an outcome observer failed"),
    );

  const claim = (): SearchSlot | null => {
    while (nextIndex < plan.slots.length && outcomes[nextIndex] !== undefined) {
      nextIndex += 1;
    }
    if (observerFailed || options.signal?.aborted === true || nextIndex >= plan.slots.length) {
      return null;
    }
    const slot = plan.slots[nextIndex];
    nextIndex += 1;
    if (slot === undefined) {
      throw new RangeError("search plan slot index is inconsistent");
    }
    return slot;
  };

  const worker = async (): Promise<void> => {
    for (let slot = claim(); slot !== null; slot = claim()) {
      const began = now();
      const deadline = slot.timeoutMs === null ? null : began + slot.timeoutMs;
      const control: SearchTrialControl = {
        cancellationReason: () => {
          if (observerFailed || options.signal?.aborted === true) {
            return "cancelled";
          }
          if (deadline !== null && now() >= deadline) {
            return "timed-out";
          }
          return null;
        },
      };
      let outcome: SearchOutcome;
      try {
        const result = await runner(
          structuredClone(slot),
          structuredClone(configurationFor(plan, slot.configurationId)),
          control,
        );
        const cancellation = control.cancellationReason();
        if (cancellation !== null) {
          outcome = interrupted(
            slot,
            cancellation,
            elapsed(now, began),
            decodeSearchTrialValue(
              result,
              slot,
              false,
              configurationFor(plan, slot.configurationId),
              options,
            ),
          );
        } else {
          outcome = {
            slot,
            status: "completed",
            elapsedMs: elapsed(now, began),
            result: decodeSearchTrialValue(
              result,
              slot,
              true,
              configurationFor(plan, slot.configurationId),
              options,
            ),
          };
        }
      } catch (error: unknown) {
        const cancellation = control.cancellationReason();
        outcome =
          cancellation === null
            ? {
                slot,
                status: "failed",
                elapsedMs: elapsed(now, began),
                error: errorText(error),
                partial: null,
              }
            : interrupted(slot, cancellation, elapsed(now, began), null);
      }
      await record(outcome);
      await yieldControl();
    }
  };

  const workers = await Promise.allSettled(
    Array.from({ length: Math.min(concurrency, plan.slots.length) }, worker),
  );
  if (observerFailed) {
    throw observerStopped();
  }
  for (const result of workers) {
    if (result.status === "rejected") {
      throw result.reason;
    }
  }
  const unclaimed =
    options.signal?.aborted === true
      ? "search cancelled before trial started"
      : "trial was not claimed";
  for (const slot of plan.slots) {
    if (outcomes[slot.index] !== undefined) {
      continue;
    }
    try {
      await record(notStarted(slot, unclaimed));
    } catch {
      throw observerStopped();
    }
  }
  return envelope(unclaimed);
}
