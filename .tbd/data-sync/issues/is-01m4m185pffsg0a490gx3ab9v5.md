---
type: is
id: is-01m4m185pffsg0a490gx3ab9v5
title: Use Row drawing scale by default on both web Atlas surfaces
kind: task
status: in_progress
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-10-08-site-layout-and-navigation.md
delegate: codex@spud10
labels: []
dependencies: []
parent_id: is-01m4ewpe4eqqjvrq6henxdzkh9
hold: null
hold_until: null
created_at: 2026-10-10T23:09:27.630Z
updated_at: 2026-10-10T23:23:00.624Z
started_at: 2026-10-10T23:09:38.404Z
---
Make Row drawing scale the first-paint and mounted web default on homepage and dedicated Atlas. Preserve explicit Fixed/Global choices and reload/query semantics, scoped homepage controls, current complete-row visibility, persistent SVG links, shared animations and scientific exports. PDF default changes require separate owner clarification.

## Notes

Implementation frozen: Row is SSR/prepaint/mounted default on both web Atlas surfaces; explicit Fixed/Global round-trip and Row omission retained, scoped home geometry/query behavior unchanged. Measurement DEFAULT_SCALE and retained URL/bootstrap/browser oracles migrated. Atlas+forward Node44PASS; measurement query1PASS1.90s; overview tsc exit0; scoped Ruff/BiomePASS. Selected index/atlas publication preserved325case/131result files, no PDF writes. Corrected HTTP proof is vn8n-live-default-proof-confirmed.log: each page has one Row grid and selected Row tab, current embed source and served atlas-view bytes equal current source. Earlier tabindex/import diagnostics failed and are not pass evidence. CLI opened http://127.0.0.1:8766/. Native browser augmentation pending final CI; no extra matrix. Keep open pending exact-head validation.
