import assert from "node:assert/strict";
import { test } from "node:test";
import { guard, runTrial } from "../probes/bench-annealing.ts";
import type { AtlasTransitions, WorkbenchApiHost } from "../src/api/workbench-api.ts";
import { assessPackingSnapshot, PACKING_VALIDITY } from "../src/core/runtime-contracts.ts";

type Pose = [number, number, number];

const PAIR_LAW = { rigidity: 0.35, repulsion: 950, attraction: 80, range: 0.15 };
const WALL_LAW = { rigidity: 0.25, repulsion: 2500, attraction: 0, range: 0 };
const TIMING = { dwell: 0.6, move: 0.9, correct: 0.25, settle: 0.4 };

function hostWith(final: Pose[], pairN = final.length - 1): WorkbenchApiHost {
  const api = {
    law: () => ({ ...PAIR_LAW, steep: 0, key: "law" }),
    wallLaw: () => ({ ...WALL_LAW }),
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
      annealSpan: 1.15,
    }),
    state: () => ({ blindInflate: 1, timing: { ...TIMING } }),
  };
  // Like the page, which opens on Pack: the catalogue API refuses every call but `setMode` and
  // `mode` until Animate owns the page.
  let view = "pack";
  const guarded = new Proxy(api, {
    get(target, property, receiver) {
      if (property === "setMode") {
        return (next: string) => {
          view = next;
          return view;
        };
      }
      if (property === "mode") {
        return () => view;
      }
      const member: unknown = Reflect.get(target, property, receiver);
      if (typeof member === "function" && view !== "animate") {
        return () => {
          throw new Error("atlasTransitions controls catalogue animation");
        };
      }
      return member;
    },
  });
  return { atlasTransitions: guarded as unknown as AtlasTransitions };
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
    pairLaw: PAIR_LAW,
    wallLaw: WALL_LAW,
    timing: TIMING,
    annealSpan: 1.15,
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

test("the probe measures and repairs overlap under the shared validity contract", () => {
  for (const final of [
    [
      [-0.5, 0, 0],
      [0.499995, 0, 0],
    ],
    [
      [0, 0, 30],
      [1.1, 0.2, 10],
      [0.3, 1.05, 0],
    ],
  ] satisfies Pose[][]) {
    const response = runTrial(
      { n: final.length, seed: 0, style: "bodies", inflate: null, anneal: null },
      hostWith(final),
    );
    assert(!("error" in response));
    const snapshot = (poses: Pose[], side: number) => ({
      squareSide: 1,
      container: { originX: 0, originY: 0, side },
      poses: poses.map(([x, y, angle]) => ({ x, y, angle })),
    });
    const raw = assessPackingSnapshot(snapshot(response.poses, response.side), final.length);
    assert.equal(response.overlap, raw.maxPairOverlap);
    assert(response.overlap > PACKING_VALIDITY.penetrationTolerance);
    const repaired = assessPackingSnapshot(
      snapshot(response.resolvedPoses, response.resolvedSide),
      final.length,
    );
    assert.equal(repaired.valid, true, JSON.stringify(repaired));
    assert.equal(response.resolvedOverlap, repaired.maxPairOverlap);
    assert.equal(response.repairConverged, true);
    assert.equal(response.resolvedSide, repaired.requiredSide);
  }
});

test("the typed trial refuses an n absent from the loaded page", () => {
  const response = runTrial(
    { n: 9, seed: 1, style: "physics", inflate: 1.1, anneal: 4 },
    hostWith([[0, 0, 0]]),
  );
  assert.deepEqual(response, { error: "the page carries no pair into n = 9" });
});
