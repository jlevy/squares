---
type: is
id: is-01m0vd89nj4857zbx0kmt9g4r5
title: "PR26 R8: describe UnitSquare gaps accurately and protect the H-030 holdout"
kind: bug
status: open
priority: 3
version: 1
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-frontier-assurance-and-verification.md
labels:
  - review-finding
dependencies: []
parent_id: is-01m0vd6xfaz5p8ccnq6xrnr5x5
created_at: 2026-08-25T02:51:08.337Z
updated_at: 2026-08-25T02:51:08.337Z
---
Source: PR #26 owner review R8; plan lines 128 and 526. The n=68 and n=69 frontier pages already report UnitSquare values and the assurance gap; the missing work is typed conflict evidence and independent replay. Correct the framing and update think-po2i so adjudication cannot publish held-out child geometry or otherwise unblind preregistered H-030 before its test is settled or versioned.
