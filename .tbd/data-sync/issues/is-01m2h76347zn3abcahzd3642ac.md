---
type: is
id: is-01m2h76347zn3abcahzd3642ac
title: "[epic] No JavaScript in Python, and one JavaScript floor with no exceptions"
kind: epic
status: open
priority: 1
version: 14
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies: []
parent_id: is-01m299tcsrh44b8n8m1c6jpgcb
child_order_hints:
  - is-01m2h763nax0cdf5p2btjjv224
  - is-01m2h7644r8f4ckfg0d93cgygq
  - is-01m2h764pcbfwx0btxez85zdsq
  - is-01m2h765488h9hcy6c3zpp4abx
  - is-01m2h765jws1b00yav58n7wzaq
  - is-01m2h7667fbtgmwgtwpq0hdtmw
  - is-01m299vc0er1aeg7dzkrvvx90m
  - is-01m2h77xckv2kewqdqhqj652sh
  - is-01m2k1rysbxnmgkspv4sa26fnm
  - is-01m2m597s65qq4bv32h9yjzb55
  - is-01m2m59g339yty13zk9v7srmtg
created_at: 2026-09-15T00:24:03.974Z
updated_at: 2026-09-16T10:03:21.627Z
---
Owner, 2026-09-14: "it looked like there was more JavaScript embedded in Python. This should be strictly forbidden. We should pull out everything and follow our high lint floors. We should create beads to track all of this tech debt and make sure that it's being addressed separately on another branch, another work tree, and land it as clean PRs stacked on top of these. We should be following the high biome and lint floors with auto formatting on all JavaScript, no exceptions."

**Measured at the workbench stack's tip (`bb3f7c99`, PR #171), with an AST scan:** 36 Python files embed JavaScript: 195 string literals passed to Playwright's evaluate-family calls and 51 JavaScript string constants, about 2,371 lines.
- `packing/devtools` explainer, print and math tools, plus two tests: about 1,700 lines. `check_print_layout.py` alone has 415.
- Video spike tools under `packing/atlas/known-best/video/spikes/`: about 600 lines, including a 279-line page script held as a Python constant in `v1-slideshow/build_candidate.py`.
- `packages/workbench/tools` checkers: about 50 lines, including two `page.evaluate` strings added to `check_workbench.py` on 2026-09-14.

**Floor exceptions to remove, because "no exceptions" means these too:**
- Biome overrides in `biome.json` switch off `noUnusedVariables` and `noUnusedFunctionParameters` for the motion-lab assets, and `noRedundantUseStrict` for those assets and `packages/workbench/src/application.js`.
- `tsc` relaxations in `tsconfig.json`, `tsconfig.motion-lab.json` and `tsconfig.probes.json` (`noImplicitAny`, `strictNullChecks`, `noUncheckedIndexedAccess` and `exactOptionalPropertyTypes` all false), tracked as `think-4cwy`.
- File-specific ESLint rule sets for `application.js` and the probes in `packages/workbench/eslint.config.js`.

**The pattern to generalise already exists.** `packages/workbench/tools/workbench_tools/probes.py` loads `probes/<name>.js`, and values reach a probe only as its one argument. Each probe is a file that Biome formats and lints, `tsc` type-checks and `check_probes` proves is used.

**Landing plan: clean PRs stacked on #171**, each in its own worktree and branch:
1. The guard and a shared probe loader, with a ratchet allowlist that names the tracking bead per file and may only shrink.
2. Extraction from `packing/devtools` and the tests.
3. Extraction from the video spikes; the allowlist reaches zero.
4. Extraction from the `packages/workbench` checkers, after that PR's review is addressed.
5. The Biome and ESLint floors without overrides.
6. `tsc` strict everywhere (`think-4cwy`).

## Notes

No-JavaScript extraction and no-exception Biome/ESLint floor are now on main through PRs #175, #178, #179, #181, and #180. HTML-shell executable bodies are file-backed and live negative controls cover reachability. Keep this epic open: think-n711/think-4cwy still track removal of the four TypeScript floor relaxations; think-b9qy separately tracks one shared browser-floor command definition.
