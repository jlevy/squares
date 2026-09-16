import assert from "node:assert/strict";
import { test } from "node:test";
import { measurePackingGeometry } from "../src/core/geometry.ts";
import type { PackingSnapshot } from "../src/core/runtime-contracts.ts";
import type {
  JsonObject,
  SearchOutcomes,
  SearchPlan,
  SearchSlot,
  SearchTrialControl,
  SearchTrialValue,
} from "../src/search/contracts.ts";
import {
  decodeSearchOutcomes,
  encodeSearchOutcomes,
  statusCounts,
} from "../src/search/outcomes.ts";
import { decodeSearchPlan } from "../src/search/registry.ts";
import { runSearchPlan, SearchObserverError } from "../src/search/scheduler.ts";
import { summarizeSearch } from "../src/search/summary.ts";

function required<T>(value: T | undefined): T {
  assert.notEqual(value, undefined);
  if (value === undefined) {
    throw new Error("missing test fixture");
  }
  return value;
}

function plan(seeds: number[] = [0, 1, 2, 3, 4]): SearchPlan {
  return decodeSearchPlan({
    contract: "packing.squares:SearchPlan/v1",
    id: "scheduler-control",
    source: { commit: "abc123", dirty: false, runtime: "node-test", engine: "pack/v1" },
    configurations: [
      {
        id: "control",
        configuration: {
          mode: "blind",
          objective: { kind: "absolute-side", state: "best-observed", require_stationary: false },
        },
      },
    ],
    cohorts: [
      {
        id: "tuning-control",
        configuration_id: "control",
        partition: "tuning",
        n: 1,
        seeds,
        block_size: 2,
        work_budget: {
          proposal_attempts: 1,
          physics_steps: 4,
          repair_iterations: 0,
        },
        timeout_ms: 5,
      },
      {
        id: "held-out-control",
        configuration_id: "control",
        partition: "held-out",
        n: 1,
        seeds: [100],
        block_size: 1,
        work_budget: {
          proposal_attempts: 1,
          physics_steps: 4,
          repair_iterations: 0,
        },
      },
    ],
  });
}

function completed(configuration: JsonObject): SearchTrialValue {
  const state = {
    snapshot: {
      squareSide: 1,
      container: { originX: 0, originY: 0, side: 1 },
      poses: [{ x: 0.5, y: 0.5, angle: 0 }],
    },
    valid: true,
    validityReason: null,
    absoluteSide: 1,
  } as const;
  return {
    raw: state,
    repaired: null,
    bestObserved: state,
    selectedState: "best-observed",
    stationarity: {
      stationary: true,
      stationarySteps: 1,
      window: 1,
      residual: { maxLinearSpeed: 0, maxAngularSpeed: 0 },
      forcingScale: 0,
      thresholds: { linearSpeed: 0, angularSpeed: 0, forcingScale: 0 },
    },
    repair: {
      termination: "not-requested",
      resolved: false,
      exhausted: false,
      tolerance: null,
      iterationLimit: 0,
    },
    objective: 1,
    work: {
      proposalAttempts: 1,
      physicsSteps: 4,
      repairIterations: 0,
      pairCandidates: 0,
      pairForces: 0,
      wallForces: 0,
      repairPairTests: 0,
      repairPairTranslations: 0,
      repairFitTranslations: 0,
    },
    configuration,
  };
}

test("the registry derives ordered disjoint blocks without pooling held-out slots", () => {
  const decoded = plan();
  assert.deepEqual(
    decoded.slots.map(({ partition, seed, block, positionInBlock }) => ({
      partition,
      seed,
      block,
      positionInBlock,
    })),
    [
      { partition: "tuning", seed: 0, block: 0, positionInBlock: 0 },
      { partition: "tuning", seed: 1, block: 0, positionInBlock: 1 },
      { partition: "tuning", seed: 2, block: 1, positionInBlock: 0 },
      { partition: "tuning", seed: 3, block: 1, positionInBlock: 1 },
      { partition: "tuning", seed: 4, block: 2, positionInBlock: 0 },
      { partition: "held-out", seed: 100, block: 0, positionInBlock: 0 },
    ],
  );
});

