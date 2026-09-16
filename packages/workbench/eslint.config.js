import { readdirSync } from "node:fs";
import { resolve } from "node:path";
import tseslint from "typescript-eslint";

// The promise floor for checked JavaScript (`tbd guidelines typescript-lint-format-rules`, "Biome
// and Checked JavaScript"). Biome formats and lints every file, but its promise rules do not reach
// plain JavaScript, so ESLint adds exactly these three, type-aware, and nothing else.
//
// **One block for all of it.** Every JavaScript file the repository owns gets the same rules, the
// same parser and the same type information: no file has a block of its own, whether to relax a
// rule or to type it differently, and no owned file is ignored. `test_browser_floor_contract.py`
// reads the configuration ESLint resolves for every tracked file and fails any difference.
//
// **Types come from the type gate's programs**: every `tsconfig*.json` at the root but the shared
// base, found here rather than listed, and each package program below. A file is typed as `tsc`
// checks it, and a file in no program fails to parse, as it would be missing from the type gate.
//
// **To bring a new tree under the floor**, add it to the `include` of the type program that
// should check it: one line, in that `tsconfig`, and nothing here. A new root program is found
// without an edit; a new package program is one line in `PACKAGE_PROGRAMS`.
//
// The ignores are what is not ours (`vendor/`) and the git-ignored directories that hold
// JavaScript nobody wrote here: dependencies, virtual environments, build output, scratch space
// and agent worktrees. Biome reads `.gitignore` itself; ESLint cannot, so they are named, one a
// line.

const REPOSITORY = resolve(import.meta.dirname, "../..");
const PACKAGE_PROGRAMS = ["packages/workbench/tsconfig.json"];
const TYPE_PROGRAMS = [
  ...readdirSync(REPOSITORY)
    .filter((name) => /^tsconfig(\..+)?\.json$/.test(name) && name !== "tsconfig.base.json")
    .sort(),
  ...PACKAGE_PROGRAMS,
];
const NOT_OURS = [
  "vendor/**",
  "**/node_modules/**",
  "**/.venv/**",
  "packages/workbench/dist/**",
  "attic/**",
  ".claude/**",
];

export default [
  { ignores: NOT_OURS },
  {
    files: ["**/*.js", "**/*.jsx", "**/*.mjs", "**/*.cjs"],
    languageOptions: {
      parser: tseslint.parser,
      parserOptions: { project: TYPE_PROGRAMS, tsconfigRootDir: REPOSITORY },
    },
    plugins: { "@typescript-eslint": tseslint.plugin },
    rules: {
      "@typescript-eslint/await-thenable": "error",
      "@typescript-eslint/no-floating-promises": "error",
      "@typescript-eslint/no-misused-promises": "error",
    },
  },
];
