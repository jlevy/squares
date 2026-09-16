---
type: is
id: is-01m2m4bsq5e2q16gvhcczxv4p5
title: "PR #178 review R3: the allowlist header still reports 460 sites in 42 files"
kind: bug
status: closed
priority: 3
version: 2
labels: []
dependencies: []
parent_id: is-01m2m4brc46s3a2pqbaqthnyz7
created_at: 2026-09-16T03:32:28.515Z
updated_at: 2026-09-16T06:17:01.664Z
closed_at: 2026-09-16T06:17:01.664Z
close_reason: "Resolved by final parent merge: the allowlist header no longer carries a stale running total, and the live inventory is 455 sites in 38 files."
resolution: null
duplicate_of: null
---
packing/devtools/embedded-javascript.yaml:55-58. Shared text; #179 removes the running totals. (PR #178, review 5218208269)
