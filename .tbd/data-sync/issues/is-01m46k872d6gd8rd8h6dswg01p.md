---
type: is
id: is-01m46k872d6gd8rd8h6dswg01p
title: "T-083 and T-084: C2 needs a machine check of Proposition 5.1 (#295)"
kind: task
status: closed
priority: 2
version: 5
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-05T17:54:41.357Z
updated_at: 2026-10-06T17:02:04.987Z
started_at: 2026-10-06T07:56:23.783Z
closed_at: 2026-10-06T17:02:04.986Z
close_reason: "Done and on main via #382 (d087422ed); reply posted 2026-10-06 and recorded"
resolution: null
duplicate_of: null
---
Lane E's reply audit (think-syk6) found no bead owning the C1 -> C2 step for T-083 and T-084 (V3/C1): a machine check of Proposition 5.1. Until it lands, check_requests keeps #295 from closing although everything wand125 asked there is done.

## Notes

2026-10-06 (lane R6, think-wyf4): the machine check is done; the review lane is not, so the exit is staged.

- d7f2c6186 (lane branch claude/ecstatic-pascal-pothtx-r6): devtools.check_karakus_strip_measure decides Proposition 5.1 by an exact Fraction branch and bound over tau = tan(theta/2) in [0, 5/12], lambda in [1, 101/100] and the cut height. Part A (only y = 1 cuts, 0 < u <= 1) closes in 5,939 leaves to depth 34: 5,933 by margin, 2 by area (F >= lambda^2), and 4 corner leaves at the tight floor square, where F - 1 = (lambda - 1)(lambda + 1/2), closed by an exact expansion in lambda - 1 (20 sympy identities). Part B (both strip lines cut) closes in one box: E(v) >= 0 for v <= 3/7, which is where 101/100 is used. The receipt holds the cover as a preorder tree; the default mode re-decides every leaf from it, reruns the search and compares. Controls: point mass 49/100, line density 49/100 and rows at 3/5 are each refused with a counterexample the search finds. The test holds the closed form to check_nagamochi_lemma1_counterexample's polygon scorer on 195 explicit squares and samples the proposition on 1,200 squares, half cut by both lines. Corollary 6.2's algebra is checked at all 301 nonsquare N in [8, 323]. CPU: 3.3 to 3.9 s per run.
- 28ffccc7c and b5778dbbe (side branch claude/ecstatic-pascal-pothtx-r6-exit): the exit. E-karakus-strip-measure-interval and V-check-karakus-strip-measure; T-083 and T-084 to V3/C3 (check_results derives C3); 203 case records; the stage's lines "(confirmed T-083)"; re-pin.
- Not done: the separately prompted adversarial review. Launching claude -p was refused by this session's permission classifier. It is think-lpul; merge the exit only when that review accepts.

2026-10-06, later: the exit is on the lane branch. The coordinator ran the separately prompted review from the lane's prompt; it accepts with non-blocking findings 1–6 and assesses V3/C3 for both results.
- c77b29307 stores the review byte-identical as docs/project/reviews/review-2026-10-06-karakus-proposition-5-1-machine-check.md, adds it to T-083's and T-084's reviews, and dispositions all six findings. The evidence entry is exact-algebraic and audited here, as the review recommends.
- 396f9beb8 re-pins.
check_results derives C3 for both results. Close this bead at R6's merge.
