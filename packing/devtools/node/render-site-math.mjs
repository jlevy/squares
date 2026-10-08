// Build-time visual math, using the same pinned KaTeX and kpress metrics as the papers.
// Only local renderer code executes; TeX is rendered with trust disabled and bounded
// expansion. No browser, network, or page scripts execute during publication.
import { readFileSync } from "node:fs";
import { createRequire } from "node:module";
import { runInNewContext } from "node:vm";

/**
 * @typedef {"prose" | "sans" | "katex"} Profile
 * @typedef {{source: string, display: boolean, profile: Profile, semantic: boolean}} Formula
 * @typedef {Record<string, number[]>} FontMetrics
 * @typedef {{version: string, renderToString(source: string, options: object): string, __setFontMetrics(face: string, metrics: FontMetrics): void}} Katex
 * @typedef {Record<string, unknown> & {sans: Record<string, FontMetrics>, katex: Record<string, FontMetrics>}} Metrics
 */

/** @type {{bundle: string, metrics: string, formulas: Formula[]}} */
const input = JSON.parse(readFileSync(0, "utf8"));
/** @type {Katex} */
const katex = createRequire(import.meta.url)(input.bundle);
/** @type {{kpressKatexTextMetrics?: Metrics}} */
const context = {};
runInNewContext(readFileSync(input.metrics, "utf8"), context, { timeout: 1000 });
const metrics = context.kpressKatexTextMetrics;
if (!metrics) {
  throw new Error("kpress's font metrics are unavailable");
}
/** @type {Profile | undefined} */
let installed;
const rendered = input.formulas.map((formula) => {
  if (installed !== formula.profile) {
    const tables = formula.profile === "prose" ? metrics : metrics[formula.profile];
    if (!tables) {
      throw new Error(`unknown mathematics profile ${formula.profile}`);
    }
    for (const [face, table] of Object.entries(tables)) {
      if (!["sans", "katex", "scale", "fonts"].includes(face)) {
        katex.__setFontMetrics(face, /** @type {FontMetrics} */ (table));
      }
    }
    installed = formula.profile;
  }
  const source = formula.source.replace(/(?<![A-Za-z\\])([a-z])\(/g, "$1\\mkern1mu(");
  return katex.renderToString(source, {
    displayMode: formula.display,
    output: formula.semantic ? "htmlAndMathml" : "html",
    throwOnError: true,
    strict: "ignore",
    trust: false,
    maxExpand: 1000,
    maxSize: 100,
  });
});
process.stdout.write(JSON.stringify({ version: katex.version, rendered }));
