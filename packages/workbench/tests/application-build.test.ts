import assert from "node:assert/strict";
import { mkdtemp, readFile, rm } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import { test } from "node:test";
import { runInNewContext } from "node:vm";
import { APPLICATION_BUNDLE, BENCHMARK_BUNDLE, buildAssets } from "../tools/build-assets.ts";

test("the page bundle is one strict script that publishes the typed namespace", async () => {
  const scratch = await mkdtemp(join(tmpdir(), "squares-workbench-assets-"));
  try {
    await buildAssets(scratch);
    const application = await readFile(resolve(scratch, APPLICATION_BUNDLE), "utf8");
    const benchmark = await readFile(resolve(scratch, BENCHMARK_BUNDLE), "utf8");

    // The page inlines the bundle as a classic script, so its strict mode is this directive and
    // nothing else: `src/application.js` is a module and carries none of its own.
    assert.ok(
      application.startsWith('"use strict";\n'),
      "the page bundle does not open with the strict-mode directive",
    );
    const applicationContext: Record<string, unknown> = {};
    runInNewContext(application, applicationContext, { filename: APPLICATION_BUNDLE });
    const namespace = applicationContext.SquaresWorkbench;
    assert.equal(typeof namespace, "object");
    assert.notEqual(namespace, null);

    const benchmarkContext: Record<string, unknown> = {};
    runInNewContext(benchmark, benchmarkContext, { filename: BENCHMARK_BUNDLE });
    const probe = benchmarkContext.SquaresWorkbenchBench;
    assert.equal(typeof probe, "object");
    assert.notEqual(probe, null);
    if (typeof probe !== "object" || probe === null) {
      assert.fail("SquaresWorkbenchBench was not an object");
    }
    assert.equal(typeof Reflect.get(probe, "guard"), "function");
    assert.equal(typeof Reflect.get(probe, "runTrial"), "function");
  } finally {
    await rm(scratch, { recursive: true });
  }
});
