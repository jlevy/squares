---
type: is
id: is-01m0qxpc5jrdzfn205qfxfvg44
title: Correct false research claims and wire every enforcement gate
kind: bug
status: open
priority: 0
version: 3
spec_path: explorations/packing/docs/project/reviews/review-2026-08-23-square-packing-program-and-pr14.md
labels:
  - packing
  - review
  - pr-14
  - technical-error
dependencies: []
parent_id: is-01m0qxka8ebkztq7erex50vvr2
created_at: 2026-08-23T18:21:29.137Z
updated_at: 2026-08-23T18:53:40.818Z
---
Category: technical errors. Correct the false claim that the n = 11 angle itself is algebraic; qualify m^2-3 grid optimality to the proved range; stop deriving small basin volume from rigidity; scope H-020 to the tested n, budget and implementation; replace n = 12 as a negative control; repair stale paths and counts; and distinguish wall time from CPU time and derivative sign from magnitude. Wire atlas_check.py and tools/regression_test.py into test.sh and CI, and fix the README layout drift.

Acceptance: every corrected mathematical statement cites primary evidence and distinguishes proved, computed, conjectured, and proposer-specific claims. The strict gate runs canonical, atlas, quench, exact, regression, schema, link, generated-artifact, and README-layout negative controls. PR CI is green, and introducing each reviewed defect makes a named test fail.

## Notes

2026-08-23 stacked-review progress: corrected the angle claim, qualified the m-squared-minus-3 theorem, reconciled the n=17 decimal, gap rank, round and hypothesis counts, and README atlas layout; regenerated the strategy table; tools/regression_test.py now runs in the green strict gate. Remaining acceptance work includes rigidity and rarity claims, H-020 scope, the n=12 control role, timing and derivative labels, CI, and repairing then wiring the still-red atlas check.
