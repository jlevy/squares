---
type: is
id: is-01m4h9s465x7mphy1xxkmdyqc9
title: Refresh generated credit inventories and fix final validation consistency failures
kind: bug
status: in_progress
priority: 1
version: 6
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4h26vpd0pe8frzehv70rt4p
child_order_hints:
  - is-01m4h9vctvqc2xap8b7hb68bt0
  - is-01m4hdhajg6838p3qzbme41s30
  - is-01m4he3z4mvvt28t2xgba2b9hw
hold: null
hold_until: null
created_at: 2026-10-09T21:40:48.440Z
updated_at: 2026-10-09T22:56:38.034Z
started_at: 2026-10-09T21:40:56.042Z
---
Final b4b127c54 push validation found Ruff smart apostrophes in test_bound_citations.py, stale site URL register/docs, and stale T-007 consumer audit after the dedicated Ahmed attribution rename and upstream integration. Reproduce at frozen source, make narrow corrections using maintained generators, preserve handles and source custody, verify lint and both generated-record checks, then requalify PR474. Track any independently confirmed fixture-lifetime failure in the same final-validation repair slice.

## Notes

Committed51e8d39d1 repairs generated site URL dates, T007 Ahmed credits, three Ruff punctuation errors and E3 Playwright fixture lifetime; all65 edit checks now pass. The normal push slice sinceb4 timed out at900s:4227 passed,32 skipped,11 actual failures before92pct completion, no full pytest verdict. Narrow independent test repairs in flight across three disjoint private clones: known_best_atlas (4 print stale expectations), site_atlas_views+overview (3 web contracts), paper_structure+n11_lower_bounds_explainer (4 paper/credit/canvas contracts). Root owns source/Git/beads and will apply only supported fixes, rerun required push gate and current-head hosted full validation; no guard/budget relaxation.
