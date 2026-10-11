---
type: is
id: is-01m4m3jy5t5t9xejnptgqz053t
title: Remove the Atlas introduction and promote the Frontier Survey heading
kind: task
status: in_progress
priority: 2
version: 4
spec_path: docs/project/specs/active/plan-2026-10-08-site-layout-and-navigation.md
delegate: codex@spud10
labels: []
dependencies: []
parent_id: is-01m4ewpe4eqqjvrq6henxdzkh9
hold: null
hold_until: null
created_at: 2026-10-10T23:50:17.527Z
updated_at: 2026-10-11T00:12:44.629Z
started_at: 2026-10-10T23:50:55.275Z
---
Remove the introductory paragraph under The Atlas of Square Packings. Render The Frontier Survey as an H1 with the shared site-title class, preserving its canonical and legacy anchors, graphics, controls, and survey prose/table. Repair the stale raw poster image assertion without duplicating the adjacent hashed-image contract. Verify affected Home/Atlas assertions and refresh only the local Atlas page without pruning existing case or result records.

## Notes

The requested H1 Best Known Results for n ≤ 324 is immediately above the full Atlas survey table. It uses an italic n and Unicode ≤ rather than literal TeX in raw HTML. The shared Survey H1 and removal of introductory prose are implemented; focused heading, download, and recency checks plus preview publication are being finalized. Root Atlas browser accessibility checks pass: 4 tests, 53.53 seconds, with all no-star/no-layer assertions retained and recent labels derived from the registry.

Final source is frozen and the sixteen owned files are staged. Existing heading/download/native-math checks pass: 3 tests in 30.21 seconds. Scoped Ruff formatting/lint and BasedPyright pass (13 Python files; 0 errors/warnings/notes). Full maintained pages+Workbench producer refreshed all 325 case and 131 result HTML files. The four paper HTML/Markdown pairs were refreshed without generating PDFs. Five latest core pages, current eight canonical Atlas exports and compatibility copies were published; private review copies were removed from the publication root. Selected-producer publication postflight passes 6579/6579. Complete-assembly check only reports six intentionally omitted paper PDFs/aliases. HTTP proof confirms all three Atlas H1s, no raw TeX in the bounds heading, no moved links, canonical dated download, and current full7497×5361 PNG bytes (hash6ecb…). Final proof: scratch/077n-7j48-live-proof-final.log and .json; actual Home/Atlas light/dark labels are red for recent cases and neutral for historical cases. No commit/push; exact-head CI pending; bead stays open.
