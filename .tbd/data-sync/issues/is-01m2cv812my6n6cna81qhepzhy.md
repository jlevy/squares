---
type: is
id: is-01m2cv812my6n6cna81qhepzhy
title: "PR #157 review MATH-03: independent witness checker counts sites, not tokens"
kind: bug
status: closed
priority: 2
version: 2
labels:
  - n11
dependencies: []
parent_id: is-01m2cv7affzce4qkz704rp2kvv
created_at: 2026-09-13T07:38:26.772Z
updated_at: 2026-09-13T08:11:10.010Z
closed_at: 2026-09-13T08:11:10.010Z
close_reason: "Fixed: exact_charge_at_witness (threshold_interval.py:380-390) now sums multiplicities in its own local sum() over zip(points, multiplicities), deliberately NOT via trace_count, so the independent check stays independent. Verified on the review's exact repro -- sites (1,1),(3/2,1), multiplicities (2,2), k=4, w=1, L=3, B=9/10, witness (1.25,1.0) at direction 0: tokens inside 4 vs threshold 4, true charge 1; witness charge 0 before, 1 after. This is the most severe of the three math findings and the disposition map should say so: it is reachable through the public verify_threshold_by_intervals (called at threshold_interval.py:633 on every refuting or pinned-below-one outcome), where confirmed = all(admissible and charge < 1) turned a genuinely charged centre into status 'fails' -- a FALSE REFUTATION of a correct weighted certificate, the exact thing the module docstring claims cannot happen. Regression: test_the_witness_charge_counts_tokens_and_not_sites."
resolution: null
duplicate_of: null
---
packing/src/sqpack/fractional/threshold_interval.py:365 counts one per site. Repro: sites (1,1),(3/2,1), multiplicities (2,2), threshold 4, weight 1, L=3, B=9/10, direction-zero witness (1.25,1.0): true charge 1 but the checker reports admissible charge 0. Fix: independently sum multiplicities in the exact witness routine; retain a weighted exact-witness regression.
