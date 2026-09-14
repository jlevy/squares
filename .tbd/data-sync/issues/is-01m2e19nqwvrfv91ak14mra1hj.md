---
type: is
id: is-01m2e19nqwvrfv91ak14mra1hj
title: "F6c: reject two-process supervisor and route-child parent cycles"
kind: bug
status: closed
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - calibration
  - admission
dependencies: []
parent_id: is-01m2dz5kzv8k9e1yq06017ngah
created_at: 2026-09-13T18:43:26.588Z
updated_at: 2026-09-14T02:25:01.335Z
closed_at: 2026-09-14T02:25:01.335Z
close_reason: "Accepted by docs/project/reviews/review-2026-09-13-n11-bc329-reader-f6f7-final.md at a5701e73 (23/23 independent full-binder controls); a5701e73 is an ancestor of PR #156 head 2f8925b2 and the reader blob 34d48ee0 is unchanged at #156, #157 and #166. Verified 2026-09-14 by the n11 stack landing audit (think-j007)."
resolution: null
duplicate_of: null
---
At exact reader head 7e4d2487, full readback accepts coordinator PID 101 with PPID 201 while route child PID 201 has PPID 101. Require every route child/task PID to differ from coordinator PPID as well as PID; retain coherent mutation and legal pool control. Evidence: docs/project/reviews/review-2026-09-13-n11-bc329-reader-rereview.md.
