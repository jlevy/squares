---
type: is
id: is-01m4wds2z1rdbysrsxkj78mzka
title: Make the font-shift negative control deterministic without relaxing CLS limits
kind: bug
status: closed
priority: 1
version: 3
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m4wcjctchxg9qv8jp0za5g13
hold: null
hold_until: null
created_at: 2026-10-14T05:22:20.256Z
updated_at: 2026-10-14T07:21:25.595Z
started_at: 2026-10-14T05:22:31.908Z
closed_at: 2026-10-14T07:21:25.595Z
close_reason: Fixed, independently reviewed, and merged in regularization stack main9f48ccc80cee8dcf94c7cadbcaded01408f94fa2; exact-head Packing and Pages CI pass. Deployment tracked by parent think-azzv.
resolution: null
duplicate_of: null
---
The unadjusted-font negative control produced CLS 0.0028717770655270654 on local Chromium instead of exceeding the unchanged 0.1 floor, although final font readability and geometry assertions passed. The implemented cleanup makes the intentionally bad fallback/arrival protocol deterministic so it demonstrates the failure it is meant to catch without depending on host font metrics or weakening production CLS checks. Relevant strong-lane validation: the font-arrival/control cases passed within the 149 browser tests. Keep in progress until final gate and merge.
