---
type: is
id: is-01m0qxpc5jrdzfn205qfxfvg44
title: Correct false research claims and wire every enforcement gate
kind: bug
status: open
priority: 0
version: 11
spec_path: explorations/packing/docs/project/reviews/review-2026-08-23-square-packing-program-and-pr14.md
labels:
  - packing
  - review
  - pr-14
  - technical-error
  - focus-process
  - focus-correctness
dependencies: []
parent_id: is-01m0r7q3f92dgx66d30wwrasbn
created_at: 2026-08-23T18:21:29.137Z
updated_at: 2026-08-23T21:48:03.904Z
---
Category: technical errors. Correct the false claim that the n = 11 angle itself is algebraic; qualify m^2-3 grid optimality to the proved range; stop deriving small basin volume from rigidity; scope H-020 to the tested n, budget and implementation; replace n = 12 as a negative control; repair stale paths and counts; and distinguish wall time from CPU time and derivative sign from magnitude. Wire atlas_check.py and tools/regression_test.py into test.sh and CI, and fix the README layout drift.

Acceptance: every corrected mathematical statement cites primary evidence and distinguishes proved, computed, conjectured, and proposer-specific claims. The strict gate runs canonical, atlas, quench, exact, regression, schema, link, generated-artifact, and README-layout negative controls. PR CI is green, and introducing each reviewed defect makes a named test fail.

## Notes

2026-08-23 merged-head delta: D-055/D-056/D-057/D-063 correct theorem scope and logic prose; D-062 replaces the executable n=12 rejection with a proved n=16 control while preserving n=12 as discovery; D-060/D-064 restore strict/deep and in-gate preflight mutation coverage; D-065 derives the README's gate-soundness claim. Full normal gate passed in 108s with 24 negative controls and 65 defects. Remaining acceptance work includes outstanding reviewed defects and configured PR CI.
