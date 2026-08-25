---
type: is
id: is-01m0vd89acg6qbqhjfvxygx60w
title: "PR26 R7: state the schema and semantic-checker enforcement split"
kind: bug
status: open
priority: 3
version: 1
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-frontier-assurance-and-verification.md
labels:
  - review-finding
dependencies: []
parent_id: is-01m0vd6xfaz5p8ccnq6xrnr5x5
created_at: 2026-08-25T02:51:07.979Z
updated_at: 2026-08-25T02:51:07.979Z
---
Source: PR #26 owner review R7; plan lines 282-289. Replace claims that the schema alone rejects cross-field rules with the actual contract split: schema where expressible and semantic checker otherwise. Incorporate S5 by restating that beat_record true requires assurance verified, and S9 by defining when new v1 artifacts stop being accepted and when remaining historical v1 records must be migrated.
