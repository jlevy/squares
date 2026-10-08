---
type: is
id: is-01m4eyh9kr2djjzbxdtnpa8w9w
title: "Atlas poster footer: put citations and repository URL last"
kind: task
status: open
priority: 3
version: 1
spec_path: docs/project/reviews/review-2026-10-06-n17-w3-consolidation.md
delegate: sol-merge-engineering
labels:
  - atlas
dependencies: []
parent_id: is-01m4eq9mdaejkedd1b09qqn09p
created_at: 2026-10-08T23:45:48.663Z
updated_at: 2026-10-08T23:45:48.663Z
---
Completed the user-requested atlas poster footer adjustment in /Users/levy/.codex/worktrees/atlas-cleanups/squares.

The final two lines are "Citations and details in The Squares Project" and "github.com/jlevy/squares". Diagram credit and release stamp precede them. The URL uses footer size 57 instead of 78, black #000000, and both final lines are right aligned at x=6369 with text-anchor=end. Closing baselines are credit1756, release1861, citations1966, URL2071; overlap/bounds checks follow this order.

Changed only the minimal footer source/related existing assertions in packing/devtools/build_known_best_atlas.py and packing/tests/test_known_best_atlas.py, plus the requested poster family: packing/atlas/known-best/known-best-1-324.svg, known-best-1-324.png and square-packings-324-20261008.pdf. The complete SVG is identical outside the four closing text nodes; five figure-family assets remained unchanged. PNG/PDF source receipts match SVG SHA256 bb6a9075fb1c33995c1f8f72058c7d0dea7ad9e47454f7973050f82cd3603682. Actual published PNG footer was visually verified; original dirty poster bytes retained for recovery.

Five focused existing pytest controls PASS (7.03s pytest /8.517s process), Ruff lint/format and configured BasedPyright clean. The existing retained-footer assertion was invoked directly after publication and passed without pytest temporary/capture/cache files. This is a bounded local visual/source/export result, not full/current CI qualification.

Work remains uncommitted in the dirty atlas-cleanups worktree: unrelated edits and pre-existing staging were preserved, no files staged/reset/reverted, no commit or push. Source-only three-file publication used maintained renderer RAM buffers and destination-local atomic publication; actual external ENOSPC was documented, with no disposable scratch/cache fallback.

Evidence in primary ignored attic/n17-merge-readiness-20261008/: atlas-footer-order-tests.json; atlas-footer-readonly-export-analysis.json; atlas-footer-renderer-io-evidence.json; atlas-footer-poster-only/published.json; atlas-footer-final-verification.json; atlas-footer-published-crop.png. Original bytes: atlas-footer-poster-only/before/. No source edits/tests/builds were run for bookkeeping.
