import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { test } from "node:test";
import { fileURLToPath } from "node:url";
import { assessPackingSnapshot, mixUint32Seed } from "../src/core/runtime-contracts.ts";
import { decodeCorpus, frameAt } from "../src/data/corpus.ts";
import type { JsonObject } from "../src/search/contracts.ts";
import { decodeSearchOutcomes, encodeSearchOutcomes } from "../src/search/outcomes.ts";
import {
  createPackSearchRunner,
  decodePackSearchConfiguration,
  validatePackSearchPlan,
} from "../src/search/pack-runner.ts";
import { decodeSearchPlan } from "../src/search/registry.ts";
import { runSearchPlan } from "../src/search/scheduler.ts";
import { summarizeSearch } from "../src/search/summary.ts";
import { createRandomPackStart } from "../src/simulation/pack.ts";
import { resolvePacking } from "../src/simulation/resolve.ts";

function required<T>(value: T | undefined): T {
  assert.notEqual(value, undefined);
  if (value === undefined) {
    throw new Error("missing test fixture");
  }
  return value;
}

function configuration(overrides: Partial<JsonObject> = {}): JsonObject {
  return {
    contract: "packing.squares:PackSearchConfiguration/v1",
    seed_base: 99,
    proposal: { kind: "record-append", inflate: 1.1, grid_step: 1 },
    reference: "corpus",
    targets: "none",
    pair_law: { rigidity: 0.15, repulsion: 2_500, attraction: 0, range: 0 },
    wall_law: { rigidity: 0.25, repulsion: 2_500, attraction: 0, range: 0 },
    related_mask: null,
    physics: {
      steps_per_second: 120,
      omega: 10,
      zeta: 0.85,
      contact_damping: 20,
      contact_torque: 0.15,
      jiggle: 0,
      jiggle_torque: 0,
      jiggle_hz: [2.5, 4],
      max_speed: 40,
      max_spin: 20,
      cell: 1.5,
    },
    anneal: { amplitude: 0, decay_power: 1.5, tau: 2, floor: 0 },
    growth: { on: false, rate: 0.05, rule: "constant" },
    container: {
      squeeze_rate: 0,
      relax_rate: 0,
      squeeze_tolerance: 0.004,
      jam_tolerance: 0.06,
      minimum_side: 0.5,
    },
    stationarity: {
      linear_speed: 1e-6,
      angular_speed: 1e-6,
      forcing_scale: 1e-6,
      window: 2,
      stop: false,
    },
    repair: { kind: "resolve", tolerance: 1e-9 },
    objective: {
      kind: "absolute-side",
      state: "repaired",
      require_stationary: false,
    },
    ...overrides,
  };
}

function plan(
  config: JsonObject = configuration(),
  proposalAttempts = 4,
  { n = 2, physicsSteps = 2, repairIterations = 8 } = {},
) {
  return decodeSearchPlan({
    contract: "packing.squares:SearchPlan/v1",
    id: "pack-runner-control",
    source: { commit: "abc123", dirty: false, runtime: "node-test", engine: "pack/v1" },
    configurations: [{ id: "control", configuration: config }],
    cohorts: [
      {
        id: "tuning-control",
        configuration_id: "control",
        partition: "tuning",
        n,
        seeds: [7],
        block_size: 1,
        work_budget: {
          proposal_attempts: proposalAttempts,
          physics_steps: physicsSteps,
          repair_iterations: repairIterations,
        },
      },
    ],
  });
}

function corpus() {
  return decodeCorpus(
    JSON.parse(
      readFileSync(fileURLToPath(new URL("fixtures/corpus.json", import.meta.url)), "utf8"),
    ),
  );
}

