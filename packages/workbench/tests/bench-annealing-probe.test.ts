import assert from "node:assert/strict";
import { test } from "node:test";
import { guard, runTrial } from "../probes/bench-annealing.ts";
import type { AtlasTransitions, WorkbenchApiHost } from "../src/api/workbench-api.ts";

type Pose = [number, number, number];

function hostWith(final: Pose[], pairN = final.length - 1): WorkbenchApiHost {
  const api = {
    setSeed: (seed: unknown) => Number(seed),
    seed: () => 17,
    setBlindInflate: () => 0,
    setAnneal: () => ({ level: 0 }),
    pairs: () => [{ n: pairN }],
    physics: () => ({
      style: "bodies",
      mode: "blind",
      anneal: 0,
      ms: 3,
      final,
      miss: { excess: 0, side: 2, record: 2, centre: 0, angle: 0 },
      steps: 12,
    }),
    state: () => ({ blindInflate: 1 }),
  } as unknown as AtlasTransitions;
  return { atlasTransitions: api };
}

test("the benchmark guard refuses a missing API and accepts a loaded one", () => {
  assert.deepEqual(guard({}), { ok: false, why: "no page API" });
  assert.deepEqual(guard(hostWith([], 0)), {
    ok: true,
    pairs: 1,
    seed: 17,
  });
});

test("a typed trial preserves valid geometry and reports its independent measurement", () => {
  const response = runTrial(
    { n: 2, seed: 0, style: "bodies", inflate: null, anneal: null },
    hostWith([
      [-0.5, 0, 0],
      [0.5, 0, 0],
    ]),
  );
  assert(!("error" in response));
  assert.equal(response.overlap, 0);
  assert.equal(response.resolvedOverlap, 0);
  assert.equal(response.resolvedSide, 2);
  assert.deepEqual(response.configuration, {
    style: "bodies",
    mode: "blind",
    seed: 17,
    inflate: 1,
    anneal: 0,
  });
  assert.equal(response.physicsMs, 3);
  assert.equal(response.repairSweeps, 1);
  assert.equal(response.repairSweepLimit, 400);
  assert.equal(response.repairConverged, true);
  assert.deepEqual(response.poses, [
    [0.5, 0.5, 0],
    [1.5, 0.5, 0],
  ]);
});

test("the typed trial refuses an n absent from the loaded page", () => {
  const response = runTrial(
    { n: 9, seed: 1, style: "physics", inflate: 1.1, anneal: 4 },
    hostWith([[0, 0, 0]]),
  );
  assert.deepEqual(response, { error: "the page carries no pair into n = 9" });
});
