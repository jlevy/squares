---
type: is
id: is-01m26rygs7f0s76v147x0px4cd
title: Reconcile PR149 onto the current v0.4.0 explainer stack and restore CI
kind: task
status: in_progress
priority: 1
version: 10
delegate: root integration lane
labels: []
dependencies: []
child_order_hints:
  - is-01m27m104h8xe13rsy1rn70r2k
  - is-01m27nzye5x8zqy5zhkmkeqy8s
created_at: 2026-09-10T23:02:51.417Z
updated_at: 2026-09-11T09:41:51.751Z
---
PR #149's page-render diagnostic work is currently red only because it predates the session-099 terminal repair in PR #150, and it also modifies the same explainer/PDF surface now advanced by PR #148. Reconcile it onto the current v0.4.0 explainer head, resolve the page-count and generated-artifact context rather than carrying a 17-page assumption, run focused PDF/page tests and the required pre-push gate, push the author branch, retarget it as a clean stack layer above PR #148, update its cost/validation/body, and require all hosted checks to pass. Preserve D-490's measured host-specific evidence and do not claim the underlying nondeterminism cause is solved.

## Notes

PR149 is pushed at d932bccf and retargeted onto PR148. Unique diff seven files, +608/-33. Exact-head focused and pre-push checks pass (5,055 tests; 1,013.93s). Hosted packing, mergeability, and build jobs pass. Firefox/WebKit first runs hit existing think-nnvo font-hold timing assertion; Firefox passed one rerun, WebKit repeated on custom-sans 1280. Artifact shows 18 visible boxes after setup crossed the 3s recovery boundary. Sol-high repair diagnosis is active; full checkpoint and final hosted green remain.
