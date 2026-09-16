import { mkdir } from "node:fs/promises";
import { resolve } from "node:path";
import { bundleBrowser } from "./bundle-browser.ts";

const PACKAGE_ROOT = resolve(import.meta.dirname, "..");

export const APPLICATION_BUNDLE = "workbench.js";
export const BENCHMARK_BUNDLE = "bench-annealing.js";

/**
 * Build the classic scripts consumed by the page and its browser benchmark.
 *
 * The page's script is one bundle whose entry is `src/application.js`: the application and the
 * typed modules it imports, with the entry's exports published as `SquaresWorkbench`.
 */
export async function buildAssets(outputDirectory: string): Promise<void> {
  const out = resolve(outputDirectory);
  await mkdir(out, { recursive: true });
  await bundleBrowser({
    entryPoint: resolve(PACKAGE_ROOT, "src/application.js"),
    outfile: resolve(out, APPLICATION_BUNDLE),
    globalName: "SquaresWorkbench",
  });
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
