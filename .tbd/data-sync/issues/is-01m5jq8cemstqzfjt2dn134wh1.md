---
type: is
id: is-01m5jq8cemstqzfjt2dn134wh1
title: Use diagonal outward arrows for the shared expand action
kind: task
status: closed
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-10-22-site-navigation.md
delegate: navigation-components
labels: []
dependencies: []
parent_id: is-01m5jnsqdwj3t8m7hkbx6mr1m2
hold: null
hold_until: null
created_at: 2026-10-22T21:11:16.179Z
updated_at: 2026-10-22T21:53:55.141Z
started_at: 2026-10-22T21:28:24.728Z
closed_at: 2026-10-22T21:53:55.141Z
close_reason: "Implemented shared five-tab disclosures, ancestor navigation and matching breadcrumb data; responsive prose popover widths and shared diagonal maximize-2 controls are documented. Focused verification: component suite 9 passed, existing overview navigation 34 passed, geometry 2 passed, long-profile controls at 320px passed, final semantic breadcrumb selector 1 passed in 24.17s. Ruff, helper types, JS types, Biome and diff checks passed. Implementation recorded in coordinator commit 09829990c3503e69b1f307b3b9269c0865b98a88 plus reviewed spacing corrections in the next coordinator checkpoint."
resolution: null
duplicate_of: null
---
Follow-up PR after #733: replace the ambiguous border-shaped expand glyph with a suitable existing Lucide diagonal outward-arrows icon, or coherent custom equivalent if needed. Retain shared icon sizing, accessible Open full page label, and identical header/footer destination. Apply wherever an overlay opens a full page and document the convention.
