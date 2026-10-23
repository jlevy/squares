---
type: is
id: is-01m5jqhrkzpwj9djae1zf261c7
title: Implement shared site navigation, dropdowns, and breadcrumb hierarchy
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
created_at: 2026-10-22T21:16:23.549Z
updated_at: 2026-10-22T21:53:55.087Z
started_at: 2026-10-22T21:28:24.696Z
closed_at: 2026-10-22T21:53:55.080Z
close_reason: "Implemented shared five-tab disclosures, ancestor navigation and matching breadcrumb data; responsive prose popover widths and shared diagonal maximize-2 controls are documented. Focused verification: component suite 9 passed, existing overview navigation 34 passed, geometry 2 passed, long-profile controls at 320px passed, final semantic breadcrumb selector 1 passed in 24.17s. Ruff, helper types, JS types, Biome and diff checks passed. Implementation recorded in coordinator commit 09829990c3503e69b1f307b3b9269c0865b98a88 plus reviewed spacing corrections in the next coordinator checkpoint."
resolution: null
duplicate_of: null
---
After PR733 merges, implement Overview, News, Results, Learn, About in that order with shared disclosure menus for Results/Learn/About. One declared hierarchy drives current-parent state and breadcrumbs across all producers. Follow existing design tokens, keyboard/touch/no-JS behavior and document the component in the existing design system.
