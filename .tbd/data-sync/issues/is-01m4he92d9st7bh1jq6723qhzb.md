---
type: is
id: is-01m4he92d9st7bh1jq6723qhzb
title: Fit redesigned atlas figure within the n11 paper page
kind: bug
status: in_progress
priority: 1
version: 2
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4h9s465x7mphy1xxkmdyqc9
hold: null
hold_until: null
created_at: 2026-10-09T22:59:25.150Z
updated_at: 2026-10-09T22:59:50.498Z
started_at: 2026-10-09T22:59:50.496Z
---
The canonical 100-packing poster is now2260x4023, but the n11 explainer print CSS forces six-inch image width with no height cap. Current production PDF has24pages with blank page6 and atlas+caption split over7-8; isolated prior Figure2 asset/dimensions control restores22pages with all current prose unchanged. Add a measured paper-only figure fit preserving full100packings, current standalone posters, caption and22-page contract; verify production font guard and page content.
