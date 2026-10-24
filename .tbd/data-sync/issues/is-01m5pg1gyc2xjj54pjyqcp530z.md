---
type: is
id: is-01m5pg1gyc2xjj54pjyqcp530z
title: "PR #788 (merge): address review A (A1-A9), update think-lsam, merge"
kind: task
status: in_progress
priority: 1
version: 3
delegate: c-fix-788-1024
labels: []
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
hold: null
hold_until: null
created_at: 2026-10-24T08:22:09.100Z
updated_at: 2026-10-24T08:56:56.214Z
started_at: 2026-10-24T08:22:16.137Z
---

## Notes

2026-10-24 c-fix-788-1024: addressing review A on #788 (https://github.com/jlevy/squares/pull/788#issuecomment-6381675002), round 1, head 463f78d3f. Findings tracked here, one line each, since the brief scopes bead writes to think-xwwb and think-lsam (no child beads created):
- A1 (High) longest task's cause is news-cards.js refresh's per-card forced layout, not page size: PR body, plan dated line (plan-2026-10-23-news-pr-feed.md ~:1324), option 1 widened, think-lsam corrected.
- A2 (Medium) second layout shift from news-filters.js:160 revealing the filter bar: PR body and plan line.
- A3 (Medium) runway range 18-28 days to 600,000, 9-13 to 450,000; bytes --pace-days N and the room line's earliest story.
- A4 (Medium) load --markdown tables in a details block, from a re-run (runs 1 and 2's JSON were not retained).
- A5 (Low) brotli withheld on projected pages.
- A6 (Low) verdict: untimed runs, page errors and failed requests decide.
- A7 (Low) p90 by nearest rank, named.
- A8 (Low) bytes --markdown help text.
- A9 (Low) 1,005,302 row's fail mark.
- A10 (suggestion) verdict test reads the checker's own failure text.
Progress: main e5c1c64e3 merged (78e64e895); fixes 73b89cd1d (tool and tests) and 29b8eda2c (plan); pushed, head 29b8eda2c (ls-remote agrees). Third load run with two controls (project --without news-cards.js / news-filters.js), 175 navigations, 08:33-08:38Z, Chromium 151.0.7922.34 installed into the session scratch directory (the container had only build 1243). think-lsam description corrected and a note added. Local: 17 tests pass (9 fail on the round-1 tool); ruff, basedpyright clean on both files; packing-validate --edit 66/69 (type floor timed out at load 15-16; browser floor blocked by the shared node_modules lacking typescript-eslint; bead tree: 3 open beads under closed parents in the local tracker, not this branch's).
