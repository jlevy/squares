---
type: is
id: is-01m0vd87w2tepzwdv6fmrk90yj
title: "PR26 R2: preserve unknown historical precision without inventing it"
kind: bug
status: closed
priority: 2
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-frontier-assurance-and-verification.md
labels:
  - review-finding
dependencies: []
parent_id: is-01m0vd6xfaz5p8ccnq6xrnr5x5
created_at: 2026-08-25T02:51:06.498Z
updated_at: 2026-08-25T03:10:52.101Z
closed_at: 2026-08-25T03:10:52.101Z
close_reason: "Resolved in PR #26 rebased head a9a2992. The framework spec and affected bead contracts now incorporate the finding and its attached suggestions; the per-finding disposition is posted at issuecomment-5404553556."
resolution: null
duplicate_of: null
---
Source: PR #26 owner review R2; plan lines 251 and 495-515. Requiring actual precision and tolerance on every migrated numerical record would force invented values where early archives did not retain them. Add a narrowly scoped unrecorded-historical migration value with a dated annotation; require concrete method, precision, and tolerance on every new numerical record and use known historical values only when supported.
