import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { test } from "node:test";
import { decodeCorpus, frameAt, pairAt } from "../src/data/corpus.ts";

function fixture(): unknown {
  return JSON.parse(readFileSync(new URL("fixtures/corpus.json", import.meta.url), "utf8"));
}

test("versioned catalogue preserves identities, palette and all four timing spans", () => {
  const corpus = decodeCorpus(fixture());
  assert.deepEqual(frameAt(corpus, 1).ident, [1]);
  assert.deepEqual([...frameAt(corpus, 2).ident].sort(), [1, 2]);
  assert.equal(pairAt(corpus, 0).n, 1);
  assert.equal(corpus.timing.correct, 0.25);
  assert.equal(corpus.colour.angleToleranceDegrees, 0.5);
  assert.equal(corpus.colour.shades.length, corpus.colour.palette.length);
  assert.throws(() => frameAt(corpus, 123456), /no frame/);
  assert.throws(() => pairAt(corpus, -1), /no transition/);
});

test("wrong versions, dimensions, phases and palette shapes fail the boundary", () => {
  const base = decodeCorpus(fixture());
  for (const malformed of [
    { ...base, schema: "future/v9" },
    { ...base, n_max: Number.NaN },
    { ...base, arrival_fraction: 2 },
    { ...base, timing: { ...base.timing, correct: -1 } },
    { ...base, motion_phases: ["unknown"] },
    { ...base, pairs: [] },
    { ...base, colour: { ...base.colour, shades: [] } },
    { ...base, colour: { ...base.colour, palette: ["url(unsafe)", "#000000", "#ffffff"] } },
  ]) {
    assert.throws(() => decodeCorpus(malformed));
  }
});

test("counts, pair maps, block indices and stable square identities are checked", () => {
  const truncated = decodeCorpus(fixture());
  frameAt(truncated, 2).squares.pop();
  assert.throws(() => decodeCorpus(truncated), /exactly/);
  const relabelled = decodeCorpus(fixture());
  frameAt(relabelled, 2).ident.reverse();
  assert.throws(() => decodeCorpus(relabelled), /identities/);
  const duplicate = decodeCorpus(fixture());
  pairAt(duplicate, 0).map = [pairAt(duplicate, 0).new];
  assert.throws(() => decodeCorpus(duplicate), /map every/);
  const missingBlock = decodeCorpus(fixture());
  pairAt(missingBlock, 0).block_of = [999];
  assert.throws(() => decodeCorpus(missingBlock), /block index/);
  const phantomBlock = decodeCorpus(fixture());
  pairAt(phantomBlock, 0).block_of = [0];
  pairAt(phantomBlock, 0).blocks = [
    { members: [], riders: [], cluster: 0, turn: 0, from: [0, 0], to: [0, 0], drift_max: 0 },
  ];
  assert.throws(() => decodeCorpus(phantomBlock), /matching member/);
  const missingStats = decodeCorpus(fixture());
  pairAt(missingStats, 0).stats = {};
  assert.throws(() => decodeCorpus(missingStats), /finite/);
  const missingFrame = decodeCorpus(fixture());
  delete missingFrame.frames["2"];
  assert.throws(() => decodeCorpus(missingFrame), /no frame/);
});
