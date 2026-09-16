import assert from "node:assert/strict";
import { test } from "node:test";
import {
  browserSearchSource,
  createBrowserSearchPlan,
  parseBrowserSearchSeeds,
} from "../src/api/search-api.ts";
import { PACKING_VALIDITY } from "../src/core/runtime-contracts.ts";
import { decodeSearchOutcomes, encodeSearchOutcomes } from "../src/search/outcomes.ts";
import { createPackSearchRunner } from "../src/search/pack-runner.ts";
import { runSearchPlan } from "../src/search/scheduler.ts";

test("browser search plans are deterministic and runnable without corpus", async () => {
  const inputs = { n: 2, seeds: [3, 4], physicsSteps: 2, proposal: "grid", repair: false } as const;
  const plan = createBrowserSearchPlan(inputs);
  assert.deepEqual(plan, createBrowserSearchPlan(inputs));
  assert.equal(plan.cohorts[0]?.partition, "exploratory");
  const ledger = await runSearchPlan(plan, createPackSearchRunner({ batchSteps: 1 }));
  assert.deepEqual(
    ledger.outcomes.map((outcome) => outcome.status),
    ["completed", "completed"],
  );
  assert.deepEqual(decodeSearchOutcomes(JSON.parse(encodeSearchOutcomes(ledger)), plan), ledger);
  assert.throws(
    () =>
      decodeSearchOutcomes(
        JSON.parse(encodeSearchOutcomes(ledger)),
        createBrowserSearchPlan({ ...inputs, physicsSteps: 3 }),
      ),
    /plan/i,
  );
});

test("the browser repair option runs Resolve and ranks the repaired state", async () => {
  const plain = createBrowserSearchPlan({
    n: 5,
    seeds: [0, 1],
    physicsSteps: 100,
    proposal: "grid",
    repair: false,
  });
  assert.deepEqual(plain.configurations[0]?.configuration.objective, {
    kind: "absolute-side",
    state: "best-observed",
    require_stationary: false,
  });
  const plan = createBrowserSearchPlan({
    n: 5,
    seeds: [0, 1],
    physicsSteps: 100,
    proposal: "grid",
    repair: true,
  });
  assert.deepEqual(plan.configurations[0]?.configuration.repair, {
    kind: "resolve",
    tolerance: PACKING_VALIDITY.penetrationTolerance,
  });
  assert.deepEqual(plan.configurations[0]?.configuration.objective, {
    kind: "absolute-side",
    state: "repaired",
    require_stationary: false,
  });
  const ledger = await runSearchPlan(plan, createPackSearchRunner({ batchSteps: 32 }), {
    now: () => 0,
  });
  assert.deepEqual(
    ledger.outcomes.map((outcome) => outcome.status),
    ["completed", "completed"],
  );
  let ranked = 0;
  for (const outcome of ledger.outcomes) {
    if (outcome.status !== "completed") {
      throw new Error("expected a completed repair slot");
    }
    const { result } = outcome;
    assert.equal(result.selectedState, "repaired");
    assert.notEqual(result.repair.termination, "not-requested");
    const repaired = result.repaired;
    const expected = repaired?.valid === true ? repaired.absoluteSide : null;
    assert.equal(result.objective, expected);
    ranked += expected === null ? 0 : 1;
  }
  assert.ok(ranked > 0, "no repaired state was valid, so the objective check proved nothing");
});

test("browser search rejects excessive work and ambiguous seed lists", () => {
  assert.deepEqual(parseBrowserSearchSeeds("0, 17,4294967295"), [0, 17, 4294967295]);
  assert.throws(() => parseBrowserSearchSeeds("1,,2"), /empty/);
  assert.throws(() => parseBrowserSearchSeeds("1,1.5"), /unsigned integer/);
  const baseline = { n: 2, seeds: [1], physicsSteps: 2, proposal: "grid", repair: false } as const;
  assert.throws(() => createBrowserSearchPlan({ ...baseline, n: 33 }), /1 to 32/);
  assert.throws(() => createBrowserSearchPlan({ ...baseline, physicsSteps: 5001 }), /5000/);
  assert.throws(() => createBrowserSearchPlan({ ...baseline, seeds: [1, 1] }), /unique/);
});

test("browser plans record the page's source revision and dirty flag", () => {
  const inputs = { n: 2, seeds: [1], physicsSteps: 2, proposal: "grid", repair: false } as const;
  const commit = "0123456789abcdef0123456789abcdef01234567";
  assert.deepEqual(
    createBrowserSearchPlan({ ...inputs, source: { commit, dirty: false } }).source,
    {
      commit,
      dirty: false,
      runtime: "browser",
      engine: "pack/v1",
    },
  );
  assert.deepEqual(createBrowserSearchPlan(inputs).source, {
    commit: "unknown",
    dirty: true,
    runtime: "browser",
    engine: "pack/v1",
  });
  assert.deepEqual(browserSearchSource(commit, "false"), { commit, dirty: false });
  assert.deepEqual(browserSearchSource(commit, "true"), { commit, dirty: true });
  assert.deepEqual(browserSearchSource(null, null), { commit: "unknown", dirty: true });
  assert.deepEqual(browserSearchSource("", "false"), { commit: "unknown", dirty: true });
  assert.deepEqual(browserSearchSource(commit, "maybe"), { commit, dirty: true });
});
