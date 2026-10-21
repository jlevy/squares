import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { isAbsolute, join, relative, resolve, sep } from "node:path";
import { test } from "node:test";
import { runInNewContext } from "node:vm";
import { bundleBrowser } from "../tools/bundle-browser.ts";

const PACKAGE_ROOT = resolve(import.meta.dirname, "..");
const TSC = resolve(PACKAGE_ROOT, "../../node_modules/typescript/bin/tsc");

function compileContractFixture(path: string): string {
  const result = spawnSync(
    process.execPath,
    [
      TSC,
      "--ignoreConfig",
      "--allowImportingTsExtensions",
      "--exactOptionalPropertyTypes",
      "--forceConsistentCasingInFileNames",
      "--lib",
      "ES2022,DOM,DOM.Iterable",
      "--module",
      "ESNext",
      "--moduleResolution",
      "Bundler",
      "--noEmit",
      "--noFallthroughCasesInSwitch",
      "--noImplicitOverride",
      "--noImplicitReturns",
      "--noUncheckedIndexedAccess",
      "--strict",
      "--target",
      "ES2022",
      path,
    ],
    { cwd: PACKAGE_ROOT, encoding: "utf8" },
  );
  return `${result.status ?? -1}\n${result.stdout}${result.stderr}`;
}

test("the public API rejects missing, extra, and incompatible members", async () => {
  const scratch = await mkdtemp(join(tmpdir(), "squares-workbench-api-contract-"));
  const scratchFromPackage = relative(PACKAGE_ROOT, scratch);
  assert.equal(
    isAbsolute(scratchFromPackage) ||
      scratchFromPackage === ".." ||
      scratchFromPackage.startsWith(`..${sep}`),
    true,
  );
  const apiFromScratch = relative(scratch, resolve(PACKAGE_ROOT, "src/api/workbench-api.ts"));
  const portableApi = apiFromScratch.split(sep).join("/");
  const relativeApi =
    isAbsolute(apiFromScratch) || portableApi.startsWith(".") ? portableApi : `./${portableApi}`;
  const fixtures = new Map([
    [
      "valid",
      `import type { AtlasPhysics, AtlasTransitions } from "${relativeApi}";\ndeclare const api: AtlasTransitions;\nconst checked: AtlasTransitions = api;\nconst integration = checked.physics(0).integration;\nconst requested: "adaptive" | number = integration.requested;\nconst warning: "below-adaptive-stability-bound" | null = integration.warning;\nconst measured: AtlasPhysics = checked.measurePhysics(0, "bodies", "free");\nconst cost: number = measured.ms + measured.bytes;\nvoid requested;\nvoid warning;\nvoid cost;\n`,
    ],
    [
      "missing",
      `import type { AtlasTransitions } from "${relativeApi}";\ndeclare const api: AtlasTransitions;\nconst { state: omitted, ...candidate } = api;\nconst checked: AtlasTransitions = candidate;\nvoid omitted;\nvoid checked;\n`,
    ],
    [
      "extra",
      `import type { AtlasTransitions } from "${relativeApi}";\ndeclare const api: AtlasTransitions;\nconst checked: AtlasTransitions = { ...api, unexpected: () => false };\nvoid checked;\n`,
    ],
    [
      "incompatible",
      `import type { AtlasTransitions } from "${relativeApi}";\ndeclare const api: AtlasTransitions;\nconst checked: AtlasTransitions = { ...api, setSpeed: (value: string) => value };\nvoid checked;\n`,
    ],
    [
      "extra-helper",
      `import { defineWorkbenchApi, type AtlasTransitions } from "${relativeApi}";\ndeclare const api: AtlasTransitions;\ndefineWorkbenchApi({ ...api, unexpected: () => false });\n`,
    ],
  ]);

  try {
    const diagnostics = new Map<string, string>();
    for (const [name, source] of fixtures) {
      const path = join(scratch, `${name}.ts`);
      await writeFile(path, source, "utf8");
      diagnostics.set(name, compileContractFixture(path));
    }
    assert.match(diagnostics.get("valid") ?? "", /^0\n$/);
    assert.match(diagnostics.get("missing") ?? "", /^[^0]\n[\s\S]*Property 'state' is missing/);
    assert.match(diagnostics.get("extra") ?? "", /^[^0]\n[\s\S]*unexpected/);
    assert.match(diagnostics.get("extra-helper") ?? "", /^[^0]\n[\s\S]*never/);
    assert.match(
      diagnostics.get("incompatible") ?? "",
      /^[^0]\n[\s\S]*\(value: string\) => string[\s\S]*\(multiplier: number\) => number/,
    );
  } finally {
    await rm(scratch, { recursive: true });
  }
});

test("the API module bundles into the named classic-browser seam", async () => {
  const scratch = await mkdtemp(join(tmpdir(), "squares-workbench-api-"));
  const output = join(scratch, "api.js");
  try {
    await bundleBrowser({
      entryPoint: resolve(PACKAGE_ROOT, "src/api/browser-entry.ts"),
      outfile: output,
      globalName: "SquaresWorkbench",
    });
    const context: Record<string, unknown> = {};
    runInNewContext(await readFile(output, "utf8"), context, { filename: output });
    const namespace = context.SquaresWorkbench;
    assert.equal(typeof namespace, "object");
    assert.notEqual(namespace, null);
    if (typeof namespace !== "object" || namespace === null) {
      assert.fail("SquaresWorkbench was not an object");
    }
    assert.equal(typeof Reflect.get(namespace, "defineWorkbenchApi"), "function");
    assert.equal(typeof Reflect.get(namespace, "installWorkbenchApi"), "function");
    const core = Reflect.get(namespace, "core");
    assert.equal(typeof core, "object");
    assert.notEqual(core, null);
    if (typeof core !== "object" || core === null) {
      assert.fail("SquaresWorkbench.core was not an object");
    }
    assert.equal(typeof Reflect.get(core, "assessPackingSnapshot"), "function");
  } finally {
    await rm(scratch, { recursive: true });
  }
});

test("the browser physics report preserves the trajectory integration receipt", async () => {
  const application = await readFile(resolve(PACKAGE_ROOT, "src/application.js"), "utf8");
  assert.match(
    application,
    /integration:\s*Object\.assign\(\{\}, tr\.receipt\.configuration\.integration\)/,
  );
  assert.match(application, /animationIntegration\(LAW, WALLLAW, response\.storedTimestep\)/);
});

test("the trajectory measurement builds past the cache that the physics report reads", async () => {
  const application = await readFile(resolve(PACKAGE_ROOT, "src/application.js"), "utf8");
  const body = (name: string): string => {
    const pattern = new RegExp(`\\n  function ${name}\\([^)]*\\) \\{\\n([\\s\\S]*?)\\n  \\}\\n`);
    const found = pattern.exec(application)?.[1];
    assert.ok(found !== undefined, `application.js defines no ${name}`);
    return found;
  };
  // The measurement builds afresh on every call, so a repeat times the build again.
  const measure = body("measurePhysics");
  assert.match(measure, /freshTrajectory\(/);
  assert.doesNotMatch(measure, /ensureTrajectory|physicsCache/);
  assert.doesNotMatch(body("freshTrajectory"), /physicsCache/);
  // The cache fills from the same build, so what is timed is the trajectory the page would play.
  assert.match(body("ensureTrajectory"), /tr = freshTrajectory\(pairIndex, style, mode\);/);
  // And the page's API object carries it.
  assert.match(application, /\n {4}physics,\n {4}measurePhysics,\n/);
});
