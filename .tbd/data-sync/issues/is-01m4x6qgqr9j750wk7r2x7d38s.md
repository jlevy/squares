---
type: is
id: is-01m4x6qgqr9j750wk7r2x7d38s
title: "Results page: a Chromium layout test for the overview's two sections at 390 and 1280"
kind: task
status: open
priority: 3
version: 1
labels: []
dependencies: []
created_at: 2026-10-14T12:38:23.224Z
updated_at: 2026-10-14T12:38:23.224Z
---
Deferred from #514 (think-2z22), review A finding A7. The spec relies on screenshots for the layout of "Added in the Last Seven Days" and the weekly rollup. Add the sections to the Chromium layout lane (SITE_LAYOUT_TESTS): no horizontal overflow at 390 and 1280 in light and dark, the newest day's first entry on the first screen, and the day and week disclosures opening without moving the table.
