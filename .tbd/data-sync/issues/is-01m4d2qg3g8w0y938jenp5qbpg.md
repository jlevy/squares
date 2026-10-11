---
type: is
id: is-01m4d2qg3g8w0y938jenp5qbpg
title: Build a searchable exact-values browser with paged coefficient views
kind: task
status: closed
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-10-06-exact-side-values.md
delegate: codex-web-browser
labels: []
dependencies: []
parent_id: is-01m4d2n7hjcxy6nh0wkvy8bpmj
hold: null
hold_until: null
created_at: 2026-10-08T06:20:37.360Z
updated_at: 2026-10-08T07:53:39.035Z
started_at: 2026-10-08T06:20:40.325Z
closed_at: 2026-10-08T07:53:39.035Z
close_reason: null
resolution: null
duplicate_of: null
---
Own browser shell/CSS, overview/exact-side-values.js, JS typings/tests and browser-floor config if needed. Search/filter/page current and historical values separately; load metadata and coefficients on demand; show original claims, source-invalid labels, source/attribution and routes; never coerce coefficient strings to JavaScript Number. Coordinate schema with renderer; no shared site builds or commits.

## Notes

Delivered in 6900cb94207eeea589dbcf3cb8c75a45eabbb633 and PR435. Search n:83, current/historical and kind/status filters, 25-entry pages, lazy metadata, 12-coefficient pages, full JSON download/copy with manual fallback, bounded retries and stale-result guards. Five required Chromium controls passed; browser Biome/ESLint/tsc floor passed with the JS actually included. Independent Astra controls preserve n83 arbitrary-precision strings and historical invalidity flags. Parent think-mo36 owns remaining hosted integration.
