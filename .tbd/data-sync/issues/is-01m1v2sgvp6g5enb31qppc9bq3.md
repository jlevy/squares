---
type: is
id: is-01m1v2sgvp6g5enb31qppc9bq3
title: Audit and disposition the post-3.81 dilation lower-bound corollary
kind: bug
status: closed
priority: 0
version: 6
labels:
  - mathematics
  - release-blocker
dependencies:
  - type: blocks
    target: is-01m1v2yhy02qmka8ez4d2f5bde
parent_id: is-01m1tvqp2v2js8437xek2xk2gz
created_at: 2026-09-06T10:04:00.245Z
updated_at: 2026-09-06T11:14:24.389Z
closed_at: 2026-09-06T11:14:24.389Z
close_reason: T-022 is integrated and independently accepted at C5. Exact weak bound is 38100*sqrt(8100042893309449)/899996306539 = 3.810025723614703407...; proof-record SHA-256 16a52d54b95cbcdf7e97eab3b40b829ca24126141b7914ff224d2794af47d442; endpoint and strictness limits are explicit; focused, record, edit, and fast checks passed.
resolution: null
duplicate_of: null
---
The current n=11 case page already records a proved dilation corollary s(11) >= 95250381/25000000 = 3.81001524 while T-018 and planning surfaces call 3.81 the current registered endpoint. At max reasoning, audit the dilation theorem and exact arithmetic; determine whether arbitrary rational scaling below c = 1/(B(1+D)) plus the infimum definition proves the sharper supremum s(11) >= 3429000000000/899996306539 (about 3.81001564), whether compactness/attainment is needed, and what finite certificate/checker evidence survives scaling. Promote only after an independent proof audit and exact tests; otherwise state the register policy and reconcile every current-facing surface. Preserve 3.81 provenance and do not overclaim strictness.

## Notes

T-022 integrated on the continuation branch as 6b4cde0a. Exact weak bound: 38100*sqrt(8100042893309449)/899996306539 = 3.810025723614703407..., from the sharpened squared containment inequality and rational-density/upward-embedding limit. The endpoint is not certified and no strict inequality is claimed. Proof-record SHA-256 16a52d54b95cbcdf7e97eab3b40b829ca24126141b7914ff224d2794af47d442; coordinator replay passed in 7.80s. Author focused 105 tests, records/edit, Ruff, and targeted type checks passed. Fast tier: 2220 passed, 1 skipped, 150 deselected; 3 sandbox-denied socket/forkserver cases passed separately outside sandbox. Independent review transport is pending exact-head integration before closure.
