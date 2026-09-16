// What each probe file evaluates to, for `devtools.check_probes`.
//
//   node inspect-probes.mjs <probe.js>...
//
// Prints one JSON object mapping each path to `{ "type": <typeof value> }`, or to
// `{ "error": <message> }` when the file does not evaluate. A probe is one expression, so it
// is wrapped in parentheses first: `(o) => o` alone on a line is a syntax error as a
// statement. The trailing semicolon the formatter writes is trimmed, because a statement
// terminator inside the parentheses is a syntax error too, and the closing parenthesis goes
// on its own line so a trailing line comment cannot swallow it.
//
// Each file is evaluated in a fresh, empty context. Evaluating an arrow function does not
// run its body, so nothing a probe does to a page happens here; a probe that is really an
// immediately-invoked function runs, fails on the missing page, and is reported as an error.
import { readFileSync } from "node:fs";
import { createContext, Script } from "node:vm";

/** @type {Record<string, { type: string } | { error: string }>} */
const verdicts = {};
for (const path of process.argv.slice(2)) {
  const source = readFileSync(path, "utf8").trimEnd().replace(/;$/, "");
  try {
    const value = new Script(`(${source}\n)`, { filename: path }).runInContext(createContext({}));
    verdicts[path] = { type: typeof value };
  } catch (error) {
    verdicts[path] = { error: error instanceof Error ? error.message : String(error) };
  }
}
process.stdout.write(JSON.stringify(verdicts));