test("the scheduler retains completed, failed, timeout, cancellation and pending slots", async () => {
  let clock = 0;
  const controller = new AbortController();
  const seen: string[] = [];
  const outcomes = await runSearchPlan(
    plan(),
    (
      slot: SearchSlot,
      configuration: JsonObject,
      control: SearchTrialControl,
    ): SearchTrialValue => {
      if (slot.seed === 1) {
        throw new Error("deliberate failure");
      }
      if (slot.seed === 2) {
        clock = 10;
        assert.equal(control.cancellationReason(), "timed-out");
      }
      if (slot.seed === 3) {
        controller.abort();
        assert.equal(control.cancellationReason(), "cancelled");
      }
      return completed(configuration);
    },
    {
      concurrency: 1,
      signal: controller.signal,
      now: () => clock,
      yieldControl: () => Promise.resolve(),
      onOutcome: (outcome) => {
        seen.push(outcome.status);
      },
    },
  );
  assert.deepEqual(
    outcomes.outcomes.map(({ status }) => status),
    ["completed", "failed", "timed-out", "cancelled", "not-started", "not-started"],
  );
  assert.deepEqual(statusCounts(outcomes.outcomes), {
    completed: 1,
    failed: 1,
    timedOut: 1,
    cancelled: 1,
    notStarted: 2,
  });
  assert.deepEqual(seen, [
    "completed",
    "failed",
    "timed-out",
    "cancelled",
    "not-started",
    "not-started",
  ]);
  assert.match(encodeSearchOutcomes(outcomes), /"planId": "scheduler-control"/);
  const summaries = summarizeSearch(plan(), outcomes);
  assert.equal(summaries[0]?.partition, "tuning");
  assert.deepEqual(summaries[0]?.completionRate, {
    numerator: 1,
    denominator: 5,
    denominatorKind: "planned",
  });
  assert.equal(summaries[0]?.blocks[0]?.bestObjective, 1);
  assert.equal(summaries[0]?.blocks[1]?.bestObjective, null);
  assert.equal(summaries[1]?.partition, "held-out");
  assert.equal(summaries[1]?.status.notStarted, 1);
});

test("fixed physics work and validity are admission conditions", async () => {
  // The plan gives each slot 5 ms; a fixed clock keeps a loaded machine from timing it out first.
  const short = await runSearchPlan(
    plan([0]),
    (_slot, configuration) => {
      const result = completed(configuration);
      return { ...result, work: { ...result.work, physicsSteps: 3 } };
    },
    { now: () => 0 },
  );
  assert.equal(short.outcomes[0]?.status, "failed");

  const invalidRank = await runSearchPlan(
    plan([0]),
    (_slot, configuration) => ({
      ...completed(configuration),
      raw: {
        ...completed(configuration).raw,
        valid: false,
        validityReason: "pair-overlap",
      },
      selectedState: "raw",
    }),
    { now: () => 0 },
  );
  assert.equal(invalidRank.outcomes[0]?.status, "failed");
});

test("the registry rejects ambiguous or non-replayable plans", () => {
  const raw = {
    contract: "packing.squares:SearchPlan/v1",
    id: "bad",
    source: { commit: "abc123", dirty: false, runtime: "node-test", engine: "pack/v1" },
    configurations: [{ id: "control", configuration: { value: Number.NaN } }],
    cohorts: [],
  };
  assert.throws(() => decodeSearchPlan(raw), /finite/);
  assert.throws(
    () =>
      decodeSearchPlan({
        ...raw,
        configurations: [{ id: "control", configuration: {} }],
        cohorts: [
          {
            id: "bad-reference",
            configuration_id: "missing",
            partition: "tuning",
            n: 1,
            seeds: [0],
            block_size: 1,
            work_budget: {
              proposal_attempts: 0,
              physics_steps: 1,
              repair_iterations: 0,
            },
          },
        ],
      }),
    /unknown configuration/,
  );
});

test("persisted ledgers keep completed and failed slots, reclaim the rest, and reject changed plans", async () => {
  const declared = plan([0, 1, 2]);
  const controller = new AbortController();
  let clock = 0;
  const first = await runSearchPlan(
    declared,
    (slot, configuration) => {
      if (slot.seed === 1) {
        throw new Error("deliberate failure");
      }
      if (slot.seed === 2) {
        clock = 10;
      }
      return completed(configuration);
    },
    {
      now: () => clock,
      signal: controller.signal,
      onOutcome: (outcome) => {
        if (outcome.status === "timed-out") {
          controller.abort();
        }
      },
    },
  );
  assert.deepEqual(
    first.outcomes.map(({ status }) => status),
    ["completed", "failed", "timed-out", "not-started"],
  );
  const decoded = decodeSearchOutcomes(JSON.parse(encodeSearchOutcomes(first)), declared);
  const visited: number[] = [];
  const resumed = await runSearchPlan(
    declared,
    (slot, configuration) => {
      visited.push(slot.seed);
      return completed(configuration);
    },
    { resume: decoded, now: () => 0 },
  );
  assert.deepEqual(visited, [2, 100]);
  assert.deepEqual(resumed.outcomes[0], first.outcomes[0]);
  assert.deepEqual(resumed.outcomes[1], first.outcomes[1]);
  assert.deepEqual(
    resumed.outcomes.map(({ status }) => status),
    ["completed", "failed", "completed", "completed"],
  );
  const changed = structuredClone(declared);
  required(changed.configurations[0]).configuration.mode = "changed";
  assert.throws(() => decodeSearchOutcomes(first, changed), /exact plan/);
  const forged = structuredClone(resumed);
  required(forged.outcomes[0]).slot.block = 99;
  assert.throws(() => summarizeSearch(declared, forged), /mismatched slot/);
});

