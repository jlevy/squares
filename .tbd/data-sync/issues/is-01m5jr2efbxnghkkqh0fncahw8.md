---
type: is
id: is-01m5jr2efbxnghkkqh0fncahw8
title: "Nav-switch benchmark devtool: click-to-settled timing with and without prerender"
kind: task
status: open
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m5jr2cr74kbbn71j05pqsgkd
created_at: 2026-10-22T21:25:30.219Z
updated_at: 2026-10-23T01:30:27.482Z
---
OR-1: the 2026-10-22 measurements were one-off scratch scripts (local mirror server with gzip + max-age=600, a beacon probe, and headless Chromium launched without DevTools so prerendering works). Build it into packing/devtools with a probe file, so the numbers in the epic can be re-measured before and after each follow-up.

## Notes

From the #740 review: when the tool exists, also measure on a phone profile. Chrome on mobile triggers moderate eagerness from viewport heuristics (500 ms after scrolling stops, near the last tap), so phones pay prerender cost without hover intent. Candidate narrowing to test: moderate for '.site-nav a, a.site-action', conservative (press) for other links.
