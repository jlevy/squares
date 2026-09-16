import { mkdir, readFile, rm, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { bundleBrowser } from "./bundle-browser.ts";

const PACKAGE_ROOT = resolve(import.meta.dirname, "..");
const APPLICATION_SOURCE = resolve(PACKAGE_ROOT, "src/application.js");

export const APPLICATION_BUNDLE = "workbench.js";
export const BENCHMARK_BUNDLE = "bench-annealing.js";

/** Build the classic scripts consumed by the page and its browser benchmark. */
export async function buildAssets(outputDirectory: string): Promise<void> {
  const out = resolve(outputDirectory);
  const apiBundle = resolve(out, ".workbench-api.js");
  await mkdir(out, { recursive: true });
  try {
    await bundleBrowser({
      entryPoint: resolve(PACKAGE_ROOT, "src/api/browser-entry.ts"),
      outfile: apiBundle,
      globalName: "SquaresWorkbench",
    });
    const [api, application] = await Promise.all([
      readFile(apiBundle, "utf8"),
      readFile(APPLICATION_SOURCE, "utf8"),
    ]);
    await writeFile(resolve(out, APPLICATION_BUNDLE), `${api.trimEnd()}\n${application}`, "utf8");
  } finally {
    await rm(apiBundle, { force: true });
  }

  await bundleBrowser({
    entryPoint: resolve(PACKAGE_ROOT, "probes/bench-annealing.ts"),
    outfile: resolve(out, BENCHMARK_BUNDLE),
    globalName: "SquaresWorkbenchBench",
  });
}

const invokedPath = process.argv[1];
if (invokedPath !== undefined && import.meta.filename === resolve(invokedPath)) {
  await buildAssets(process.argv[2] ?? resolve(PACKAGE_ROOT, "dist"));
}
