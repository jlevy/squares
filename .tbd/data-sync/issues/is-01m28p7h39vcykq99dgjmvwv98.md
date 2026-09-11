---
type: is
id: is-01m28p7h39vcykq99dgjmvwv98
title: "[epic] Phase 6: the workbench stops being a prototype"
kind: epic
status: open
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-09-09-packing-strategies-as-a-shared-language.md
labels: []
dependencies: []
created_at: 2026-09-11T16:53:49.786Z
updated_at: 2026-09-11T18:53:57.661Z
---
The page carries a banner calling itself a prototype and the banner is honest: a retained spike, excluded from the lint floor, run by hand, drawing with its own copy of the palette. It is also the thing the owner uses and the thing the video is captured from, and those two facts cannot both keep being true.

Five chunks, each landing on its own, in this order. The banner comes off LAST, because it is what makes the current state honest.

A. One source for the palette
B. The floors (ruff, BasedPyright, and a decision about the JavaScript)
C. The gates run where gates run
D. It reads the contracts
E. It lives where the code lives, and the banner comes off

## Notes

The deployment is ALREADY the one we want, and the conversion does not touch it. build_workbench_site.py writes site/workbench/, pages.yml builds it with --check before the upload, Pages serves it at /workbench/ while the explainer keeps /, and the path filter names its inputs with two tests holding it there. Phase 6 changes what FEEDS that pipeline, not the pipeline.

The first seam is cut as of b0fa05a6: the panel's mathematics is set by render_explainer.katex_css and guarded by render_explainer.EXTERNAL_REFERENCE, so the spike now imports project code rather than carrying its own copy. That is the direction every remaining chunk goes in, and it forced the fix that made the spike importable at all -- build_candidate.py held an absolute path to one worktree, so it only ran from that checkout and would have run silently against the wrong tree from any other.

The conversion table is now in the plan spec under 'The deployment is already the real one'.
