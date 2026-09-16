import tseslint from "typescript-eslint";

const promiseRules = {
  "@typescript-eslint/await-thenable": "error",
  "@typescript-eslint/no-floating-promises": "error",
  "@typescript-eslint/no-misused-promises": "error",
};

const parser = tseslint.parser;
const plugins = { "@typescript-eslint": tseslint.plugin };

export default [
  {
    ignores: ["node_modules/**", "vendor/**", "packages/workbench/dist/**"],
  },
  {
    // Every workbench JavaScript file outside the two legacy programs below, so no package
    // JavaScript escapes the promise floor. A file a package tsconfig includes is typed by
    // that program; one no program includes yet is typed at the shared strict floor rather
    // than skipped. typescript-eslint refuses `**` in `allowDefaultProject`, so the globs
    // name depths: a file deeper than they reach fails to parse, which fails the lint.
    files: ["packages/workbench/**/*.js"],
    ignores: ["packages/workbench/src/application.js", "packages/workbench/probes/**"],
    languageOptions: {
      parser,
      parserOptions: {
        projectService: {
          allowDefaultProject: ["packages/workbench/*/*.js", "packages/workbench/*/*/*.js"],
          defaultProject: "tsconfig.base.json",
        },
      },
    },
    plugins,
    rules: promiseRules,
  },
  {
    files: ["packages/workbench/src/application.js"],
    languageOptions: {
      parser,
      parserOptions: { project: "./tsconfig.json" },
    },
    plugins,
    rules: promiseRules,
  },
  {
    files: ["packages/workbench/probes/**/*.js"],
    languageOptions: {
      parser,
      parserOptions: { project: "./tsconfig.probes.json" },
    },
    plugins,
    rules: promiseRules,
  },
  {
    // The probes the Python tools under `packing/` load through `sqpack.probes`, with the v1
    // slideshow's page script that shares their program, and the Node scripts those tools run.
    // Both programs are strict; neither inherits a relaxation.
    files: [
      "packing/**/probes/**/*.js",
      "packing/atlas/known-best/video/spikes/v1-slideshow/assets/*.js",
    ],
    languageOptions: {
      parser,
      parserOptions: { project: "./tsconfig.packing-probes.json" },
    },
    plugins,
    rules: promiseRules,
  },
  {
    files: ["packing/devtools/node/**/*.mjs"],
    languageOptions: {
      parser,
      parserOptions: { project: "./tsconfig.devtools-node.json" },
    },
    plugins,
    rules: promiseRules,
  },
  {
    files: [
      "packing/src/sqpack/motion_lab/assets/**/*.js",
      "packing/atlas/known-best/video/spikes/v1-slideshow/*.js",
    ],
    languageOptions: {
      parser,
      parserOptions: { project: "./tsconfig.motion-lab.json" },
    },
    plugins,
    rules: promiseRules,
  },
];
