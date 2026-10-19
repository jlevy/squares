import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { test } from "node:test";
import { decodeCorpus } from "../src/data/corpus.ts";
import { loadCorpus } from "../src/published.ts";

const origin = "https://example.test";
const url = new URL("/workbench/data/corpus.json", origin);

test("published startup validates decoded data before handing it to the application", async (context) => {
  const data: unknown = JSON.parse(
    readFileSync(new URL("fixtures/corpus.json", import.meta.url), "utf8"),
  );
  context.mock.method(globalThis, "fetch", async () => new Response(JSON.stringify(data)));
  assert.deepEqual(await loadCorpus(url, origin), decodeCorpus(data));
});

test("HTTP failures and malformed data reject startup with actionable errors", async (context) => {
  const fetch = context.mock.method(
    globalThis,
    "fetch",
    async () => new Response("", { status: 503 }),
  );
  await assert.rejects(loadCorpus(url, origin), /HTTP 503/);
  fetch.mock.mockImplementation(async () => new Response("not json"));
  await assert.rejects(loadCorpus(url, origin), SyntaxError);
  fetch.mock.mockImplementation(async () => new Response('{"schema":"future/v9"}'));
  await assert.rejects(loadCorpus(url, origin));
});

test("startup refuses data from a different origin before making a request", async (context) => {
  const fetch = context.mock.method(globalThis, "fetch", async () => new Response("{}"));
  await assert.rejects(
    loadCorpus(new URL("https://other.test/data.json"), origin),
    /served by this site/,
  );
  assert.equal(fetch.mock.callCount(), 0);
});
