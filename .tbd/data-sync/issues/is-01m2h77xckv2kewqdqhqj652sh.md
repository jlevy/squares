---
type: is
id: is-01m2h77xckv2kewqdqhqj652sh
title: tsc strict for every JavaScript program; the think-4cwy ratchet ends
kind: task
status: open
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies: []
parent_id: is-01m2h76347zn3abcahzd3642ac
created_at: 2026-09-15T00:25:03.631Z
updated_at: 2026-09-15T01:17:56.938Z
---
`tsc` strict for every JavaScript program, which removes the ratchet `think-4cwy` adopted.

`tsconfig.json` (`packages/workbench/src/application.js`), `tsconfig.motion-lab.json` and `tsconfig.probes.json` set `noImplicitAny`, `strictNullChecks`, `noUncheckedIndexedAccess` and `exactOptionalPropertyTypes` to false, and each comment names `think-4cwy` as the tracker. **`think-4cwy` is closed**, so the relaxations currently name a tracker that tracks nothing, which the floor's rule 8 does not allow.

Repoint those comments to this bead immediately, in the first PR of the stack that touches the configs. Then remove the relaxations program by program, moving files out of each relaxed program and never in, with `test_browser_floor_contract.py` failing any relaxation left without an open tracker.

The workbench's `application.js` is the large one: over 5,000 lines of JSDoc-typed JavaScript, and a candidate for conversion to TypeScript modules under the package's existing strict `tsconfig` instead of being hardened in place.

## Notes

PR #175 (head 1ec9ea7b) repoints the relaxation comments in tsconfig.json, tsconfig.motion-lab.json and tsconfig.probes.json from the closed think-4cwy to this bead. The relaxations are unchanged.

test_browser_floor_contract.py does not pin a tracker id: it accepts any think-XXXX match. It does not check that the tracker is open, which is how the stale think-4cwy survived. Add that check when removing the relaxations.

The two new programs in #175, tsconfig.packing-probes.json and tsconfig.devtools-node.json, are strict with no relaxations.
