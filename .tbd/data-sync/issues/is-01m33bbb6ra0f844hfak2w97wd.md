---
type: is
id: is-01m33bbb6ra0f844hfak2w97wd
title: Lower the stage's n = headline, with a little more space above it
kind: task
status: closed
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies: []
parent_id: is-01m32t2yc3xenfb97kxn844rc7
created_at: 2026-09-22T01:23:10.166Z
updated_at: 2026-09-22T01:57:09.626Z
closed_at: 2026-09-22T01:57:09.625Z
close_reason: "80f597f9e: #headline top 41 -> 65 stage px, its ink starting near 80 instead of 55.6; gapbar/clearance still holds the space under it (check_animate_view OK)."
resolution: null
duplicate_of: null
---
The owner (2026-09-21): lower the n = ... heading on the stage and put a little more padding above it. The headline currently starts level with the packing's own top edge (assets/workbench.css #headline; the rule is held in animate_view_contract's headline check). Move it down a little, keep it clear of the gap bar under it, and move the rule that pins its place to the new offset so the gate holds the new position rather than the old one.
