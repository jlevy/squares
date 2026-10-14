---
type: is
id: is-01m4wds2z1rdbysrsxkj78mzka
title: Make the font-shift negative control deterministic without relaxing CLS limits
kind: bug
status: in_progress
priority: 1
version: 2
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m4wcjctchxg9qv8jp0za5g13
hold: null
hold_until: null
created_at: 2026-10-14T05:22:20.256Z
updated_at: 2026-10-14T05:22:31.908Z
started_at: 2026-10-14T05:22:31.908Z
---
The unadjusted-font negative control produced CLS 0.0028717770655270654 on local Chromium instead of exceeding the unchanged 0.1 floor, although final font readability and geometry assertions passed. The implemented cleanup makes the intentionally bad fallback/arrival protocol deterministic so it demonstrates the failure it is meant to catch without depending on host font metrics or weakening production CLS checks. Relevant strong-lane validation: the font-arrival/control cases passed within the 149 browser tests. Keep in progress until final gate and merge.
