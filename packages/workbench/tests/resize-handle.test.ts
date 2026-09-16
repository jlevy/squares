import assert from "node:assert/strict";
import { test } from "node:test";
import {
  clampSeparator,
  keyedSeparatorPosition,
  SEPARATOR_LARGE_STEP,
  SEPARATOR_STEP,
} from "../src/view/resize-handle.ts";

const bounds = { min: 120, max: 900 };

test("a separator stays inside its bounds, and an empty range collapses to the minimum", () => {
  assert.equal(clampSeparator(500, bounds), 500);
  assert.equal(clampSeparator(10, bounds), 120);
  assert.equal(clampSeparator(2000, bounds), 900);
  assert.equal(clampSeparator(500, { min: 300, max: 200 }), 300);
  assert.throws(() => clampSeparator(Number.NaN, bounds), /finite/);
  assert.throws(() => clampSeparator(500, { min: 0, max: Number.POSITIVE_INFINITY }), /finite/);
});

test("arrows step the separator, Shift steps further, and Home and End reach the bounds", () => {
  assert.equal(keyedSeparatorPosition("ArrowUp", 500, bounds, false), 500 - SEPARATOR_STEP);
  assert.equal(keyedSeparatorPosition("ArrowDown", 500, bounds, false), 500 + SEPARATOR_STEP);
  assert.equal(keyedSeparatorPosition("ArrowUp", 500, bounds, true), 500 - SEPARATOR_LARGE_STEP);
  assert.equal(keyedSeparatorPosition("ArrowDown", 890, bounds, true), 900);
  assert.equal(keyedSeparatorPosition("Home", 500, bounds, false), 120);
  assert.equal(keyedSeparatorPosition("End", 500, bounds, false), 900);
  assert.equal(keyedSeparatorPosition("ArrowLeft", 500, bounds, false), null);
  assert.equal(keyedSeparatorPosition("Enter", 500, bounds, false), null);
});
