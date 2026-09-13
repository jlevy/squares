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
    ignores: ["node_modules/**", "vendor/**"],
  },
  {
    files: ["packing/atlas/known-best/video/spikes/v2-transitions/assets/**/*.js"],
    languageOptions: {
      parser,
      parserOptions: { project: "./tsconfig.json" },
    },
    plugins,
    rules: promiseRules,
  },
  {
    files: ["packing/atlas/known-best/video/spikes/v2-transitions/probes/**/*.js"],
    languageOptions: {
      parser,
      parserOptions: { project: "./tsconfig.probes.json" },
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
