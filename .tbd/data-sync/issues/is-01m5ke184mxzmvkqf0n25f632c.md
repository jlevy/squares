---
type: is
id: is-01m5ke184mxzmvkqf0n25f632c
title: Align News Reset Filters text with the item tally at the right edge
kind: task
status: closed
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-10-22-site-navigation.md
delegate: site-followups-ui
labels: []
dependencies: []
parent_id: is-01m5jnsqdwj3t8m7hkbx6mr1m2
hold: null
hold_until: null
created_at: 2026-10-23T03:49:19.636Z
updated_at: 2026-10-23T04:17:29.591Z
started_at: 2026-10-23T03:49:27.528Z
closed_at: 2026-10-23T04:17:29.590Z
close_reason: "Implemented in ab238b2f73e60dbe331b2c22e94165e8083de41b, https://github.com/jlevy/squares/pull/743. The shared News Reset Filters rule now sets padding-inline-end: 0, aligning the visible right edge while retaining the remaining shared padding, placement, hover and focus rules. Scoped Ruff/Biome and diff whitespace checks passed. This is a localized reversible presentation fix; no separate literal CSS-value test was added. Implementation complete; no hosted CI or deployment claim."
resolution: null
duplicate_of: null
---
On News, remove right/end padding from right-aligned Reset Filters button so its visible text edge aligns with item tally below. Preserve same filter row placement, pointer target/focus outline, mobile wrapping and shared button tokens except intentional edge-alignment modifier.
