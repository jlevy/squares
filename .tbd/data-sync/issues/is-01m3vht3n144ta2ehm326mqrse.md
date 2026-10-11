---
type: is
id: is-01m3vht3n144ta2ehm326mqrse
title: "Results tables at 1024 and 768: decide between sideways scroll and a narrower layout"
kind: task
status: open
priority: 3
version: 3
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-01T10:57:51.721Z
updated_at: 2026-10-01T17:02:14.844Z
---
From the table agent's report, 2026-10-01: with six columns the tables still scroll sideways at 1024 (18 px on the homepage, 63 px on the Results page) and at 768 (274 and 319 px), less than before. Result is held to 411 px by four unbreakable formulas and Credit has an 11.5rem floor. Options: let long formulas break or scroll inside their cell, switch to the card layout below about 1100 px, or accept the scroll. Also: at 1280 the columns use 1006 of 1104 px, so a result with a formula about 98 px wider than today's longest fails test_site_result_columns; and on a phone T-061's summary wraps so a line starts with a comma.

## Notes

Being done under think-y6js (2026-10-01): Result narrower with formulas that break, n wider; the agent reports sideways scroll at 1024 and 768 before and after.
