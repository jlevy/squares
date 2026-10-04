import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { test } from "node:test";
import { type CorpusBoundCitations, decodeCorpus } from "../src/data/corpus.ts";
import { planCitations, RECORD } from "../src/view/facts.ts";

/**
 * The stage's citation data and version, held at the corpus boundary, and the plan the facts
 * view draws the CITATION section from. What the page draws from the plan is measured in
 * Chromium by `check_animate_view` and `check_layout`.
 */
function fixture(): Record<string, unknown> {
  return JSON.parse(readFileSync(new URL("fixtures/corpus.json", import.meta.url), "utf8"));
}

const verified = {
  text: "Nagamochi 2005, Discrete Optim. 2",
  note: null,
  basis: "external",
  assurance: "verified",
};

function withCitations(citations: unknown): Record<string, unknown> {
  return { ...fixture(), citations };
}

test("the corpus carries its version and its citations with their file's digest", () => {
  const corpus = decodeCorpus(fixture());
  assert.equal(corpus.version, "v0.4.0-f5e113");
  assert.match(corpus.citations.sha256 ?? "", /^[0-9a-f]{64}$/);
  assert.deepEqual(Object.keys(corpus.citations.entries), ["2"]);
  assert.equal(corpus.citations.entries["2"]?.upper?.assurance, "reported");
  assert.equal(corpus.citations.entries["2"]?.record, "n-002");
});

test("a page built without a citation file carries no citations and a null digest", () => {
  const corpus = decodeCorpus(withCitations({ sha256: null, entries: {} }));
  assert.equal(corpus.citations.sha256, null);
  assert.deepEqual(corpus.citations.entries, {});
});

test("a version that is not the shared version's shape is refused", () => {
  for (const version of ["", "0.4.0-f5e113", "v0.4-f5e113", "v0.4.0", "v0.4.0-XYZ123", 4]) {
    assert.throws(() => decodeCorpus({ ...fixture(), version }), /version|string/);
  }
  assert.equal(decodeCorpus({ ...fixture(), version: "v0.5.0-rc.1-abc123" }).version.length, 18);
});

test("citations that break the contract are refused at the boundary", () => {
  const sha256 = "a".repeat(64);
  const at2 = (lower: unknown, upper: unknown = null, record: unknown = "n-002") => ({
    sha256,
    entries: { "2": { lower, upper, record } },
  });
  const refused: [unknown, RegExp][] = [
    [{ sha256: "abc", entries: {} }, /sha256/],
    [{ ...at2(verified), sha256: null }, /digest/],
    [at2(null, null), /neither/],
    [{ sha256, entries: { "0": { lower: verified, upper: null, record: "n-000" } } }, /integer/],
    [{ sha256, entries: { "9": { lower: verified, upper: null, record: "n-009" } } }, /no facts/],
    [at2({ ...verified, text: "" }), /one/],
    [at2({ ...verified, text: " x" }), /one/],
    [at2({ ...verified, text: "a\nb" }), /one/],
    [at2({ ...verified, text: "x".repeat(67) }), /66/],
    [at2({ ...verified, basis: "folk" }), /basis/],
    [at2({ ...verified, assurance: "certain" }), /assurance/],
    [{ sha256, entries: { "2": { upper: verified, record: "n-002" } } }, /string|object|citation/],
    // The record is the n's own frontier case record, named as its file is.
    [at2(verified, null, "n-017"), /record n-017/],
    [at2(verified, null, "n-2"), /record n-2/],
    [{ sha256, entries: { "2": { lower: verified, upper: null } } }, /string/],
  ];
  for (const [citations, reason] of refused) {
    assert.throws(() => decodeCorpus(withCitations(citations)), reason, JSON.stringify(citations));
  }
  assert.throws(() => decodeCorpus({ ...fixture(), citations: undefined }), /object/);
});

test("the plan keeps each bound on its own line and carries the record's own note", () => {
  const cited = (lower: unknown, upper: unknown) =>
    ({ lower, upper, record: "n-017" }) as unknown as CorpusBoundCitations;
  const reported = {
    ...verified,
    text: "in Friedman & Ellsworth",
    note: "(reported)",
    assurance: "reported",
  };
  assert.equal(planCitations(undefined), null);
  assert.equal(planCitations(cited(null, null)), null);
  assert.deepEqual(planCitations(cited(verified, reported)), {
    record: "n-017",
    lines: [
      { bound: "lower", text: verified.text, corrects: null, note: null },
      { bound: "upper", text: reported.text, corrects: null, note: "(reported)" },
    ],
  });
  // A lone upper bound stays on the second line, so it does not move up between two n.
  assert.deepEqual(planCitations(cited(null, verified))?.lines, [
    null,
    { bound: "upper", text: verified.text, corrects: null, note: null },
  ]);
  assert.deepEqual(planCitations(cited(verified, null))?.lines, [
    { bound: "lower", text: verified.text, corrects: null, note: null },
    null,
  ]);
  // A reported lower bound carries the note too: it follows the register, not the bound.
  assert.equal(planCitations(cited(reported, null))?.lines[0]?.note, "(reported)");
  // The words are the record's. The plan passes them through and spells none of them.
  const both = { ...verified, note: "(reported; confirmed T-009)", assurance: "reported" };
  assert.equal(planCitations(cited(null, both))?.lines[1]?.note, "(reported; confirmed T-009)");
  // A lower bound standing in for a published result found unsound names that work on its
  // line, between the reference and the note.
  const correcting = { ...verified, corrects: "corrects Nagamochi 2005" };
  assert.equal(
    planCitations(cited(correcting, null))?.lines[0]?.corrects,
    "corrects Nagamochi 2005",
  );
  assert.equal(RECORD, "record");
});
