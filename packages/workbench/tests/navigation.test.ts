import assert from "node:assert/strict";
import { test } from "node:test";
import {
  availableStyles,
  nearestSupportedIndex,
  normalizeRange,
  planAspectTransition,
  rangeIndexBounds,
  transportIntent,
} from "../src/core/navigation.ts";

const SUPPORTED = [2, 5, 11, 17, 29, 324] as const;

test("sparse and arbitrary supported n values resolve deterministically", () => {
  assert.equal(nearestSupportedIndex(SUPPORTED, 2), 0);
  assert.equal(nearestSupportedIndex(SUPPORTED, 14), 2);
  assert.equal(nearestSupportedIndex(SUPPORTED, 15), 3);
  assert.deepEqual(normalizeRange(SUPPORTED, { from: 17, to: 17 }, 272, 272), {
    from: 324,
    to: 324,
    collapsed: true,
    forcedAspect: null,
  });
  assert.deepEqual(normalizeRange(SUPPORTED, { from: 17, to: 29 }, "bad", Infinity), {
    from: 17,
    to: 29,
    collapsed: false,
    forcedAspect: "animate",
  });
});

test("range bounds never turn an empty sparse interval into the whole corpus", () => {
  assert.deepEqual(rangeIndexBounds(SUPPORTED, { from: 12, to: 16 }), { first: 3, last: 3 });
  assert.deepEqual(rangeIndexBounds(SUPPORTED, { from: 5, to: 29 }), { first: 1, last: 4 });
});

test("Pack and Animate transitions remember their separate navigation state", () => {
  const toAnimate = planAspectTransition({
    currentAspect: "pack",
    currentRange: { from: 17, to: 17 },
    currentStepN: 17,
    rememberedPackN: null,
    rememberedAnimateRange: null,
    supportedSteps: SUPPORTED,
    target: "sweep",
  });
  assert.deepEqual(toAnimate, {
    changed: true,
    aspect: "animate",
    range: { from: 2, to: 324 },
    pairIndex: 0,
    rememberedPackN: 17,
    rememberedAnimateRange: null,
  });

  const toPack = planAspectTransition({
    currentAspect: "animate",
    currentRange: { from: 11, to: 29 },
    currentStepN: 17,
    rememberedPackN: 5,
    rememberedAnimateRange: null,
    supportedSteps: SUPPORTED,
    target: "pack",
  });
  assert.deepEqual(toPack, {
    changed: true,
    aspect: "pack",
    range: { from: 5, to: 5 },
    pairIndex: 1,
    rememberedPackN: 5,
    rememberedAnimateRange: { from: 11, to: 29 },
  });
});

test("the shared transport maps each visible state to one explicit action", () => {
  assert.deepEqual(availableStyles("pack"), ["physics", "bodies"]);
  assert.deepEqual(availableStyles("animate"), ["tween", "physics", "bodies"]);
  assert.equal(
    transportIntent({
      aspect: "pack",
      playing: false,
      optimizing: false,
      continuous: false,
      pairIndex: 0,
      firstPairIndex: 0,
      lastPairIndex: 0,
      atEnd: false,
    }),
    "start-pack",
  );
  assert.equal(
    transportIntent({
      aspect: "animate",
      playing: false,
      optimizing: false,
      continuous: false,
      pairIndex: 4,
      firstPairIndex: 1,
      lastPairIndex: 4,
      atEnd: true,
    }),
    "start-range",
  );
  assert.equal(
    transportIntent({
      aspect: "animate",
      playing: true,
      optimizing: false,
      continuous: true,
      pairIndex: 2,
      firstPairIndex: 1,
      lastPairIndex: 4,
      atEnd: false,
    }),
    "pause",
  );
});
