---
type: is
id: is-01m0vd8852z3m41ebezkbmqdgk
title: "PR26 R3: distinguish ceremonial digests from staleness guards"
kind: bug
status: closed
priority: 2
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-frontier-assurance-and-verification.md
labels:
  - review-finding
dependencies: []
parent_id: is-01m0vd6xfaz5p8ccnq6xrnr5x5
created_at: 2026-08-25T02:51:06.785Z
updated_at: 2026-08-25T03:10:52.109Z
closed_at: 2026-08-25T03:10:52.109Z
close_reason: "Resolved in PR #26 rebased head a9a2992. The framework spec and affected bead contracts now incorporate the finding and its attached suggestions; the per-finding disposition is posted at issuecomment-5404553556."
resolution: null
duplicate_of: null
---
Source: PR #26 owner review R3; plan lines 357 and 378-387; implementation bead think-4fcn. Remove reader-facing hashes that merely restate Git-tracked source identity. Retain or replace embedded-source pins only where they catch the named failure that a corrected archive no longer matches hand-transcribed tuples in a replay checker, and document that purpose at each retained site. Resolve S6 by replacing blanket check aspirations with the reactive rule: when a consequential defect escapes all checks, add the smallest check that prevents recurrence.
