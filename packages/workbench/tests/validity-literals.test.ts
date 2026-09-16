import assert from "node:assert/strict";
import { readdirSync, readFileSync } from "node:fs";
import { join, relative } from "node:path";
import { test } from "node:test";

/**
 * Validity has one definition: `PACKING_VALIDITY` and the declared `CATALOGUE_PRECISION` in
 * `core/runtime-contracts.ts`. A tolerance written inline beside a validity decision is how the
 * gap bar came to call shrunken and overlapping squares a packing (#125 F3, #160 R2), so this
 * reads the browser sources for scientific literals (`1e-9`, `4e-6`) and holds two rules.
 */
const SOURCE = join(import.meta.dirname, "..", "src");
const CONTRACT = "core/runtime-contracts.ts";
const LITERAL = /(?<![\w.])\d+(?:\.\d+)?e-\d+\b/g;
/** Words that mark a decision about validity, a hit on the record, or a packing. */
const VALIDITY =
  /valid|\bmet\b|excess|\block(?:ed|s)?\b|packing|suspect|tolerance|overlap|penetration|feasible/i;
const NAMED_CONSTANT = /^\s*(?:export\s+)?const\s+([A-Z][A-Z0-9_]*)\s*=/;
const PROPERTY = /^\s*["']?(\w+)["']?\s*:\s*-?\d+(?:\.\d+)?e-\d+\s*,?\s*$/;
/**
 * Files outside the page and Pack sources that still hold an unnamed numerical epsilon, and how
 * many. None decides validity; each count may only fall, and a file leaves when it reaches zero.
 */
const UNNAMED_EPSILONS: Readonly<Record<string, number>> = {
  "simulation/trajectory.ts": 4,
  "view/colour.ts": 1,
};

interface Site {
  file: string;
  line: number;
  code: string;
  name: string | null;
}

function sources(directory: string): string[] {
  return readdirSync(directory, { withFileTypes: true }).flatMap((entry) => {
    const path = join(directory, entry.name);
    if (entry.isDirectory()) {
      return sources(path);
    }
    return /\.(?:ts|js)$/.test(entry.name) && !entry.name.endsWith(".d.ts") ? [path] : [];
  });
}

/** Every scientific literal in code, with its line and the constant or property it names. */
function sites(): Site[] {
  const found: Site[] = [];
  for (const path of sources(SOURCE)) {
    const file = relative(SOURCE, path).split("\\").join("/");
    if (file === CONTRACT) {
      continue;
    }
    // Comments say what a tolerance is; only code can apply one.
    const text = readFileSync(path, "utf8").replace(/\/\*[\s\S]*?\*\//g, (block) =>
      block.replace(/[^\n]/g, " "),
    );
    text.split("\n").forEach((raw, index) => {
      const code = raw.replace(/(^|[^:"'`])\/\/.*$/, "$1");
      for (const _ of code.matchAll(LITERAL)) {
        const name = NAMED_CONSTANT.exec(code)?.[1] ?? PROPERTY.exec(code)?.[1] ?? null;
        found.push({ file, line: index + 1, code: code.trim(), name });
      }
    });
  }
  return found;
}

test("no validity, hit or packing decision applies an inline tolerance", () => {
  const offending = sites()
    .filter((site) => VALIDITY.test(site.code) || (site.name !== null && VALIDITY.test(site.name)))
    .map((site) => `${site.file}:${site.line}: ${site.code}`);
  assert.deepEqual(offending, [], "use PACKING_VALIDITY or CATALOGUE_PRECISION instead");
});

test("every other scientific literal is a named constant or a named setting", () => {
  const unnamed = new Map<string, string[]>();
  for (const site of sites()) {
    if (site.name === null) {
      unnamed.set(site.file, [...(unnamed.get(site.file) ?? []), `${site.line}: ${site.code}`]);
    }
  }
  const counts = Object.fromEntries([...unnamed].map(([file, lines]) => [file, lines.length]));
  assert.deepEqual(
    counts,
    UNNAMED_EPSILONS,
    `name each epsilon with a comment saying what it guards: ${JSON.stringify(Object.fromEntries(unnamed), null, 2)}`,
  );
});
