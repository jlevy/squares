import assert from "node:assert/strict";
import { test } from "node:test";
import {
  forceAtGap,
  forceLawAttracts,
  forceLawSteep,
  forceLawSubsteps,
} from "../src/simulation/force-law.ts";

const DEFAULT_LAW = { rigidity: 0.15, repulsion: 2_500, attraction: 0, range: 0 };
const RIGID_LAW = { rigidity: 0.01, repulsion: 4_000, attraction: 0, range: 0 };
const STICKY_LAW = { rigidity: 0.08, repulsion: 2_500, attraction: 120, range: 0.25 };

test("the shared default law preserves the shipped repulsion curve", () => {
  assert.equal(forceLawSteep(DEFAULT_LAW), 0);
  assert.equal(forceAtGap(DEFAULT_LAW, 0), 0);
  assert.equal(forceAtGap(DEFAULT_LAW, -0.1), 250);
  assert.equal(forceAtGap(DEFAULT_LAW, -0.15), 375);
  assert.equal(forceAtGap(DEFAULT_LAW, -0.2), 375);
  assert.equal(forceLawAttracts(DEFAULT_LAW), false);
});

test("rigid and sticky settings use the same curve in both simulation modes", () => {
  assert(forceLawSteep(RIGID_LAW) > 7.4);
  assert(forceAtGap(RIGID_LAW, -0.02) > forceAtGap(RIGID_LAW, -0.01));
  assert.equal(forceLawAttracts(STICKY_LAW), true);
  assert.equal(forceAtGap(STICKY_LAW, 0.125), -120);
  assert.equal(forceAtGap(STICKY_LAW, 0.25), 0);
  assert.equal(forceAtGap(STICKY_LAW, 1), 0);
});

test("law-driven substeps retain the legacy default and bound stiff settings", () => {
  assert.equal(forceLawSubsteps(DEFAULT_LAW, 1 / 120), 1);
  assert.equal(forceLawSubsteps(RIGID_LAW, 1 / 120), 2);
  assert.equal(forceLawSubsteps({ ...RIGID_LAW, repulsion: Number.MAX_VALUE }, 1), 12);
});
