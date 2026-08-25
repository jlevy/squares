---
type: is
id: is-01m0vd88eem4tfvmqf7z833eat
title: "PR26 R4: repair exp-012 orphaned provenance and validation claim"
kind: bug
status: open
priority: 2
version: 1
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-frontier-assurance-and-verification.md
labels:
  - review-finding
dependencies: []
parent_id: is-01m0vd6xfaz5p8ccnq6xrnr5x5
created_at: 2026-08-25T02:51:07.085Z
updated_at: 2026-08-25T02:51:07.085Z
---
Source: PR #26 owner review R4. A fresh checkout of head f1d1c2b fails the provenance gate because exp-012 records unreachable commit 5384209 without an annotation at campaign/series/series-000-smoke-and-calibration/experiments/exp-012-h-024-n29-angle-classes.md lines 18, 28, and 60. Add the dated correction-by-addition annotation following exp-001, rerun all 30 steps from the published head, and correct the PR validation report.
