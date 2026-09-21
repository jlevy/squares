---
type: is
id: is-01m31gpgmxd034echmxq2peq0s
title: Gate the archive annotation census
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m31gn7263sfhfbq8xfabkh3p
created_at: 2026-09-21T08:18:10.190Z
updated_at: 2026-09-21T08:18:10.190Z
---
PR 204 review finding F4 (Medium). AGENTS.md makes the count the guarantee - repairs flagged inline and counted in the archive README - and PR 204 moves Bentz 2016 from 3 to 7 across packing/resources/README.md:128, the file banner, and the D-505/D-506 fix fields. It is correct (hand-verified 7 markers = banner = README) but nothing under packing/devtools/ or packing/tests/ recomputes it, while the defect count is gated end to end. A miscount would pass every gate and silently degrade the one ground-truth boundary the repo keeps against an external source.
