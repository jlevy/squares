---
type: is
id: is-01m0qxpc5jrdzfn205qfxfvg44
title: Correct false research claims and wire every enforcement gate
kind: bug
status: open
priority: 0
version: 7
spec_path: explorations/packing/docs/project/reviews/review-2026-08-23-square-packing-program-and-pr14.md
labels:
  - packing
  - review
  - pr-14
  - technical-error
dependencies: []
parent_id: is-01m0qxka8ebkztq7erex50vvr2
created_at: 2026-08-23T18:21:29.137Z
updated_at: 2026-08-23T20:20:50.095Z
---
Category: technical errors. Correct the false claim that the n = 11 angle itself is algebraic; qualify m^2-3 grid optimality to the proved range; stop deriving small basin volume from rigidity; scope H-020 to the tested n, budget and implementation; replace n = 12 as a negative control; repair stale paths and counts; and distinguish wall time from CPU time and derivative sign from magnitude. Wire atlas_check.py and tools/regression_test.py into test.sh and CI, and fix the README layout drift.

Acceptance: every corrected mathematical statement cites primary evidence and distinguishes proved, computed, conjectured, and proposer-specific claims. The strict gate runs canonical, atlas, quench, exact, regression, schema, link, generated-artifact, and README-layout negative controls. PR CI is green, and introducing each reviewed defect makes a named test fail.

## Notes

2026-08-23 final PR14 reassessment at c412b8c: factual corrections remain applied; checks and historical regressions are wired; uv and Cargo resolution is frozen or locked. F-16 repairs include source-built deep/update runs, selected ladder seeds, convergence enforcement, matching pose/side verification, tier-aligned serialization, count-frequency checks, and atomic refusal. F-17 found raw strict mode skipped deep regeneration and the atlas never exercised a false convergence field; the stack makes strict imply deep and adds a firing negative control. Remaining work includes non-converged promotion policy, oracle versus characterization separation, full poses, criterion evaluators, claim scope, and configured CI.