test("resume finishes a slot that was cancelled mid-run", async () => {
  const declared = plan([0, 1]);
  const controller = new AbortController();
  const first = await runSearchPlan(
    declared,
    (_slot, configuration, control) => {
      controller.abort();
      assert.equal(control.cancellationReason(), "cancelled");
      return completed(configuration);
    },
    { now: () => 0, signal: controller.signal },
  );
  assert.deepEqual(
    first.outcomes.map(({ status }) => status),
    ["cancelled", "not-started", "not-started"],
  );
  const visit = async (resume: SearchOutcomes) => {
    const visited: number[] = [];
    const ledger = await runSearchPlan(
      declared,
      (slot, configuration) => {
        visited.push(slot.seed);
        return completed(configuration);
      },
      {
        resume: decodeSearchOutcomes(JSON.parse(encodeSearchOutcomes(resume)), declared),
        now: () => 0,
      },
    );
    return { visited, ledger };
  };
  const resumed = await visit(first);
  assert.deepEqual(resumed.visited, [0, 1, 100]);
  assert.deepEqual(
    resumed.ledger.outcomes.map(({ status }) => status),
    ["completed", "completed", "completed"],
  );
  for (const summary of summarizeSearch(declared, resumed.ledger)) {
    assert.equal(summary.completionRate.numerator, summary.completionRate.denominator);
  }
  const again = await visit(resumed.ledger);
  assert.deepEqual(again.visited, []);
  assert.deepEqual(again.ledger, resumed.ledger);
});

test("ledger admission recomputes geometry and refuses missing work and unknown status", async () => {
  const declared = plan([0]);
  const ledger = await runSearchPlan(declared, (_slot, configuration) => completed(configuration), {
    now: () => 0,
  });
  const mutate = (change: (value: Record<string, unknown>) => void) => {
    const value: Record<string, unknown> = JSON.parse(encodeSearchOutcomes(ledger));
    change(value);
    return value;
  };
  assert.throws(
    () =>
      decodeSearchOutcomes(
        mutate((value) => {
          const entries = value.outcomes as Array<{ status: string }>;
          required(entries[0]).status = "success";
        }),
        declared,
      ),
    /unsupported.*status/,
  );
  const forged = structuredClone(ledger);
  const first = forged.outcomes[0];
  assert.equal(first?.status, "completed");
  if (first?.status !== "completed") {
    throw new Error("missing trial");
  }
  required(first.result.raw.snapshot.poses[0]).x = 100;
  assert.throws(() => decodeSearchOutcomes(forged, declared), /validity disagrees/);
  assert.throws(
    () =>
      decodeSearchOutcomes(
        mutate((value) => {
          const entries = value.outcomes as Array<{ result: { work: Record<string, unknown> } }>;
          delete entries[0]?.result.work.physicsSteps;
        }),
        declared,
      ),
    /physicsSteps/,
  );
});

function singleSlotPlan(n: number): SearchPlan {
  return decodeSearchPlan({
    contract: "packing.squares:SearchPlan/v1",
    id: `forgery-n${n}`,
    source: { commit: "abc123", dirty: false, runtime: "node-test", engine: "pack/v1" },
    configurations: [
      {
        id: "control",
        configuration: {
          mode: "blind",
          objective: { kind: "absolute-side", state: "best-observed", require_stationary: false },
        },
      },
    ],
    cohorts: [
      {
        id: "forgery",
        configuration_id: "control",
        partition: "tuning",
        n,
        seeds: [0],
        block_size: 1,
        work_budget: { proposal_attempts: 1, physics_steps: 4, repair_iterations: 0 },
      },
    ],
  });
}

/** A trial that claims `snapshot` is a valid packing, with every field a forger can compute. */
function claimedValid(configuration: JsonObject, snapshot: PackingSnapshot): SearchTrialValue {
  const side = measurePackingGeometry(snapshot).requiredSide;
  const state = { snapshot, valid: true, validityReason: null, absoluteSide: side };
  return { ...completed(configuration), raw: state, bestObserved: state, objective: side };
}

