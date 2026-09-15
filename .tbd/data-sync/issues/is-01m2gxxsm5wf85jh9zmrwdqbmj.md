---
type: is
id: is-01m2gxxsm5wf85jh9zmrwdqbmj
title: Restore checks PR 160 weakened or dropped, and its stale harness references
kind: bug
status: open
priority: 2
version: 4
spec_path: docs/project/specs/active/plan-2026-09-11-annealing-as-a-search.md
labels: []
dependencies: []
parent_id: is-01m29kqwefbzzpt7bngm68pq6p
created_at: 2026-09-14T21:42:14.902Z
updated_at: 2026-09-15T02:59:20.688Z
---
Checks weakened or dropped by PR #160's consolidation (2026-09-14 audit; the probe items were read by a helper and not re-verified):

- `probes/stage/visible-count.js`: BASE kept squares with `opacity > 0.01`, and #160 rejects only `<= 0.01`, so NaN opacity now counts as drawn.
- `export_animation_svg.py`: the exit code 1 on `<script` (BASE `:119-124`) was dropped.
- `build_site.py` / `self_contained.py` no longer scan script text for `url(` as `build_workbench_site.py` did.
- The drift checks in `test_candidate.py:1288-1299` were lost, and the `index-all` sweep can no longer run.
- `animation_from_trace.py`'s summary CLI was dropped.
- None of the browser checkers runs automatically: `check_workbench.py:571-591`, the only gap-bar validity assertion, has no caller in `validate.py` or the workflows (think-kpvc).
- Stale references to the deleted `packing/devtools/bench_annealing.py`: H-207..211 `instrument`, X-029 `sources`, `benchmark.py:450`, `grade_motion.py:208`, and the product plan at `:91` and `:96`.

Restore each unique assertion or record why it is obsolete, under think-cqfc's rule that removal follows preservation of unique assertions.

## Notes

2026-09-14, PR #160 review lane D-tools, items of this bead fixed on #160: the NaN-opacity probe (D88, c0aba3b9); `export_animation_svg` refusing a script and accepting `--out` again (D88, a093ec7a); the self-contained scan of SVG hrefs and script text plus a page CSP (D56, 269fefcc); `check_candidate` retiring its claim over the frozen spike views, building with `--all` and dropping `facts_opacities.js` (D67, 9baad048); stale entry-point references in `grade_motion`, eight instruments, `build_candidate`, `check_candidate`, `capture_video` and the package README (D89, a3d6813f and others). Still open here: the annealing plan's `packing_strategy.py` line (D89, after lane B merges up) and lane C's D44/D45 items. Beads: think-9hky, think-81zr, think-o73e, think-h4kl.

2026-09-14, PR #160 review lane C: X-034's folded `sources` entry is unfolded and names `packages/workbench/src/application.js` instead of the deleted spike page (D44, #160 R20, 43e6a46e); the benchmark's withdrawn claims, unused OUTCOME and the deleted build command are gone (D45, #155 R16 and #160 R23 benchmark item, 03c16a32; TOLERANCES comment in fbc74c0e). Other items belong to lane D-tools (D56, D67, D88, D89).
