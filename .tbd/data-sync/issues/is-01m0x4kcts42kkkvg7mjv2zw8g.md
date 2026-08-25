---
type: is
id: is-01m0x4kcts42kkkvg7mjv2zw8g
title: "PR37-F1: reconcile colliding defect IDs and generated views"
kind: bug
status: closed
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01m0x4c75pqtywfdr4cfnzzvhp
created_at: 2026-08-25T18:58:23.705Z
updated_at: 2026-08-25T19:11:20.451Z
closed_at: 2026-08-25T19:11:20.434Z
close_reason: "Fixed in b450072: merged current main, integrated the two findings as D-326/D-327, and regenerated the 327-entry views and synopsis aggregates."
resolution: null
duplicate_of: null
---
PR #37 adds D-320 and D-321, but current main already owns D-320 through D-325. Merge main into the review branch, preserve the stale-aggregate finding as a newly numbered historical defect, assign the compound-adjective defect the next available ID, and regenerate every derived aggregate and view.