test("ledger admission binds objectives, effective seeds and policies to the plan", async () => {
  const declared = plan();
  const envelope = await runSearchPlan(declared, createPackSearchRunner({ corpus: corpus() }));
  const outcome = required(envelope.outcomes[0]);
  assert.equal(outcome.status, "completed");
  if (outcome.status !== "completed") {
    throw new Error("expected completed trial");
  }
  assert.equal(outcome.result.objective, outcome.result.repaired?.absoluteSide);
  for (const forge of [
    (result: typeof outcome.result) => {
      result.objective = -999;
    },
    (result: typeof outcome.result) => {
      result.configuration.effective_seed = 0;
    },
    (result: typeof outcome.result) => {
      result.configuration.requested_seed = 999;
    },
    (result: typeof outcome.result) => {
      result.configuration.seed_base = 0;
    },
    (result: typeof outcome.result) => {
      result.selectedState = "raw";
    },
    (result: typeof outcome.result) => {
      result.stationarity.thresholds.linearSpeed = 100;
    },
  ]) {
    const changed = structuredClone(envelope);
    const changedOutcome = required(changed.outcomes[0]);
    if (changedOutcome.status !== "completed") {
      throw new Error("expected completed trial");
    }
    forge(changedOutcome.result);
    assert.throws(
      () => decodeSearchOutcomes(changed, declared),
      /disagrees|cannot carry a ranking objective/,
    );
    assert.throws(
      () => summarizeSearch(declared, changed),
      /disagrees|cannot carry a ranking objective/,
    );
    await assert.rejects(
      runSearchPlan(declared, createPackSearchRunner({ corpus: corpus() }), { resume: changed }),
      /disagrees|cannot carry a ranking objective/,
    );
  }
});

test("relative objectives require an independently supplied reference on import and replay", async () => {
  const source = corpus();
  const declared = plan(
    configuration({
      objective: { kind: "relative-excess", state: "repaired", require_stationary: false },
    }),
  );
  const admission = { referenceSide: (slot: { n: number }) => frameAt(source, slot.n).side };
  const envelope = await runSearchPlan(
    declared,
    createPackSearchRunner({ corpus: source }),
    admission,
  );
  const outcome = required(envelope.outcomes[0]);
  assert.equal(outcome.status, "completed");
  if (outcome.status !== "completed") {
    throw new Error("expected completed trial");
  }
  const absolute = required(outcome.result.repaired?.absoluteSide ?? undefined);
  const reference = frameAt(source, 2).side;
  assert.equal(outcome.result.objective, (absolute - reference) / reference);
  assert.throws(() => decodeSearchOutcomes(envelope, declared), /trusted corpus reference/);
  const encoded = encodeSearchOutcomes(envelope, admission);
  assert.equal(
    summarizeSearch(
      declared,
      decodeSearchOutcomes(JSON.parse(encoded), declared, admission),
      admission,
    )[0]?.rankable,
    1,
  );
  assert.throws(
    () => decodeSearchOutcomes(envelope, declared, { referenceSide: () => reference * 2 }),
    /objective disagrees/,
  );
});

test("Pack search declarations reject unsupported or variable-work semantics", () => {
  assert.throws(
    () => decodePackSearchConfiguration(configuration({ stationarity: { window: 2, stop: true } })),
    /stationarity.*stop=false/i,
  );
  assert.throws(
    () => decodePackSearchConfiguration(configuration({ repair: { kind: "none" } })),
    /repaired objective requires/i,
  );
  assert.throws(
    () => decodePackSearchConfiguration(configuration({ ignored: true })),
    /unsupported field ignored/,
  );
});

test("Pack search preflight checks corpus joins and proposal work before execution", () => {
  assert.throws(() => validatePackSearchPlan(plan(), {}), /decoded corpus/);
  assert.throws(
    () => validatePackSearchPlan(plan(configuration(), 3), { corpus: corpus() }),
    /proposal needs 4 attempts/,
  );
  validatePackSearchPlan(plan(), { corpus: corpus() });
});

