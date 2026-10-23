---
type: is
id: is-01m5kdx61fs83hcj366fcbptvp
title: Navigate person-name links directly to profile pages site-wide
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
created_at: 2026-10-23T03:47:06.414Z
updated_at: 2026-10-23T04:17:29.263Z
started_at: 2026-10-23T03:47:19.458Z
closed_at: 2026-10-23T04:17:29.262Z
close_reason: Completed in ab238b2f73e60dbe331b2c22e94165e8083de41b, https://github.com/jlevy/squares/pull/743. Coordinator removed the global contributor popover controller/shell so person-name links use native profile navigation across pages and open retained panels; generated-profile expectations and shared design notes were updated. Coordinator reported 24 native profile/retained-popover tests passing. Shared popover controls already render identical diagonal outward maximize-2 paths in sprite and inline modes; the focused control test verifies the glyph, accessible action, and destination, so no extra glyph mutation was needed. Implementation/audit complete; hosted CI and deployment remain pending coordinator work.
resolution: null
duplicate_of: null
---
Person-name links on About and all other pages should navigate directly to the individual profile, never open a profile popover. Preserve useful canonical hrefs, surname/full-name context rules, keyboard and modified-click behavior. Remove profile-specific interception consistently rather than per-page exceptions; result/case popovers remain.
