// Parse Markdown mathematics with the pinned KaTeX bundle, for `devtools.check_katex`.
//
// Reads `{bundle, files: [{path, spans: [{source, display}]}]}` as JSON on stdin, parses
// every span in strict mode, and writes `{version, files: [{path, spans, errors}]}` to
// stdout. Each error names the span's one-based index, its source and KaTeX's message.
import { readFileSync } from "node:fs";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);

/**
 * @typedef {{ source: string, display: boolean }} Span
 * @typedef {{ path: string, spans: Span[] }} SpanFile
 * @typedef {{ span: number, source: string, error: string }} ParseError
 */

/** @type {{ bundle: string, files: SpanFile[] }} */
const input = JSON.parse(readFileSync(0, "utf8"));
/** @type {{ version: string, renderToString(source: string, options: object): string }} */
const katex = require(input.bundle);
const files = input.files.map((file) => {
  /** @type {ParseError[]} */
  const errors = [];
  file.spans.forEach((span, index) => {
    const source = span.source;
    try {
      katex.renderToString(source, {
        displayMode: span.display,
        throwOnError: true,
        strict: "error",
        trust: false,
      });
    } catch (error) {
      errors.push({ span: index + 1, source, error: String(error) });
    }
  });
  return { path: file.path, spans: file.spans.length, errors };
});
process.stdout.write(JSON.stringify({ version: katex.version, files }));
