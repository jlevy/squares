import assert from "node:assert/strict";
import { test } from "node:test";
import { createBrowserSearchPlan } from "../src/api/search-api.ts";
import { formatSearchSummary, searchRunFailure } from "../src/app/search-panel.ts";
import { createPackSearchRunner } from "../src/search/pack-runner.ts";
import { runSearchPlan, SearchObserverError } from "../src/search/scheduler.ts";
import type { SearchCohortSummary } from "../src/search/summary.ts";

function cohort(overrides: Partial<SearchCohortSummary>): SearchCohortSummary {
  return {
    cohortId: "exploratory-browser",
    configurationId: "browser-control",
    partition: "exploratory",
    n: 5,
    status: { completed: 2, failed: 0, timedOut: 0, cancelled: 1, notStarted: 0 },
    valid: 1,
    stationary: 0,
    rankable: 1,
    completionRate: { numerator: 2, denominator: 3, denominatorKind: "planned" },
    validityRate: { numerator: 1, denominator: 2, denominatorKind: "completed" },
    absoluteSides: [3.000691080660531],
    objectives: [3.000691080660531],
    work: {
      proposalAttempts: 3,
      physicsSteps: 240,
      repairIterations: 12,
      pairCandidates: 998,
      pairForces: 267,
      wallForces: 516,
      repairPairTests: 120,
      repairPairTranslations: 23,
      repairFitTranslations: 60,
    },
    best: null,
    blocks: [
      {
        block: 0,
        planned: 2,
        completed: 2,
        valid: 1,
        rankable: 1,
        bestObjective: 3.000691080660531,
        bestSlotId: "exploratory-browser:0",
      },
      {
        block: 1,
        planned: 1,
        completed: 0,
        valid: 0,
        rankable: 0,
        bestObjective: null,
        bestSlotId: null,
      },
    ],
    ...overrides,
  };
}

test("the Search summary line reports validity, stationarity, rank, work and block bests", () => {
  assert.deepEqual(formatSearchSummary([cohort({})]), [
    "exploratory n = 5: 1 of 2 completed valid, 0 stationary, 1 rankable; " +
      "240 physics steps, 12 repair iterations; " +
      "best objective by block: 3.000691 (block 0), none (block 1)",
  ]);
});

test("the Search summary gives each cohort its own line", () => {
  assert.deepEqual(
    formatSearchSummary([
      cohort({ partition: "tuning", n: 7, stationary: 2 }),
      cohort({
        partition: "held-out",
        n: 7,
        valid: 0,
        rankable: 0,
        validityRate: { numerator: 0, denominator: 0, denominatorKind: "completed" },
        work: { ...cohort({}).work, physicsSteps: 0, repairIterations: 0 },
        blocks: [],
      }),
    ]),
    [
      "tuning n = 7: 1 of 2 completed valid, 2 stationary, 1 rankable; " +
        "240 physics steps, 12 repair iterations; " +
        "best objective by block: 3.000691 (block 0), none (block 1)",
      "held-out n = 7: 0 of 0 completed valid, 0 stationary, 0 rankable; " +
        "0 physics steps, 0 repair iterations; best objective by block: none",
    ],
  );
});

test("an observer failure leaves the panel the outcomes collected so far", async () => {
  const plan = createBrowserSearchPlan({
    n: 1,
    seeds: [0, 1],
    physicsSteps: 1,
    proposal: "grid",
    repair: false,
  });
  const error: unknown = await runSearchPlan(plan, createPackSearchRunner({ batchSteps: 1 }), {
    now: () => 0,
    onOutcome: () => {
      throw new Error("redraw failed");
    },
  }).then(
    () => null,
    (failure: unknown) => failure,
  );
  assert.ok(error instanceof SearchObserverError, String(error));
  assert.deepEqual(searchRunFailure(error), {
    ledger: error.outcomes,
    message:
      "Search stopped: redraw failed. Export the ledger to keep its finished slots; resuming it runs the rest.",
  });
  assert.deepEqual(
    error.outcomes.outcomes.map(({ status }) => status),
    ["completed", "not-started"],
  );
  assert.deepEqual(searchRunFailure(new RangeError("bad seeds")), {
    ledger: null,
    message: "Search could not run: bad seeds",
  });
});
