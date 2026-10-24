---
type: is
id: is-01m5pn385t6saqvecp4w6nbp0e
title: "PR #736 (merge): follow-up review C of review B's fixes (c0ce843f9) and the main merges since 17a264be0"
kind: task
status: in_progress
priority: 1
version: 3
delegate: c-rev-736c-1024
labels: []
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
hold: null
hold_until: null
created_at: 2026-10-24T09:50:28.538Z
updated_at: 2026-10-24T10:31:32.496Z
started_at: 2026-10-24T09:50:36.439Z
---

## Notes

2026-10-24 c-rev-736c-1024: Review C (follow-up, round 4) published at head 8e3692a31, base b2ea7b09c: https://github.com/jlevy/squares/pull/736#issuecomment-6383128770. Verdict: approve. Findings: C1 (Low) NEWS_BOX_BYTES comment stale, box fragment 55,692 of 64,000 (worst case of heaviest three per level 59,874); C2 (suggestion) think-aqv8's last note still calls the 30-day rule current. B1-B5 hold; B2 test fails with the guard removed; landings.yaml re-derived from main's history, 70 houses and 36 sources, 0 differences; builds at head and main: 710 of 711 pages identical, index.html 579,134 vs 482,299. Tests: 698 passed plus 32 in Chromium.