test("Pack search retains raw, repaired and observed-best states with exact work and seeds", async () => {
  const context = { corpus: corpus() };
  // Pack samples its best state every 10 steps, so 30 steps sample it three times, and by the
  // end the pair has spread past the best sample: raw and best-observed are different states.
  const declared = plan(configuration(), 4, { physicsSteps: 30 });
  validatePackSearchPlan(declared, context);
  const envelope = await runSearchPlan(declared, createPackSearchRunner(context), {
    now: () => 0,
  });
  const outcome = envelope.outcomes[0];
  assert.equal(outcome?.status, "completed", JSON.stringify(outcome));
  if (outcome?.status !== "completed") {
    throw new Error("expected the Pack trial to complete");
  }
  const { result } = outcome;
  assert.equal(result.raw.snapshot.poses.length, 2);
  assert.equal(result.selectedState, "repaired");
  assert.equal(result.work.proposalAttempts, 4);
  assert.equal(result.work.physicsSteps, 30);
  assert.equal(result.configuration.requested_seed, 7);
  assert.equal(result.configuration.effective_seed, mixUint32Seed(99, 7));

  const best = required(result.bestObserved ?? undefined);
  assert.equal(best.valid, true);
  assert.equal(assessPackingSnapshot(best.snapshot, 2).valid, true);
  assert.notEqual(best.absoluteSide, result.raw.absoluteSide);

  // The repair receipt, work and state are exactly what Resolve does to the raw state.
  const resolve = resolvePacking(result.raw.snapshot, {
    expectedCount: 2,
    iterationLimit: 8,
    tolerance: 1e-9,
  });
  assert.deepEqual(result.repair, {
    termination: resolve.termination.reason,
    resolved: resolve.termination.resolved,
    exhausted: resolve.termination.exhausted,
    tolerance: 1e-9,
    iterationLimit: 8,
  });
  assert.deepEqual(
    {
      iterations: result.work.repairIterations,
      pairTests: result.work.repairPairTests,
      pairTranslations: result.work.repairPairTranslations,
      fitTranslations: result.work.repairFitTranslations,
    },
    resolve.work,
  );
  assert.ok(resolve.work.fitTranslations > 0, "Resolve did no work, so the receipt proves little");
  const repaired = required(result.repaired ?? undefined);
  assert.notStrictEqual(result.raw.snapshot, repaired.snapshot);
  assert.deepEqual(repaired.snapshot, resolve.repaired?.snapshot);

  // The objective is the repaired state's side, measured here, which best-observed is not.
  const side = assessPackingSnapshot(repaired.snapshot, 2).requiredSide;
  assert.equal(result.objective, side);
  assert.notEqual(best.absoluteSide, side);
});

test("Pack Search yields to timer cancellation and retains partial physics work", async () => {
  const declared = plan(configuration({ proposal: { kind: "grid" } }), 1);
  required(declared.slots[0]).workBudget.physicsSteps = 1_000;
  const controller = new AbortController();
  let yields = 0;
  const runner = createPackSearchRunner({
    corpus: corpus(),
    batchSteps: 1,
    yieldControl: async () => {
      yields += 1;
      if (yields === 2) {
        await new Promise<void>((resolve) =>
          globalThis.setTimeout(() => {
            controller.abort();
            resolve();
          }, 0),
        );
      }
    },
  });
  const ledger = await runSearchPlan(declared, runner, { signal: controller.signal });
  const outcome = ledger.outcomes[0];
  assert.equal(outcome?.status, "cancelled");
  if (outcome?.status !== "cancelled") {
    throw new Error("expected cancellation");
  }
  assert.equal(outcome.partial?.work.physicsSteps, 1);
  assert.equal(outcome.partial?.work.repairIterations, 0);
  assert.deepEqual(outcome.partial?.repair, {
    termination: "cancelled",
    resolved: false,
    exhausted: false,
    tolerance: 1e-9,
    iterationLimit: 8,
  });
});

test("Pack Search receipts do not depend on cooperative batch size", async () => {
  // Five squares dropped at random into a side of 2.5 overlap: Pack pushes them apart for 45
  // steps and Resolve still has to iterate, so every batch boundary lands mid-motion.
  const declared = plan(
    configuration({ reference: "none", proposal: { kind: "random", container_side: 2.5 } }),
    1,
    { n: 5, physicsSteps: 45, repairIterations: 64 },
  );
  const execute = (batchSteps: number) =>
    runSearchPlan(
      declared,
      createPackSearchRunner({ batchSteps, yieldControl: () => Promise.resolve() }),
      { now: () => 0 },
    );
  const single = await execute(1);
  const outcome = single.outcomes[0];
  assert.equal(outcome?.status, "completed", JSON.stringify(outcome));
  if (outcome?.status !== "completed") {
    throw new Error("expected the Pack trial to complete");
  }
  const start = createRandomPackStart(5, 2.5, mixUint32Seed(99, 7));
  assert.notDeepEqual(outcome.result.raw.snapshot.poses, start.poses);
  assert.ok(outcome.result.work.pairForces > 0, "Pack did not move the squares");
  assert.equal(outcome.result.raw.valid, false);
  assert.equal(outcome.result.repair.termination, "resolved");
  assert.ok(outcome.result.work.repairIterations > 1, "Resolve did not iterate");
  for (const batchSteps of [7, 32]) {
    assert.deepEqual(await execute(batchSteps), single, `batch size ${batchSteps}`);
  }
});
