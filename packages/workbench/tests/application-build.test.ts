import assert from "node:assert/strict";
import { mkdtemp, readFile, rm } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import { test } from "node:test";
import { runInNewContext } from "node:vm";
import { APPLICATION_BUNDLE, BENCHMARK_BUNDLE, buildAssets } from "../tools/build-assets.ts";

const REPOSITORY_ROOT = resolve(import.meta.dirname, "../../..");
const LEGACY_APPLICATION = resolve(
  REPOSITORY_ROOT,
  "packing/atlas/known-best/video/spikes/v2-transitions/assets/workbench.js",
);

test("the retained application refuses to run before its package bundle", async () => {
  const application = await readFile(LEGACY_APPLICATION, "utf8");
  assert.throws(
    () => runInNewContext(application, {}),
    /SquaresWorkbench bundle must load before the application script/,
  );
});

test("the package build orders the typed namespace before the retained application", async () => {
  const scratch = await mkdtemp(join(tmpdir(), "squares-workbench-assets-"));
  try {
    await buildAssets(scratch);
    const application = await readFile(resolve(scratch, APPLICATION_BUNDLE), "utf8");
    const benchmark = await readFile(resolve(scratch, BENCHMARK_BUNDLE), "utf8");

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
