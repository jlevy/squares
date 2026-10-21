---
type: is
id: is-01m5fpym28xzgmka3ym4q3e7pf
title: "PR #706 (merge): T-223 stage 4 and adoption at 204 and 260 (#678)"
kind: task
status: in_progress
priority: 1
version: 4
delegate: coord-intake-1021b
labels: []
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-21T17:08:13.000Z
updated_at: 2026-10-21T18:40:23.737Z
started_at: 2026-10-21T17:08:19.050Z
---

## Notes

2026-10-21 coord: #712 review A3 — the reply #706 owes #678 must also say #678's 343 row is superseded by #702's (evand-n343-sweep-2026-10-20), once #712 merges. check_requests will not flag it.

2026-10-21 c-lane-706-refresh (phase 1): merged origin/main 51ac9d7ee into #706 (merge a6db78d19, no rebase); paper no-public-change record f8b1837df; re-pin 7831b00b1; test fix e8f964eda. Pushed head e8f964eda; nothing unpushed. No site edition cut (phase 2). Hosted at e8f964eda: all green but validate (site edition only) and suite-d (custody receipt snapshot_source_bytes 232,929,700 > cap 232,783,872; waits on #714). Next step: phase 2 after #704 merges — merge main, re-adopt 260 from T-196, re-run custody/censuses/screen/views/paper record/site_urls, re-cut the site.
