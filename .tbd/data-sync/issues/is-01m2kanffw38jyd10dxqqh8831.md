---
type: is
id: is-01m2kanffw38jyd10dxqqh8831
title: "[task] Lane 1: Certificate page PR wall under OR-14 (parallel check jobs, scoped halves, apt cache, geometry split, parallel determinism render, sparse checkout, one PDF draw, cancellable loops, Pages budgets)"
kind: task
status: closed
priority: 1
version: 13
labels: []
dependencies:
  - type: blocks
    target: is-01m2m5ad594cv9k37w6nm9e533
  - type: blocks
    target: is-01m2m5zjmj7dsycs1x6yxwcwwt
parent_id: is-01m2k0eqwj7en422j33wtvw5dt
child_order_hints:
  - is-01m2m59rqzb3m4qjs4h3qca405
created_at: 2026-09-15T20:03:22.746Z
updated_at: 2026-09-16T06:55:03.565Z
closed_at: 2026-09-16T05:03:07.644Z
close_reason: "PR #183 final head is green, mergeable, and measured at 173 s, meeting the lane objective."
resolution: null
duplicate_of: null
---
Lane 1 of epic think-xfqk. Branch claude/ci-pages-parallel in worktree lane-d-tools, PR into main. Items P1-P5 and the Pages section of gate-budgets.yaml (G4 with lane 3), from attic/ci-review/pages.md and synthesis.md in the squares-viz-explanations worktree. Before: 472 s median on stack PRs, about 381 s on PRs into main. Target: a full run in about 3 min and no browser work on PRs outside the workflow's inputs.

## Notes

2026-09-16 completed review repair: PR #183 final head 4e25f5f5 was mergeable/CLEAN and all exact-head checks were green. Sparse/blobless checkout cut the adverse exact-head run from 281 s (workbench 234 s; checkout about 171–174 s) to 186 s, then a final exact-head run to 173 s (workbench 53 s; checkout 8 s). The slowest browser cell was 92 s. Focused 103 tests, 19 workflow tests, edit tier, records tier, page budgets, and deterministic build all passed. think-sqi7 remains intentionally separate because its future probe trees/files did not exist on that branch.

2026-09-16 main reconciliation: after PRs #175 and #178 merged, PR #183 conflicted in the Pages trigger. Head aee9cf0f is a real merge of origin/main at 6e212693. The resolution preserves the PR's per-page scope and no-browser-work skip for unrelated changes, while adding main's new check_published_site probe directory to the push/deploy input filter and retaining main's suite-a/suite-b validation and no-JavaScript contracts. Focused evidence: 35 passed and 6 browser-dependent skipped across the Pages scope/workflow/build/PDF files; 146 passed across Pages scope/workflow, gate budgets, and validation CLI (the two ps-based process tests were rerun outside the restricted sandbox); Ruff and Ruff format passed on the touched Python surface; BasedPyright reported 0 errors, 0 warnings, and 0 notes; the edit tier's substantive checks passed, including 911 Python files, 455 tracked JavaScript sites in 38 files, 182 probes in 3 trees, and 11 declared tiers. The local browser floor could not be rerun because the host had 138 MiB free and the reused node_modules predated main's new typescript-eslint dependency; exact-head GitHub CI is the authority for that lane.

2026-09-16 final-parent reconciliation: main advanced again with merged PR #179 at 8484d616 while the first exact-head run was in flight. Head 0197fc4a is a second real merge, with parents aee9cf0f and 8484d616. The probe/browser-floor extraction merged without conflict and the PR's diff against final main remains the same ten-file Pages change. After that merge, all 146 focused Pages scope/workflow, gate-budget, and validation-CLI tests passed (144 in the restricted runner plus the two ps-dependent process-tree tests outside it). The final no-JavaScript contracts passed over 910 Python files with 331 tracked sites in 25 files and 249 probes across 5 trees. Exact-head GitHub CI is green and GitHub reports CLEAN against base 8484d616: both required aggregates, all six packing lanes, mergeability, and all Pages cells passed. The slowest Pages cell was browser-geometry WebKit at 145 seconds; prepare was 48 seconds and workbench was 59 seconds.
