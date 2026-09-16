import { readFile } from "node:fs/promises";
import { resolve } from "node:path";
import { type Corpus, decodeCorpus } from "../src/data/corpus.ts";

const DATA_BLOCK = /<script\s+id="atlas-data"\s+type="application\/json">([\s\S]*?)<\/script>/g;

/** Read the versioned workbench corpus from a generated candidate page. */
export function candidateCorpus(page: string): unknown {
  const blocks = [...page.matchAll(DATA_BLOCK)];
  if (blocks.length !== 1 || blocks[0]?.[1] === undefined) {
    throw new RangeError("candidate page must contain exactly one atlas-data JSON block");
  }
  return JSON.parse(blocks[0][1]);
}

/** Require a complete, ordered catalogue after the ordinary schema decoder succeeds. */
export function checkCompleteCorpus(value: unknown, expectedMaximum = 324): Corpus {
  const corpus = decodeCorpus(value);
  const frames = Object.keys(corpus.frames)
    .map(Number)
    .sort((a, b) => a - b);
  const pairs = corpus.pairs.map(({ n }) => n);
  const expectedFrames = Array.from({ length: expectedMaximum }, (_, index) => index + 1);
  const expectedPairs = expectedFrames.slice(0, -1);
  if (
    corpus.n_max !== expectedMaximum ||
    frames.length !== expectedMaximum ||
    !frames.every((n, index) => n === expectedFrames[index]) ||
    pairs.length !== expectedMaximum - 1 ||
    !pairs.every((n, index) => n === expectedPairs[index])
  ) {
    throw new RangeError(
      `candidate corpus must contain frames 1..${expectedMaximum} and every transition`,
    );
  }
  return corpus;
}

const invokedPath = process.argv[1];
if (invokedPath !== undefined && import.meta.filename === resolve(invokedPath)) {
  const candidate = process.argv[2];
  if (candidate === undefined) {
    throw new Error("usage: check-candidate-corpus.ts CANDIDATE_HTML");
  }
  checkCompleteCorpus(candidateCorpus(await readFile(candidate, "utf8")));
}
