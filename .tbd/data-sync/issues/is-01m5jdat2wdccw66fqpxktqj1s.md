---
type: is
id: is-01m5jdat2wdccw66fqpxktqj1s
title: Add standalone-page expand links to shared popover headers
kind: task
status: in_progress
priority: 2
version: 5
spec_path: docs/project/specs/active/plan-2026-10-10-contributor-profiles.md
delegate: upstream_integration
labels: []
dependencies: []
parent_id: is-01m5jct23n8s7fj3ydf94n0yhv
hold: null
hold_until: null
created_at: 2026-10-22T18:17:49.915Z
updated_at: 2026-10-22T18:43:19.595Z
started_at: 2026-10-22T18:18:20.287Z
---
Add a Lucide expand icon immediately before the close control in every shared popover with a standalone page, using the same target as its bottom full-record action. Preserve bottom CTA, keyboard and focus behavior, mobile targets and non-navigable overlays. Own shared popover JavaScript/templates, popover-only CSS and the popover design-contract section; coordinate disjoint News/document edits. Focused behavioral coverage; no commit or push.

## Notes

Implemented the shared maximize link immediately before Close for row, card, case and profile popovers. Header and bottom actions share an escaped destination and accessible label; no-page and fragment-only overlays retain Close alone. Dynamic case/profile replacement updates both links, keeps native navigation, and preserves Close focus. Shared controls use equal 44px targets, equal Lucide icon sizing and mobile clearance; case controls remain sticky.

Row/card glyphs now reference the existing KPress maximize/x sprite through the shared helper option, avoiding repeated inline paths. Lightweight standalone case/profile shells retain the same canonical inline glyphs. Source is frozen for the parent render; no commit or push was made. Results byte/timing evidence and any budget decision belong to domain_squares.

Validation: pytest tests/test_site_popover_controls.py --maxfail=1 --tb=short: 9 passed in 8.33s, including native link navigation, target equality, focus, no-page omission and 320/390/1280 layouts with nonempty rendered SVG glyphs. check_no_embedded_js --since origin/main: 2789 Python files, zero allowlisted sites, none added. Ruff, targeted Biome, tsconfig.overview, tsconfig.probes and diff whitespace checks pass. Existing row-popover Node suite previously passed 35 tests. Parent-requested packing-validate --only 'browser floor' passed both selected steps in 83.92s, including 56 browser-floor liveness tests; this is a subset, not the full gate. Log: /Volumes/spud-ext2/agent-scratch/about-profiles-20261020/popover-controls-browser-floor.log. Keep open for parent integration review and aggregate gates.
