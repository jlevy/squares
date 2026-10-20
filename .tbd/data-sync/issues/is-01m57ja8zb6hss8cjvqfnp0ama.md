---
type: is
id: is-01m57ja8zb6hss8cjvqfnp0ama
title: "PR #665 A4: reduce expanded T-174 result payload"
kind: bug
status: in_progress
priority: 2
version: 4
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m57j9xsga57szgfah5ex2bcd
hold: null
hold_until: null
created_at: 2026-10-18T13:13:16.522Z
updated_at: 2026-10-18T14:48:16.504Z
started_at: 2026-10-18T13:13:25.548Z
---
Medium; review A https://github.com/jlevy/squares/pull/665#pullrequestreview-5562201404. packing/frontier/results.yaml:21986 expands t-174.html to 335153 bytes vs 300000 budget. Reduce repeated renderer payload with behavior preserved, measure overview.

## Notes

Fixed in391fdc594: native repeated count labels preserve every detail through prose_html; full T-174 result page335153→249465 bytes against unchanged300000 budget. Payload regression passes. Generated comparison of all4 papers yields8 byte-equal HTML/Markdown files and linked assets before/after provisional site cut; noPDF rebuilt. Fresh exact-path no-public-change declarations and v0.7.26 site ownership pass release-impact at2890be7fa. Full overview/Pages CI and disposition pending.
