---
type: is
id: is-01m2hpnk78rqnf4qa846re4m8m
title: "Define the browser floor's commands once: npm scripts and validate.py disagree"
kind: task
status: open
priority: 3
version: 2
labels: []
dependencies: []
created_at: 2026-09-15T04:54:40.615Z
updated_at: 2026-09-16T08:08:24.326Z
---
From the PR #125 review (`attic/reviews/pr125-review-7b06254c.md`, pinned `7b06254c`), non-blocking suggestion 4, "Duplicate floor commands": the browser floor's commands exist both in `package.json` (`lint`, `typecheck`) and in `validate.py`; have one call the other.

Still true at `91cf28d6` (#171, `claude/workbench-defaults-and-bounds`), and the two definitions now differ in what they discover:

- Root `package.json:18-22`: `lint` is `biome ci` plus the workspace ESLint overlay; `typecheck` names three root programs (`tsconfig.json`, `tsconfig.probes.json`, `tsconfig.motion-lab.json`) plus the workspace `tsc -p tsconfig.json`. Neither runs the package's Node tests.
- `packages/workbench/package.json:19-23` repeats Biome and the ESLint command line for the package.
- `packing/src/sqpack/cli/validate.py:1468-1522` (`_browser_floor`) spells out Biome, the ESLint paths and flags, `tsc` over every `tsconfig*.json` at the root and in `packages/workbench` (the glob D54 relies on), and `npm test --workspace @squares/workbench`.

So a new `tsconfig.*.json` is checked by the gate but not by `npm run typecheck`, and a change to the ESLint paths must be made in three places.

Not cheap as a one-liner: the program discovery is a Python glob that npm scripts cannot express, and `packing/tests/test_browser_floor_contract.py` pins the gate's command shape. Options: `validate.py` runs `npm run lint`, `npm run typecheck` and `npm test` and the contract test reads the scripts; or one small Node entry point both call. Related: think-m0zb (one JavaScript floor), think-6o9n, think-4ylo.

## Notes

PR #180 integration at ba2cde3b fixed the newly observed partial-command symptom: root npm run typecheck now names final #181's tsconfig.explainer.json, and test_the_root_typecheck_script_names_every_root_type_program requires parity with every root tsconfig program plus the isolated probe and workbench commands. Direct npm run typecheck and the official dynamic browser-floor gate both pass. Keep this bead open: the larger requested consolidation (one command definition shared by npm and validate.py, including Node tests) remains.