function grid(columns: number, base: number, squareSide = 1): PackingSnapshot {
  return {
    squareSide,
    container: { originX: base, originY: base, side: columns * squareSide },
    poses: Array.from({ length: columns * columns }, (_unused, index) => ({
      x: base + ((index % columns) + 0.5) * squareSide,
      y: base + (Math.floor(index / columns) + 0.5) * squareSide,
      angle: 0,
    })),
  };
}

test("ledger admission refuses forged geometry at any magnitude, rotation or square size", async () => {
  // Integers near 2^52 are exact, but a centre +- 0.5 rounds to one of them, so this grid of
  // touching squares reads with no overlap and a side of 2.
  const far = 2 ** 52 + 2;
  const forgeries: ReadonlyArray<{
    name: string;
    honest: PackingSnapshot;
    forged: PackingSnapshot;
  }> = [
    {
      name: "a 3 by 3 grid at 2^52 whose side reads 2",
      honest: grid(3, 0),
      forged: {
        squareSide: 1,
        container: { originX: far, originY: far, side: 2 },
        poses: Array.from({ length: 9 }, (_unused, index) => ({
          x: far + (index % 3),
          y: far + Math.floor(index / 3),
          angle: 0,
        })),
      },
    },
    {
      name: "one square at 1e17 whose side reads 0",
      honest: grid(1, 0),
      forged: {
        squareSide: 1,
        container: { originX: 1e17, originY: 1e17, side: 1 },
        poses: [{ x: 1e17, y: 1e17, angle: 0 }],
      },
    },
    {
      name: "two squares 5e-6 into each other",
      honest: grid(2, 0),
      forged: {
        ...grid(2, 0),
        poses: grid(2, 0).poses.map((pose, index) =>
          index === 1 ? { ...pose, x: pose.x - 5e-6 } : pose,
        ),
      },
    },
    {
      name: "a rotated square's corner 2e-9 into its neighbour",
      honest: grid(2, 0),
      forged: {
        squareSide: 1,
        container: { originX: 0, originY: 0, side: 3 },
        poses: [
          { x: 1, y: 1, angle: Math.PI / 4 },
          { x: 2.2071067791865473, y: 1, angle: 0 },
          { x: 0.5, y: 2.5, angle: 0 },
          { x: 2.5, y: 2.5, angle: 0 },
        ],
      },
    },
    { name: "half-size squares", honest: grid(2, 0), forged: grid(2, 0, 0.5) },
  ];
  for (const { name, honest, forged } of forgeries) {
    const n = honest.poses.length;
    const declared = singleSlotPlan(n);
    const ledger = await runSearchPlan(
      declared,
      (_slot, configuration) => claimedValid(configuration, honest),
      { now: () => 0 },
    );
    assert.equal(ledger.outcomes[0]?.status, "completed", `${name}: honest control`);
    const forgedLedger = structuredClone(ledger);
    const outcome = required(forgedLedger.outcomes[0]);
    if (outcome.status !== "completed") {
      throw new Error("expected a completed control");
    }
    const configuration = outcome.result.configuration;
    outcome.result = claimedValid(configuration, forged);
    assert.throws(() => decodeSearchOutcomes(forgedLedger, declared), /validity disagrees/, name);
    assert.throws(() => summarizeSearch(declared, forgedLedger), /validity disagrees/, name);
    await assert.rejects(
      runSearchPlan(declared, (_slot, again) => claimedValid(again, honest), {
        resume: forgedLedger,
        now: () => 0,
      }),
      /validity disagrees/,
      name,
    );
    const direct = await runSearchPlan(declared, (_slot, again) => claimedValid(again, forged), {
      now: () => 0,
    });
    assert.equal(direct.outcomes[0]?.status, "failed", name);
  }
});

test("no observed valid packing completes with a null objective rather than failing", async () => {
  const ledger = await runSearchPlan(
    plan([0]),
    (_slot, configuration) => ({
      ...completed(configuration),
      bestObserved: null,
      objective: null,
    }),
    { now: () => 0 },
  );
  assert.equal(ledger.outcomes[0]?.status, "completed");
  const summary = summarizeSearch(plan([0]), ledger);
  assert.equal(summary[0]?.rankable, 0);
  assert.equal(summary[0]?.valid, 0);
});

