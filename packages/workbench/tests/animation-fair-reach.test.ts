import assert from "node:assert/strict";
import { test } from "node:test";
import { ANIMATION_CONTRACT, decodeAnimation, encodeAnimation } from "../src/data/animation.ts";

// An ascent's fair reach is a side only beside a checked packing: a settle the geometry check
// rejected reached no side, and the decoder refuses a row that claims one.
function withReach(fairReach: unknown[]) {
  return {
    contract: ANIMATION_CONTRACT,
    name: "fair reach",
    n: 1,
    fair_reach: fairReach,
    frames: [{ t: 0, side: 1, squares: [[0.5, 0.5, 0]], feasible: true }],
  };
}

test("a settle that is not a packing carries no side, and round-trips that way", () => {
  const row = { n: 5, fair_side: null, record: 2, excess_pct: null, packing_valid: false };
  const document = decodeAnimation(withReach([row]));
  assert.deepEqual(document.fairReach, [
    { n: 5, fairSide: null, record: 2, excessPct: null, packingValid: false },
  ]);
  assert.deepEqual(decodeAnimation(JSON.parse(encodeAnimation(document))).fairReach, [
    { n: 5, fairSide: null, record: 2, excessPct: null, packingValid: false },
  ]);
});

test("a side beside a settle that is not a packing is refused", () => {
  const claimed = { n: 5, fair_side: 2.1, record: 2, excess_pct: 5, packing_valid: false };
  assert.throws(() => decodeAnimation(withReach([claimed])), /reached no side/);
});

test("a checked settle keeps its side, and a row from before validity was recorded still reads", () => {
  const checked = { n: 5, fair_side: 2, record: 2, excess_pct: 0, packing_valid: true };
  const legacy = { n: 6, fair_side: 2.5, record: 2.5, excess_pct: 0 };
  const document = decodeAnimation(withReach([checked, legacy]));
  assert.equal(document.fairReach[0]?.fairSide, 2);
  assert.equal(document.fairReach[0]?.packingValid, true);
  assert.equal(document.fairReach[1]?.packingValid, null);
  assert.equal("packing_valid" in JSON.parse(encodeAnimation(document)).fair_reach[1], false);
  assert.throws(() => decodeAnimation(withReach([{ ...legacy, fair_side: null }])));
});
