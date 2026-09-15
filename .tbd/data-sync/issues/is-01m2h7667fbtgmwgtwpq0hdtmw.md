---
type: is
id: is-01m2h7667fbtgmwgtwpq0hdtmw
title: Biome and ESLint floors with no overrides
kind: task
status: open
priority: 1
version: 3
labels: []
dependencies: []
parent_id: is-01m2h76347zn3abcahzd3642ac
created_at: 2026-09-15T00:24:07.150Z
updated_at: 2026-09-15T02:41:48.853Z
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
