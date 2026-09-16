import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { test } from "node:test";
import { runInNewContext } from "node:vm";
import { bundleBrowser } from "../tools/bundle-browser.ts";
import { candidateCorpus, checkCompleteCorpus } from "../tools/check-candidate-corpus.ts";

test("the build tool bundles typed modules into an executable classic browser script", async () => {
  const scratch = await mkdtemp(join(tmpdir(), "squares-workbench-build-"));
  const dependency = join(scratch, "dependency.ts");
  const entry = join(scratch, "entry.ts");
  const output = join(scratch, "bundle.js");
  try {
    await writeFile(dependency, "export const answer: number = 42;\n", "utf8");
    await writeFile(
      entry,
      'import { answer } from "./dependency.ts";\nexport const result = answer + 1;\n',
      "utf8",
    );

    await bundleBrowser({ entryPoint: entry, outfile: output, globalName: "FixtureBundle" });

    const context: Record<string, unknown> = {};
    runInNewContext(await readFile(output, "utf8"), context, { filename: output });
    assert.deepEqual(JSON.parse(JSON.stringify(context.FixtureBundle)), { result: 43 });
  } finally {
    await rm(scratch, { recursive: true });
  }
});

test("the generated-page boundary decodes one complete versioned corpus", () => {
  const fixture = JSON.parse(
    readFileSync(new URL("fixtures/corpus.json", import.meta.url), "utf8"),
  ) as Record<string, unknown>;
  fixture.n_max = 2;
  const page = `<script id="atlas-data" type="application/json">${JSON.stringify(fixture)}</script>`;
  const corpus = checkCompleteCorpus(candidateCorpus(page), 2);
  assert.equal(corpus.n_max, 2);
  assert.deepEqual(
    corpus.pairs.map(({ n }) => n),
    [1],
  );

  const frames = fixture.frames as Record<string, unknown>;
  delete frames["2"];
  assert.throws(() => checkCompleteCorpus(fixture, 2), /no frame|frames 1\.\.2/);
  assert.throws(() => candidateCorpus(`${page}${page}`), /exactly one/);
});
