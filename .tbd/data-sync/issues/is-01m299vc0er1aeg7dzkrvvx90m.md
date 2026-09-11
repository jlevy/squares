---
type: is
id: is-01m299vc0er1aeg7dzkrvvx90m
title: "J3: the type gate, adopted through the ratchet"
kind: task
status: closed
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies: []
parent_id: is-01m299tcsrh44b8n8m1c6jpgcb
created_at: 2026-09-11T22:36:42.893Z
updated_at: 2026-09-11T23:08:50.182Z
closed_at: 2026-09-11T23:08:50.166Z
close_reason: "Zero across all three programs: the workbench's script 1,145 -> 109 -> 0, the 180 probes 446 -> 170 -> 0, the motion lab and slideshow 506 -> 62 -> 0. No flag relaxed beyond the four the ratchet declares, no @ts-ignore and no blanket any anywhere. probes/atlas-transitions.d.ts writes the page's API down -- 114 keys, cross-checked against what the page exports. Landed as c803f848; the ratchet itself (the four flags) stays open as think-xxxx follow-ups when JSDoc arrives."
resolution: null
duplicate_of: null
---
Floor rule 3: type checking is a separate strict gate, and a JavaScript-only project gets it through `allowJs` + `checkJs` + `noEmit`. Floor rule 8: legacy code ratchets toward strict and never loosens the default.

Both matter here, because the honest measurement is that `assets/workbench.js` is one 5,079-line IIFE with 129 DOM handles (107 `getElementById`, 22 `querySelector`) and zero JSDoc. Under `strictNullChecks` every one of those is `HTMLElement | null` before it is anything useful.

So: write the base `tsconfig.json` at the floor -- `strict`, `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`, `noImplicitOverride`, `noImplicitReturns`, `noFallthroughCasesInSwitch`, `forceConsistentCasingInFileNames` -- and then MEASURE what the workbench reports under it. Enable what passes. For each flag that does not, follow the ratchet: keep the default strict, relax only the blocking flag over an explicit file list in a second config, and name this bead's ID in a comment beside the off-switch.

Do not skip the measurement and assume it is hopeless, and do not turn `strict` off to make a number go to zero. The deliverable is a live gate plus an honest list of what it does not yet cover.

Note: Biome's promise rules do not cover plain JavaScript, so a Biome-only checked-JS project runs below the floor. The page has no promises to speak of -- it is a requestAnimationFrame loop -- so state that and decline the ESLint overlay explicitly, or add it. The guideline is clear that declining must be documented rather than silent.

## Notes

MEASURED, which floor rule 8 asks for before any relaxation. Per program, full floor vs the four flags relaxed:

  workbench assets   1,145 -> 109
  probes               446 -> 170
  motion_lab + v1        43 ->  62   (43 is slideshow alone; motion_lab 463 -> 53)
  total              2,097 -> 341

The four relaxed are noImplicitAny, strictNullChecks, noUncheckedIndexedAccess and exactOptionalPropertyTypes. tsconfig.base.json keeps the full floor; each program's config extends it and relaxes only those four, naming this bead.

Three tsconfigs rather than one, and the reason matters: these are independent PROGRAMS, not modules. exact-n5-model.js defines what motion-lab.js calls because Python concatenates them into one page; one include covering everything would put every file in one global scope and invent collisions. The same fact had already bitten Biome, which renamed four cross-file functions as unused.

The 341 are delegated to three agents, one per program. What remains after that is the ratchet itself: the four flags, which come back on a program at a time as JSDoc types arrive.

Promise safety: Biome's promise rules are TypeScript-only, so a Biome-only checked-JS project runs below the floor there. The page has no promises -- it is a requestAnimationFrame loop -- so the ESLint overlay is declined deliberately, which the guideline requires be written down rather than left silent.
