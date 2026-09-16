import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { test } from "node:test";
import { sampleAnimation } from "../src/animation/trace.ts";
import {
  ANIMATION_CONTRACT,
  decodeAnimation,
  decodeLegacyAnimation,
  encodeAnimation,
} from "../src/data/animation.ts";

function example() {
  const records: number[] = [];
  return {
    contract: ANIMATION_CONTRACT,
    name: "Two-square illustration",
    n: 2,
    duration_seconds: 5,
    palette: { hue: "identity", shade: "full-side-contact" },
    source: { seed: 0, records, configuration: { seed: 0, phases: [] } },
    reference: { best_known: 2, proved_lower_bound: Math.SQRT2 },
    fair_reach: [{ n: 2, fair_side: 2, record: 2, excess_pct: 0 }],
    frames: [
      {
        t: 0,
        side: 2,
        squares: [
          [0.5, 0.5, 0],
          [1.5, 0.5, 0],
        ],
        square_ids: [3, 7],
        feasible: true,
      },
      {
        t: 0.5,
        side: 3,
        squares: [
          [0.5, 0.5, Math.PI],
          [2.5, 0.5, 0],
        ],
        square_ids: [3, 7],
        guided: true,
      },
      {
        t: 1,
        side: 4,
        squares: [
          [0.5, 0.5, 2 * Math.PI],
          [3.5, 0.5, 0],
        ],
        square_ids: [3, 7],
        guided: false,
      },
    ],
  };
}

test("Python and browser share the guidance and invalid-geometry contract vector", () => {
  const fixture: unknown = JSON.parse(
    readFileSync(new URL("./fixtures/packing-animation-v1.json", import.meta.url), "utf8"),
  );
  const document = decodeAnimation(fixture);
  assert.deepEqual(
    document.frames.map((frame) => frame.guided),
    [false, true, true],
  );
  assert.deepEqual(
    document.frames.map((frame) => frame.assessment.valid),
    [true, false, true],
  );
  assert.deepEqual(
    document.frames.map((frame) => frame.claimedFeasible),
    [true, true, true],
  );
  assert.deepEqual(document.frames[0]?.squareIds, [2, 1]);
  assert.equal(document.palette?.shade, "evidence");
});

test("versioned animation preserves geometry, stable IDs, source and presentation selections", () => {
  const document = decodeAnimation(example());
  assert.equal(document.frames.length, 3);
  assert.deepEqual(
    document.frames.map((frame) => frame.guided),
    [false, true, true],
  );
  assert.deepEqual(document.frames[0]?.squareIds, [3, 7]);
  assert.equal(document.frames[0]?.assessment.valid, true);
  assert.equal(document.frames[1]?.claimedFeasible, null);
  assert.equal(document.durationSeconds, 5);
  assert.equal(document.source?.seed, 0);
  assert.equal(document.palette?.shade, "full-side-contact");
  assert.equal(document.reference?.provedLowerBound, Math.SQRT2);
  assert.equal(document.fairReach[0]?.record, 2);
  const exported = decodeAnimation(JSON.parse(encodeAnimation(document)));
  assert.deepEqual(
    exported.frames.map((frame) => frame.guided),
    [false, true, true],
  );
  assert.deepEqual(exported.reference, document.reference);
  assert.deepEqual(exported.fairReach, document.fairReach);
});

test("coincident and escaped imported poses cannot inherit their feasible claim", () => {
  const value = example();
  const first = value.frames[0];
  assert.ok(first !== undefined);
  first.squares = [
    [0.5, 0.5, 0],
    [0.5, 0.5, 0],
  ];
  let decoded = decodeAnimation(value).frames[0];
  assert.equal(decoded?.claimedFeasible, true);
  assert.equal(decoded?.assessment.valid, false);
  first.squares = [
    [-1, 0.5, 0],
    [1.5, 0.5, 0],
  ];
  decoded = decodeAnimation(value).frames[0];
  assert.equal(decoded?.assessment.valid, false);
  first.squares = [
    [Number.NaN, 0.5, 0],
    [1.5, 0.5, 0],
  ];
  assert.throws(() => decodeAnimation(value), /finite/);
});

test("unknown versions, shapes, reordered IDs, nonmonotone times and unsupported schemes fail", () => {
  const value = example();
  assert.throws(
    () => decodeAnimation({ ...value, contract: "v0" }),
    /unsupported animation contract/,
  );
  assert.throws(() => decodeAnimation({ ...value, palette: { hue: null } }), /scheme names/);
  assert.throws(
    () => decodeAnimation({ ...value, palette: { hue: "record-proof" } }),
    /hue scheme/,
  );
  assert.throws(() => decodeAnimation({ ...value, n: 325 }), /at most 324/);
  const second = value.frames[1];
  assert.ok(second !== undefined);
  second.square_ids = [7, 3];
  assert.throws(() => decodeAnimation(value), /identities must remain stable/);
  second.square_ids = [3, 7];
  second.t = -0.1;
  assert.throws(() => decodeAnimation(value), /between zero and one/);
  second.t = 1;
  const final = value.frames[2];
  assert.ok(final !== undefined);
  final.t = 0.8;
  assert.throws(() => decodeAnimation(value), /nondecreasing/);
});

test("unversioned input needs the named adapter and source records carry guidance", () => {
  const { contract: _contract, ...value } = example();
  assert.throws(() => decodeAnimation(value), /legacy adapter/);
  value.source.records = [2];
  assert.deepEqual(
    decodeLegacyAnimation(value).frames.map((frame) => frame.guided),
    [true, true, true],
  );
});

test("trace sampling retains full turns and does not transfer a keyframe's check", () => {
  const document = decodeAnimation(example());
  const sampled = sampleAnimation(document, 0.25);
  assert.equal(sampled.side, 2.5);
  assert.equal(sampled.squares[0]?.angle, Math.PI / 2);
  assert.equal(sampled.assessment, null);
  assert.equal(sampled.interpolated, true);
  assert.equal(sampled.guided, true);
  assert.equal(sampleAnimation(document, 0).assessment?.valid, true);
  assert.equal(sampleAnimation(document, 1).squares[0]?.angle, Math.PI * 2);
  assert.deepEqual(sampleAnimation(document, -10), sampleAnimation(document, 0));
  assert.deepEqual(sampleAnimation(document, 10), sampleAnimation(document, 1));
  assert.throws(() => sampleAnimation(document, Number.NaN), /finite/);
});

test("equal-time keyframes have deterministic last-frame ownership", () => {
  const value = example();
  const second = value.frames[1];
  assert.ok(second !== undefined);
  second.t = 0;
  const sampled = sampleAnimation(decodeAnimation(value), 0);
  assert.equal(sampled.side, 3);
  assert.equal(sampled.guided, true);
  assert.equal(sampled.interpolated, false);
});

test("editing away a guide frame cannot wash ancestry out of an exported suffix", () => {
  const document = decodeAnimation(example());
  const final = document.frames[2];
  assert.ok(final !== undefined);
  const trimmed = { ...document, frames: [{ ...final, t: 0 }] };
  const roundTrip = decodeAnimation(JSON.parse(encodeAnimation(trimmed)));
  assert.equal(roundTrip.frames[0]?.guided, true);
});
