---
type: is
id: is-01m4m6yg8cnpm1pz0jsg77jv2n
title: Diagnose initial-fragment Headroom startup race
kind: task
status: closed
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-10-08-site-layout-and-navigation.md
delegate: codex@spud10
labels: []
dependencies: []
parent_id: is-01m4m588mffw9ac4ssy5qa9hhd
hold: null
hold_until: null
created_at: 2026-10-11T00:49:02.219Z
updated_at: 2026-10-11T00:52:13.497Z
started_at: 2026-10-11T00:49:35.832Z
closed_at: 2026-10-11T00:52:13.495Z
close_reason: "Confirmed production initial-fragment race with a parser-gated regression: before fix 1 failed in 4.69s. Parent expanded ownership to headroom.js; reset on every pageshow preserves restored history and initializes late native fragment arrivals. Both fragment nodes PASS 4.98s; whole Headroom module 17 PASS 14.34s (TMPDIR/headroom-module-fixed.log). Scoped Ruff lint/format, Biome, overview TypeScript, diff check PASS. No commit or push."
resolution: null
duplicate_of: null
---
Own test_site_headroom.py and dedicated probes. Diagnose hosted failure where initial fragment navigation leaves header hidden; repair only a stale or timing-sensitive oracle, otherwise report product defect to root for shared-source fix. Run focused browser case and the Headroom module. No commit or push.
