---
type: is
id: is-01m5kjds5y8w5nc6ygd5nhkd12
title: "Stage 4 mathematical review of T-231: Polkovskyi's lower s(204) side, n204.cert at 12fc466 (#719)"
kind: task
status: closed
priority: 1
version: 4
delegate: c-review-t231-math
labels:
  - result-import
  - validation
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
hold: null
hold_until: null
created_at: 2026-10-23T05:06:04.606Z
updated_at: 2026-10-24T08:26:42.135Z
started_at: 2026-10-23T05:06:05.506Z
closed_at: 2026-10-24T08:26:42.135Z
close_reason: "T-231's stage 4 review landed on main: docs/project/reviews/review-2026-10-23-mishapolk-n204.md and the packet's review/review-2026-10-23/ (merged with #753, 5f5294d82)."
resolution: null
duplicate_of: null
---

## Notes

2026-10-23 06:14Z c-review-t231-math: review written, not committed (read-only lane). Verdict: accepted, for finite feasibility only; 7 findings, none blocking (RF-1 minor; RF-2 to RF-7 notes). Significance S2 (by T-225's precedent; S1 is the by-kind alternative, stated).

Result: s(204) <= 14808642830513087197802415708703/10^30 (certificates/n204.cert at Mishapolk/square-packing-records@12fc4667, SHA-256 9c5dabc8...3e7d, blob 4117e9d). Walls >= 5e-21 exactly (left, bottom) and 5.00000000068827e-21 (right, top); least pair gap 9.99999999999998720936e-21 at (63, 84), equal to their Euclidean distance. Below T-229 by 14809457954896291297/10^30 and below every earlier report at 204 and every bound at 205-224.

Deciders: own clean-room checker (routes Z integers, C Fraction+clipping; 2c8053b1...) and both maintained routes (exact_verify, independent) via evand-cert adapter + kernel run_case/validate_job; 63/63 shared numbers equal, including the records lane's receipt at 15ecb0a68. 16 sharp/gross/reader mutants as expected on all 4 deciders; kernel run_sharp exact.

Identity/lineage: T-229 is this certificate dilated about the corner by 1 + 1.000055e-12 (to 2.9e-15, same tilts): one solved point at two paddings. The side equals Daniel's exactsolve S' for T-229's witness (project run of 22 Oct, rerun here reproduces input digest and view blobs); 119/204 rows byte-identical to the solve's certificate; the 85 others are exactly the solver's 21 free squares and the 64 squares of its frozen flat variables. Frame = Couzo #678's (as T-229). Author's accounts omit the solver (RF-1, question 1).

Outputs (scratch, for the records lane to commit): /tmp/claude-0/-home-user-squares/f8504540-2b5a-5f78-8968-eb4ffa4c4b64/scratchpad/review-t231/ (docs/project/reviews/review-2026-10-23-mishapolk-n204.md; packing/resources/web/mishapolk-n204-2026-10-22/review/review-2026-10-23/; record-changes.md).
