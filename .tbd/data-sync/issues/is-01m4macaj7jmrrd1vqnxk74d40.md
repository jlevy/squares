---
type: is
id: is-01m4macaj7jmrrd1vqnxk74d40
title: Merge upstream site layout into contributor profiles and verify combined publication
kind: task
status: closed
priority: 2
version: 6
spec_path: docs/project/specs/active/plan-2026-10-10-contributor-profiles.md
delegate: claude-code@vm
labels: []
dependencies: []
parent_id: is-01m4kvnfe7f9nak96hc7bgdwer
child_order_hints:
  - is-01m4mafs7sfpch465k5p9fbg0f
hold: null
hold_until: null
created_at: 2026-10-11T01:49:00.870Z
updated_at: 2026-10-13T07:36:45.245Z
started_at: 2026-10-11T01:49:31.026Z
closed_at: 2026-10-13T07:36:45.244Z
close_reason: "Accepted on PR #578 head 5e09548cf: every hosted check green, mergeable clean. The push gate's reachable step covers 579 of 767 test files for this branch (68 min at -n 3 on a 4-CPU container), so its 900 s ceiling is capacity, not a hidden failure. Of the 6 local failures, 2 were merge leftovers fixed in 11ceaab32; 4 (two process-group reaping, two Playwright build 1234 missing) fail identically on main in that container and pass in hosted CI."
resolution: null
duplicate_of: null
---
Follow merge-upstream shortcut: fetch and stack preflight, reconcile main6038af33c site layout with contributor profiles, preserve shared overlays and reviewed credits, validate, push PR490 and await CI.

## Notes

Taken over by claude-code@vm on 2026-10-13 at the owner's request; continuing on branch claude/admiring-goodall-q8xeuh from PR #490's head.
