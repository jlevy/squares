---
type: is
id: is-01m2h7667fbtgmwgtwpq0hdtmw
title: Biome and ESLint floors with no overrides
kind: task
status: closed
priority: 1
version: 7
labels: []
dependencies: []
parent_id: is-01m2h76347zn3abcahzd3642ac
created_at: 2026-09-15T00:24:07.150Z
updated_at: 2026-09-16T10:03:35.681Z
closed_at: 2026-09-16T10:03:35.680Z
close_reason: "Delivered on main by PR #180 merge a4f801e8: no Biome override/exclusion, one effective ESLint configuration for every owned script, repository-wide reachability, live negative controls, and fully green exact-head required/Page/deep gates."
resolution: null
duplicate_of: null
---
The Biome and ESLint floors with no overrides, and auto-formatting on all JavaScript.

- Remove the `biome.json` overrides:
  - `noUnusedVariables` and `noUnusedFunctionParameters` off for `packing/src/sqpack/motion_lab/assets/**`, which exists because the assets are concatenated scripts calling each other's functions;
  - `noRedundantUseStrict` off for those assets and `packages/workbench/src/application.js`, which exists because they are non-module scripts whose `'use strict'` matters.
  The fix is structural: make them modules with explicit imports and exports, bundled where the page needs one file, or declare their shared globals explicitly. Silencing the rules is not a fix.
- Remove the file-specific relaxed rule sets for `application.js` and the probes in `packages/workbench/eslint.config.js`.
- Confirm Biome's includes reach every JavaScript and TypeScript file we own, and that nothing we own is excluded. Vendored third-party code under `vendor/` and minified files may stay excluded; say so explicitly.
- Extend `packing/tests/test_browser_floor_contract.py` so a reintroduced override or a relaxed ESLint block fails.

## Notes

2026-09-14, PR #160 review lane D-tools (D54, commit f7a640a2): `test_browser_floor_contract.py` declares the two tolerated Biome overrides exactly, naming this bead, and fails any other override. Remove each entry from `DECLARED_BIOME_OVERRIDES` as its override goes.

2026-09-15, branch claude/js-floor-no-overrides (PR https://github.com/jlevy/squares/pull/180, head 564ed2a3), based on claude/no-js-explainer-tools after merging #179 and that branch:
- Biome: both overrides removed. application.js is the ES-module entry of the page bundle (esbuild emits the strict directive; application-build.test.ts requires it). Each Motion Lab page runs its model and page script as separate module scripts; exact-n5-model.js publishes globalThis.MotionLabModel. tsconfig.base.json sets moduleDetection "force". noUnusedFunctionParameters in the old override was a no-op.
- Measured alternatives: bundling the motion lab needs Node+esbuild at render time in npm-less CI jobs (rejected); a "type": "commonjs" package.json leaves the four unused-function findings (rejected); deleting application.js's directive alone passes Biome but leaves the incoherent script (rejected).
- ESLint: one block for all owned JS, typed by every type-gate program (root tsconfig*.json found by name + PACKAGE_PROGRAMS). 184 files resolved to 6 configurations at #175; 433 resolve to 1 after both merges. Gates lint `.`. New tree = one tsconfig include line.
- Contract test: DECLARED_BIOME_OVERRIDES removed; any override or rule below error fails; devtools/node/eslint-file-configs.mjs reads ESLint's resolution for every tracked file and fails any difference; reintroduced overrides/blocks fail live; hook glob and biome ci formatting verdict checked.
- New devtools.check_motion_lab_pages (in the Chromium step): 48-state report byte-identical before/after.
- At the explainer merge: its Biome exclusion for packing/tests/fixtures/browser-floor was removed and the three liveness samples renamed *.js.txt (data, not source; tests copy them as sample.js); any files.includes exclusion beyond node_modules/vendor/.venv/*.min.js now fails. exact-model-projection.mjs reads globalThis.MotionLabModel.
- think-n711 stacks on this: application.js is a module in the bundle graph, and moduleDetection force is in the base.