test("observer failure waits for active runners, then rejects with the outcomes so far", async () => {
  let active = 0;
  let sawCancellation = false;
  const declared = plan([0, 1, 2]);
  const failure: unknown = await runSearchPlan(
    declared,
    async (slot, configuration, control) => {
      active += 1;
      if (slot.seed === 1) {
        await new Promise<void>((resolve) => globalThis.setTimeout(resolve, 0));
        sawCancellation = control.cancellationReason() === "cancelled";
      }
      active -= 1;
      return completed(configuration);
    },
    {
      concurrency: 2,
      now: () => 0,
      onOutcome: () => {
        throw new Error("ledger write failed");
      },
    },
  ).then(
    () => null,
    (error: unknown) => error,
  );
  assert.equal(active, 0);
  assert.equal(sawCancellation, true);
  assert.ok(failure instanceof SearchObserverError, String(failure));
  assert.match(failure.message, /ledger write failed/);
  const carried = failure.outcomes;
  assert.deepEqual(
    carried.outcomes.map(({ slot, status }) => [slot.seed, status]),
    [
      [0, "completed"],
      [1, "cancelled"],
      [2, "not-started"],
      [100, "not-started"],
    ],
  );
  assert.deepEqual(
    decodeSearchOutcomes(JSON.parse(encodeSearchOutcomes(carried)), declared),
    carried,
  );
  const visited: number[] = [];
  const resumed = await runSearchPlan(
    declared,
    (slot, configuration) => {
      visited.push(slot.seed);
      return completed(configuration);
    },
    { resume: carried, now: () => 0 },
  );
  assert.deepEqual(visited, [1, 2, 100]);
  assert.deepEqual(resumed.outcomes[0], carried.outcomes[0]);
});

/** A trial whose repair Resolve reported as already valid, with every flag consistent. */
function repairedTrial(configuration: JsonObject): SearchTrialValue {
  const base = completed(configuration);
  return {
    ...base,
    repaired: base.raw,
    repair: {
      termination: "already-valid",
      resolved: true,
      exhausted: false,
      tolerance: 1e-9,
      iterationLimit: 0,
    },
  };
}

test("ledger admission accepts only Resolve's terminations with consistent flags", async () => {
  const declared = plan([0]);
  const forgeries: ReadonlyArray<{
    name: string;
    base: (configuration: JsonObject) => SearchTrialValue;
    forge: (repair: Record<string, unknown>) => void;
  }> = [
    {
      name: "an unknown termination",
      base: completed,
      forge: (repair) => {
        repair.termination = "succeeded";
      },
    },
    {
      name: "no repair requested, with a tolerance",
      base: completed,
      forge: (repair) => {
        repair.tolerance = 1e-9;
      },
    },
    {
      name: "a Resolve termination without a tolerance",
      base: repairedTrial,
      forge: (repair) => {
        repair.tolerance = null;
      },
    },
    {
      name: "a resolving termination not marked resolved",
      base: repairedTrial,
      forge: (repair) => {
        repair.resolved = false;
      },
    },
    {
      name: "a stall marked resolved",
      base: repairedTrial,
      forge: (repair) => {
        repair.termination = "stalled";
      },
    },
    {
      name: "no repair requested, marked resolved",
      base: repairedTrial,
      forge: (repair) => {
        repair.termination = "not-requested";
        repair.tolerance = null;
      },
    },
    {
      name: "budget exhaustion not marked exhausted",
      base: repairedTrial,
      forge: (repair) => {
        repair.termination = "budget-exhausted";
        repair.resolved = false;
      },
    },
    {
      name: "a stall marked exhausted",
      base: repairedTrial,
      forge: (repair) => {
        repair.termination = "stalled";
        repair.resolved = false;
        repair.exhausted = true;
      },
    },
  ];
  for (const { name, base, forge } of forgeries) {
    const ledger = await runSearchPlan(declared, (_slot, configuration) => base(configuration), {
      now: () => 0,
    });
    assert.equal(ledger.outcomes[0]?.status, "completed", `${name}: honest control`);
    const forged = structuredClone(ledger);
    const outcome = required(forged.outcomes[0]);
    if (outcome.status !== "completed") {
      throw new Error("expected a completed control");
    }
    forge(outcome.result.repair as unknown as Record<string, unknown>);
    assert.throws(() => decodeSearchOutcomes(forged, declared), /repair/, name);
    const direct = await runSearchPlan(
      declared,
      (_slot, configuration) => {
        const trial = base(configuration);
        forge(trial.repair as unknown as Record<string, unknown>);
        return trial;
      },
      { now: () => 0 },
    );
    assert.equal(direct.outcomes[0]?.status, "failed", name);
  }
});
