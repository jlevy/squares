---
type: is
id: is-01m0qxpc5jrdzfn205qfxfvg44
title: Correct false research claims and wire every enforcement gate
kind: bug
status: open
priority: 0
version: 6
spec_path: explorations/packing/docs/project/reviews/review-2026-08-23-square-packing-program-and-pr14.md
labels:
  - packing
  - review
  - pr-14
  - technical-error
dependencies: []
parent_id: is-01m0qxka8ebkztq7erex50vvr2
created_at: 2026-08-23T18:21:29.137Z
updated_at: 2026-08-23T19:50:07.456Z
---
Category: technical errors. Correct the false claim that the n = 11 angle itself is algebraic; qualify m^2-3 grid optimality to the proved range; stop deriving small basin volume from rigidity; scope H-020 to the tested n, budget and implementation; replace n = 12 as a negative control; repair stale paths and counts; and distinguish wall time from CPU time and derivative sign from magnitude. Wire atlas_check.py and tools/regression_test.py into test.sh and CI, and fix the README layout drift.

Acceptance: every corrected mathematical statement cites primary evidence and distinguishes proved, computed, conjectured, and proposer-specific claims. The strict gate runs canonical, atlas, quench, exact, regression, schema, link, generated-artifact, and README-layout negative controls. PR CI is green, and introducing each reviewed defect makes a named test fail.

## Notes

2026-08-23 stacked-review progress: factual angle, m-squared-minus-3, n=17, gap-rank, round-count, and hypothesis-count corrections remain applied; regression and atlas/golden checks are wired; project uv invocations and Cargo builds are frozen or locked. Reassessment of PR14 head 5b1ae653 adds F-16: the committed golden did not reproduce from the source-built engine, asserted exact discovery-map drift while saying discovery was not asserted, serialized below its numerical floor, could verify a pose different from the reported minimum side, and wrote an invalid replacement before reporting oracle failure. The stack builds the engine, records the selected ladder seed, uses an n=10 control seed that reaches the intended basin, enforces converged ladder results, aligns precision with the tier floor, keeps the matching pose, and checks failures before atomic update. Remaining acceptance work includes the non-converged atlas policy, characterization-versus-oracle separation, rigidity and rarity claims, H-020 scope, n=12 control role, timing and derivative labels, and CI.
