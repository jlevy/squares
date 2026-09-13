import assert from "node:assert/strict";
import { test } from "node:test";
import {
  reducedMotionAction,
  stageDescription,
  stageKeyCommand,
} from "../src/view/accessibility.ts";

test("the stage description states the current mode, packing, and activity", () => {
  assert.equal(
    stageDescription({
      aspect: "pack",
      n: 17,
      squareCount: 17,
      containerSide: 4.675,
      playing: false,
      edited: true,
    }),
    "Pack mode shows n = 17. 17 squares are inside a container of side 4.6750. Playback is paused. The arrangement has been edited by hand.",
  );
  assert.match(
    stageDescription({
      aspect: "animate",
      n: 29,
      squareCount: 29,
      containerSide: 5.8,
      playing: true,
      edited: false,
    }),
    /Animate mode.*transition is playing/,
  );
});

test("stage keys enter the square layer and move or rotate the focused square", () => {
  assert.deepEqual(stageKeyCommand("Enter", false, false), { kind: "focus-square" });
  assert.deepEqual(stageKeyCommand("ArrowLeft", false, true), {
    kind: "move-square",
    dx: -0.05,
    dy: 0,
  });
  assert.deepEqual(stageKeyCommand("ArrowUp", true, true), {
    kind: "move-square",
    dx: 0,
    dy: 0.2,
  });
  assert.deepEqual(stageKeyCommand("q", false, true), {
    kind: "rotate-square",
    degrees: -15,
  });
  assert.deepEqual(stageKeyCommand("Escape", false, true), { kind: "leave-square" });
  assert.equal(stageKeyCommand("ArrowRight", false, false), null);
});

test("reduced motion turns transport into one discrete visible result", () => {
  assert.equal(
    reducedMotionAction({
      aspect: "pack",
      optimizing: false,
      pairIndex: 16,
      firstPairIndex: 16,
      lastPairIndex: 16,
      atPairEnd: false,
    }),
    "initialize-pack",
  );
  assert.equal(
    reducedMotionAction({
      aspect: "pack",
      optimizing: true,
      pairIndex: 16,
      firstPairIndex: 16,
      lastPairIndex: 16,
      atPairEnd: false,
    }),
    "step-pack",
  );
  assert.equal(
    reducedMotionAction({
      aspect: "animate",
      optimizing: false,
      pairIndex: 15,
      firstPairIndex: 15,
      lastPairIndex: 17,
      atPairEnd: false,
    }),
    "finish-pair",
  );
  assert.equal(
    reducedMotionAction({
      aspect: "animate",
      optimizing: false,
      pairIndex: 15,
      firstPairIndex: 15,
      lastPairIndex: 17,
      atPairEnd: true,
    }),
    "finish-next-pair",
  );
  assert.equal(
    reducedMotionAction({
      aspect: "animate",
      optimizing: false,
      pairIndex: 17,
      firstPairIndex: 15,
      lastPairIndex: 17,
      atPairEnd: true,
    }),
    "restart-and-finish",
  );
});
