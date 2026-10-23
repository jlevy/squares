---
type: is
id: is-01m5karnxfykw9p1teb6p4t3pa
title: Refresh suite partition record from complete hosted reports
kind: task
status: closed
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-10-22-site-navigation.md
delegate: sol-upstream-final
labels: []
dependencies: []
parent_id: is-01m5k19kqedc9vp30sk9wm3s5f
hold: null
hold_until: null
created_at: 2026-10-23T02:52:13.101Z
updated_at: 2026-10-23T02:55:26.032Z
started_at: 2026-10-23T02:52:21.728Z
closed_at: 2026-10-23T02:55:26.030Z
close_reason: Generated suite-file-costs.json from all four successful hosted integration-suite cost reports of main run 39883305639 (SHA 4ad09803c); preserved four-shard target ceilings. Current-tree check 839 files, worst shard 9/195 unrecorded (4.6%); focused real-tree contract passed. Committed/pushed de99072dd.
resolution: null
duplicate_of: null
---
Current-head suite-d fails suite_files real-tree cap: shard 3 has 23/227 unrecorded test files (10.1%), including new site_source_actions. Refresh the partition using devtools.suite_files record from complete hosted cohort reports only; verify focused contract and stage for coordinator.
