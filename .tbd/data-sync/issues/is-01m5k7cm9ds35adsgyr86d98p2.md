---
type: is
id: is-01m5k7cm9ds35adsgyr86d98p2
title: Add shared source actions to repository document pages
kind: feature
status: closed
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-10-22-site-navigation.md
delegate: frontier-split
labels: []
dependencies: []
parent_id: is-01m5jnsqdwj3t8m7hkbx6mr1m2
hold: null
hold_until: null
created_at: 2026-10-23T01:53:12.480Z
updated_at: 2026-10-23T02:15:06.610Z
started_at: 2026-10-23T01:54:04.270Z
closed_at: 2026-10-23T02:15:06.609Z
close_reason: "Completed in coordinator-published cf951e550 and 164e5381a. All seven metadata-backed repository documents and every derived Synopsis chapter share the existing paper source-action helper with actual GitHub and raw Markdown paths and no invented PDF links. Shared first-title CSS preserves the normal page-top gap after controls. uv run --frozen --all-extras --group dev pytest tests/test_site_frontier_split.py tests/test_site_source_actions.py -q: 9 passed in 40.90s, including desktop 1280px and mobile 390px visibility, viewport fit, and first-H1 spacing. Ruff and Biome passed; plan and design updated."
resolution: null
duplicate_of: null
---
Systematically add the existing paper-style upper-right GitHub original-source action and optional raw Markdown action to every site page that hosts a real repository document. Derive destinations from shared source metadata with correct repository-relative source paths; exclude generated data views and pages without a real source document. Read-only inventory/design first; do not edit source until the coordinator merges origin/main.
