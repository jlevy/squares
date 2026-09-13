import { resolve } from "node:path";
import { build } from "esbuild";

export interface BrowserBundleOptions {
  entryPoint: string;
  outfile: string;
  globalName?: string;
}

/** Bundle one typed module graph into a classic browser script. */
export async function bundleBrowser(options: BrowserBundleOptions): Promise<void> {
  await build({
    bundle: true,
    entryPoints: [options.entryPoint],
    format: "iife",
    ...(options.globalName === undefined ? {} : { globalName: options.globalName }),
    legalComments: "none",
    logLevel: "silent",
    outfile: options.outfile,
    platform: "browser",
    sourcemap: false,
    target: ["es2022"],
  });
}

const invokedPath = process.argv[1];
if (invokedPath !== undefined && import.meta.filename === resolve(invokedPath)) {
  const [entryPoint, outfile, globalName] = process.argv.slice(2);
  if (entryPoint === undefined || outfile === undefined) {
    throw new Error("usage: bundle-browser.ts ENTRY_POINT OUTFILE [GLOBAL_NAME]");
  }
  await bundleBrowser({
    entryPoint,
    outfile,
    ...(globalName === undefined ? {} : { globalName }),
  });
}
