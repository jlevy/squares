---
type: is
id: is-01m68j95k4h00b9dwww5sz44jc
title: Print a zero displacement as 0, and take sharp controls below sub-1e-30 margins (RV-10, RV-8 of the 31 October Polkovskyi review)
kind: chore
status: open
priority: 3
version: 1
labels: []
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
created_at: 2026-10-31T08:47:36.548Z
updated_at: 2026-10-31T08:47:36.548Z
---
Two notes of docs/project/reviews/review-2026-10-31-polkovskyi-846-and-23-oct.md (#852), on shared tooling, filed rather than fixed in the records pull request because each changes code whose receipts other packets hold.

- RV-10: `_root` in packing/devtools/check_half_angle_area.py (about line 570) formats a Decimal zero with `.6e`, which Python renders as `0.000000e+6`. The identity receipts of mishapolk-issue846-2026-10-30 at 105, 146, 156, 229 and 308 (measure/identity-nNNN.json, `largest_displacement`), both Polkovskyi packet READMEs, and pingyou-pr622-certificate-2026-10-15/review/outputs/third-route.json (`least_distance`) carry it. Fix: print zero as `0`; re-render the five identity receipts and the READMEs; check that no receipt-equality test binds the old text. The register's prose already says 0 (T-260).
- RV-8: `upper_bound_reports PACKET sharp-controls` steps 1e-30 past contact. At 156 (#846) the certificate's margins are 4e-41 at the walls and 1e-40 between pairs, and at the nine 23 October counts the walls clear by 5e-31, so the controls do not show the routes exact at the certificate's own scale (both routes are exact Fraction arithmetic by construction, and the review's own controls at 1e-60 refused past contact). Fix: take an epsilon below the certificate's least margin where that is below 1e-30, or have the receipt say the epsilon exceeds it; re-run the sharp controls of the two Polkovskyi packets.

Neither holds a rung or an adoption. Depends on nothing.
